from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from statistics import mean, median, stdev

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.inventory_forecasting.autogluon_runner import run_autogluon_backtest, summarize_prediction_rows

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
        prediction_frames.append(reconciled)
        metrics = summarize_prediction_rows(reconciled.to_dict(orient="records"))
        metric_rows.append({"fold": fold, "train_points_per_sku": end_size - 7, "selected_model": selected_model, **metrics})

        for sku, sku_frame in reconciled.groupby("ID_PRODUTO", sort=True):
            calibration_rows.append({"fold": fold, "ID_PRODUTO": sku, **summarize_prediction_rows(sku_frame.to_dict(orient="records"))})

    leaderboard_all = pd.concat(leaderboard_rows, ignore_index=True)
    metrics_df = pd.DataFrame(metric_rows)
    predictions_df = pd.concat(prediction_frames, ignore_index=True)
    calibration_df = pd.DataFrame(calibration_rows)

    leaderboard_all.to_csv(OUTPUT_DIR / "multifold_leaderboard.csv", index=False)
    metrics_df.to_csv(OUTPUT_DIR / "multifold_metrics.csv", index=False)
    predictions_df.to_csv(OUTPUT_DIR / "multifold_predictions.csv", index=False)
    calibration_df.to_csv(OUTPUT_DIR / "multifold_calibration_by_sku.csv", index=False)

    metric_names = [column for column in metrics_df.columns if column not in {"fold", "train_points_per_sku", "selected_model"}]
    summary = {"folds": len(metrics_df)}
    for metric in metric_names:
        values = [float(v) for v in metrics_df[metric].tolist()]
        summary[f"{metric}_mean"] = mean(values)
        summary[f"{metric}_median"] = median(values)
        summary[f"{metric}_stdev"] = stdev(values) if len(values) > 1 else 0.0

    weighted_wins = sum(model == "WeightedEnsemble" for model in selected_models)
    if weighted_wins == len(selected_models):
        stability = "stable"
    elif weighted_wins >= 2:
        stability = "partially_stable"
    else:
        stability = "unstable"
    summary.update(
        {
            "selected_models": "|".join(selected_models),
            "weighted_ensemble_selected_folds": weighted_wins,
            "weighted_ensemble_stability": stability,
        }
    )
    pd.DataFrame([summary]).to_csv(OUTPUT_DIR / "multifold_summary.csv", index=False)

    manifest = {
        "protocol": "external rolling-origin expanding-window",
        "folds": 3,
        "horizon": 7,
        "train_points_per_sku": [19, 26, 33],
        "test_windows_non_overlapping": True,
        "model_selection": "AutoGluon validation only; test holdout not used to choose model",
        "presets": args.presets,
        "time_limit_seconds_per_fold": args.time_limit,
        "selected_models": selected_models,
        "weighted_ensemble_stability": stability,
        "artifacts": [
            "multifold_leaderboard.csv",
            "multifold_metrics.csv",
            "multifold_predictions.csv",
            "multifold_calibration_by_sku.csv",
            "multifold_summary.csv",
        ],
    }
    (OUTPUT_DIR / "multifold_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("=== AutoGluon rolling-origin ===")
    print(f"Selected models: {selected_models}")
    print(f"WeightedEnsemble stability: {stability} ({weighted_wins}/3 folds)")
    print(metrics_df.to_string(index=False))
    print(f"Predictions: {len(predictions_df)}")


if __name__ == "__main__":
    main()
