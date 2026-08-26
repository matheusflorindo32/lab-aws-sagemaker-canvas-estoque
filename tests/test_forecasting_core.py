import math
import unittest
from datetime import date

from src.inventory_forecasting.backtest import temporal_holdout
from src.inventory_forecasting.metrics import mae, mase, mape, rmse, wape, weighted_quantile_loss


class ForecastingCoreTests(unittest.TestCase):
    def test_temporal_holdout_keeps_last_n_points_per_sku(self) -> None:
        rows = []
        for sku in ("A", "B"):
            for day in range(1, 11):
                rows.append({"ID_PRODUTO": sku, "DATA_EVENTO": date(2024, 1, day), "QUANTIDADE_ESTOQUE": float(day)})

        train, holdout = temporal_holdout(rows, horizon=3)

        self.assertEqual(len(train), 14)
        self.assertEqual(len(holdout), 6)
        for sku in ("A", "B"):
            sku_holdout = [r for r in holdout if r["ID_PRODUTO"] == sku]
            self.assertEqual([r["DATA_EVENTO"].day for r in sku_holdout], [8, 9, 10])

    def test_point_metrics_are_computed_from_known_values(self) -> None:
        actual = [10.0, 20.0, 30.0]
        predicted = [12.0, 18.0, 33.0]

        self.assertAlmostEqual(mae(actual, predicted), 7 / 3)
        self.assertAlmostEqual(rmse(actual, predicted), math.sqrt(17 / 3))
        self.assertAlmostEqual(wape(actual, predicted), 7 / 60)
        self.assertAlmostEqual(mape(actual, predicted), ((2 / 10) + (2 / 20) + (3 / 30)) / 3)

    def test_mase_uses_training_naive_scale(self) -> None:
        actual = [4.0, 5.0]
        predicted = [3.0, 7.0]
        insample = [1.0, 2.0, 4.0, 3.0]
        # MAE forecast = 1.5; naive scale = mean(|1|, |2|, |1|)=4/3
        self.assertAlmostEqual(mase(actual, predicted, insample), 1.125)

    def test_weighted_quantile_loss_is_zero_for_perfect_quantiles(self) -> None:
        actual = [5.0, 10.0]
        forecasts = {0.1: [5.0, 10.0], 0.5: [5.0, 10.0], 0.9: [5.0, 10.0]}
        self.assertEqual(weighted_quantile_loss(actual, forecasts), 0.0)


if __name__ == "__main__":
    unittest.main()
