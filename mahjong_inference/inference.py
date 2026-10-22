from __future__ import annotations

from dataclasses import dataclass

from .state import OpponentState, remaining_counts, visible_counts
from .tiles import ALL_TILES, is_terminal_or_honor, tile_number, tile_suit


@dataclass(frozen=True)
class DangerEstimate:
    tile: str
    score: float
    reasons: tuple[str, ...]
    confidence: str


def _neighbor_count(tile: str, discards: list[str]) -> int:
    number, suit = tile_number(tile), tile_suit(tile)
    if number is None:
        return 0
    return sum(1 for other in discards if tile_suit(other) == suit and abs(tile_number(other) - number) == 1)


def estimate_danger(state: OpponentState, known_tiles: list[str] | None = None) -> list[DangerEstimate]:
    visible = visible_counts(state, known_tiles)
    remaining = remaining_counts(state, known_tiles)
    discard_counts = {tile: state.discards.count(tile) for tile in ALL_TILES}
    results: list[DangerEstimate] = []

    for tile in ALL_TILES:
        reasons: list[str] = []
        score = 1.0
        copies = remaining[tile]
        score *= 0.25 + copies / 4
        if copies == 0:
            reasons.append("no unseen copies remain")
        if discard_counts[tile]:
            score *= 0.55 ** discard_counts[tile]
            reasons.append(f"discarded {discard_counts[tile]} time(s)")
        if _neighbor_count(tile, state.discards):
            score *= 0.9
            reasons.append("near a discarded suited tile")
        if is_terminal_or_honor(tile):
            score *= 0.82
            reasons.append("terminal/honor baseline reduction")
        else:
            score *= 1.08
        if state.open_melds:
            score *= 1.08
            reasons.append("opponent has open meld(s)")
        if state.riichi:
            score *= 1.9
            reasons.append("riichi increases tenpai danger")
        if visible[tile] >= 2:
            reasons.append(f"{visible[tile]} visible copy/copies")
        results.append((tile, score, tuple(reasons)))

    total = sum(item[1] for item in results) or 1.0
    confidence = "high" if state.riichi else ("medium" if state.discards else "low")
    return [DangerEstimate(tile, round(score / total, 6), reasons, confidence)
            for tile, score, reasons in sorted(results, key=lambda x: (-x[1], x[0]))]
