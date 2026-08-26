from __future__ import annotations

from math import sqrt
from statistics import mean
from typing import Mapping, Sequence


def _validate_lengths(actual: Sequence[float], predicted: Sequence[float]) -> None:
    if not actual or len(actual) != len(predicted):
        raise ValueError("actual e predicted devem ter o mesmo tamanho e não podem estar vazios")


def mae(actual: Sequence[float], predicted: Sequence[float]) -> float:
    _validate_lengths(actual, predicted)
    return mean(abs(a - p) for a, p in zip(actual, predicted))


def rmse(actual: Sequence[float], predicted: Sequence[float]) -> float:
    _validate_lengths(actual, predicted)
    return sqrt(mean((a - p) ** 2 for a, p in zip(actual, predicted)))


def wape(actual: Sequence[float], predicted: Sequence[float]) -> float:
    _validate_lengths(actual, predicted)
    denominator = sum(abs(a) for a in actual)
    if denominator == 0:
        raise ValueError("WAPE indefinido quando a soma absoluta dos valores reais é zero")
    return sum(abs(a - p) for a, p in zip(actual, predicted)) / denominator


def mape(actual: Sequence[float], predicted: Sequence[float]) -> float:
    _validate_lengths(actual, predicted)
    errors = [abs((a - p) / a) for a, p in zip(actual, predicted) if a != 0]
    if not errors:
        raise ValueError("MAPE indefinido quando todos os valores reais são zero")
    return mean(errors)


def mase(
    actual: Sequence[float],
    predicted: Sequence[float],
    insample: Sequence[float],
    season_length: int = 1,
) -> float:
    _validate_lengths(actual, predicted)
    if season_length < 1 or len(insample) <= season_length:
        raise ValueError("Histórico insuficiente para calcular a escala do MASE")
    scale = mean(abs(insample[i] - insample[i - season_length]) for i in range(season_length, len(insample)))
    if scale == 0:
        raise ValueError("MASE indefinido quando a escala naïve é zero")
    return mae(actual, predicted) / scale


def weighted_quantile_loss(
    actual: Sequence[float],
    forecasts: Mapping[float, Sequence[float]],
) -> float:
    if not actual or not forecasts:
        raise ValueError("actual e forecasts não podem estar vazios")
    denominator = sum(abs(a) for a in actual)
    if denominator == 0:
        raise ValueError("WQL indefinido quando a soma absoluta dos valores reais é zero")

    losses: list[float] = []
    for quantile, predicted in sorted(forecasts.items()):
        if not 0 < quantile < 1:
            raise ValueError("Quantis devem estar entre 0 e 1")
        _validate_lengths(actual, predicted)
        pinball = 0.0
        for a, p in zip(actual, predicted):
            error = a - p
            pinball += max(quantile * error, (quantile - 1) * error)
        losses.append(2 * pinball / denominator)
    return mean(losses)
