import { useMemo } from "react";
import { alphabet } from "./alphabet.js";

const triangleGlyphs = Object.values(alphabet);

export default function TriangleField() {
  const triangles = useMemo(
    () => Array.from({ length: 34 }, (_, index) => ({
      glyph: triangleGlyphs[(index * 7) % triangleGlyphs.length],
      left: `${(index * 29 + 7) % 101}%`,
      top: `${(index * 41 + 3) % 103}%`,
      size: `${18 + ((index * 13) % 48)}px`,
      duration: `${13 + ((index * 17) % 22)}s`,
      delay: `${-((index * 11) % 25)}s`,
      drift: `${-80 + ((index * 37) % 161)}px`,
      opacity: 0.05 + ((index * 3) % 9) / 100,
    })),
    [],
  );

  return (
    <div className="triangle-field" aria-hidden="true">
      {triangles.map((triangle, index) => (
        <span
          className="floating-triangle"
          key={`${triangle.glyph}-${index}`}
          style={{
            "--left": triangle.left,
            "--top": triangle.top,
            "--size": triangle.size,
            "--duration": triangle.duration,
            "--delay": triangle.delay,
            "--drift": triangle.drift,
            "--opacity": triangle.opacity,
          }}
        >
          {triangle.glyph}
        </span>
      ))}
    </div>
  );
}
