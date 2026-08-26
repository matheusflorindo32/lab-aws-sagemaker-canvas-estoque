from __future__ import annotations

from collections import defaultdict
from statistics import mean
from typing import Callable

from .backtest import temporal_holdout
from .baselines import drift_forecast, naive_forecast, seasonal_naive_forecast
from .metrics import mae, mase, mape, rmse, wape, weighted_quantile_loss

ModelFn = Callable[[list[float], int], list[float]]

MODELS: dict[str, ModelFn] = {
    "Naive": naive_forecast,
    "SeasonalNaive7": lambda history, horizon: seasonal_naive_forecast(history, horizon, season_length=7),
    "Drift": drift_forecast,
}


def _quantile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(float(v) for v in values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * q
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def _innovation_quantiles(history: list[float]) -> dict[float, float]:
    # Empirical one-step innovations provide a transparent uncertainty baseline.
    residuals = [history[i] - history[i - 1] for i in range(1, len(history))]
    return {q: _quantile(residuals, q) for q in (0.1, 0.5, 0.9)}


def run_benchmarks(rows: list[dict], horizon: int = 7) -> tuple[list[dict], list[dict]]:
    train, holdout = temporal_holdout(rows, horizon=horizon)
    train_by_sku: dict[str, list[dict]] = defaultdict(list)
    holdout_by_sku: dict[str, list[dict]] = defaultdict(list)
    for row in train:
        train_by_sku[str(row["ID_PRODUTO"])].append(row)
    for row in holdout:
        holdout_by_sku[str(row["ID_PRODUTO"])].append(row)

    leaderboard: list[dict] = []
    prediction_rows: list[dict] = []

    for model_name, model_fn in MODELS.items():
        all_actual: list[float] = []
        all_point: list[float] = []
        all_quantiles: dict[float, list[float]] = {0.1: [], 0.5: [], 0.9: []}
        per_sku_mase: list[float] = []

        for sku in sorted(train_by_sku):
            train_rows = sorted(train_by_sku[sku], key=lambda r: r["DATA_EVENTO"])
            test_rows = sorted(holdout_by_sku[sku], key=lambda r: r["DATA_EVENTO"])
            history = [float(r["QUANTIDADE_ESTOQUE"]) for r in train_rows]
            actual = [float(r["QUANTIDADE_ESTOQUE"]) for r in test_rows]
            point = model_fn(history, horizon)
            innovations = _innovation_quantiles(history)
            quantile_forecasts = {
                q: [max(0.0, p + innovations[q]) for p in point]
                for q in (0.1, 0.5, 0.9)
            }

            all_actual.extend(actual)
            all_point.extend(point)
            for q in all_quantiles:
                all_quantiles[q].extend(quantile_forecasts[q])

            try:
                per_sku_mase.append(mase(actual, point, history, season_length=1))
            except ValueError:
                pass

            for index, row in enumerate(test_rows):
                prediction_rows.append(
                    {
                        "model": model_name,
                        "ID_PRODUTO": sku,
                        "DATA_EVENTO": row["DATA_EVENTO"].isoformat(),
                        "actual": actual[index],
                        "point": point[index],
                        "P10": quantile_forecasts[0.1][index],
                        "P50": quantile_forecasts[0.5][index],
                        "P90": quantile_forecasts[0.9][index],
                    }
                )

        leaderboard.append(
            {
                "model": model_name,
                "MAE": mae(all_actual, all_point),
                "RMSE": rmse(all_actual, all_point),
                "WAPE": wape(all_actual, all_point),
                "MAPE": mape(all_actual, all_point),
                "MASE": mean(per_sku_mase) if per_sku_mase else float("nan"),
                "WQL": weighted_quantile_loss(all_actual, all_quantiles),
            }
        )

    leaderboard.sort(key=lambda row: (row["WAPE"], row["RMSE"]))
    for rank, row in enumerate(leaderboard, start=1):
        row["rank"] = rank
    return leaderboard, prediction_rows
