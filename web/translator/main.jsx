import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "../styles.css";
import "./translator.css";
import TranslatorApp from "./TranslatorApp.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <TranslatorApp />
  </StrictMode>,
);
