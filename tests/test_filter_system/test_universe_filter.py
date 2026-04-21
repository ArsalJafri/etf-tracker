import unittest

from src.filter_system.blacklist_checker import is_blacklisted

MOCK_BLACKLIST = {
    "tickers": ["PLTR", "JPM"],
    "reasons": {"PLTR": "defense/surveillance", "JPM": "interest-based financial"}
}


class TestIsBlacklisted(unittest.TestCase):

    def test_returns_true_for_blacklisted_ticker(self):
        self.assertTrue(is_blacklisted("PLTR", MOCK_BLACKLIST))

    def test_returns_false_for_clean_ticker(self):
        self.assertFalse(is_blacklisted("AAPL", MOCK_BLACKLIST))

    def test_is_case_insensitive(self):
        self.assertTrue(is_blacklisted("pltr", MOCK_BLACKLIST))

    def test_returns_false_on_empty_blacklist(self):
        self.assertFalse(is_blacklisted("PLTR", {"tickers": [], "reasons": {}}))


if __name__ == "__main__":
    unittest.main()