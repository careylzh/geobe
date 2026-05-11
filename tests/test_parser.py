"""Tests for program grid parsing."""

from __future__ import annotations

import pytest

from geobe.grid import Position
from geobe.parser import ProgramParseError, parse_program


def test_parse_program_normalizes_uneven_rows() -> None:
    grid = parse_program("○→\n▽")

    assert grid.width == 2
    assert grid.height == 2
    assert grid.rows() == ["○→", "▽ "]


def test_parse_program_preserves_unicode_symbols() -> None:
    grid = parse_program("○→□\n ↑△▽")

    assert grid.get(Position(0, 0)) == "○"
    assert grid.get(Position(0, 1)) == "→"
    assert grid.get(Position(0, 2)) == "□"
    assert grid.get(Position(1, 1)) == "↑"
    assert grid.get(Position(1, 2)) == "△"
    assert grid.get(Position(1, 3)) == "▽"


def test_parse_program_preserves_meaningful_whitespace() -> None:
    grid = parse_program(" ○ \n  ▽")

    assert grid.width == 3
    assert grid.rows() == [" ○ ", "  ▽"]
    assert grid.get(Position(0, 0)) == " "
    assert grid.get(Position(1, 1)) == " "


def test_grid_lookup_is_safe_for_out_of_bounds_positions() -> None:
    grid = parse_program("○")

    assert grid.get(Position(0, 0)) == "○"
    assert grid.get(Position(-1, 0)) is None
    assert grid.get(Position(0, 1)) is None
    assert grid.get(Position(1, 0)) is None


def test_parse_program_rejects_empty_source() -> None:
    with pytest.raises(ProgramParseError, match="must not be empty"):
        parse_program("")


def test_parse_program_rejects_blank_line_only_source() -> None:
    with pytest.raises(ProgramParseError, match="at least one character"):
        parse_program("\n")
