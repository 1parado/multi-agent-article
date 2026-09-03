# -*- coding: utf-8 -*-
"""beautify_v5.py — v5 全站注入（产品/艺术家双轮 8 项勾选落地）。

依赖：beautify_v4.py（PAPER/CAT_COLOR/CAT_CN/ALIASES 元数据 + v4 已注过的字体/meta）。

注入清单（idempotent，重复运行会被 assertion 拦截）：
  - 全部页 head：theme-color / apple-touch-icon / canonical / JSON-LD / og:image→covers/*.png
  - 论文页 body.class="page-paper"；正文包 .paper-main，末尾加 .mnotes 旁注栏；
    在 .meta 后加 .pubmeta（arXiv 编号 / 投稿月份 / 收录日），在 .tldr 上加 .epigraph 引语；
    v5 脚本记录已读到 LS。
  - index：插入 .viewbar + #gallery + #star 容器；v5 脚本：视图切换、URL 同步、
    已读印章、画廊渲染、星图渲染。
  - glossary / about：只加 head 元数据（canonical / theme-color / apple-touch-icon / JSON-LD）。
"""
import re, sys, json, os
from urllib.parse import quote
import beautify_v4 as V4  # noqa: E402  （v4 顶部会自行把 stdout 重包为 UTF-8）

BASE = "D:/multi-agent-article/"
SITE = V4.SITE
RED = "#A02C2C"
CITE_DATE = "2026-09-03"  # 本批次收录日

PAGES_ALL = list(V4.PAGES) + ["glossary.html", "about.html"]
ORDER_ARX = [
    "2603.11445", "2602.16873", "2603.25723", "2603.28052", "2606.03005",
    "2608.27338", "2609.00595", "2509.24323", "2601.04861", "2602.00966", "2609.01736",
]
ARX_NUM = {a: str(i + 1) for i, a in enumerate(ORDER_ARX)}
ARX_PREV = {a: (ORDER_ARX[i - 1] if i > 0 else None) for i, a in enumerate(ORDER_ARX)}
ARX_NEXT = {a: (ORDER_ARX[i + 1] if i < len(ORDER_ARX) - 1 else None) for i, a in enumerate(ORDER_ARX)}

EPIGRAPH = {
    "2603.11445": "别让模型自说自话——给它一个会验收的同事。",
    "2602.16873": "模型都差不多的时候，怎么搭队才是真正的杠杆。",
    "2603.25723": "把策略从代码里解放出来，写成人话。",
    "2603.28052": "最会写 harness 的，可能是一个会翻历史记录的 agent。",
    "2606.03005": "许多「模型不行」，其实是「harness 不行」。",
    "2608.27338": "多视角不必靠多张嘴——一次推理也能内化一支团队。",
    "2609.00595": "单个 agent 再安全，也架不住一群 agent 一起犯错。",
    "2509.24323": "别再手搓 MAS 了，让系统自己生成、自己纠偏。",
    "2601.04861": "每个人用得上多大模型，路由说了算。",
    "2602.00966": "没有中央指挥，秩序照样从交互中长出来。",
    "2609.01736": "与其让模型迁就工具，不如让工具学会说人话。",
}


def prefix_date(arx):
    if not arx or len(arx) < 4:
        return ""
    y = "20" + arx[:2]
    m = arx[2:4]
    try:
        mm = int(m); mm = mm if 1 <= mm <= 12 else None
    except Exception:
        mm = None
    return (y + "-" + (str(mm).zfill(2) if mm else m)) if mm else y


def ld_paper(arx, p, url):
    return {
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle",
        "headline": p["og"], "name": p["og"],
        "alternativeHeadline": p["title"],
        "url": url,
        "inLanguage": "zh-CN",
        "datePublished": prefix_date(arx),
        "dateModified": CITE_DATE,
        "isPartOf": {"@type": "WebSite", "name": "Multi-Agent Paper Digest 2026", "url": SITE + "/"},
        "description": p["desc"],
        "keywords": ["multi-agent", "agent harness", V4.CAT_CN.get(p["cat"], p["cat"])],
        "publisher": {"@type": "Organization", "name": "1parado/multi-agent-article"},
    }


def ld_index():
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Multi-Agent Paper Digest 2026",
        "url": SITE + "/",
        "inLanguage": "zh-CN",
        "publisher": {"@type": "Organization", "name": "1parado/multi-agent-article"},
        "description": "11 篇 multi-agent 代表性论文（framework / harness / 自生成 / 安全）的中文编译：含对比表、术语表与阅读顺序。",
    }


def ld_static(name, desc, url):
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": name, "description": desc, "url": url, "inLanguage": "zh-CN",
        "isPartOf": {"@type": "WebSite", "name": "Multi-Agent Paper Digest 2026", "url": SITE + "/"},
        "publisher": {"@type": "Organization", "name": "1parado/multi-agent-article"},
    }


V5_CSS = """
  /* ---- v5 enhancements (spec: AGENT.md): covers/views/marginalia/epigraph ---- */
  body.page-paper .wrap { display:grid; grid-template-columns:minmax(0,1fr) 232px; gap:48px; }
  body.page-paper .wrap > .paper-main { min-width:0; }
  body.page-paper .mnotes { display:flex; flex-direction:column; gap:14px; align-self:start; position:sticky; top:36px; }
  body.page-paper .mnotes h4 { font-family:"IBM Plex Mono",Consolas,monospace; font-size:11px; letter-spacing:1.5px; color:var(--red); margin:0 0 6px; font-weight:600; }
  body.page-paper .mnote { border:1px solid var(--line); border-radius:8px; padding:12px 14px; background:#fdfcfa; font-size:13.5px; color:var(--gray); }
  body.page-paper .mnote p { margin:0; line-height:1.65; font-size:13.5px; }
  body.page-paper .mnote a { color:var(--red); text-decoration:none; }
  body.page-paper .mnote a:hover { text-decoration:underline; }
  body.page-paper .mnote .dotc { color:var(--cat,var(--red)); }
  @media (max-width:1240px) {
    body.page-paper .wrap { display:block; }
    body.page-paper .mnotes { position:static; margin-top:42px; padding-top:22px; border-top:1px solid var(--line); flex-direction:column; }
  }
  .pubmeta { font-family:"IBM Plex Mono",Consolas,monospace; font-size:12px; letter-spacing:1.2px; color:var(--soft); margin:8px 0 0; }
  .pubmeta b { color:var(--ink); font-weight:500; }
  .epigraph { margin:0 0 28px; padding:18px 22px 16px; border-left:3px solid var(--red); background:#fdfaf7; border-radius:0 8px 8px 0; }
  .epigraph p { margin:0 0 6px; font-size:15.5px; color:var(--ink); font-style:italic; line-height:1.85; }
  .epigraph cite { font-family:"IBM Plex Mono",Consolas,monospace; font-size:11px; letter-spacing:1.5px; color:var(--soft); font-style:normal; }
  /* index views */
  .viewbar { display:flex; align-items:center; gap:6px; margin:0 0 26px; flex-wrap:wrap; }
  .vbtn { font-family:"IBM Plex Mono",Consolas,monospace; font-size:11.5px; letter-spacing:1.5px; color:var(--gray); background:#fff; border:1px solid var(--line); border-radius:99px; padding:4px 14px; cursor:pointer; transition:color .2s,border-color .2s,background .2s; }
  .vbtn:hover { color:var(--red); border-color:var(--red); }
  .vbtn.on { color:var(--red); border-color:var(--red); background:#fdfaf7; }
  .vhint { font-family:"IBM Plex Mono",Consolas,monospace; font-size:11px; letter-spacing:1.5px; color:var(--soft); margin-left:8px; }
  #vhint-r { margin-left:auto; color:var(--red); }
  .gallery { display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:18px; margin:0 0 36px; }
  .gallery a { display:block; position:relative; border:1px solid var(--line); border-radius:10px; overflow:hidden; text-decoration:none; color:inherit; transition:transform .25s ease, box-shadow .25s ease; background:#fff; }
  .gallery a:hover { transform:translateY(-3px); box-shadow:0 6px 22px rgba(0,0,0,.10); }
  .gallery img { display:block; width:100%; height:auto; }
  .gallery .ov { padding:10px 12px 12px; background:#fdfaf7; border-left:3px solid var(--red); }
  .gallery .ov .id { font-family:"IBM Plex Mono",Consolas,monospace; font-size:11px; letter-spacing:2px; color:var(--red); }
  .gallery .ov .ti { font-size:14.5px; font-weight:600; margin-top:2px; color:var(--ink); }
  .gallery .ov .en { font-family:"IBM Plex Mono",Consolas,monospace; font-size:11px; color:var(--soft); margin-top:4px; }
  #star { position:relative; height:380px; border:1px solid var(--line); border-radius:12px; background:linear-gradient(180deg,#fdfaf7 0%,#fff 100%); padding:18px 22px; margin:0 0 36px; }
  #star svg { width:100%; height:100%; display:block; overflow:visible; }
  #star .tip { position:absolute; pointer-events:none; padding:8px 12px; background:#fff; border:1px solid var(--line); border-radius:8px; box-shadow:0 4px 14px rgba(0,0,0,.08); font-size:12.5px; max-width:260px; opacity:0; transition:opacity .15s; }
  #star .tip.on { opacity:1; }
  #star .tip b { color:var(--red); font-family:"IBM Plex Mono",Consolas,monospace; font-size:11px; letter-spacing:1.5px; display:block; margin-bottom:4px; }
  #star .tip .en { color:var(--soft); font-size:11px; }
  /* 藏书章 */
  .readmark { position:absolute; top:14px; right:14px; transform:rotate(-8deg); font-family:"IBM Plex Mono",Consolas,monospace; font-size:11px; letter-spacing:2px; color:#fff; background:var(--red); border:2px solid #fff; padding:3px 9px; border-radius:4px; box-shadow:0 0 0 1px var(--red); display:none; z-index:2; }
  .paper { position:relative; }
  .paper.read .readmark { display:inline-block; }
  @media print {
    .viewbar, #gallery, #star, .mnotes, .pubmeta, .readmark { display:none !important; }
    .epigraph { background:#fff !important; border-left-color:#A02C2C !important; }
    body.page-paper .wrap { display:block; }
  }
"""

V5_SCRIPT = r"""
<script>
/* ---- page enhancements v5 (spec: AGENT.md): read-mark + index views + URL deep-link ---- */
(function () {
  var LS_KEY = "mpa-read";
  function getRead() { try { return JSON.parse(localStorage.getItem(LS_KEY) || "{}"); } catch (e) { return {}; } }
  function setRead(o) { try { localStorage.setItem(LS_KEY, JSON.stringify(o)); } catch (e) {} }
  function arxOfCard(c) { var a = c.querySelector("h3 a"); if (!a) return ""; var m = a.getAttribute("href").match(/(\d{4}\.\d+)/); return m ? m[1] : ""; }

  if (document.body.classList.contains("page-paper")) {
    var wm = document.querySelector(".wm");
    var arx = wm ? (wm.textContent.match(/\d{4}\.\d+/) || [""])[0] : "";
    if (arx) {
      var done = false;
      function mark() {
        if (done) return;
        var o = getRead(); o[arx] = Date.now(); setRead(o); done = true;
        document.body.setAttribute("data-read", arx);
      }
      window.addEventListener("scroll", function () {
        var doc = document.documentElement; var max = doc.scrollHeight - window.innerHeight;
        if (max > 0 && window.scrollY / max > 0.85) mark();
      }, { passive: true });
      setTimeout(mark, 30000);
    }
    return;
  }

  var viewbar = document.getElementById("viewbar");
  if (!viewbar) return;
  var vbtns = viewbar.querySelectorAll(".vbtn");
  var views = { list: null, gallery: document.getElementById("gallery"), star: document.getElementById("star") };
  var hint = document.getElementById("vhint");
  var fread = document.getElementById("vhint-r");
  var cards = [].slice.call(document.querySelectorAll(".wrap > .paper"));
  var current = "list";
  var CAT_COLORS = { FRAMEWORK:"#A02C2C", HARNESS:"#9C6B1E", ACTIVATION:"#6B4FA0", SECURITY:"#2E7D74", "SELF-GENERATIVE":"#A34A7D", ROUTING:"#3E6FA3", DECENTRALIZED:"#557B3F" };

  var DATA = cards.map(function (c) {
    var num = (c.querySelector(".idx").textContent.match(/\d+/) || [""])[0];
    return { num: num, cat: c.getAttribute("data-cat"),
             title: c.querySelector("h3").textContent.trim(),
             en: (c.querySelector(".en") || {}).textContent || "",
             desc: c.querySelector("p").textContent.trim(),
             url: c.querySelector("h3 a").getAttribute("href"),
             arx: arxOfCard(c) };
  });

  function buildGallery() {
    var g = views.gallery; if (g.dataset.built) return;
    g.innerHTML = DATA.map(function (d) {
      return '<a href="' + d.url + '" data-arx="' + d.arx + '" data-cat="' + d.cat + '"><img src="covers/' + d.arx + '.png" alt="' + d.title + '" loading="lazy"><div class="ov"><div class="id">N\u00ba ' + d.num + ' \u00b7 ' + d.cat + '</div><div class="ti">' + d.title + '</div><div class="en">' + d.en + '</div></div></a>';
    }).join("");
    g.dataset.built = "1";
  }
  function buildStar() {
    var s = views.star; if (s.dataset.built) return;
    var N = DATA.length, W = 1000, H = 320;
    var svg = ['<svg viewBox="0 0 ' + W + ' ' + H + '" xmlns="http://www.w3.org/2000/svg">'];
    var pts = DATA.map(function (d, i) {
      var x = 60 + (W - 120) * i / (N - 1);
      var y = H/2 + Math.sin(i * 1.3) * 70 + Math.cos(i * 0.7) * 22;
      return { x: x, y: y, cat: d.cat, arx: d.arx, num: d.num, title: d.title, en: d.en, desc: d.desc, url: d.url };
    });
    for (var i = 0; i < N - 1; i++) svg.push('<line x1="' + pts[i].x + '" y1="' + pts[i].y + '" x2="' + pts[i+1].x + '" y2="' + pts[i+1].y + '" stroke="#E4DFD6" stroke-width="1.5" />');
    pts.forEach(function (p, i) {
      var c = CAT_COLORS[p.cat] || "#A02C2C";
      svg.push('<a href="' + p.url + '" data-arx="' + p.arx + '"><circle cx="' + p.x + '" cy="' + p.y + '" r="13" fill="' + c + '" stroke="#fff" stroke-width="2" /></a>');
      svg.push('<text x="' + p.x + '" y="' + (p.y - 22) + '" text-anchor="middle" font-family="IBM Plex Mono,Consolas,monospace" font-size="12" fill="#8a8a86" letter-spacing="1">N\u00ba ' + p.num + '</text>');
    });
    svg.push('</svg>');
    s.innerHTML = svg.join("") + '<div class="tip" id="startip"></div>';
    var tip = s.querySelector("#startip");
    var circles = [].slice.call(s.querySelectorAll("circle"));
    s.addEventListener("mousemove", function (e) {
      var t = e.target; if (t.tagName !== "CIRCLE") { tip.classList.remove("on"); return; }
      var idx = circles.indexOf(t); if (idx < 0) return;
      var p = pts[idx];
      tip.innerHTML = '<b>N\u00ba ' + p.num + ' \u00b7 ' + p.cat + '</b>' + p.title + '<br><span class="en">' + p.en + '</span>';
      var rect = s.getBoundingClientRect();
      tip.style.left = Math.min(rect.width - 270, e.clientX - rect.left + 12) + "px";
      tip.style.top = (e.clientY - rect.top + 12) + "px";
      tip.classList.add("on");
    });
    s.addEventListener("mouseleave", function () { tip.classList.remove("on"); });
    s.dataset.built = "1";
  }

  function getActiveCat() { var c = document.querySelector(".chip.on"); return c ? (c.getAttribute("data-cat") || "*") : "*"; }
  function getActiveQ() { var q = document.getElementById("q"); return q ? q.value.trim().toLowerCase() : ""; }
  function matches(d, cat, q) {
    var okc = (cat === "*" || d.cat === cat);
    var okq = !q || ((d.title + " " + d.en + " " + d.desc + " " + d.arx).toLowerCase().indexOf(q) !== -1);
    return okc && okq;
  }
  function applyFilterToViews() {
    var cat = getActiveCat(), q = getActiveQ();
    var shown = 0;
    DATA.forEach(function (d, i) {
      var ok = matches(d, cat, q);
      if (current === "list") cards[i].style.display = ok ? "" : "none";
      else if (current === "gallery") {
        var a = views.gallery.querySelector('a[data-arx="' + d.arx + '"]');
        if (a) a.style.display = ok ? "" : "none";
      } else if (current === "star") {
        var anchors = [].slice.call(views.star.querySelectorAll("a[data-arx]"));
        if (anchors[i]) anchors[i].style.opacity = ok ? 1 : 0.18;
      }
      if (ok) shown++;
    });
    var stat = document.getElementById("fltstat");
    if (stat) stat.textContent = "SHOWING " + shown + " / " + DATA.length;
    var none = document.getElementById("fltnone");
    if (none) none.hidden = shown !== 0;
  }
  function syncURL() {
    var p = new URLSearchParams();
    var c = getActiveCat(); if (c !== "*") p.set("cat", c);
    var q = getActiveQ(); if (q) p.set("q", q);
    if (current !== "list") p.set("view", current);
    var qs = p.toString();
    if (qs) history.replaceState(null, "", "?" + qs);
    else history.replaceState(null, "", location.pathname);
  }
  function setView(v) {
    current = v;
    vbtns.forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-view") === v); });
    if (hint) hint.textContent = "展示模式 · " + ({ list: "列表", gallery: "画廊", star: "星图" }[v] || v);
    if (v === "list") { views.gallery.hidden = true; views.star.hidden = true; cards.forEach(function (c) { c.style.display = ""; }); }
    else { cards.forEach(function (c) { c.style.display = "none"; }); }
    if (v === "gallery") { buildGallery(); views.gallery.hidden = false; views.star.hidden = true; }
    else if (v === "star") { buildStar(); views.star.hidden = false; views.gallery.hidden = true; }
    applyFilterToViews(); syncURL();
  }
  vbtns.forEach(function (b) { b.addEventListener("click", function () { setView(b.getAttribute("data-view")); }); });
  var bar = document.getElementById("fltbar");
  if (bar) bar.addEventListener("click", function (e) { if (e.target.classList && e.target.classList.contains("chip")) { setTimeout(function () { applyFilterToViews(); syncURL(); }, 0); } }, true);
  var q = document.getElementById("q"); if (q) q.addEventListener("input", function () { applyFilterToViews(); syncURL(); }, true);

  function paintRead() {
    var o = getRead();
    cards.forEach(function (c) { var arx = arxOfCard(c); if (o[arx]) c.classList.add("read"); });
    var n = Object.keys(o).length;
    if (fread) fread.textContent = "已读 " + n + " / " + DATA.length;
  }
  paintRead();

  var up = new URLSearchParams(location.search);
  var initCat = up.get("cat"); if (initCat) { var ch = document.querySelector('.chip[data-cat="' + initCat + '"]'); if (ch) ch.click(); }
  var initQ = up.get("q"); if (initQ) { var qi = document.getElementById("q"); if (qi) { qi.value = initQ; qi.dispatchEvent(new Event("input")); } }
  var initView = up.get("view"); if (initView && initView !== "list") setView(initView);
})();
</script>
"""


def head_meta_block(arx, p, url, is_index, is_glossary, is_about):
    if is_index:
        ld = ld_index(); cover = SITE + "/covers/index.png"
    elif is_glossary:
        ld = ld_static("术语表 · Glossary", "multi-agent 论文常用术语中英对照（31 条）。", url)
        cover = SITE + "/covers/glossary.png"
    elif is_about:
        ld = ld_static("关于 · About", "收录标准、阅读指南、维护者与许可。", url)
        cover = SITE + "/covers/about.png"
    else:
        ld = ld_paper(arx, p, url)
        cover = SITE + "/covers/" + arx + ".png"
    jsonld = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>\n"
    return (
        '<meta name="theme-color" content="#A02C2C">\n'
        '<link rel="apple-touch-icon" href="apple-touch-icon.png">\n'
        '<link rel="canonical" href="' + url + '">\n'
        '<meta property="og:image" content="' + cover + '">\n'
        '<meta property="og:image:width" content="1200">\n'
        '<meta property="og:image:height" content="630">\n'
        '<meta name="twitter:image" content="' + cover + '">\n'
        + jsonld
    ), cover


def paper_extras(arx, p):
    num = ARX_NUM[arx]
    date = prefix_date(arx)
    cat_cn = V4.CAT_CN.get(p["cat"], p["cat"])
    cat_color = V4.CAT_COLOR.get(p["cat"], RED)

    pubmeta = (
        '<p class="pubmeta">arXiv <b>' + arx + '</b> \u00b7 投稿 <b>' + date + '</b>'
        + (' \u00b7 ' + p["venue"] if p.get("venue") else "")
        + ' \u00b7 中文版收录 <b>' + CITE_DATE + '</b></p>'
    )

    epi = (
        '<blockquote class="epigraph"><p>' + EPIGRAPH[arx] + '</p>'
        '<cite>\u2014 \u672c\u7ad9\u5bfc\u8bfb</cite></blockquote>'
    )

    tids = V4.TERM_LINKS.get(arx, [])
    if tids:
        first = tids[0]
        alias = V4.ALIASES.get(first, [first])[0]
        term_html = '<p>\u6838\u5fc3\u672f\u8bed\uff1a<a href="glossary.html#' + first + '">' + alias + '</a>'
        if len(tids) > 1:
            term_html += ' \u7b49 ' + str(len(tids)) + ' \u4e2a'
        term_html += "</p>"
    else:
        term_html = "<p>\u6682\u65e0\u6620\u5c04\u672f\u8bed</p>"

    prev_arx = ARX_PREV[arx]
    next_arx = ARX_NEXT[arx]
    order_html = "<p>"
    if prev_arx:
        prev_n = V4.PAPER[prev_arx]["og"].split("：")[0]
        order_html += '上一篇：<a href="' + V4.PAPER[prev_arx]["name"] + '_中文版.html">' + prev_n + '</a><br>'
    order_html += '<span style="color:var(--red);">本篇 Nº ' + num + '</span><br>'
    if next_arx:
        next_n = V4.PAPER[next_arx]["og"].split("：")[0]
        order_html += '下一篇：<a href="' + V4.PAPER[next_arx]["name"] + '_中文版.html">' + next_n + '</a>'
    order_html += "</p>"

    notes_html = (
        '<aside class="mnotes" aria-label="\u7f16\u8005\u65c1\u6ce8">'
        '<div class="mnote"><h4>\u9986\u85cf\u4fe1\u606f</h4>'
        '<p>arXiv <b>' + arx + '</b><br>\u6295\u7a3f <b>' + date + '</b><br>'
        '\u4e2d\u6587\u7248\u6536\u5f55 <b>' + CITE_DATE + '</b></p></div>'
        '<div class="mnote"><h4>\u5206\u7c7b</h4>'
        '<p><span class="dotc" style="color:' + cat_color + '">\u25cf</span> <a href="glossary.html#' + p["cat"] + '">' + cat_cn + '</a></p></div>'
        '<div class="mnote"><h4>\u6838\u5fc3\u672f\u8bed</h4>' + term_html + '</div>'
        '<div class="mnote"><h4>\u9605\u8bfb\u987a\u5e8f</h4>' + order_html + '</div>'
        '</aside>'
    )
    return pubmeta, epi, notes_html


def main():
    for name in PAGES_ALL:
        path = BASE + name
        txt = open(path, encoding="utf-8").read()
        n = "\n"
        is_index = name == "index.html"
        is_paper = (not is_index) and name not in ("glossary.html", "about.html")
        is_glossary = name == "glossary.html"
        is_about = name == "about.html"
        arx = None
        p = None
        if is_paper:
            arx = re.match(r"(\d{4}\.\d+)", name).group(1)
            p = V4.PAPER[arx]

        url = SITE + "/" + quote(name)
        meta_block, cover = head_meta_block(arx, p, url, is_index, is_glossary, is_about)

        marker_v5 = "/* ---- v5 enhancements"
        if marker_v5 not in txt:
            txt = txt.replace("</head>", "<style>" + V5_CSS + "</style>\n" + meta_block + "\n<!-- v5-meta-injected -->\n</head>", 1)

        # og:image 归一（历史 dup 根因，勿回退）：meta 块已自带 og:image→width→height 三连对；
        # 若页面还留有 v4 时代的旧 og:image（不在 width 之前），必须删掉而非替换，否则同页出现两条 og:image。
        txt = re.sub(r'<meta property="og:image" content="[^"]*">\n(?!<meta property="og:image:width")', '', txt, count=1)
        if 'name="twitter:image"' in txt:
            txt = re.sub(r'<meta name="twitter:image" content="[^"]*">',
                         '<meta name="twitter:image" content="' + cover + '">', txt, count=1)

        if is_paper:
            if 'class="page-paper"' not in txt:
                txt = txt.replace("<body>", '<body class="page-paper">', 1)
            pubmeta_html, epi_html, notes_html = paper_extras(arx, p)
            if 'class="pubmeta"' not in txt:
                m = re.search(r'(<(?:p|div)[^>]*\bclass="meta"[^>]*>.*?</(?:p|div)>)', txt, flags=re.S)
                if m:
                    txt = txt[:m.end()] + n + pubmeta_html + txt[m.end():]
            if 'class="epigraph"' not in txt:
                tldrm = re.search(r'(\n\n<div class="tldr">)', txt)
                if tldrm:
                    txt = txt[:tldrm.start()] + n + epi_html + n + txt[tldrm.start():]
            if 'class="paper-main"' not in txt:
                txt = txt.replace('<div class="wrap">', '<div class="wrap">' + n + '<div class="paper-main">', 1)
                txt = txt.replace('\n<footer>', n + '</div>' + n + notes_html + n + '<footer>', 1)

        if is_index and 'id="viewbar"' not in txt:
            viewbar = (
                '<div class="viewbar" id="viewbar" role="group" aria-label="\u5207\u6362\u89c6\u56fe">'
                '<button type="button" class="vbtn on" data-view="list">\u5217\u8868</button>'
                '<button type="button" class="vbtn" data-view="gallery">\u753b\u5eca</button>'
                '<button type="button" class="vbtn" data-view="star">\u661f\u56fe</button>'
                '<span class="vhint" id="vhint">\u5c55\u793a\u6a21\u5f0f \u00b7 \u5217\u8868</span>'
                '<span class="vhint" id="vhint-r">\u5df2\u8bfb 0 / 11</span>'
                '</div>'
                '<div id="gallery" class="gallery" hidden></div>'
                '<div id="star" hidden></div>'
            )
            marker = '</p>\n</div>\n\n<div class="paper" data-cat="FRAMEWORK">'
            if marker in txt:
                txt = txt.replace(marker, '</p>\n</div>' + n + n + viewbar + n + '<div class="paper" data-cat="FRAMEWORK">', 1)

        if "page enhancements v5" not in txt:
            bi = txt.rfind("</body>")
            assert bi != -1, name + " no </body>"
            txt = txt[:bi] + V5_SCRIPT + n + txt[bi:]

        open(path, "w", encoding="utf-8", newline="\n").write(txt)
        rep = {
            "v5-css": txt.count(marker_v5),
            "ld+json": txt.count('"@type"'),
            "og:image": txt.count('property="og:image"'),
            "theme-color": txt.count('name="theme-color"'),
            "apple-touch": txt.count('apple-touch-icon'),
            "canonical": txt.count('rel="canonical"'),
            "og-cover": txt.count('/covers/'),
            "pubmeta": txt.count('class="pubmeta"'),
            "epigraph": txt.count('class="epigraph"'),
            "paper-main": txt.count('class="paper-main"'),
            "mnotes": txt.count('class="mnotes"'),
            "viewbar": txt.count('id="viewbar"'),
            "v5-script": txt.count("page enhancements v5"),
        }
        print(name, rep)
        assert txt.count('property="og:image"') == 1, name + " og:image 数量异常（应为 1）"
        assert txt.count('name="twitter:image"') == 1, name + " twitter:image 数量异常（应为 1）"


if __name__ == "__main__":
    main()