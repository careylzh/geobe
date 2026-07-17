import {
  englishPortuguese,
  maxTranslationWords,
} from "../engPorDictionary.js";
import { tatoebaEnglishPortuguese } from "../tatoebaPhrases.js";
import { portugueseEnglish, reverseMaxWords } from "./ptReverseDictionary.js";

export const meta = {
  code: "pt-BR",
  forwardMaxWords: maxTranslationWords,
  reverseMaxWords,
};
export const forwardDictionary = englishPortuguese;
export const reverseDictionary = portugueseEnglish;
export const forwardSentences = tatoebaEnglishPortuguese;
