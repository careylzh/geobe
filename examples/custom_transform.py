"""Run the documented Geobe example with a custom Python transform."""

from __future__ import annotations

import json
from pathlib import Path

from geobe import Interpreter, TransformContext


EXAMPLE_PATH = Path(__file__).with_name("input_store_transform_output.geo")


def bracket_transform(context: TransformContext) -> str:
    """Wrap the current value to make the transform step visible."""
    return f"[{context.current_value}]"


def run_demo(input_value: str = "custom") -> list[object]:
    """Run the example program with ``△`` registered to Python code."""
    program = EXAMPLE_PATH.read_text(encoding="utf-8")
    interpreter = Interpreter(transforms={"△": bracket_transform})
    return interpreter.run(program, inputs=[input_value]).output_buffer


def main() -> int:
    """Print the custom transform demo output as stable JSON."""
    print(json.dumps({"outputs": run_demo()}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
