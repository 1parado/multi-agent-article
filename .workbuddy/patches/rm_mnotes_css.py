#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 v5 CSS 里已无对应 HTML 的失效规则（v5 后续：mnotes/paper-main 已移除）。

幂等：再次运行会全部 assert 命中（计数=0 即不再处理）。
"""
import os, re, sys

BASE = "D:/multi-agent-article/"
TARGETS = [
    "2509.24323_MAS2_中文版.html",
    "2601.04861_OI-MAS_中文版.html",
    "2602.00966_Symphony-Coord_中文版.html",
    "2602.16873_AdaptOrch_中文版.html",
    "2603.11445_VMAO_中文版.html",
    "2603.25723_NLAH_中文版.html",
    "2603.28052_Meta-Harness_中文版.html",
    "2606.03005_MUSE_中文版.html",
    "2608.27338_MoRe_中文版.html",
    "2609.00595_SoK_中文版.html",
    "2609.01736_HEART_中文版.html",
]

# 一行内含下列选择器，整行删掉
LINE_DROP_SELECTORS = (
    "body.page-paper .wrap { display:grid; grid-template-columns:minmax(0,1fr) 232px; gap:48px; }",
    "body.page-paper .wrap > .paper-main { min-width:0; }",
    "body.page-paper .mnotes { display:flex; flex-direction:column; gap:14px; align-self:start; position:sticky; top:36px; }",
    "body.page-paper .mnotes h4 {",
    "body.page-paper .mnote { border:1px solid var(--line); border-radius:8px;",
    "body.page-paper .mnote p { margin:0; line-height:1.65;",
    "body.page-paper .mnote a { color:var(--red);",
    "body.page-paper .mnote a:hover {",
    "body.page-paper .mnote .dotc {",
    "body.page-paper .wrap { display:block; }",
    "body.page-paper .mnotes { position:static; margin-top:42px;",
)
# @media (max-width:1240px) 整块删除（其中只剩 .wrap+.mnotes；两行都已被 LINE_DROP 覆盖，但若仅剩 .mnotes 一行也整块删）
RE_MEDIA_BLOCK = re.compile(r'@media \(max-width:1240px\) \{\n(?:  [^\n]*\n)+?  \}\n')
# print 块内 , .mnotes 清理（保留其它规则）
RE_PRINT_MNOTES = re.compile(r', \.mnotes')


def process(src: str) -> str:
    out_lines = []
    for line in src.splitlines(keepends=True):
        stripped = line.rstrip("\n")
        if any(stripped.lstrip().startswith(sel) or sel in stripped for sel in LINE_DROP_SELECTORS):
            continue
        out_lines.append(line)
    out = "".join(out_lines)
    out = RE_MEDIA_BLOCK.sub("", out)
    out = RE_PRINT_MNOTES.sub("", out)
    return out


def run():
    for name in TARGETS:
        p = os.path.join(BASE, name)
        src = open(p, encoding="utf-8").read()
        before_m = src.count("mnotes")
        before_p = src.count("paper-main")
        if before_m == 0 and before_p == 0:
            print(name, "skip (clean)")
            continue
        out = process(src)
        after_m = out.count("mnotes")
        after_p = out.count("paper-main")
        print(name, "mnotes", before_m, "->", after_m, "; paper-main", before_p, "->", after_p)
        if after_m or after_p:
            # 还有残留：可能是 print 块里有 .mnotes 等，assert 失败以便补 pattern
            assert False, name + " still has residual mnotes/paper-main"
        if out != src:
            open(p, "w", encoding="utf-8", newline="\n").write(out)


if __name__ == "__main__":
    run()