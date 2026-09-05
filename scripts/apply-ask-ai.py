#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inject Ask AI (v7) component into all content HTML pages (idempotent).

Usage (from repo root):
  python3 scripts/apply-ask-ai.py

Affects: index.html, about.html, glossary.html, and all *_中文版.html
Skips: 404.html
"""
from __future__ import print_function
import re
import sys
from pathlib import Path

MARKER_CSS = "/* ---- v7 enhancements (spec: AGENT.md): Ask AI ---- */"
MARKER_JS = "/* ---- page enhancements v7 (spec: AGENT.md): Ask AI ---- */"

CSS_BLOCK = r'''
<style>
/* ---- v7 enhancements (spec: AGENT.md): Ask AI ---- */
#ask-ai-wrap { position:fixed; right:20px; bottom:140px; z-index:1000; }
#ask-ai-btn {
  font-family:"IBM Plex Mono",Consolas,monospace;
  font-size:12px; letter-spacing:1px;
  color:var(--red); background:#fff;
  border:1px solid var(--line); border-radius:99px;
  padding:8px 14px; cursor:pointer;
  box-shadow:0 2px 10px rgba(0,0,0,.12);
  display:flex; align-items:center; gap:6px;
  transition:background .2s, color .2s, border-color .2s, opacity .25s, transform .25s;
  opacity:0; pointer-events:none; transform:translateY(8px);
}
#ask-ai-btn.show { opacity:1; pointer-events:auto; transform:none; }
#ask-ai-btn:hover, #ask-ai-btn.open {
  background:var(--red); color:#fff; border-color:var(--red);
}
#ask-ai-menu {
  position:absolute; right:0; bottom:calc(100% + 8px);
  min-width:200px; background:#fff;
  border:1px solid var(--line); border-radius:10px;
  box-shadow:0 6px 24px rgba(0,0,0,.14);
  padding:6px; display:none;
}
#ask-ai-menu.open { display:block; }
#ask-ai-menu button {
  display:block; width:100%; text-align:left;
  font-family:"IBM Plex Mono",Consolas,monospace;
  font-size:13px; color:var(--gray);
  background:none; border:0; border-radius:6px;
  padding:9px 12px; cursor:pointer;
}
#ask-ai-menu button:hover { background:#f6f5f3; color:var(--red); }
@media (max-width:640px) {
  #ask-ai-wrap { right:12px; bottom:140px; }
}
@media print {
  #ask-ai-wrap { display:none !important; }
}
</style>
'''

JS_BLOCK = r'''
<script>
/* ---- page enhancements v7 (spec: AGENT.md): Ask AI ---- */
(function () {
  if (document.getElementById("ask-ai-wrap")) return;

  var wrap = document.createElement("div");
  wrap.id = "ask-ai-wrap";

  var btn = document.createElement("button");
  btn.id = "ask-ai-btn";
  btn.type = "button";
  btn.setAttribute("aria-haspopup", "true");
  btn.setAttribute("aria-expanded", "false");
  btn.title = "向 AI 提问本页内容";
  btn.innerHTML = "Ask AI <span style=\"font-size:10px\">▾</span>";

  var menu = document.createElement("div");
  menu.id = "ask-ai-menu";
  menu.setAttribute("role", "menu");

  function pageLabel() {
    var og = document.querySelector('meta[property="og:title"]');
    var t = og ? (og.getAttribute("content") || "") : (document.title || "");
    t = t.replace(/\s*[·|—\-].*$/, "").trim();
    return t || "当前页面";
  }

  function buildPrompt() {
    var url = window.location.href;
    var label = pageLabel();
    return "我正在阅读 Multi-Agent Framework / Harness 2026 论文导读站点「" + label + "」。\n" +
      "请先阅读（或访问）这个页面：" + url + "\n" +
      "然后帮我深入理解它。\n\n" +
      "要求：\n" +
      "1. 先给出一个紧凑摘要：一段话 + 要点列表（bulleted）。\n" +
      "2. 假设我零背景，但请详细、深入，不要只是表面浏览。\n" +
      "3. 然后问我：想深入哪一部分？或者我正在尝试构建什么？";
  }

  function openAI(kind) {
    var prompt = buildPrompt();
    var encoded = encodeURIComponent(prompt);
    var url = "";

    if (kind === "chatgpt") {
      url = "https://chatgpt.com/?q=" + encoded;
    } else if (kind === "claude") {
      url = "https://claude.ai/new";
      try { navigator.clipboard && navigator.clipboard.writeText(prompt); } catch (e) {}
    } else if (kind === "grok") {
      url = "https://x.com/i/grok";
      try { navigator.clipboard && navigator.clipboard.writeText(prompt); } catch (e) {}
    } else if (kind === "copy") {
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(prompt).then(function () {
            var old = btn.innerHTML;
            btn.textContent = "已复制 ✓";
            setTimeout(function () { btn.innerHTML = old; }, 1600);
          });
        }
      } catch (e) {}
      return;
    }

    if (url) window.open(url, "_blank", "noopener");
    menu.classList.remove("open");
    btn.classList.remove("open");
    btn.setAttribute("aria-expanded", "false");
  }

  [
    { k: "grok",    t: "Ask Grok" },
    { k: "chatgpt", t: "Ask ChatGPT" },
    { k: "claude",  t: "Ask Claude" },
    { k: "copy",    t: "复制提示词" }
  ].forEach(function (item) {
    var b = document.createElement("button");
    b.type = "button";
    b.setAttribute("role", "menuitem");
    b.textContent = item.t;
    b.addEventListener("click", function (e) {
      e.stopPropagation();
      openAI(item.k);
    });
    menu.appendChild(b);
  });

  btn.addEventListener("click", function (e) {
    e.stopPropagation();
    var open = menu.classList.toggle("open");
    btn.classList.toggle("open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  });

  document.addEventListener("click", function () {
    menu.classList.remove("open");
    btn.classList.remove("open");
    btn.setAttribute("aria-expanded", "false");
  });

  // Show after slight scroll (same feel as #totop)
  function onScroll() {
    if (window.scrollY > 180) btn.classList.add("show");
    else btn.classList.remove("show");
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  wrap.appendChild(btn);
  wrap.appendChild(menu);
  document.body.appendChild(wrap);
})();
</script>
'''


def patch_print_rule(content: str) -> str:
    """Ensure #ask-ai-wrap is hidden in print media queries."""
    # Common print hide lists in this repo
    patterns = [
        (r'(#pbar, #toc-btn, #toc-panel, #totop, [^\{]+)(\{ display:none !important; \})',
         lambda m: m.group(1) + (", #ask-ai-wrap" if "#ask-ai-wrap" not in m.group(1) else "") + m.group(2)),
    ]
    for pat, repl in patterns:
        content = re.sub(pat, repl, content)
    # Also cover the more complete lists that already include more ids
    if "#ask-ai-wrap" not in content and "@media print" in content:
        content = content.replace(
            "#pbar, #toc-btn, #toc-panel, #totop, .wm, .hlink, #fltbar, .fltnone, .fltstat, #q { display:none !important; }",
            "#pbar, #toc-btn, #toc-panel, #totop, .wm, .hlink, #fltbar, .fltnone, .fltstat, #q, #ask-ai-wrap { display:none !important; }"
        )
        content = content.replace(
            "#pbar, #toc-btn, #toc-panel, #totop, .wm, .hlink, #fltbar, .fltnone, .fltstat, #q, #imm-btn, #skip, #imm-chip { display:none !important; }",
            "#pbar, #toc-btn, #toc-panel, #totop, .wm, .hlink, #fltbar, .fltnone, .fltstat, #q, #imm-btn, #skip, #imm-chip, #ask-ai-wrap { display:none !important; }"
        )
        content = content.replace(
            ".giscwrap, .annbar, .annmask, .anntoast { display:none !important; }",
            ".giscwrap, .annbar, .annmask, .anntoast, #ask-ai-wrap { display:none !important; }"
        )
    return content


def inject(content: str) -> tuple[str, bool]:
    changed = False

    if MARKER_CSS not in content:
        # Insert CSS just before </head>
        content = content.replace("</head>", CSS_BLOCK + "\n</head>", 1)
        changed = True
    else:
        # Already has CSS; nothing to do for CSS
        pass

    if MARKER_JS not in content:
        # Insert JS just before </body>
        content = content.replace("</body>", JS_BLOCK + "\n</body>", 1)
        changed = True

    new_content = patch_print_rule(content)
    if new_content != content:
        changed = True
        content = new_content

    return content, changed


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    targets = []
    for name in ["index.html", "about.html", "glossary.html"]:
        p = root / name
        if p.is_file():
            targets.append(p)
    for p in sorted(root.glob("*_中文版.html")):
        targets.append(p)

    if not targets:
        print("ERROR: no target HTML found", file=sys.stderr)
        return 1

    updated = 0
    skipped = 0
    for p in targets:
        raw = p.read_text(encoding="utf-8")
        new, changed = inject(raw)
        if changed:
            p.write_text(new, encoding="utf-8")
            print(f"updated: {p.name}")
            updated += 1
        else:
            print(f"already ok: {p.name}")
            skipped += 1

    print(f"\nDone. updated={updated} already_ok={skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
