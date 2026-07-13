"""Tests for the command-line runner."""

from __future__ import annotations

import json
from io import StringIO
from pathlib import Path

import pytest

from geobe.cli import main


def test_cli_runs_geo_file_path(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    program_path = tmp_path / "echo.geo"
    program_path.write_text("○→▽", encoding="utf-8")

    exit_code = main([str(program_path), "--input", "file-value"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert json.loads(captured.out) == {"outputs": ["file-value"]}
    assert captured.err == ""


def test_cli_runs_inline_program_string(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["--code", "○→▽", "--input", "inline-value"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert json.loads(captured.out) == {"outputs": ["inline-value"]}


def test_cli_accepts_input_from_stdin(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr("sys.stdin", StringIO("first\nsecond\n"))

    exit_code = main(["--code", "○→▽\n○→▽", "--stdin-input"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert json.loads(captured.out) == {"outputs": ["first", "second"]}


def test_cli_console_mode_starts_terminal_console(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    called_with_language = ""

    def fake_run_console(*, output_language: str = "english") -> int:
        nonlocal called_with_language
        called_with_language = output_language
        return 0

    monkeypatch.setattr("geobe.cli.run_console", fake_run_console)

    exit_code = main(["--console"])

    assert exit_code == 0
    assert called_with_language == "english"


def test_cli_console_mode_accepts_portuguese_output_language(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    called_with_language = ""

    def fake_run_console(*, output_language: str = "english") -> int:
        nonlocal called_with_language
        called_with_language = output_language
        return 0

    monkeypatch.setattr("geobe.cli.run_console", fake_run_console)

    exit_code = main(["--console", "--console-output-language", "portuguese"])

    assert exit_code == 0
    assert called_with_language == "portuguese"


def test_cli_trace_mode_prints_execution_trace(
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = main(["--code", "○→▽", "--input", "traced", "--trace"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 0
    assert payload["outputs"] == ["traced"]
    assert payload["trace"] == [
        {
            "current_value": "traced",
            "direction": None,
            "input_buffer": [],
            "input_value": "traced",
            "memory": {},
            "memory_changes": {},
            "output_buffer": [],
            "output_changes": [],
            "position": {"column": 0, "row": 0},
            "step": 1,
            "symbol": "○",
        },
        {
            "current_value": "traced",
            "direction": "right",
            "input_buffer": [],
            "input_value": None,
            "memory": {},
            "memory_changes": {},
            "output_buffer": [],
            "output_changes": [],
            "position": {"column": 1, "row": 0},
            "step": 2,
            "symbol": "→",
        },
        {
            "current_value": "traced",
            "direction": "right",
            "input_buffer": [],
            "input_value": None,
            "memory": {},
            "memory_changes": {},
            "output_buffer": ["traced"],
            "output_changes": ["traced"],
            "position": {"column": 2, "row": 0},
            "step": 3,
            "symbol": "▽",
        },
    ]


def test_cli_trace_text_mode_renders_readable_steps(
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = main(
        [
            "--code",
            "○→□→▽",
            "--input",
            "text-value",
            "--trace",
            "--trace-format",
            "text",
        ],
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.splitlines() == [
        'outputs: ["text-value"]',
        "trace:",
        (
            '1. row=0 column=0 symbol=○ direction=None current="text-value" '
            'input="text-value"'
        ),
        '2. row=0 column=1 symbol=→ direction=right current="text-value"',
        (
            '3. row=0 column=2 symbol=□ direction=right current="text-value" '
            'memory+={"□": "text-value"}'
        ),
        '4. row=0 column=3 symbol=→ direction=right current="text-value"',
        (
            '5. row=0 column=4 symbol=▽ direction=right current="text-value" '
            'outputs+=["text-value"]'
        ),
    ]
    assert captured.err == ""


def test_cli_invalid_runtime_input_returns_nonzero_and_message(
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = main(["--code", "○→▽"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert "geobe: Missing input for ○ source at row 0, column 0" in captured.err
