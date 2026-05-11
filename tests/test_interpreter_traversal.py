"""Tests for directional flow traversal."""

from __future__ import annotations

import pytest

from geobe.grid import Position
from geobe.interpreter import Interpreter, InterpreterStepLimitError


def test_traversal_runs_left_to_right_from_source() -> None:
    state = Interpreter().run("○→  ▽", inputs=["value"])

    assert [entry.symbol for entry in state.trace] == ["○", "→", "▽"]
    assert [entry.position for entry in state.trace] == [
        Position(0, 0),
        Position(0, 1),
        Position(0, 4),
    ]
    assert state.current_direction == "right"


def test_traversal_runs_right_to_left_from_source() -> None:
    state = Interpreter().run("▽  ←○", inputs=["value"])

    assert [entry.symbol for entry in state.trace] == ["○", "←", "▽"]
    assert [entry.position for entry in state.trace] == [
        Position(0, 4),
        Position(0, 3),
        Position(0, 0),
    ]
    assert state.current_direction == "left"


def test_traversal_runs_vertically_from_source() -> None:
    program = "○\n↓\n \n▽"

    state = Interpreter().run(program, inputs=["value"])

    assert [entry.symbol for entry in state.trace] == ["○", "↓", "▽"]
    assert [entry.position for entry in state.trace] == [
        Position(0, 0),
        Position(1, 0),
        Position(3, 0),
    ]
    assert state.current_direction == "down"


def test_traversal_terminates_when_source_has_no_valid_direction() -> None:
    state = Interpreter().run("○  ▽", inputs=["value"])

    assert [entry.symbol for entry in state.trace] == ["○"]
    assert state.current_position == Position(0, 0)
    assert state.current_direction is None


def test_traversal_terminates_cleanly_at_boundary() -> None:
    state = Interpreter().run("○→", inputs=["value"])

    assert [entry.symbol for entry in state.trace] == ["○", "→"]
    assert state.current_position == Position(0, 1)
    assert state.current_direction == "right"


def test_multiple_source_flows_run_in_row_major_order() -> None:
    state = Interpreter().run("○→▽\n○→□", inputs=["first", "second"])

    assert [entry.symbol for entry in state.trace] == [
        "○",
        "→",
        "▽",
        "○",
        "→",
        "□",
    ]
    assert [entry.position for entry in state.trace] == [
        Position(0, 0),
        Position(0, 1),
        Position(0, 2),
        Position(1, 0),
        Position(1, 1),
        Position(1, 2),
    ]


def test_traversal_enforces_maximum_step_limit() -> None:
    program = "○→↓\n ↑←"

    with pytest.raises(InterpreterStepLimitError, match="maximum step limit of 5"):
        Interpreter(max_steps=5).run(program, inputs=["value"])
