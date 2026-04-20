import logging
from dotenv import load_dotenv

from fetcher import fetch_all
from snapshot import save
from universe import build

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def run() -> dict:
    log.info("=== pipeline start ===")

    holdings = fetch_all()

    if not any(holdings.values()):
        log.error("All ETF fetches failed")
        return {}

    save(holdings)
    universe = build(holdings)

    log.info("=== pipeline complete — %d stocks in universe ===", len(universe))
    return universe


if __name__ == "__main__":  # pragma: no cover
    universe = run()

    top = sorted(universe.items(), key=lambda x: x[1]["avgWeight"], reverse=True)[:20]
    print(f"\n{'Ticker':<8} {'ETFs':<8} {'Avg weight %':<14} Name")
    print("-" * 60)
    for ticker, data in top:
        print(f"{ticker:<8} {data['etfCount']:<8} {data['avgWeight']:<14.4f} {data['name']}")
