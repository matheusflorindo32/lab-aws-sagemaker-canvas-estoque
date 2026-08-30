import math
import unittest
from datetime import date

from src.inventory_forecasting.backtest import rolling_origin_folds, temporal_holdout
from src.inventory_forecasting.metrics import (
    interval_coverage,
    mae,
    mase,
    mape,
    mean_interval_width,
    pinball_loss,
    quantile_crossing_count,
    rmse,
    wape,
    weighted_quantile_loss,
)


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

    def test_rolling_origin_builds_three_non_overlapping_expanding_folds(self) -> None:
        rows = []
        for sku in ("A", "B"):
            for day in range(1, 41):
                rows.append({"ID_PRODUTO": sku, "DATA_EVENTO": date(2024, 1, 1).replace(day=1), "STEP": day})
                rows[-1]["DATA_EVENTO"] = date.fromordinal(date(2024, 1, 1).toordinal() + day - 1)

        folds = rolling_origin_folds(rows, horizon=7, n_folds=3, min_train_size=14)

        self.assertEqual(len(folds), 3)
        expected_train_sizes = [19, 26, 33]
        expected_test_steps = [(20, 26), (27, 33), (34, 40)]
        for fold_index, (train, test) in enumerate(folds):
            for sku in ("A", "B"):
                sku_train = [row for row in train if row["ID_PRODUTO"] == sku]
                sku_test = [row for row in test if row["ID_PRODUTO"] == sku]
                self.assertEqual(len(sku_train), expected_train_sizes[fold_index])
                self.assertEqual((sku_test[0]["STEP"], sku_test[-1]["STEP"]), expected_test_steps[fold_index])
                self.assertLess(max(row["DATA_EVENTO"] for row in sku_train), min(row["DATA_EVENTO"] for row in sku_test))

    def test_rolling_origin_rejects_configuration_with_insufficient_training_history(self) -> None:
        rows = []
        for day in range(1, 21):
            rows.append({"ID_PRODUTO": "A", "DATA_EVENTO": date.fromordinal(date(2024, 1, 1).toordinal() + day - 1)})
        with self.assertRaises(ValueError):
            rolling_origin_folds(rows, horizon=7, n_folds=2, min_train_size=14)

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

    def test_probabilistic_metrics_measure_coverage_width_pinball_and_crossing(self) -> None:
        actual = [5.0, 10.0, 20.0, 30.0]
        p10 = [4.0, 8.0, 18.0, 28.0]
        p50 = [5.0, 10.0, 21.0, 31.0]
        p90 = [6.0, 12.0, 22.0, 32.0]

        self.assertEqual(interval_coverage(actual, p10, p90), 1.0)
        self.assertEqual(mean_interval_width(p10, p90), 3.0)
        self.assertEqual(quantile_crossing_count({0.1: p10, 0.5: p50, 0.9: p90}), 0)
        self.assertGreater(pinball_loss(actual, p10, 0.1), 0.0)
        self.assertEqual(
            quantile_crossing_count({0.1: [5.0], 0.5: [4.0], 0.9: [6.0]}),
            1,
        )


if __name__ == "__main__":
    unittest.main()
