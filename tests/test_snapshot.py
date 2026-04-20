import unittest
import json
import tempfile
from datetime import date
from pathlib import Path

import sys
sys.path.insert(0, "src")

import snapshot


MOCK_HOLDINGS = {
    "VTI": [{"asset": "AAPL", "name": "Apple Inc.", "weightPercentage": 6.5}],
    "VGT": [{"asset": "NVDA", "name": "Nvidia",     "weightPercentage": 8.1}],
}


class TestSave(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.original_dir = snapshot.SNAPSHOT_DIR
        snapshot.SNAPSHOT_DIR = Path(self.tmp.name)

    def tearDown(self):
        snapshot.SNAPSHOT_DIR = self.original_dir
        self.tmp.cleanup()

    def test_creates_json_file_named_by_date(self):
        path = snapshot.save(MOCK_HOLDINGS, date(2026, 4, 19))

        self.assertTrue(path.exists())
        self.assertEqual(path.name, "2026-04-19.json")

    def test_saved_file_contains_holdings(self):
        snapshot.save(MOCK_HOLDINGS, date(2026, 4, 19))
        data = json.loads((snapshot.SNAPSHOT_DIR / "2026-04-19.json").read_text())

        self.assertEqual(data["etfs"]["VTI"][0]["asset"], "AAPL")

    def test_defaults_to_today(self):
        path = snapshot.save(MOCK_HOLDINGS)

        self.assertEqual(path.name, f"{date.today().isoformat()}.json")


class TestLoad(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.original_dir = snapshot.SNAPSHOT_DIR
        snapshot.SNAPSHOT_DIR = Path(self.tmp.name)
        snapshot.save(MOCK_HOLDINGS, date(2026, 4, 19))

    def tearDown(self):
        snapshot.SNAPSHOT_DIR = self.original_dir
        self.tmp.cleanup()

    def test_loads_saved_snapshot(self):
        result = snapshot.load(date(2026, 4, 19))

        self.assertIsNotNone(result)
        self.assertIn("VTI", result["etfs"])

    def test_returns_none_for_missing_date(self):
        result = snapshot.load(date(2000, 1, 1))

        self.assertIsNone(result)

    def test_load_latest_returns_most_recent(self):
        snapshot.save(MOCK_HOLDINGS, date(2026, 4, 20))

        result = snapshot.load_latest()

        self.assertEqual(result["date"], "2026-04-20")

    def test_load_latest_returns_none_when_empty(self):
        snapshot.SNAPSHOT_DIR = Path(self.tmp.name) / "empty"
        snapshot.SNAPSHOT_DIR.mkdir()

        result = snapshot.load_latest()

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
