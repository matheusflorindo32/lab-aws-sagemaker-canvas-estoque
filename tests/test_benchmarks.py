import unittest

from src.inventory_forecasting.baselines import drift_forecast, naive_forecast, seasonal_naive_forecast


class BaselineTests(unittest.TestCase):
    def test_naive_repeats_last_observation(self) -> None:
        self.assertEqual(naive_forecast([1, 3, 5], horizon=3), [5.0, 5.0, 5.0])

    def test_seasonal_naive_repeats_last_season(self) -> None:
        history = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertEqual(seasonal_naive_forecast(history, horizon=4, season_length=3), [7.0, 8.0, 9.0, 7.0])

    def test_drift_extends_line_from_first_to_last(self) -> None:
        self.assertEqual(drift_forecast([1, 2, 3], horizon=3), [4.0, 5.0, 6.0])


if __name__ == "__main__":
    unittest.main()
