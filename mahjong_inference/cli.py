from __future__ import annotations

import argparse

from .inference import estimate_danger
from .state import OpponentState, parse_melds
from .tiles import parse_tiles


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Estimate dangerous Mahjong tiles heuristically.")
    parser.add_argument("--discards", required=True, help="Comma-separated tiles, e.g. 1m,2m,E")
    parser.add_argument("--melds", help="Semicolon-separated melds, e.g. 2m,3m,4m;E,E,E")
    parser.add_argument("--known", help="Comma-separated visible tiles in your hand or elsewhere")
    parser.add_argument("--riichi", action="store_true")
    parser.add_argument("--limit", type=int, default=10)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        state = OpponentState(parse_tiles(args.discards), parse_melds(args.melds), args.riichi)
        estimates = estimate_danger(state, parse_tiles(args.known))[:args.limit]
    except ValueError as exc:
        raise SystemExit(f"Input error: {exc}")
    print(f"Opponent riichi: {'yes' if state.riichi else 'no'}")
    print("Approximate dangerous tiles (heuristic, not certainty):")
    for item in estimates:
        explanation = "; ".join(item.reasons) or "remaining-tile baseline"
        print(f"  {item.tile:>2}  {item.score:.2%}  [{item.confidence}]  {explanation}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
