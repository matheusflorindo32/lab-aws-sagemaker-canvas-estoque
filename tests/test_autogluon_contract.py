import unittest

from src.inventory_forecasting.autogluon_runner import (
    autogluon_config,
    summarize_model_stability,
    summarize_prediction_rows,
)


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

    def test_external_stability_is_distinct_from_validation_selection(self) -> None:
        rows = [
            {"fold": 1, "model": "Chronos2", "score_test": -0.33, "selected_by_validation": False},
            {"fold": 1, "model": "WeightedEnsemble", "score_test": -0.42, "selected_by_validation": True},
            {"fold": 1, "model": "DirectTabular", "score_test": -0.49, "selected_by_validation": False},
            {"fold": 2, "model": "WeightedEnsemble", "score_test": -0.26, "selected_by_validation": True},
            {"fold": 2, "model": "DirectTabular", "score_test": -0.27, "selected_by_validation": False},
            {"fold": 2, "model": "Chronos2", "score_test": -0.31, "selected_by_validation": False},
            {"fold": 3, "model": "WeightedEnsemble", "score_test": -0.22, "selected_by_validation": True},
            {"fold": 3, "model": "DirectTabular", "score_test": -0.23, "selected_by_validation": False},
            {"fold": 3, "model": "Chronos2", "score_test": -0.27, "selected_by_validation": False},
        ]
        per_fold, summary = summarize_model_stability(rows)
        self.assertEqual(summary["weighted_ensemble_selected_by_validation_folds"], 3)
        self.assertEqual(summary["weighted_ensemble_external_wins"], 2)
        self.assertEqual(summary["weighted_ensemble_external_top2_folds"], 3)
        self.assertEqual(summary["selection_stability"], "stable")
        self.assertEqual(summary["external_test_stability"], "partially_stable")
        self.assertEqual(per_fold[0]["test_winner"], "Chronos2")
        self.assertEqual(per_fold[0]["weighted_ensemble_test_rank"], 2)
        self.assertGreater(per_fold[0]["weighted_ensemble_relative_wql_gap_to_winner"], 0.20)


if __name__ == "__main__":
    unittest.main()
