import unittest

from src.change_detector.change_aggregator import diff_all, aggregate_changes

OLD_SNAP = {
    "etfs": {
        "VTI": [
            {"asset": "AAPL", "name": "Apple",     "weightPercentage": 6.5},
            {"asset": "MSFT", "name": "Microsoft", "weightPercentage": 5.8},
        ],
        "VGT": [
            {"asset": "AAPL", "name": "Apple",     "weightPercentage": 7.2},
            {"asset": "INTC", "name": "Intel",     "weightPercentage": 2.1},
        ],
    }
}

NEW_SNAP = {
    "etfs": {
        "VTI": [
            {"asset": "AAPL", "name": "Apple",   "weightPercentage": 6.8},
            {"asset": "NVDA", "name": "Nvidia",  "weightPercentage": 8.1},
        ],
        "VGT": [
            {"asset": "AAPL", "name": "Apple",   "weightPercentage": 7.5},
            {"asset": "NVDA", "name": "Nvidia",  "weightPercentage": 9.0},
        ],
    }
}


class TestDiffAll(unittest.TestCase):

    def test_returns_diff_for_each_etf(self):
        result = diff_all(OLD_SNAP, NEW_SNAP)
        self.assertIn("VTI", result)
        self.assertIn("VGT", result)

    def test_detects_addition_in_etf(self):
        result = diff_all(OLD_SNAP, NEW_SNAP)
        self.assertIn("NVDA", result["VTI"]["added"])

    def test_detects_removal_in_etf(self):
        result = diff_all(OLD_SNAP, NEW_SNAP)
        self.assertIn("MSFT", result["VTI"]["removed"])

    def test_handles_etf_present_in_only_one_snapshot(self):
        old = {"etfs": {"VTI": [{"asset": "AAPL", "name": "Apple", "weightPercentage": 6.5}]}}
        new = {"etfs": {}}
        result = diff_all(old, new)
        self.assertIn("VTI", result)
        self.assertIn("AAPL", result["VTI"]["removed"])


class TestAggregateChanges(unittest.TestCase):

    def setUp(self):
        per_etf = diff_all(OLD_SNAP, NEW_SNAP)
        self.changes = aggregate_changes(per_etf)

    def test_added_stock_appears_in_added(self):
        self.assertIn("NVDA", self.changes["added"])

    def test_removed_stock_appears_in_removed(self):
        self.assertIn("MSFT", self.changes["removed"])
        self.assertIn("INTC", self.changes["removed"])

    def test_etf_count_reflects_how_many_etfs_added_stock(self):
        self.assertEqual(self.changes["added"]["NVDA"]["etfCount"], 2)

    def test_etfs_list_contains_correct_etfs(self):
        self.assertIn("VTI", self.changes["added"]["NVDA"]["etfs"])
        self.assertIn("VGT", self.changes["added"]["NVDA"]["etfs"])

    def test_unchanged_stock_not_in_added_or_removed(self):
        self.assertNotIn("AAPL", self.changes["added"])
        self.assertNotIn("AAPL", self.changes["removed"])

    def test_returns_empty_dicts_when_no_changes(self):
        result = aggregate_changes({"VTI": {"added": set(), "removed": set()}})
        self.assertEqual(result["added"], {})
        self.assertEqual(result["removed"], {})


if __name__ == "__main__":
    unittest.main()
