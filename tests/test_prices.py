import unittest
from unittest.mock import patch
import pandas as pd

import sys
sys.path.insert(0, "src")

from prices import fetch_prices


MOCK_HISTORY = pd.DataFrame({"Close": [188.50, 189.30]})


class TestFetchPrices(unittest.TestCase):

    @patch("prices.yf.Ticker")
    def test_returns_price_for_valid_ticker(self, mock_ticker):
        mock_ticker.return_value.history.return_value = MOCK_HISTORY

        result = fetch_prices(["AAPL"])

        self.assertIn("AAPL", result)
        self.assertEqual(result["AAPL"], 189.30)

    @patch("prices.yf.Ticker")
    def test_returns_empty_on_empty_history(self, mock_ticker):
        mock_ticker.return_value.history.return_value = pd.DataFrame()

        result = fetch_prices(["AAPL"])

        self.assertEqual(result, {})

    @patch("prices.yf.Ticker")
    def test_skips_failed_ticker(self, mock_ticker):
        mock_ticker.side_effect = Exception("timeout")

        result = fetch_prices(["AAPL"])

        self.assertNotIn("AAPL", result)

    def test_returns_empty_on_no_tickers(self):
        result = fetch_prices([])

        self.assertEqual(result, {})

    @patch("prices.yf.Ticker")
    def test_fetches_multiple_tickers(self, mock_ticker):
        mock_ticker.return_value.history.return_value = MOCK_HISTORY

        result = fetch_prices(["AAPL", "MSFT"])

        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
