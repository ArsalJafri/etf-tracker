import logging
import yfinance as yf

log = logging.getLogger(__name__)

TARGET_ETFS = [
    "VTI",   # Vanguard Total Stock Market
    "VGT",   # Vanguard Information Technology
    "QQQ",   # Invesco Nasdaq-100
    "SCHG",  # Schwab US Large-Cap Growth
    "VOO",   # Vanguard S&P 500
    "SPUS",  # SP Funds S&P 500 Shariah
    "ARKK",  # ARK Innovation
    "VUG",   # Vanguard Growth
    "SMH",   # Semi conductor stock
]


def _parse_row(symbol, row) -> dict:
    return {
        "asset":            symbol.upper().strip(),
        "name":             str(row.get("Name", "")),
        "weightPercentage": round(float(row.get("Holding Percent", 0)) * 100, 6),
    }


def _parse_holdings(data) -> list[dict]:
    if data is None or data.empty:
        return []
    return [_parse_row(symbol, row) for symbol, row in data.iterrows() if symbol]


def fetch_holdings(ticker: str) -> list[dict]:
    log.info("Fetching holdings for %s", ticker)
    try:
        data = yf.Ticker(ticker).funds_data.top_holdings
        holdings = _parse_holdings(data)
        if not holdings:
            log.warning("No holdings returned for %s", ticker)
        return holdings
    except Exception as e:
        log.error("Failed to fetch %s: %s", ticker, e)
        return []


def fetch_all(etfs: list[str] = TARGET_ETFS) -> dict[str, list[dict]]:
    results = {ticker: fetch_holdings(ticker) for ticker in etfs}
    fetched = sum(1 for v in results.values() if v)
    log.info("Fetched %d/%d ETFs successfully", fetched, len(etfs))
    return results
