"""标点与符号字形。"""
import math
from .path import Path, ring, annulus_sector, rect, quad, ellipse, append_arc
from .parts import serif_stem, plain_stem, bar, dot, diag
from . import params as P


def _wedge(x0, x1, y_top, y_bot, taper=0.55):
    w = x1 - x0
    cx = (x0 + x1) / 2
    hw = w * taper / 2
    return quad((x0, y_top), (x1, y_top), (cx + hw, y_bot), (cx - hw, y_bot))


def g_period():
    return 280, dot(140, 52, 52)


def g_comma():
    p = dot(140, 52, 52)
    p.extend(quad((96, 60), (162, 60), (120, -110), (78, -88)))
    return 280, p


def g_colon():
    p = dot(140, 52, 52).extend(dot(140, 360, 52))
    return 280, p


def g_semicolon():
    p = dot(140, 360, 52)
    p.extend(dot(140, 52, 52))
    p.extend(quad((96, 60), (162, 60), (120, -110), (78, -88)))
    return 280, p


def g_exclam():
    p = quad((100, 700), (180, 700), (160, 200), (120, 200))
    p.extend(dot(140, 52, 52))
    return 280, p


def g_question():
    p = annulus_sector(250, 520, 190, 180, 84, 32, 160, 270)
    p.extend(rect(206, 180, 294, 360))
    p.extend(rect(60, 560, 140, 600))
    p.extend(dot(250, 52, 52))
    return 500, p


def g_quotesingle():
    return 250, _wedge(95, 155, 700, 500)


def g_quotedbl():
    p = _wedge(80, 140, 700, 500).extend(_wedge(230, 290, 700, 500))
    return 380, p


def g_quoteleft():
    p = dot(140, 620, 50)
    p.extend(quad((98, 612), (162, 612), (122, 760), (80, 742)))
    return 280, p


def g_quoteright():
    p = dot(140, 620, 50)
    p.extend(quad((98, 628), (162, 628), (120, 470), (78, 490)))
    return 280, p


def g_quotedblleft():
    p = g_quoteleft()[1]
    p.extend(g_quoteleft()[1].translate(170))
    return 450, p


def g_quotedblright():
    p = g_quoteright()[1]
    p.extend(g_quoteright()[1].translate(170))
    return 450, p


def g_hyphen():
    return 400, bar(60, 340, 240, 42)


def g_endash():
    return 600, bar(40, 560, 240, 38)


def g_emdash():
    return 1000, bar(0, 1000, 240, 38)


def g_parenleft():
    p = Path()
    append_arc(p, 330, 250, 230, 490, 100, 260, move=True)
    append_arc(p, 330, 250, 140, 450, 260, 100)
    p.closePath()
    return 380, p


def g_parenright():
    return 380, g_parenleft()[1].mirror_x(190)


def g_bracketleft():
    p = rect(100, -140, 180, 740)
    p.extend(bar(100, 310, 704, 36))
    p.extend(bar(100, 310, -140, 36))
    return 380, p


def g_bracketright():
    return 380, g_bracketleft()[1].mirror_x(190)


def g_slash():
    return 400, diag(60, -80, 340, 760, 72, 72)


def g_backslash():
    return 400, diag(340, -80, 60, 760, 72, 72)


def g_asterisk():
    p = Path()
    cx, cy = 200, 560
    for ang in (90, 162, 234, 306, 18):
        a = math.radians(ang)
        dx, dy = math.cos(a), math.sin(a)
        L, W = 130, 20
        px, py = -dy, dx
        p.extend(quad(
            (cx + dx * L + px * W, cy + dy * L + py * W),
            (cx + dx * L - px * W, cy + dy * L - py * W),
            (cx - dx * L - px * W, cy - dy * L - py * W),
            (cx - dx * L + px * W, cy - dy * L + py * W)))
    return 400, p


def g_plus():
    p = bar(60, 440, 270, 40)
    p.extend(rect(230, 70, 270, 470))
    return 500, p


def g_minus():
    return 500, bar(60, 440, 270, 40)


def g_equal():
    p = bar(60, 440, 350, 40).extend(bar(60, 440, 190, 40))
    return 500, p


def g_less():
    p = quad((420, 90), (420, 140), (110, 290), (110, 250))
    p.extend(quad((110, 250), (110, 290), (420, 440), (420, 390)))
    return 500, p


def g_greater():
    return 500, g_less()[1].mirror_x(265)


def g_numbersign():
    p = diag(150, 0, 230, 660, 60, 60)
    p.extend(diag(330, 0, 410, 660, 60, 60))
    p.extend(bar(40, 520, 180, 40))
    p.extend(bar(60, 540, 420, 40))
    return 560, p


def g_dollar():
    from .lowercase import _s_shape
    p = _s_shape(280, 480, 200, 185, 265, 180, 215, 185, 84, 88, 32)
    p.extend(rect(252, -60, 308, 720))
    return 560, p


def g_percent():
    p = ring(170, 520, 130, 145, 62, 26)
    p.extend(ring(630, 140, 130, 145, 62, 26))
    p.extend(diag(230, -20, 570, 680, 64, 64))
    return 800, p


def g_ampersand():
    p = annulus_sector(300, 490, 155, 160, 78, 30, -35, 270)
    p.extend(annulus_sector(280, 170, 200, 180, 88, 32, 30, 330))
    p.extend(diag(640, 0, 330, 330, 84, 52))
    p.extend(rect(560, 0, 680, 40))
    return 700, p


def g_at():
    p = annulus_sector(450, 330, 380, 390, 72, 30, -25, 330)
    p.extend(ring(420, 330, 170, 175, 60, 26))
    p.extend(rect(530, 170, 592, 480))
    p.extend(quad((530, 170), (762, 170), (762, 222), (530, 226)))
    return 900, p


def g_underscore():
    return 500, bar(0, 500, -140, 38)


def g_exclamdown():
    p = quad((100, -200), (180, -200), (160, 300), (120, 300))
    p.extend(dot(140, 448, 52))
    return 280, p


def g_questiondown():
    p = g_question()[1].transformed(lambda t: (500 - t[0], 500 - t[1]))
    return 500, p


def g_guillemotleft():
    c = Path()
    c.moveTo((230, 60)).lineTo((272, 60)).lineTo((142, 250))
    c.lineTo((272, 440)).lineTo((230, 440)).lineTo((100, 250)).closePath()
    c = c.orient_ccw()
    p = c.extend(c.translate(160))
    return 500, p


def g_guillemotright():
    return 500, g_guillemotleft()[1].mirror_x(250)


def g_degree():
    return 400, ring(200, 580, 110, 115, 44, 22)


def g_bullet():
    return 400, dot(200, 280, 85)


def g_dagger():
    p = rect(170, -100, 230, 700)
    p.extend(bar(50, 350, 480, 44))
    return 400, p


def g_daggerdbl():
    p = rect(170, -100, 230, 700)
    p.extend(bar(50, 350, 480, 44))
    p.extend(bar(50, 350, 120, 44))
    return 400, p


def g_section():
    from .lowercase import _s_shape
    p = _s_shape(250, 480, 160, 140, 240, 250, 170, 140, 66, 70, 28)
    p.extend(_s_shape(250, 300, 160, 140, 240, 70, 170, 140, 66, 70, 28).translate(0, -0))
    return 500, p


def g_paragraph():
    p = annulus_sector(300, 500, 220, 200, 88, 34, 90, 270)
    p.extend(rect(256, 0, 336, 700))
    p.extend(rect(420, 0, 480, 700))
    p.extend(bar(256, 480, 664, 36))
    return 560, p


def g_copyright():
    p = ring(450, 350, 390, 390, 52, 28)
    p.extend(annulus_sector(450, 350, 210, 220, 70, 28, 40, 320))
    return 900, p


def g_registered():
    p = ring(450, 350, 390, 390, 52, 28)
    p.extend(rect(310, 140, 372, 560))
    p.extend(annulus_sector(430, 460, 140, 110, 60, 26, -90, 90))
    p.extend(bar(310, 440, 534, 26))
    p.extend(bar(310, 440, 350, 26))
    p.extend(diag(560, 140, 430, 360, 60, 40))
    return 900, p


def g_cent():
    p = annulus_sector(260, 280, 190, 220, 80, 30, 40, 320)
    p.extend(rect(352, 420, 440, 452))
    p.extend(rect(232, -40, 288, 600))
    return 520, p


def g_sterling():
    p = annulus_sector(300, 480, 190, 180, 84, 32, 90, 220)
    p.extend(quad((110, 300), (200, 300), (160, 60), (70, 60)))
    p.extend(bar(40, 480, 0, 38))
    p.extend(bar(60, 380, 280, 34))
    return 560, p


def g_yen():
    p = diag(280, 300, 80, 700, 60, 92)
    p.extend(diag(280, 300, 480, 700, 34, 34))
    p.extend(plain_stem(280, 0, 330, 90))
    p.extend(bar(80, 480, 200, 34))
    p.extend(bar(80, 480, 320, 34))
    return 560, p


def g_euro():
    p = annulus_sector(330, 350, 270, 330, 90, 32, 40, 320)
    p.extend(bar(30, 420, 260, 32))
    p.extend(bar(30, 400, 380, 32))
    return 620, p


def g_florin():
    p = serif_stem(200, -120, 560, top=False, bottom=False)
    p.extend(annulus_sector(300, 560, 140, 140, 84, 36, 90, 180))
    p.extend(annulus_sector(100, -120, 140, 120, 84, 36, 270, 360))
    p.extend(bar(60, 380, 444, 36))
    return 460, p


def g_ellipsis():
    p = dot(140, 52, 52).extend(dot(440, 52, 52)).extend(dot(740, 52, 52))
    return 900, p


def g_micro():
    p = plain_stem(110, -200, 480, 88)
    p.extend(serif_stem(450, 0, 480, top=False))
    from .lowercase import _n_shoulder
    sh = _n_shoulder(154, 406, 494)
    p.extend(sh.transformed(lambda t: (t[0], 480 - t[1])).orient_ccw())
    return 560, p


PUNCT = {
    ".": g_period, ",": g_comma, ":": g_colon, ";": g_semicolon,
    "!": g_exclam, "?": g_question, "'": g_quotesingle, '"': g_quotedbl,
    "\u2018": g_quoteleft, "\u2019": g_quoteright,
    "\u201c": g_quotedblleft, "\u201d": g_quotedblright,
    "-": g_hyphen, "\u2013": g_endash, "\u2014": g_emdash,
    "(": g_parenleft, ")": g_parenright, "[": g_bracketleft, "]": g_bracketright,
    "/": g_slash, "\\": g_backslash, "*": g_asterisk,
    "+": g_plus, "\u2212": g_minus, "=": g_equal, "<": g_less, ">": g_greater,
    "#": g_numbersign, "$": g_dollar, "%": g_percent, "&": g_ampersand,
    "@": g_at, "_": g_underscore,
    "\u00a1": g_exclamdown, "\u00bf": g_questiondown,
    "\u00ab": g_guillemotleft, "\u00bb": g_guillemotright,
    "\u00b0": g_degree, "\u2022": g_bullet,
    "\u2020": g_dagger, "\u2021": g_daggerdbl,
    "\u00a7": g_section, "\u00b6": g_paragraph,
    "\u00a9": g_copyright, "\u00ae": g_registered,
    "\u00a2": g_cent, "\u00a3": g_sterling, "\u00a5": g_yen, "\u20ac": g_euro,
    "\u0192": g_florin, "\u2026": g_ellipsis, "\u00b5": g_micro,
}
