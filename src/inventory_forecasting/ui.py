from __future__ import annotations

from pathlib import Path


def execution_status(path: str | Path) -> str:
    return "EXECUTADO" if Path(path).exists() else "NÃO EXECUTADO"


def studio_model_catalog() -> list[dict[str, str]]:
    return [
        {"model": "Naive", "type": "baseline", "status": "disponível"},
        {"model": "SeasonalNaive7", "type": "baseline sazonal", "status": "disponível"},
        {"model": "Drift", "type": "baseline de tendência", "status": "disponível"},
        {"model": "AutoGluon TimeSeries", "type": "AutoML probabilístico", "status": "opcional"},
    ]
