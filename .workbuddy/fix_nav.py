# -*- coding: utf-8 -*-
"""Fix nav links to relative paths + inject heading-TOC widget into all paper HTML files."""
import io, os, sys

ROOT = r"D:\multi-agent-article"
FILES = [
    "2603.11445_VMAO_中文版.html",
    "2602.16873_AdaptOrch_中文版.html",
    "2603.25723_NLAH_中文版.html",
    "2603.28052_Meta-Harness_中文版.html",
    "2606.03005_MUSE_中文版.html",
    "2608.27338_MoRe_中文版.html",
    "2609.00595_SoK_中文版.html",
    "2509.24323_MAS2_中文版.html",
]

BLOB = "https://github.com/1parado/multi-agent-article/blob/main/"
RAW = "https://github.com/1parado/multi-agent-article/raw/main/"

# local PDFs exist -> relative; missing -> arxiv pdf
PDF_MAP = {
    "2603.11445_VMAO_Verified-Multi-Agent-Orchestration.pdf": "2603.11445_VMAO_Verified-Multi-Agent-Orchestration.pdf",
    "2602.16873_AdaptOrch_Task-Adaptive-Multi-Agent-Orchestration.pdf": "2602.16873_AdaptOrch_Task-Adaptive-Multi-Agent-Orchestration.pdf",
    "2603.25723_Natural-Language-Agent-Harnesses.pdf": "2603.25723_Natural-Language-Agent-Harnesses.pdf",
    "2603.28052_Meta-Harness_End-to-End-Optimization-of-Model-Harnesses.pdf": "2603.28052_Meta-Harness_End-to-End-Optimization-of-Model-Harnesses.pdf",
    "2606.03005_MUSE_Unified-Agentic-Harness-for-MLLMs.pdf": "2606.03005_MUSE_Unified-Agentic-Harness-for-MLLMs.pdf",
    "2608.27338_MoRe_Mixture_of_Roles.pdf": "https://arxiv.org/pdf/2608.27338.pdf",
    "2609.00595_SoK_Security_Multi-Agent.pdf": "https://arxiv.org/pdf/2609.00595.pdf",
    "2509.24323_MAS2_Self-Generative.pdf": "https://arxiv.org/pdf/2509.24323.pdf",
}

TOC_STYLE = """<style>
  /* ---- heading TOC widget (spec: AGENT.md) ---- */
  #toc-btn { position:fixed; right:20px; bottom:28px; z-index:1000; width:44px; height:44px; border-radius:50%; border:1px solid var(--line); background:#fff; color:var(--red); font-size:20px; line-height:1; cursor:pointer; box-shadow:0 2px 10px rgba(0,0,0,.12); opacity:0; pointer-events:none; transition:opacity .25s, transform .25s; transform:translateY(8px); }
  #toc-btn.show { opacity:1; pointer-events:auto; transform:none; }
  #toc-btn.on { background:var(--red); color:#fff; border-color:var(--red); }
  #toc-panel { position:fixed; right:20px; bottom:80px; z-index:1000; min-width:200px; max-width:320px; max-height:62vh; overflow-y:auto; background:#fff; border:1px solid var(--line); border-radius:10px; box-shadow:0 6px 24px rgba(0,0,0,.14); padding:12px 6px 8px; display:none; }
  #toc-panel.open { display:block; }
  #toc-panel .toc-title { font-family:"IBM Plex Mono",Consolas,monospace; font-size:11px; letter-spacing:2px; color:var(--red); padding:0 12px 8px; border-bottom:1px solid var(--line); }
  #toc-panel a { display:block; color:var(--gray); text-decoration:none; font-size:13.5px; line-height:1.6; padding:6px 12px; border-radius:6px; }
  #toc-panel a:hover { background:#f6f5f3; color:var(--red); }
  #toc-panel a.t1 { font-weight:700; color:var(--ink); }
  #toc-panel a.t2 { padding-left:24px; }
</style>
"""

TOC_SCRIPT = """<script>
/* ---- heading TOC widget (spec: AGENT.md) ---- */
(function () {
  var heads = [].slice.call(document.querySelectorAll(".wrap h1, .wrap h2"));
  if (heads.length < 2) return;
  heads.forEach(function (h, i) { if (!h.id) h.id = "h-" + (i + 1); });
  var btn = document.createElement("button");
  btn.id = "toc-btn"; btn.type = "button"; btn.title = "文章目录"; btn.innerHTML = "&#9776;";
  var panel = document.createElement("nav");
  panel.id = "toc-panel"; panel.setAttribute("aria-label", "文章目录");
  var html = '<div class="toc-title">CONTENTS</div>';
  heads.forEach(function (h) {
    html += '<a href="#' + h.id + '" class="' + (h.tagName === "H1" ? "t1" : "t2") + '">' + h.textContent + "</a>";
  });
  panel.innerHTML = html;
  document.body.appendChild(btn);
  document.body.appendChild(panel);
  function close() { panel.classList.remove("open"); btn.classList.remove("on"); }
  btn.addEventListener("click", function (e) {
    e.stopPropagation();
    panel.classList.toggle("open"); btn.classList.toggle("on");
  });
  panel.addEventListener("click", function (e) {
    var a = e.target.closest("a");
    if (!a) return;
    e.preventDefault();
    var t = document.getElementById(a.getAttribute("href").slice(1));
    if (t) t.scrollIntoView({ behavior: "smooth", block: "start" });
    close();
  });
  document.addEventListener("click", function (e) {
    if (!panel.contains(e.target) && e.target !== btn) close();
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
  function onScroll() {
    var show = window.scrollY > 180;
    btn.classList.toggle("show", show);
    if (!show) close();
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
})();
</script>
"""

def must(cond, msg):
    if not cond:
        print("  !! " + msg)
        return False
    return True

changed = 0
for name in FILES:
    path = os.path.join(ROOT, name)
    with io.open(path, "r", encoding="utf-8") as f:
        s = f.read()
    orig = s
    print("== " + name)

    # 1. nav row fixes (do before global replaces)
    if name.startswith("2606.03005_MUSE"):
        old = '<div class="nav"><a href="' + BLOB + '2603.28052_Meta-Harness_中文版.html">← Meta-Harness</a><a href="' + BLOB + 'index.html">目录</a></div>'
        new = '<div class="nav"><a href="2603.28052_Meta-Harness_中文版.html">← 上一篇：Meta-Harness</a><a href="index.html">目录</a><a href="2608.27338_MoRe_中文版.html">下一篇：MoRe →</a></div>'
        if must(old in s, "MUSE nav row not found"): s = s.replace(old, new)
    if name.startswith("2608.27338_MoRe"):
        old = '  <a href="' + BLOB + 'index.html">← 目录</a>'
        new = '  <a href="2606.03005_MUSE_中文版.html">← 上一篇：MUSE</a>'
        if must(old in s, "MoRe prev row not found"): s = s.replace(old, new)

    # 2. PDF links
    for pdf, target in PDF_MAP.items():
        s = s.replace(RAW + pdf, target)

    # 3. blob -> relative (index.html + prev/next)
    s = s.replace(BLOB, "")

    # 4. inject TOC widget
    if "#toc-btn" not in s:
        if must("</head>" in s and "</body>" in s, "missing </head>/</body>"):
            s = s.replace("</head>", TOC_STYLE + "</head>", 1)
            s = s.replace("</body>", TOC_SCRIPT + "</body>", 1)

    if s != orig:
        with io.open(path, "w", encoding="utf-8", newline="") as f:
            f.write(s)
        changed += 1
        print("  updated")
    else:
        print("  no change")

print("\n%d/%d files updated" % (changed, len(FILES)))
# sanity check: no absolute github links left in paper pages
for name in FILES:
    with io.open(os.path.join(ROOT, name), "r", encoding="utf-8") as f:
        s = f.read()
    if "github.com/1parado" in s:
        print("LEFTOVER in " + name)
print("check done")
