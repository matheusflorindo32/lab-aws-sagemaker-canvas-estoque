from __future__ import annotations


def naive_forecast(history: list[float], horizon: int) -> list[float]:
    if not history:
        raise ValueError("history não pode estar vazio")
    return [float(history[-1])] * horizon


def seasonal_naive_forecast(history: list[float], horizon: int, season_length: int = 7) -> list[float]:
    if season_length < 1 or len(history) < season_length:
        raise ValueError("Histórico insuficiente para seasonal naive")
    season = [float(v) for v in history[-season_length:]]
    return [season[i % season_length] for i in range(horizon)]


def drift_forecast(history: list[float], horizon: int) -> list[float]:
    if len(history) < 2:
        raise ValueError("Drift requer pelo menos duas observações")
    slope = (float(history[-1]) - float(history[0])) / (len(history) - 1)
    last = float(history[-1])
    return [last + slope * step for step in range(1, horizon + 1)]
