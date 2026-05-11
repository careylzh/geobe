"""Tests for core symbol semantics."""

from __future__ import annotations

import pytest

from geobe.interpreter import Interpreter, InterpreterInputError
from geobe.state import DEFAULT_MEMORY_KEY
from geobe.transforms import TransformContext, default_transform_registry


def test_circle_reads_next_input_value_into_current_flow() -> None:
    state = Interpreter().run("○", inputs=["first", "second"])

    assert state.current_value == "first"
    assert state.input_buffer == ["second"]
    assert state.trace[0].current_value == "first"
    assert state.trace[0].input_buffer == ("second",)


def test_square_stores_current_flow_value_in_memory() -> None:
    state = Interpreter().run("○→□", inputs=["stored"])

    assert state.current_value == "stored"
    assert state.memory == {DEFAULT_MEMORY_KEY: "stored"}
    assert state.trace[-1].memory == {DEFAULT_MEMORY_KEY: "stored"}


def test_default_triangle_transform_is_identity() -> None:
    state = Interpreter().run("○→△→▽", inputs=[42])

    assert state.current_value == 42
    assert state.output_buffer == [42]


def test_triangle_uses_configured_transform_behavior() -> None:
    def shout(context: TransformContext) -> str:
        return f"{context.current_value}!"

    interpreter = Interpreter(transforms={"△": shout})

    state = interpreter.run("○→△→▽", inputs=["go"])

    assert state.current_value == "go!"
    assert state.output_buffer == ["go!"]


def test_triangle_transform_can_be_registered_programmatically() -> None:
    registry = default_transform_registry()

    def increment(context: TransformContext) -> int:
        return int(context.current_value) + 1

    registry["△"] = increment

    state = Interpreter(transforms=registry).run("○→△→▽", inputs=[41])

    assert state.current_value == 42
    assert state.output_buffer == [42]


def test_triangle_transform_receives_execution_context() -> None:
    observed_steps: list[int] = []
    observed_memory: list[dict[str, object]] = []

    def annotate(context: TransformContext) -> str:
        observed_steps.append(context.state.visited_steps)
        observed_memory.append(dict(context.state.memory))
        return f"{context.symbol}:{context.current_value}"

    state = Interpreter(transforms={"△": annotate}).run(
        "○→□→△→▽",
        inputs=["seen"],
    )

    assert state.output_buffer == ["△:seen"]
    assert observed_steps == [4]
    assert observed_memory == [{DEFAULT_MEMORY_KEY: "seen"}]


def test_down_triangle_appends_current_flow_value_to_output() -> None:
    state = Interpreter().run("○→▽", inputs=["result"])

    assert state.output_buffer == ["result"]
    assert state.trace[-1].output_buffer == ("result",)
    assert state.trace[-1].output_changes == ("result",)


def test_trace_records_effects_for_known_program() -> None:
    state = Interpreter().run("○→□→▽", inputs=["known"])

    assert [
        (
            entry.step,
            entry.position.row if entry.position is not None else None,
            entry.position.column if entry.position is not None else None,
            entry.symbol,
            entry.direction,
            entry.input_value,
            entry.current_value,
            entry.output_changes,
            entry.memory_changes,
        )
        for entry in state.trace
    ] == [
        (1, 0, 0, "○", None, "known", "known", (), {}),
        (2, 0, 1, "→", "right", None, "known", (), {}),
        (3, 0, 2, "□", "right", None, "known", (), {DEFAULT_MEMORY_KEY: "known"}),
        (4, 0, 3, "→", "right", None, "known", (), {}),
        (5, 0, 4, "▽", "right", None, "known", ("known",), {}),
    ]


def test_missing_input_at_circle_raises_clear_interpreter_error() -> None:
    with pytest.raises(
        InterpreterInputError,
        match="Missing input for ○ source at row 0, column 0",
    ):
        Interpreter().run("○→▽")
