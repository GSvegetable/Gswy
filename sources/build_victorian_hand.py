"""Build the separate Victorian Hand italic cut.

This is a historically-inspired pen-written display serif: a measured right
slant, narrower rhythm, and preserved high-contrast pen logic. It is not
marketed as a fully connected copperplate script.
"""
import os
from sources.gswy import params as P
from sources.gswy.build import collect, build_ttf, build_otf, build_woff2
from sources.gswy.path import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLANT = 0.1763  # 10 degrees
WIDTH = 0.94


def pen_written(glyphs):
    """Apply a true outline shear, not a CSS-only italic simulation."""
    result = {}
    for name, (advance, path, uni) in glyphs.items():
        transformed = Path()
        for contour in path.contours:
            new_contour = []
            for seg in contour:
                points = []
                for x, y in seg[1:]:
                    # Slightly tighter proportions and a consistent pen angle.
                    points.append((x * WIDTH + y * SLANT, y))
                new_contour.append(tuple([seg[0]] + points))
            transformed.contours.append(new_contour)
        result[name] = (round(advance * WIDTH + P.UPM * SLANT * 0.72), transformed, uni)
    return result


def main():
    old_family, old_style, old_version = P.FAMILY, P.STYLE, P.VERSION
    try:
        P.FAMILY = "Gswy Victorian Hand"
        P.STYLE = "Italic"
        P.VERSION = "0.1.0"
        glyphs = pen_written(collect())
        fonts = os.path.join(ROOT, "fonts")
        os.makedirs(fonts, exist_ok=True)
        ttf = build_ttf(glyphs, os.path.join(fonts, "GswyVictorianHand-Italic.ttf"))
        build_otf(glyphs, os.path.join(fonts, "GswyVictorianHand-Italic.otf"))
        build_woff2(ttf, os.path.join(fonts, "GswyVictorianHand-Italic.woff2"))
        print(f"Built {len(glyphs)} Victorian Hand italic glyphs")
    finally:
        P.FAMILY, P.STYLE, P.VERSION = old_family, old_style, old_version


if __name__ == "__main__":
    main()
