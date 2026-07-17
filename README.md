# Geobe

Geobe is an experimental geometric esolang toolkit written in Python. Its
most complete experience is an interactive triangle-alphabet console. It also
includes a small interpreter for 2D Unicode-symbol programs.

Geobe is not yet a general-purpose programming language. The current runtime is
an experiment in directional flow, one memory cell, input/output nodes,
pluggable transforms, and array traversal.

## Interactive Triangle Console

Start the console:

```console
geobe --console
```

Type lowercase ASCII letters and Geobe immediately renders their geometric
encoding. Press Enter to decode the visible symbols back to English.

To print an offline Portuguese translation on Enter instead, run:

```console
geobe --console --console-output-language portuguese
```

Portuguese output is backed by bundled FreeDict English-Portuguese dictionary
data plus a compact exact-match Tatoeba sentence-pair table. It does not call a
remote translation API.

For example, typing `hello!` displays:

```text
▹▶▿▿◂!
```

Pressing Enter then prints:

```text
hello!
```

Backspace removes the most recent encoded character. Press Ctrl-C or Ctrl-D to
exit. Uppercase letters, numbers, spaces, and punctuation pass through unchanged.

## Web Translator Page

The project site includes an offline multilingual translator at
[`/geobe/translator/`](https://careylzh.github.io/geobe/translator/). Type in
English (or the selected language, after pressing swap), watch the text render
in the triangle alphabet, then press Enter to fill a split English/target
panel. Supported targets are English, Mandarin Chinese (Simplified),
Portuguese (Brazil), Vietnamese, and French, in both directions.

Every language pack is bundled with the page — FreeDict and Wiktionary
dictionary layers plus OPUS Tatoeba exact-match sentence tables — so no
remote translation API is called. Packs are generated offline by
`scripts/build_language_packs.py`; sources and licenses are listed in
`THIRD_PARTY_NOTICES.md`.

## Quick Start

Install the CLI:

```console
pipx install geobe
```

Run a small program that reads one input value and writes it to output:

```console
geobe --code "○→▽" --input hello
```

Expected output:

```json
{"outputs": ["hello"]}
```

## What Exists Today

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

The triangle alphabet is deliberately separate from the execution model. In a
`.geo` file, `spell ▹▶▿▿◂` is parser shorthand for a literal string output. In
`geobe --console`, typing lowercase English letters shows their triangle-symbol
encoding and Enter decodes the visible line back to English.

## Installation

The project targets Python 3.11+.

For normal CLI use, install Geobe with `pipx`:

```console
pipx install geobe
```

To install a specific release:

```console
pipx install geobe==0.1.1
```

If `pipx` is not installed and you use Homebrew on macOS:

```console
brew install pipx
pipx ensurepath
pipx install geobe
```

If `pipx` is not installed in another Python environment, follow the
[pipx installation guide](https://pipx.pypa.io/stable/installation/).

For local development from a cloned checkout, install Geobe in a virtual
environment:

```console
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e ".[dev]"
```

Avoid installing Geobe into a system Python with `pip install geobe`. On modern
macOS Homebrew Python and some Linux distributions, pip may fail with
`externally-managed-environment` because the operating system or package manager
owns that Python installation. Use `pipx install geobe` for the CLI, or install
inside a virtual environment for development.

## Running Programs

Run a `.geo` file:

```console
geobe examples/input_store_transform_output.geo --input hello
```

```json
{"outputs": ["hello"]}
```

Run inline source:

```console
geobe --code "○→▽" --input hello
```

```json
{"outputs": ["hello"]}
```

Run a literal string program:

```console
geobe --code "«hello, Geobe!»→▽"
```

```json
{"outputs": ["hello, Geobe!"]}
```

Read additional input values from standard input:

```console
printf 'first\nsecond\n' | geobe --code "○→▽\n○→▽" --stdin-input
```

```json
{"outputs": ["first", "second"]}
```

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

Triangle alphabet shorthand:

```geo
spell ▹▶▿▿◂ ◮◂ ◣▿▵!
```

This decodes to `hello world!` and is expanded by the parser into a literal
string output program.

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
