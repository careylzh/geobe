# Ralph Progress Log

This file tracks progress across iterations. Agents update this file
after each iteration and it's included in prompts for context.

## Codebase Patterns (Study These First)

*Add reusable patterns discovered during development here.*
- Use a `src/` package layout with `tool.pytest.ini_options.pythonpath = ["src"]` so tests can import the package directly before it is installed.
- Model parser output as an immutable `Grid` dataclass with width, height, normalized rows, and safe `Position` lookups so later interpreter stories can share one grid API.
- Keep runtime state explicit in typed dataclasses, with small state methods for input, output, memory, and trace mutation so later interpreter stories can add traversal semantics without spreading buffer bookkeeping across modules.
- Keep traversal deterministic by discovering `○` source positions in row-major order, running one flow at a time, and recording every traversed semantic or arrow symbol through `ExecutionState.record_step`.
- Apply semantic symbol effects before recording each trace snapshot so trace entries reflect the state after the visited symbol executes.
- Use small context dataclasses for library extension hooks so callbacks can inspect current values and execution state without widening positional callable signatures later.

---

## 2026-05-11 - US-001
- Implemented a standard Python package scaffold for `geobe` with CLI, parser, grid/model, state, interpreter, and transform modules.
- Added `pyproject.toml` metadata, Hatchling build configuration, `geobe` console script entry point, and pytest, mypy, and ruff configuration.
- Added dedicated smoke tests under `tests/` proving package imports and CLI entry point configuration without manual `sys.path` edits in test files.
- Files changed: `pyproject.toml`, `src/geobe/__init__.py`, `src/geobe/__main__.py`, `src/geobe/cli.py`, `src/geobe/grid.py`, `src/geobe/interpreter.py`, `src/geobe/parser.py`, `src/geobe/py.typed`, `src/geobe/state.py`, `src/geobe/transforms.py`, `tests/test_package_structure.py`, `.ralph-tui/progress.md`.
- **Learnings:**
  - Patterns discovered: the repo started as a fresh scaffold, so a conservative `src/` layout keeps library and CLI concerns separated for later stories.
  - Gotchas encountered: this environment has `python3` but no `python` executable on PATH, and `mypy`/`ruff` are not installed in the active Python 3.14 interpreter.
---

## 2026-05-11 - US-002
- Implemented multiline program parsing into a normalized rectangular `Grid`, preserving spaces and Unicode symbols while padding shorter rows with spaces.
- Added grid width, height, row rendering, bounds checks, and safe `Position` lookup returning `None` outside the grid.
- Added clear `ProgramParseError` validation for empty source and newline-only source.
- Added parser unit tests for uneven rows, Unicode symbols, whitespace preservation, safe lookup, and invalid empty programs.
- Files changed: `src/geobe/grid.py`, `src/geobe/parser.py`, `src/geobe/__init__.py`, `tests/test_parser.py`, `.ralph-tui/progress.md`.
- **Learnings:**
  - Patterns discovered: keeping grid cells immutable as tuples gives later traversal code a stable read-only model while preserving simple string row assertions in tests.
  - Gotchas encountered: `python -m pytest`, `python -m mypy .`, and `python -m ruff check .` cannot run because `python` is not on PATH; `python3 -m pytest` passes, but `mypy` and `ruff` are not installed for `python3`.
---

## 2026-05-11 - US-003
- Implemented explicit execution state fields for current position, current direction, current value, memory, input buffer, output buffer, visited step count, and structured execution trace entries.
- Added typed runtime aliases, a deterministic `□` memory policy using a single implicit key, and small state helpers for reading input, appending output, storing memory, and recording trace snapshots.
- Added repeated CLI `--input`/`-i` parsing so command-line input values can be supplied as strings.
- Added state tests for interpreter initialization, ordered output collection, deterministic memory overwrite behavior, structured trace snapshots, and CLI input parsing.
- Files changed: `src/geobe/state.py`, `src/geobe/interpreter.py`, `src/geobe/cli.py`, `src/geobe/__init__.py`, `tests/test_state.py`, `.ralph-tui/progress.md`.
- **Learnings:**
  - Patterns discovered: use typed state dataclasses as the boundary between traversal and symbol semantics; this keeps future interpreter changes observable without coupling them to CLI or parser code.
  - Gotchas encountered: this environment still has no `python` executable on PATH, and `mypy`/`ruff` are not installed for `python3`; `python3 -m pytest`, `python3 -m compileall -q src tests`, and `git diff --check` pass.
---

## 2026-05-11 - US-004
- Implemented directional traversal in `Interpreter.run`, including row-major `○` source discovery, single-threaded flow execution, arrow direction changes, whitespace skipping, boundary/dead-end termination, and a configurable maximum step limit.
- Added `InterpreterStepLimitError` and exported it from the package API.
- Added traversal tests covering left-to-right, right-to-left, vertical movement, source dead ends, boundary termination, deterministic multi-source ordering, and step-limit loops.
- Updated existing state and package smoke tests for the now-active interpreter traversal.
- Files changed: `src/geobe/interpreter.py`, `src/geobe/__init__.py`, `tests/test_interpreter_traversal.py`, `tests/test_state.py`, `tests/test_package_structure.py`, `.ralph-tui/progress.md`.
- **Learnings:**
  - Patterns discovered: traversal can stay independent from symbol semantics by recording visits now and leaving value/memory/output effects for the semantic execution story.
  - Gotchas encountered: an initial source has no active direction, so the engine only starts a flow when the first reachable non-space cell in a cardinal direction is an arrow pointing away from the source; direct semantic neighbors without an arrow terminate cleanly for the MVP.
  - Quality gates: `python -m pytest`, `python -m mypy .`, and `python -m ruff check .` could not run because `python` is not on PATH; `python3 -m pytest`, `python3 -m compileall -q src tests`, and `git diff --check` pass, while `mypy` and `ruff` are not installed for `python3`.
---

## 2026-05-11 - US-005
- Implemented core symbol semantics: `○` consumes the next input into the current flow, `□` stores the current value in deterministic implicit memory, `△` applies the configured transform with identity fallback, and `▽` appends the current value to output.
- Added `InterpreterInputError` with source coordinates for missing input at `○`.
- Added focused semantics tests for input consumption, memory storage, identity and configured transforms, output append behavior, and missing-input errors; updated traversal/state smoke tests to supply source inputs.
- Files changed: `src/geobe/interpreter.py`, `src/geobe/__init__.py`, `tests/test_interpreter_semantics.py`, `tests/test_interpreter_traversal.py`, `tests/test_state.py`, `tests/test_package_structure.py`, `.ralph-tui/progress.md`.
- **Learnings:**
  - Patterns discovered: semantic execution belongs in the interpreter loop immediately after position/direction are set and before `ExecutionState.record_step`, keeping state mutation centralized and trace snapshots meaningful.
  - Gotchas encountered: once `○` performs real input reads, existing traversal-only tests must provide dummy input values or intentionally assert `InterpreterInputError`.
  - Quality gates: `python -m pytest`, `python -m mypy .`, and `python -m ruff check .` could not run because `python` is not on PATH; `python3 -m pytest`, `python3 -m compileall -q src tests`, and `git diff --check` pass, while `mypy` and `ruff` are not installed for `python3`.
---

## 2026-05-11 - US-006
- Implemented a context-aware transform registry API for `△` using `TransformContext`, `Transform`, and `TransformRegistry`.
- Kept the default transform registry mapping `△` to identity while allowing callers to pass or mutate registries programmatically.
- Updated interpreter `△` execution to pass symbol, current value, and mutable execution state into transform callbacks, with the callback return value becoming the next flow value.
- Added semantics tests for configured custom behavior, programmatic registration, numeric increment, and transform access to execution state/memory.
- Files changed: `src/geobe/transforms.py`, `src/geobe/interpreter.py`, `src/geobe/__init__.py`, `tests/test_interpreter_semantics.py`, `.ralph-tui/progress.md`.
- **Learnings:**
  - Patterns discovered: context dataclasses make callback APIs extensible while preserving a single typed argument for custom behavior.
  - Gotchas encountered: the previous one-argument transform callable did not expose execution state, so tests and custom transform examples needed to move to the explicit context contract.
  - Quality gates: `python -m pytest`, `python -m mypy .`, and `python -m ruff check .` could not run because `python` is not on PATH; `python3 -m pytest`, `python3 -m compileall -q src tests`, and `git diff --check` pass, while `mypy` and `ruff` are not installed for `python3`.
---
