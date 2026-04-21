import logging
from src.filter_system.blacklist_loader import load_blacklist
from src.filter_system.universe_filter import filter_universe
from src.filter_system.weight_redistributor import redistribute_weights

log = logging.getLogger(__name__)


def apply_filter(universe: dict) -> dict:
    blacklist = load_blacklist()
    filtered = filter_universe(universe, blacklist)
    redistributed = redistribute_weights(filtered)
    log.info(
        "Filter complete — %d stocks removed, %d remaining",
        len(universe) - len(filtered),
        len(redistributed),
    )
    return redistributed