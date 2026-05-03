import logging
from src.change_detector.snapshot_loader import load_two_latest
from src.change_detector.change_aggregator import diff_all, aggregate_changes

log = logging.getLogger(__name__)


def detect() -> dict:
    previous, current = load_two_latest()

    if not previous or not current:
        log.warning("Cannot detect changes — insufficient snapshots")
        return {"added": {}, "removed": {}}

    per_etf = diff_all(previous, current)
    changes  = aggregate_changes(per_etf)

    log.info(
        "Detected %d additions and %d removals across tracked ETFs",
        len(changes["added"]),
        len(changes["removed"]),
    )

    return changes
