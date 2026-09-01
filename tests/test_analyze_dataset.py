import unittest

from scripts.analyze_dataset import summarize_rows


class AnalyzeDatasetTests(unittest.TestCase):
    def test_summarizes_stock_price_and_promotion_rate(self) -> None:
        rows = [
            {"ID_PRODUTO": "1000", "DATA_EVENTO": "2024-01-01", "PRECO": "10", "FLAG_PROMOCAO": "0", "QUANTIDADE_ESTOQUE": "100"},
            {"ID_PRODUTO": "1000", "DATA_EVENTO": "2024-01-02", "PRECO": "20", "FLAG_PROMOCAO": "1", "QUANTIDADE_ESTOQUE": "80"},
        ]
        summary = summarize_rows(rows)
        self.assertEqual(summary["records"], 2)
        self.assertEqual(summary["skus"], 1)
        self.assertEqual(summary["mean_price"], 15.0)
        self.assertEqual(summary["mean_stock"], 90.0)
        self.assertEqual(summary["promotion_rate"], 0.5)


if __name__ == "__main__":
    unittest.main()
