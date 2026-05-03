from src.change_detector.etf_differ import diff_etf


def diff_all(old_snap: dict, new_snap: dict) -> dict[str, dict]:
    old_etfs = old_snap.get("etfs", {})
    new_etfs = new_snap.get("etfs", {})
    etfs = set(old_etfs) | set(new_etfs)

    return {
        etf: diff_etf(old_etfs.get(etf, []), new_etfs.get(etf, []))
        for etf in etfs
    }


def _accumulate(ticker_map: dict, tickers: set, etf: str) -> None:
    for ticker in tickers:
        ticker_map.setdefault(ticker, []).append(etf)


def _to_signal(ticker_map: dict) -> dict:
    return {t: {"etfs": etfs, "etfCount": len(etfs)} for t, etfs in ticker_map.items()}


def aggregate_changes(per_etf_diffs: dict[str, dict]) -> dict:
    added   = {}
    removed = {}

    for etf, diff in per_etf_diffs.items():
        _accumulate(added,   diff["added"],   etf)
        _accumulate(removed, diff["removed"], etf)

    return {"added": _to_signal(added), "removed": _to_signal(removed)}
