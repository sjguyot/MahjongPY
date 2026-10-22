from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from .tiles import ALL_TILES, parse_tiles, validate_tile


@dataclass
class OpponentState:
    discards: list[str] = field(default_factory=list)
    open_melds: list[list[str]] = field(default_factory=list)
    riichi: bool = False
    riichi_turn: int | None = None

    def __post_init__(self) -> None:
        self.discards = [validate_tile(t) for t in self.discards]
        self.open_melds = [[validate_tile(t) for t in meld] for meld in self.open_melds]
        if self.riichi_turn is not None and self.riichi_turn < 0:
            raise ValueError("riichi_turn must be non-negative")


def visible_counts(state: OpponentState, known_tiles: list[str] | None = None) -> Counter[str]:
    result: Counter[str] = Counter(state.discards)
    for meld in state.open_melds:
        result.update(meld)
    result.update(known_tiles or [])
    for tile, count in result.items():
        if count > 4:
            raise ValueError(f"More than four copies of {tile} are visible")
    return result


def remaining_counts(state: OpponentState, known_tiles: list[str] | None = None) -> dict[str, int]:
    counts = visible_counts(state, known_tiles)
    return {tile: 4 - counts[tile] for tile in ALL_TILES}


def parse_melds(value: str | None) -> list[list[str]]:
    if not value:
        return []
    return [parse_tiles(meld) for meld in value.split(";")]
