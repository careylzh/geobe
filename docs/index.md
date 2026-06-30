---
title: Geobe
---

# Geobe

Geobe is an experimental geometric esolang toolkit. Its most complete experience
is the interactive triangle console below. The project also contains a small 2D
Unicode-symbol interpreter, but it is not yet a general-purpose programming
language.

## Try `geobe --console`

Type lowercase ASCII letters. Their geometric encodings appear immediately;
press Enter to decode the visible line back to English.

<form class="geobe-console" data-geobe-console>
  <label for="geobe-input">Input</label>
  <textarea id="geobe-input" data-geobe-input rows="3" spellcheck="false" autocomplete="off" autocapitalize="off" placeholder="type hello and press Enter"></textarea>
  <div class="geobe-terminal" role="log" aria-live="polite">
    <div><span class="geobe-prompt" aria-hidden="true">›</span> <output data-geobe-encoded></output><span class="geobe-cursor" aria-hidden="true"></span></div>
    <div data-geobe-decoded hidden></div>
  </div>
  <button type="submit">Decode</button>
</form>

Backspace edits the input normally. Uppercase letters, numbers, spaces, and
punctuation pass through unchanged. Shift-Enter inserts a newline.

## Triangle Alphabet

The `spell` directive decodes Geobe's geometric alphabet symbols into lowercase
English letters. Parser expansion turns a `spell ...` line into a literal
string output program.

| Letter | Geometry |
| --- | --- |
| a | ▲ |
| b | △ |
| c | ▴ |
| d | ▵ |
| e | ▶ |
| f | ▷ |
| g | ▸ |
| h | ▹ |
| i | ▼ |
| j | ▽ |
| k | ▾ |
| l | ▿ |
| m | ◀ |
| n | ◁ |
| o | ◂ |
| p | ◃ |
| q | ◢ |
| r | ◣ |
| s | ◤ |
| t | ◥ |
| u | ◬ |
| v | ◭ |
| w | ◮ |
| x | ◸ |
| y | ◹ |
| z | ◺ |

Example:

```geo
spell ▹▶▿▿◂ ◮◂ ◣▿▵!
```

Decodes to:

```text
hello world!
```

The same mapping powers the terminal command:

```console
geobe --console
```
