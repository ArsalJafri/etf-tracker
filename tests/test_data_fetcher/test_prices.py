import unittest
from unittest.mock import patch
import pandas as pd

from src.data_fetcher.prices import fetch_prices

MOCK_HISTORY = pd.DataFrame({"Close": [188.50, 189.30]})


class TestFetchPrices(unittest.TestCase):

    @patch("src.data_fetcher.prices.yf.Ticker")
    def test_returns_price_for_valid_ticker(self, mock_ticker):
        mock_ticker.return_value.history.return_value = MOCK_HISTORY
        result = fetch_prices(["AAPL"])
        self.assertIn("AAPL", result)
        self.assertEqual(result["AAPL"], 189.30)

    @patch("src.data_fetcher.prices.yf.Ticker")
    def test_returns_empty_on_empty_history(self, mock_ticker):
        mock_ticker.return_value.history.return_value = pd.DataFrame()
        self.assertEqual(fetch_prices(["AAPL"]), {})

    @patch("src.data_fetcher.prices.yf.Ticker")
    def test_skips_failed_ticker(self, mock_ticker):
        mock_ticker.side_effect = Exception("timeout")
        self.assertNotIn("AAPL", fetch_prices(["AAPL"]))

    def test_returns_empty_on_no_tickers(self):
        self.assertEqual(fetch_prices([]), {})

    @patch("src.data_fetcher.prices.yf.Ticker")
    def test_fetches_multiple_tickers(self, mock_ticker):
        mock_ticker.return_value.history.return_value = MOCK_HISTORY
        self.assertEqual(len(fetch_prices(["AAPL", "MSFT"])), 2)


if __name__ == "__main__":
    unittest.main()