# -*- coding: utf-8 -*-
"""beautify_v6.py — v6 全站注入（目录左上角 + giscus 评论区 + WPS 式批注）。

依赖：beautify_v4.py（PAPER/CAT_COLOR 等元数据；本脚本仅用其 SITE 常量做断言对照）。

注入内容（idempotent，重复运行会被 assertion 拦截）：
  1) </head> 前追加 v6 <style>：
     - #toc-btn/#toc-panel 由右下改为左上角（fixed left:14 top:14 / 面板 top:66 left:14）；
       桌面(≥1040px) 目录按钮常显（opacity/pointer-events !important 压过 v1 的 .show 逻辑），
       移动端保留「滚动后出现」；
     - .giscwrap 评论区容器样式（含 .gistitle/.gismount 加载占位）；
     - .annbar（选中文字悬浮工具条）/ .annmask+.anncard（批注弹层）/ .anntoast（轻提示）样式；
     - @media print 全部隐藏。
  2) </body> 前追加 v6 <script>（标记 `page enhancements v6`）：
     - giscus 懒加载：观察 #giscus，接近视口才注入 giscus.app/client.js；
     - 批注交互：mouseup 选中正文 → 工具条「复制引用 / ✎ 批注」→ 弹层带原文引用 + 文本框，
       一键把「引用块+出处+批注」复制为 Markdown，滚动到评论区引导粘贴发布。

giscus 配置常量（2026-09-03 实测，仓库 1parado/multi-agent-article 已启用 Discussions）：
  repo-id R_kgDOUK42-A · category General · category-id DIC_kwDOUK42-M4DExUU
  mapping=og:title（14 页 og:title 全站唯一，本地/预览/Pages 均落同一讨论串）。
注意：giscus App 需仓库管理员在 github.com/apps/giscus 安装一次；未安装时评论区显示错误提示，安装后无需改动代码。
"""
import io, re, sys, glob, os

BASE = "D:/multi-agent-article/"
MARK = "/* ---- v6 enhancements"
SCRIPT_MARK = "page enhancements v6"

V6_CSS = """
  /* ---- v6 enhancements (spec: AGENT.md): toc-top-left + giscus comments + annotate ---- */
  #toc-btn { right:auto !important; left:14px !important; top:14px !important; bottom:auto !important; }
  #toc-panel { right:auto !important; left:14px !important; top:66px !important; bottom:auto !important; }
  @media (max-width:640px) {
    #toc-btn { left:10px !important; top:10px !important; }
    #toc-panel { left:10px !important; top:60px !important; max-width:82vw !important; }
  }
  @media (min-width:1040px) {
    #toc-btn { opacity:1 !important; pointer-events:auto !important; transform:none !important; }
  }
  .giscwrap { max-width:760px; margin:0 auto; padding:54px 24px 30px; }
  .gistitle { display:flex; flex-wrap:wrap; gap:4px 18px; align-items:baseline; margin-bottom:16px; padding-top:16px; border-top:1px solid var(--line); }
  .gt { font-family:"IBM Plex Mono",Consolas,monospace; font-size:12px; letter-spacing:2.5px; color:var(--red); font-weight:600; }
  .gs { font-size:12.5px; color:var(--soft); }
  .gismount { min-height:220px; }
  .gismount iframe { width:100%; border:0; }
  .giscwrap.hit .gismount { animation:gishit 1.1s ease; border-radius:10px; }
  @keyframes gishit { 0% { box-shadow:0 0 0 0 rgba(160,44,44,.5); } 100% { box-shadow:0 0 0 16px rgba(160,44,44,0); } }
  .annbar { position:fixed; z-index:1500; display:flex; align-items:center; gap:2px; background:#fff; border:1px solid var(--red); border-radius:99px; padding:4px; box-shadow:0 6px 20px rgba(0,0,0,.16); opacity:0; pointer-events:none; transform:translateY(6px); transition:opacity .15s, transform .15s; }
  .annbar.on { opacity:1; pointer-events:auto; transform:none; }
  .annbar button { border:0; background:transparent; color:var(--gray); font-size:12.5px; padding:4px 12px; border-radius:99px; cursor:pointer; white-space:nowrap; }
  .annbar button:hover { background:#fdf0ef; color:var(--red); }
  .annbar .sp { width:1px; height:15px; background:var(--line); }
  .annbar button.pri { background:var(--red); color:#fff; }
  .annbar button.pri:hover { background:#8a2424; color:#fff; }
  .annmask { position:fixed; inset:0; z-index:2000; background:rgba(26,26,26,.36); display:flex; align-items:center; justify-content:center; padding:20px; opacity:0; pointer-events:none; transition:opacity .15s; }
  .annmask.on { opacity:1; pointer-events:auto; }
  .anncard { width:min(580px,100%); max-height:84vh; overflow:auto; background:#fff; border-radius:14px; box-shadow:0 18px 50px rgba(0,0,0,.22); padding:20px 22px 16px; }
  .anncard h4 { margin:0 0 3px; font-family:"IBM Plex Mono",Consolas,monospace; font-size:11px; letter-spacing:2px; color:var(--red); }
  .anncard .pos { font-size:12px; color:var(--soft); margin-bottom:12px; }
  .annq { margin:0 0 12px; padding:10px 14px; background:#fdf7f3; border:1px solid var(--line); border-left:3px solid var(--red); border-radius:0 8px 8px 0; color:var(--gray); font-size:13.5px; line-height:1.8; max-height:150px; overflow:auto; white-space:pre-wrap; word-break:break-word; }
  .anncard textarea { width:100%; min-height:96px; resize:vertical; border:1px solid var(--line); border-radius:8px; padding:9px 12px; font:13.5px/1.8 -apple-system,"Segoe UI","Microsoft YaHei",system-ui,sans-serif; color:var(--ink); background:#fdfcfb; }
  .anncard textarea:focus { outline:none; border-color:var(--red); background:#fff; }
  .annacts { display:flex; justify-content:flex-end; gap:8px; margin-top:12px; align-items:center; }
  .annacts .hint { margin-right:auto; font-size:12px; color:var(--soft); }
  .abtn { border:1px solid var(--line); background:#fff; color:var(--gray); border-radius:99px; padding:6px 16px; cursor:pointer; font-size:13px; }
  .abtn:hover { border-color:var(--red); color:var(--red); }
  .abtn.ok { border-color:var(--red); background:var(--red); color:#fff; }
  .anntoast { position:fixed; left:50%; bottom:34px; transform:translate(-50%,10px); z-index:2100; background:var(--ink); color:#fff; font-size:13px; padding:9px 18px; border-radius:99px; box-shadow:0 8px 24px rgba(0,0,0,.25); opacity:0; pointer-events:none; transition:opacity .2s, transform .2s; max-width:86vw; text-align:center; }
  .anntoast.on { opacity:1; transform:translate(-50%,0); }
  .anntoast b { color:#f4cfc8; }
  @media print {
    .giscwrap, .annbar, .annmask, .anntoast { display:none !important; }
  }
"""

GISCUS_BLOCK = """
<section class="giscwrap" id="giscus" data-repo="1parado/multi-agent-article" data-repo-id="R_kgDOUK42-A" data-category="General" data-category-id="DIC_kwDOUK42-M4DExUU" data-mapping="og:title" data-strict="0" data-reactions-enabled="1" data-emit-metadata="0" data-input-position="top" data-theme="light" data-lang="zh-CN" aria-label="评论与批注">
  <div class="gistitle"><span class="gt">DISCUSSION</span><span class="gs">选中正文任意文字 → 点「✎ 批注」即可带原文引用发言 · 需 GitHub 登录</span></div>
  <div class="gismount"></div>
</section>
"""

V6_SCRIPT = """
<script>
/* ---- page enhancements v6 (spec: AGENT.md): giscus comments + text annotate ---- */
(function () {
  "use strict";
  /* ===== giscus 懒加载 ===== */
  var gwrap = document.getElementById("giscus");
  if (gwrap) {
    var gLoaded = false;
    function loadGiscus() {
      if (gLoaded) return; gLoaded = true;
      var box = gwrap.querySelector(".gismount"); if (!box) return;
      var s = document.createElement("script");
      ["repo","repo-id","category","category-id","mapping","strict","reactions-enabled","emit-metadata","input-position","theme","lang"].forEach(function (k) {
        var v = gwrap.getAttribute("data-" + k); if (v != null) s.setAttribute("data-" + k, v);
      });
      s.src = "https://giscus.app/client.js"; s.crossOrigin = "anonymous"; s.async = true;
      box.appendChild(s);
    }
    if ("IntersectionObserver" in window) {
      var gio = new IntersectionObserver(function (en) {
        if (en.some(function (e) { return e.isIntersecting; })) { loadGiscus(); gio.disconnect(); }
      }, { rootMargin: "1400px 0px" });
      gio.observe(gwrap);
    } else {
      window.addEventListener("load", function () { setTimeout(loadGiscus, 700); });
    }
  }

  /* ===== 选中批注（WPS 式：引原文 → 评论） ===== */
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var bar = null, mask = null, toast = null, annQuote = "", annHead = "";

  function clean(s) { return s.replace(/\\s+/g, " ").replace(/^[\\s\\u00a0]+|[\\s\\u00a0]+$/g, ""); }
  function cap(s, n) { n = n || 300; return s.length > n ? s.slice(0, n - 1) + "…" : s; }
  function copyTxt(txt, ok) {
    function fb() {
      var ta = document.createElement("textarea");
      ta.value = txt; ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      var done = false;
      try { done = document.execCommand("copy"); } catch (e) {}
      document.body.removeChild(ta); if (ok) ok(done);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(function () { ok && ok(true); }, fb);
    else fb();
  }
  function toastMsg(html, ms) {
    if (!toast) return;
    toast.innerHTML = html; toast.classList.add("on");
    clearTimeout(toast._t);
    toast._t = setTimeout(function () { toast.classList.remove("on"); }, ms || 4200);
  }
  function jumpGiscus() {
    if (!gwrap) return;
    gwrap.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
    gwrap.classList.remove("hit"); void gwrap.offsetWidth; gwrap.classList.add("hit");
    setTimeout(function () { gwrap.classList.remove("hit"); }, 1300);
  }
  function buildUI() {
    if (bar) return;
    bar = document.createElement("div"); bar.className = "annbar"; bar.setAttribute("role", "toolbar"); bar.setAttribute("aria-label", "批注工具");
    var b1 = document.createElement("button"); b1.type = "button"; b1.innerHTML = "✎ 写批注"; b1.className = "pri";
    var b2 = document.createElement("button"); b2.type = "button"; b2.textContent = "复制引用";
    var sp = document.createElement("span"); sp.className = "sp";
    bar.appendChild(b1); bar.appendChild(sp); bar.appendChild(b2);
    b1.addEventListener("click", openModal); b2.addEventListener("click", function () {
      if (!annQuote) return;
      copyTxt(annQuote, function (okc) {
        toastMsg(okc ? "引用已复制 ✓" : "复制失败，请手动选择复制");
      });
      hideBar();
    });
    document.body.appendChild(bar);

    mask = document.createElement("div"); mask.className = "annmask"; mask.setAttribute("role", "dialog"); mask.setAttribute("aria-modal", "true"); mask.setAttribute("aria-label", "写批注");
    mask.innerHTML =
      '<div class="anncard">' +
      '<h4>WRITE AN ANNOTATION · 写批注</h4>' +
      '<div class="pos"></div>' +
      '<div class="annq"></div>' +
      '<textarea placeholder="写下你的看法、疑问或补充……（发布到下方评论区，所有人可见）"></textarea>' +
      '<div class="annacts"><span class="hint">提交后复制到剪贴板 → 粘贴到评论区即可发布</span>' +
      '<button type="button" class="abtn" data-act="cancel">取消</button>' +
      '<button type="button" class="abtn ok" data-act="go">复制批注 · 去评论区</button></div>' +
      '</div>';
    document.body.appendChild(mask);
    mask.addEventListener("click", function (e) {
      if (e.target === mask) closeModal();
      var btn = e.target.closest("[data-act]");
      if (!btn) return;
      if (btn.getAttribute("data-act") === "cancel") closeModal();
      else submitAnno();
    });
    var kd = function (e) {
      if (!mask.classList.contains("on")) return;
      if (e.key === "Escape") { e.stopPropagation(); closeModal(); }
      if ((e.key === "ArrowLeft" || e.key === "ArrowRight")) { e.preventDefault(); e.stopPropagation(); }
    };
    document.addEventListener("keydown", kd, true);
    document.addEventListener("keydown", function (e) {
      if (e.key !== "ArrowLeft" && e.key !== "ArrowRight") return;
      var t = e.target; if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA")) return;
      var s = window.getSelection();
      if ((s && !s.isCollapsed) || (bar.classList.contains("on"))) { e.preventDefault(); e.stopPropagation(); }
    }, true);

    toast = document.createElement("div"); toast.className = "anntoast"; toast.setAttribute("role", "status");
    document.body.appendChild(toast);
  }
  function hideBar() { if (bar) bar.classList.remove("on"); }
  function openModal() {
    if (!annQuote) return;
    buildUI(); hideBar();
    var head = annHead || nearestHead();
    mask.querySelector(".pos").textContent = (head ? "章节 · " + head + "　·　" : "") + "摘自《" + pageTitle() + "》";
    var q = mask.querySelector(".annq");
    q.textContent = annQuote;
    mask.classList.add("on");
    var ta = mask.querySelector("textarea");
    ta.value = ""; setTimeout(function () { ta.focus(); }, 30);
  }
  function closeModal() { if (mask) mask.classList.remove("on"); }
  function pageTitle() {
    var og = document.querySelector('meta[property="og:title"]');
    return og ? og.getAttribute("content") : document.title;
  }
  function nearestHead() {
    var s = window.getSelection(); if (!s || s.rangeCount === 0) return "";
    var r = s.getRangeAt(0);
    var node = r.commonAncestorContainer; var el = node.nodeType === 1 ? node : node.parentElement;
    var n = el, depth = 0;
    while (n && n.nodeType === 1 && depth < 14) {
      if (/^H[1-3]$/.test(n.tagName)) {
        var txt = clean(n.textContent || "");
        return txt ? cap(txt, 40) : "";
      }
      n = n.parentNode; depth++;
    }
    return "";
  }
  document.addEventListener("mouseup", function (e) {
    buildUI();
    if (e.target && e.target.closest && e.target.closest(".giscwrap, .annmask, .annbar")) { hideBar(); return; }
    setTimeout(function () {
      var s = window.getSelection();
      if (!s || s.isCollapsed || !s.toString().trim()) { hideBar(); return; }
      var txt = clean(s.toString());
      if (txt.length < 4) { hideBar(); return; }
      var r = s.getRangeAt(0);
      var rc = r.commonAncestorContainer;
      var el = rc.nodeType === 1 ? rc : (rc.parentElement || null);
      if (!el || !el.closest(".wrap")) { hideBar(); return; }
      var rect = r.getBoundingClientRect();
      if ((rect.width < 4 && rect.height < 4) && s.anchorNode && s.anchorNode.parentElement) {
        rect = s.anchorNode.parentElement.getBoundingClientRect();
      }
      annQuote = cap(txt);
      annHead = nearestHead();
      var w = Math.min(bar.offsetWidth, 240);
      bar.style.left = Math.max(8, Math.min(window.innerWidth - w - 8, rect.left + rect.width / 2 - w / 2)) + "px";
      bar.style.top = Math.max(6, rect.top - 54) + "px";
      bar.classList.add("on");
    }, 10);
  });
  document.addEventListener("selectionchange", function () {
    var s = window.getSelection(); if (!s || s.isCollapsed) hideBar();
  });
  window.addEventListener("scroll", hideBar, { passive: true });
  window.addEventListener("resize", hideBar);
  function submitAnno() {
    var ta = mask.querySelector("textarea");
    var body = clean(ta.value);
    if (!body) { ta.focus(); return; }
    var head = annHead || nearestHead();
    var md = "> " + annQuote.split("\\n").join("\\n> ") +
      "\\n>\\n> —— 摘自《" + pageTitle() + "》" + (head ? " · " + head : "") +
      "\\n\\n" + body +
      "\\n\\n<sub>via 「选中文字 → ✎ 批注」</sub>";
    copyTxt(md, function (okc) {
      closeModal();
      toastMsg(okc
        ? "批注已复制 ✓ 点击下方评论区输入框粘贴提交（需 GitHub 登录）"
        : "复制失败，请重试");
      jumpGiscus();
    });
  }
})();
</script>
"""


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    papers = [os.path.basename(p) for p in glob.glob(BASE + "*_中文版.html")]
    pages = ["index.html"] + sorted(papers) + ["glossary.html", "about.html"]
    for name in pages:
        path = BASE + name
        txt = open(path, encoding="utf-8").read()
        n = "\n"
        # 1) head v6 样式
        if MARK not in txt:
            assert "</head>" in txt, name
            txt = txt.replace("</head>", "<style>" + V6_CSS + "</style>\n<!-- v6-style-injected -->\n</head>", 1)
        # 2) giscus 容器（每页唯一）
        if 'id="giscus"' not in txt:
            bi = txt.rfind("</body>")
            assert bi != -1, name
            txt = txt[:bi] + GISCUS_BLOCK + n + txt[bi:]
        # 3) v6 脚本
        if SCRIPT_MARK not in txt:
            bi = txt.rfind("</body>")
            assert bi != -1, name
            txt = txt[:bi] + V6_SCRIPT + n + txt[bi:]
        open(path, "w", encoding="utf-8", newline="\n").write(txt)
        rep = {
            "v6-css": txt.count(MARK),
            "giscus-wrap": txt.count('id="giscus"'),
            "gismount": txt.count('class="gismount"'),
            "v6-script": txt.count(SCRIPT_MARK),
            "toc-left": ('#toc-btn { right:auto !important; left:14px' in txt),
            "ann-ui": txt.count("annbar"),
            "print-hide": txt.count(".giscwrap, .annbar, .annmask, .anntoast"),
        }
        assert txt.count('id="giscus"') == 1, name + " giscus 容器数异常"
        assert txt.count(SCRIPT_MARK) == 1, name + " v6 脚本数异常"
        print(name, rep)


if __name__ == "__main__":
    main()
