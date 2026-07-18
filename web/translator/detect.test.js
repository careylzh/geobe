import assert from "node:assert/strict";
import test from "node:test";
import { detectLanguageCode } from "./detect.js";

const packs = {};

test.before(async () => {
  packs.fr = await import("../packs/fr.js");
  packs["pt-BR"] = await import("../packs/pt.js");
  packs.vi = await import("../packs/vi.js");
});

test("detects Chinese from Han characters", () => {
  assert.equal(detectLanguageCode("你好", packs), "zh-Hans");
  assert.equal(detectLanguageCode("我很高兴见到你。", packs), "zh-Hans");
});

test("detects Vietnamese from its tone-marked letters", () => {
  assert.equal(detectLanguageCode("Tôi phải đi ngủ.", packs), "vi");
  assert.equal(detectLanguageCode("xin chào", packs), "vi");
});

test("detects French from dictionary words", () => {
  assert.equal(detectLanguageCode("Bonjour le monde", packs), "fr");
  assert.equal(detectLanguageCode("Je t'aime !", packs), "fr");
});

test("detects Portuguese from dictionary words", () => {
  assert.equal(detectLanguageCode("Onde fica o banheiro?", packs), "pt-BR");
  assert.equal(detectLanguageCode("olá mundo", packs), "pt-BR");
});

test("defaults to English for English and unknown input", () => {
  assert.equal(detectLanguageCode("hello world", packs), "en");
  assert.equal(detectLanguageCode("I love you.", packs), "en");
  assert.equal(detectLanguageCode("xqzzy 123", packs), "en");
});
