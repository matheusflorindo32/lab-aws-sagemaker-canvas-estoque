import unittest
from datetime import datetime

from scripts.validate_dataset import validate_rows


class ValidateDatasetTests(unittest.TestCase):
    def test_rejects_negative_price(self) -> None:
        rows = [{
            "ID_PRODUTO": "1000",
            "DATA_EVENTO": "2024-01-01",
            "PRECO": "-1.00",
            "FLAG_PROMOCAO": "0",
            "QUANTIDADE_ESTOQUE": "10",
        }]
        report = validate_rows(rows)
        self.assertEqual(report.invalid_rows, 1)

    def test_detects_duplicate_sku_date_key(self) -> None:
        row = {
            "ID_PRODUTO": "1000",
            "DATA_EVENTO": "2024-01-01",
            "PRECO": "10.00",
            "FLAG_PROMOCAO": "0",
            "QUANTIDADE_ESTOQUE": "10",
        }
        report = validate_rows([row, row.copy()])
        self.assertEqual(report.duplicate_keys, 1)

    def test_detects_missing_daily_date_for_sku(self) -> None:
        rows = [
            {"ID_PRODUTO": "1000", "DATA_EVENTO": "2024-01-01", "PRECO": "10", "FLAG_PROMOCAO": "0", "QUANTIDADE_ESTOQUE": "10"},
            {"ID_PRODUTO": "1000", "DATA_EVENTO": "2024-01-03", "PRECO": "10", "FLAG_PROMOCAO": "0", "QUANTIDADE_ESTOQUE": "8"},
        ]
        report = validate_rows(rows)
        self.assertEqual(report.missing_daily_points, 1)
        self.assertEqual(report.min_date, datetime(2024, 1, 1))
        self.assertEqual(report.max_date, datetime(2024, 1, 3))


if __name__ == "__main__":
    unittest.main()
