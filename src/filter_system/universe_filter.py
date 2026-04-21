import logging
from src.filter_system.blacklist_checker import is_blacklisted

log = logging.getLogger(__name__)


def _removed_tickers(universe: dict, blacklist: dict) -> set:
    return {t for t in universe if is_blacklisted(t, blacklist)}


def _log_removals(removed: set, blacklist: dict) -> None:
    for ticker in removed:
        reason = blacklist.get("reasons", {}).get(ticker, "no reason specified")
        log.info("Removed %s — %s", ticker, reason)


def filter_universe(universe: dict, blacklist: dict) -> dict:
    removed = _removed_tickers(universe, blacklist)
    _log_removals(removed, blacklist)
    return {t: data for t, data in universe.items() if t not in removed}