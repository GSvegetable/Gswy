"""数字字形（等高数字，字高 660，等宽 560）。"""
from .path import ring, annulus_sector, rect, quad
from .parts import serif_stem, plain_stem, bar, diag
from . import params as P

DH = 660


def g_zero():
    return 560, ring(280, 330, 220, 342, 90, 32)


def g_one():
    p = serif_stem(300, 0, DH, top=False, bot_ext=95)
    p.extend(diag(150, 480, 290, 640, 64, 80))
    return 560, p


def g_two():
    # 上半碗从右下绕过顶部回到左上，随后以斜干落向基线。
    p = annulus_sector(280, 470, 210, 190, 90, 32, 340, 515)
    p.extend(rect(60, 520, 150, 560))
    p.extend(diag(120, 18, 460, 400, 100, 80))
    p.extend(bar(60, 500, 0, 36))
    return 560, p


def g_three():
    # 上下两个右向碗形以右侧弧干相连，左侧保留清晰的开口端。
    p = annulus_sector(265, 495, 195, 165, 88, 32, 20, 160)
    p.extend(annulus_sector(265, 165, 205, 175, 90, 32, 200, 340))
    p.extend(rect(60, 520, 155, 560))
    p.extend(rect(60, 85, 155, 125))
    p.extend(rect(425, 105, 465, 555))
    return 560, p


def g_four():
    p = diag(100, 180, 390, DH, 84, 60)
    p.extend(bar(50, 520, 160, 36))
    p.extend(serif_stem(390, 0, DH, top=False))
    return 560, p


def g_five():
    p = bar(80, 480, 624, 36)
    p.extend(plain_stem(110, 180, DH, 88))
    # 下半碗从左中段向右下展开，避免与 6 的闭合轮廓混淆。
    p.extend(annulus_sector(270, 190, 210, 190, 90, 32, 180, 360))
    p.extend(rect(80, 560, 170, 660))
    return 560, p


def g_six():
    p = ring(280, 190, 210, 200, 90, 32)
    p.extend(annulus_sector(330, 400, 250, 290, 88, 32, 90, 195))
    p.extend(rect(290, 640, 380, 680))
    return 560, p


def g_seven():
    p = bar(60, 500, 624, 36)
    p.extend(rect(60, 560, 100, 660))
    p.extend(diag(200, 0, 460, 624, 96, 80))
    return 560, p


def g_eight():
    p = ring(280, 500, 185, 172, 88, 32)
    p.extend(ring(280, 175, 205, 187, 90, 32))
    return 560, p


def g_nine():
    p = ring(280, 470, 210, 200, 90, 32)
    p.extend(annulus_sector(230, 260, 250, 290, 88, 32, 270, 375))
    p.extend(rect(180, -20, 270, 20))
    return 560, p


FIGURES = {
    "0": g_zero, "1": g_one, "2": g_two, "3": g_three, "4": g_four,
    "5": g_five, "6": g_six, "7": g_seven, "8": g_eight, "9": g_nine,
}
