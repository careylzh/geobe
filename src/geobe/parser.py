"""Parser entry points for geometric programs."""

from __future__ import annotations


def parse_program(source: str) -> list[list[str]]:
    """Parse source text into a provisional character grid.

    Normalization and validation are implemented by the parser story.
    """
    return [list(line) for line in source.splitlines()]
