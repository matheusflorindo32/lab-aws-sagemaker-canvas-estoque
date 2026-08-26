from __future__ import annotations

import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
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
EXPECTED_RECORDS = 1000
EXPECTED_SKUS = 25
EXPECTED_OBSERVATIONS_PER_SKU = 40
EXPECTED_START = datetime(2023, 12, 31)
EXPECTED_END = datetime(2024, 2, 8)


@dataclass(frozen=True)
class ValidationReport:
    records: int
    sku_counts: Counter[str]
    min_date: datetime | None
    max_date: datetime | None
    missing_rows: int
    exact_duplicates: int
    duplicate_keys: int
    invalid_rows: int
    missing_daily_points: int


def fail(message: str) -> None:
    raise SystemExit(f"[ERRO] {message}")


def validate_rows(rows: list[dict[str, str]]) -> ValidationReport:
    missing_rows = sum(
        any(value is None or value.strip() == "" for value in row.values())
        for row in rows
    )
    exact_duplicates = len(rows) - len(
        {tuple(row.get(col, "") for col in EXPECTED_COLUMNS) for row in rows}
    )

    sku_counts: Counter[str] = Counter()
    dates_by_sku: dict[str, list[datetime]] = defaultdict(list)
    valid_keys: list[tuple[str, datetime]] = []
    invalid_rows = 0

    for row in rows:
        try:
            sku = row["ID_PRODUTO"].strip()
            if not sku:
                raise ValueError("SKU vazio")
            date = datetime.strptime(row["DATA_EVENTO"].strip(), "%Y-%m-%d")
            price = float(row["PRECO"])
            promotion = int(row["FLAG_PROMOCAO"])
            stock = int(row["QUANTIDADE_ESTOQUE"])
            if price < 0 or stock < 0 or promotion not in (0, 1):
                raise ValueError("Valor fora do domínio esperado")
        except (KeyError, ValueError, TypeError, AttributeError):
            invalid_rows += 1
            continue

        sku_counts[sku] += 1
        dates_by_sku[sku].append(date)
        valid_keys.append((sku, date))

    duplicate_keys = len(valid_keys) - len(set(valid_keys))
    all_dates = [date for dates in dates_by_sku.values() for date in dates]

    missing_daily_points = 0
    for dates in dates_by_sku.values():
        unique_dates = sorted(set(dates))
        if not unique_dates:
            continue
        expected_points = (unique_dates[-1] - unique_dates[0]).days + 1
        missing_daily_points += expected_points - len(unique_dates)

    return ValidationReport(
        records=len(rows),
        sku_counts=sku_counts,
        min_date=min(all_dates) if all_dates else None,
        max_date=max(all_dates) if all_dates else None,
        missing_rows=missing_rows,
        exact_duplicates=exact_duplicates,
        duplicate_keys=duplicate_keys,
        invalid_rows=invalid_rows,
        missing_daily_points=missing_daily_points,
    )


def validate_baseline_cardinality(report: ValidationReport) -> list[str]:
    problems: list[str] = []
    if report.records != EXPECTED_RECORDS:
        problems.append(f"esperados {EXPECTED_RECORDS} registros; encontrados {report.records}")
    if len(report.sku_counts) != EXPECTED_SKUS:
        problems.append(f"esperados {EXPECTED_SKUS} SKUs; encontrados {len(report.sku_counts)}")
    irregular = {sku: count for sku, count in report.sku_counts.items() if count != EXPECTED_OBSERVATIONS_PER_SKU}
    if irregular:
        problems.append(f"SKUs com cardinalidade diferente de {EXPECTED_OBSERVATIONS_PER_SKU}: {irregular}")
    if report.min_date != EXPECTED_START or report.max_date != EXPECTED_END:
        problems.append(
            "intervalo temporal divergente do baseline: "
            f"{report.min_date.date() if report.min_date else 'N/A'} a "
            f"{report.max_date.date() if report.max_date else 'N/A'}"
        )
    return problems


def main() -> None:
    if not DATASET.exists():
        fail(f"Dataset não encontrado: {DATASET}")

    with DATASET.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != EXPECTED_COLUMNS:
            fail(f"Schema inesperado: {reader.fieldnames}")
        rows = list(reader)

    if not rows:
        fail("Dataset vazio")

    report = validate_rows(rows)
    cardinality_problems = validate_baseline_cardinality(report)

    print("=== Validação do dataset ===")
    print(f"Arquivo: {DATASET}")
    print(f"Registros: {report.records}")
    print(f"SKUs únicos: {len(report.sku_counts)}")
    print(f"Observações por SKU: min={min(report.sku_counts.values())}, max={max(report.sku_counts.values())}")
    print(f"Data inicial: {report.min_date.date() if report.min_date else 'N/A'}")
    print(f"Data final: {report.max_date.date() if report.max_date else 'N/A'}")
    print(f"Linhas com campos ausentes: {report.missing_rows}")
    print(f"Duplicatas exatas: {report.exact_duplicates}")
    print(f"Chaves SKU+data duplicadas: {report.duplicate_keys}")
    print(f"Pontos diários ausentes nas séries: {report.missing_daily_points}")
    print(f"Linhas inválidas: {report.invalid_rows}")

    structural_problems = (
        report.missing_rows
        + report.exact_duplicates
        + report.duplicate_keys
        + report.invalid_rows
        + report.missing_daily_points
    )
    if structural_problems or cardinality_problems:
        for problem in cardinality_problems:
            print(f"[ERRO] {problem}")
        fail("Foram encontradas inconsistências que exigem revisão")

    print("[OK] Dataset baseline íntegro e regular para prosseguir com o Lab.")


if __name__ == "__main__":
    main()
