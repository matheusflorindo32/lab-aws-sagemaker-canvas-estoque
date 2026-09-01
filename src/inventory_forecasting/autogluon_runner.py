from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from statistics import mean

from .metrics import (
    interval_coverage,
    mae,
    mape,
    mean_interval_width,
    pinball_loss,
    quantile_crossing_count,
    rmse,
    wape,
    weighted_quantile_loss,
)


def autogluon_config() -> dict:
    return {
        "prediction_length": 7,
        "target": "QUANTIDADE_ESTOQUE",
        "known_covariates_names": ["PRECO", "FLAG_PROMOCAO"],
        "quantile_levels": [0.1, 0.5, 0.9],
        "eval_metric": "WQL",
        "freq": "D",
        "random_seed": 123,
    }


def summarize_model_stability(rows: list[dict]) -> tuple[list[dict], dict]:
    """Separate validation-selection stability from external holdout performance.

    AutoGluon loss metrics are exposed as scores where higher is better, so the
    external winner is the row with the largest ``score_test`` in each fold.
    """
    if not rows:
        raise ValueError("rows não pode estar vazio")

    by_fold: dict[int, list[dict]] = defaultdict(list)
    for row in rows:
        by_fold[int(row["fold"])].append(row)

    per_fold: list[dict] = []
    weighted_selected = 0
    weighted_wins = 0
    weighted_top2 = 0

    for fold in sorted(by_fold):
        fold_rows = sorted(by_fold[fold], key=lambda row: float(row["score_test"]), reverse=True)
        winner = fold_rows[0]
        weighted_matches = [row for row in fold_rows if str(row["model"]) == "WeightedEnsemble"]
        if not weighted_matches:
            raise ValueError(f"WeightedEnsemble ausente no fold {fold}")
        weighted = weighted_matches[0]
        weighted_rank = next(index for index, row in enumerate(fold_rows, start=1) if row is weighted)
        selected_rows = [row for row in fold_rows if bool(row.get("selected_by_validation"))]
        selected_model = str(selected_rows[0]["model"]) if selected_rows else "UNKNOWN"

        if selected_model == "WeightedEnsemble":
            weighted_selected += 1
        if weighted_rank == 1:
            weighted_wins += 1
        if weighted_rank <= 2:
            weighted_top2 += 1

        winner_loss = abs(float(winner["score_test"]))
        weighted_loss = abs(float(weighted["score_test"]))
        relative_gap = (weighted_loss - winner_loss) / winner_loss if winner_loss else 0.0
        per_fold.append(
            {
                "fold": fold,
                "selected_by_validation": selected_model,
                "test_winner": str(winner["model"]),
                "weighted_ensemble_test_rank": weighted_rank,
                "weighted_ensemble_score_test": float(weighted["score_test"]),
                "winner_score_test": float(winner["score_test"]),
                "weighted_ensemble_relative_wql_gap_to_winner": relative_gap,
            }
        )

    folds = len(per_fold)
    selection_stability = "stable" if weighted_selected == folds else "partially_stable" if weighted_selected >= 2 else "unstable"
    if folds < 3:
        external_stability = "inconclusive"
    elif weighted_wins == folds:
        external_stability = "stable"
    elif weighted_wins >= 2 and weighted_top2 == folds:
        external_stability = "partially_stable"
    else:
        external_stability = "unstable"

    ranks = [float(row["weighted_ensemble_test_rank"]) for row in per_fold]
    summary = {
        "folds": folds,
        "weighted_ensemble_selected_by_validation_folds": weighted_selected,
        "weighted_ensemble_external_wins": weighted_wins,
        "weighted_ensemble_external_top2_folds": weighted_top2,
        "weighted_ensemble_external_win_rate": weighted_wins / folds,
        "weighted_ensemble_mean_external_rank": mean(ranks),
        "selection_stability": selection_stability,
        "external_test_stability": external_stability,
    }
    return per_fold, summary


def summarize_prediction_rows(rows: list[dict]) -> dict[str, float]:
    if not rows:
        raise ValueError("rows não pode estar vazio")
    actual = [float(row["actual"]) for row in rows]
    point = [float(row["mean"]) for row in rows]
    p10 = [float(row["P10"]) for row in rows]
    p50 = [float(row["P50"]) for row in rows]
    p90 = [float(row["P90"]) for row in rows]
    forecasts = {0.1: p10, 0.5: p50, 0.9: p90}

    by_sku: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_sku[str(row["ID_PRODUTO"])].append(row)

    macro_mae = mean(
        mae([float(r["actual"]) for r in sku_rows], [float(r["mean"]) for r in sku_rows])
        for sku_rows in by_sku.values()
    )
    macro_wape_values = []
    for sku_rows in by_sku.values():
        sku_actual = [float(r["actual"]) for r in sku_rows]
        sku_point = [float(r["mean"]) for r in sku_rows]
        try:
            macro_wape_values.append(wape(sku_actual, sku_point))
        except ValueError:
            pass

    return {
        "MAE": mae(actual, point),
        "RMSE": rmse(actual, point),
        "WAPE": wape(actual, point),
        "MAPE": mape(actual, point),
        "WQL": weighted_quantile_loss(actual, forecasts),
        "MACRO_MAE": macro_mae,
        "MACRO_WAPE": mean(macro_wape_values) if macro_wape_values else float("nan"),
        "PINBALL_P10": pinball_loss(actual, p10, 0.1),
        "PINBALL_P50": pinball_loss(actual, p50, 0.5),
        "PINBALL_P90": pinball_loss(actual, p90, 0.9),
        "P10_P90_COVERAGE": interval_coverage(actual, p10, p90),
        "MEAN_INTERVAL_WIDTH": mean_interval_width(p10, p90),
        "QUANTILE_CROSSINGS": float(quantile_crossing_count(forecasts)),
        "CALIBRATION_P10": mean(1.0 if a <= q else 0.0 for a, q in zip(actual, p10)),
        "CALIBRATION_P50": mean(1.0 if a <= q else 0.0 for a, q in zip(actual, p50)),
        "CALIBRATION_P90": mean(1.0 if a <= q else 0.0 for a, q in zip(actual, p90)),
    }


def run_autogluon_backtest(
    csv_path: str = "datasets/dataset-1000-com-preco-promocional-e-renovacao-estoque.csv",
    model_path: str = "artifacts/autogluon",
    presets: str = "medium_quality",
    time_limit: int | None = 300,
):
    """Train AutoGluon on all but the final 7 days/SKU and evaluate that holdout."""
    try:
        import pandas as pd
        from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor
    except ImportError as exc:
        raise RuntimeError(
            "AutoGluon TimeSeries não está instalado. Instale `requirements-ml.txt` antes de executar este treinamento."
        ) from exc

    config = autogluon_config()
    frame = pd.read_csv(csv_path, parse_dates=["DATA_EVENTO"])
    frame = frame.sort_values(["ID_PRODUTO", "DATA_EVENTO"]).copy()
    frame["ID_PRODUTO"] = frame["ID_PRODUTO"].astype(str)

    train_parts = []
    holdout_parts = []
    for _, group in frame.groupby("ID_PRODUTO", sort=True):
        if len(group) <= config["prediction_length"]:
            raise ValueError("Série insuficiente para holdout de 7 dias")
        train_parts.append(group.iloc[:-config["prediction_length"]])
        holdout_parts.append(group.iloc[-config["prediction_length"]:])

    train_df = pd.concat(train_parts, ignore_index=True)
    holdout_df = pd.concat(holdout_parts, ignore_index=True)

    train_ts = TimeSeriesDataFrame.from_data_frame(train_df, id_column="ID_PRODUTO", timestamp_column="DATA_EVENTO")
    full_ts = TimeSeriesDataFrame.from_data_frame(frame, id_column="ID_PRODUTO", timestamp_column="DATA_EVENTO")
    known_covariates = TimeSeriesDataFrame.from_data_frame(
        holdout_df[["ID_PRODUTO", "DATA_EVENTO", "PRECO", "FLAG_PROMOCAO"]],
        id_column="ID_PRODUTO",
        timestamp_column="DATA_EVENTO",
    )

    path = Path(model_path)
    path.mkdir(parents=True, exist_ok=True)
    predictor = TimeSeriesPredictor(
        target=config["target"],
        prediction_length=config["prediction_length"],
        known_covariates_names=config["known_covariates_names"],
        quantile_levels=config["quantile_levels"],
        eval_metric=config["eval_metric"],
        freq=config["freq"],
        path=str(path),
    )
    predictor.fit(
        train_ts,
        presets=presets,
        time_limit=time_limit,
        random_seed=config["random_seed"],
    )
    predictions = predictor.predict(
        train_ts,
        known_covariates=known_covariates,
        random_seed=config["random_seed"],
    )
    leaderboard = predictor.leaderboard(full_ts)
    evaluation = predictor.evaluate(full_ts)
    feature_importance = predictor.feature_importance(full_ts, random_seed=config["random_seed"])
    return {
        "predictor": predictor,
        "predictions": predictions,
        "leaderboard": leaderboard,
        "evaluation": evaluation,
        "feature_importance": feature_importance,
        "holdout": holdout_df,
        "config": config,
    }
