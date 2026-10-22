"""Mahjong opponent-hand inference MVP."""

from .inference import DangerEstimate, estimate_danger
from .state import OpponentState

__all__ = ["DangerEstimate", "OpponentState", "estimate_danger"]
