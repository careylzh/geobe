# Geometric interpreter

Geobe programs are rectangular text grids. The interpreter finds each source
node and follows arrows until the path ends.

## Run a program

Execute inline source:

```console
geobe --code "○→▽" --input hello
```

Expected output:

```json
{"outputs": ["hello"]}
```

Run a `.geo` file instead:

```console
geobe examples/input_store_transform_output.geo --input hello
```

## Core symbols

| Symbol | Meaning |
| --- | --- |
| `○` | Read the next input value |
| `□` | Store the current value in memory |
| `△`, `▲` | Transform the current value |
| `▽`, `◀` | Append the current value to output |
| `▶` | Start array traversal |
| `▶▶` | Continue or finish array traversal |
| `→`, `←`, `↑`, `↓` | Set execution direction |
| `«... »` | Read a literal string |

## Trace execution

Request machine-readable trace output:

```console
geobe --code "○→□→▽" --input hello --trace
```

For readable terminal output, add `--trace-format text`.

## Current boundaries

The interpreter has deterministic path traversal, one memory cell, buffered
input and output, and pluggable transforms. It does not yet include general
expressions, named variables, conditional blocks, functions, or classes.
