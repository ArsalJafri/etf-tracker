import json
import logging
import src.data_fetcher.snapshot as snapshot_module

log = logging.getLogger(__name__)


def load_two_latest() -> tuple[dict | None, dict | None]:
    snapshots = sorted(snapshot_module.SNAPSHOT_DIR.glob("*.json"))

    if len(snapshots) < 2:
        log.warning("Need at least 2 snapshots to diff — found %d", len(snapshots))
        return None, None

    previous = json.loads(snapshots[-2].read_text())
    current  = json.loads(snapshots[-1].read_text())

    log.info("Loaded snapshots: %s vs %s", snapshots[-2].name, snapshots[-1].name)
    return previous, current
