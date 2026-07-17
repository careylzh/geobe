import { useRef, useState } from "react";
import { decode, encode } from "../alphabet.js";
import TriangleField from "../TriangleField.jsx";
import { createTranslator } from "./engine.js";
import { getLanguage, languages } from "./languages.js";

const translatorCache = new Map();

function loadTranslator(code) {
  if (!translatorCache.has(code)) {
    translatorCache.set(
      code,
      getLanguage(code).load().then((pack) => createTranslator(pack)),
    );
  }
  return translatorCache.get(code);
}

export default function TranslatorApp() {
  const [input, setInput] = useState("");
  const [languageCode, setLanguageCode] = useState("zh-Hans");
  const [toEnglish, setToEnglish] = useState(false);
  const [result, setResult] = useState(null);
  const [isLoadingPack, setIsLoadingPack] = useState(false);
  const submitId = useRef(0);

  const language = getLanguage(languageCode);
  const encoded = encode(input);

  async function submit(code = languageCode, reversed = toEnglish, value = input) {
    const text = decode(encode(value)).trim();
    if (!text) {
      setResult(null);
      return;
    }
    const id = ++submitId.current;
    if (code === "en") {
      setResult({ english: text, target: text });
      return;
    }

    setIsLoadingPack(!translatorCache.has(code));
    const translator = await loadTranslator(code);
    if (id !== submitId.current) return;
    setIsLoadingPack(false);
    setResult(
      reversed
        ? { english: translator.reverse(text), target: text }
        : { english: text, target: translator.forward(text) },
    );
  }

  function chooseLanguage(code) {
    setLanguageCode(code);
    if (result) void submit(code);
  }

  function toggleDirection() {
    const reversed = !toEnglish;
    setToEnglish(reversed);
    if (result) void submit(languageCode, reversed);
  }

  const sourceLabel = toEnglish ? language.nativeName : "English";
  const placeholder = toEnglish && language.code !== "en"
    ? `try ${language.sample}`
    : "try hello world";

  return (
    <main>
      <TriangleField />
      <nav className="topbar" aria-label="Primary navigation">
        <a className="brand" href="/geobe/" aria-label="Geobe home">
          <span className="brand-mark">△</span>
          <span>geobe</span>
        </a>
        <div className="nav-links">
          <a href="/geobe/">Home</a>
          <a href="/geobe/docs/">Documentation</a>
          <a className="github-link" href="https://github.com/careylzh/geobe">GitHub ↗</a>
        </div>
      </nav>

      <div className="translator-page">
        <header className="translator-heading">
          <p className="eyebrow hero-kicker"><span /> Offline multilingual console</p>
          <h1>The Geobe translator.</h1>
          <p className="hero-copy">
            Type in {toEnglish ? language.label : "English"}, watch it become
            triangles, then translate it — every language pack is bundled, so
            nothing leaves your browser.
          </p>
        </header>

        <section className="console-card translator-card" aria-labelledby="translator-title">
          <div className="console-heading">
            <div>
              <p className="eyebrow">Interactive translator</p>
              <h2 id="translator-title">
                {toEnglish ? `${language.label} → English` : `English → ${language.label}`}
              </h2>
            </div>
            <div className="window-controls" aria-hidden="true"><i /><i /><i /></div>
          </div>

          <label className="input-label" htmlFor="translator-input">
            Your message · {sourceLabel}
          </label>
          <div className="input-shell">
            <textarea
              autoCapitalize="off"
              autoComplete="off"
              autoFocus
              id="translator-input"
              onChange={(event) => {
                setInput(event.target.value);
                setResult(null);
              }}
              onKeyDown={(event) => {
                if (event.key === "Enter" && !event.shiftKey) {
                  event.preventDefault();
                  void submit();
                }
              }}
              placeholder={placeholder}
              rows="2"
              spellCheck="false"
              value={input}
            />
            <span className="key-hint">↵ translate</span>
          </div>

          <div className="geometry-output" aria-live="polite">
            <span className="terminal-mark">›</span>
            <output data-testid="encoded-output">{encoded || "▹ ▶ ◂ △ ▶"}</output>
            <span className="beam" />
          </div>

          <div className="translator-toolbar">
            <label className="toolbar-label" htmlFor="translator-language">
              Translate {toEnglish ? "from" : "to"}
            </label>
            <select
              id="translator-language"
              onChange={(event) => chooseLanguage(event.target.value)}
              value={languageCode}
            >
              {languages.map((option) => (
                <option key={option.code} value={option.code}>
                  {option.label}
                </option>
              ))}
            </select>
            <button
              aria-label="Swap translation direction"
              className="swap-button"
              onClick={toggleDirection}
              type="button"
            >
              ⇄ swap
            </button>
          </div>

          <div
            aria-live="polite"
            className={`split-panels ${result || isLoadingPack ? "is-visible" : ""}`}
          >
            <section className={`panel ${toEnglish ? "" : "is-source"}`}>
              <header>
                <span>English</span>
                <span className="panel-role">{toEnglish ? "translation" : "source"}</span>
              </header>
              <output data-testid="english-output">
                {isLoadingPack ? "…" : result?.english}
              </output>
            </section>
            <section className={`panel ${toEnglish ? "is-source" : ""}`}>
              <header>
                <span>{language.code === "en" ? "English" : language.nativeName}</span>
                <span className="panel-role">{toEnglish ? "source" : "translation"}</span>
              </header>
              <output data-testid="target-output">
                {isLoadingPack ? "loading offline pack…" : result?.target}
              </output>
            </section>
          </div>

          <button className="encode-button" onClick={() => void submit()} type="button">
            Translate <span aria-hidden="true">→</span>
          </button>
        </section>

        <p className="translator-footnote">
          Dictionaries and phrase tables from FreeDict, OPUS Tatoeba, and
          Wiktionary ship with the page — no translation API is called.
        </p>
      </div>

      <footer>
        <span>Experimental by design.</span>
        <span>Open source · MIT</span>
      </footer>
    </main>
  );
}
