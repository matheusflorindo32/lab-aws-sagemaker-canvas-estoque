from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.inventory_forecasting.benchmark import run_benchmarks
from src.inventory_forecasting.data import load_dataset

METRICS_PATH = Path("results/metrics/benchmark_metrics.csv")
PREDICTIONS_PATH = Path("results/predictions/benchmark_holdout_predictions.csv")
LEADERBOARD_PATH = Path("results/exports/benchmark_leaderboard.csv")


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Nenhum dado para exportar em {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows = load_dataset()
    leaderboard, predictions = run_benchmarks(rows, horizon=7)

    rounded = []
    for row in leaderboard:
        rounded.append(
            {
                "rank": row["rank"],
                "model": row["model"],
                "MAE": f'{row["MAE"]:.6f}',
                "RMSE": f'{row["RMSE"]:.6f}',
                "WAPE": f'{row["WAPE"]:.6f}',
                "MAPE": f'{row["MAPE"]:.6f}',
                "MASE": f'{row["MASE"]:.6f}',
                "WQL": f'{row["WQL"]:.6f}',
            }
        )

    write_csv(METRICS_PATH, rounded)
    write_csv(LEADERBOARD_PATH, rounded)
    write_csv(PREDICTIONS_PATH, predictions)

    print("=== Benchmark leaderboard (holdout temporal: 7 dias por SKU) ===")
    for row in rounded:
        print(
            f'#{row["rank"]} {row["model"]}: '
            f'MAE={row["MAE"]} RMSE={row["RMSE"]} WAPE={row["WAPE"]} '
            f'MAPE={row["MAPE"]} MASE={row["MASE"]} WQL={row["WQL"]}'
        )
    print(f"Predições exportadas: {len(predictions)} linhas")
    print(f"Artefatos: {METRICS_PATH}, {PREDICTIONS_PATH}, {LEADERBOARD_PATH}")


if __name__ == "__main__":
    main()
