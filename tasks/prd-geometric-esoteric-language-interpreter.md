# PRD: Geometric Esoteric Language Interpreter

## Overview
Build a Python 3 interpreter for a new esoteric spatial programming language where programs are represented as ASCII/Unicode geometric diagrams on a 2D grid. The interpreter will parse multiline text or `.geo` files, traverse directional flow arrows from input source nodes, execute semantic symbols, and expose both a reusable Python library and a CLI runner.

The repository currently appears minimal, so this PRD assumes a new standalone Python package will be introduced under this repo with modern packaging, tests, typing, linting, and a command-line entry point.

## Goals
- Implement a reusable Python library for parsing and executing geometric grid programs.
- Provide a CLI that can run inline programs or `.geo` files.
- Support the core symbols: `○`, `□`, `△`, `▽`, `→`, `←`, `↑`, `↓`.
- Support user-defined transformations for `△` through an extensible registry or callback system.
- Produce deterministic execution traces for debugging.
- Keep the architecture modular enough for future branching, concurrency, annotations, and additional symbols.

## Quality Gates
These commands must pass for every user story:
- `python -m pytest` - Automated tests
- `python -m mypy .` - Static type checking
- `python -m ruff check .` - Linting

## User Stories

### US-001: Project Structure and Packaging
**Description:** As a Python developer, I want a standard package structure so that the interpreter can be used as both a library and CLI.

**Acceptance Criteria:**
- [ ] A Python package is created for the geometric language interpreter.
- [ ] The project includes a `pyproject.toml` with package metadata, CLI entry point, pytest, mypy, and ruff configuration.
- [ ] Source code is organized into clear modules for parser, model/state, interpreter/engine, transforms, and CLI.
- [ ] Tests are placed in a dedicated test directory.
- [ ] The package can be imported from tests without modifying `sys.path` manually.

### US-002: Grid Parser
**Description:** As a language user, I want multiline diagram text converted into a normalized 2D grid so that spatial programs can be interpreted.

**Acceptance Criteria:**
- [ ] The parser accepts a multiline string.
- [ ] The parser preserves spaces and meaningful Unicode symbols.
- [ ] Rows are normalized to a rectangular grid by padding shorter rows with spaces.
- [ ] The parser exposes grid width, height, and safe position lookup.
- [ ] Empty input is handled with a clear validation error.
- [ ] Unit tests cover uneven row lengths, Unicode symbols, whitespace, and invalid empty programs.

### US-003: Core Execution State
**Description:** As an interpreter developer, I want explicit execution state so that program behavior is observable and extensible.

**Acceptance Criteria:**
- [ ] Execution state tracks the current position, current direction, current value, memory store, input buffer, output buffer, visited steps, and execution trace.
- [ ] Input values can be supplied as a list of Python values or strings from the CLI.
- [ ] Output values are collected in order.
- [ ] Memory store behavior for `□` is deterministic and documented.
- [ ] State objects use typed Python structures suitable for mypy checking.

### US-004: Directional Flow Traversal
**Description:** As a language user, I want execution to follow arrow symbols so that geometry defines control flow.

**Acceptance Criteria:**
- [ ] Execution starts from each `○` source node found in the grid.
- [ ] The MVP executes flows deterministically in a single-threaded order.
- [ ] Arrow symbols `→`, `←`, `↑`, and `↓` set or continue movement direction.
- [ ] Node traversal skips whitespace while moving in the active direction until it reaches a semantic symbol, arrow, boundary, or dead end.
- [ ] If no valid direction is available from a node, that flow terminates cleanly.
- [ ] The engine has an explicit maximum step limit to prevent infinite loops.
- [ ] Tests cover left-to-right, right-to-left, vertical, dead-end, boundary, and step-limit behavior.

### US-005: Core Symbol Semantics
**Description:** As a language user, I want the core geometric symbols to execute predictable behavior so that simple diagrams can process data.

**Acceptance Criteria:**
- [ ] `○` reads the next input value into the current flow.
- [ ] `□` stores the current flow value in memory.
- [ ] `△` transforms the current flow value using the configured transform behavior.
- [ ] `▽` appends the current flow value to the output buffer.
- [ ] Default `△` behavior is identity transformation.
- [ ] Missing input at `○` is handled with a clear interpreter error.
- [ ] Tests verify input, storage, identity transform, output, and error cases.

### US-006: User-Defined Transformations
**Description:** As a Python developer, I want to register custom behavior for `△` so that the language can perform real computation beyond identity transforms.

**Acceptance Criteria:**
- [ ] The interpreter accepts a transformation registry or callback configuration.
- [ ] The default transform registry maps `△` to identity.
- [ ] Custom transforms can be registered programmatically when using the library.
- [ ] Transform functions receive enough context to inspect current value and execution state.
- [ ] Transform functions return the next flow value.
- [ ] Tests demonstrate at least one custom transform, such as uppercasing a string or incrementing a number.

### US-007: CLI Runner
**Description:** As a command-line user, I want to run geometric programs from files or inline strings so that I can execute `.geo` programs outside Python code.

**Acceptance Criteria:**
- [ ] A CLI command is exposed through the package entry point.
- [ ] The CLI can run a `.geo` file path.
- [ ] The CLI can run an inline program string.
- [ ] The CLI accepts input values through arguments or stdin.
- [ ] The CLI prints output values in a predictable format.
- [ ] The CLI has an option to print the execution trace.
- [ ] CLI errors produce non-zero exit codes and readable messages.
- [ ] Tests cover successful file execution, inline execution, trace mode, and invalid input.

### US-008: Execution Trace and Debug Output
**Description:** As a developer debugging spatial programs, I want an execution trace so that I can understand how the interpreter moved through the grid.

**Acceptance Criteria:**
- [ ] Each executed step records position, symbol, direction, input value/current value, output changes, and memory changes when relevant.
- [ ] Trace records are structured data in the library API.
- [ ] The CLI can render trace records as readable text.
- [ ] Trace output is deterministic for the same program and input.
- [ ] Tests assert trace content for a small known program.

### US-009: Example Programs and Demo Runner
**Description:** As a new user, I want example programs so that I can understand how the language works quickly.

**Acceptance Criteria:**
- [ ] The repository includes at least one `.geo` example for input-store-transform-output behavior.
- [ ] The repository includes at least one example demonstrating a custom transform through Python code.
- [ ] Running the package module directly or invoking the CLI demonstrates the example behavior.
- [ ] Documentation explains the core symbols and expected output for each example.
- [ ] Tests verify that the documented example program produces the expected output.

## Functional Requirements
- FR-1: The system must parse multiline program text into a rectangular 2D grid.
- FR-2: The system must preserve Unicode geometric symbols during parsing.
- FR-3: The system must discover `○` source nodes as execution start points.
- FR-4: The system must maintain explicit execution state for each flow.
- FR-5: The system must support the symbols `○`, `□`, `△`, `▽`, `→`, `←`, `↑`, and `↓`.
- FR-6: The system must read input values when visiting `○`.
- FR-7: The system must store the current value when visiting `□`.
- FR-8: The system must apply a transform when visiting `△`.
- FR-9: The system must append current values to output when visiting `▽`.
- FR-10: The system must terminate flows cleanly at dead ends or grid boundaries.
- FR-11: The system must expose a Python API for parsing and interpreting programs.
- FR-12: The system must expose a CLI for running inline programs and `.geo` files.
- FR-13: The system must support user-defined transformations for `△`.
- FR-14: The system must provide structured execution traces.
- FR-15: The system must enforce a configurable maximum step count.

## Non-Goals
- Full concurrent multi-flow execution is out of scope for the initial implementation.
- Visual step-by-step terminal animation is out of scope.
- Graphical editor support is out of scope.
- Complex expression syntax inside the grid is out of scope.
- Persistent variables beyond the runtime memory store are out of scope.
- Network or external I/O beyond stdin/file loading is out of scope.
- A formal language specification beyond implementation docs is out of scope for MVP.

## Technical Considerations
- The repo currently appears to contain only `PROMPT.md` and Ralph metadata, so implementation should introduce a clean Python project structure.
- Suggested structure:
  - `pyproject.toml`
  - `src/geobe/__init__.py`
  - `src/geobe/parser.py`
  - `src/geobe/grid.py`
  - `src/geobe/state.py`
  - `src/geobe/transforms.py`
  - `src/geobe/interpreter.py`
  - `src/geobe/cli.py`
  - `examples/basic.geo`
  - `tests/`
- The interpreter should use typed dataclasses or similarly typed structures.
- Unicode handling should rely on normal Python `str` behavior, with tests proving symbol preservation.
- Transform extension should avoid dynamic imports for MVP; programmatic registration is enough.
- CLI file loading should use UTF-8.
- Future branching should be supported by keeping flow state separable from global interpreter state.

## Success Metrics
- A user can run the sample `.geo` program from the CLI and see the input value emitted unchanged.
- A developer can import the package, register a custom transform, and execute a program in Python.
- Execution traces make movement and symbol execution understandable without reading interpreter internals.
- All quality gates pass: `python -m pytest`, `python -m mypy .`, and `python -m ruff check .`.
- The codebase is modular enough that adding a new symbol does not require rewriting parser or CLI code.

## Open Questions
- Should `□` memory be a single implicit cell for MVP, or should future versions allow multiple named/addressed storage nodes?
- Should multiple `○` nodes consume from the same global input buffer or each receive an independent copy?
- Should `▽` terminate a flow after output, or allow flow to continue if arrows are present?
- Should annotations/comments be ignored in MVP or deferred entirely?