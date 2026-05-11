"""Interpreter engine facade."""

from __future__ import annotations

from dataclasses import dataclass, field

from geobe.state import ExecutionState, Value
from geobe.transforms import TransformRegistry, default_transform_registry


@dataclass(slots=True)
class Interpreter:
    """Coordinate parsing, state, transforms, and execution."""

    transforms: TransformRegistry = field(default_factory=default_transform_registry)

    def run(self, program: str, inputs: list[Value] | None = None) -> ExecutionState:
        """Run a program and return its state.

        Full traversal semantics are implemented by later user stories.
        """
        return ExecutionState(program=program, input_buffer=list(inputs or []))
