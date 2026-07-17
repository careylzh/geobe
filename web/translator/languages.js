export const languages = [
  {
    code: "en",
    label: "English",
    nativeName: "English",
    sample: "hello world",
    load: null,
  },
  {
    code: "zh-Hans",
    label: "Mandarin Chinese (Simplified)",
    nativeName: "简体中文",
    sample: "你好",
    load: () => import("../packs/zh.js"),
  },
  {
    code: "pt-BR",
    label: "Portuguese (Brazil)",
    nativeName: "Português (Brasil)",
    sample: "olá mundo",
    load: () => import("../packs/pt.js"),
  },
  {
    code: "vi",
    label: "Vietnamese",
    nativeName: "Tiếng Việt",
    sample: "xin chào",
    load: () => import("../packs/vi.js"),
  },
  {
    code: "fr",
    label: "French",
    nativeName: "Français",
    sample: "bonjour le monde",
    load: () => import("../packs/fr.js"),
  },
];

export function getLanguage(code) {
  return languages.find((language) => language.code === code) ?? languages[0];
}
