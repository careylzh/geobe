import assert from "node:assert/strict";
import test from "node:test";
import { decode, encode } from "./alphabet.js";
import { translateEnglishToPortuguese } from "./translation.js";

test("encodes lowercase ASCII and preserves other characters", () => {
  assert.equal(encode("hello, Geobe!"), "▹▶▿▿◂, G▶◂△▶!");
});

test("decodes triangle symbols to lowercase ASCII", () => {
  assert.equal(decode("▹▶▿▿◂ ◮◂◣▿▵!"), "hello world!");
});

test("translates exact Tatoeba sentence pairs to Portuguese", () => {
  assert.equal(translateEnglishToPortuguese("How are you?"), "Como você está?");
  assert.equal(translateEnglishToPortuguese("Good morning!"), "Bom dia!");
});

test("falls back to FreeDict dictionary translation for unmatched text", () => {
  assert.equal(translateEnglishToPortuguese("the red book"), "a rubro livro");
});
