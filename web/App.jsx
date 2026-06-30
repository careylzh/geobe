import { useMemo, useRef, useState } from "react";
import { alphabet, decode, encode } from "./alphabet.js";

const triangleGlyphs = Object.values(alphabet);

function TriangleField() {
  const triangles = useMemo(
    () => Array.from({ length: 34 }, (_, index) => ({
      glyph: triangleGlyphs[(index * 7) % triangleGlyphs.length],
      left: `${(index * 29 + 7) % 101}%`,
      top: `${(index * 41 + 3) % 103}%`,
      size: `${18 + ((index * 13) % 48)}px`,
      duration: `${13 + ((index * 17) % 22)}s`,
      delay: `${-((index * 11) % 25)}s`,
      drift: `${-80 + ((index * 37) % 161)}px`,
      opacity: 0.05 + ((index * 3) % 9) / 100,
    })),
    [],
  );

  return (
    <div className="triangle-field" aria-hidden="true">
      {triangles.map((triangle, index) => (
        <span
          className="floating-triangle"
          key={`${triangle.glyph}-${index}`}
          style={{
            "--left": triangle.left,
            "--top": triangle.top,
            "--size": triangle.size,
            "--duration": triangle.duration,
            "--delay": triangle.delay,
            "--drift": triangle.drift,
            "--opacity": triangle.opacity,
          }}
        >
          {triangle.glyph}
        </span>
      ))}
    </div>
  );
}

function Console() {
  const [input, setInput] = useState("");
  const [submitted, setSubmitted] = useState("");
  const inputRef = useRef(null);
  const encoded = encode(input);

  function submit() {
    setSubmitted(decode(encoded));
  }

  return (
    <section className="console-card" aria-labelledby="console-title">
      <div className="console-heading">
        <div>
          <p className="eyebrow">Interactive alphabet</p>
          <h2 id="console-title">Type in English. See in geometry.</h2>
        </div>
        <div className="window-controls" aria-hidden="true"><i /><i /><i /></div>
      </div>

      <label className="input-label" htmlFor="geobe-input">Your message</label>
      <div className="input-shell">
        <textarea
          autoCapitalize="off"
          autoComplete="off"
          autoFocus
          id="geobe-input"
          onChange={(event) => {
            setInput(event.target.value);
            setSubmitted("");
          }}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              submit();
            }
          }}
          placeholder="try hello world"
          ref={inputRef}
          rows="2"
          spellCheck="false"
          value={input}
        />
        <span className="key-hint">↵ encode</span>
      </div>

      <div className="geometry-output" aria-live="polite">
        <span className="terminal-mark">›</span>
        <output data-testid="encoded-output">{encoded || "▹ ▶ ◂ △ ▶"}</output>
        <span className="beam" />
      </div>

      <div className={`decoded-row ${submitted ? "is-visible" : ""}`}>
        <span>Decoded</span>
        <output data-testid="decoded-output">{submitted}</output>
      </div>

      <button className="encode-button" onClick={submit} type="button">
        Decode geometry <span aria-hidden="true">→</span>
      </button>
    </section>
  );
}

export default function App() {
  return (
    <main>
      <TriangleField />
      <nav className="topbar" aria-label="Primary navigation">
        <a className="brand" href="/geobe/" aria-label="Geobe home">
          <span className="brand-mark">△</span>
          <span>geobe</span>
        </a>
        <div className="nav-links">
          <a href="/geobe/docs/">Documentation</a>
          <a className="github-link" href="https://github.com/careylzh/geobe">GitHub ↗</a>
        </div>
      </nav>

      <div className="page-grid">
        <section className="hero">
          <p className="eyebrow hero-kicker"><span /> A geometric language experiment</p>
          <h1>Language,<br /><em>reimagined</em><br />in shape.</h1>
          <p className="hero-copy">
            Geobe turns lowercase letters into a visual alphabet of triangles—an
            expressive bridge between text, geometry, and code.
          </p>
          <div className="hero-actions">
            <a className="primary-action" href="#playground">Try the console <span>↓</span></a>
            <a className="text-action" href="/geobe/docs/">Read the docs <span>→</span></a>
          </div>
          <div className="alphabet-ribbon" aria-label="A sample of the Geobe alphabet">
            {["▲", "△", "▴", "▵", "▶", "▷", "▸", "▹"].map((glyph, index) => (
              <span key={glyph} style={{ "--index": index }}>{glyph}</span>
            ))}
          </div>
        </section>

        <div id="playground"><Console /></div>
      </div>

      <footer>
        <span>Experimental by design.</span>
        <span>Open source · MIT</span>
      </footer>
    </main>
  );
}
