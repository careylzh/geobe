"""Command-line interface for Geobe."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from geobe.console import run_console
from geobe.interpreter import Interpreter
from geobe.parser import ProgramParseError
from geobe.state import ExecutionState, TraceEntry, Value

EXIT_RUNTIME_ERROR = 1
EXIT_USAGE_ERROR = 2
DEMO_PROGRAM = "○→□→△→▽"
DEMO_INPUTS: tuple[Value, ...] = ("demo-value",)


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="geobe",
        description=(
            "Run Geobe's geometric esolang programs or open the triangle "
            "alphabet console."
        ),
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="Path to a .geo file to execute.",
    )
    parser.add_argument(
        "-c",
        "--code",
        dest="inline_program",
        help="Inline program source to execute instead of a file.",
    )
    parser.add_argument(
        "-i",
        "--input",
        dest="inputs",
        action="append",
        default=[],
        help="Input value supplied to the program. Repeat to pass multiple strings.",
    )
    parser.add_argument(
        "--stdin-input",
        action="store_true",
        help="Read additional input values from stdin, one value per line.",
    )
    parser.add_argument(
        "--trace",
        action="store_true",
        help="Include execution trace entries in the output.",
    )
    parser.add_argument(
        "--trace-format",
        choices=("json", "text"),
        default="json",
        help="Render trace as structured JSON or readable text.",
    )
    parser.add_argument(
        "--console",
        action="store_true",
        help=(
            "Start an interactive spelling console that echoes lowercase "
            "letters as Geobe symbols and decodes them on Enter."
        ),
    )
    parser.add_argument(
        "--console-output-language",
        choices=("english", "portuguese", "portugese"),
        default="english",
        help=(
            "Language printed after Enter in --console mode. Use portuguese "
            "to translate decoded English text."
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the Geobe CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.console:
        if (
            args.path
            or args.inline_program is not None
            or args.inputs
            or args.stdin_input
            or args.trace
        ):
            parser.error("provide either --console or program execution options")
        return run_console(output_language=args.console_output_language)

    if args.console_output_language != "english":
        parser.error("--console-output-language requires --console")

    if args.path and args.inline_program is not None:
        parser.error("provide either a .geo file path or --code, not both")

    program = args.inline_program
    inputs: list[Value] = list(args.inputs)
    if not args.path and args.inline_program is None:
        program = DEMO_PROGRAM
        if not inputs and not args.stdin_input:
            inputs.extend(DEMO_INPUTS)

    if program is None:
        try:
            program = Path(args.path).read_text(encoding="utf-8")
        except OSError as error:
            print(f"geobe: failed to read program: {error}", file=sys.stderr)
            return EXIT_USAGE_ERROR

    if args.stdin_input:
        inputs.extend(line.rstrip("\n") for line in sys.stdin)

    try:
        state = Interpreter().run(program, inputs=inputs)
    except (ProgramParseError, RuntimeError) as error:
        print(f"geobe: {error}", file=sys.stderr)
        return EXIT_RUNTIME_ERROR

    print(
        _format_result(
            state,
            include_trace=args.trace,
            trace_format=args.trace_format,
        ),
    )
    return 0


def _format_result(
    state: ExecutionState,
    *,
    include_trace: bool,
    trace_format: str = "json",
) -> str:
    if include_trace and trace_format == "text":
        return _format_text_result(state)

    payload: dict[str, Any] = {"outputs": state.output_buffer}
    if include_trace:
        payload["trace"] = [_trace_entry_to_json(entry) for entry in state.trace]
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _trace_entry_to_json(entry: TraceEntry) -> dict[str, Any]:
    position = None
    if entry.position is not None:
        position = {
            "row": entry.position.row,
            "column": entry.position.column,
        }

    return {
        "step": entry.step,
        "position": position,
        "direction": entry.direction,
        "symbol": entry.symbol,
        "input_value": entry.input_value,
        "current_value": entry.current_value,
        "output_changes": list(entry.output_changes),
        "memory_changes": entry.memory_changes,
        "input_buffer": list(entry.input_buffer),
        "output_buffer": list(entry.output_buffer),
        "memory": entry.memory,
    }


def _format_text_result(state: ExecutionState) -> str:
    lines = [
        f"outputs: {_format_value(state.output_buffer)}",
        "trace:",
    ]
    lines.extend(_format_trace_line(entry) for entry in state.trace)
    return "\n".join(lines)


def _format_trace_line(entry: TraceEntry) -> str:
    position = "position=None"
    if entry.position is not None:
        position = f"row={entry.position.row} column={entry.position.column}"

    parts = [
        f"{entry.step}.",
        position,
        f"symbol={entry.symbol}",
        f"direction={entry.direction}",
        f"current={_format_value(entry.current_value)}",
    ]
    if entry.input_value is not None:
        parts.append(f"input={_format_value(entry.input_value)}")
    if entry.output_changes:
        parts.append(f"outputs+={_format_value(list(entry.output_changes))}")
    if entry.memory_changes:
        parts.append(f"memory+={_format_value(entry.memory_changes)}")
    return " ".join(parts)


def _format_value(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)
