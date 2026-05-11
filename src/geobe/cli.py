"""Command-line interface for Geobe."""

from __future__ import annotations

import argparse
from collections.abc import Sequence


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="geobe",
        description="Run geometric esoteric language programs.",
    )
    parser.add_argument(
        "program",
        nargs="?",
        help="Path to a .geo file. Inline execution will be added in a later story.",
    )
    parser.add_argument(
        "-i",
        "--input",
        dest="inputs",
        action="append",
        default=[],
        help="Input value supplied to the program. Repeat to pass multiple strings.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the Geobe CLI."""
    parser = build_parser()
    parser.parse_args(argv)
    return 0
