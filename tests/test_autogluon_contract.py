import unittest

from src.inventory_forecasting.autogluon_runner import autogluon_config


class AutoGluonContractTests(unittest.TestCase):
    def test_configuration_matches_project_forecasting_contract(self) -> None:
        config = autogluon_config()
        self.assertEqual(config["prediction_length"], 7)
        self.assertEqual(config["target"], "QUANTIDADE_ESTOQUE")
        self.assertEqual(config["known_covariates_names"], ["PRECO", "FLAG_PROMOCAO"])
        self.assertEqual(config["quantile_levels"], [0.1, 0.5, 0.9])
        self.assertEqual(config["eval_metric"], "WQL")
        self.assertEqual(config["freq"], "D")


if __name__ == "__main__":
    unittest.main()
