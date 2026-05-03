def _ticker_set(holdings: list[dict]) -> set[str]:
    return {h["asset"] for h in holdings}


def diff_etf(old_holdings: list[dict], new_holdings: list[dict]) -> dict:
    old_tickers = _ticker_set(old_holdings)
    new_tickers  = _ticker_set(new_holdings)

    return {
        "added":   new_tickers - old_tickers,
        "removed": old_tickers - new_tickers,
    }
