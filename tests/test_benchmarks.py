import unittest
from datetime import date

from src.inventory_forecasting.baselines import drift_forecast, naive_forecast, seasonal_naive_forecast
from src.inventory_forecasting.benchmark import run_benchmarks_multifold, run_future_forecast


class BaselineTests(unittest.TestCase):
    def test_naive_repeats_last_observation(self) -> None:
        self.assertEqual(naive_forecast([1, 3, 5], horizon=3), [5.0, 5.0, 5.0])

    def test_seasonal_naive_repeats_last_season(self) -> None:
        history = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertEqual(seasonal_naive_forecast(history, horizon=4, season_length=3), [7.0, 8.0, 9.0, 7.0])

    def test_drift_extends_line_from_first_to_last(self) -> None:
        self.assertEqual(drift_forecast([1, 2, 3], horizon=3), [4.0, 5.0, 6.0])

    def test_multifold_benchmark_reports_fold_metrics_summary_and_predictions(self) -> None:
        rows = []
        start = date(2024, 1, 1)
        for sku_index, sku in enumerate(("A", "B")):
            for step in range(40):
                rows.append(
                    {
                        "ID_PRODUTO": sku,
                        "DATA_EVENTO": date.fromordinal(start.toordinal() + step),
                        "PRECO": 10.0 + sku_index,
                        "FLAG_PROMOCAO": step % 5 == 0,
                        "QUANTIDADE_ESTOQUE": float(100 - ((step + sku_index) % 20)),
                    }
                )

        fold_metrics, summary, predictions = run_benchmarks_multifold(rows, horizon=7, n_folds=3, min_train_size=14)

        self.assertEqual(len(fold_metrics), 3 * 3)
        self.assertEqual(len(summary), 3)
        self.assertEqual(len(predictions), 3 * 3 * 2 * 7)
        self.assertTrue(all("fold" in row for row in fold_metrics))
        self.assertTrue(all("MACRO_MASE" in row for row in fold_metrics))
        self.assertTrue(all("WAPE_mean" in row and "WAPE_median" in row and "WAPE_stdev" in row for row in summary))

    def test_future_forecast_starts_after_last_observation_and_has_no_actuals(self) -> None:
        rows = []
        start = date(2024, 1, 1)
        for sku in ("A", "B"):
            for step in range(10):
                rows.append(
                    {
                        "ID_PRODUTO": sku,
                        "DATA_EVENTO": date.fromordinal(start.toordinal() + step),
                        "PRECO": 10.0,
                        "FLAG_PROMOCAO": False,
                        "QUANTIDADE_ESTOQUE": float(100 - step),
                    }
                )

        predictions = run_future_forecast(rows, horizon=3, model_name="Naive")

        self.assertEqual(len(predictions), 2 * 3)
        self.assertEqual(predictions[0]["DATA_EVENTO"], "2024-01-11")
        self.assertEqual(predictions[-1]["DATA_EVENTO"], "2024-01-13")
        self.assertTrue(all("actual" not in row for row in predictions))
        self.assertTrue(all(row["P10"] <= row["P50"] <= row["P90"] for row in predictions))


if __name__ == "__main__":
    unittest.main()
