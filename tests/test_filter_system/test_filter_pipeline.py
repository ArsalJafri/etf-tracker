import unittest
from unittest.mock import patch

from src.filter_system.filter_pipeline import apply_filter

MOCK_BLACKLIST = {
    "tickers": ["PLTR", "JPM"],
    "reasons": {"PLTR": "defense/surveillance", "JPM": "interest-based financial"}
}

MOCK_UNIVERSE = {
    "AAPL": {"name": "Apple Inc.", "avgWeight": 40.0, "etfCount": 3, "etfs": ["VTI"]},
    "MSFT": {"name": "Microsoft",  "avgWeight": 30.0, "etfCount": 2, "etfs": ["VTI"]},
    "PLTR": {"name": "Palantir",   "avgWeight": 20.0, "etfCount": 1, "etfs": ["QQQ"]},
    "JPM":  {"name": "JPMorgan",   "avgWeight": 10.0, "etfCount": 1, "etfs": ["VTI"]},
}


class TestApplyFilter(unittest.TestCase):

    @patch("src.filter_system.filter_pipeline.load_blacklist")
    def test_removes_blacklisted_stocks(self, mock_load):
        mock_load.return_value = MOCK_BLACKLIST
        result = apply_filter(MOCK_UNIVERSE)
        self.assertNotIn("PLTR", result)
        self.assertNotIn("JPM", result)

    @patch("src.filter_system.filter_pipeline.load_blacklist")
    def test_weights_sum_to_100_after_filter(self, mock_load):
        mock_load.return_value = MOCK_BLACKLIST
        total = sum(d["avgWeight"] for d in apply_filter(MOCK_UNIVERSE).values())
        self.assertAlmostEqual(total, 100.0, places=4)

    @patch("src.filter_system.filter_pipeline.load_blacklist")
    def test_returns_full_universe_when_blacklist_empty(self, mock_load):
        mock_load.return_value = {"tickers": [], "reasons": {}}
        self.assertEqual(len(apply_filter(MOCK_UNIVERSE)), len(MOCK_UNIVERSE))

    @patch("src.filter_system.filter_pipeline.load_blacklist")
    def test_returns_empty_dict_when_all_stocks_removed(self, mock_load):
        mock_load.return_value = {"tickers": list(MOCK_UNIVERSE.keys()), "reasons": {}}
        self.assertEqual(apply_filter(MOCK_UNIVERSE), {})


if __name__ == "__main__":
    unittest.main()