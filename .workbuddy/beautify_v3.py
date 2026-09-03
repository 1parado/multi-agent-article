# -*- coding: utf-8 -*-
"""Beautification pass v3: anchor links, back-to-top, keyboard nav, section numbers,
cmp-table polish, mobile polish, GitHub icon links."""
import io, os, re

ROOT = r"D:\multi-agent-article"
PAPERS = [
    "2603.11445_VMAO_中文版.html",
    "2602.16873_AdaptOrch_中文版.html",
    "2603.25723_NLAH_中文版.html",
    "2603.28052_Meta-Harness_中文版.html",
    "2606.03005_MUSE_中文版.html",
    "2608.27338_MoRe_中文版.html",
    "2609.00595_SoK_中文版.html",
    "2509.24323_MAS2_中文版.html",
    "2601.04861_OI-MAS_中文版.html",
    "2602.00966_Symphony-Coord_中文版.html",
    "2609.01736_HEART_中文版.html",
]
INDEX = "index.html"
REPO = "https://github.com/1parado/multi-agent-article"

GH_ICON = '<a class="ghlink" href="' + REPO + '" target="_blank" rel="noopener"><svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>GitHub</a>'

V3_STYLE = """<style>
  /* ---- v3 enhancements (spec: AGENT.md) ---- */
  #totop { position:fixed; right:20px; bottom:80px; z-index:1000; width:44px; height:44px; border-radius:50%; border:1px solid var(--line); background:#fff; color:var(--red); font-size:18px; line-height:1; cursor:pointer; box-shadow:0 2px 10px rgba(0,0,0,.12); opacity:0; pointer-events:none; transition:opacity .25s, transform .25s; transform:translateY(8px); }
  #totop.show { opacity:1; pointer-events:auto; transform:none; }
  #totop:hover { background:var(--red); color:#fff; border-color:var(--red); }
  #toc-panel { bottom:132px; }
  h2 { position:relative; }
  .secno { font-family:"IBM Plex Mono",Consolas,monospace; font-size:13px; color:var(--red); margin-right:12px; letter-spacing:1px; }
  .hlink { position:absolute; left:-20px; top:50%; transform:translateY(-50%); color:var(--red); opacity:0; text-decoration:none; font-family:"IBM Plex Mono",Consolas,monospace; font-size:16px; font-weight:600; transition:opacity .2s; }
  h2:hover .hlink { opacity:.55; }
  .hlink:hover { opacity:1; }
  .ghlink { color:inherit; text-decoration:none; }
  .ghlink:hover { color:var(--red); }
  .ghlink svg { vertical-align:-2px; margin-right:5px; }
  table.cmp td { transition:background .2s ease; }
  table.cmp tr:nth-child(odd) td { background:#faf9f7; }
  table.cmp tr:hover td { background:#f3efe9; }
  table.cmp td:first-child b { color:var(--red); }
  table.cmp td:first-child { font-family:"IBM Plex Mono",Consolas,monospace; font-size:13px; letter-spacing:.3px; }
  @media (max-width:640px) {
    body { font-size:15px; line-height:1.9; }
    .wrap { padding:48px 18px 72px; }
    h1 { font-size:24px; }
    h2 { font-size:19px; margin-top:44px; }
    .zh, .sub { font-size:17px; }
    .chart { gap:20px; }
    .bars { height:160px; }
    #toc-btn, #totop { right:12px; }
    #toc-panel { right:12px; max-width:78vw; }
    .hlink { display:none; }
    .hero { padding:12px 4px 4px; }
    .paper { padding-left:12px; margin-left:-12px; padding-right:8px; }
  }
</style>
"""

SCRIPT_V3 = """<script>
/* ---- page enhancements v3 (spec: AGENT.md): TOC + scroll-spy + progress + reveal + bars + anchors + totop + kbd ---- */
(function () {
  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* reading progress bar */
  var pbar = document.createElement("div");
  pbar.id = "pbar";
  document.body.appendChild(pbar);

  /* back to top */
  var totop = document.createElement("button");
  totop.id = "totop"; totop.type = "button"; totop.title = "回到顶部"; totop.innerHTML = "&#8593;";
  totop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" }); });
  document.body.appendChild(totop);

  /* heading TOC */
  var heads = [].slice.call(document.querySelectorAll(".wrap h1, .wrap h2"));
  heads.forEach(function (h, i) { if (!h.id) h.id = "h-" + (i + 1); });
  var btn = null, panel = null, links = [];
  if (heads.length >= 2) {
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

  /* section numbers + hover anchor links on h2 (after TOC build, so labels stay clean) */
  var h2n = 0;
  heads.forEach(function (h) {
    if (h.tagName !== "H2") return;
    h2n++;
    var no = document.createElement("span");
    no.className = "secno";
    no.textContent = (h2n < 10 ? "0" : "") + h2n;
    h.insertBefore(no, h.firstChild);
    var hl = document.createElement("a");
    hl.className = "hlink"; hl.href = "#" + h.id; hl.textContent = "#"; hl.title = "复制章节链接";
    hl.addEventListener("click", function (e) {
      e.preventDefault();
      var url = location.href.split("#")[0] + "#" + h.id;
      function done() { hl.textContent = "\\u2713"; setTimeout(function () { hl.textContent = "#"; }, 1200); }
      function fallback() {
        var ta = document.createElement("textarea");
        ta.value = url; document.body.appendChild(ta); ta.select();
        try { document.execCommand("copy"); } catch (err) {}
        document.body.removeChild(ta); done();
      }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(done, fallback);
      else fallback();
      if (history.replaceState) history.replaceState(null, "", "#" + h.id);
    });
    h.appendChild(hl);
  });

  /* keyboard prev/next (paper pages with .nav) */
  var prevA = null, nextA = null;
  [].slice.call(document.querySelectorAll(".nav a")).forEach(function (a) {
    var t = a.textContent || "";
    if (t.indexOf("←") !== -1 && !prevA) prevA = a;
    else if (t.indexOf("→") !== -1 && !nextA) nextA = a;
  });
  document.addEventListener("keydown", function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey || e.shiftKey) return;
    var t = e.target && e.target.tagName;
    if (t === "INPUT" || t === "TEXTAREA") return;
    if (e.key === "ArrowLeft" && prevA) location.href = prevA.getAttribute("href");
    if (e.key === "ArrowRight" && nextA) location.href = nextA.getAttribute("href");
  });

  /* scroll: progress + scroll-spy + totop visibility */
  function onScroll() {
    var doc = document.documentElement;
    var max = doc.scrollHeight - window.innerHeight;
    pbar.style.width = (max > 0 ? (window.scrollY / max) * 100 : 0) + "%";
    totop.classList.toggle("show", window.scrollY > 600);
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

INDEX_FOOTER = """
<footer><span class="ghlink-wrap">' + GH_ICON + '</span></footer>
"""

def read(p):
    with io.open(os.path.join(ROOT, p), "r", encoding="utf-8") as f:
        return f.read()

def write(p, s):
    with io.open(os.path.join(ROOT, p), "w", encoding="utf-8", newline="") as f:
        f.write(s)

def replace_v2_script(s):
    m = s.find("page enhancements v2")
    if m == -1:
        return None
    start = s.rfind("<script>", 0, m)
    end = s.find("</script>", m)
    if start == -1 or end == -1:
        return None
    return s[:start] + SCRIPT_V3 + s[end + len("</script>"):]

GH_SVG_ONLY = GH_ICON[GH_ICON.index("<svg"):GH_ICON.index("</svg>") + len("</svg>")]

# ---------- paper pages ----------
for name in PAPERS:
    s = read(name)
    orig = s
    msgs = []

    if "page enhancements v3" not in s:
        r = replace_v2_script(s)
        if r is not None:
            s = r; msgs.append("script-v3")
        else:
            print("!! v2 script not found in", name)

    if "v3 enhancements" not in s:
        s = s.replace("</head>", V3_STYLE + "</head>", 1)
        msgs.append("css")

    arxiv_id = name.split("_")[0]
    pat = '<a href="https://arxiv.org/abs/' + arxiv_id + '">arXiv</a>'
    if pat in s and "ghlink" not in s.split("</head>")[1]:
        s = s.replace(pat, pat + GH_ICON, 1)
        msgs.append("gh-links")

    if s != orig:
        write(name, s)
    print("==", name, "->", ",".join(msgs) if msgs else "no change")

# ---------- index ----------
s = read(INDEX)
orig = s
msgs = []

if "page enhancements v3" not in s:
    r = replace_v2_script(s)
    if r is not None:
        s = r; msgs.append("script-v3")
    else:
        print("!! v2 script not found in index")

if "v3 enhancements" not in s:
    s = s.replace("</head>", V3_STYLE + "</head>", 1)
    msgs.append("css")

if "ghlink" not in s:
    footer_html = '\n<footer>' + GH_ICON + '</footer>\n'
    anchor = 'HEART</a>。</p>\n'
    if anchor in s:
        s = s.replace(anchor, anchor + footer_html, 1)
        msgs.append("gh-footer")
    else:
        print("!! index footer anchor not found")

if s != orig:
    write(INDEX, s)
print("==", INDEX, "->", ",".join(msgs) if msgs else "no change")
print("done")
