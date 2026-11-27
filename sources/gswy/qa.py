"""Source and compiled-font quality gate for Gswy Serif.

Run after build with: python3 -m sources.gswy.qa
"""
from __future__ import annotations

import os
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

from .build import collect
from . import params as P

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONT_FILES = {
    "TTF": os.path.join(ROOT, "fonts", "GswySerif-Regular.ttf"),
    "OTF": os.path.join(ROOT, "fonts", "GswySerif-Regular.otf"),
    "WOFF2": os.path.join(ROOT, "fonts", "GswySerif-Regular.woff2"),
}


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


def source_checks(glyphs):
    names = set(glyphs)
    required = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    missing = sorted(required - names)
    if missing:
        fail("missing required glyph names: " + ", ".join(missing))

    codepoints = [entry[2] for entry in glyphs.values() if entry[2] is not None]
    if len(codepoints) != len(set(codepoints)):
        fail("duplicate Unicode codepoint mapping in source glyph registry")

    if len(glyphs) < 200:
        fail(f"expected a broad Latin character set; found only {len(glyphs)} glyphs")

    required_punctuation = {
        0x2E: "period", 0x2C: "comma", 0x3A: "colon",
        0x3B: "semicolon", 0x21: "exclam", 0x3F: "question",
    }
    for codepoint, expected_name in required_punctuation.items():
        entry = glyphs.get(expected_name)
        if not entry or entry[2] != codepoint:
            fail(f"U+{codepoint:04X} must be registered as {expected_name}")

    for name, (advance, path, codepoint) in glyphs.items():
        is_combining_mark = codepoint is not None and 0x0300 <= codepoint <= 0x036F
        if advance < 0 or (advance == 0 and not is_combining_mark):
            fail(f"{name}: only combining marks may have zero advance width")
        if name != "space" and not path.contours:
            fail(f"{name}: non-space glyph has no outline")
        for index, contour in enumerate(path.contours):
            if len(contour) < 3:
                fail(f"{name}: contour {index} has too few segments")

    return set(codepoints)


def compiled_checks(label, path, expected_codepoints):
    if not os.path.isfile(path):
        fail(f"{label} file is missing: {path}")
    try:
        font = TTFont(path, recalcBBoxes=True, recalcTimestamp=False)
    except Exception as exc:
        fail(f"{label} cannot be opened by fontTools: {exc}")

    cmap = font.getBestCmap() or {}
    missing = sorted(expected_codepoints - set(cmap))
    if missing:
        preview = ", ".join(f"U+{cp:04X}" for cp in missing[:12])
        fail(f"{label} is missing {len(missing)} source codepoints: {preview}")

    family = next(
        (record.toUnicode() for record in font["name"].names
         if record.nameID == 1),
        "",
    )
    if family != P.FAMILY:
        fail(f"{label} family name is {family!r}, expected {P.FAMILY!r}")

    if "hmtx" not in font or "head" not in font or "cmap" not in font:
        fail(f"{label} is missing a required OpenType table")

    glyph_set = font.getGlyphSet()
    for codepoint in expected_codepoints:
        glyph_name = cmap.get(codepoint)
        if not glyph_name or glyph_name == ".notdef" or glyph_name not in glyph_set:
            fail(f"{label}: U+{codepoint:04X} does not resolve to a real glyph")
        if codepoint != 0x20:
            pen = BoundsPen(glyph_set)
            glyph_set[glyph_name].draw(pen)
            if pen.bounds is None:
                fail(f"{label}: U+{codepoint:04X} ({glyph_name}) has an empty outline")

    punctuation_names = {
        0x2E: "period", 0x2C: "comma", 0x3A: "colon",
        0x3B: "semicolon", 0x21: "exclam", 0x3F: "question",
    }
    for codepoint, expected_name in punctuation_names.items():
        if cmap.get(codepoint) != expected_name:
            fail(f"{label}: U+{codepoint:04X} should map to {expected_name}, got {cmap.get(codepoint)!r}")

    print(f"PASS {label}: {len(cmap)} mapped characters, {len(font.getGlyphOrder())} glyphs")
    font.close()


def main():
    glyphs = collect()
    expected = source_checks(glyphs)
    print(f"PASS source: {len(glyphs)} glyphs, {len(expected)} Unicode mappings")
    for label, path in FONT_FILES.items():
        compiled_checks(label, path, expected)
    print("Gswy Serif quality gate passed.")


if __name__ == "__main__":
    main()
