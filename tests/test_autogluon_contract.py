import unittest

from src.inventory_forecasting.autogluon_runner import autogluon_config, summarize_prediction_rows


class AutoGluonContractTests(unittest.TestCase):
    def test_configuration_matches_project_forecasting_contract(self) -> None:
        config = autogluon_config()
        self.assertEqual(config["prediction_length"], 7)
        self.assertEqual(config["target"], "QUANTIDADE_ESTOQUE")
        self.assertEqual(config["known_covariates_names"], ["PRECO", "FLAG_PROMOCAO"])
        self.assertEqual(config["quantile_levels"], [0.1, 0.5, 0.9])
        self.assertEqual(config["eval_metric"], "WQL")
        self.assertEqual(config["freq"], "D")
        self.assertEqual(config["random_seed"], 123)

    def test_prediction_summary_contains_point_and_calibration_metrics(self) -> None:
        rows = [
            {"ID_PRODUTO": "A", "actual": 10.0, "mean": 9.0, "P10": 7.0, "P50": 9.0, "P90": 12.0},
            {"ID_PRODUTO": "A", "actual": 20.0, "mean": 21.0, "P10": 18.0, "P50": 20.0, "P90": 23.0},
            {"ID_PRODUTO": "B", "actual": 30.0, "mean": 29.0, "P10": 27.0, "P50": 30.0, "P90": 32.0},
        ]
        summary = summarize_prediction_rows(rows)
        self.assertAlmostEqual(summary["MAE"], 1.0)
        self.assertEqual(summary["P10_P90_COVERAGE"], 1.0)
        self.assertEqual(summary["QUANTILE_CROSSINGS"], 0)
        self.assertIn("PINBALL_P10", summary)
        self.assertIn("CALIBRATION_P90", summary)
        self.assertIn("MACRO_MAE", summary)


if __name__ == "__main__":
    unittest.main()
