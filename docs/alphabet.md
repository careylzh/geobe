# Triangle alphabet

The Geobe alphabet maps each lowercase ASCII letter to a distinct triangle
symbol. Other characters pass through unchanged.

## Interactive console

Start the terminal experience:

```console
geobe --console
```

As you type, lowercase letters are rendered as geometry. Press Enter to decode
the visible line. Backspace edits the latest character; Ctrl-C or Ctrl-D exits.

Use Portuguese output instead of English with:

```console
geobe --console --console-output-language portuguese
```

Portuguese output uses bundled FreeDict dictionary data and exact Tatoeba
sentence-pair matches, so it works without a remote translation API.

## Mapping

| Letter | Geometry | Letter | Geometry |
| --- | --- | --- | --- |
| a | ▲ | n | ◁ |
| b | △ | o | ◂ |
| c | ▴ | p | ◃ |
| d | ▵ | q | ◢ |
| e | ▶ | r | ◣ |
| f | ▷ | s | ◤ |
| g | ▸ | t | ◥ |
| h | ▹ | u | ◬ |
| i | ▼ | v | ◭ |
| j | ▽ | w | ◮ |
| k | ▾ | x | ◸ |
| l | ▿ | y | ◹ |
| m | ◀ | z | ◺ |

## Spell directive

The `spell` parser directive decodes symbols into a literal output program:

```geo
spell ▹▶▿▿◂ ◮◂ ◣▿▵!
```

This produces `hello world!`.

## Python API

The codec is also available from Python:

```python
from geobe.parser import decode_spell_text, encode_spell_text

symbols = encode_spell_text("hello")
text = decode_spell_text(symbols)
```
