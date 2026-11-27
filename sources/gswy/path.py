"""轮廓路径工具：三次贝塞尔轮廓的构建、变换与回放。

约定：外轮廓逆时针（PostScript 方向），内孔顺时针。
重叠部件依靠非零环绕规则自然并集——因此所有实心部件必须同为逆时针。
"""
import math

K = 0.5522847498  # 圆的贝塞尔逼近常数


def pt(x, y):
    return (float(x), float(y))


def contour_area(c):
    pts = [seg[-1] for seg in c]
    s = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        s += x1 * y2 - x2 * y1
    return s / 2


class Path:
    def __init__(self):
        self.contours = []
        self._cur = None

    # ---- 构建 ----
    def moveTo(self, p):
        self._cur = [("m", pt(*p))]
        self.contours.append(self._cur)
        return self

    def lineTo(self, p):
        self._cur.append(("l", pt(*p)))
        return self

    def curveTo(self, p1, p2, p3):
        self._cur.append(("c", pt(*p1), pt(*p2), pt(*p3)))
        return self

    def closePath(self):
        self._cur = None
        return self

    # ---- 回放 ----
    def draw(self, pen):
        for c in self.contours:
            for seg in c:
                if seg[0] == "m":
                    pen.moveTo(seg[1])
                elif seg[0] == "l":
                    pen.lineTo(seg[1])
                else:
                    pen.curveTo(seg[1], seg[2], seg[3])
            pen.closePath()

    def drawPoints(self, pointPen):
        """UFO pointPen 适配（闭合轮廓：末段终点即起点）。"""
        for c in self.contours:
            start = c[0][1]
            segs = list(c[1:])
            if segs and segs[-1][-1] != start:
                segs.append(("l", start))
            pointPen.beginPath()
            for seg in segs:
                if seg[0] == "l":
                    pointPen.addPoint(seg[1], segmentType="line")
                else:
                    pointPen.addPoint(seg[1])
                    pointPen.addPoint(seg[2])
                    pointPen.addPoint(seg[3], segmentType="curve")
            pointPen.endPath()

    # ---- 变换 ----
    def transformed(self, fn):
        out = Path()
        for c in self.contours:
            nc = []
            for seg in c:
                nc.append(tuple([seg[0]] + [fn(p) for p in seg[1:]]))
            out.contours.append(nc)
        return out

    def translate(self, dx, dy=0):
        return self.transformed(lambda p: (p[0] + dx, p[1] + dy))

    def scale(self, sx, sy=None, cx=0, cy=0):
        if sy is None:
            sy = sx
        return self.transformed(
            lambda p: (cx + (p[0] - cx) * sx, cy + (p[1] - cy) * sy))

    def mirror_x(self, axis=0):
        return self.transformed(lambda p: (2 * axis - p[0], p[1]))

    def reverse(self):
        """反转所有轮廓方向。"""
        out = Path()
        for c in self.contours:
            start = c[0][1]
            segs = c[1:]
            nc = [("m", segs[-1][-1] if segs else start)]
            for i in range(len(segs) - 1, -1, -1):
                seg = segs[i]
                prev_end = segs[i - 1][-1] if i > 0 else start
                if seg[0] == "l":
                    nc.append(("l", prev_end))
                else:
                    nc.append(("c", seg[2], seg[1], prev_end))
            out.contours.append(nc)
        return out

    def orient_ccw(self):
        """把所有负面积（顺时针）轮廓翻正。仅用于实心部件路径。"""
        out = Path()
        for c in self.contours:
            if contour_area(c) < 0:
                single = Path()
                single.contours = [c]
                out.contours.extend(single.reverse().contours)
            else:
                out.contours.append(c)
        return out

    def extend(self, other):
        self.contours.extend(other.contours)
        return self

    def bounds(self):
        xs, ys = [], []
        for c in self.contours:
            for seg in c:
                for p in seg[1:]:
                    xs.append(p[0]); ys.append(p[1])
        return (min(xs), min(ys), max(xs), max(ys)) if xs else (0, 0, 0, 0)


def arc_points(cx, cy, rx, ry, a0, a1):
    """椭圆弧 a0→a1（度；a1>a0 逆时针）。返回 (起点, [(c1, c2, end), ...])。"""
    a0r, a1r = math.radians(a0), math.radians(a1)
    total = a1r - a0r
    n = max(1, math.ceil(abs(total) / (math.pi / 2 + 1e-9)))
    step = total / n
    alpha = 4.0 / 3.0 * math.tan(step / 4.0)

    def P(a):
        return (cx + rx * math.cos(a), cy + ry * math.sin(a))

    def D(a):
        return (-rx * math.sin(a), ry * math.cos(a))

    start = P(a0r)
    segs = []
    for i in range(n):
        t0 = a0r + i * step
        t1 = t0 + step
        p0, p1 = P(t0), P(t1)
        d0, d1 = D(t0), D(t1)
        c1 = (p0[0] + alpha * d0[0], p0[1] + alpha * d0[1])
        c2 = (p1[0] - alpha * d1[0], p1[1] - alpha * d1[1])
        segs.append((c1, c2, p1))
    return start, segs


def append_arc(path, cx, cy, rx, ry, a0, a1, move=False):
    start, segs = arc_points(cx, cy, rx, ry, a0, a1)
    if move:
        path.moveTo(start)
    else:
        path.lineTo(start)
    for c1, c2, p in segs:
        path.curveTo(c1, c2, p)
    return path


def ellipse(cx, cy, rx, ry, clockwise=False):
    p = Path()
    if not clockwise:
        append_arc(p, cx, cy, rx, ry, 0, 360, move=True)
    else:
        append_arc(p, cx, cy, rx, ry, 360, 0, move=True)
    p.closePath()
    return p


def ring(cx, cy, rx, ry, w_side, w_top):
    """带粗细对比的圆环：左右厚 w_side，上下厚 w_top。外逆时针，内顺时针。"""
    p = ellipse(cx, cy, rx, ry)
    p.extend(ellipse(cx, cy, rx - w_side, ry - w_top, clockwise=True))
    return p


def annulus_sector(cx, cy, rx, ry, w_side, w_top, a0, a1):
    """圆环扇区（CCW 从 a0 到 a1，a1>a0），两端平切。用于 c e G S 等。"""
    p = Path()
    append_arc(p, cx, cy, rx, ry, a0, a1, move=True)
    append_arc(p, cx, cy, rx - w_side, ry - w_top, a1, a0)
    p.closePath()
    return p


def rect(x0, y0, x1, y1):
    p = Path()
    p.moveTo((x0, y0)).lineTo((x1, y0)).lineTo((x1, y1)).lineTo((x0, y1)).closePath()
    return p


def quad(p0, p1, p2, p3):
    """实心四边形，自动保证逆时针。"""
    p = Path()
    p.moveTo(p0).lineTo(p1).lineTo(p2).lineTo(p3).closePath()
    return p.orient_ccw()
