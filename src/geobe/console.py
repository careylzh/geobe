"""Interactive terminal console for Geobe spelling symbols."""

from __future__ import annotations

import re
import sys
import termios
import tty
from collections.abc import Iterator
from contextlib import contextmanager
from typing import TextIO

from geobe.parser import decode_spell_text, encode_spell_text

BACKSPACE_CHARACTERS = {"\b", "\x7f"}
ENTER_CHARACTERS = {"\n", "\r"}
EXIT_CHARACTERS = {"\x03", "\x04"}
PORTUGUESE_WORDS = {
    "a": "um",
    "am": "sou",
    "and": "e",
    "are": "e",
    "day": "dia",
    "english": "ingles",
    "friend": "amigo",
    "geobe": "geobe",
    "good": "bom",
    "hello": "ola",
    "hi": "oi",
    "i": "eu",
    "is": "e",
    "love": "amo",
    "morning": "manha",
    "night": "noite",
    "no": "nao",
    "or": "ou",
    "please": "por favor",
    "portuguese": "portugues",
    "thanks": "obrigado",
    "the": "o",
    "to": "para",
    "welcome": "bem-vindo",
    "world": "mundo",
    "yes": "sim",
    "you": "voce",
}
PORTUGUESE_PHRASES = {
    "hello world": "ola mundo",
    "hello, world": "ola, mundo",
    "good morning": "bom dia",
    "good night": "boa noite",
    "thank you": "obrigado",
}


def run_console(
    input_stream: TextIO | None = None,
    output_stream: TextIO | None = None,
    *,
    output_language: str = "english",
) -> int:
    """Run the interactive spelling console until EOF or Ctrl-C."""
    input_stream = input_stream if input_stream is not None else sys.stdin
    output_stream = output_stream if output_stream is not None else sys.stdout

    with _raw_terminal(input_stream):
        _run_console_loop(input_stream, output_stream, output_language=output_language)
    return 0


def render_console_keypress(character: str) -> str:
    """Return the visible terminal character for a typed key."""
    if len(character) != 1:
        return character
    if "a" <= character <= "z":
        return encode_spell_text(character)
    return character


def decode_console_line(line: str) -> str:
    """Decode a visible console line back to English equivalent text."""
    return decode_spell_text(line)


def translate_console_line(line: str, output_language: str = "english") -> str:
    """Decode a visible console line and return it in the requested language."""
    decoded = decode_console_line(line)
    if output_language == "english":
        return decoded
    if output_language == "portugese":
        output_language = "portuguese"
    if output_language == "portuguese":
        return _translate_english_to_portuguese(decoded)
    msg = f"Unsupported console output language: {output_language}"
    raise ValueError(msg)


def _run_console_loop(
    input_stream: TextIO,
    output_stream: TextIO,
    *,
    output_language: str,
) -> None:
    line: list[str] = []

    while True:
        character = input_stream.read(1)
        if character == "" or character in EXIT_CHARACTERS:
            return
        if character in ENTER_CHARACTERS:
            output_stream.write("\n")
            output_stream.write(
                f"{translate_console_line(''.join(line), output_language)}\n",
            )
            output_stream.flush()
            line.clear()
            continue
        if character in BACKSPACE_CHARACTERS:
            if line:
                line.pop()
                output_stream.write("\b \b")
                output_stream.flush()
            continue

        rendered = render_console_keypress(character)
        line.append(rendered)
        output_stream.write(rendered)
        output_stream.flush()


def _translate_english_to_portuguese(text: str) -> str:
    phrase_key = re.sub(r"\s+", " ", text.strip().lower())
    if phrase_key in PORTUGUESE_PHRASES:
        return PORTUGUESE_PHRASES[phrase_key]

    def replace_word(match: re.Match[str]) -> str:
        word = match.group(0)
        translated = PORTUGUESE_WORDS.get(word.lower(), word)
        if word.isupper():
            return translated.upper()
        if word[:1].isupper():
            return translated.capitalize()
        return translated

    return re.sub(r"[A-Za-z]+", replace_word, text)


@contextmanager
def _raw_terminal(input_stream: TextIO) -> Iterator[None]:
    if not input_stream.isatty():
        yield
        return

    file_descriptor = input_stream.fileno()
    attributes = termios.tcgetattr(file_descriptor)
    try:
        tty.setraw(file_descriptor)
        yield
    finally:
        termios.tcsetattr(file_descriptor, termios.TCSADRAIN, attributes)
