"""Geobe, a geometric esoteric language interpreter."""

from geobe.grid import Grid, Position
from geobe.interpreter import (
    Interpreter,
    InterpreterInputError,
    InterpreterLiteralError,
    InterpreterStepLimitError,
    InterpreterTraversalError,
)
from geobe.parser import ProgramParseError, parse_program
from geobe.state import ExecutionState, TraceEntry
from geobe.transforms import (
    Transform,
    TransformContext,
    TransformRegistry,
    default_transform_registry,
    identity,
)

__all__ = [
    "ExecutionState",
    "Grid",
    "Interpreter",
    "InterpreterInputError",
    "InterpreterLiteralError",
    "InterpreterStepLimitError",
    "InterpreterTraversalError",
    "Position",
    "ProgramParseError",
    "TraceEntry",
    "Transform",
    "TransformContext",
    "TransformRegistry",
    "default_transform_registry",
    "identity",
    "parse_program",
]

__version__ = "0.1.0"
