# From Geometric Toolkit to Small Programming Language

## Question, scope, and method

This bounded repo synthesis asks: what minimum architecture and feature sequence
would turn Geobe from its current geometric interpreter and spelling console into
a usable programming language while preserving Python-like simplicity?

The analysis covers the current parser, interpreter, state model, CLI, tests, and
README as of 2026-06-30, together with primary Python language documentation and
the implementation-oriented *Crafting Interpreters* text. It is a design guide,
not a claim that Geobe currently implements the proposed syntax.

## Current baseline

Geobe currently parses source directly into a rectangular character grid. The
interpreter finds source nodes, follows arrows, and mutates one execution state.
It supports literals, input, one memory slot, transforms, output, and array
traversal. `spell` is parser shorthand, while `geobe --console` is an alphabet
encoder/decoder. There is no token stream, abstract syntax tree (AST), general
expression evaluator, named environment, conditional branch, reusable function,
or user-defined type.

That is enough for an esoteric data-flow experiment, but not yet enough for users
to express general algorithms. The first useful milestone is therefore a small
procedural language—not simultaneous support for procedural, functional, and
object-oriented programming.

## How small languages are generally implemented

A conventional interpreter separates these responsibilities:

1. **Scanning/tokenization:** source characters become tokens with locations.
2. **Parsing:** tokens become an AST according to an explicit grammar.
3. **Static checks/resolution:** names and structurally invalid constructs are
   diagnosed before execution where practical.
4. **Evaluation:** AST nodes operate on runtime values in an environment.
5. **Runtime services:** calls, errors, built-ins, and later modules or objects
   sit behind stable interfaces.

This separation matters more than whether execution uses a tree-walk interpreter,
bytecode, or native code. For Geobe, a tree-walk AST evaluator is the smallest
appropriate next architecture. Bytecode and a virtual machine should wait until
profiling or portability requirements justify their complexity.

Python's readable surface comes from a small set of consistent rules: lexical
tokens, newline-delimited simple statements, indentation-delimited suites,
names bound without separate declarations, and compound statements whose headers
end in a colon. Python itself is a large language; Geobe should copy these
clarity principles, not its entire feature set.

## Recommended Geobe language core

Preserve geometric symbols where they add identity, but give each construct one
clear meaning and provide text-friendly keywords for structure. A first coherent
grammar could support:

```text
program      := statement* EOF
statement    := "let" NAME "=" expression NEWLINE
              | "emit" expression NEWLINE
              | "if" expression ":" suite
              | "while" expression ":" suite
              | "for" NAME "in" expression ":" suite
              | "def" NAME "(" parameters? ")" ":" suite
              | "return" expression? NEWLINE
              | expression NEWLINE
suite        := NEWLINE INDENT statement+ DEDENT
expression   := equality
equality     := comparison (("==" | "!=") comparison)*
comparison   := term (("<" | "<=" | ">" | ">=") term)*
term         := factor (("+" | "-") factor)*
factor       := unary (("*" | "/") unary)*
unary        := ("not" | "-") unary | call
call         := primary ("(" arguments? ")")*
primary      := NUMBER | STRING | "true" | "false" | "none"
              | NAME | list | "(" expression ")"
```

`let` is intentionally explicit in the first version even though Python uses
plain assignment. It makes initial binding unambiguous, leaves room for later
reassignment syntax, and gives better errors. Once semantics are stable, Geobe
can decide whether `name = value` is sufficiently clear.

Runtime values should initially be `none`, booleans, numbers, strings, and lists.
Use lexical environments chained by parent scope. Functions should be first-class
values with closures, positional parameters, and explicit `return`. Built-ins
such as `input`, `emit`, `len`, and `range` should use the same call protocol as
user functions.

The existing grid interpreter should remain available as a documented legacy or
geometric mode while the new grammar matures. Do not silently reinterpret old
`.geo` files. Select the mode explicitly (for example by file directive or CLI
flag) until a migration path is defined.

## Staged roadmap

### 1. Expressions and diagnostics

- Add a token type and source-span model.
- Implement a scanner and precedence parser.
- Add literal values and arithmetic/comparison/boolean expressions.
- Report filename, line, column, offending token, and a useful message.
- Test scanner, parser, evaluator, and error output independently.

This makes the parser architecture real before control flow multiplies edge
cases.

### 2. Names and sequential programs

- Add environments and `let` bindings.
- Add expression and `emit` statements.
- Define truthiness and equality once, centrally.
- Provide a non-interactive runner and a REPL using the same parser/evaluator.

### 3. Structured control flow

- Tokenize `NEWLINE`, `INDENT`, and `DEDENT` using an indentation stack.
- Add `if`/`else`, `while`, then `for` over iterables.
- Add `break` and `continue` only after loops work end-to-end.
- Keep suites syntactically uniform; avoid special geometric exceptions inside
  blocks.

### 4. Functions and a functional style

- Add definitions, calls, parameters, closures, and `return`.
- Make functions first-class values so users can pass and return them.
- Prefer ordinary functions plus list operations before adding lambdas,
  comprehensions, decorators, or pattern matching.

### 5. Objects only after demonstrated need

Start with records or dictionaries if programs need grouped state. Add classes
only when concrete Geobe programs show that identity, encapsulated mutable state,
and method dispatch improve the language. OOP is not a prerequisite for being a
programming language.

## Design constraints and rejected shortcuts

- **Do not encode every semantic distinction as a new Unicode glyph.** Glyphs
  are useful for the alphabet and spatial mode, but keywords improve typing,
  searchability, error messages, and accessibility for structured programs.
- **Do not parse control flow by extending direct grid traversal.** Nested blocks,
  precedence, and lexical scope need an explicit syntax representation.
- **Do not couple the console widget to interpreter internals.** Share pure codec
  functions and, later, a public evaluator API.
- **Do not add multiple paradigms as checklist features.** A small language with
  first-class functions already permits procedural and functional styles. Add
  objects only with use cases and semantics.
- **Do not optimize into bytecode early.** A tree-walk implementation is easier
  to inspect and change while syntax and semantics are unsettled.

## Confidence, limitations, and next decision

Confidence is high that Geobe needs explicit syntax, AST, environments, control
flow, and functions to support general algorithms. Confidence is moderate on the
exact proposed surface syntax because no user studies or representative Geobe
program corpus were supplied. The next defensible step is to write 5–10 example
programs (branching, looping, aggregation, and a reusable function), then accept
the grammar only if those examples remain concise and unambiguous.

## Source inventory

| ID | Source | Role and limitation |
| --- | --- | --- |
| S001 | `src/geobe/parser.py` | Current parsing behavior; direct grid construction and `spell` expansion. |
| S002 | `src/geobe/interpreter.py` | Current execution semantics; no general AST or named environments. |
| S003 | `src/geobe/state.py` | Current runtime state and value boundary. |
| S004 | `src/geobe/console.py` | Current interactive alphabet codec behavior. |
| S005 | `README.md` and `tests/` | Stated and tested product behavior; not an independent design authority. |
| S006 | [Python lexical analysis](https://docs.python.org/3/reference/lexical_analysis.html) | Primary specification for tokens, logical lines, and indentation. Python is much broader than the proposed language. |
| S007 | [Python execution model](https://docs.python.org/3/reference/executionmodel.html) | Primary specification for blocks, binding, environments, and scopes. |
| S008 | [Python compound statements](https://docs.python.org/3/reference/compound_stmts.html) | Primary specification for suites, control flow, functions, and classes. |
| S009 | [Crafting Interpreters](https://craftinginterpreters.com/contents.html) | Implementation-oriented secondary guide to scanning, parsing, evaluation, control flow, functions, classes, and bytecode. Its example language is not a Geobe specification. |

Nine sources were discovered, screened, and substantively examined. No claim of
comprehensive programming-language-design coverage is made.

## Claim-evidence ledger

| ID | Claim | Evidence | Status |
| --- | --- | --- | --- |
| C001 | Geobe lacks general expressions, names, branches, and functions. | S001–S005 | Supported by repository inspection. |
| C002 | Tokenization, parsing, environments, and evaluation are separable interpreter responsibilities. | S006–S009 | Supported; exact implementation remains a design choice. |
| C003 | Python-like readability can be approximated with statements, colon headers, and indentation suites. | S006–S008 | Supported as a Python design observation; suitability for Geobe remains to be tested. |
| C004 | A tree-walk evaluator is the smallest suitable next architecture. | S001–S009 | Agent design inference; supported but not uniquely required. |
| C005 | OOP and bytecode should be deferred. | S001–S009 | Normative recommendation based on current scope, not a universal language-design rule. |
