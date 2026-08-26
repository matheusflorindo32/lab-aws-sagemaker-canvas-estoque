from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, pstdev

DATASET = Path("datasets/dataset-1000-com-preco-promocional-e-renovacao-estoque.csv")


def summarize_rows(rows: list[dict[str, str]]) -> dict[str, object]:
    prices = [float(row["PRECO"]) for row in rows]
    stocks = [int(row["QUANTIDADE_ESTOQUE"]) for row in rows]
    promotions = [int(row["FLAG_PROMOCAO"]) for row in rows]
    skus = {row["ID_PRODUTO"] for row in rows}

    stock_by_promo: dict[int, list[int]] = defaultdict(list)
    stock_by_sku: dict[str, list[int]] = defaultdict(list)
    for row in rows:
        promo = int(row["FLAG_PROMOCAO"])
        stock = int(row["QUANTIDADE_ESTOQUE"])
        stock_by_promo[promo].append(stock)
        stock_by_sku[row["ID_PRODUTO"]].append(stock)

    sku_volatility = {
        sku: round(pstdev(values), 2) if len(values) > 1 else 0.0
        for sku, values in stock_by_sku.items()
    }

    return {
        "records": len(rows),
        "skus": len(skus),
        "mean_price": round(mean(prices), 2),
        "min_price": min(prices),
        "max_price": max(prices),
        "mean_stock": round(mean(stocks), 2),
        "min_stock": min(stocks),
        "max_stock": max(stocks),
        "promotion_rate": round(sum(promotions) / len(promotions), 4),
        "mean_stock_promo": round(mean(stock_by_promo[1]), 2) if stock_by_promo[1] else None,
        "mean_stock_no_promo": round(mean(stock_by_promo[0]), 2) if stock_by_promo[0] else None,
        "most_volatile_skus": sorted(
            sku_volatility.items(), key=lambda item: item[1], reverse=True
        )[:5],
        "observations_per_sku": Counter(row["ID_PRODUTO"] for row in rows),
    }


def main() -> None:
    if not DATASET.exists():
        raise SystemExit(f"[ERRO] Dataset não encontrado: {DATASET}")

    with DATASET.open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    summary = summarize_rows(rows)

    print("=== Análise exploratória descritiva ===")
    print(f"Registros: {summary['records']}")
    print(f"SKUs: {summary['skus']}")
    print(
        "Preço: "
        f"média={summary['mean_price']}, min={summary['min_price']}, max={summary['max_price']}"
    )
    print(
        "Estoque: "
        f"média={summary['mean_stock']}, min={summary['min_stock']}, max={summary['max_stock']}"
    )
    print(f"Proporção de registros promocionais: {summary['promotion_rate']:.2%}")
    print(f"Estoque médio em promoção: {summary['mean_stock_promo']}")
    print(f"Estoque médio sem promoção: {summary['mean_stock_no_promo']}")
    print("Top 5 SKUs por volatilidade descritiva do estoque (desvio-padrão):")
    for sku, volatility in summary["most_volatile_skus"]:
        print(f"- SKU {sku}: {volatility}")

    print(
        "\nNota: estas estatísticas são descritivas e não demonstram causalidade "
        "entre preço, promoção e nível de estoque."
    )


if __name__ == "__main__":
    main()
