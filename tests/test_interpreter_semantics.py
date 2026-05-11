"""Tests for core symbol semantics."""

from __future__ import annotations

import pytest

from geobe.interpreter import Interpreter, InterpreterInputError
from geobe.state import DEFAULT_MEMORY_KEY


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
    interpreter = Interpreter(transforms={"△": lambda value: f"{value}!"})

    state = interpreter.run("○→△→▽", inputs=["go"])

    assert state.current_value == "go!"
    assert state.output_buffer == ["go!"]


def test_down_triangle_appends_current_flow_value_to_output() -> None:
    state = Interpreter().run("○→▽", inputs=["result"])

    assert state.output_buffer == ["result"]
    assert state.trace[-1].output_buffer == ("result",)


def test_missing_input_at_circle_raises_clear_interpreter_error() -> None:
    with pytest.raises(
        InterpreterInputError,
        match="Missing input for ○ source at row 0, column 0",
    ):
        Interpreter().run("○→▽")
