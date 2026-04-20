import unittest
from unittest.mock import patch

import sys
sys.path.insert(0, "src")

from pipeline import run


MOCK_HOLDINGS = {
    "VTI": [{"asset": "AAPL", "name": "Apple Inc.", "weightPercentage": 6.5}],
}

MOCK_UNIVERSE = {
    "AAPL": {"name": "Apple Inc.", "avgWeight": 6.5, "etfCount": 1, "etfs": ["VTI"]},
}


class TestRun(unittest.TestCase):

    @patch("pipeline.build")
    @patch("pipeline.save")
    @patch("pipeline.fetch_all")
    def test_calls_all_stages_in_order(self, mock_fetch, mock_save, mock_build):
        mock_fetch.return_value = MOCK_HOLDINGS
        mock_build.return_value = MOCK_UNIVERSE

        run()

        mock_fetch.assert_called_once()
        mock_save.assert_called_once_with(MOCK_HOLDINGS)
        mock_build.assert_called_once_with(MOCK_HOLDINGS)

    @patch("pipeline.fetch_all")
    def test_returns_empty_when_all_fetches_fail(self, mock_fetch):
        mock_fetch.return_value = {"VTI": [], "VGT": []}

        result = run()

        self.assertEqual(result, {})

    @patch("pipeline.build")
    @patch("pipeline.save")
    @patch("pipeline.fetch_all")
    def test_returns_universe_from_build(self, mock_fetch, mock_save, mock_build):
        mock_fetch.return_value = MOCK_HOLDINGS
        mock_build.return_value = MOCK_UNIVERSE

        result = run()

        self.assertEqual(result, MOCK_UNIVERSE)

    @patch("pipeline.build")
    @patch("pipeline.save")
    @patch("pipeline.fetch_all")
    def test_does_not_save_when_all_fetches_fail(self, mock_fetch, mock_save, mock_build):
        mock_fetch.return_value = {"VTI": [], "VGT": []}

        run()

        mock_save.assert_not_called()


if __name__ == "__main__":
    unittest.main()
