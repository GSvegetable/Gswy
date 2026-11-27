"""构建管线：字形注册表 → UFO 源 + TTF + OTF + WOFF2。"""
import os
import sys

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.ttLib import TTFont
from fontTools.agl import UV2AGL

from . import params as P
from .path import Path, rect
from .lowercase import LOWER
from .uppercase import UPPER

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def collect():
    """返回 {glyphName: (advance, Path, unicode)}。"""
    glyphs = {}
    glyphs[".notdef"] = (500, rect(60, 0, 440, 700), None)
    glyphs["space"] = (260, Path(), 0x20)
    for ch, fn in LOWER.items():
        adv, path = fn()
        glyphs[ch] = (adv, path, ord(ch))
    for ch, fn in UPPER.items():
        adv, path = fn()
        glyphs[ch] = (adv, path, ord(ch))
    try:
        from .figures import FIGURES
        for ch, fn in FIGURES.items():
            adv, path = fn()
            glyphs[ch] = (adv, path, ord(ch))
    except ImportError:
        pass
    try:
        from .punctuation import PUNCT
        for ch, fn in PUNCT.items():
            adv, path = fn()
            name = UV2AGL.get(ord(ch), "uni%04X" % ord(ch))
            glyphs[name] = (adv, path, ord(ch))
    except ImportError:
        pass
    try:
        from .accents import build_accented
        for name, adv, path, uni in build_accented(glyphs):
            glyphs[name] = (adv, path, uni)
    except ImportError:
        pass
    return glyphs


def name_strings():
    fam = P.FAMILY
    full = f"{fam} {P.STYLE}"
    ps = f"{fam.replace(' ', '')}-{P.STYLE}"
    return {
        "familyName": fam,
        "styleName": P.STYLE,
        "uniqueFontIdentifier": f"{P.VERSION};{ps}",
        "fullName": full,
        "psName": ps,
        "version": f"Version {P.VERSION}",
        "copyright": "Copyright 2026 The Gswy Serif Project Authors",
        "licenseDescription": "This Font Software is licensed under the SIL Open Font License, Version 1.1.",
        "licenseInfoURL": "https://openfontlicense.org",
    }


KERN_PAIRS = {
    ("T", "a"): -60, ("T", "o"): -55, ("T", "e"): -55, ("T", "c"): -50,
    ("T", "u"): -45, ("T", "w"): -40, ("T", "y"): -40, ("T", "s"): -45,
    ("V", "a"): -55, ("V", "o"): -50, ("V", "e"): -50, ("V", "u"): -35,
    ("V", "y"): -25, ("W", "a"): -45, ("W", "o"): -40, ("W", "e"): -40,
    ("W", "u"): -30, ("Y", "a"): -60, ("Y", "o"): -60, ("Y", "e"): -60,
    ("Y", "u"): -45, ("Y", "p"): -40, ("A", "v"): -35, ("A", "w"): -30,
    ("A", "y"): -35, ("A", "V"): -60, ("A", "W"): -50, ("A", "Y"): -60,
    ("A", "T"): -55, ("F", "a"): -35, ("F", "o"): -25, ("F", "e"): -25,
    ("P", "a"): -25, ("P", "o"): -20, ("L", "T"): -50, ("L", "V"): -55,
    ("L", "Y"): -55, ("L", "W"): -40, ("r", "a"): -12, ("r", "o"): -10,
    ("r", "e"): -10, ("v", "a"): -18, ("w", "a"): -15, ("y", "a"): -18,
    ("k", "o"): -12, ("x", "o"): -12, ("f", "a"): -15, ("f", "o"): -12,
}
KERN_PAIRS = {k: v for k, v in KERN_PAIRS.items() if v != 0}


def add_kerning(font):
    from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
    line = " ".join(f"pos {a} {b} {v};" for (a, b), v in KERN_PAIRS.items())
    fea = f"feature kern {{ {line} }} kern;"
    addOpenTypeFeaturesFromString(font, fea)


def setup_common(fb, glyphs, ns):
    order = list(glyphs.keys())
    cmap = {u: n for n, (a, p, u) in glyphs.items() if u is not None}
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap)
    fb.setupHorizontalMetrics({n: (a, p.bounds()[0] if p.contours else 0)
                               for n, (a, p, u) in glyphs.items()})
    fb.setupHorizontalHeader(ascent=900, descent=-280)
    fb.setupNameTable(ns)
    fb.setupOS2(
        sTypoAscender=750, sTypoDescender=-250, sTypoLineGap=100,
        usWinAscent=900, usWinDescent=280,
        sxHeight=P.XH, sCapHeight=P.CAP,
        usWeightClass=400, usWidthClass=5,
        fsType=0,
    )
    fb.setupPost()
    return order


def build_ttf(glyphs, out):
    ns = name_strings()
    fb = FontBuilder(P.UPM, isTTF=True)
    setup_common(fb, glyphs, ns)
    tt = {}
    for n, (a, p, u) in glyphs.items():
        pen = TTGlyphPen(None)
        cu = Cu2QuPen(pen, max_err=1.0, reverse_direction=True)
        p.draw(cu)
        tt[n] = pen.glyph()
    fb.setupGlyf(tt)
    add_kerning(fb.font)
    fb.font.save(out)
    return out


def build_otf(glyphs, out):
    ns = name_strings()
    fb = FontBuilder(P.UPM, isTTF=False)
    setup_common(fb, glyphs, ns)
    cs = {}
    for n, (a, p, u) in glyphs.items():
        pen = T2CharStringPen(a, None)
        p.draw(pen)
        cs[n] = pen.getCharString()
    fb.setupCFF(
        ns["psName"],
        {"FullName": ns["fullName"], "FamilyName": P.FAMILY,
         "Weight": P.STYLE,
         "FontBBox": [-100, -300, 1100, 900]},
        cs, {})
    add_kerning(fb.font)
    fb.font.save(out)
    return out


def build_woff2(ttf_path, out):
    f = TTFont(ttf_path)
    f.flavor = "woff2"
    f.save(out)
    return out


def build_ufo(glyphs, out_dir):
    from fontTools.ufoLib import UFOWriter
    from fontTools.ufoLib.glifLib import writeGlyphToString

    class G:
        pass

    import shutil
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    w = UFOWriter(out_dir, formatVersion=3)
    w.writeInfo(dict(
        familyName=P.FAMILY, styleName=P.STYLE,
        unitsPerEm=P.UPM, ascender=750, descender=-250,
        capHeight=P.CAP, xHeight=P.XH,
        copyright="Copyright 2026 The Gswy Serif Project Authors",
        openTypeNameRecords=[],
    ))
    w.writeLib({"public.glyphOrder": list(glyphs.keys())})
    gs = w.getGlyphSet()
    for n, (a, p, u) in glyphs.items():
        g = G()
        g.width = a
        g.unicodes = [u] if u is not None else []
        fn = n
        gs.writeGlyph(fn, g, p.drawPoints)
    gs.writeContents()
    return out_dir


def main():
    glyphs = collect()
    fonts = os.path.join(ROOT, "fonts")
    os.makedirs(fonts, exist_ok=True)
    ttf = build_ttf(glyphs, os.path.join(fonts, "GswySerif-Regular.ttf"))
    otf = build_otf(glyphs, os.path.join(fonts, "GswySerif-Regular.otf"))
    w2 = build_woff2(ttf, os.path.join(fonts, "GswySerif-Regular.woff2"))
    build_ufo(glyphs, os.path.join(ROOT, "ufo", "GswySerif-Regular.ufo"))
    print(f"字形数: {len(glyphs)}")
    for f in (ttf, otf, w2):
        print("OK", f, os.path.getsize(f), "bytes")


if __name__ == "__main__":
    main()
