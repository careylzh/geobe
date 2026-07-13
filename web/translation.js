import {
  englishPortuguese,
  maxTranslationWords,
} from "./engPorDictionary.js";
import { tatoebaEnglishPortuguese } from "./tatoebaPhrases.js";

const wordPattern = /[A-Za-z]+(?:[-'][A-Za-z]+)*/gu;

export function translateEnglishToPortuguese(value) {
  const exact = translateExactSentence(value);
  if (exact !== "") return exact;

  const matches = Array.from(value.matchAll(wordPattern));
  if (matches.length === 0) return value;

  const translated = [];
  let cursor = 0;
  let index = 0;
  while (index < matches.length) {
    const match = findLongestMatch(value, matches, index);
    if (!match) {
      const word = matches[index];
      translated.push(value.slice(cursor, word.index));
      translated.push(word[0]);
      cursor = word.index + word[0].length;
      index += 1;
      continue;
    }

    translated.push(value.slice(cursor, match.start));
    translated.push(matchCase(value.slice(match.start, match.end), match.replacement));
    cursor = match.end;
    index = match.nextIndex;
  }

  translated.push(value.slice(cursor));
  return translated.join("");
}

function translateExactSentence(value) {
  const translated = tatoebaEnglishPortuguese[normalizeKey(value)];
  if (translated) return matchCase(value, translated);

  const [, phrase = value, punctuation = ""] = value.trim().match(/^(.*?)([.!?]+)?$/u);
  const withoutPunctuation = tatoebaEnglishPortuguese[normalizeKey(phrase)];
  return withoutPunctuation ? matchCase(phrase, withoutPunctuation) + punctuation : "";
}

function findLongestMatch(value, matches, startIndex) {
  const limit = Math.min(matches.length, startIndex + maxTranslationWords);
  for (let endIndex = limit; endIndex > startIndex; endIndex -= 1) {
    const start = matches[startIndex].index;
    const last = matches[endIndex - 1];
    const end = last.index + last[0].length;
    const candidate = value.slice(start, end);
    if (!containsOnlyWordSeparators(candidate)) continue;

    const translations = englishPortuguese[normalizeKey(candidate)];
    if (translations?.length) {
      return { start, end, replacement: translations[0], nextIndex: endIndex };
    }
  }
  return null;
}

function containsOnlyWordSeparators(value) {
  return /^[A-Za-z]+(?:[-' ]+[A-Za-z]+)*$/u.test(value);
}

function normalizeKey(value) {
  return value.toLowerCase().replace(/\s+/gu, " ").trim();
}

function matchCase(source, translated) {
  const words = Array.from(source.matchAll(wordPattern), (match) => match[0]);
  if (words.length > 0 && words.every((word) => word.toUpperCase() === word)) {
    return translated.toUpperCase();
  }
  if (/^[A-Z]/u.test(source)) {
    return translated.charAt(0).toUpperCase() + translated.slice(1);
  }
  return translated;
}
