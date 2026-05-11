"""Grid model primitives for spatial programs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Position:
    """A zero-based coordinate in a program grid."""

    row: int
    column: int
