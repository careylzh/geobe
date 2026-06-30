---
title: Geobe
---

# Geobe

Geobe is an experimental geometric esolang toolkit. It combines a triangle
alphabet with a small interpreter for 2D Unicode-symbol programs.

Geobe is not yet a general-purpose programming language. Its current runtime is
an experiment in directional flow, one memory cell, input/output nodes,
pluggable transforms, and array traversal.

## Start here

Install the command-line interface:

```console
pipx install geobe
```

Then explore the visual alphabet:

```console
geobe --console
```

Typing lowercase letters displays their geometric encoding. Press Enter to
decode the visible symbols back to English.

## Choose a path

- [Learn the triangle alphabet](alphabet.md) for encoding, decoding, and the
  interactive console.
- [Explore the interpreter](interpreter.md) for grid execution, symbols, and
  example programs.

## Project status

The triangle alphabet and grid interpreter are related experiments with
different responsibilities. The alphabet maps text to shape. The interpreter
executes paths through a geometric grid. Neither should be read as a claim that
Geobe already provides the control structures or abstractions of a mature
programming language.

The [language design findings](https://github.com/careylzh/geobe/blob/main/LANGUAGE_DESIGN_FINDINGS.md)
describe a staged path toward expressions, names, control flow, and functions.
