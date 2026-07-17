const wordPattern = /\p{L}+(?:[-'’]\p{L}+)*/gu;
const trailingPunctuation = /^(.*?)([.!?。！？…]+)?$/u;
const hanCharacter = /\p{Script=Han}/u;

export function createTranslator(pack) {
  let reverseSentences = null;

  function getReverseSentences() {
    if (reverseSentences === null) {
      reverseSentences = invertSentences(pack.forwardSentences);
    }
    return reverseSentences;
  }

  return {
    forward(text) {
      const translated = translateWithLayers(text, {
        sentences: pack.forwardSentences,
        dictionary: pack.forwardDictionary,
        maxWords: pack.meta.forwardMaxWords,
        hanSource: false,
      });
      return pack.meta.targetIsHan ? joinHanRuns(translated) : translated;
    },
    reverse(text) {
      return translateWithLayers(text, {
        sentences: getReverseSentences(),
        dictionary: pack.reverseDictionary,
        maxWords: pack.meta.reverseMaxWords ?? 1,
        maxChars: pack.meta.reverseMaxChars ?? 0,
        hanSource: Boolean(pack.meta.targetIsHan),
        preferDictionary: true,
      });
    },
  };
}

function translateWithLayers(text, options) {
  if (options.preferDictionary) {
    const single = translateSingleTerm(text, options.dictionary);
    if (single !== "") return single;
  }
  const exact = translateExactSentence(text, options.sentences);
  if (exact !== "") return exact;
  return options.hanSource
    ? translateHanBySegments(text, options)
    : translateWordByWord(text, options);
}

function translateSingleTerm(value, dictionary) {
  const [, phrase = value, punctuation = ""] = value.trim().match(trailingPunctuation);
  const key = normalizeKey(phrase);
  if (!key || key.includes(" ")) return "";
  const translations = dictionary[key];
  if (!translations?.length) return "";
  return appendPunctuation(matchCase(phrase, translations[0]), punctuation);
}

function translateExactSentence(value, sentences) {
  const direct = sentences[normalizeKey(value)];
  if (direct) return matchCase(value, direct);

  const [, phrase = value, punctuation = ""] = value.trim().match(trailingPunctuation);
  const withoutPunctuation = sentences[normalizeKey(phrase)];
  if (!withoutPunctuation) return "";
  return appendPunctuation(matchCase(phrase, withoutPunctuation), punctuation);
}

function appendPunctuation(translated, punctuation) {
  if (!punctuation || /[.!?。！？…]$/u.test(translated)) return translated;
  return translated + punctuation;
}

function translateWordByWord(value, { dictionary, maxWords }) {
  const matches = Array.from(value.matchAll(wordPattern));
  if (matches.length === 0) return value;

  const translated = [];
  let cursor = 0;
  let index = 0;
  while (index < matches.length) {
    const match = findLongestMatch(value, matches, index, dictionary, maxWords);
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

function translateHanBySegments(value, { dictionary, maxChars }) {
  const translated = [];
  let index = 0;
  let previousWasTranslation = false;
  while (index < value.length) {
    const segment = findLongestHanSegment(value, index, dictionary, maxChars);
    if (segment) {
      if (previousWasTranslation) translated.push(" ");
      translated.push(segment.replacement);
      index += segment.length;
      previousWasTranslation = true;
      continue;
    }
    translated.push(value[index]);
    previousWasTranslation = false;
    index += 1;
  }
  return translated.join("");
}

function findLongestHanSegment(value, start, dictionary, maxChars) {
  if (!hanCharacter.test(value[start])) return null;
  const limit = Math.min(maxChars, value.length - start);
  for (let length = limit; length >= 1; length -= 1) {
    const translations = dictionary[value.slice(start, start + length)];
    if (translations?.length) {
      return { length, replacement: translations[0] };
    }
  }
  return null;
}

function findLongestMatch(value, matches, startIndex, dictionary, maxWords) {
  const limit = Math.min(matches.length, startIndex + maxWords);
  for (let endIndex = limit; endIndex > startIndex; endIndex -= 1) {
    const start = matches[startIndex].index;
    const last = matches[endIndex - 1];
    const end = last.index + last[0].length;
    const candidate = value.slice(start, end);
    if (!containsOnlyWordSeparators(candidate)) continue;

    const translations = dictionary[normalizeKey(candidate)];
    if (translations?.length) {
      return { start, end, replacement: translations[0], nextIndex: endIndex };
    }
  }
  return null;
}

function invertSentences(sentences) {
  const inverted = {};
  for (const [english, target] of Object.entries(sentences)) {
    const key = normalizeKey(stripTrailingPunctuation(target));
    if (key && !(key in inverted)) {
      inverted[key] = english.charAt(0).toUpperCase() + english.slice(1);
    }
  }
  return inverted;
}

function stripTrailingPunctuation(value) {
  const [, phrase = value] = value.trim().match(trailingPunctuation);
  return phrase;
}

function joinHanRuns(value) {
  return value.replace(/(?<=\p{Script=Han})[ \t]+(?=\p{Script=Han})/gu, "");
}

function containsOnlyWordSeparators(value) {
  return /^\p{L}+(?:[-'’ ]+\p{L}+)*$/u.test(value);
}

function normalizeKey(value) {
  return value.toLowerCase().replace(/\s+/gu, " ").trim();
}

function matchCase(source, translated) {
  const words = Array.from(source.matchAll(wordPattern), (match) => match[0]);
  if (
    words.length > 0 &&
    words.every((word) => word.toUpperCase() === word) &&
    words.some((word) => word.toLowerCase() !== word)
  ) {
    return translated.toUpperCase();
  }
  if (/^\p{Lu}/u.test(source)) {
    return translated.charAt(0).toUpperCase() + translated.slice(1);
  }
  return translated;
}
