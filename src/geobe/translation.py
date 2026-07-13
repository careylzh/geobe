"""English-to-Portuguese translation helpers backed by FreeDict data."""

from __future__ import annotations

import re

from geobe.eng_por_dictionary import ENGLISH_PORTUGUESE, MAX_TRANSLATION_WORDS
from geobe.tatoeba_phrases import TATOEBA_ENGLISH_PORTUGUESE

WORD_RE = re.compile(r"[A-Za-z]+(?:[-'][A-Za-z]+)*")


def translate_english_to_portuguese(text: str) -> str:
    """Translate English words and phrases to Portuguese dictionary equivalents."""
    phrase = _translate_exact_sentence(text)
    if phrase is not None:
        return phrase

    matches = list(WORD_RE.finditer(text))
    if not matches:
        return text

    translated: list[str] = []
    cursor = 0
    index = 0
    while index < len(matches):
        match = _find_longest_match(text, matches, index)
        if match is None:
            word = matches[index]
            translated.append(text[cursor : word.start()])
            translated.append(word.group(0))
            cursor = word.end()
            index += 1
            continue

        start, end, replacement, next_index = match
        translated.append(text[cursor:start])
        translated.append(_match_case(text[start:end], replacement))
        cursor = end
        index = next_index

    translated.append(text[cursor:])
    return "".join(translated)


def _translate_exact_sentence(text: str) -> str | None:
    translated = TATOEBA_ENGLISH_PORTUGUESE.get(_normalize_key(text))
    if translated is not None:
        return _match_case(text, translated)
    phrase, punctuation = _split_terminal_punctuation(text)
    translated = TATOEBA_ENGLISH_PORTUGUESE.get(_normalize_key(phrase))
    if translated is None:
        return None
    return _match_case(phrase, translated) + punctuation


def _find_longest_match(
    text: str,
    matches: list[re.Match[str]],
    start_index: int,
) -> tuple[int, int, str, int] | None:
    limit = min(len(matches), start_index + MAX_TRANSLATION_WORDS)
    for end_index in range(limit, start_index, -1):
        start = matches[start_index].start()
        end = matches[end_index - 1].end()
        candidate = text[start:end]
        if not _contains_only_word_separators(candidate):
            continue

        translations = ENGLISH_PORTUGUESE.get(_normalize_key(candidate))
        if translations:
            return start, end, translations[0], end_index
    return None


def _contains_only_word_separators(value: str) -> bool:
    return re.fullmatch(r"[A-Za-z]+(?:[-' ]+[A-Za-z]+)*", value) is not None


def _normalize_key(value: str) -> str:
    return re.sub(r"\s+", " ", value.lower()).strip()


def _split_terminal_punctuation(text: str) -> tuple[str, str]:
    match = re.search(r"([.!?]+)$", text.strip())
    if match is None:
        return text, ""
    return text[: match.start()], match.group(1)


def _match_case(source: str, translated: str) -> str:
    words = WORD_RE.findall(source)
    if words and all(word.isupper() for word in words):
        return translated.upper()
    if source[:1].isupper():
        return translated[:1].upper() + translated[1:]
    return translated
