import assert from "node:assert/strict";
import test from "node:test";
import { decode, encode } from "./alphabet.js";

test("encodes lowercase ASCII and preserves other characters", () => {
  assert.equal(encode("hello, Geobe!"), "▹▶▿▿◂, G▶◂△▶!");
});

test("decodes triangle symbols to lowercase ASCII", () => {
  assert.equal(decode("▹▶▿▿◂ ◮◂◣▿▵!"), "hello world!");
});
