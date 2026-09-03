# -*- coding: utf-8 -*-
import re, glob, os
BASE = "D:/multi-agent-article/"
files = sorted(glob.glob(BASE + "2*_中文版.html"))
total = 0
for f in files:
    name = os.path.basename(f)
    txt = open(f, encoding="utf-8").read()
    pat = re.compile(r'<div class="mnote"><h4>馆藏信息</h4>.*?</div>', re.S)
    if not pat.search(txt):
        print(name, "SKIP")
        continue
    before = txt.count('class="mnote"')
    txt2 = pat.sub('', txt, count=1)
    open(f, "w", encoding="utf-8", newline="\n").write(txt2)
    total += 1
    print(name, "mnote-cards %d -> %d" % (before, txt2.count('class="mnote"')))
print("changed:", total)
