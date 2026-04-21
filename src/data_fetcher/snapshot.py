import json
import logging
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Optional

log = logging.getLogger(__name__)

SNAPSHOT_DIR = Path(__file__).parent.parent / "data" / "etf_snapshots"


def save(holdings: dict[str, list[dict]], snapshot_date: date = None) -> Path:
    snapshot_date = snapshot_date or date.today()
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

    path = SNAPSHOT_DIR / f"{snapshot_date.isoformat()}.json"
    payload = {
        "date":      snapshot_date.isoformat(),
        "fetchedAt": datetime.now(timezone.utc).isoformat(),
        "etfs":      holdings,
    }

    path.write_text(json.dumps(payload, indent=2))
    log.info("Snapshot saved -> %s", path)
    return path


def load(snapshot_date: date) -> Optional[dict]:
    path = SNAPSHOT_DIR / f"{snapshot_date.isoformat()}.json"
    if not path.exists():
        log.warning("No snapshot found for %s", snapshot_date.isoformat())
        return None
    return json.loads(path.read_text())


def load_latest() -> Optional[dict]:
    snapshots = sorted(SNAPSHOT_DIR.glob("*.json"))
    if not snapshots:
        log.warning("No snapshots in %s", SNAPSHOT_DIR)
        return None
    log.info("Loading snapshot: %s", snapshots[-1].name)
    return json.loads(snapshots[-1].read_text())
