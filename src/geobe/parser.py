"""Parser entry points for geometric programs."""

from __future__ import annotations

from geobe.grid import Grid


class ProgramParseError(ValueError):
    """Raised when program source cannot be parsed."""


def parse_program(source: str) -> Grid:
    """Parse source text into a normalized rectangular grid."""
    lines = source.splitlines()
    if not lines:
        raise ProgramParseError("Program source must not be empty.")

    width = max(len(line) for line in lines)
    if width == 0:
        raise ProgramParseError("Program source must contain at least one character.")

    cells = tuple(tuple(line.ljust(width)) for line in lines)
    return Grid(cells=cells)
