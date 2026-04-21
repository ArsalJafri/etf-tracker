import unittest
from unittest.mock import patch
import pandas as pd

from src.data_fetcher.fetcher import fetch_holdings, fetch_all, _parse_holdings, _parse_row


MOCK_HOLDINGS_DF = pd.DataFrame(
    [{"Name": "Apple Inc.", "Holding Percent": 0.065}],
    index=["AAPL"]
)


class TestParseRow(unittest.TestCase):

    def test_uppercases_symbol(self):
        result = _parse_row("aapl", {"Name": "Apple", "Holding Percent": 0.065})
        self.assertEqual(result["asset"], "AAPL")

    def test_converts_holding_percent_to_percentage(self):
        result = _parse_row("AAPL", {"Name": "Apple", "Holding Percent": 0.065})
        self.assertAlmostEqual(result["weightPercentage"], 6.5)

    def test_defaults_missing_name_to_empty_string(self):
        result = _parse_row("AAPL", {"Holding Percent": 0.065})
        self.assertEqual(result["name"], "")


class TestParseHoldings(unittest.TestCase):

    def test_returns_empty_on_none(self):
        self.assertEqual(_parse_holdings(None), [])

    def test_returns_empty_on_empty_dataframe(self):
        self.assertEqual(_parse_holdings(pd.DataFrame()), [])

    def test_parses_valid_dataframe(self):
        result = _parse_holdings(MOCK_HOLDINGS_DF)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["asset"], "AAPL")


class TestFetchHoldings(unittest.TestCase):

    @patch("src.data_fetcher.fetcher.yf.Ticker")
    def test_returns_parsed_holdings(self, mock_ticker):
        mock_ticker.return_value.funds_data.top_holdings = MOCK_HOLDINGS_DF
        result = fetch_holdings("VTI")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["asset"], "AAPL")
        self.assertAlmostEqual(result[0]["weightPercentage"], 6.5)

    @patch("src.data_fetcher.fetcher.yf.Ticker")
    def test_returns_empty_on_none_data(self, mock_ticker):
        mock_ticker.return_value.funds_data.top_holdings = None
        self.assertEqual(fetch_holdings("VTI"), [])

    @patch("src.data_fetcher.fetcher.yf.Ticker")
    def test_returns_empty_on_exception(self, mock_ticker):
        mock_ticker.side_effect = Exception("network error")
        self.assertEqual(fetch_holdings("VTI"), [])


class TestFetchAll(unittest.TestCase):

    @patch("src.data_fetcher.fetcher.fetch_holdings")
    def test_fetches_all_provided_etfs(self, mock_fetch):
        mock_fetch.return_value = [{"asset": "AAPL", "name": "Apple", "weightPercentage": 6.5}]
        result = fetch_all(["VTI", "VGT"])
        self.assertIn("VTI", result)
        self.assertIn("VGT", result)
        self.assertEqual(mock_fetch.call_count, 2)

    @patch("src.data_fetcher.fetcher.fetch_holdings")
    def test_failed_etf_returns_empty_list(self, mock_fetch):
        mock_fetch.return_value = []
        self.assertEqual(fetch_all(["VTI"])["VTI"], [])


if __name__ == "__main__":
    unittest.main()
