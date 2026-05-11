`use this repo: /Users/careylai/Desktop/geobe`

You are an expert programming language designer and Python engineer.

Design and implement a Python-based interpreter for a new esoteric programming language where computation is represented using ASCII/Unicode geometric shapes arranged spatially in 2D grids.

====================
LANGUAGE CONCEPT
====================

The language encodes programs as diagrams like:

      △
○ → □
      ▽

Each symbol is a semantic operator:

CORE SYMBOLS:
- ○ = input source (read / stdin / external value)
- □ = storage / variable / memory node
- △ = transformation / function / computation
- ▽ = output / sink (print / return)
- → = directional flow (left-to-right execution)

Optional:
- ↑ ↓ ← → = directional flow modifiers

====================
EXECUTION MODEL
====================

1. Program is a 2D grid of characters (multiline string)
2. Execution starts at any ○ node
3. Flow follows arrows (→ ← ↑ ↓)
4. Nodes execute when visited
5. Output is collected from ▽
6. Multiple flows may exist (you may implement single-threaded traversal for MVP, but design should allow extension)

====================
REQUIRED FEATURES (MVP)
====================

1. PARSER
- Accept multiline string input
- Convert into a 2D grid (list of lists)

2. INTERPRETER ENGINE
- Traverse grid based on directional arrows
- Maintain execution state:
  - current position(s)
  - memory store (for □ nodes)
  - input buffer (for ○ nodes)
  - output buffer (for ▽ nodes)

3. SYMBOL SEMANTICS

Implement behavior:

○ : read input value into flow
□ : store current value
△ : transform value (start with identity function, but design extensible system)
▽ : output current value
→ ← ↑ ↓ : control movement

4. FLOW RULES
- Movement determined by arrows
- If no direction exists, terminate path
- Support branching if multiple directions exist (can be BFS/DFS or simplified single-path MVP)

====================
EXAMPLE PROGRAM
====================

      △
○ → □
      ▽

EXPECTED BEHAVIOR:
- Take input
- Store it
- Transform it (identity by default)
- Output unchanged value

====================
IMPLEMENTATION REQUIREMENTS
====================

- Use Python 3
- Modular architecture:
  - Parser
  - Interpreter
  - Execution Engine
- Include a demo runner (__main__)
- Print execution trace for debugging
- Keep code extensible for future symbol additions

====================
ADVANCED (OPTIONAL)
====================

If possible, include:
- User-defined transformations for △
- Multi-flow concurrency model
- Step-by-step visual debug mode
- Support for annotations in grid (ignored characters)
- File loading/saving for ".geo" programs

====================
DESIGN PHILOSOPHY
====================

This is a spatial programming language:
- Geometry defines syntax
- Flow defines execution
- English is a semantic interpretation layer, not the source of truth

Return:
1. Full Python implementation
2. Example program(s)
3. Short architecture explanation (max 10 lines)
