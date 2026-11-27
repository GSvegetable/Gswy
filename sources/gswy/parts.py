"""笔画部件库：衬线竖笔、拱形、斜笔、横杠、点。

所有部件外轮廓逆时针。部件之间允许重叠，靠非零环绕规则并集。
"""
from .path import Path, append_arc, rect, quad, ellipse, ring, annulus_sector
from . import params as P


def serif_stem(cx, y0, y1, w=None, top=True, bottom=True,
               ext=None, sh=None, br=None, top_ext=None, bot_ext=None):
    """带 bracketed 衬线的竖笔。cx 为中心，y0/y1 为上下端（含衬线面）。
    top/bottom: True 全衬线；False 平切；'left'/'right' 单侧衬线。"""
    w = P.STEM if w is None else w
    ext = P.SER_EXT if ext is None else ext
    sh = P.SER_H if sh is None else sh
    br = P.SER_BR if br is None else br
    x0, x1 = cx - w / 2, cx + w / 2
    te = ext if top_ext is None else top_ext
    be = ext if bot_ext is None else bot_ext
    tip = P.SER_TIP

    def sides(mode):
        if mode is True:
            return (True, True)
        if mode == "left":
            return (True, False)
        if mode == "right":
            return (False, True)
        return (False, False)

    tl, tr = sides(top)
    bl, brt = sides(bottom)
    p = Path()
    # 从左下角起，逆时针
    if bl:
        p.moveTo((x0 - be, y0))
    else:
        p.moveTo((x0, y0))
    # 底边 → 右下
    if brt:
        p.lineTo((x1 + be, y0))
        p.lineTo((x1 + be, y0 + sh - tip))
        p.lineTo((x1 + br, y0 + sh))
        p.curveTo((x1 + br * 0.42, y0 + sh), (x1, y0 + sh + br * 0.42),
                  (x1, y0 + sh + br))
    else:
        p.lineTo((x1, y0))
    # 右缘上行
    if tr:
        p.lineTo((x1, y1 - sh - br))
        p.curveTo((x1, y1 - sh - br * 0.42), (x1 + br * 0.42, y1 - sh),
                  (x1 + br, y1 - sh))
        p.lineTo((x1 + te, y1 - sh + tip))
        p.lineTo((x1 + te, y1))
    else:
        p.lineTo((x1, y1))
    # 顶边 → 左上
    if tl:
        p.lineTo((x0 - te, y1))
        p.lineTo((x0 - te, y1 - sh + tip))
        p.lineTo((x0 - br, y1 - sh))
        p.curveTo((x0 - br * 0.42, y1 - sh), (x0, y1 - sh - br * 0.42),
                  (x0, y1 - sh - br))
    else:
        p.lineTo((x0, y1))
    # 左缘下行
    if bl:
        p.lineTo((x0, y0 + sh + br))
        p.curveTo((x0, y0 + sh + br * 0.42), (x0 - br * 0.42, y0 + sh),
                  (x0 - br, y0 + sh))
        p.lineTo((x0 - be, y0 + sh - tip))
    else:
        p.lineTo((x0, y0))
    p.closePath()
    return p.orient_ccw()


def plain_stem(cx, y0, y1, w=None):
    w = P.STEM if w is None else w
    return rect(cx - w / 2, y0, cx + w / 2, y1)


def bar(x0, x1, y, h=None, tilt=0):
    """横杠（H 横杠、e 横杠等）。tilt>0 时右端抬高。"""
    h = P.THIN if h is None else h
    return quad((x0, y), (x1, y + tilt), (x1, y + tilt + h), (x0, y + h))


def dot(cx, cy, r=None, squash=0.92):
    """i/j 的点、句号：略扁的圆点。"""
    r = P.STEM * 0.62 if r is None else r
    return ellipse(cx, cy, r, r * squash)


def diag(x0, y0, x1, y1, w0, w1, ser_top=None, ser_bot=None,
         ext=None, sh=None):
    """斜笔：从顶端 (x1,y1) 到底端 (x0,y0)，宽度过渡 w1→w0。
    宽度沿水平方向量取。ser_top/ser_bot: 端部水平衬线 (宽单侧外伸)。"""
    ext = P.SER_EXT if ext is None else ext
    sh = P.SER_H if sh is None else sh
    p = Path()
    bl, br = x0 - w0 / 2, x0 + w0 / 2
    tl, tr = x1 - w1 / 2, x1 + w1 / 2
    if ser_bot:
        e = ext if ser_bot is True else ser_bot
        p.moveTo((bl - e, y0))
        p.lineTo((br + e, y0))
        p.lineTo((br + e, y0 + sh - P.SER_TIP))
        p.lineTo((br + 6, y0 + sh))
        p.lineTo((tr, y1) if not ser_top else (tr, y1 - sh))
    else:
        p.moveTo((bl, y0))
        p.lineTo((br, y0))
        p.lineTo((tr, y1) if not ser_top else (tr, y1 - sh))
    if ser_top:
        e = ext if ser_top is True else ser_top
        p.lineTo((tr + e, y1 - sh))
        p.lineTo((tr + e, y1 - P.SER_TIP))
        p.lineTo((tl - e, y1 - P.SER_TIP))
        p.lineTo((tl - e, y1 - sh))
        p.lineTo((tl, y1 - sh))
        p.lineTo((bl, y0) if not ser_bot else (bl - 6, y0 + sh))
    else:
        p.lineTo((tl, y1))
        p.lineTo((bl, y0) if not ser_bot else (bl - 6, y0 + sh))
    if ser_bot:
        e = ext if ser_bot is True else ser_bot
        p.lineTo((bl - e, y0 + sh))
        p.lineTo((bl - e, y0 + sh - P.SER_TIP))
    p.closePath()
    return p.orient_ccw()


def shoulder(lx1, rx0, rx1, y_top, y_join_out, y_join_in, w_thin=None,
             ov=None):
    """n/h/m 的拱肩：从左竖笔右缘 lx1 出发，越过顶部到右竖笔。
    返回拱形轮廓（不含右竖笔下半段）。
    y_join_out: 外侧曲线落到右竖笔右缘的高度；
    y_join_in: 内侧曲线回到左竖笔右缘的高度。"""
    wt = P.THIN + 14 if w_thin is None else w_thin
    ov = P.OV if ov is None else ov
    top = y_top + ov
    mid = (lx1 + rx0) / 2
    p = Path()
    p.moveTo((lx1, y_join_in))
    # 外侧：左上 → 顶 → 右
    p.curveTo((lx1, y_top - 40), (lx1 + 30, top), (mid + 20, top))
    p.curveTo((rx1 - 30, top), (rx1, top - 60), (rx1, y_join_out))
    # 沿右缘下行一点再折回内侧（与右竖笔重叠）
    p.lineTo((rx1, y_join_out - 60))
    p.lineTo((rx0, y_join_out - 60))
    p.lineTo((rx0, y_join_out - 20))
    # 内侧：右 → 顶下 wt → 左
    p.curveTo((rx0, top - wt - 40), (rx0 - 40, top - wt), (mid + 10, top - wt))
    p.curveTo((lx1 + 60, top - wt), (lx1, y_top - 90), (lx1, y_join_in - 0))
    p.closePath()
    return p


def bowl_join_stem(cx, y0, y1, w=None, **kw):
    """b/d/p/q 的主干（全衬线竖笔别名）。"""
    return serif_stem(cx, y0, y1, w=w, **kw)
