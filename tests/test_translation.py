"""Tests for English-to-Portuguese learning translations."""

from __future__ import annotations

from geobe.translation import translate_english_to_portuguese


def test_translates_exact_tatoeba_sentence_pairs() -> None:
    assert translate_english_to_portuguese("How are you?") == "Como você está?"
    assert translate_english_to_portuguese("Good morning!") == "Bom dia!"


def test_falls_back_to_freedict_dictionary_translation() -> None:
    assert translate_english_to_portuguese("the red book") == "a rubro livro"
    assert translate_english_to_portuguese("good morning") == "bom dia"


def test_preserves_unknown_words_and_spacing() -> None:
    assert translate_english_to_portuguese("geobe   xyzzy") == "geobe   xyzzy"
