"""Smoke tests for package structure and imports."""

from __future__ import annotations

import tomllib
from pathlib import Path

import geobe
from geobe.cli import build_parser
from geobe.interpreter import Interpreter


def test_package_imports_without_sys_path_changes() -> None:
    assert geobe.__version__ == "0.1.0"
    assert Interpreter().run("").program == ""


def test_cli_entry_point_is_configured() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    assert pyproject["project"]["scripts"]["geobe"] == "geobe.cli:main"


def test_cli_parser_exists() -> None:
    parser = build_parser()

    assert parser.prog == "geobe"
