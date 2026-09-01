import tempfile
import unittest
from pathlib import Path

from src.inventory_forecasting.ui import execution_status, studio_model_catalog


class UIContractTests(unittest.TestCase):
    def test_execution_status_distinguishes_missing_and_existing_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "result.csv"
            self.assertEqual(execution_status(path), "NÃO EXECUTADO")
            path.write_text("metric,value\n", encoding="utf-8")
            self.assertEqual(execution_status(path), "EXECUTADO")

    def test_catalog_exposes_baselines_and_autogluon(self) -> None:
        models = {row["model"] for row in studio_model_catalog()}
        self.assertIn("Naive", models)
        self.assertIn("SeasonalNaive7", models)
        self.assertIn("Drift", models)
        self.assertIn("AutoGluon TimeSeries", models)


if __name__ == "__main__":
    unittest.main()
