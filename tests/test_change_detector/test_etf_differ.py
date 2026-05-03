import unittest

from src.change_detector.etf_differ import diff_etf

OLD = [
    {"asset": "AAPL", "name": "Apple",   "weightPercentage": 6.5},
    {"asset": "MSFT", "name": "Microsoft","weightPercentage": 5.8},
]

NEW = [
    {"asset": "AAPL", "name": "Apple",   "weightPercentage": 6.8},
    {"asset": "NVDA", "name": "Nvidia",  "weightPercentage": 8.1},
]


class TestDiffEtf(unittest.TestCase):

    def test_detects_added_ticker(self):
        result = diff_etf(OLD, NEW)
        self.assertIn("NVDA", result["added"])

    def test_detects_removed_ticker(self):
        result = diff_etf(OLD, NEW)
        self.assertIn("MSFT", result["removed"])

    def test_unchanged_ticker_not_in_added_or_removed(self):
        result = diff_etf(OLD, NEW)
        self.assertNotIn("AAPL", result["added"])
        self.assertNotIn("AAPL", result["removed"])

    def test_returns_empty_sets_when_holdings_identical(self):
        result = diff_etf(OLD, OLD)
        self.assertEqual(result["added"], set())
        self.assertEqual(result["removed"], set())

    def test_all_tickers_added_when_old_is_empty(self):
        result = diff_etf([], NEW)
        self.assertEqual(result["added"], {"AAPL", "NVDA"})
        self.assertEqual(result["removed"], set())

    def test_all_tickers_removed_when_new_is_empty(self):
        result = diff_etf(OLD, [])
        self.assertEqual(result["removed"], {"AAPL", "MSFT"})
        self.assertEqual(result["added"], set())


if __name__ == "__main__":
    unittest.main()
