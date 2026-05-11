"""Execution state models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from geobe.grid import Position


@dataclass(slots=True)
class ExecutionState:
    """Mutable runtime state for a single interpreter run."""

    program: str
    input_buffer: list[Any] = field(default_factory=list)
    output_buffer: list[Any] = field(default_factory=list)
    memory: dict[str, Any] = field(default_factory=dict)
    current_position: Position | None = None
    current_direction: str | None = None
    current_value: Any = None
    visited_steps: int = 0
    trace: list[str] = field(default_factory=list)
