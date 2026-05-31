"""Tests for program grid parsing."""

from __future__ import annotations

import pytest

from geobe.grid import Position
from geobe.parser import (
    ProgramParseError,
    decode_spell_text,
    encode_spell_text,
    parse_program,
)

LONG_ENGLISH_MESSAGE = (
    "Hello world! Welcome to geobe, a fun,new programming language to express "
    "yourself, geometrically. Use shapes to write encoded messages to your "
    "friends, and receive an equally fun message from your friends to be "
    "decoded (by you, human, of course). Have fun! Sincerely, geobe founder"
)


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


def test_decode_spell_text_maps_triangle_alphabet_to_lowercase() -> None:
    assert decode_spell_text("▹▶▿▿◂ ◮◂ ◣▿▵!") == "hello world!"


def test_encode_spell_text_maps_english_to_triangle_alphabet() -> None:
    assert encode_spell_text("Hello, geobe!") == "▹▶▿▿◂, ▸▶◂△▶!"


def test_spell_text_round_trips_long_english_message() -> None:
    encoded = encode_spell_text(LONG_ENGLISH_MESSAGE)

    assert encoded.startswith("▹▶▿▿◂ ◮◂◣▿▵!")
    assert decode_spell_text(encoded) == LONG_ENGLISH_MESSAGE.lower()


def test_parse_program_expands_spell_directive_to_literal_output() -> None:
    grid = parse_program("spell ▹▶▿▿◂ ◮◂ ◣▿▵!")

    assert grid.rows() == ["«hello world!»→◀"]


def test_parse_program_rejects_empty_source() -> None:
    with pytest.raises(ProgramParseError, match="must not be empty"):
        parse_program("")


def test_parse_program_rejects_blank_line_only_source() -> None:
    with pytest.raises(ProgramParseError, match="at least one character"):
        parse_program("\n")
