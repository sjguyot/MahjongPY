from __future__ import annotations

from dataclasses import dataclass, field
import re

SUITS = "mps"
HONORS = ("E", "S", "W", "N", "P", "F", "C")
ALL_TILES = tuple(f"{n}{s}" for s in SUITS for n in range(1, 10)) + HONORS
_TILE_RE = re.compile(r"^[1-9][mps]$")


def validate_tile(tile: str) -> str:
    if not isinstance(tile, str) or (tile not in HONORS and not _TILE_RE.fullmatch(tile)):
        raise ValueError(f"Invalid tile {tile!r}; use 1-9m/1-9p/1-9s or E,S,W,N,P,F,C")
    return tile


def parse_tiles(value: str | None) -> list[str]:
    if not value:
        return []
    tiles = [part.strip() for part in value.split(",") if part.strip()]
    return [validate_tile(tile) for tile in tiles]


def tile_number(tile: str) -> int | None:
    return int(tile[0]) if tile not in HONORS else None


def tile_suit(tile: str) -> str | None:
    return tile[-1] if tile not in HONORS else None


def is_terminal_or_honor(tile: str) -> bool:
    return tile in HONORS or tile_number(tile) in (1, 9)
