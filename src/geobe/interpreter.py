"""Interpreter engine facade."""

from __future__ import annotations

from dataclasses import dataclass, field

from geobe.grid import Grid, Position
from geobe.parser import parse_program
from geobe.state import Direction, ExecutionState, Value
from geobe.transforms import (
    TransformContext,
    TransformRegistry,
    default_transform_registry,
    identity,
)

DIRECTIONS: tuple[Direction, ...] = ("right", "down", "left", "up")
ARROW_DIRECTIONS: dict[str, Direction] = {
    "→": "right",
    "←": "left",
    "↑": "up",
    "↓": "down",
}
SEMANTIC_SYMBOLS = frozenset({"○", "□", "△", "▽"})
TRAVERSABLE_SYMBOLS = frozenset(ARROW_DIRECTIONS) | SEMANTIC_SYMBOLS
DEFAULT_MAX_STEPS = 1000


@dataclass(frozen=True, slots=True)
class StepEffects:
    """State changes produced while executing one symbol."""

    input_value: Value | None = None
    output_changes: tuple[Value, ...] = ()
    memory_changes: dict[str, Value] = field(default_factory=dict)


class InterpreterStepLimitError(RuntimeError):
    """Raised when execution exceeds the configured maximum step count."""


class InterpreterInputError(RuntimeError):
    """Raised when a source node needs an input value that is unavailable."""


@dataclass(slots=True)
class Interpreter:
    """Coordinate parsing, state, transforms, and execution."""

    transforms: TransformRegistry = field(default_factory=default_transform_registry)
    max_steps: int = DEFAULT_MAX_STEPS

    def run(self, program: str, inputs: list[Value] | None = None) -> ExecutionState:
        """Run a program and return its state."""
        grid = parse_program(program)
        state = ExecutionState(program=program, input_buffer=list(inputs or []))
        for source in _source_positions(grid):
            self._run_flow(grid, source, state)
        return state

    def _run_flow(
        self,
        grid: Grid,
        source: Position,
        state: ExecutionState,
    ) -> None:
        position: Position | None = source
        direction: Direction | None = None

        while position is not None:
            symbol = grid.get(position)
            if symbol not in TRAVERSABLE_SYMBOLS:
                return

            if symbol in ARROW_DIRECTIONS:
                direction = ARROW_DIRECTIONS[symbol]

            state.current_position = position
            state.current_direction = direction
            effects = self._execute_symbol(state, symbol)
            self._record_step(state, symbol, effects)

            if direction is None:
                direction = _outgoing_direction(grid, position)
                if direction is None:
                    return
                state.current_direction = direction

            position = _next_position(grid, position, direction)

    def _record_step(
        self,
        state: ExecutionState,
        symbol: str,
        effects: StepEffects,
    ) -> None:
        if state.visited_steps >= self.max_steps:
            msg = f"Execution exceeded maximum step limit of {self.max_steps}."
            raise InterpreterStepLimitError(msg)
        state.record_step(
            symbol=symbol,
            input_value=effects.input_value,
            output_changes=effects.output_changes,
            memory_changes=effects.memory_changes,
        )

    def _execute_symbol(self, state: ExecutionState, symbol: str) -> StepEffects:
        output_start = len(state.output_buffer)
        memory_before = dict(state.memory)
        input_value: Value | None = None

        if symbol == "○":
            if not state.input_buffer:
                msg = _missing_input_message(state)
                raise InterpreterInputError(msg)
            input_value = state.read_input()
            state.current_value = input_value
        elif symbol == "□":
            state.store_current_value()
        elif symbol == "△":
            transform = self.transforms.get("△", identity)
            context = TransformContext(
                symbol=symbol,
                current_value=state.current_value,
                state=state,
            )
            state.current_value = transform(context)
        elif symbol == "▽":
            state.append_output()

        return StepEffects(
            input_value=input_value,
            output_changes=tuple(state.output_buffer[output_start:]),
            memory_changes=_memory_changes(memory_before, state.memory),
        )


def _memory_changes(
    before: dict[str, Value],
    after: dict[str, Value],
) -> dict[str, Value]:
    return {key: value for key, value in after.items() if before.get(key) != value}


def _missing_input_message(state: ExecutionState) -> str:
    position = state.current_position
    if position is None:
        return "Missing input for ○ source."
    return (
        "Missing input for ○ source "
        f"at row {position.row}, column {position.column}."
    )


def _source_positions(grid: Grid) -> list[Position]:
    return [
        Position(row, column)
        for row in range(grid.height)
        for column in range(grid.width)
        if grid.get(Position(row, column)) == "○"
    ]


def _outgoing_direction(grid: Grid, position: Position) -> Direction | None:
    for direction in DIRECTIONS:
        next_position = _next_position(grid, position, direction)
        if next_position is None:
            continue

        symbol = grid.get(next_position)
        if symbol in ARROW_DIRECTIONS and ARROW_DIRECTIONS[symbol] == direction:
            return direction
    return None


def _next_position(
    grid: Grid,
    position: Position,
    direction: Direction,
) -> Position | None:
    next_position = _move(position, direction)
    while grid.contains(next_position):
        symbol = grid.get(next_position)
        if symbol == " ":
            next_position = _move(next_position, direction)
            continue
        if symbol in TRAVERSABLE_SYMBOLS:
            return next_position
        return None
    return None


def _move(position: Position, direction: Direction) -> Position:
    if direction == "up":
        return Position(position.row - 1, position.column)
    if direction == "down":
        return Position(position.row + 1, position.column)
    if direction == "left":
        return Position(position.row, position.column - 1)
    return Position(position.row, position.column + 1)
