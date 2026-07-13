import assert from "node:assert/strict";
import test from "node:test";
import {
  englishPortuguese,
  maxTranslationWords,
} from "./engPorDictionary.js";
import { tatoebaEnglishPortuguese } from "./tatoebaPhrases.js";
import { translateEnglishToPortuguese } from "./translation.js";

test("bundles broad dictionary and exact sentence language-pack layers", () => {
  assert.ok(
    Object.keys(englishPortuguese).length >= 15_000,
    "expected the FreeDict layer to retain roughly the full eng-por dictionary",
  );
  assert.ok(
    Object.keys(tatoebaEnglishPortuguese).length >= 160_000,
    "expected the Tatoeba layer to retain all short sentence pairs",
  );
  assert.ok(maxTranslationWords >= 5);
});

test("dictionary layer covers the full English alphabet", () => {
  const coveredInitials = new Set(
    Object.keys(englishPortuguese).map((entry) => entry.at(0)),
  );

  for (const letter of "abcdefghijklmnopqrstuvwxyz") {
    assert.ok(coveredInitials.has(letter), `missing entries for ${letter}`);
  }
});

test("dictionary layer covers common learning verbs and adjectives", () => {
  const expectedWords = [
    "be",
    "have",
    "do",
    "go",
    "come",
    "make",
    "get",
    "see",
    "know",
    "think",
    "want",
    "need",
    "learn",
    "speak",
    "read",
    "write",
    "eat",
    "drink",
    "buy",
    "help",
    "good",
    "bad",
    "big",
    "small",
    "new",
    "old",
    "happy",
    "sad",
    "hot",
    "cold",
    "fast",
    "slow",
    "beautiful",
    "important",
    "different",
    "easy",
    "difficult",
    "right",
    "wrong",
  ];

  for (const word of expectedWords) {
    assert.ok(englishPortuguese[word]?.length > 0, `missing ${word}`);
  }
});

test("sentence layer covers representative language-learning prompts", () => {
  const expectedSentences = [
    "how are you?",
    "good morning!",
    "where is the bathroom?",
    "i love you.",
    "i need help.",
    "do you speak english?",
    "what is your name?",
    "thank you.",
    "see you tomorrow.",
    "i am hungry.",
    "i am thirsty.",
  ];

  for (const sentence of expectedSentences) {
    assert.ok(tatoebaEnglishPortuguese[sentence], `missing ${sentence}`);
  }
});

test("translator uses exact sentences before dictionary fallback", () => {
  assert.equal(translateEnglishToPortuguese("Where is the bathroom?"), (
    "Onde fica o banheiro?"
  ));
  assert.equal(translateEnglishToPortuguese("Do you speak English?"), (
    "Você fala inglês?"
  ));
  assert.equal(translateEnglishToPortuguese("read the important book"), (
    "ler a importante livro"
  ));
});
