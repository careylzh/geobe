"""Transformation registry for semantic symbols."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

Transform = Callable[[Any], Any]
TransformRegistry = dict[str, Transform]


def identity(value: Any) -> Any:
    """Return a value unchanged."""
    return value


def default_transform_registry() -> TransformRegistry:
    """Create the default symbol transform registry."""
    return {"△": identity}
