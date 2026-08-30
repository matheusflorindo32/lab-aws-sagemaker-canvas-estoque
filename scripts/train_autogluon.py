from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.inventory_forecasting.autogluon_runner import run_autogluon_backtest, summarize_prediction_rows

DATASET = Path("datasets/dataset-1000-com-preco-promocional-e-renovacao-estoque.csv")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def reconciled_prediction_frame(result):
    import pandas as pd

    pred = result["predictions"].reset_index().copy()
    id_col = "item_id" if "item_id" in pred.columns else "ID_PRODUTO"
    time_col = "timestamp" if "timestamp" in pred.columns else "DATA_EVENTO"
    pred = pred.rename(
        columns={
            id_col: "ID_PRODUTO",
            time_col: "DATA_EVENTO",
            "0.1": "P10",
            "0.5": "P50",
            "0.9": "P90",
        }
    )
    pred["ID_PRODUTO"] = pred["ID_PRODUTO"].astype(str)
    pred["DATA_EVENTO"] = pd.to_datetime(pred["DATA_EVENTO"])

    holdout = result["holdout"].copy()
    holdout["ID_PRODUTO"] = holdout["ID_PRODUTO"].astype(str)
    holdout["DATA_EVENTO"] = pd.to_datetime(holdout["DATA_EVENTO"])
    merged = pred.merge(
        holdout[["ID_PRODUTO", "DATA_EVENTO", "QUANTIDADE_ESTOQUE"]],
        on=["ID_PRODUTO", "DATA_EVENTO"],
        how="inner",
        validate="one_to_one",
    ).rename(columns={"QUANTIDADE_ESTOQUE": "actual"})
    required = ["ID_PRODUTO", "DATA_EVENTO", "actual", "mean", "P10", "P50", "P90"]
    if len(merged) != len(holdout):
        raise RuntimeError(f"Reconciliação incompleta: forecasts={len(merged)} holdout={len(holdout)}")
    return merged[required].sort_values(["ID_PRODUTO", "DATA_EVENTO"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Treina e avalia AutoGluon TimeSeries no holdout temporal de 7 dias.")
    parser.add_argument("--time-limit", type=int, default=300, help="Limite de treino em segundos.")
    parser.add_argument("--presets", default="medium_quality", help="Preset do AutoGluon TimeSeries.")
    args = parser.parse_args()

    result = run_autogluon_backtest(time_limit=args.time_limit, presets=args.presets)
    output_dir = Path("results/autogluon")
    output_dir.mkdir(parents=True, exist_ok=True)

    result["leaderboard"].to_csv(output_dir / "leaderboard.csv", index=False)
    result["feature_importance"].to_csv(output_dir / "feature_importance.csv")

    prediction_frame = reconciled_prediction_frame(result)
    prediction_frame.to_csv(output_dir / "holdout_predictions.csv", index=False)
    prediction_rows = prediction_frame.to_dict(orient="records")
    metrics = summarize_prediction_rows(prediction_rows)
    model_name = str(result["predictor"].model_best)

    import pandas as pd
    pd.DataFrame([{"model": model_name, **metrics}]).to_csv(output_dir / "metrics_summary.csv", index=False)

    calibration_rows = []
    for sku, sku_frame in prediction_frame.groupby("ID_PRODUTO", sort=True):
        calibration_rows.append({"ID_PRODUTO": sku, **summarize_prediction_rows(sku_frame.to_dict(orient="records"))})
    pd.DataFrame(calibration_rows).to_csv(output_dir / "calibration_by_sku.csv", index=False)

    evaluation = result["evaluation"]
    with (output_dir / "evaluation.txt").open("w", encoding="utf-8") as handle:
        for key, value in evaluation.items():
            handle.write(f"{key}={value}\n")

    import autogluon
    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "dataset": str(DATASET),
        "dataset_sha256": sha256_file(DATASET),
        "python": platform.python_version(),
        "autogluon": autogluon.__version__,
        "presets": args.presets,
        "time_limit_seconds": args.time_limit,
        "config": result["config"],
        "best_model_validation": model_name,
        "holdout_rows": len(prediction_frame),
        "artifacts": [
            "leaderboard.csv",
            "holdout_predictions.csv",
            "metrics_summary.csv",
            "calibration_by_sku.csv",
            "feature_importance.csv",
            "evaluation.txt",
        ],
    }
    (output_dir / "experiment_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("=== AutoGluon TimeSeries ===")
    print(f"Configuração: {result['config']}")
    print(f"Best model (validation): {model_name}")
    for key, value in metrics.items():
        print(f"{key}={value}")
    print(f"Forecasts reconciliados: {len(prediction_frame)}")
    print(f"Artefatos exportados em: {output_dir}")


if __name__ == "__main__":
    main()
