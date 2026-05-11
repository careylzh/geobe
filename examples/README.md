# Geobe Examples

## Core Symbols

- `○` reads the next input value into the current flow.
- `→`, `←`, `↑`, and `↓` move execution through the grid.
- `□` stores the current value in the default memory cell.
- `△` transforms the current value. The default transform is identity.
- `▽` appends the current value to the output list.

## `input_store_transform_output.geo`

Program:

```geo
○→□→△→▽
```

Expected behavior with input `hello`:

1. `○` reads `hello`.
2. `→` moves right.
3. `□` stores `hello`.
4. `→` moves right.
5. `△` applies the default identity transform, leaving `hello` unchanged.
6. `→` moves right.
7. `▽` outputs `hello`.

Run it with the CLI:

```console
$ geobe examples/input_store_transform_output.geo --input hello
{"outputs": ["hello"]}
```

Running the package module directly demonstrates the same input-store-transform-output flow with a built-in demo value:

```console
$ python -m geobe
{"outputs": ["demo-value"]}
```

## `custom_transform.py`

This Python example registers a custom `△` transform. The transform receives a `TransformContext`, reads `context.current_value`, and returns a bracketed string.

Run it from the repository root:

```console
$ PYTHONPATH=src python examples/custom_transform.py
{"outputs": ["[custom]"]}
```
