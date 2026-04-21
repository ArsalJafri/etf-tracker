import unittest

from src.data_fetcher.universe import build

MOCK_HOLDINGS = {
    "VTI": [
        {"asset": "AAPL", "name": "Apple Inc.", "weightPercentage": 6.5},
        {"asset": "MSFT", "name": "Microsoft",  "weightPercentage": 5.8},
    ],
    "VGT": [
        {"asset": "AAPL", "name": "Apple Inc.", "weightPercentage": 7.2},
        {"asset": "NVDA", "name": "Nvidia",     "weightPercentage": 8.1},
    ],
}


class TestBuild(unittest.TestCase):

    def setUp(self):
        self.universe = build(MOCK_HOLDINGS)

    def test_contains_all_unique_stocks(self):
        self.assertIn("AAPL", self.universe)
        self.assertIn("MSFT", self.universe)
        self.assertIn("NVDA", self.universe)

    def test_etf_count_reflects_appearances(self):
        self.assertEqual(self.universe["AAPL"]["etfCount"], 2)
        self.assertEqual(self.universe["MSFT"]["etfCount"], 1)

    def test_avg_weight_is_mean_across_holding_etfs(self):
        self.assertAlmostEqual(self.universe["AAPL"]["avgWeight"], round((6.5 + 7.2) / 2, 6))

    def test_single_etf_avg_weight_equals_its_weight(self):
        self.assertAlmostEqual(self.universe["NVDA"]["avgWeight"], 8.1)

    def test_etfs_list_tracks_which_etfs_hold_stock(self):
        self.assertIn("VTI", self.universe["AAPL"]["etfs"])
        self.assertIn("VGT", self.universe["AAPL"]["etfs"])

    def test_weights_key_removed_from_output(self):
        self.assertNotIn("weights", self.universe["AAPL"])

    def test_empty_holdings_returns_empty_universe(self):
        self.assertEqual(build({}), {})

    def test_etf_with_no_stocks_is_skipped(self):
        result = build({"VTI": [], "VGT": MOCK_HOLDINGS["VGT"]})
        self.assertIn("NVDA", result)
        self.assertNotIn("MSFT", result)


if __name__ == "__main__":
    unittest.main()