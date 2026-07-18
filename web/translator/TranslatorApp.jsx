import { useEffect, useRef, useState } from "react";
import { decode, encode } from "../alphabet.js";
import TriangleField from "../TriangleField.jsx";
import { detectLanguageCode } from "./detect.js";
import { createTranslator } from "./engine.js";
import { getLanguage, languages } from "./languages.js";

const packCache = new Map();
const translatorCache = new Map();
const historyKey = "geobe-translator-history-v1";
const historyLimit = 200;

function loadPack(code) {
  if (!packCache.has(code)) {
    packCache.set(code, getLanguage(code).load());
  }
  return packCache.get(code);
}

function loadTranslator(code) {
  if (!translatorCache.has(code)) {
    translatorCache.set(code, loadPack(code).then((pack) => createTranslator(pack)));
  }
  return translatorCache.get(code);
}

// Reverse output from Han packs keeps CJK punctuation, which would miss the
// Latin sentence tables on the second hop of a pivot translation.
function normalizePivotEnglish(text) {
  const latin = text.replace(
    /[。！？，]/gu,
    (mark) => ({ "。": ".", "！": "!", "？": "?", "，": "," })[mark],
  );
  return latin.charAt(0).toUpperCase() + latin.slice(1);
}

async function detectInputLanguage(text) {
  const [fr, pt, vi] = await Promise.all([
    loadPack("fr"),
    loadPack("pt-BR"),
    loadPack("vi"),
  ]);
  return detectLanguageCode(text, { fr, "pt-BR": pt, vi });
}

function loadHistory() {
  try {
    const stored = JSON.parse(localStorage.getItem(historyKey) ?? "[]");
    return Array.isArray(stored) ? stored.filter((entry) => !entry.pending) : [];
  } catch {
    return [];
  }
}

function messageTime() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

export default function TranslatorApp() {
  const [input, setInput] = useState("");
  const [languageCode, setLanguageCode] = useState("zh-Hans");
  const [toEnglish, setToEnglish] = useState(false);
  const [autoDetect, setAutoDetect] = useState(false);
  const [messages, setMessages] = useState(loadHistory);
  const nextId = useRef(Date.now());
  const scrollRef = useRef(null);

  const language = getLanguage(languageCode);
  const encoded = encode(input);
  const sourceLabel = autoDetect
    ? "any supported language"
    : toEnglish
      ? language.nativeName
      : "English";
  const targetLabel = !autoDetect && toEnglish ? "English" : language.nativeName;

  useEffect(() => {
    localStorage.setItem(historyKey, JSON.stringify(messages.slice(-historyLimit)));
  }, [messages]);

  useEffect(() => {
    const list = scrollRef.current;
    if (list) list.scrollTop = list.scrollHeight;
  }, [messages]);

  async function translateDetected(text) {
    const detected = await detectInputLanguage(text);
    if (detected === languageCode) return { detected, translated: text };

    let english = text;
    if (detected !== "en") {
      const source = await loadTranslator(detected);
      english = normalizePivotEnglish(source.reverse(text));
    }
    if (languageCode === "en") return { detected, translated: english };
    const target = await loadTranslator(languageCode);
    return { detected, translated: target.forward(english) };
  }

  async function submit() {
    const text = decode(encode(input)).trim();
    if (!text) return;

    const id = ++nextId.current;
    const outgoing = {
      id,
      kind: "outgoing",
      text,
      encoded: encode(text),
      label: autoDetect ? "detecting…" : languageCode === "en" ? "English" : sourceLabel,
      time: messageTime(),
    };
    const incoming = {
      id: id + 0.5,
      kind: "incoming",
      text: "",
      label: languageCode === "en" ? "English" : targetLabel,
      time: messageTime(),
      pending: true,
    };
    setInput("");
    setMessages((previous) => [...previous, outgoing, incoming].slice(-historyLimit));

    let translated = text;
    let sourceName = outgoing.label;
    if (autoDetect) {
      const result = await translateDetected(text);
      translated = result.translated;
      sourceName = getLanguage(result.detected).nativeName;
    } else if (languageCode !== "en") {
      const translator = await loadTranslator(languageCode);
      translated = toEnglish ? translator.reverse(text) : translator.forward(text);
    }
    setMessages((previous) =>
      previous.map((message) => {
        if (message.id === incoming.id) {
          return { ...message, text: translated, pending: false, time: messageTime() };
        }
        if (message.id === id && message.label !== sourceName) {
          return { ...message, label: sourceName };
        }
        return message;
      }),
    );
  }

  return (
    <main className="translator-main">
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
        <section className="chat-card" aria-label="Geobe translator chat">
          <header className="chat-header">
            <div className="chat-title">
              <p className="eyebrow">Offline translator</p>
              <h1>
                {autoDetect
                  ? `Auto-detect → ${language.label}`
                  : toEnglish
                    ? `${language.label} → English`
                    : `English → ${language.label}`}
              </h1>
            </div>
            <div className="chat-controls">
              <select
                aria-label="Language"
                id="translator-language"
                onChange={(event) => setLanguageCode(event.target.value)}
                value={languageCode}
              >
                {languages.map((option) => (
                  <option key={option.code} value={option.code}>
                    {option.label}
                  </option>
                ))}
              </select>
              <button
                aria-label="Detect the input language automatically"
                aria-pressed={autoDetect}
                className={`swap-button ${autoDetect ? "is-active" : ""}`}
                onClick={() => setAutoDetect((value) => !value)}
                type="button"
              >
                ✦ auto
              </button>
              {!autoDetect && (
                <button
                  aria-label="Swap translation direction"
                  className="swap-button"
                  onClick={() => setToEnglish((value) => !value)}
                  type="button"
                >
                  ⇄ swap
                </button>
              )}
              <button
                aria-label="Clear chat history"
                className="clear-button"
                disabled={messages.length === 0}
                onClick={() => setMessages([])}
                type="button"
              >
                clear
              </button>
            </div>
          </header>

          <div aria-live="polite" className="chat-scroll" ref={scrollRef}>
            {messages.length === 0 && (
              <div className="chat-empty">
                <span aria-hidden="true">▹ ▶ ◂ △ ▶</span>
                <p>
                  Send a message in {sourceLabel} — it stacks up here with its
                  triangle encoding and {targetLabel} translation.
                  {autoDetect && " The input language is detected for you."}{" "}
                  Everything stays in your browser.
                </p>
              </div>
            )}
            {messages.map((message) => (
              <article
                className={`bubble ${message.kind} ${message.pending ? "is-pending" : ""}`}
                data-testid={`bubble-${message.kind}`}
                key={message.id}
              >
                <header>
                  <span>{message.label}</span>
                  <span className="bubble-time">{message.time}</span>
                </header>
                <p className="bubble-text">
                  {message.pending ? "translating…" : message.text}
                </p>
                {message.encoded && message.encoded !== message.text && (
                  <p aria-label="Geobe encoding" className="bubble-encoded">
                    {message.encoded}
                  </p>
                )}
              </article>
            ))}
          </div>

          <div className="composer">
            <div
              className={`composer-preview ${input ? "is-visible" : ""}`}
              aria-live="polite"
            >
              <span className="terminal-mark">›</span>
              <output data-testid="encoded-output">{encoded}</output>
            </div>
            <div className="composer-row">
              <textarea
                aria-label={`Message in ${sourceLabel}`}
                autoCapitalize="off"
                autoComplete="off"
                autoFocus
                id="translator-input"
                onChange={(event) => setInput(event.target.value)}
                onKeyDown={(event) => {
                  if (event.key === "Enter" && !event.shiftKey) {
                    event.preventDefault();
                    void submit();
                  }
                }}
                placeholder={
                  autoDetect
                    ? "type in any supported language"
                    : toEnglish && language.code !== "en"
                      ? `try ${language.sample}`
                      : "try hello world"
                }
                rows="1"
                spellCheck="false"
                value={input}
              />
              <button
                aria-label="Send"
                className="send-button"
                onClick={() => void submit()}
                type="button"
              >
                ➤
              </button>
            </div>
          </div>
        </section>

        <p className="translator-footnote">
          Dictionaries and phrase tables from FreeDict, OPUS Tatoeba, and
          Wiktionary ship with the page — no translation API is called, and
          your chat history never leaves this browser.
        </p>
      </div>
    </main>
  );
}
