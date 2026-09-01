from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from statistics import mean, median, stdev

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.inventory_forecasting.autogluon_runner import (
    run_autogluon_backtest,
    summarize_model_stability,
    summarize_prediction_rows,
)
from src.inventory_forecasting.metrics import mase

DATASET = Path("datasets/dataset-1000-com-preco-promocional-e-renovacao-estoque.csv")
OUTPUT_DIR = Path("results/autogluon")
FOLD_DIR = Path("artifacts/autogluon_multifold_data")


def reconcile(result):
    import pandas as pd

    pred = result["predictions"].reset_index().copy()
    id_col = "item_id" if "item_id" in pred.columns else "ID_PRODUTO"
    time_col = "timestamp" if "timestamp" in pred.columns else "DATA_EVENTO"
    pred = pred.rename(columns={id_col: "ID_PRODUTO", time_col: "DATA_EVENTO", "0.1": "P10", "0.5": "P50", "0.9": "P90"})
    pred["ID_PRODUTO"] = pred["ID_PRODUTO"].astype(str)
    pred["DATA_EVENTO"] = pd.to_datetime(pred["DATA_EVENTO"])
    holdout = result["holdout"].copy()
    holdout["ID_PRODUTO"] = holdout["ID_PRODUTO"].astype(str)
    holdout["DATA_EVENTO"] = pd.to_datetime(holdout["DATA_EVENTO"])
    merged = pred.merge(
        holdout[["ID_PRODUTO", "DATA_EVENTO", "QUANTIDADE_ESTOQUE"]],
        on=["ID_PRODUTO", "DATA_EVENTO"],
        validate="one_to_one",
    ).rename(columns={"QUANTIDADE_ESTOQUE": "actual"})
    if len(merged) != len(holdout):
        raise RuntimeError("Reconciliação de fold incompleta")
    return merged[["ID_PRODUTO", "DATA_EVENTO", "actual", "mean", "P10", "P50", "P90"]].copy()


def _dataset_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa 3 folds rolling-origin/expanding-window com AutoGluon.")
    parser.add_argument("--time-limit", type=int, default=180)
    parser.add_argument("--presets", default="medium_quality")
    args = parser.parse_args()

    import pandas as pd

    frame = pd.read_csv(DATASET, parse_dates=["DATA_EVENTO"]).sort_values(["ID_PRODUTO", "DATA_EVENTO"])
    counts = frame.groupby("ID_PRODUTO").size()
    if counts.nunique() != 1 or int(counts.iloc[0]) != 40:
        raise RuntimeError("O protocolo multifold atual exige 40 observações por SKU")

    # 3 non-overlapping 7-day test windows -> train sizes 19, 26, 33.
    fold_end_sizes = [26, 33, 40]
    FOLD_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    leaderboard_rows = []
    metric_rows = []
    prediction_frames = []
    calibration_rows = []
    selected_models = []

    for fold, end_size in enumerate(fold_end_sizes, start=1):
        fold_frame = frame.groupby("ID_PRODUTO", group_keys=False, sort=True).head(end_size).copy()
        fold_csv = FOLD_DIR / f"fold_{fold}.csv"
        fold_frame.to_csv(fold_csv, index=False)
        result = run_autogluon_backtest(
            csv_path=str(fold_csv),
            model_path=f"artifacts/autogluon_multifold/fold_{fold}",
            presets=args.presets,
            time_limit=args.time_limit,
        )
        selected_model = str(result["predictor"].model_best)
        selected_models.append(selected_model)

        leaderboard = result["leaderboard"].copy()
        leaderboard.insert(0, "fold", fold)
        leaderboard["selected_by_validation"] = leaderboard["model"].astype(str) == selected_model
        leaderboard_rows.append(leaderboard)

        reconciled = reconcile(result)
        reconciled.insert(0, "fold", fold)
        reconciled.insert(1, "selected_model", selected_model)
        reconciled["horizon_step"] = reconciled.groupby("ID_PRODUTO", sort=True).cumcount() + 1
        prediction_frames.append(reconciled)
        metrics = summarize_prediction_rows(reconciled.to_dict(orient="records"))
        metric_rows.append({"fold": fold, "train_points_per_sku": end_size - 7, "selected_model": selected_model, **metrics})

        train_frame = fold_frame.groupby("ID_PRODUTO", group_keys=False, sort=True).head(end_size - 7)
        for sku, sku_frame in reconciled.groupby("ID_PRODUTO", sort=True):
            sku_summary = summarize_prediction_rows(sku_frame.to_dict(orient="records"))
            insample = train_frame.loc[train_frame["ID_PRODUTO"].astype(str) == str(sku), "QUANTIDADE_ESTOQUE"].astype(float).tolist()
            actual = sku_frame["actual"].astype(float).tolist()
            point = sku_frame["mean"].astype(float).tolist()
            sku_summary["MACRO_MASE"] = mase(actual, point, insample)
            sku_summary["BIAS"] = mean(p - a for a, p in zip(actual, point))
            calibration_rows.append({"fold": fold, "ID_PRODUTO": sku, **sku_summary})

    leaderboard_all = pd.concat(leaderboard_rows, ignore_index=True)
    metrics_df = pd.DataFrame(metric_rows)
    predictions_df = pd.concat(prediction_frames, ignore_index=True)
    calibration_df = pd.DataFrame(calibration_rows)

    stability_rows, stability_summary = summarize_model_stability(leaderboard_all.to_dict(orient="records"))
    stability_df = pd.DataFrame(stability_rows)

    leaderboard_all.to_csv(OUTPUT_DIR / "multifold_leaderboard.csv", index=False)
    metrics_df.to_csv(OUTPUT_DIR / "multifold_metrics.csv", index=False)
    predictions_df.to_csv(OUTPUT_DIR / "multifold_predictions.csv", index=False)
    calibration_df.to_csv(OUTPUT_DIR / "multifold_calibration_by_sku.csv", index=False)
    stability_df.to_csv(OUTPUT_DIR / "model_stability.csv", index=False)

    metric_names = [column for column in metrics_df.columns if column not in {"fold", "train_points_per_sku", "selected_model"}]
    summary = {"folds": len(metrics_df)}
    for metric in metric_names:
        values = [float(v) for v in metrics_df[metric].tolist()]
        summary[f"{metric}_mean"] = mean(values)
        summary[f"{metric}_median"] = median(values)
        summary[f"{metric}_stdev"] = stdev(values) if len(values) > 1 else 0.0
    summary.update(stability_summary)
    summary["selected_models"] = "|".join(selected_models)
    pd.DataFrame([summary]).to_csv(OUTPUT_DIR / "multifold_summary.csv", index=False)

    # Aggregate SKU diagnostics across the three external folds.
    sku_rows = []
    for sku, sku_frame in calibration_df.groupby("ID_PRODUTO", sort=True):
        sku_rows.append(
            {
                "ID_PRODUTO": sku,
                "folds": len(sku_frame),
                "MAE_mean": sku_frame["MAE"].mean(),
                "WAPE_mean": sku_frame["WAPE"].mean(),
                "MACRO_MASE_mean": sku_frame["MACRO_MASE"].mean(),
                "WQL_mean": sku_frame["WQL"].mean(),
                "P10_P90_COVERAGE_mean": sku_frame["P10_P90_COVERAGE"].mean(),
                "MEAN_INTERVAL_WIDTH_mean": sku_frame["MEAN_INTERVAL_WIDTH"].mean(),
                "BIAS_mean": sku_frame["BIAS"].mean(),
                "best_fold_by_MAE": int(sku_frame.loc[sku_frame["MAE"].idxmin(), "fold"]),
                "worst_fold_by_MAE": int(sku_frame.loc[sku_frame["MAE"].idxmax(), "fold"]),
            }
        )
    pd.DataFrame(sku_rows).to_csv(OUTPUT_DIR / "sku_metrics.csv", index=False)

    # Exploratory calibration by forecast horizon (h=1..7).
    horizon_rows = []
    for horizon, hframe in predictions_df.groupby("horizon_step", sort=True):
        horizon_rows.append({"horizon_step": int(horizon), **summarize_prediction_rows(hframe.to_dict(orient="records"))})
    pd.DataFrame(horizon_rows).to_csv(OUTPUT_DIR / "horizon_calibration.csv", index=False)

    manifest = {
        "protocol": "external rolling-origin expanding-window",
        "folds": 3,
        "horizon": 7,
        "train_points_per_sku": [19, 26, 33],
        "test_windows_non_overlapping": True,
        "dataset": str(DATASET),
        "dataset_sha256": _dataset_sha256(DATASET),
        "model_selection": "AutoGluon validation only; external test holdout not used to choose model",
        "presets": args.presets,
        "time_limit_seconds_per_fold": args.time_limit,
        "selected_models": selected_models,
        "selection_stability": stability_summary["selection_stability"],
        "external_test_stability": stability_summary["external_test_stability"],
        "weighted_ensemble_external_win_rate": stability_summary["weighted_ensemble_external_win_rate"],
        "artifacts": [
            "multifold_leaderboard.csv",
            "multifold_metrics.csv",
            "multifold_predictions.csv",
            "multifold_calibration_by_sku.csv",
            "multifold_summary.csv",
            "model_stability.csv",
            "sku_metrics.csv",
            "horizon_calibration.csv",
        ],
    }
    (OUTPUT_DIR / "multifold_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("=== AutoGluon rolling-origin ===")
    print(f"Selected by validation: {selected_models}")
    print(f"Selection stability: {stability_summary['selection_stability']}")
    print(f"External test stability: {stability_summary['external_test_stability']}")
    print(f"WeightedEnsemble external wins: {stability_summary['weighted_ensemble_external_wins']}/3")
    print(metrics_df.to_string(index=False))
    print(stability_df.to_string(index=False))
    print(f"Predictions: {len(predictions_df)}")


if __name__ == "__main__":
    main()
