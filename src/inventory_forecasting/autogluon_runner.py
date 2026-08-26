from __future__ import annotations

from pathlib import Path


def autogluon_config() -> dict:
    return {
        "prediction_length": 7,
        "target": "QUANTIDADE_ESTOQUE",
        "known_covariates_names": ["PRECO", "FLAG_PROMOCAO"],
        "quantile_levels": [0.1, 0.5, 0.9],
        "eval_metric": "WQL",
        "freq": "D",
    }


def run_autogluon_backtest(
    csv_path: str = "datasets/dataset-1000-com-preco-promocional-e-renovacao-estoque.csv",
    model_path: str = "artifacts/autogluon",
    presets: str = "medium_quality",
    time_limit: int | None = 300,
):
    """Train AutoGluon on the first 33 days/SKU and evaluate the final 7-day holdout.

    AutoGluon is imported lazily so the lightweight CI remains dependency-free.
    The holdout contains future covariate values that are known for the historical
    backtest; future production forecasts require an explicit scenario for these
    covariates and are never fabricated by this function.
    """
    try:
        import pandas as pd
        from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor
    except ImportError as exc:
        raise RuntimeError(
            "AutoGluon TimeSeries não está instalado. Instale `requirements-ml.txt` "
            "antes de executar este treinamento."
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

    train_ts = TimeSeriesDataFrame.from_data_frame(
        train_df,
        id_column="ID_PRODUTO",
        timestamp_column="DATA_EVENTO",
    )
    full_ts = TimeSeriesDataFrame.from_data_frame(
        frame,
        id_column="ID_PRODUTO",
        timestamp_column="DATA_EVENTO",
    )
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
    predictor.fit(train_ts, presets=presets, time_limit=time_limit)
    predictions = predictor.predict(train_ts, known_covariates=known_covariates)
    leaderboard = predictor.leaderboard(full_ts)
    evaluation = predictor.evaluate(full_ts)
    feature_importance = predictor.feature_importance(full_ts)
    return {
        "predictor": predictor,
        "predictions": predictions,
        "leaderboard": leaderboard,
        "evaluation": evaluation,
        "feature_importance": feature_importance,
        "holdout": holdout_df,
        "config": config,
    }
