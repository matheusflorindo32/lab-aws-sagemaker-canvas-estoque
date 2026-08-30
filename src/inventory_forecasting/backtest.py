from __future__ import annotations

from collections import defaultdict
from typing import Iterable


def _group_ordered(rows: Iterable[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[str(row["ID_PRODUTO"])].append(row)
    return {
        sku: sorted(sku_rows, key=lambda r: r["DATA_EVENTO"])
        for sku, sku_rows in sorted(grouped.items())
    }


def temporal_holdout(rows: Iterable[dict], horizon: int = 7) -> tuple[list[dict], list[dict]]:
    if horizon < 1:
        raise ValueError("horizon deve ser >= 1")

    grouped = _group_ordered(rows)
    train: list[dict] = []
    holdout: list[dict] = []
    for sku, ordered in grouped.items():
        if len(ordered) <= horizon:
            raise ValueError(f"SKU {sku} possui histórico insuficiente para holdout de {horizon} passos")
        train.extend(ordered[:-horizon])
        holdout.extend(ordered[-horizon:])

    return train, holdout


def rolling_origin_folds(
    rows: Iterable[dict],
    horizon: int = 7,
    n_folds: int = 3,
    min_train_size: int = 14,
) -> list[tuple[list[dict], list[dict]]]:
    """Build expanding-window folds with non-overlapping test windows per SKU.

    For N observations, the first training window uses all observations left
    after reserving ``n_folds * horizon`` points for evaluation. Each next fold
    expands the training set by one horizon. This keeps every test window
    strictly after its corresponding training window and avoids overlap among
    test windows.
    """
    if horizon < 1 or n_folds < 1 or min_train_size < 1:
        raise ValueError("horizon, n_folds e min_train_size devem ser >= 1")

    grouped = _group_ordered(rows)
    if not grouped:
        raise ValueError("rows não pode estar vazio")

    per_sku_slices: dict[str, list[tuple[list[dict], list[dict]]]] = {}
    for sku, ordered in grouped.items():
        initial_train_size = len(ordered) - n_folds * horizon
        if initial_train_size < min_train_size:
            raise ValueError(
                f"SKU {sku} possui histórico insuficiente: treino inicial={initial_train_size}, "
                f"mínimo={min_train_size}, horizon={horizon}, folds={n_folds}"
            )
        sku_folds: list[tuple[list[dict], list[dict]]] = []
        for fold_index in range(n_folds):
            train_end = initial_train_size + fold_index * horizon
            test_end = train_end + horizon
            train_rows = ordered[:train_end]
            test_rows = ordered[train_end:test_end]
            if len(test_rows) != horizon:
                raise ValueError(f"Fold incompleto para SKU {sku}")
            if train_rows[-1]["DATA_EVENTO"] >= test_rows[0]["DATA_EVENTO"]:
                raise ValueError(f"Ordem temporal inválida para SKU {sku}")
            sku_folds.append((train_rows, test_rows))
        per_sku_slices[sku] = sku_folds

    folds: list[tuple[list[dict], list[dict]]] = []
    for fold_index in range(n_folds):
        train: list[dict] = []
        test: list[dict] = []
        for sku in sorted(per_sku_slices):
            sku_train, sku_test = per_sku_slices[sku][fold_index]
            train.extend(sku_train)
            test.extend(sku_test)
        folds.append((train, test))
    return folds
