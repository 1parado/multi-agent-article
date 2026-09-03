# -*- coding: utf-8 -*-
"""Site-wide beautification pass v2 (8 selected enhancements).

1. category color tags   -> --cat on eyebrow / idx + color dot
2. hero visual           -> index SVG pipeline illustration + paper arXiv watermark
3. progress bar          -> #pbar fixed top
4. scroll-spy TOC        -> active heading highlight
5. typography            -> IBM Plex Mono webfont links + tldr drop cap
6. card hover            -> index .paper hover elevation
7. scroll reveal         -> IntersectionObserver fade-up (reduced-motion safe)
8. chart animation       -> bars grow from 0 on first view
All pages get the shared script v2 (TOC + spy + progress + reveal + bars).
"""
import io, os, re

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
INDEX = "index.html"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">\n')

VIEWPORT = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'

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

EXTRA_CSS = """  /* ---- v2 enhancements (spec: AGENT.md) ---- */
  #pbar { position:fixed; top:0; left:0; height:3px; width:0; background:var(--red); z-index:1200; }
  .dot { display:inline-block; width:8px; height:8px; border-radius:50%; background:var(--cat,var(--red)); margin-right:8px; vertical-align:1px; }
  .eyebrow { color:var(--cat,var(--red)); }
  #toc-panel a.active { color:var(--red); background:#f6f5f3; font-weight:600; }
  .bar { transition:height .9s cubic-bezier(.22,.7,.3,1); }
  .barwrap:hover .bar { filter:brightness(1.1); }
  .reveal { opacity:0; transform:translateY(16px); transition:opacity .6s ease, transform .6s ease; }
  .reveal.in { opacity:1; transform:none; }
  @media (prefers-reduced-motion: reduce) { .reveal { opacity:1; transform:none; transition:none; } .bar { transition:none; } }
  .tldr::first-letter { float:left; font-size:2.5em; line-height:.95; margin:4px 12px 0 0; font-weight:700; font-family:"IBM Plex Mono",Consolas,monospace; color:var(--red); }
  .wrap { position:relative; }
  .wm { position:absolute; top:56px; right:20px; font-family:"IBM Plex Mono",Consolas,monospace; font-size:58px; font-weight:700; letter-spacing:1px; color:var(--red); opacity:.06; user-select:none; pointer-events:none; white-space:nowrap; }
  @media (max-width:700px) { .wm { display:none; } }
"""

INDEX_CSS = """  /* ---- index enhancements (spec: AGENT.md) ---- */
  .hero { margin:36px 0 0; padding:20px 10px 8px; border:1px solid var(--line); border-radius:10px; background:#fdfcfa; }
  .hero svg { width:100%; height:auto; display:block; }
  .fl { stroke-dasharray:5 7; animation:dashmove 1.4s linear infinite; }
  @keyframes dashmove { to { stroke-dashoffset:-24; } }
  @media (prefers-reduced-motion: reduce) { .fl { animation:none; } }
  .paper { transition:background .25s ease, border-color .25s ease; border-left:3px solid transparent; padding-left:18px; margin-left:-18px; border-radius:0 8px 8px 0; }
  .paper:hover { background:#faf8f6; border-left-color:var(--cat,var(--red)); }
  .paper .idx { color:var(--cat,var(--red)); }
"""

SCRIPT_V2 = """<script>
/* ---- page enhancements v2 (spec: AGENT.md): TOC + scroll-spy + progress + reveal + bars ---- */
(function () {
  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* reading progress bar */
  var pbar = document.createElement("div");
  pbar.id = "pbar";
  document.body.appendChild(pbar);

  /* heading TOC */
  var heads = [].slice.call(document.querySelectorAll(".wrap h1, .wrap h2"));
  var btn = null, panel = null, links = [];
  if (heads.length >= 2) {
    heads.forEach(function (h, i) { if (!h.id) h.id = "h-" + (i + 1); });
    btn = document.createElement("button");
    btn.id = "toc-btn"; btn.type = "button"; btn.title = "文章目录"; btn.innerHTML = "&#9776;";
    panel = document.createElement("nav");
    panel.id = "toc-panel"; panel.setAttribute("aria-label", "文章目录");
    var html = '<div class="toc-title">CONTENTS</div>';
    heads.forEach(function (h) {
      html += '<a href="#' + h.id + '" class="' + (h.tagName === "H1" ? "t1" : "t2") + '">' + h.textContent + "</a>";
    });
    panel.innerHTML = html;
    document.body.appendChild(btn);
    document.body.appendChild(panel);
    links = [].slice.call(panel.querySelectorAll("a"));
    function toggle(e) { e.stopPropagation(); panel.classList.toggle("open"); btn.classList.toggle("on"); }
    btn.addEventListener("click", toggle);
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
  }
  function close() { if (!panel) return; panel.classList.remove("open"); btn.classList.remove("on"); }

  /* scroll: progress + scroll-spy */
  function onScroll() {
    var doc = document.documentElement;
    var max = doc.scrollHeight - window.innerHeight;
    pbar.style.width = (max > 0 ? (window.scrollY / max) * 100 : 0) + "%";
    if (!panel) return;
    var show = window.scrollY > 180;
    btn.classList.toggle("show", show);
    if (!show) close();
    var cur = -1;
    for (var i = 0; i < heads.length; i++) {
      if (heads[i].getBoundingClientRect().top <= 120) cur = i; else break;
    }
    links.forEach(function (a, i) { a.classList.toggle("active", i === cur); });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* reveal on scroll + bar growth animation */
  if (!reduced && "IntersectionObserver" in window) {
    var targets = [].slice.call(document.querySelectorAll(".wrap h2, .hline, .contrib, .chart, .paper, .trend, table.cmp, .tldr"));
    var bars = [].slice.call(document.querySelectorAll(".bar"));
    bars.forEach(function (b) { b.dataset.h = b.style.height; b.style.height = "0%"; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add("in");
        [].slice.call(e.target.querySelectorAll(".bar")).forEach(function (b) { b.style.height = b.dataset.h; });
        io.unobserve(e.target);
      });
    }, { threshold: 0.12 });
    targets.forEach(function (el) { el.classList.add("reveal"); io.observe(el); });
  }
})();
</script>
"""

HERO_SVG = """<div class="hero">
<svg viewBox="0 0 780 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="多智能体编排示意：计划-并行执行-验证-合成">
  <g stroke="#C9CBC0" stroke-width="1.5" fill="none">
    <line class="fl" x1="68" y1="100" x2="118" y2="100"/>
    <line class="fl" x1="218" y1="100" x2="314" y2="28"/>
    <line class="fl" x1="218" y1="100" x2="314" y2="76"/>
    <line class="fl" x1="218" y1="100" x2="314" y2="124"/>
    <line class="fl" x1="218" y1="100" x2="314" y2="172"/>
    <line class="fl" x1="346" y1="28" x2="468" y2="94"/>
    <line class="fl" x1="346" y1="76" x2="468" y2="97"/>
    <line class="fl" x1="346" y1="124" x2="468" y2="103"/>
    <line class="fl" x1="346" y1="172" x2="468" y2="106"/>
    <line class="fl" x1="572" y1="100" x2="622" y2="100"/>
  </g>
  <circle cx="52" cy="100" r="15" fill="#fff" stroke="#1a1a1a" stroke-width="1.5"/>
  <text x="52" y="136" text-anchor="middle" font-family="IBM Plex Mono,Consolas,monospace" font-size="10" fill="#8a8a86" letter-spacing="1">QUERY</text>
  <rect x="120" y="78" width="98" height="44" rx="8" fill="#A02C2C"/>
  <text x="169" y="104" text-anchor="middle" font-family="IBM Plex Mono,Consolas,monospace" font-size="11" fill="#fff" letter-spacing="1">PLANNER</text>
  <circle cx="330" cy="28" r="14" fill="#9C6B1E"/>
  <circle cx="330" cy="76" r="14" fill="#2E7D74"/>
  <circle cx="330" cy="124" r="14" fill="#6B4FA0"/>
  <circle cx="330" cy="172" r="14" fill="#3E6FA3"/>
  <text x="330" y="196" text-anchor="middle" font-family="IBM Plex Mono,Consolas,monospace" font-size="10" fill="#8a8a86" letter-spacing="1">AGENTS ×N</text>
  <rect x="470" y="78" width="102" height="44" rx="8" fill="#fff" stroke="#A02C2C" stroke-width="1.5"/>
  <text x="521" y="104" text-anchor="middle" font-family="IBM Plex Mono,Consolas,monospace" font-size="11" fill="#A02C2C" letter-spacing="1">VERIFIER</text>
  <circle cx="644" cy="100" r="15" fill="#A02C2C"/>
  <path d="M637 100 l5 5 l10 -11" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="644" y="136" text-anchor="middle" font-family="IBM Plex Mono,Consolas,monospace" font-size="10" fill="#8a8a86" letter-spacing="1">ANSWER</text>
</svg>
</div>
"""

def read(p):
    with io.open(os.path.join(ROOT, p), "r", encoding="utf-8") as f:
        return f.read()

def write(p, s):
    with io.open(os.path.join(ROOT, p), "w", encoding="utf-8", newline="") as f:
        f.write(s)

def replace_old_script(s):
    """Replace legacy TOC-only script block with SCRIPT_V2 (marker-based)."""
    m = s.find("/* ---- heading TOC widget (spec: AGENT.md) ---- */")
    if m == -1:
        return None
    start = s.rfind("<script>", 0, m)
    end = s.find("</script>", m)
    if start == -1 or end == -1:
        return None
    return s[:start] + SCRIPT_V2 + s[end + len("</script>"):]

ok = True

# ---------- paper pages ----------
for name, color in PAPERS:
    s = read(name)
    orig = s
    arxiv_id = name.split("_")[0]
    msgs = []

    # 1. webfont links
    if "fonts.googleapis.com" not in s:
        s = s.replace(VIEWPORT, VIEWPORT + "\n" + FONTS, 1)
        msgs.append("fonts")

    # 2. category dot + --cat on eyebrow
    if "--cat:" not in s:
        old = '<div class="eyebrow">PAPER'
        new = '<div class="eyebrow" style="--cat:%s"><span class="dot"></span>PAPER' % color
        if old in s:
            s = s.replace(old, new, 1)
            msgs.append("cat-dot")

    # 3. arXiv watermark after .wrap
    if 'class="wm"' not in s:
        s = s.replace('<div class="wrap">', '<div class="wrap">\n<div class="wm">arXiv ' + arxiv_id + "</div>", 1)
        msgs.append("wm")

    # 4. extra css before </style></head>
    if "#pbar" not in s:
        s = s.replace("</style>\n</head>", EXTRA_CSS + "</style>\n</head>", 1)
        msgs.append("css")

    # 5. script v2
    if "#pbar {" in s and "toc-btn" in s and "scroll-spy" not in s:
        r = replace_old_script(s)
        if r is not None:
            s = r
            msgs.append("script-v2")
        else:
            print("!! script marker not found in", name); ok = False

    if s != orig:
        write(name, s)
    print("==", name, "->", ",".join(msgs) if msgs else "no change")

# ---------- index ----------
s = read(INDEX)
orig = s
msgs = []

if "fonts.googleapis.com" not in s:
    s = s.replace(VIEWPORT, VIEWPORT + "\n" + FONTS, 1)
    msgs.append("fonts")

s = s.replace("8 篇经核验的 arXiv 论文", "11 篇经核验的 arXiv 论文", 1)
msgs.append("count-11")

if '<div class="eyebrow">PAPER DIGEST' in s:
    s = s.replace('<div class="eyebrow">PAPER DIGEST', '<div class="eyebrow"><span class="dot"></span>PAPER DIGEST', 1)
    msgs.append("dot")

# color the 11 .idx lines in order
idx_colors = [c for _, c in PAPERS]
parts = s.split('<div class="idx">')
if len(parts) == len(idx_colors) + 1:
    buf = [parts[0]]
    for i, c in enumerate(idx_colors):
        buf.append('<div class="idx" style="--cat:%s"><span class="dot"></span>%s' % (c, parts[i + 1]))
    s = "".join(buf)
    msgs.append("idx-colors")
else:
    print("!! unexpected .idx count:", len(parts) - 1); ok = False

# hero svg after intro paragraph
if 'class="hero"' not in s:
    m = re.search(r'<p class="intro">[^<]*</p>\n', s)
    if m:
        s = s[:m.end()] + "\n" + HERO_SVG + s[m.end():]
        msgs.append("hero")
    else:
        print("!! intro paragraph not found"); ok = False

if "#pbar" not in s:
    s = s.replace("</style>\n</head>", EXTRA_CSS + INDEX_CSS + "</style>\n</head>", 1)
    msgs.append("css")
if "fonts.googleapis.com" in s and "toc-btn" not in s:
    s = s.replace("</head>", TOC_STYLE + "</head>", 1)
    msgs.append("toc-style")
if "</script>\n</body>" not in s:
    s = s.replace("</body>", SCRIPT_V2 + "</body>", 1)
    msgs.append("script-v2")

if s != orig:
    write(INDEX, s)
print("==", INDEX, "->", ",".join(msgs))

print("\nOK" if ok else "\nWITH ERRORS")
