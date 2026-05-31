"""Execution state models.

The MVP memory store uses one deterministic implicit cell for ``□``. Each visit
to ``□`` stores the current value under :data:`DEFAULT_MEMORY_KEY`, replacing
any previous value. Later stories can add addressed memory without changing the
basic state shape.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, TypeAlias

from geobe.grid import Position

Direction: TypeAlias = Literal["up", "down", "left", "right"]
Value: TypeAlias = Any

DEFAULT_MEMORY_KEY = "□"
_UNSET: object = object()


@dataclass(frozen=True, slots=True)
class TraceEntry:
    """A structured snapshot of one observable execution step."""

    step: int
    position: Position | None
    direction: Direction | None
    symbol: str | None
    input_value: Value | None
    current_value: Value
    output_changes: tuple[Value, ...]
    memory_changes: dict[str, Value]
    input_buffer: tuple[Value, ...]
    output_buffer: tuple[Value, ...]
    memory: dict[str, Value]


@dataclass(slots=True)
class ExecutionState:
    """Mutable runtime state for a single interpreter run."""

    program: str
    input_buffer: list[Value] = field(default_factory=list)
    output_buffer: list[Value] = field(default_factory=list)
    memory: dict[str, Value] = field(default_factory=dict)
    current_position: Position | None = None
    current_direction: Direction | None = None
    current_value: Value = None
    traversal_values: tuple[Value, ...] | None = None
    traversal_index: int = -1
    traversal_loop_start: Position | None = None
    visited_steps: int = 0
    trace: list[TraceEntry] = field(default_factory=list)

    def read_input(self) -> Value:
        """Remove and return the next input value."""
        return self.input_buffer.pop(0)

    def append_output(self, value: Value = _UNSET) -> None:
        """Append a value to the output buffer in execution order."""
        if value is _UNSET:
            value = self.current_value
        self.output_buffer.append(value)

    def store_current_value(self, key: str = DEFAULT_MEMORY_KEY) -> None:
        """Store the current value in deterministic implicit memory."""
        self.memory[key] = self.current_value

    def record_step(
        self,
        symbol: str | None = None,
        *,
        input_value: Value | None = None,
        output_changes: tuple[Value, ...] = (),
        memory_changes: dict[str, Value] | None = None,
    ) -> TraceEntry:
        """Record a typed trace snapshot for the current state."""
        self.visited_steps += 1
        entry = TraceEntry(
            step=self.visited_steps,
            position=self.current_position,
            direction=self.current_direction,
            symbol=symbol,
            input_value=input_value,
            current_value=self.current_value,
            output_changes=output_changes,
            memory_changes=dict(memory_changes or {}),
            input_buffer=tuple(self.input_buffer),
            output_buffer=tuple(self.output_buffer),
            memory=dict(self.memory),
        )
        self.trace.append(entry)
        return entry
