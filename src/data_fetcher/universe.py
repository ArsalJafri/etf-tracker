import logging

log = logging.getLogger(__name__)


def build(holdings: dict[str, list[dict]]) -> dict[str, dict]:
    universe: dict[str, dict] = {}

    for etf_ticker, stocks in holdings.items():
        for stock in stocks:
            asset = stock["asset"]

            if asset not in universe:
                universe[asset] = {
                    "name":     stock["name"],
                    "etfCount": 0,
                    "etfs":     [],
                    "weights":  [],
                }

            universe[asset]["weights"].append(stock["weightPercentage"])
            universe[asset]["etfCount"] += 1
            universe[asset]["etfs"].append(etf_ticker)

    for data in universe.values():
        weights = data.pop("weights")
        data["avgWeight"] = round(sum(weights) / len(weights), 6)

    log.info("Universe: %d unique stocks across %d ETFs", len(universe), len(holdings))
    return universe
