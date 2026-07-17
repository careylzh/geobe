import { resolve } from "node:path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "/geobe/",
  plugins: [react()],
  build: {
    outDir: "site",
    emptyOutDir: false,
    rollupOptions: {
      input: {
        main: resolve(import.meta.dirname, "index.html"),
        translator: resolve(import.meta.dirname, "translator/index.html"),
      },
    },
  },
});
