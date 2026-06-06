---
title: Geobe
---

# Geobe

Geobe is an experimental geometric esolang toolkit. Today it has two closely
related pieces:

- a small interpreter for 2D Unicode-symbol programs where arrows guide
  execution through input, memory, transform, traversal, and output nodes
- a triangle alphabet that maps geometric symbols to lowercase English letters
  for `spell` programs and the interactive `geobe --console` mode

The project is currently an MVP, not a complete general-purpose language. The
alphabet is a spelling layer on top of the runtime, while grid execution remains
the language core.

## Triangle Alphabet

The `spell` directive decodes Geobe's geometric alphabet symbols into lowercase
English letters. Parser expansion turns a `spell ...` line into a literal
string output program.

| Letter | Geometry |
| --- | --- |
| a | ▲ |
| b | △ |
| c | ▴ |
| d | ▵ |
| e | ▶ |
| f | ▷ |
| g | ▸ |
| h | ▹ |
| i | ▼ |
| j | ▽ |
| k | ▾ |
| l | ▿ |
| m | ◀ |
| n | ◁ |
| o | ◂ |
| p | ◃ |
| q | ◢ |
| r | ◣ |
| s | ◤ |
| t | ◥ |
| u | ◬ |
| v | ◭ |
| w | ◮ |
| x | ◸ |
| y | ◹ |
| z | ◺ |

Example:

```geo
spell ▹▶▿▿◂ ◮◂ ◣▿▵!
```

Decodes to:

```text
hello world!
```

The same mapping powers `geobe --console`: typed lowercase letters are shown as
triangle symbols, and Enter decodes the visible line back to English.
