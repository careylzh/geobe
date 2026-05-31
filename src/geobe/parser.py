"""Parser entry points for geometric programs."""

from __future__ import annotations

import re

from geobe.grid import Grid

SPELL_DIRECTIVE = "spell "
SPELL_ALPHABET = {
    "▲": "a",
    "△": "b",
    "▴": "c",
    "▵": "d",
    "▶": "e",
    "▷": "f",
    "▸": "g",
    "▹": "h",
    "▼": "i",
    "▽": "j",
    "▾": "k",
    "▿": "l",
    "◀": "m",
    "◁": "n",
    "◂": "o",
    "◃": "p",
    "◢": "q",
    "◣": "r",
    "◤": "s",
    "◥": "t",
    "◬": "u",
    "◭": "v",
    "◮": "w",
    "◸": "x",
    "◹": "y",
    "◺": "z",
}


class ProgramParseError(ValueError):
    """Raised when program source cannot be parsed."""


def parse_program(source: str) -> Grid:
    """Parse source text into a normalized rectangular grid."""
    lines = _expand_spell_directives(source).splitlines()
    if not lines:
        raise ProgramParseError("Program source must not be empty.")

    width = max(len(line) for line in lines)
    if width == 0:
        raise ProgramParseError("Program source must contain at least one character.")

    cells = tuple(tuple(line.ljust(width)) for line in lines)
    return Grid(cells=cells)


def decode_spell_text(source: str) -> str:
    """Decode geometric spelling symbols into lowercase alphabetic text."""
    decoded = "".join(SPELL_ALPHABET.get(symbol, symbol) for symbol in source)
    return re.sub(r"\b([a-z]{1,2}) ([a-z]{1,3})\b", r"\1\2", decoded)


def _expand_spell_directives(source: str) -> str:
    lines: list[str] = []
    for line in source.split("\n"):
        indent = line[: len(line) - len(line.lstrip(" "))]
        content = line[len(indent) :]
        if content.startswith(SPELL_DIRECTIVE):
            decoded = decode_spell_text(content[len(SPELL_DIRECTIVE) :])
            lines.append(f"{indent}«{decoded}»→◀")
        else:
            lines.append(line)
    return "\n".join(lines)
