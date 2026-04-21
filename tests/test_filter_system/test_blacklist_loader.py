import unittest
import json
import tempfile
from pathlib import Path

import src.filter_system.blacklist_loader as blacklist_loader
from src.filter_system.blacklist_loader import load_blacklist

MOCK_BLACKLIST = {
    "tickers": ["PLTR", "JPM"],
    "reasons": {"PLTR": "defense/surveillance", "JPM": "interest-based financial"}
}


class TestLoadBlacklist(unittest.TestCase):

    def setUp(self):
        self.original_path = blacklist_loader.BLACKLIST_PATH

    def tearDown(self):
        blacklist_loader.BLACKLIST_PATH = self.original_path

    def test_loads_tickers_from_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "blacklist.json"
            path.write_text(json.dumps(MOCK_BLACKLIST))
            blacklist_loader.BLACKLIST_PATH = path
            self.assertEqual(load_blacklist()["tickers"], ["PLTR", "JPM"])

    def test_loads_reasons_from_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "blacklist.json"
            path.write_text(json.dumps(MOCK_BLACKLIST))
            blacklist_loader.BLACKLIST_PATH = path
            self.assertEqual(load_blacklist()["reasons"]["PLTR"], "defense/surveillance")

    def test_returns_empty_tickers_when_file_missing(self):
        blacklist_loader.BLACKLIST_PATH = Path("/nonexistent/blacklist.json")
        self.assertEqual(load_blacklist()["tickers"], [])

    def test_returns_empty_reasons_when_file_missing(self):
        blacklist_loader.BLACKLIST_PATH = Path("/nonexistent/blacklist.json")
        self.assertEqual(load_blacklist()["reasons"], {})


if __name__ == "__main__":
    unittest.main()
