from __future__ import annotations

import csv
from collections import Counter
from datetime import datetime
from pathlib import Path

DATASET = Path("datasets/dataset-1000-com-preco-promocional-e-renovacao-estoque.csv")
EXPECTED_COLUMNS = [
    "ID_PRODUTO",
    "DATA_EVENTO",
    "PRECO",
    "FLAG_PROMOCAO",
    "QUANTIDADE_ESTOQUE",
]


def fail(message: str) -> None:
    raise SystemExit(f"[ERRO] {message}")


def main() -> None:
    if not DATASET.exists():
        fail(f"Dataset não encontrado: {DATASET}")

    rows: list[dict[str, str]] = []
    with DATASET.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != EXPECTED_COLUMNS:
            fail(f"Schema inesperado: {reader.fieldnames}")
        rows = list(reader)

    if not rows:
        fail("Dataset vazio")

    missing = sum(any(value is None or value.strip() == "" for value in row.values()) for row in rows)
    duplicates = len(rows) - len({tuple(row[col] for col in EXPECTED_COLUMNS) for row in rows})

    sku_counts: Counter[str] = Counter()
    dates: list[datetime] = []
    invalid_rows = 0

    for row in rows:
        try:
            sku = row["ID_PRODUTO"].strip()
            date = datetime.strptime(row["DATA_EVENTO"], "%Y-%m-%d")
            float(row["PRECO"])
            promotion = int(row["FLAG_PROMOCAO"])
            stock = int(row["QUANTIDADE_ESTOQUE"])
            if promotion not in (0, 1) or stock < 0:
                raise ValueError
        except (ValueError, TypeError):
            invalid_rows += 1
            continue
        sku_counts[sku] += 1
        dates.append(date)

    print("=== Validação do dataset ===")
    print(f"Arquivo: {DATASET}")
    print(f"Registros: {len(rows)}")
    print(f"SKUs únicos: {len(sku_counts)}")
    print(f"Data inicial: {min(dates).date() if dates else 'N/A'}")
    print(f"Data final: {max(dates).date() if dates else 'N/A'}")
    print(f"Linhas com campos ausentes: {missing}")
    print(f"Duplicatas exatas: {duplicates}")
    print(f"Linhas inválidas: {invalid_rows}")

    if missing or invalid_rows:
        fail("Foram encontradas inconsistências que exigem revisão")

    print("[OK] Dataset válido para prosseguir com a preparação do Lab.")


if __name__ == "__main__":
    main()
