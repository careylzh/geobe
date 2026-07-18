const hanCharacter = /\p{Script=Han}/u;
// ă, đ, ơ, ư and the tone-marked vowels in Latin Extended Additional are
// unique to Vietnamese among the supported languages (â/ê/ô are shared).
const vietnameseMark = /[ăđơưẠ-ỹ]/iu;
const portugueseMark = /[ãõ]/iu;
const frenchMark = /[èùœ]/iu;
const nonAsciiLetter = /[à-ʯ]/iu;
const wordPattern = /\p{L}+(?:[-'’]\p{L}+)*/gu;

// packs: latin-script packs keyed by language code, e.g. { fr, "pt-BR": pt, vi }.
// English is scored against the packs' forward (English-keyed) dictionaries.
export function detectLanguageCode(text, packs) {
  if (hanCharacter.test(text)) return "zh-Hans";
  if (vietnameseMark.test(text)) return "vi";

  const words = Array.from(text.matchAll(wordPattern), (match) => match[0].toLowerCase());
  if (words.length === 0) return "en";

  const candidates = Object.entries(packs);
  const scores = { en: 0 };
  for (const [code] of candidates) scores[code] = 0;

  for (const word of words) {
    if (candidates.some(([, pack]) => Object.hasOwn(pack.forwardDictionary, word))) {
      scores.en += 1;
    }
    for (const [code, pack] of candidates) {
      if (Object.hasOwn(pack.reverseDictionary, word)) scores[code] += 1;
    }
  }
  for (const code of Object.keys(scores)) scores[code] /= words.length;

  if (nonAsciiLetter.test(text)) scores.en = 0;
  if ("pt-BR" in scores && portugueseMark.test(text)) scores["pt-BR"] += 0.4;
  if ("fr" in scores && frenchMark.test(text)) scores.fr += 0.4;

  let best = "en";
  for (const code of Object.keys(scores)) {
    if (scores[code] > scores[best]) best = code;
  }
  return best;
}
