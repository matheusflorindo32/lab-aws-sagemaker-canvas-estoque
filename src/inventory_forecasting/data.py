from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

DEFAULT_DATASET = Path("datasets/dataset-1000-com-preco-promocional-e-renovacao-estoque.csv")


def load_dataset(path: str | Path = DEFAULT_DATASET) -> list[dict]:
    rows: list[dict] = []
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                {
                    "ID_PRODUTO": row["ID_PRODUTO"].strip(),
                    "DATA_EVENTO": datetime.strptime(row["DATA_EVENTO"], "%Y-%m-%d").date(),
                    "PRECO": float(row["PRECO"]),
                    "FLAG_PROMOCAO": int(row["FLAG_PROMOCAO"]),
                    "QUANTIDADE_ESTOQUE": float(row["QUANTIDADE_ESTOQUE"]),
                }
            )
    if not rows:
        raise ValueError("Dataset vazio")
    return rows
