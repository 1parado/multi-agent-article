# -*- coding: utf-8 -*-
"""Remove .tldr::first-letter drop-cap rule from all pages + AGENT.md."""
import io, os, glob

ROOT = r"D:\multi-agent-article"
RULE = '  .tldr::first-letter { float:left; font-size:2.5em; line-height:.95; margin:4px 12px 0 0; font-weight:700; font-family:"IBM Plex Mono",Consolas,monospace; color:var(--red); }\n'

files = ["index.html", "AGENT.md"] + sorted(glob.glob(os.path.join(ROOT, "*_中文版.html")))
for path in files:
    name = os.path.basename(path)
    full = path if os.path.isabs(path) else os.path.join(ROOT, path)
    with io.open(full, "r", encoding="utf-8") as f:
        s = f.read()
    if RULE in s:
        s = s.replace(RULE, "")
    # spec text mentions
    s = s.replace("`.tldr` 首字下沉、", "").replace("、`.tldr` 首字下沉", "")
    s = s.replace("tldr 首字下沉、", "").replace("、tldr 首字下沉", "")
    s = s.replace("tldr 首字下沉", "")
    with io.open(full, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print(name, "STILL PRESENT" if "first-letter" in s else "cleaned")
