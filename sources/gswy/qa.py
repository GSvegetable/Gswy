"""Quality gate for both original Gswy font families and all web/desktop builds."""
from __future__ import annotations

import os
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

from .build import collect, KERN_PAIRS
from . import params as P
from sources.build_victorian_hand import pen_written

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONT_SETS = {
    "Gswy Serif": {
        "family": "Gswy Serif",
        "style": "Regular",
        "italic": False,
        "files": {
            "TTF": "GswySerif-Regular.ttf",
            "OTF": "GswySerif-Regular.otf",
            "WOFF2": "GswySerif-Regular.woff2",
        },
    },
    "Victorian Hand": {
        "family": "Gswy Victorian Hand",
        "style": "Italic",
        "italic": True,
        "files": {
            "TTF": "GswyVictorianHand-Italic.ttf",
            "OTF": "GswyVictorianHand-Italic.otf",
            "WOFF2": "GswyVictorianHand-Italic.woff2",
        },
    },
}


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


def source_checks(glyphs, label):
    names = set(glyphs)
    required = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    missing = sorted(required - names)
    if missing:
        fail(f"{label}: missing required glyph names: " + ", ".join(missing))

    codepoints = [entry[2] for entry in glyphs.values() if entry[2] is not None]
    if len(codepoints) != len(set(codepoints)):
        fail(f"{label}: duplicate Unicode codepoint mapping")

    if len(glyphs) < 200:
        fail(f"{label}: expected at least 200 glyphs; found {len(glyphs)}")

    required_punctuation = {
        0x2E: "period", 0x2C: "comma", 0x3A: "colon",
        0x3B: "semicolon", 0x21: "exclam", 0x3F: "question",
    }
    for codepoint, expected_name in required_punctuation.items():
        entry = glyphs.get(expected_name)
        if not entry or entry[2] != codepoint:
            fail(f"{label}: U+{codepoint:04X} must be registered as {expected_name}")

    for name, (advance, path, codepoint) in glyphs.items():
        is_mark = codepoint is not None and 0x0300 <= codepoint <= 0x036F
        if advance < 0 or (advance == 0 and not is_mark):
            fail(f"{label}/{name}: invalid advance width")
        if name != "space" and not path.contours:
            fail(f"{label}/{name}: no outline")
        for index, contour in enumerate(path.contours):
            if len(contour) < 3:
                fail(f"{label}/{name}: contour {index} has too few segments")

    return set(codepoints)


def compiled_checks(label, path, expected_codepoints, family, style, italic):
    if not os.path.isfile(path):
        fail(f"{label}: missing file {path}")
    if os.path.getsize(path) < 1024:
        fail(f"{label}: suspiciously small font file")

    try:
        font = TTFont(path, recalcBBoxes=True, recalcTimestamp=False)
        font.ensureDecompiled()
    except Exception as exc:
        fail(f"{label}: cannot parse font: {exc}")

    required_tables = {"name", "head", "hhea", "hmtx", "maxp", "cmap", "OS/2", "post", "GPOS"}
    missing_tables = required_tables - set(font.keys())
    if missing_tables:
        fail(f"{label}: missing OpenType tables: {', '.join(sorted(missing_tables))}")

    cmap = font.getBestCmap() or {}
    missing = sorted(expected_codepoints - set(cmap))
    if missing:
        sample = ", ".join(f"U+{cp:04X}" for cp in missing[:12])
        fail(f"{label}: {len(missing)} Unicode mappings missing: {sample}")

    names = font["name"].names
    def name_value(name_id):
        return next((record.toUnicode() for record in names if record.nameID == name_id), "")

    if name_value(1) != family:
        fail(f"{label}: family name {name_value(1)!r}, expected {family!r}")
    if name_value(2) != style:
        fail(f"{label}: subfamily name {name_value(2)!r}, expected {style!r}")
    if font["head"].unitsPerEm != P.UPM:
        fail(f"{label}: unitsPerEm {font['head'].unitsPerEm}, expected {P.UPM}")

    feature_list = getattr(font["GPOS"].table, "FeatureList", None)
    feature_tags = {record.FeatureTag for record in feature_list.FeatureRecord} if feature_list else set()
    if "kern" not in feature_tags:
        fail(f"{label}: GPOS kern feature is missing")

    selection = font["OS/2"].fsSelection
    mac_style = font["head"].macStyle
    italic_angle = font["post"].italicAngle
    if italic and not (selection & 0x01 and mac_style & 0x02 and italic_angle < -1):
        fail(f"{label}: italic metadata is incomplete (fsSelection/macStyle/post.italicAngle)")
    if not italic and (selection & 0x01 or mac_style & 0x02 or italic_angle != 0):
        fail(f"{label}: Regular font is incorrectly marked italic")

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

    for cp, glyph_name in {
        0x2E: "period", 0x2C: "comma", 0x3A: "colon",
        0x3B: "semicolon", 0x21: "exclam", 0x3F: "question",
    }.items():
        if cmap.get(cp) != glyph_name:
            fail(f"{label}: U+{cp:04X} should map to {glyph_name}")

    print(f"PASS {label}: {len(cmap)} mapped characters, {len(font.getGlyphOrder())} glyphs")
    font.close()


def main():
    base_glyphs = collect()
    families = {
        "Gswy Serif": base_glyphs,
        "Victorian Hand": pen_written(base_glyphs),
    }

    for family_key, config in FONT_SETS.items():
        glyphs = families[family_key]
        expected = source_checks(glyphs, family_key)
        print(f"PASS {family_key} source: {len(glyphs)} glyphs, {len(expected)} Unicode mappings")
        for format_name, filename in config["files"].items():
            path = os.path.join(ROOT, "fonts", filename)
            compiled_checks(
                f"{family_key} {format_name}", path, expected,
                config["family"], config["style"], config["italic"],
            )

    if len(KERN_PAIRS) < 40:
        fail(f"expected at least 40 kerning pairs; found {len(KERN_PAIRS)}")
    for left, right in KERN_PAIRS:
        if left not in base_glyphs or right not in base_glyphs:
            fail(f"kerning pair {left}/{right} references a missing glyph")

    print("All Gswy font quality checks passed.")


if __name__ == "__main__":
    main()
