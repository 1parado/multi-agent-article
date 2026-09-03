#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""移除论文页旁注栏（含 .mnotes / .paper-main 双栏包裹）。
幂等：再次运行会被断言拦截。

操作：
  1. 删除整段 <aside class="mnotes">…</aside>
  2. 解开 <div class="paper-main">…</div> 包裹（双栏 → 单栏），若该包裹除 aside 外没有其它直接子节点
     则一并删除外层 wrapper；其余情况只去掉 aside 子节点

依赖：仅需 Python 3.8+ 标准库，无外部依赖。
"""
import glob, os, sys, re

BASE = "D:/multi-agent-article/"
PAPER_NAMES = [
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
MARK = '<aside class="mnotes"'   # 全文唯一：论文页只剩这一处 aside
PAPER_MAIN = 'class="paper-main"'

ASIDE_RE = re.compile(r'\n*<aside class="mnotes".*?</aside>\n*', re.S)
PAPER_MAIN_OPEN_RE = re.compile(r'\n*<div class="paper-main">\n*', re.S)
PAPER_MAIN_CLOSE_RE = re.compile(r'\n*</div>\n+(?=<footer)', re.S)


def patch(name: str) -> dict:
    path = os.path.join(BASE, name)
    src = open(path, encoding="utf-8").read()

    rep = {
        "aside_before": src.count(MARK),
        "paper_main_before": src.count(PAPER_MAIN),
    }
    if rep["aside_before"] == 0 and rep["paper_main_before"] == 0:
        rep["skipped"] = True
        return rep

    # 1) 拆 aside 整段
    new = ASIDE_RE.sub('\n', src, count=1)
    # 2) 拆 paper-main wrapper（open + 对应 close）
    new = PAPER_MAIN_OPEN_RE.sub('', new, count=1)
    new = PAPER_MAIN_CLOSE_RE.sub('', new, count=1)

    rep["aside_after"] = new.count(MARK)
    rep["paper_main_after"] = new.count(PAPER_MAIN)
    assert rep["aside_after"] == 0, name + " aside 未彻底移除"
    assert rep["paper_main_after"] == 0, name + " paper-main 未彻底移除"

    if new != src:
        open(path, "w", encoding="utf-8", newline="\n").write(new)
        rep["written"] = True
    else:
        rep["written"] = False
    return rep


def run():
    for n in PAPER_NAMES:
        r = patch(n)
        print(n, r)


if __name__ == "__main__":
    run()