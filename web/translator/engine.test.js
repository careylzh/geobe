import assert from "node:assert/strict";
import test from "node:test";
import { createTranslator } from "./engine.js";

test("French pack translates sentences and words in both directions", async () => {
  const translator = createTranslator(await import("../packs/fr.js"));

  assert.equal(translator.forward("I love you."), "Je t'aime !");
  assert.match(translator.forward("the water"), /eau/);
  assert.match(translator.reverse("Je t'aime !"), /love you/i);
  assert.match(translator.reverse("bonjour"), /good (morning|day)/i);
});

test("Chinese pack outputs Simplified and reads Han input", async () => {
  const translator = createTranslator(await import("../packs/zh.js"));

  assert.equal(translator.forward("I love you."), "我爱你。");
  assert.match(translator.forward("water"), /水/);
  assert.match(translator.reverse("我爱你。"), /I love you/i);
  assert.match(translator.reverse("谢谢"), /thank/i);
});

test("Chinese word fallback joins Han output without spaces", async () => {
  const translator = createTranslator(await import("../packs/zh.js"));
  const output = translator.forward("red water");

  assert.ok(!/\p{Script=Han} \p{Script=Han}/u.test(output), output);
  assert.match(output, /水/);
});

test("Vietnamese pack translates sentences and words in both directions", async () => {
  const translator = createTranslator(await import("../packs/vi.js"));

  assert.equal(translator.forward("I have to go to sleep."), "Tôi phải đi ngủ.");
  assert.match(translator.forward("water"), /nước/);
  assert.match(translator.reverse("Tôi phải đi ngủ."), /sleep/i);
  assert.match(translator.reverse("nước"), /water/i);
});

test("Portuguese pack reuses bundled tables and supports reverse mode", async () => {
  const translator = createTranslator(await import("../packs/pt.js"));

  assert.equal(translator.forward("Where is the bathroom?"), "Onde fica o banheiro?");
  assert.match(translator.reverse("Onde fica o banheiro?"), /bathroom/i);
  assert.match(translator.reverse("obrigado"), /thank/i);
});

test("reverse translation does not double terminal punctuation", async () => {
  const zh = createTranslator(await import("../packs/zh.js"));
  const fr = createTranslator(await import("../packs/fr.js"));

  assert.doesNotMatch(zh.reverse("我很高兴见到你。"), /[.!?]。$|。$/u);
  assert.doesNotMatch(fr.reverse("Je t'aime !"), /[.!?][.!?]$/);
});

test("unknown words pass through unchanged", async () => {
  const translator = createTranslator(await import("../packs/fr.js"));

  assert.match(translator.forward("xqzzy water"), /^xqzzy /);
});
