# -*- coding: utf-8 -*-
"""Patch pass: swap legacy TOC script -> v2 everywhere; add --cat to 3 files with non-PAPER eyebrows."""
import io, os

ROOT = r"D:\multi-agent-article"
PAPERS = [
    ("2603.11445_VMAO_中文版.html", "#A02C2C"),
    ("2602.16873_AdaptOrch_中文版.html", "#A02C2C"),
    ("2603.25723_NLAH_中文版.html", "#9C6B1E"),
    ("2603.28052_Meta-Harness_中文版.html", "#9C6B1E"),
    ("2606.03005_MUSE_中文版.html", "#9C6B1E"),
    ("2608.27338_MoRe_中文版.html", "#6B4FA0"),
    ("2609.00595_SoK_中文版.html", "#2E7D74"),
    ("2509.24323_MAS2_中文版.html", "#A34A7D"),
    ("2601.04861_OI-MAS_中文版.html", "#3E6FA3"),
    ("2602.00966_Symphony-Coord_中文版.html", "#557B3F"),
    ("2609.01736_HEART_中文版.html", "#9C6B1E"),
]

with io.open(os.path.join(ROOT, ".workbuddy", "beautify_v2.py"), "r", encoding="utf-8") as f:
    src = f.read()
a = src.index('SCRIPT_V2 = """') + len('SCRIPT_V2 = """')
b = src.index('"""\n\nHERO_SVG')
SCRIPT_V2 = src[a:b]

def read(p):
    with io.open(os.path.join(ROOT, p), "r", encoding="utf-8") as f:
        return f.read()

def write(p, s):
    with io.open(os.path.join(ROOT, p), "w", encoding="utf-8", newline="") as f:
        f.write(s)

for name, color in PAPERS:
    s = read(name)
    orig = s
    msgs = []

    # 1. script v2 via unique JS marker
    if "scroll-spy" not in s:
        m = s.find("var heads = [].slice.call")
        if m == -1:
            print("!! no script marker:", name)
            continue
        start = s.rfind("<script>", 0, m)
        end = s.find("</script>", m)
        s = s[:start] + SCRIPT_V2 + s[end + len("</script>"):]
        msgs.append("script-v2")

    # 2. cat dot for eyebrow variants without PAPER prefix
    if "--cat:" not in s:
        old = '<div class="eyebrow">'
        new = '<div class="eyebrow" style="--cat:%s"><span class="dot"></span>' % color
        if old in s:
            s = s.replace(old, new, 1)
            msgs.append("cat-dot")
        else:
            print("!! no eyebrow:", name)

    if s != orig:
        write(name, s)
    print("==", name, "->", ",".join(msgs) if msgs else "no change")
