import unittest
from unittest.mock import patch

from src.change_detector.detector_pipeline import detect

MOCK_PREVIOUS = {
    "date": "2026-04-12",
    "etfs": {
        "VTI": [{"asset": "AAPL", "name": "Apple", "weightPercentage": 6.5}]
    }
}

MOCK_CURRENT = {
    "date": "2026-04-19",
    "etfs": {
        "VTI": [{"asset": "NVDA", "name": "Nvidia", "weightPercentage": 8.1}]
    }
}


class TestDetect(unittest.TestCase):

    @patch("src.change_detector.detector_pipeline.load_two_latest")
    def test_returns_added_and_removed_keys(self, mock_load):
        mock_load.return_value = (MOCK_PREVIOUS, MOCK_CURRENT)

        result = detect()

        self.assertIn("added", result)
        self.assertIn("removed", result)

    @patch("src.change_detector.detector_pipeline.load_two_latest")
    def test_detects_added_stock(self, mock_load):
        mock_load.return_value = (MOCK_PREVIOUS, MOCK_CURRENT)

        result = detect()

        self.assertIn("NVDA", result["added"])

    @patch("src.change_detector.detector_pipeline.load_two_latest")
    def test_detects_removed_stock(self, mock_load):
        mock_load.return_value = (MOCK_PREVIOUS, MOCK_CURRENT)

        result = detect()

        self.assertIn("AAPL", result["removed"])

    @patch("src.change_detector.detector_pipeline.load_two_latest")
    def test_returns_empty_when_no_snapshots(self, mock_load):
        mock_load.return_value = (None, None)

        result = detect()

        self.assertEqual(result, {"added": {}, "removed": {}})

    @patch("src.change_detector.detector_pipeline.load_two_latest")
    def test_returns_empty_when_no_changes(self, mock_load):
        mock_load.return_value = (MOCK_PREVIOUS, MOCK_PREVIOUS)

        result = detect()

        self.assertEqual(result["added"], {})
        self.assertEqual(result["removed"], {})


if __name__ == "__main__":
    unittest.main()
