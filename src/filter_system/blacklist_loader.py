import json
import logging
from pathlib import Path

log = logging.getLogger(__name__)

BLACKLIST_PATH = Path(__file__).parent.parent.parent / "data" / "blacklist.json"


def load_blacklist() -> dict:
    if not BLACKLIST_PATH.exists():
        log.warning("blacklist.json not found — proceeding with empty blacklist")
        return {"tickers": [], "reasons": {}}
    return json.loads(BLACKLIST_PATH.read_text())