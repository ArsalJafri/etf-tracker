def redistribute_weights(universe: dict) -> dict:
    total = sum(data["avgWeight"] for data in universe.values())
    if total == 0:
        return universe
    return {
        ticker: {**data, "avgWeight": round(data["avgWeight"] / total * 100, 6)}
        for ticker, data in universe.items()
    }
