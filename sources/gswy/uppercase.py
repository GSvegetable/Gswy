"""大写字母字形。"""
from .path import Path, ring, annulus_sector, rect
from .parts import serif_stem, bar, diag
from . import params as P

CAP, CSTEM, CTHIN = P.CAP, P.CSTEM, P.CTHIN
CE = 36  # 大写衬线外伸


def _stem(cx, y0=0, y1=CAP, **kw):
    kw.setdefault("ext", CE)
    kw.setdefault("w", CSTEM)
    return serif_stem(cx, y0, y1, **kw)


def g_H():
    p = _stem(130).extend(_stem(590))
    p.extend(bar(168, 552, 330, CTHIN))
    return 720, p


def g_I():
    return 340, _stem(170)


def g_E():
    p = _stem(130)
    p.extend(bar(80, 566, 664, 36))
    p.extend(rect(530, 616, 566, 700))
    p.extend(bar(180, 500, 330, 34))
    p.extend(rect(466, 300, 500, 398))
    p.extend(bar(80, 580, 0, 36))
    p.extend(rect(544, 0, 580, 84))
    return 620, p


def g_F():
    p = _stem(130)
    p.extend(bar(80, 566, 664, 36))
    p.extend(rect(530, 616, 566, 700))
    p.extend(bar(180, 500, 330, 34))
    p.extend(rect(466, 300, 500, 398))
    return 580, p


def g_L():
    p = _stem(130)
    p.extend(bar(80, 560, 0, 36))
    p.extend(rect(524, 0, 560, 84))
    return 560, p


def g_T():
    p = _stem(310, 0, 680, top=False)
    p.extend(bar(30, 590, 664, 36))
    p.extend(rect(30, 616, 66, 700))
    p.extend(rect(554, 616, 590, 700))
    return 620, p


def g_U():
    p = _stem(130, 200, CAP, bottom=False)
    p.extend(_stem(590, 200, CAP, bottom=False))
    p.extend(annulus_sector(360, 210, 280, 222, CSTEM, CTHIN, 180, 360))
    return 720, p


def g_N():
    p = _stem(120).extend(_stem(620))
    p.extend(diag(610, 20, 130, 680, 96, 96))
    return 740, p


def g_O():
    return 760, ring(380, 350, 330, 362, CSTEM, CTHIN)


def g_C():
    p = annulus_sector(360, 350, 310, 362, CSTEM, CTHIN, 40, 320)
    p.extend(rect(505, 556, 640, 600))
    return 680, p


def g_G():
    # 开口只在右上（-5°~40°），右侧下半保留圆环以便接竖桩
    p = annulus_sector(360, 350, 310, 362, CSTEM, CTHIN, -5, 320)
    p.extend(rect(505, 556, 640, 600))
    p.extend(rect(570, 170, 670, 360))
    p.extend(bar(470, 670, 326, 34))
    return 740, p


def g_D():
    p = _stem(130)
    p.extend(annulus_sector(330, 350, 340, 362, CSTEM, CTHIN, -90, 90))
    p.extend(bar(80, 340, 664, 36))
    p.extend(bar(80, 340, 0, 36))
    return 720, p


def g_B():
    p = _stem(130)
    p.extend(annulus_sector(330, 525, 270, 187, 96, 34, -90, 90))
    p.extend(annulus_sector(340, 175, 280, 187, 96, 34, -90, 90))
    p.extend(bar(80, 340, 664, 36))
    p.extend(bar(80, 340, 330, 34))
    p.extend(bar(80, 340, 0, 36))
    return 650, p


def g_P():
    p = _stem(130)
    p.extend(annulus_sector(330, 525, 280, 187, 96, 34, -90, 90))
    p.extend(bar(80, 340, 664, 36))
    p.extend(bar(80, 340, 330, 34))
    return 620, p


def g_R():
    p = _stem(130)
    p.extend(annulus_sector(330, 525, 280, 187, 96, 34, -90, 90))
    p.extend(bar(80, 340, 664, 36))
    p.extend(bar(80, 340, 330, 34))
    p.extend(diag(560, 0, 380, 340, 96, 60, ser_bot=True, ext=CE))
    return 680, p


def g_Q():
    p = ring(380, 350, 330, 362, CSTEM, CTHIN)
    p.extend(diag(700, -60, 500, 150, 80, 44))
    return 760, p


def g_S():
    from .lowercase import _s_shape
    return 580, _s_shape(295, 505, 225, 207, 280, 195, 240, 207, 92, 96, 34)


def g_V():
    p = diag(340, 0, 110, CAP, 44, 100, ser_top=True, ext=CE)
    p.extend(diag(340, 0, 570, CAP, 34, 34, ser_top=True, ext=CE))
    return 680, p


def g_W():
    p = diag(250, 0, 100, CAP, 48, 96, ser_top=True, ext=CE)
    p.extend(diag(250, 0, 480, CAP, 32, 32, ser_top=True, ext=CE))
    p.extend(diag(650, 0, 480, CAP, 48, 96, ser_top=True, ext=CE))
    p.extend(diag(650, 0, 830, CAP, 32, 32, ser_top=True, ext=CE))
    return 960, p


def g_X():
    p = diag(120, 0, 560, CAP, 100, 64, ser_top=True, ser_bot=True, ext=CE)
    p.extend(diag(560, 0, 120, CAP, 100, 34, ser_top=True, ser_bot=True, ext=CE))
    return 680, p


def g_Y():
    p = diag(320, 320, 100, CAP, 60, 96, ser_top=True, ext=CE)
    p.extend(diag(320, 320, 540, CAP, 34, 34, ser_top=True, ext=CE))
    p.extend(_stem(320, 0, 350, top=False))
    return 640, p


def g_Z():
    p = bar(50, 570, 664, 36)
    p.extend(rect(50, 616, 86, 700))
    p.extend(bar(50, 570, 0, 36))
    p.extend(rect(534, 0, 570, 84))
    p.extend(diag(110, 18, 510, 682, 104, 80))
    return 620, p


def g_K():
    p = _stem(130)
    p.extend(diag(580, 0, 160, 360, 96, 44, ser_bot=True, ext=CE))
    p.extend(diag(200, 320, 560, CAP, 88, 60, ser_top=True, ext=CE))
    return 700, p


def g_J():
    p = _stem(330, 120, CAP, bottom=False)
    p.extend(annulus_sector(210, 150, 170, 162, CSTEM, CTHIN, 180, 360))
    p.extend(rect(40, 150, 76, 214))
    return 460, p


def g_M():
    p = _stem(120).extend(_stem(760))
    p.extend(diag(440, 160, 150, 680, 92, 92))
    p.extend(diag(440, 160, 730, 680, 92, 92))
    return 880, p


def g_A():
    p = diag(120, 0, 340, CAP, 40, 34, ser_bot=True, ext=CE)
    p.extend(diag(560, 0, 340, CAP, 100, 96, ser_bot=True, ext=CE))
    p.extend(bar(200, 480, 220, 34))
    return 680, p


UPPER = {
    "A": g_A, "B": g_B, "C": g_C, "D": g_D, "E": g_E, "F": g_F,
    "G": g_G, "H": g_H, "I": g_I, "J": g_J, "K": g_K, "L": g_L,
    "M": g_M, "N": g_N, "O": g_O, "P": g_P, "Q": g_Q, "R": g_R,
    "S": g_S, "T": g_T, "U": g_U, "V": g_V, "W": g_W, "X": g_X,
    "Y": g_Y, "Z": g_Z,
}
