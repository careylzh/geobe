# Geobe Examples

Geobe currently combines a small 2D-symbol interpreter with a triangle alphabet
spelling layer. The first examples exercise runtime flow through input, memory,
transform, traversal, and output nodes. The `spell` example shows parser
shorthand that decodes triangle symbols into lowercase text output.

## Core Symbols

- `○` reads the next input value into the current flow.
- `→`, `←`, `↑`, and `↓` move execution through the grid.
- `□` stores the current value in the default memory cell.
- `△` transforms the current value. The default transform is identity.
- `▲` represents change/delta and transforms the current value. The default
  transform is identity.
- `▽` appends the current value to the output list.
- `◀` appends the current value to the output list.
- `▶` traverses the current array by one index.
- `▶▶` continues the current array loop or finishes it when exhausted.

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
$ python3 -m geobe
{"outputs": ["demo-value"]}
```

## `hello_world_new_mappings.geo`

Program:

```geo
«Hello, world!»→▲→◀
```

Expected behavior:

1. `«Hello, world!»` sets the current value.
2. `→` moves right.
3. `▲` applies the default identity delta transform.
4. `→` moves right.
5. `◀` appends `Hello, world!` to the output list.

Run it with the CLI:

```console
$ geobe examples/hello_world_new_mappings.geo
{"outputs": ["Hello, world!"]}
```

## `hello_world_spell.geo`

Program:

```geo
spell ▹▶▿▿◂ ◮◂ ◣▿▵!
```

Expected behavior:

1. `spell` decodes triangle alphabet symbols into lowercase letters.
2. `▹▶▿▿◂ ◮◂ ◣▿▵!` becomes `hello world!`.
3. The parser expands the line to a literal string output program.
4. The decoded string is emitted as the program output.

Run it with the CLI:

```console
$ geobe examples/hello_world_spell.geo
{"outputs": ["hello world!"]}
```

## `custom_transform.py`

This Python example registers a custom `△` transform. The transform receives a `TransformContext`, reads `context.current_value`, and returns a bracketed string.

Run it from the repository root:

```console
$ PYTHONPATH=src python examples/custom_transform.py
{"outputs": ["[custom]"]}
```
