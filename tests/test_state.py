"""Tests for execution state models."""

from __future__ import annotations

from geobe.cli import build_parser
from geobe.grid import Position
from geobe.interpreter import Interpreter
from geobe.state import DEFAULT_MEMORY_KEY, ExecutionState


def test_interpreter_returns_explicit_execution_state_after_traversal() -> None:
    state = Interpreter().run("○→▽", inputs=[1, "two"])

    assert state.program == "○→▽"
    assert state.current_position == Position(0, 2)
    assert state.current_direction == "right"
    assert state.current_value == 1
    assert state.input_buffer == ["two"]
    assert state.output_buffer == [1]
    assert state.memory == {}
    assert state.visited_steps == 3
    assert [entry.symbol for entry in state.trace] == ["○", "→", "▽"]


def test_output_values_are_collected_in_order() -> None:
    state = ExecutionState(program="▽")

    state.append_output("first")
    state.current_value = "second"
    state.append_output()

    assert state.output_buffer == ["first", "second"]


def test_square_memory_store_uses_deterministic_implicit_cell() -> None:
    state = ExecutionState(program="□□")

    state.current_value = "initial"
    state.store_current_value()
    state.current_value = "replacement"
    state.store_current_value()

    assert state.memory == {DEFAULT_MEMORY_KEY: "replacement"}


def test_trace_records_typed_state_snapshots() -> None:
    state = ExecutionState(
        program="○",
        input_buffer=["next"],
        output_buffer=["done"],
        memory={DEFAULT_MEMORY_KEY: "stored"},
        current_position=Position(2, 3),
        current_direction="right",
        current_value="current",
    )

    entry = state.record_step(symbol="○")
    state.output_buffer.append("later")

    assert state.visited_steps == 1
    assert state.trace == [entry]
    assert entry.step == 1
    assert entry.position == Position(2, 3)
    assert entry.direction == "right"
    assert entry.symbol == "○"
    assert entry.current_value == "current"
    assert entry.input_buffer == ("next",)
    assert entry.output_buffer == ("done",)
    assert entry.memory == {DEFAULT_MEMORY_KEY: "stored"}


def test_cli_accepts_repeated_string_input_values() -> None:
    args = build_parser().parse_args(["program.geo", "--input", "a", "-i", "b"])

    assert args.inputs == ["a", "b"]
