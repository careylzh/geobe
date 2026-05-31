"""Transformation registry for semantic symbols."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from geobe.state import ExecutionState, Value


@dataclass(frozen=True, slots=True)
class TransformContext:
    """Runtime context passed to a semantic transform."""

    symbol: str
    current_value: Value
    state: ExecutionState


Transform = Callable[[TransformContext], Value]
TransformRegistry = dict[str, Transform]


def identity(context: TransformContext) -> Value:
    """Return a value unchanged."""
    return context.current_value


def default_transform_registry() -> TransformRegistry:
    """Create the default symbol transform registry."""
    return {"△": identity, "▲": identity}
