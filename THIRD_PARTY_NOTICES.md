# Third-Party Notices

## Translator Page Language Packs

The web translator page (`web/packs/`) bundles generated lookup tables
built by `scripts/build_language_packs.py` from the datasets below. All
lookups run in the browser; no translation API is called.

### FreeDict Dictionaries (French, Chinese, Portuguese reverse)

- `eng-fra` 0.1.6 and `fra-eng` 0.4.1 — GNU GPL v2.0 or later.
- `por-eng` 0.2 — GNU GPL v2.0 or later.
- `eng-zho` 2025.11.23 — Creative Commons Attribution-ShareAlike 3.0
  Unported (Wiktionary-derived).

Source archives:
https://download.freedict.org/dictionaries/{eng-fra/0.1.6,fra-eng/0.4.1,por-eng/0.2,eng-zho/2025.11.23}/

License texts copied from the source archives are included under
`third_party/freedict-{eng-fra,fra-eng,por-eng,eng-zho}/COPYING`.

Generated files: `web/packs/fr.js` (dictionary layers),
`web/packs/zh.js` (dictionary layers), `web/packs/ptReverseDictionary.js`.

### OPUS Tatoeba Sentence Pairs (French, Chinese, Vietnamese)

Generated exact-match phrase tables derived from the OPUS Tatoeba
Moses-format datasets `Tatoeba.en-fr`, `Tatoeba.cmn-en`, and
`Tatoeba.en-vi`, release `v2023-04-12`, licensed CC BY 2.0 FR.

Source archives:
https://object.pouta.csc.fi/OPUS-Tatoeba/v2023-04-12/moses/{en-fr,cmn-en,en-vi}.txt.zip

The license and README copied from the source archives are included
under `third_party/tatoeba-{en-fr,cmn-en,en-vi}/`.

Generated files: sentence layers of `web/packs/{fr,zh,vi}.js`.

### Wiktextract Vietnamese Extract (kaikki.org)

The Vietnamese word dictionary layer is derived from the kaikki.org
machine-readable Wiktextract extract of Wiktionary's Vietnamese
entries, available under the Creative Commons Attribution-ShareAlike
3.0 Unported license and the GNU Free Documentation License.

Source: https://kaikki.org/dictionary/Vietnamese/

Generated file: dictionary layers of `web/packs/vi.js`.

### OpenCC Conversion Tables (build time only)

`scripts/build_language_packs.py` uses the OpenCC `TSCharacters.txt`
and `TSPhrases.txt` tables (Apache License 2.0) to normalize Chinese
output to Simplified script. The tables are not shipped in the web
bundle. The license is included at `third_party/opencc/LICENSE`.

Source: https://github.com/BYVoid/OpenCC

## FreeDict English-Portuguese Dictionary

Geobe includes generated lookup tables derived from the FreeDict
English-Portuguese dictionary (`eng-por`) version 0.3, published by the
FreeDict Project with 15,766 headwords.

Source archive:
https://download.freedict.org/dictionaries/eng-por/0.3/freedict-eng-por-0.3.src.tar.xz

FreeDict describes its dictionaries as free to use, modify, and
redistribute when the licensing terms are met. The `eng-por` TEI header
states that the dictionary is available under the GNU General Public
License version 2.0 or later.

The generated files are:

- `src/geobe/eng_por_dictionary.py`
- `web/engPorDictionary.js`

The GPL license text copied from the source archive is included at
`third_party/freedict-eng-por/COPYING` and packaged at
`src/geobe/data/freedict-eng-por-COPYING.txt`.

## OPUS Tatoeba English-Portuguese Sentence Pairs

Geobe includes a generated exact-match phrase table derived from the OPUS
Tatoeba English-Portuguese Moses-format dataset (`Tatoeba.en-pt`) release
`v2023-04-12`. The generated table keeps all 169,190 unique short English
sentence pairs that pass Geobe's lightweight offline lookup filters.

Source archive:
https://object.pouta.csc.fi/OPUS-Tatoeba/v2023-04-12/moses/en-pt.txt.zip

OPUS lists the Tatoeba corpus license as CC BY 2.0 FR and identifies the
corpus as translated sentences from Tatoeba.

The generated files are:

- `src/geobe/tatoeba_phrases.py`
- `web/tatoebaPhrases.js`

The license and README copied from the source archive are included under
`third_party/tatoeba-en-pt/`. The license text is also packaged at
`src/geobe/data/tatoeba-en-pt-LICENSE.txt`.
