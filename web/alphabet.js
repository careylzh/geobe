export const alphabet = {
  a: "▲", b: "△", c: "▴", d: "▵", e: "▶", f: "▷", g: "▸",
  h: "▹", i: "▼", j: "▽", k: "▾", l: "▿", m: "◀", n: "◁",
  o: "◂", p: "◃", q: "◢", r: "◣", s: "◤", t: "◥", u: "◬",
  v: "◭", w: "◮", x: "◸", y: "◹", z: "◺",
};

const reverseAlphabet = Object.fromEntries(
  Object.entries(alphabet).map(([letter, symbol]) => [symbol, letter]),
);

export function encode(value) {
  return Array.from(value, (character) => alphabet[character] || character).join("");
}

export function decode(value) {
  return Array.from(value, (character) => reverseAlphabet[character] || character).join("");
}
