"""Grid model primitives for spatial programs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Position:
    """A zero-based coordinate in a program grid."""

    row: int
    column: int


@dataclass(frozen=True, slots=True)
class Grid:
    """A rectangular program grid."""

    cells: tuple[tuple[str, ...], ...]

    @property
    def height(self) -> int:
        """Return the number of grid rows."""
        return len(self.cells)

    @property
    def width(self) -> int:
        """Return the number of grid columns."""
        if not self.cells:
            return 0
        return len(self.cells[0])

    def get(self, position: Position) -> str | None:
        """Return the cell at a position, or None when out of bounds."""
        if not self.contains(position):
            return None
        return self.cells[position.row][position.column]

    def contains(self, position: Position) -> bool:
        """Return whether a position is inside the grid."""
        return (
            0 <= position.row < self.height
            and 0 <= position.column < self.width
        )

    def rows(self) -> list[str]:
        """Return grid rows as normalized strings."""
        return ["".join(row) for row in self.cells]
