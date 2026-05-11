"""Tests for documented example programs."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Protocol, cast

import pytest

from geobe import Interpreter
from geobe.cli import main


EXAMPLES_DIR = Path("examples")
DOCUMENTED_PROGRAM = EXAMPLES_DIR / "input_store_transform_output.geo"
CUSTOM_TRANSFORM_EXAMPLE = EXAMPLES_DIR / "custom_transform.py"


class CustomTransformExample(Protocol):
    """Callable surface exposed by the custom transform example module."""

    def run_demo(self, input_value: str = "custom") -> list[object]:
        """Run the custom transform demo."""
        ...


def test_documented_geo_example_produces_expected_output() -> None:
    program = DOCUMENTED_PROGRAM.read_text(encoding="utf-8")

    state = Interpreter().run(program, inputs=["hello"])

    assert state.output_buffer == ["hello"]
    assert state.memory == {"□": "hello"}


def test_cli_runs_documented_geo_example(
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = main([str(DOCUMENTED_PROGRAM), "--input", "hello"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert json.loads(captured.out) == {"outputs": ["hello"]}
    assert captured.err == ""


def test_package_module_default_demo_runs_example_behavior(
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = main([])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert json.loads(captured.out) == {"outputs": ["demo-value"]}
    assert captured.err == ""


def test_custom_transform_example_uses_python_code() -> None:
    spec = importlib.util.spec_from_file_location(
        "geobe_custom_transform_example",
        CUSTOM_TRANSFORM_EXAMPLE,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    example = cast(CustomTransformExample, module)

    assert example.run_demo("custom") == ["[custom]"]
