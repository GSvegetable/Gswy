# Gswy Serif

一款**完全原创的参数化衬线字体**（Regular 0.3.0）：所有字形由统一的 Python 笔画部件库（竖笔、衬线、碗形、拱形、斜笔）拼装生成，输出行业标准 UFO 设计源，并编译为 TTF / OTF / WOFF2 三种格式。

![样张](docs/样张.png)

## 设计定位

- **风格**：过渡风格衬线体（Transitional Serif），中等笔画粗细对比、括号形衬线（bracketed serifs），气质介于书卷气与现代感之间
- **用途**：标题与正文兼顾的通用型西文字体
- **度量**：UPM 1000 · 大写字高 700 · x 高 480 · 主干 88 / 细笔 30
- **字符集**：208 字形 —— 大小写字母、等高数字、常用标点与符号、Latin-1 重音字母、æ œ ß ø Ð Þ 等扩展字母
- **字距**：内置 47 组 OpenType GPOS kerning 对（T/V/W/Y/A 等经典组合）
- **许可**：SIL Open Font License 1.1（可自由使用、嵌入、修改与再分发）

## 快速使用

字体成品在 `fonts/`：

| 文件 | 用途 |
| --- | --- |
| `GswySerif-Regular.ttf` | 桌面安装（Windows / macOS / Linux） |
| `GswySerif-Regular.otf` | 桌面安装 / 专业排版软件（CFF 轮廓） |
| `GswySerif-Regular.woff2` | 网页 `@font-face` |

网页用法：

```css
@font-face {
  font-family: "Gswy Serif";
  src: url("fonts/GswySerif-Regular.woff2") format("woff2");
}
body { font-family: "Gswy Serif", Georgia, serif; }
```

打开 `specimen/index.html` 可查看完整字体样张页；打开 `font-lab/index.html` 可进入独立的 **Gswy Font Lab 字体实验室**，实时输入文字并调整字号、行距与字距。

## 从源码构建

依赖：Python 3.10+ 与 `fonttools`（含 brotli，用于 WOFF2）。

```bash
pip install fonttools brotli
./build.sh          # 或 python3 -m sources.gswy.build
```

构建产物：`fonts/`（三种格式）+ `ufo/GswySerif-Regular.ufo`（设计源）。

渲染自检预览（可选，需 Pillow）：

```bash
python3 -m sources.gswy.preview sample
python3 -m sources.gswy.preview grid abcdefghijklmnopqrstuvwxyz
```

## 质量检查\n\n每次构建后运行源码与成品字体检查，核对必需字母、Unicode 映射、字形轮廓和 TTF / OTF / WOFF2 文件是否完整：\n\n```bash\npython3 -m sources.gswy.qa\n```\n\nGitHub Actions 会在推送到主分支、开发分支或提交 Pull Request 时自动构建并执行同一套检查，并将通过检查的 TTF / OTF / WOFF2 与字形检查 PNG 发布为 `gswy-serif-build` 构建产物。`build-font-assets.yml` 还会在分支推送后同步更新仓库内的字体成品、UFO 源和样张图。\n\n## 仓库结构

```
sources/gswy/
  params.py       全局设计参数（度量、笔画、衬线）
  path.py         贝塞尔轮廓工具（弧线、圆环、扇区、绕向规范化）
  parts.py        笔画部件库（衬线竖笔、斜笔、横杠、点）
  lowercase.py    小写字母
  uppercase.py    大写字母
  figures.py      数字
  punctuation.py  标点与符号
  accents.py      重音符号与组合字形
  build.py        构建管线（UFO / TTF / OTF / WOFF2 / GPOS kerning）
  preview.py      渲染自检
ufo/              UFO 设计源（可在 FontForge / Glyphs 等工具中继续编辑）
fonts/            字体成品
specimen/         样张展示页
docs/             设计定稿
```

## 工程要点

- **统一部件库**：改一个参数（如衬线高度、主干粗细），全族字形联动更新
- **轮廓约定**：实心部件统一采用逆时针方向，字腔使用反向轮廓；质量检查会验证字形注册、轮廓基本结构与成品字体字符映射
- **字体命名**：标点与符号使用 Adobe Glyph List 标准字形名，避免把可见字符直接当作 PostScript 字形名
- **可编辑源**：UFO 源文件随仓库发布，任何字体编辑器都能接手继续打磨

## 路线图

- [x] Regular 字重 · 208 字形 · 三种格式
- [ ] 造型二轮打磨（a/g/s/y 等曲线细节、小字号 hinting）
- [ ] Bold 字重（部件参数联动加粗）
- [ ] Italic 斜体
- [ ] 扩展字符集（Latin Extended-A、更多货币与排版符号）

## 许可

Copyright 2026 The Gswy Serif Project Authors.
本项目字体软件采用 [SIL Open Font License 1.1](LICENSE) 授权。
