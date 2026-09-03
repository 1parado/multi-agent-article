# -*- coding: utf-8 -*-
"""gen_covers.py — v5 期刊封面生成器（程序化，arXiv 编号为随机种子）。

输出 D:/multi-agent-article/covers/<arxiv>.png（1200×630）+ index.png，
另生成 apple-touch-icon.png（180×180）。复用 beautify_v4.PAPER/CAT_COLOR 元数据。
"""
import os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import beautify_v4 as V4  # noqa: E402  （其顶部会自行重包 stdout 为 UTF-8）

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

BASE = "D:/multi-agent-article/"
OUT = BASE + "covers/"

RED = "#A02C2C"
INK = "#1a1a1a"
CREAM = "#FAF7F2"
CREAM2 = "#F1ECE3"
LINE = "#E4DFD6"
SOFT = "#8a8a86"

FW = "C:/Windows/Fonts/msyh.ttc"
FWB = "C:/Windows/Fonts/msyhbd.ttc"
FMONO = "C:/Windows/Fonts/consola.ttf"
FMONOB = "C:/Windows/Fonts/consolab.ttf"
FALLBACK = "C:/Windows/Fonts/arial.ttf"


def font(path, size, bold=False):
    p = FWB if bold and path == FW else path
    for cand in (p, FALLBACK):
        try:
            return ImageFont.truetype(cand, size)
        except Exception:
            continue
    return ImageFont.load_default()


def wrap(draw, text, fnt, maxw):
    """按像素宽度折行（中英混排，按字符切）。"""
    lines, cur = [], ""
    for ch in text:
        if draw.textlength(cur + ch, font=fnt) <= maxw:
            cur += ch
        else:
            lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines


def draw_motif(d, box, seed, n, cat_color, size=1.0):
    """在 box=(x0,y0,x1,y1) 内画确定性点线网络。"""
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    pts = []
    for i in range(n):
        pts.append((x0 + w * (0.08 + 0.84 * rnd.random()),
                    y0 + h * (0.10 + 0.80 * rnd.random())))
    # 时间序连线（细灰）
    for i in range(n - 1):
        d.line([pts[i], pts[i + 1]], fill=LINE, width=2)
    # 全连接淡线（随机 40%）
    for i in range(n):
        for j in range(i + 1, n):
            if rnd.random() < 0.40:
                d.line([pts[i], pts[j]], fill="#EFE9DF", width=1)
    r = 7 * size
    for i, (x, y) in enumerate(pts):
        fill = cat_color if i % 3 == 0 else (INK if i % 3 == 1 else RED)
        d.ellipse([x - r, y - r, x + r, y + r], fill=fill, outline=CREAM, width=2)
    # 起终点强调
    sx, sy = pts[0]
    d.ellipse([sx - r - 4, sy - r - 4, sx + r + 4, sy + r + 4], outline=RED, width=2)


def render(arxiv, number, zh, en, cat, seed_extra, index=False):
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    cat_color = V4.CAT_COLOR.get(cat, RED)
    seed = int("".join(ch for ch in (arxiv + str(seed_extra)) if ch.isdigit())) % (2 ** 31)

    # 纸本底纹（细横线）
    for yy in range(0, H, 14):
        d.line([(0, yy), (W, yy)], fill="#F6F1E8", width=1)
    # 边框：外细 + 内红
    d.rectangle([16, 16, W - 16, H - 16], outline=LINE, width=2)
    d.rectangle([24, 24, W - 24, H - 24], outline=RED, width=2)

    # 右上巨型幽灵编号
    f_ghost = font(FWB, 240, bold=True)
    d.text((W - 80, -52), number, font=f_ghost, fill="#EFE6DA", anchor="rt")

    # 顶栏 eyebrow
    f_eye = font(FMONO, 21, bold=False)
    top = "INDEX · VOL.1" if index else ("PAPER DIGEST · VOL.1 · Nº " + number)
    d.text((56, 52), top, font=f_eye, fill=RED, anchor="ls")

    # 中文题名（红色主标题，两行内）
    f_zh = font(FWB, 62, bold=True)
    lines = wrap(d, zh, f_zh, 840)
    if len(lines) > 2:
        f_zh = font(FWB, 50, bold=True)
        lines = wrap(d, zh, f_zh, 840)
    yy = 250 if len(lines) == 1 else 218
    for ln in lines:
        d.text((56, yy), ln, font=f_zh, fill=INK, anchor="ls")
        yy += 74

    # 英文题名（mono）
    f_en = font(FMONO, 24)
    en_lines = wrap(d, en, f_en, 840)
    yy += 16
    for ln in en_lines[:2]:
        d.text((56, yy), ln, font=f_en, fill=SOFT, anchor="ls")
        yy += 38

    # 右侧拓扑点线（在标题/幽灵编号之间区域）
    motif = (900, 60, 1140, 300)
    draw_motif(d, motif, seed, 9 if not index else 11, cat_color)

    # 底部信息条
    f_mono = font(FMONO, 17)
    f_cjk = font(FW, 16)
    bot1 = "ARXIV " + arxiv if not index else "11 PAPERS · arXiv 2509 – 2609"
    cat_cn = V4.CAT_CN.get(cat, "")
    d.text((56, H - 78), bot1, font=f_mono, fill=INK, anchor="ls")
    d.text((56, H - 50), "1parado.github.io/multi-agent-article", font=f_mono, fill=SOFT, anchor="ls")
    if not index:
        d.rectangle([1150 - 220, H - 92, 1150, H - 56], outline=cat_color, width=2)
        d.line([(1150 - 220, H - 92), (1150 - 220 + 34, H - 58)], fill=cat_color, width=2)
        d.text((1150 - 100, H - 74), cat_cn, font=f_cjk, fill=cat_color, anchor="ms")
    else:
        d.text((1150, H - 50), "MULTI-AGENT · 2026", font=f_mono, fill=RED, anchor="rs")

    img.save(OUT + (arxiv + ".png" if not index else "index.png"), "PNG", optimize=True)
    print("cover:", "index.png" if index else arxiv + ".png", "seed", seed)


def apple_icon():
    S = 180
    img = Image.new("RGB", (S, S), RED)
    d = ImageDraw.Draw(img)
    # 内边框
    d.rounded_rectangle([10, 10, S - 10, S - 10], radius=28, outline="#ffffff", width=5)
    # planner（左大方点）→ 三个 agent（右侧小点）
    px, py = 52, S // 2
    agents = [(112, 58), (116, S // 2), (112, S - 58)]
    for ax, ay in agents:
        d.line([(px + 16, py), (ax - 18, ay)], fill="#ffffff", width=4)
    d.rounded_rectangle([px - 22, py - 22, px + 22, py + 22], radius=12, fill="#ffffff")
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED)
    for ax, ay in agents:
        d.ellipse([ax - 15, ay - 15, ax + 15, ay + 15], fill="#ffffff", outline=RED, width=3)
        d.ellipse([ax - 5, ay - 5, ax + 5, ay + 5], fill=RED)
    img.save(BASE + "apple-touch-icon.png", "PNG", optimize=True)
    print("apple-touch-icon.png 180x180")


def render_static(title_zh, title_en, file, accent="#A02C2C"):
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    for yy in range(0, H, 14):
        d.line([(0, yy), (W, yy)], fill="#F6F1E8", width=1)
    d.rectangle([16, 16, W - 16, H - 16], outline=LINE, width=2)
    d.rectangle([24, 24, W - 24, H - 24], outline=accent, width=2)
    f_ghost = font(FWB, 240, bold=True)
    d.text((W - 80, -52), "§", font=f_ghost, fill="#EFE6DA", anchor="rt")
    f_eye = font(FMONO, 21)
    d.text((56, 52), "PAPER DIGEST · VOL.1 · STATIC PAGE", font=f_eye, fill=accent, anchor="ls")
    f_zh = font(FWB, 74, bold=True)
    lines = wrap(d, title_zh, f_zh, 900)
    if len(lines) > 2:
        f_zh = font(FWB, 56, bold=True)
        lines = wrap(d, title_zh, f_zh, 900)
    yy = 260 if len(lines) == 1 else 226
    for ln in lines:
        d.text((56, yy), ln, font=f_zh, fill=INK, anchor="ls")
        yy += 96
    f_en = font(FMONO, 24)
    en_lines = wrap(d, title_en, f_en, 900)
    yy += 14
    for ln in en_lines[:2]:
        d.text((56, yy), ln, font=f_en, fill=SOFT, anchor="ls")
        yy += 38
    f_mono = font(FMONO, 17)
    d.text((56, H - 50), "1parado.github.io/multi-agent-article", font=f_mono, fill=SOFT, anchor="ls")
    d.text((1150, H - 50), "MULTI-AGENT · 2026", font=f_mono, fill=accent, anchor="rs")
    img.save(OUT + file, "PNG", optimize=True)
    print("cover:", file)


ORDER = [
    # (arxiv, number, zh, cat, index_flag)
    ("2603.11445", "01", "VMAO：验证式多智能体编排", "Verified Multi-Agent Orchestration", "FRAMEWORK"),
    ("2602.16873", "02", "AdaptOrch：任务自适应拓扑编排", "Task-Adaptive Multi-Agent Orchestration", "FRAMEWORK"),
    ("2603.25723", "03", "NLAH：自然语言 Agent Harness", "Natural-Language Agent Harnesses", "HARNESS"),
    ("2603.28052", "04", "Meta-Harness：自动搜索最优 harness", "End-to-End Optimization of Model Harnesses", "HARNESS"),
    ("2606.03005", "05", "MUSE：面向多模态大模型的统一 Harness", "MUSE: A Unified Agentic Harness for MLLMs", "HARNESS"),
    ("2608.27338", "06", "MoRe：把多角色协同压进单次推理", "MoRe: Mixture of Roles", "ACTIVATION"),
    ("2609.00595", "07", "SoK：安全的智能体也可能一起失败", "SoK: When Safe Agents Fail Together", "SECURITY"),
    ("2509.24323", "08", "MAS²：自生成、自配置、自纠偏的多智能体系统", "Self-Generative Multi-Agent Systems", "SELF-GENERATIVE"),
    ("2601.04861", "09", "OI-MAS：跨多尺度模型的置信感知路由", "OI-MAS: Confidence-Aware Routing across Multi-Scale Models", "ROUTING"),
    ("2602.00966", "10", "Symphony-Coord：去中心化的涌现式协调", "Symphony-Coord: Adaptive Routing for Multi-Agent LLM Systems", "DECENTRALIZED"),
    ("2609.01736", "11", "HEART：自然语言工具原语 + 2.5 万函数仓库", "HEART: Harness Engineering via Agent-Native Reusable Tool Primitives", "HARNESS"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    # index 封面（全 11 色点）
    render("", "11", "Multi-Agent Framework / Harness",
           "2026 代表性论文 · 中文编译版 · 11 Papers", None, 20260903, index=True)
    for i, (arx, num, zh, en, cat) in enumerate(ORDER, 1):
        p = V4.PAPER[arx]
        render(arx, num, p["og"], p["title"], cat, i * 7)
    apple_icon()
    render_static("术语表 · GLOSSARY", "31 Terms · Multi-Agent Papers 2026", "glossary.png", "#557B3F")
    render_static("关于 · ABOUT", "收录标准 / 阅读指南 / 许可", "about.png", "#3E6FA3")


if __name__ == "__main__":
    main()
