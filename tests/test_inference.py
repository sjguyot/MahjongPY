import unittest

from mahjong_inference.inference import estimate_danger
from mahjong_inference.state import OpponentState, remaining_counts, visible_counts
from mahjong_inference.tiles import ALL_TILES, parse_tiles


class MahjongTests(unittest.TestCase):
    def test_tiles(self):
        self.assertEqual(parse_tiles("1m, E,9s"), ["1m", "E", "9s"])
        with self.assertRaises(ValueError):
            parse_tiles("10m")

    def test_visible_and_remaining(self):
        state = OpponentState(["5m", "5m"], [["E", "E", "E"]])
        self.assertEqual(visible_counts(state)["5m"], 2)
        self.assertEqual(remaining_counts(state)["5m"], 2)

    def test_repeated_discard_reduces_danger(self):
        clean = estimate_danger(OpponentState(["1m"]))
        repeated = estimate_danger(OpponentState(["1m", "1m", "1m"]))
        a = next(x for x in clean if x.tile == "1m")
        b = next(x for x in repeated if x.tile == "1m")
        self.assertLess(b.score, a.score)

    def test_riichi_changes_confidence_and_score(self):
        normal = estimate_danger(OpponentState(["1m", "2m"]))
        riichi = estimate_danger(OpponentState(["1m", "2m"], riichi=True))
        self.assertEqual(riichi[0].confidence, "high")
        self.assertNotEqual(normal[0].score, riichi[0].score)

    def test_normalized_and_deterministic(self):
        state = OpponentState(["1m", "2m", "E"])
        first = estimate_danger(state)
        second = estimate_danger(state)
        self.assertEqual(first, second)
        self.assertEqual(set(x.tile for x in first), set(ALL_TILES))
        self.assertAlmostEqual(sum(x.score for x in first), 1.0, places=5)


if __name__ == "__main__":
    unittest.main()
