# Third-Party Notices

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
`v2023-04-12`. The generated table keeps the first 50,000 unique short
English sentence pairs suitable for a lightweight browser bundle.

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
