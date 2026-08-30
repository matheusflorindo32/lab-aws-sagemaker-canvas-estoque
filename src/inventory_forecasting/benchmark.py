from __future__ import annotations

from collections import defaultdict
from statistics import mean, median, stdev
from typing import Callable

from .backtest import rolling_origin_folds, temporal_holdout
from .baselines import drift_forecast, naive_forecast, seasonal_naive_forecast
from .metrics import (
    interval_coverage,
    mae,
    mase,
    mape,
    mean_interval_width,
    quantile_crossing_count,
    rmse,
    wape,
    weighted_quantile_loss,
)

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
    residuals = [history[i] - history[i - 1] for i in range(1, len(history))]
    return {q: _quantile(residuals, q) for q in (0.1, 0.5, 0.9)}


def _safe_metric(fn, *args) -> float:
    try:
        return float(fn(*args))
    except ValueError:
        return float("nan")


def _evaluate_split(
    train: list[dict],
    test: list[dict],
    horizon: int,
    fold: int | None = None,
) -> tuple[list[dict], list[dict]]:
    train_by_sku: dict[str, list[dict]] = defaultdict(list)
    test_by_sku: dict[str, list[dict]] = defaultdict(list)
    for row in train:
        train_by_sku[str(row["ID_PRODUTO"])].append(row)
    for row in test:
        test_by_sku[str(row["ID_PRODUTO"])].append(row)

    leaderboard: list[dict] = []
    prediction_rows: list[dict] = []

    for model_name, model_fn in MODELS.items():
        all_actual: list[float] = []
        all_point: list[float] = []
        all_quantiles: dict[float, list[float]] = {0.1: [], 0.5: [], 0.9: []}
        sku_metric_rows: list[dict] = []

        for sku in sorted(train_by_sku):
            train_rows = sorted(train_by_sku[sku], key=lambda r: r["DATA_EVENTO"])
            test_rows = sorted(test_by_sku[sku], key=lambda r: r["DATA_EVENTO"])
            history = [float(r["QUANTIDADE_ESTOQUE"]) for r in train_rows]
            actual = [float(r["QUANTIDADE_ESTOQUE"]) for r in test_rows]
            if len(actual) != horizon:
                raise ValueError(f"SKU {sku} possui {len(actual)} pontos no teste; esperado={horizon}")
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

            sku_metric_rows.append(
                {
                    "MAE": _safe_metric(mae, actual, point),
                    "RMSE": _safe_metric(rmse, actual, point),
                    "WAPE": _safe_metric(wape, actual, point),
                    "MAPE": _safe_metric(mape, actual, point),
                    "MASE": _safe_metric(mase, actual, point, history, 1),
                    "WQL": _safe_metric(weighted_quantile_loss, actual, quantile_forecasts),
                }
            )

            for index, row in enumerate(test_rows):
                prediction = {
                    "model": model_name,
                    "ID_PRODUTO": sku,
                    "DATA_EVENTO": row["DATA_EVENTO"].isoformat(),
                    "actual": actual[index],
                    "point": point[index],
                    "P10": quantile_forecasts[0.1][index],
                    "P50": quantile_forecasts[0.5][index],
                    "P90": quantile_forecasts[0.9][index],
                }
                if fold is not None:
                    prediction["fold"] = fold
                prediction_rows.append(prediction)

        def macro(metric: str) -> float:
            values = [row[metric] for row in sku_metric_rows if row[metric] == row[metric]]
            return mean(values) if values else float("nan")

        metrics = {
            "model": model_name,
            "MAE": mae(all_actual, all_point),
            "RMSE": rmse(all_actual, all_point),
            "WAPE": wape(all_actual, all_point),
            "MAPE": mape(all_actual, all_point),
            "MACRO_MAE": macro("MAE"),
            "MACRO_RMSE": macro("RMSE"),
            "MACRO_WAPE": macro("WAPE"),
            "MACRO_MAPE": macro("MAPE"),
            "MACRO_MASE": macro("MASE"),
            "WQL": weighted_quantile_loss(all_actual, all_quantiles),
            "MACRO_WQL": macro("WQL"),
            "P10_P90_COVERAGE": interval_coverage(all_actual, all_quantiles[0.1], all_quantiles[0.9]),
            "MEAN_INTERVAL_WIDTH": mean_interval_width(all_quantiles[0.1], all_quantiles[0.9]),
            "QUANTILE_CROSSINGS": quantile_crossing_count(all_quantiles),
        }
        if fold is not None:
            metrics = {"fold": fold, **metrics}
        leaderboard.append(metrics)

    leaderboard.sort(key=lambda row: (row["WAPE"], row["RMSE"]))
    for rank, row in enumerate(leaderboard, start=1):
        row["rank"] = rank
    return leaderboard, prediction_rows


def run_benchmarks(rows: list[dict], horizon: int = 7) -> tuple[list[dict], list[dict]]:
    train, holdout = temporal_holdout(rows, horizon=horizon)
    return _evaluate_split(train, holdout, horizon=horizon)


def run_benchmarks_multifold(
    rows: list[dict],
    horizon: int = 7,
    n_folds: int = 3,
    min_train_size: int = 14,
) -> tuple[list[dict], list[dict], list[dict]]:
    folds = rolling_origin_folds(rows, horizon=horizon, n_folds=n_folds, min_train_size=min_train_size)
    fold_metrics: list[dict] = []
    predictions: list[dict] = []
    for fold_number, (train, test) in enumerate(folds, start=1):
        metrics, fold_predictions = _evaluate_split(train, test, horizon=horizon, fold=fold_number)
        fold_metrics.extend(metrics)
        predictions.extend(fold_predictions)

    numeric_metrics = [
        "MAE",
        "RMSE",
        "WAPE",
        "MAPE",
        "MACRO_MAE",
        "MACRO_RMSE",
        "MACRO_WAPE",
        "MACRO_MAPE",
        "MACRO_MASE",
        "WQL",
        "MACRO_WQL",
        "P10_P90_COVERAGE",
        "MEAN_INTERVAL_WIDTH",
        "QUANTILE_CROSSINGS",
    ]
    summary: list[dict] = []
    for model_name in MODELS:
        model_rows = [row for row in fold_metrics if row["model"] == model_name]
        item: dict[str, object] = {"model": model_name, "folds": len(model_rows)}
        for metric in numeric_metrics:
            values = [float(row[metric]) for row in model_rows]
            item[f"{metric}_mean"] = mean(values)
            item[f"{metric}_median"] = median(values)
            item[f"{metric}_stdev"] = stdev(values) if len(values) > 1 else 0.0
        summary.append(item)

    summary.sort(key=lambda row: (float(row["WAPE_mean"]), float(row["RMSE_mean"])))
    for rank, row in enumerate(summary, start=1):
        row["rank"] = rank
    return fold_metrics, summary, predictions
