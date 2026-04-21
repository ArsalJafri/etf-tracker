import unittest

from src.filter_system.weight_redistributor import redistribute_weights


class TestRedistributeWeights(unittest.TestCase):

    def test_weights_sum_to_100_after_redistribution(self):
        universe = {
            "AAPL": {"name": "Apple",     "avgWeight": 40.0, "etfCount": 1, "etfs": []},
            "MSFT": {"name": "Microsoft", "avgWeight": 30.0, "etfCount": 1, "etfs": []},
        }
        total = sum(d["avgWeight"] for d in redistribute_weights(universe).values())
        self.assertAlmostEqual(total, 100.0, places=4)

    def test_proportions_preserved_after_redistribution(self):
        universe = {
            "AAPL": {"name": "Apple",     "avgWeight": 40.0, "etfCount": 1, "etfs": []},
            "MSFT": {"name": "Microsoft", "avgWeight": 60.0, "etfCount": 1, "etfs": []},
        }
        result = redistribute_weights(universe)
        self.assertAlmostEqual(result["AAPL"]["avgWeight"], 40.0)
        self.assertAlmostEqual(result["MSFT"]["avgWeight"], 60.0)

    def test_returns_universe_unchanged_when_total_weight_is_zero(self):
        universe = {"AAPL": {"name": "Apple", "avgWeight": 0.0, "etfCount": 1, "etfs": []}}
        self.assertEqual(redistribute_weights(universe), universe)

    def test_does_not_mutate_original_universe(self):
        universe = {
            "AAPL": {"name": "Apple",     "avgWeight": 40.0, "etfCount": 1, "etfs": []},
            "MSFT": {"name": "Microsoft", "avgWeight": 30.0, "etfCount": 1, "etfs": []},
        }
        original_weight = universe["AAPL"]["avgWeight"]
        redistribute_weights(universe)
        self.assertEqual(universe["AAPL"]["avgWeight"], original_weight)


if __name__ == "__main__":
    unittest.main()