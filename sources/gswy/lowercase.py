"""小写字母字形。每个函数返回 (advance, Path)。"""
from .path import Path, ring, annulus_sector, rect, ellipse, quad
from .parts import serif_stem, plain_stem, bar, dot, shoulder
from . import params as P

XH, ASC, DESC, OV = P.XH, P.ASC, P.DESC, P.OV
STEM, THIN = P.STEM, P.THIN


def _n_shoulder(lx1, rx0, rx1, top=None):
    top = XH if top is None else top
    t = top + OV
    lx = lx1 - 14  # 咬入左竖笔，避免零宽搭接
    mid = (lx1 + rx1) / 2
    p = Path()
    p.moveTo((lx, 360))
    p.curveTo((lx, 448), (lx1 + 36, t), (mid + 10, t))
    p.curveTo((rx1 - 34, t), (rx1, top - 42), (rx1, 330))
    p.lineTo((rx1, 200))
    p.lineTo((rx0, 200))
    p.lineTo((rx0, 320))
    p.curveTo((rx0, 418), (rx0 - 38, t - 42), (mid, t - 42))
    p.curveTo((lx1 + 62, t - 42), (lx, 396), (lx, 250))
    p.closePath()
    return p.orient_ccw()


def g_n():
    p = serif_stem(110, 0, XH)
    p.extend(serif_stem(450, 0, 340, top=False))
    p.extend(_n_shoulder(154, 406, 494))
    return 560, p


def g_h():
    p = serif_stem(110, 0, ASC)
    p.extend(serif_stem(450, 0, 340, top=False))
    p.extend(_n_shoulder(154, 406, 494))
    return 560, p


def g_m():
    p = serif_stem(100, 0, XH)
    p.extend(serif_stem(420, 0, 340, top=False))
    p.extend(serif_stem(740, 0, 340, top=False))
    p.extend(_n_shoulder(144, 376, 464))
    p.extend(_n_shoulder(464, 696, 784))
    return 850, p


def g_o():
    return 540, ring(270, 240, 230, 252, STEM, THIN)


def g_b():
    p = serif_stem(110, 0, ASC)
    p.extend(ring(300, 240, 215, 252, STEM, THIN))
    return 550, p


def g_d():
    p = serif_stem(440, 0, ASC)
    p.extend(ring(250, 240, 215, 252, STEM, THIN))
    return 550, p


def g_p():
    p = serif_stem(110, DESC, XH)
    p.extend(ring(300, 240, 215, 252, STEM, THIN))
    return 550, p


def g_q():
    p = serif_stem(440, DESC, XH)
    p.extend(ring(250, 240, 215, 252, STEM, THIN))
    return 550, p


def g_u():
    p = serif_stem(450, 0, XH)
    p.extend(serif_stem(110, 140, XH, bottom=False))
    sh = _n_shoulder(154, 406, 494)
    sh = sh.transformed(lambda pt: (pt[0], XH - pt[1])).orient_ccw()
    p.extend(sh)
    return 560, p


def g_i():
    p = serif_stem(140, 0, XH)
    p.extend(dot(140, 600))
    return 280, p


def g_l():
    return 280, serif_stem(140, 0, ASC)


def g_j():
    p = serif_stem(206, -100, XH, bottom=False)
    p.extend(annulus_sector(130, -100, 120, 120, STEM, 40, 270, 360))
    p.extend(dot(206, 600))
    return 300, p


def g_t():
    p = serif_stem(140, 110, 620, bottom=False, top_ext=26)
    p.extend(annulus_sector(230, 110, 134, 110, STEM, 36, 180, 270))
    p.extend(bar(24, 292, 444, 36))
    return 340, p


def g_f():
    p = serif_stem(130, 0, 600, top=False)
    p.extend(annulus_sector(230, 600, 144, 140, STEM, 40, 90, 180))
    p.extend(bar(24, 282, 444, 36))
    return 320, p


def g_r():
    p = serif_stem(110, 0, XH)
    p.extend(annulus_sector(250, 330, 140, 152, 80, 42, 55, 185))
    p.extend(rect(300, 400, 356, 462))
    return 400, p


def g_c():
    p = annulus_sector(255, 240, 215, 252, STEM, THIN, 40, 320)
    p.extend(rect(352, 380, 448, 414))
    return 480, p


def g_e():
    p = annulus_sector(260, 240, 220, 252, STEM, THIN, -2, 320)
    p.extend(quad((44, 268), (479, 268), (473, 302), (44, 302)))
    return 520, p


def g_a():
    p = serif_stem(430, 0, 440, top=False)
    p.extend(ring(245, 165, 205, 177, 84, THIN))
    p.extend(annulus_sector(265, 330, 185, 162, 78, 36, 40, 200))
    return 520, p


def g_g():
    p = ring(255, 250, 205, 240, 84, THIN)
    p.extend(serif_stem(450, -100, XH, bottom=False, top_ext=28))
    p.extend(annulus_sector(360, -100, 134, 120, STEM, 40, 270, 360))
    return 540, p


def g_s():
    return 440, _s_shape(225, 350, 165, 142, 215, 130, 175, 142, 76, 80, THIN)


def _s_shape(cxt, cyt, rxt, ryt, cxb, cyb, rxb, ryb, ws_t, ws_b, wt):
    """S/s：上钩 + 下钩 + 显式脊柱 + 两端衬线。"""
    import math
    p = annulus_sector(cxt, cyt, rxt, ryt, ws_t, wt, 28, 230)
    p.extend(annulus_sector(cxb, cyb, rxb, ryb, ws_b, wt, 200, 420))

    def rad(cx, cy, rx, ry, a):
        ar = math.radians(a)
        return (cx + rx * math.cos(ar), cy + ry * math.sin(ar))

    # 脊柱：上钩外缘(230°)连下钩内缘(60°)，上钩内缘连下钩外缘
    to = rad(cxt, cyt, rxt, ryt, 230)
    ti = rad(cxt, cyt, rxt - ws_t, ryt - wt, 230)
    bo = rad(cxb, cyb, rxb, ryb, 60)
    bi = rad(cxb, cyb, rxb - ws_b, ryb - wt, 60)
    p.extend(quad(to, bi, bo, ti))
    # 两端衬线：置于切口中点，保证与笔画重叠
    t_out = rad(cxt, cyt, rxt, ryt, 28)
    t_in = rad(cxt, cyt, rxt - ws_t, ryt - wt, 28)
    tm = ((t_out[0] + t_in[0]) / 2, (t_out[1] + t_in[1]) / 2)
    p.extend(rect(tm[0] - 46, tm[1] - 19, tm[0] + 46, tm[1] + 19))
    b_out = rad(cxb, cyb, rxb, ryb, 200)
    b_in = rad(cxb, cyb, rxb - ws_b, ryb - wt, 200)
    bm = ((b_out[0] + b_in[0]) / 2, (b_out[1] + b_in[1]) / 2)
    p.extend(rect(bm[0] - 48, bm[1] - 19, bm[0] + 48, bm[1] + 19))
    return p


def g_v():
    from .parts import diag
    p = diag(250, 0, 105, XH, 58, 90, ser_top=True)
    p.extend(diag(250, 0, 395, XH, 30, 30, ser_top=True))
    return 500, p


def g_w():
    from .parts import diag
    p = diag(185, 0, 80, XH, 54, 84, ser_top=True)
    p.extend(diag(185, 0, 330, XH, 30, 30, ser_top=True))
    p.extend(diag(455, 0, 330, XH, 54, 84, ser_top=True))
    p.extend(diag(455, 0, 575, XH, 30, 30, ser_top=True))
    return 660, p


def g_x():
    from .parts import diag
    p = diag(110, 0, 390, XH, 88, 60, ser_top=True, ser_bot=True)
    p.extend(diag(390, 0, 110, XH, 88, 30, ser_top=True, ser_bot=True))
    return 500, p


def g_y():
    from .parts import diag
    p = diag(250, 0, 105, XH, 58, 90, ser_top=True)
    p.extend(diag(160, -150, 395, XH, 56, 30, ser_top=True))
    p.extend(annulus_sector(70, -150, 134, 70, 90, 30, 270, 360))
    return 500, p


def g_k():
    from .parts import diag
    p = serif_stem(110, 0, ASC)
    p.extend(diag(420, 0, 150, 340, 88, 44, ser_bot=True))
    p.extend(diag(190, 300, 400, XH, 76, 56, ser_top=True))
    return 530, p


def g_z():
    p = bar(40, 420, 444, 36)
    p.extend(bar(40, 420, 0, 36))
    from .parts import diag
    p.extend(diag(95, 18, 370, 462, 96, 72))
    return 460, p


LOWER = {
    "a": g_a, "b": g_b, "c": g_c, "d": g_d, "e": g_e, "f": g_f,
    "g": g_g, "h": g_h, "i": g_i, "j": g_j, "k": g_k, "l": g_l,
    "m": g_m, "n": g_n, "o": g_o, "p": g_p, "q": g_q, "r": g_r,
    "s": g_s, "t": g_t, "u": g_u, "v": g_v, "w": g_w, "x": g_x,
    "y": g_y, "z": g_z,
}
