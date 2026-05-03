import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import json
import tempfile

import src.data_fetcher.snapshot as snapshot_module
from src.change_detector.snapshot_loader import load_two_latest

SNAP_A = {"date": "2026-04-12", "etfs": {"VTI": [{"asset": "AAPL", "name": "Apple", "weightPercentage": 6.5}]}}
SNAP_B = {"date": "2026-04-19", "etfs": {"VTI": [{"asset": "NVDA", "name": "Nvidia", "weightPercentage": 8.1}]}}


class TestLoadTwoLatest(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.original_dir = snapshot_module.SNAPSHOT_DIR
        snapshot_module.SNAPSHOT_DIR = Path(self.tmp.name)

    def tearDown(self):
        snapshot_module.SNAPSHOT_DIR = self.original_dir
        self.tmp.cleanup()

    def test_returns_two_snapshots_in_chronological_order(self):
        (Path(self.tmp.name) / "2026-04-12.json").write_text(json.dumps(SNAP_A))
        (Path(self.tmp.name) / "2026-04-19.json").write_text(json.dumps(SNAP_B))

        previous, current = load_two_latest()

        self.assertEqual(previous["date"], "2026-04-12")
        self.assertEqual(current["date"], "2026-04-19")

    def test_returns_none_none_when_only_one_snapshot(self):
        (Path(self.tmp.name) / "2026-04-19.json").write_text(json.dumps(SNAP_B))

        previous, current = load_two_latest()

        self.assertIsNone(previous)
        self.assertIsNone(current)

    def test_returns_none_none_when_no_snapshots(self):
        previous, current = load_two_latest()

        self.assertIsNone(previous)
        self.assertIsNone(current)


if __name__ == "__main__":
    unittest.main()
