(function () {
  "use strict";

  const alphabet = {
    a: "▲", b: "△", c: "▴", d: "▵", e: "▶", f: "▷", g: "▸",
    h: "▹", i: "▼", j: "▽", k: "▾", l: "▿", m: "◀", n: "◁",
    o: "◂", p: "◃", q: "◢", r: "◣", s: "◤", t: "◥", u: "◬",
    v: "◭", w: "◮", x: "◸", y: "◹", z: "◺"
  };
  const reverseAlphabet = Object.fromEntries(
    Object.entries(alphabet).map(([letter, symbol]) => [symbol, letter])
  );

  function encode(value) {
    return Array.from(value, (character) => alphabet[character] || character).join("");
  }

  function decode(value) {
    return Array.from(value, (character) => reverseAlphabet[character] || character).join("");
  }

  function initializeConsole() {
    const input = document.querySelector("[data-geobe-input]");
    const encoded = document.querySelector("[data-geobe-encoded]");
    const decoded = document.querySelector("[data-geobe-decoded]");
    const form = document.querySelector("[data-geobe-console]");

    if (!input || !encoded || !decoded || !form || form.dataset.ready === "true") {
      return;
    }

    form.dataset.ready = "true";

    function render() {
      encoded.textContent = encode(input.value);
      decoded.textContent = "";
      decoded.hidden = true;
    }

    input.addEventListener("input", render);
    input.addEventListener("keydown", function (event) {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        const visibleLine = encode(input.value);
        encoded.textContent = visibleLine;
        decoded.textContent = decode(visibleLine);
        decoded.hidden = false;
      }
    });
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      const visibleLine = encode(input.value);
      encoded.textContent = visibleLine;
      decoded.textContent = decode(visibleLine);
      decoded.hidden = false;
    });

    render();
    input.focus();
  }

  window.GeobeConsole = { encode, decode, initializeConsole };

  if (typeof document$ !== "undefined") {
    document$.subscribe(initializeConsole);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeConsole);
  } else {
    initializeConsole();
  }
})();
