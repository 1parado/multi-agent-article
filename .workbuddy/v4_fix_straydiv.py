# -*- coding: utf-8 -*-
"""移除 beautify_v4 误插的游离 </div>（citebar 前的多余闭合标签）。"""
import glob, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

PAT_A = "</div>\n\n</div>\n\n<div class=\"citebar\">"
PAT_B = "</div>\n\n<div class=\"citebar\">"

for f in glob.glob("D:/multi-agent-article/*_中文版.html"):
    txt = open(f, encoding="utf-8").read()
    c = txt.count(PAT_A)
    if c:
        txt = txt.replace(PAT_A, "</div>\n\n<div class=\"citebar\">")
        open(f, "w", encoding="utf-8", newline="\n").write(txt)
        print(f.split("/")[-1], "fixed", c)
    elif txt.count(PAT_B) == 1:
        print(f.split("/")[-1], "clean")
    else:
        print(f.split("/")[-1], "!! 未命中 citebar 结构", txt.count(PAT_B))
