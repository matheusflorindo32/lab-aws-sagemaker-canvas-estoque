from __future__ import annotations

import csv
import io
from datetime import datetime
from pathlib import Path
from typing import BinaryIO, TextIO

DEFAULT_DATASET = Path("datasets/dataset-1000-com-preco-promocional-e-renovacao-estoque.csv")
REQUIRED_COLUMNS = [
    "ID_PRODUTO",
    "DATA_EVENTO",
    "PRECO",
    "FLAG_PROMOCAO",
    "QUANTIDADE_ESTOQUE",
]


def _parse_reader(reader: csv.DictReader) -> list[dict]:
    fieldnames = reader.fieldnames or []
    missing = [column for column in REQUIRED_COLUMNS if column not in fieldnames]
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(missing)}")

    rows: list[dict] = []
    for line_number, row in enumerate(reader, start=2):
        try:
            rows.append(
                {
                    "ID_PRODUTO": row["ID_PRODUTO"].strip(),
                    "DATA_EVENTO": datetime.strptime(row["DATA_EVENTO"].strip(), "%Y-%m-%d").date(),
                    "PRECO": float(row["PRECO"]),
                    "FLAG_PROMOCAO": int(row["FLAG_PROMOCAO"]),
                    "QUANTIDADE_ESTOQUE": float(row["QUANTIDADE_ESTOQUE"]),
                }
            )
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Linha {line_number} inválida: {exc}") from exc

    if not rows:
        raise ValueError("Dataset vazio")
    return rows


def load_dataset(path: str | Path = DEFAULT_DATASET) -> list[dict]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return _parse_reader(csv.DictReader(handle))


def load_dataset_file(file_obj: BinaryIO | TextIO) -> list[dict]:
    payload = file_obj.read()
    if isinstance(payload, bytes):
        text = payload.decode("utf-8-sig")
    else:
        text = str(payload)
    return _parse_reader(csv.DictReader(io.StringIO(text)))
