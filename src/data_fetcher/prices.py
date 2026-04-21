import logging
import yfinance as yf

log = logging.getLogger(__name__)


def fetch_prices(tickers: list[str]) -> dict[str, float]:
    if not tickers:
        return {}

    log.info("Fetching prices for %d tickers", len(tickers))
    prices = {}

    for ticker in tickers:
        try:
            history = yf.Ticker(ticker).history(period="2d")
            if not history.empty:
                prices[ticker] = round(float(history["Close"].dropna().iloc[-1]), 4)
        except Exception as e:
            log.warning("No price data for %s: %s", ticker, e)

    log.info("Prices fetched for %d/%d tickers", len(prices), len(tickers))
    return prices
