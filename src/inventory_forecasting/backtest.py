from __future__ import annotations

from collections import defaultdict
from typing import Iterable


def temporal_holdout(rows: Iterable[dict], horizon: int = 7) -> tuple[list[dict], list[dict]]:
    if horizon < 1:
        raise ValueError("horizon deve ser >= 1")

    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[str(row["ID_PRODUTO"])].append(row)

    train: list[dict] = []
    holdout: list[dict] = []
    for sku, sku_rows in sorted(grouped.items()):
        ordered = sorted(sku_rows, key=lambda r: r["DATA_EVENTO"])
        if len(ordered) <= horizon:
            raise ValueError(f"SKU {sku} possui histórico insuficiente para holdout de {horizon} passos")
        train.extend(ordered[:-horizon])
        holdout.extend(ordered[-horizon:])

    return train, holdout
