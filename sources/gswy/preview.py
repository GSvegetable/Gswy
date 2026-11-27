"""渲染预览：用 Pillow 渲染 TTF 生成自检 PNG。"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TTF = os.path.join(ROOT, "fonts", "GswySerif-Regular.ttf")
OUT = os.path.join(ROOT, "preview")


def render_lines(lines, sizes, out, width=1600):
    os.makedirs(OUT, exist_ok=True)
    pad = 40
    imgs = []
    total_h = pad
    for text, size in zip(lines, sizes):
        font = ImageFont.truetype(TTF, size)
        img = Image.new("RGB", (width, int(size * 1.6)), "white")
        d = ImageDraw.Draw(img)
        d.text((pad, size * 0.25), text, font=font, fill="black")
        imgs.append(img)
        total_h += img.height
    canvas = Image.new("RGB", (width, total_h + pad), "white")
    y = pad
    for im in imgs:
        canvas.paste(im, (0, y))
        y += im.height
    path = os.path.join(OUT, out)
    canvas.save(path)
    print("MEDIA:" + path)


def render_grid(chars, size, out, cols=10):
    os.makedirs(OUT, exist_ok=True)
    font = ImageFont.truetype(TTF, size)
    cell_w, cell_h = int(size * 1.3), int(size * 1.5)
    rows = (len(chars) + cols - 1) // cols
    img = Image.new("RGB", (cell_w * cols, cell_h * rows), "white")
    d = ImageDraw.Draw(img)
    for i, ch in enumerate(chars):
        x = (i % cols) * cell_w
        y = (i // cols) * cell_h
        d.rectangle([x, y, x + cell_w - 1, y + cell_h - 1], outline="#dddddd")
        d.text((x + cell_w * 0.15, y + cell_h * 0.1), ch, font=font, fill="black")
    path = os.path.join(OUT, out)
    img.save(path)
    print("MEDIA:" + path)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "sample"
    if mode == "sample":
        render_lines(
            ["Hamburgefonstiv", "HOIEA nioae sg", "The quick brown fox jumps over the lazy dog.",
             "Sphinx of black quartz, judge my vow. 0123456789"],
            [110, 110, 48, 36], "样张.png")
    elif mode == "grid":
        chars = sys.argv[2] if len(sys.argv) > 2 else "abcdefghijklmnopqrstuvwxyz"
        render_grid(list(chars), 120, "网格.png")
