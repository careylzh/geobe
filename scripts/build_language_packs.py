"""Generate offline web language packs for the Geobe translator page.

Builds ``web/packs/{fr,zh,vi,ptReverse}.js`` from openly licensed datasets:

- FreeDict TEI dictionaries (eng-fra, fra-eng, eng-zho, por-eng), GPL.
- OPUS Tatoeba Moses sentence pairs (en-fr, cmn-en, en-vi), CC BY 2.0 FR.
- kaikki.org Wiktextract Vietnamese extract, CC BY-SA 3.0 / GFDL.
- OpenCC TSCharacters/TSPhrases tables (build-time only), Apache 2.0.

Usage: python3 scripts/build_language_packs.py <data-dir>

The data directory must contain the extracted archives listed in
``THIRD_PARTY_NOTICES.md``. Generated modules are committed so the site
builds without network access.
"""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

TEI_NS = "{http://www.tei-c.org/ns/1.0}"
MAX_SENTENCE_CHARS = 72
MAX_FORWARD_WORDS = 5

REPO_ROOT = Path(__file__).resolve().parent.parent
PACKS_DIR = REPO_ROOT / "web" / "packs"


def is_dictionary_key(value: str, ascii_only: bool) -> bool:
    if not value or len(value) > 64:
        return False
    for char in value:
        if char in " -'’":
            continue
        if ascii_only and not ("a" <= char <= "z"):
            return False
        if not char.isalpha():
            return False
    return value[0].isalpha()


def normalize_key(value: str) -> str:
    return " ".join(value.lower().split())


def parse_tei_dictionary(path: Path, ascii_keys: bool) -> dict[str, list[str]]:
    """Map lowercased headwords to their ordered unique translations."""
    entries: dict[str, list[str]] = {}
    for _, element in ET.iterparse(path):
        if element.tag != f"{TEI_NS}entry":
            continue
        orth = element.find(f"{TEI_NS}form/{TEI_NS}orth")
        if orth is None or not (orth.text or "").strip():
            element.clear()
            continue
        key = normalize_key(orth.text)
        if not is_dictionary_key(key, ascii_only=ascii_keys):
            element.clear()
            continue
        translations = entries.setdefault(key, [])
        for cit in element.iter(f"{TEI_NS}cit"):
            if cit.get("type") != "trans":
                continue
            quote = cit.find(f"{TEI_NS}quote")
            text = (quote.text or "").strip() if quote is not None else ""
            if text and text not in translations:
                translations.append(text)
        if not translations:
            del entries[key]
        element.clear()
    return entries


def count_word_frequencies(path: Path) -> dict[str, int]:
    import re
    from collections import Counter

    counts: Counter[str] = Counter()
    token_re = re.compile(r"[^\W\d_]+", re.UNICODE)
    for line in path.read_text().splitlines():
        counts.update(token.lower() for token in token_re.findall(line))
    return counts


def phrase_frequency(phrase: str, frequencies: dict[str, int]) -> int:
    words = phrase.split()
    return min((frequencies.get(word, 0) for word in words), default=0)


def invert_dictionary(
    entries: dict[str, list[str]],
    max_key_words: int,
    key_filter=None,
    frequencies: dict[str, int] | None = None,
) -> dict[str, list[str]]:
    """Invert a dictionary, ranking primary translations and frequent headwords."""
    ranked: dict[str, list[tuple[int, int, int, str]]] = {}
    for order, (headword, translations) in enumerate(entries.items()):
        rarity = -phrase_frequency(headword, frequencies) if frequencies else 0
        for priority, translation in enumerate(translations):
            key = normalize_key(translation)
            if not key or len(key.split()) > max_key_words:
                continue
            if key_filter is not None and not key_filter(key):
                continue
            candidates = ranked.setdefault(key, [])
            if all(candidate[3] != headword for candidate in candidates):
                candidates.append((priority, rarity, order, headword))
    return {
        key: [headword for _, _, _, headword in sorted(candidates)]
        for key, candidates in ranked.items()
    }


def load_opencc_table(data_dir: Path) -> tuple[dict[str, str], dict[str, str], int]:
    chars: dict[str, str] = {}
    phrases: dict[str, str] = {}
    for name, table in (("TSCharacters.txt", chars), ("TSPhrases.txt", phrases)):
        for line in (data_dir / name).read_text().splitlines():
            if not line or line.startswith("#"):
                continue
            key, _, values = line.partition("\t")
            if key and values:
                table[key] = values.split()[0]
    max_phrase = max(len(key) for key in phrases)
    return chars, phrases, max_phrase


def make_simplifier(data_dir: Path):
    chars, phrases, max_phrase = load_opencc_table(data_dir)

    def simplify(text: str) -> str:
        result: list[str] = []
        index = 0
        while index < len(text):
            match = None
            for length in range(min(max_phrase, len(text) - index), 1, -1):
                candidate = text[index : index + length]
                if candidate in phrases:
                    match = phrases[candidate]
                    index += length
                    break
            if match is None:
                char = text[index]
                match = chars.get(char, char)
                index += 1
            result.append(match)
        return "".join(result)

    return simplify


def parse_tatoeba_pairs(directory: Path, source_ext: str, target_ext: str, stem: str):
    """Yield (english, target) pairs; ``source_ext`` names the English file."""
    source_lines = (directory / f"{stem}.{source_ext}").read_text().splitlines()
    target_lines = (directory / f"{stem}.{target_ext}").read_text().splitlines()
    for english, target in zip(source_lines, target_lines):
        yield english.strip(), target.strip()


def build_sentence_table(pairs, transform_target=None) -> dict[str, str]:
    table: dict[str, str] = {}
    for english, target in pairs:
        if not english or not target or len(english) > MAX_SENTENCE_CHARS:
            continue
        key = normalize_key(english)
        if not key or key in table:
            continue
        table[key] = transform_target(target) if transform_target else target
    return table


def clean_gloss(gloss: str) -> str:
    while "(" in gloss and ")" in gloss:
        start = gloss.index("(")
        end = gloss.index(")", start)
        gloss = gloss[:start] + gloss[end + 1 :]
    return " ".join(gloss.replace("’", "'").split()).strip(" .,;:")


def parse_kaikki_vietnamese(path: Path):
    """Map Vietnamese words to short English glosses."""
    vi_to_en: dict[str, list[str]] = {}
    with path.open() as handle:
        for line in handle:
            record = json.loads(line)
            if record.get("lang_code") != "vi" or record.get("pos") == "character":
                continue
            word = normalize_key(record.get("word", ""))
            if not is_dictionary_key(word, ascii_only=False):
                continue
            for sense in record.get("senses", []):
                for gloss in sense.get("glosses", []):
                    for piece in clean_gloss(gloss).split(";"):
                        piece = piece.strip(" .,;:").lower()
                        if piece.startswith("to "):
                            piece = piece[3:]
                        if not piece or len(piece.split()) > 4:
                            continue
                        if not is_dictionary_key(piece, ascii_only=True):
                            continue
                        values = vi_to_en.setdefault(word, [])
                        if piece not in values:
                            values.append(piece)
    return vi_to_en


def js_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def write_pack(
    path: Path,
    header: str,
    meta: dict,
    forward_dictionary: dict[str, list[str]],
    reverse_dictionary: dict[str, list[str]],
    forward_sentences: dict[str, str],
) -> None:
    def dictionary_lines(name: str, entries: dict[str, list[str]]) -> list[str]:
        lines = [f"export const {name} = {{"]
        for key in sorted(entries):
            values = ", ".join(js_string(value) for value in entries[key])
            lines.append(f"  {js_string(key)}: [{values}],")
        lines.append("};")
        return lines

    lines = [header, ""]
    lines.append(f"export const meta = {json.dumps(meta, ensure_ascii=False)};")
    lines.extend(dictionary_lines("forwardDictionary", forward_dictionary))
    lines.extend(dictionary_lines("reverseDictionary", reverse_dictionary))
    lines.append("export const forwardSentences = {")
    for key in sorted(forward_sentences):
        lines.append(f"  {js_string(key)}: {js_string(forward_sentences[key])},")
    lines.append("};")
    lines.append("")
    path.write_text("\n".join(lines))
    print(f"wrote {path.relative_to(REPO_ROOT)} ({path.stat().st_size / 1e6:.1f} MB)")


def max_words(entries: dict[str, list[str]]) -> int:
    return min(
        MAX_FORWARD_WORDS,
        max((len(key.split()) for key in entries), default=1),
    )


def cross_rank(
    entries: dict[str, list[str]], counterpart: dict[str, list[str]]
) -> dict[str, list[str]]:
    """Stable-sort translations so ones the counterpart dictionary confirms lead."""

    def score(headword: str, translation: str) -> int:
        counterparts = counterpart.get(normalize_key(translation), [])
        if counterparts[:1] == [headword]:
            return 0
        return 1 if headword in counterparts else 2

    return {
        headword: sorted(translations, key=lambda t: score(headword, t))
        for headword, translations in entries.items()
    }


def build_french(data_dir: Path) -> None:
    forward = parse_tei_dictionary(data_dir / "eng-fra" / "eng-fra.tei", ascii_keys=True)
    reverse = parse_tei_dictionary(data_dir / "fra-eng" / "fra-eng.tei", ascii_keys=False)
    forward, reverse = cross_rank(forward, reverse), cross_rank(reverse, forward)
    sentences = build_sentence_table(
        parse_tatoeba_pairs(data_dir / "tatoeba-en-fr", "en", "fr", "Tatoeba.en-fr")
    )
    write_pack(
        PACKS_DIR / "fr.js",
        "// Generated by scripts/build_language_packs.py. Do not edit by hand.\n"
        "// Sources: FreeDict eng-fra 0.1.6 + fra-eng 0.4.1 (GPL);\n"
        "// OPUS Tatoeba en-fr v2023-04-12 (CC BY 2.0 FR). See THIRD_PARTY_NOTICES.md.",
        {
            "code": "fr",
            "forwardMaxWords": max_words(forward),
            "reverseMaxWords": max_words(reverse),
        },
        forward,
        reverse,
        sentences,
    )


def build_chinese(data_dir: Path) -> None:
    simplify = make_simplifier(data_dir)
    raw = parse_tei_dictionary(data_dir / "eng-zho" / "eng-zho.tei", ascii_keys=True)
    forward: dict[str, list[str]] = {}
    variants: dict[str, list[str]] = {}
    for headword, translations in raw.items():
        simplified: list[str] = []
        both_scripts: list[str] = []
        for translation in translations:
            converted = simplify(translation)
            if converted not in simplified:
                simplified.append(converted)
            for variant in (converted, translation):
                if variant not in both_scripts:
                    both_scripts.append(variant)
        forward[headword] = simplified
        variants[headword] = both_scripts
    reverse = invert_dictionary(
        variants,
        max_key_words=MAX_FORWARD_WORDS,
        frequencies=count_word_frequencies(
            data_dir / "tatoeba-cmn-en" / "Tatoeba.cmn-en.en"
        ),
    )
    sentences = build_sentence_table(
        parse_tatoeba_pairs(data_dir / "tatoeba-cmn-en", "en", "cmn", "Tatoeba.cmn-en"),
        transform_target=simplify,
    )
    write_pack(
        PACKS_DIR / "zh.js",
        "// Generated by scripts/build_language_packs.py. Do not edit by hand.\n"
        "// Sources: FreeDict eng-zho 2025.11.23 (GPL); OPUS Tatoeba cmn-en\n"
        "// v2023-04-12 (CC BY 2.0 FR); OpenCC conversion tables (Apache 2.0,\n"
        "// build-time only). See THIRD_PARTY_NOTICES.md.",
        {
            "code": "zh-Hans",
            "forwardMaxWords": max_words(forward),
            "reverseMaxChars": max((len(key) for key in reverse), default=1),
            "targetIsHan": True,
        },
        forward,
        reverse,
        sentences,
    )


def build_vietnamese(data_dir: Path) -> None:
    reverse = parse_kaikki_vietnamese(data_dir / "kaikki-vietnamese.jsonl")
    forward = invert_dictionary(
        reverse,
        max_key_words=MAX_FORWARD_WORDS,
        key_filter=lambda key: is_dictionary_key(key, ascii_only=True),
        frequencies=count_word_frequencies(
            data_dir / "tatoeba-en-vi" / "Tatoeba.en-vi.vi"
        ),
    )
    sentences = build_sentence_table(
        parse_tatoeba_pairs(data_dir / "tatoeba-en-vi", "en", "vi", "Tatoeba.en-vi")
    )
    write_pack(
        PACKS_DIR / "vi.js",
        "// Generated by scripts/build_language_packs.py. Do not edit by hand.\n"
        "// Sources: kaikki.org Wiktextract Vietnamese extract (CC BY-SA 3.0 /\n"
        "// GFDL); OPUS Tatoeba en-vi v2023-04-12 (CC BY 2.0 FR).\n"
        "// See THIRD_PARTY_NOTICES.md.",
        {
            "code": "vi",
            "forwardMaxWords": max_words(forward),
            "reverseMaxWords": max_words(reverse),
        },
        forward,
        reverse,
        sentences,
    )


def build_portuguese_reverse(data_dir: Path) -> None:
    reverse = parse_tei_dictionary(data_dir / "por-eng" / "por-eng.tei", ascii_keys=False)
    lines = [
        "// Generated by scripts/build_language_packs.py. Do not edit by hand.",
        "// Source: FreeDict por-eng 0.2 (GPL). See THIRD_PARTY_NOTICES.md.",
        "",
        f"export const reverseMaxWords = {max_words(reverse)};",
        "export const portugueseEnglish = {",
    ]
    for key in sorted(reverse):
        values = ", ".join(js_string(value) for value in reverse[key])
        lines.append(f"  {js_string(key)}: [{values}],")
    lines.extend(["};", ""])
    path = PACKS_DIR / "ptReverseDictionary.js"
    path.write_text("\n".join(lines))
    print(f"wrote {path.relative_to(REPO_ROOT)} ({path.stat().st_size / 1e6:.1f} MB)")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    data_dir = Path(sys.argv[1])
    PACKS_DIR.mkdir(parents=True, exist_ok=True)
    build_french(data_dir)
    build_chinese(data_dir)
    build_vietnamese(data_dir)
    build_portuguese_reverse(data_dir)


if __name__ == "__main__":
    main()
