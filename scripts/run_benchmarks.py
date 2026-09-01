from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.inventory_forecasting.benchmark import run_benchmarks, run_benchmarks_multifold
from src.inventory_forecasting.data import load_dataset

METRICS_PATH = Path("results/metrics/benchmark_metrics.csv")
PREDICTIONS_PATH = Path("results/predictions/benchmark_holdout_predictions.csv")
LEADERBOARD_PATH = Path("results/exports/benchmark_leaderboard.csv")
MULTIFOLD_METRICS_PATH = Path("results/metrics/benchmark_multifold_metrics.csv")
MULTIFOLD_SUMMARY_PATH = Path("results/metrics/benchmark_multifold_summary.csv")
MULTIFOLD_PREDICTIONS_PATH = Path("results/predictions/benchmark_multifold_predictions.csv")


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Nenhum dado para exportar em {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def rounded_single(leaderboard: list[dict]) -> list[dict]:
    rows = []
    for row in leaderboard:
        rows.append(
            {
                "rank": row["rank"],
                "model": row["model"],
                "MAE": f'{row["MAE"]:.6f}',
                "RMSE": f'{row["RMSE"]:.6f}',
                "WAPE": f'{row["WAPE"]:.6f}',
                "MAPE": f'{row["MAPE"]:.6f}',
                "MACRO_MASE": f'{row["MACRO_MASE"]:.6f}',
                "WQL": f'{row["WQL"]:.6f}',
                "P10_P90_COVERAGE": f'{row["P10_P90_COVERAGE"]:.6f}',
                "MEAN_INTERVAL_WIDTH": f'{row["MEAN_INTERVAL_WIDTH"]:.6f}',
                "QUANTILE_CROSSINGS": int(row["QUANTILE_CROSSINGS"]),
            }
        )
    return rows


def main() -> None:
    rows = load_dataset()
    leaderboard, predictions = run_benchmarks(rows, horizon=7)
    rounded = rounded_single(leaderboard)

    write_csv(METRICS_PATH, rounded)
    write_csv(LEADERBOARD_PATH, rounded)
    write_csv(PREDICTIONS_PATH, predictions)

    fold_metrics, multifold_summary, multifold_predictions = run_benchmarks_multifold(
        rows,
        horizon=7,
        n_folds=3,
        min_train_size=14,
    )
    write_csv(MULTIFOLD_METRICS_PATH, fold_metrics)
    write_csv(MULTIFOLD_SUMMARY_PATH, multifold_summary)
    write_csv(MULTIFOLD_PREDICTIONS_PATH, multifold_predictions)

    print("=== Benchmark leaderboard (holdout final: 7 dias por SKU) ===")
    for row in rounded:
        print(
            f'#{row["rank"]} {row["model"]}: '
            f'MAE={row["MAE"]} RMSE={row["RMSE"]} WAPE={row["WAPE"]} '
            f'MAPE={row["MAPE"]} MACRO_MASE={row["MACRO_MASE"]} WQL={row["WQL"]}'
        )

    print("=== Rolling-origin benchmark summary (3 folds, expanding window) ===")
    for row in multifold_summary:
        print(
            f'#{row["rank"]} {row["model"]}: '
            f'WAPE_mean={float(row["WAPE_mean"]):.6f} '
            f'RMSE_mean={float(row["RMSE_mean"]):.6f} '
            f'MACRO_MASE_mean={float(row["MACRO_MASE_mean"]):.6f}'
        )
    print(f"Holdout final: {len(predictions)} previsões")
    print(f"Multi-window: {len(multifold_predictions)} previsões")


if __name__ == "__main__":
    main()
