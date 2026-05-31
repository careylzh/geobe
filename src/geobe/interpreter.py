"""Interpreter engine facade."""

from __future__ import annotations

from collections.abc import Sequence
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
TRANSFORM_SYMBOLS = frozenset({"△", "▲"})
APPEND_SYMBOLS = frozenset({"▽", "◀"})
TRAVERSE_SYMBOL = "▶"
CONTINUE_SYMBOL = "▶▶"
SEMANTIC_SYMBOLS = (
    frozenset({"○", "□", TRAVERSE_SYMBOL})
    | TRANSFORM_SYMBOLS
    | APPEND_SYMBOLS
)
LITERAL_STRING_OPEN = "«"
LITERAL_STRING_CLOSE = "»"
TRAVERSABLE_SYMBOLS = (
    frozenset(ARROW_DIRECTIONS)
    | SEMANTIC_SYMBOLS
    | frozenset({LITERAL_STRING_OPEN})
)
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


class InterpreterLiteralError(RuntimeError):
    """Raised when a literal string block cannot be parsed."""


class InterpreterTraversalError(RuntimeError):
    """Raised when array traversal symbols cannot operate on the current value."""


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

            if symbol == LITERAL_STRING_OPEN:
                if direction is None:
                    direction = "right"
                state.current_position = position
                state.current_direction = direction
                literal_value, position = _read_string_literal(
                    grid,
                    position,
                    direction,
                )
                state.current_value = literal_value
                self._record_step(state, symbol, StepEffects())
                continue

            if symbol == TRAVERSE_SYMBOL and _is_continue_symbol(
                grid,
                position,
                direction,
            ):
                state.current_position = position
                state.current_direction = direction
                should_continue = _advance_traversal(state)
                self._record_step(state, CONTINUE_SYMBOL, StepEffects())

                if should_continue and state.traversal_loop_start is not None:
                    position = state.traversal_loop_start
                    continue

                position = _position_after_continue_symbol(grid, position, direction)
                continue

            state.current_position = position
            state.current_direction = direction
            effects = self._execute_symbol(state, symbol)
            self._record_step(state, symbol, effects)

            if direction is None:
                direction = _outgoing_direction(grid, position)
                if direction is None:
                    return
                state.current_direction = direction

            if symbol == TRAVERSE_SYMBOL:
                state.traversal_loop_start = _next_position(grid, position, direction)

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
        elif symbol in TRANSFORM_SYMBOLS:
            transform = self.transforms.get(symbol, self.transforms.get("△", identity))
            context = TransformContext(
                symbol=symbol,
                current_value=state.current_value,
                state=state,
            )
            state.current_value = transform(context)
        elif symbol in APPEND_SYMBOLS:
            state.append_output()
        elif symbol == TRAVERSE_SYMBOL:
            _start_traversal(state)

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
        if _is_source_symbol(grid, Position(row, column))
    ]


def _is_source_symbol(grid: Grid, position: Position) -> bool:
    symbol = grid.get(position)
    if symbol == "○":
        return True
    if symbol == LITERAL_STRING_OPEN:
        return not _has_incoming_arrow(grid, position)
    return False


def _has_incoming_arrow(grid: Grid, position: Position) -> bool:
    for direction in DIRECTIONS:
        cursor = _move(position, _opposite_direction(direction))
        while grid.contains(cursor):
            symbol = grid.get(cursor)
            if symbol == " ":
                cursor = _move(cursor, _opposite_direction(direction))
                continue
            if symbol in ARROW_DIRECTIONS and ARROW_DIRECTIONS[symbol] == direction:
                return True
            break
    return False


def _is_continue_symbol(
    grid: Grid,
    position: Position,
    direction: Direction | None,
) -> bool:
    if direction is None:
        return False
    next_position = _move(position, direction)
    return grid.get(next_position) == TRAVERSE_SYMBOL


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


def _position_after_continue_symbol(
    grid: Grid,
    position: Position,
    direction: Direction | None,
) -> Position | None:
    if direction is None:
        return None
    second_symbol_position = _move(position, direction)
    return _next_position(grid, second_symbol_position, direction)


def _start_traversal(state: ExecutionState) -> None:
    values = _coerce_traversal_values(state.current_value)
    state.traversal_values = values
    state.traversal_index = 0
    state.current_value = values[0]


def _advance_traversal(state: ExecutionState) -> bool:
    values = state.traversal_values
    if values is None:
        msg = "Cannot continue array traversal before visiting ▶."
        raise InterpreterTraversalError(msg)

    next_index = state.traversal_index + 1
    if next_index >= len(values):
        return False

    state.traversal_index = next_index
    state.current_value = values[next_index]
    return True


def _coerce_traversal_values(value: Value) -> tuple[Value, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        msg = "▶ requires the current value to be a non-empty array."
        raise InterpreterTraversalError(msg)
    values = tuple(value)
    if not values:
        msg = "▶ requires the current value to be a non-empty array."
        raise InterpreterTraversalError(msg)
    return values


def _read_string_literal(
    grid: Grid,
    position: Position,
    direction: Direction,
) -> tuple[str, Position | None]:
    cursor = _move(position, direction)
    literal: list[str] = []

    while grid.contains(cursor):
        symbol = grid.get(cursor)
        if symbol is None:
            break
        if symbol == LITERAL_STRING_CLOSE:
            return "".join(literal), _next_position(grid, cursor, direction)
        literal.append(symbol)
        cursor = _move(cursor, direction)

    msg = (
        "Missing closing delimiter for string literal "
        f"at row {position.row}, column {position.column}."
    )
    raise InterpreterLiteralError(msg)


def _move(position: Position, direction: Direction) -> Position:
    if direction == "up":
        return Position(position.row - 1, position.column)
    if direction == "down":
        return Position(position.row + 1, position.column)
    if direction == "left":
        return Position(position.row, position.column - 1)
    return Position(position.row, position.column + 1)


def _opposite_direction(direction: Direction) -> Direction:
    if direction == "up":
        return "down"
    if direction == "down":
        return "up"
    if direction == "left":
        return "right"
    return "left"
