"""Tests for the interactive spelling console."""

from __future__ import annotations

from io import StringIO

from geobe.console import (
    decode_console_line,
    render_console_keypress,
    run_console,
)


def test_render_console_keypress_maps_lowercase_letters_to_symbols() -> None:
    assert render_console_keypress("a") == "▲"
    assert render_console_keypress("z") == "◺"


def test_render_console_keypress_preserves_non_lowercase_characters() -> None:
    assert render_console_keypress("A") == "A"
    assert render_console_keypress("!") == "!"


def test_decode_console_line_returns_english_equivalent_text() -> None:
    assert decode_console_line("▹▶▿▿◂ ◮◂◣▿▵!") == "hello world!"


def test_console_echoes_symbols_then_prints_decoded_text_on_enter() -> None:
    output_stream = StringIO()

    exit_code = run_console(StringIO("hello!\n"), output_stream)

    assert exit_code == 0
    assert output_stream.getvalue() == "▹▶▿▿◂!\nhello!\n"


def test_console_supports_backspace_before_enter() -> None:
    output_stream = StringIO()

    exit_code = run_console(StringIO("az\x7fb\n"), output_stream)

    assert exit_code == 0
    assert output_stream.getvalue() == "▲◺\b \b△\nab\n"
