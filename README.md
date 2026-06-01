# Geobe

Geobe is a geometric esoteric programming language interpreter written in Python.
Programs are 2D grids of Unicode symbols where arrows control flow and shapes
carry semantics.

## Overview

Geobe programs are rectangular text grids. The interpreter finds every `○`
source node and follows directional flow through the grid until a path ends.
The current MVP supports a single deterministic memory cell, input buffering,
output collection, and pluggable `△` transforms.

Core symbols:

- `○` read the next input value
- `□` store the current value in memory
- `△` transform the current value
- `▲` change/delta transform the current value
- `▽` append the current value to output
- `◀` append the current value to output
- `▶` traverse the current array by one index
- `▶▶` continue the current array loop, or finish when exhausted
- `→`, `←`, `↑`, `↓` move execution through the grid
- `«... »` read a literal string into the current value
- `spell ...` decode triangle alphabet symbols into lowercase text output

Spaces are treated as empty cells for traversal. Other non-traversable
characters stop a path.

## Installation

The project targets Python 3.11+.

```console
#cd into project root:
python3 -m pip install .
```

## Running Programs

Run a `.geo` file:

```console
geobe examples/input_store_transform_output.geo --input hello
```

Run inline source:

```console
geobe --code "○→▽" --input hello
```

Run a literal string program:

```console
geobe --code "«hello, Geobe!»→▽"
```

Read additional input values from standard input:

```console
printf 'first\nsecond\n' | geobe --code "○→▽\n○→▽" --stdin-input
```

Start the interactive spelling console:

```console
geobe --console
```

In console mode, lowercase letters are echoed as Geobe's mapped alphabet
symbols. Pressing Enter prints the English equivalent of the current line.
For example, typing `hello!` displays `▹▶▿▿◂!`, then Enter prints `hello!`.

Trace execution as JSON:

```console
geobe --code "○→□→▽" --input hello --trace
```

Trace execution in readable text:

```console
geobe --code "○→□→▽" --input hello --trace --trace-format text
```

Running the package module directly executes the built-in demo program:

```console
python3 -m geobe
```

## Example Program

`examples/input_store_transform_output.geo`

```geo
○→□→△→▽
```

With input `hello`, the program stores the value, applies the default identity
transform, and outputs `hello`.

Array loop:

```geo
○→▶→◀→▶▶
```

With Python input `[1, 2, 3]`, the program traverses the array and outputs
`[1, 2, 3]`.

Spelled text:

```geo
spell ▹▶▿▿◂ ◮◂ ◣▿▵!
```

This decodes to `hello world!` and outputs it.

Python code can also encode English into the triangle alphabet:

```python
from geobe.parser import encode_spell_text

encoded = encode_spell_text("Hello world!")
```

## Custom Transforms

The `△` symbol is backed by a transform registry. The default transform is
identity, and you can register your own behavior in Python code.

See `examples/custom_transform.py` for a minimal example that returns a custom
formatted value.

## Development

Run the test suite:

```console
pytest
```

Run linting and type checks:

```console
ruff check .
mypy src tests
```

## Project Layout

- `src/geobe/` interpreter, parser, runtime state, and CLI
- `examples/` documented sample programs
- `tests/` coverage for the CLI, parser, interpreter, and examples

## Package Entry Points

- `geobe` CLI: `geobe.cli:main`
- Module entry point: `python3 -m geobe`
