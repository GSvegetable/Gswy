"""重音符号与组合字形。"""
import math
from .path import Path, ring, annulus_sector, rect, quad
from .parts import dot
from .parts import serif_stem, plain_stem, bar, diag
from . import params as P


# ---- 重音部件（原点为附着点，向上生长）----

def acc_acute():
    return quad((-70, 0), (10, 0), (110, 150), (50, 160))


def acc_grave():
    return acc_acute().mirror_x(20)


def acc_circumflex():
    p = Path()
    p.moveTo((-120, 0)).lineTo((-58, 0)).lineTo((0, 102))
    p.lineTo((58, 0)).lineTo((120, 0)).lineTo((0, 168)).closePath()
    return p.orient_ccw()


def acc_caron():
    return acc_circumflex().transformed(lambda t: (t[0], 150 - t[1]))


def acc_tilde():
    p = Path()
    p.moveTo((-115, 30))
    p.curveTo((-70, 105), (-30, 105), (10, 60))
    p.curveTo((45, 22), (75, 25), (110, 80))
    p.lineTo((110, 122))
    p.curveTo((70, 55), (40, 55), (5, 95))
    p.curveTo((-30, 135), (-75, 135), (-115, 72))
    p.closePath()
    return p.orient_ccw()


def acc_dieresis():
    return dot(-68, 70, 42).extend(dot(68, 70, 42))


def acc_macron():
    return bar(-105, 105, 50, 38)


def acc_breve():
    return annulus_sector(0, 150, 115, 105, 42, 30, 200, 340)


def acc_ring():
    return ring(0, 95, 72, 72, 30, 26)


def acc_dotaccent():
    return dot(0, 70, 42)


def acc_hungarumlaut():
    a = acc_acute().scale(0.8)
    return a.translate(-60).extend(a.translate(70))


def acc_cedilla():
    p = rect(-16, -60, 16, 10)
    p.extend(annulus_sector(0, -100, 55, 50, 30, 24, 0, 270))
    return p


def acc_ogonek():
    return annulus_sector(30, -90, 60, 70, 30, 24, 90, 250)


ACCENTS = {
    "acute": acc_acute, "grave": acc_grave, "circumflex": acc_circumflex,
    "caron": acc_caron, "tilde": acc_tilde, "dieresis": acc_dieresis,
    "macron": acc_macron, "breve": acc_breve, "ring": acc_ring,
    "dotaccent": acc_dotaccent, "hungarumlaut": acc_hungarumlaut,
    "cedilla": acc_cedilla, "ogonek": acc_ogonek,
}

# 独立占位重音（spacing）
SPACING = {
    "\u00b4": ("acute", 300), "\u0060": ("grave", 300),
    "\u00a8": ("dieresis", 300), "\u00af": ("macron", 300),
    "\u00b8": ("cedilla", 300), "\u02c6": ("circumflex", 300),
    "\u02dc": ("tilde", 300), "\u02da": ("ring", 300),
    "\u02dd": ("hungarumlaut", 300), "\u02d8": ("breve", 300),
    "\u02d9": ("dotaccent", 300), "\u02db": ("ogonek", 300),
    "\u02c7": ("caron", 300),
}

# 组合用重音（零宽）
COMBINING = {
    "\u0301": "acute", "\u0300": "grave", "\u0302": "circumflex",
    "\u0303": "tilde", "\u0308": "dieresis", "\u0304": "macron",
    "\u0306": "breve", "\u030a": "ring", "\u030b": "hungarumlaut",
    "\u030c": "caron", "\u0307": "dotaccent", "\u0327": "cedilla",
    "\u0328": "ogonek",
}

LOWER_COMBOS = {
    "a": ["grave", "acute", "circumflex", "tilde", "dieresis", "ring"],
    "c": ["cedilla"],
    "e": ["grave", "acute", "circumflex", "dieresis"],
    "i": ["grave", "acute", "circumflex", "dieresis"],
    "n": ["tilde"],
    "o": ["grave", "acute", "circumflex", "tilde", "dieresis"],
    "u": ["grave", "acute", "circumflex", "dieresis"],
    "y": ["acute", "dieresis"],
}
UPPER_COMBOS = {
    "A": ["grave", "acute", "circumflex", "tilde", "dieresis", "ring"],
    "C": ["cedilla"],
    "E": ["grave", "acute", "circumflex", "dieresis"],
    "I": ["grave", "acute", "circumflex", "dieresis"],
    "N": ["tilde"],
    "O": ["grave", "acute", "circumflex", "tilde", "dieresis"],
    "U": ["grave", "acute", "circumflex", "dieresis"],
    "Y": ["acute", "dieresis"],
}

UNI_MAP = {
    ("a", "grave"): 0xE0, ("a", "acute"): 0xE1, ("a", "circumflex"): 0xE2,
    ("a", "tilde"): 0xE3, ("a", "dieresis"): 0xE4, ("a", "ring"): 0xE5,
    ("c", "cedilla"): 0xE7,
    ("e", "grave"): 0xE8, ("e", "acute"): 0xE9, ("e", "circumflex"): 0xEA,
    ("e", "dieresis"): 0xEB,
    ("i", "grave"): 0xEC, ("i", "acute"): 0xED, ("i", "circumflex"): 0xEE,
    ("i", "dieresis"): 0xEF,
    ("n", "tilde"): 0xF1,
    ("o", "grave"): 0xF2, ("o", "acute"): 0xF3, ("o", "circumflex"): 0xF4,
    ("o", "tilde"): 0xF5, ("o", "dieresis"): 0xF6,
    ("u", "grave"): 0xF9, ("u", "acute"): 0xFA, ("u", "circumflex"): 0xFB,
    ("u", "dieresis"): 0xFC,
    ("y", "acute"): 0xFD, ("y", "dieresis"): 0xFF,
    ("A", "grave"): 0xC0, ("A", "acute"): 0xC1, ("A", "circumflex"): 0xC2,
    ("A", "tilde"): 0xC3, ("A", "dieresis"): 0xC4, ("A", "ring"): 0xC5,
    ("C", "cedilla"): 0xC7,
    ("E", "grave"): 0xC8, ("E", "acute"): 0xC9, ("E", "circumflex"): 0xCA,
    ("E", "dieresis"): 0xCB,
    ("I", "grave"): 0xCC, ("I", "acute"): 0xCD, ("I", "circumflex"): 0xCE,
    ("I", "dieresis"): 0xCF,
    ("N", "tilde"): 0xD1,
    ("O", "grave"): 0xD2, ("O", "acute"): 0xD3, ("O", "circumflex"): 0xD4,
    ("O", "tilde"): 0xD5, ("O", "dieresis"): 0xD6,
    ("U", "grave"): 0xD9, ("U", "acute"): 0xDA, ("U", "circumflex"): 0xDB,
    ("U", "dieresis"): 0xDC,
    ("Y", "acute"): 0xDD, ("Y", "dieresis"): 0x178,
}


def extra_letters():
    out = []
    # 无点 i
    out.append(("dotlessi", 280, serif_stem(140, 0, P.XH), 0x131))
    # æ / Æ
    from .lowercase import g_a, g_e
    from .uppercase import g_A, g_E
    pa = g_a()[1].extend(g_e()[1].translate(420))
    out.append(("ae", 950, pa, 0xE6))
    pA = g_A()[1].extend(g_E()[1].translate(520))
    out.append(("AE", 1150, pA, 0xC6))
    # œ / Œ
    from .lowercase import g_o
    from .uppercase import g_O
    po = g_o()[1].extend(g_e()[1].translate(440))
    out.append(("oe", 970, po, 0x153))
    pO = g_O()[1].extend(g_E()[1].translate(620))
    out.append(("OE", 1250, pO, 0x152))
    # ø / Ø
    p = g_o()[1].extend(diag(90, -40, 450, 520, 64, 64))
    out.append(("oslash", 540, p, 0xF8))
    p = g_O()[1].extend(diag(140, -40, 620, 740, 80, 80))
    out.append(("Oslash", 760, p, 0xD8))
    # Ð / ð
    from .uppercase import g_D
    p = g_D()[1].extend(bar(10, 250, 330, 34))
    out.append(("Eth", 720, p, 0xD0))
    p = ring(250, 200, 210, 212, 88, 30)
    p.extend(annulus_sector(280, 480, 180, 230, 80, 32, -30, 210))
    p.extend(bar(150, 470, 560, 32))
    out.append(("eth", 540, p, 0xF0))
    # Þ / þ
    p = serif_stem(130, 0, P.CAP, ext=36, w=P.CSTEM)
    p.extend(annulus_sector(330, 350, 280, 187, 96, 34, -90, 90))
    p.extend(bar(80, 340, 500, 36))
    p.extend(bar(80, 340, 164, 36))
    out.append(("Thorn", 620, p, 0xDE))
    p = serif_stem(110, P.DESC, P.ASC)
    p.extend(ring(300, 240, 215, 252, P.STEM, P.THIN))
    out.append(("thorn", 550, p, 0xFE))
    # ß
    p = serif_stem(110, 0, 700)
    p.extend(annulus_sector(330, 530, 200, 170, 88, 32, -90, 90))
    p.extend(bar(80, 340, 664, 36))
    p.extend(annulus_sector(340, 190, 210, 190, 90, 32, -90, 150))
    p.extend(bar(80, 340, 330, 34))
    out.append(("germandbls", 620, p, 0xDF))
    return out


def build_accented(glyphs):
    out = []
    for name, adv, path, uni in extra_letters():
        out.append((name, adv, path, uni))
        glyphs[name] = (adv, path, uni)
    # 占位与组合重音
    for ch, (acc, adv) in SPACING.items():
        p = ACCENTS[acc]().translate(150, 620 if acc != "cedilla" else 0)
        out.append(("uni%04X" % ord(ch), adv, p, ord(ch)))
    for ch, acc in COMBINING.items():
        below = acc in ("cedilla", "ogonek")
        p = ACCENTS[acc]().translate(0, 0 if below else 500)
        out.append(("uni%04X" % ord(ch), 0, p, ord(ch)))
    # 组合字母
    for base, accs in list(LOWER_COMBOS.items()) + list(UPPER_COMBOS.items()):
        badv, bpath, _ = glyphs[base]
        bx0, by0, bx1, by1 = bpath.bounds()
        cx = (bx0 + bx1) / 2
        for acc in accs:
            uni = UNI_MAP[(base, acc)]
            if acc == "cedilla":
                ap = ACCENTS[acc]().translate(cx, 0)
            else:
                bb = bpath
                if base == "i":
                    bb = glyphs["dotlessi"][1]
                top = bb.bounds()[3]
                ap = ACCENTS[acc]().translate(cx, top + 24)
            p = Path()
            p.contours = list(bpath.contours)
            if base == "i" and acc != "cedilla":
                p.contours = list(glyphs["dotlessi"][1].contours)
            p.extend(ap)
            name = "uni%04X" % uni
            out.append((name, badv, p, uni))
    return out
