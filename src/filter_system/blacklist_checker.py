def is_blacklisted(ticker: str, blacklist: dict) -> bool:
    return ticker.upper() in [t.upper() for t in blacklist.get("tickers", [])]
