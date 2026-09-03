# AGENT.md — 论文 HTML 页面编写规范

本目录（multi-agent-article）是论文中文编译版的静态站点：`index.html` 为目录页，每篇论文一个独立 HTML。**任何 Agent / 人在新增或修改页面时必须遵守本规范**，否则会出现「页面之间无法互相跳转」等回归问题（历史上发生过：① 导航曾被写成 GitHub blob 绝对链接导致全站跳转失效；② TOC/增强组件版本落后）。

---

## 1. 链接：必须用相对路径

**规则：站内页面之间的所有 `<a href>` 一律使用相对路径，禁止任何形式的绝对 URL。**

```html
<!-- ✅ 正确 -->
<a href="index.html">目录</a>
<a href="2603.11445_VMAO_中文版.html">← 上一篇：VMAO</a>
<a href="2603.11445_VMAO_Verified-Multi-Agent-Orchestration.pdf">PDF</a>

<!-- ❌ 禁止 -->
<a href="https://github.com/1parado/multi-agent-article/blob/main/index.html">目录</a>
```

原因：
- 相对路径在本地双击打开、GitHub Pages、任何静态托管下都能跳转；
- `github.com/.../blob/...` 指向的是代码查看页，点击后**不会渲染 HTML**；
- 绝对链接在本地文件系统下直接失效。

允许使用绝对 URL 的唯一场景：站外资源（arXiv 摘要页、arXiv PDF、GitHub 仓库本身）。

PDF 链接规则：本目录存在对应 PDF 文件的用相对路径；不存在的用 `https://arxiv.org/pdf/<id>.pdf`。

## 2. 页面导航链（上一篇 / 目录 / 下一篇）

**规则：每篇论文页底部必须有 `.nav` 导航块，指向关系与 `index.html` 论文列表的顺序严格一致。**

当前确定的顺序（新增论文时追加到末尾，并回写前一页的「下一篇」）：

| # | 文件 | 上一篇 | 下一篇 |
|---|------|--------|--------|
| 01 | 2603.11445_VMAO_中文版.html | —（只有目录） | AdaptOrch |
| 02 | 2602.16873_AdaptOrch_中文版.html | VMAO | NLAH |
| 03 | 2603.25723_NLAH_中文版.html | AdaptOrch | Meta-Harness |
| 04 | 2603.28052_Meta-Harness_中文版.html | NLAH | MUSE |
| 05 | 2606.03005_MUSE_中文版.html | Meta-Harness | MoRe |
| 06 | 2608.27338_MoRe_中文版.html | MUSE | SoK |
| 07 | 2609.00595_SoK_中文版.html | MoRe | MAS² |
| 08 | 2509.24323_MAS2_中文版.html | SoK | OI-MAS |
| 09 | 2601.04861_OI-MAS_中文版.html | MAS² | Symphony-Coord |
| 10 | 2602.00966_Symphony-Coord_中文版.html | OI-MAS | HEART |
| 11 | 2609.01736_HEART_中文版.html | Symphony-Coord | —（只有目录） |

标准模板（首篇无「上一篇」、末篇无「下一篇」，但必须有「目录」）：

```html
<div class="nav">
  <a href="<上一篇文件名>">← 上一篇：<短名></a>
  <a href="index.html">目录</a>
  <a href="<下一篇文件名>">下一篇：<短名> →</a>
</div>
```

另外，页首 `.links` 行中的「目录」链接同样必须指向 `index.html`（相对路径）。

**新增论文的必做步骤**：
1. 在 `index.html` 论文列表末尾追加条目；
2. 新页面 `.nav` 指向 `index.html`，并回写当前末篇页面的「下一篇」；
3. 更新本文件的顺序表与第 5 节类别色表；index 的横向对比表、阅读顺序、篇数、README 表格同步更新；
4. 页面内所有站内链接逐条自检（见第 4 节）。

## 3. 页面增强组件 v2 — 必须包含

每篇论文页（index.html 同样适用，论文页另加 `.wm` 水印）必须包含以下组件。**实现方式：固定的代码块，原样复制，不做改写。**

### 3.1 `<head>` 内：字体链接（在 viewport meta 之后）

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

### 3.2 `</head>` 前：增强样式块

```html
<style>
  /* ---- v2 enhancements (spec: AGENT.md) ---- */
  #pbar { position:fixed; top:0; left:0; height:3px; width:0; background:var(--red); z-index:1200; }
  .dot { display:inline-block; width:8px; height:8px; border-radius:50%; background:var(--cat,var(--red)); margin-right:8px; vertical-align:1px; }
  .eyebrow { color:var(--cat,var(--red)); }
  #toc-panel a.active { color:var(--red); background:#f6f5f3; font-weight:600; }
  .bar { transition:height .9s cubic-bezier(.22,.7,.3,1); }
  .barwrap:hover .bar { filter:brightness(1.1); }
  .reveal { opacity:0; transform:translateY(16px); transition:opacity .6s ease, transform .6s ease; }
  .reveal.in { opacity:1; transform:none; }
  @media (prefers-reduced-motion: reduce) { .reveal { opacity:1; transform:none; transition:none; } .bar { transition:none; } }
  .wrap { position:relative; }
  .wm { position:absolute; top:56px; right:20px; font-family:"IBM Plex Mono",Consolas,monospace; font-size:58px; font-weight:700; letter-spacing:1px; color:var(--red); opacity:.06; user-select:none; pointer-events:none; white-space:nowrap; }
  @media (max-width:700px) { .wm { display:none; } }
</style>
```

外加 TOC 组件基础样式（`#toc-btn` / `#toc-panel` 系列，与 v1 相同，见现有页面）。

### 3.3 `</body>` 前：增强脚本 v2（TOC + scroll-spy + 进度条 + 滚动显现 + 图表动效）

```html
<script>
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
```

组件要点：
- TOC 从 `.wrap` 内收集 `h1`/`h2` 自动生成锚点，滚动时自动高亮当前章节（scroll-spy）；
- 顶部 3px 进度条 `#pbar` 随滚动填充；
- 标题/图表/条目进入视口时淡入上移；`.bar` 条形图入场时从 0 生长——全部尊重 `prefers-reduced-motion`；
- 纯前端零依赖。检查方法：源码含 `#pbar {` 与 `scroll-spy` 即合格。

### 3.4 类别色签（分类色）

每个类别一个专属色，用于论文页 eyebrow（含色点 `.dot`）与 index 列表 `.idx` 行：

| 类别 | 色值 | 论文 |
|------|------|------|
| MULTI-AGENT FRAMEWORK | `#A02C2C` | VMAO、AdaptOrch |
| AGENT HARNESS（含多模态 / TOOL USE） | `#9C6B1E` | NLAH、Meta-Harness、MUSE、HEART |
| ACTIVATION | `#6B4FA0` | MoRe |
| SECURITY | `#2E7D74` | SoK |
| SELF-GENERATIVE | `#A34A7D` | MAS² |
| MODEL ROUTING | `#3E6FA3` | OI-MAS |
| DECENTRALIZED | `#557B3F` | Symphony-Coord |

论文页 eyebrow 写法（`--cat` 内联在 eyebrow 上）：

```html
<div class="eyebrow" style="--cat:#9C6B1E"><span class="dot"></span>PAPER 03 · AGENT HARNESS</div>
```

index 条目写法：`<div class="idx" style="--cat:#9C6B1E"><span class="dot"></span>03 · AGENT HARNESS</div>`

### 3.5 论文页水印 / index Hero

- 论文页：`<div class="wrap">` 后紧跟 `<div class="wm">arXiv <编号></div>`（右上角超大淡色水印，<700px 自动隐藏）；
- index：intro 段后紧跟 `.hero` SVG 插画（编排流水线示意，见现有 index.html，动画线尊重 reduced-motion）。

## 4. 完成前的自检清单

新增或修改页面后，逐项确认：

- [ ] 页内没有任何 `github.com/.../blob/main/` 或 `github.com/.../raw/main/` 形式的站内链接；
- [ ] `.nav` 中「上一篇 / 下一篇」与第 2 节顺序表一致，文件名与磁盘实际文件一一对应（含中文字符完全一致）；
- [ ] 页首 `.links` 的「目录」指向 `index.html`；
- [ ] 源码包含 `#pbar {`（增强样式）、`scroll-spy`（v2 脚本）、`fonts.googleapis.com`（字体链接）；
- [ ] eyebrow 带 `--cat` 与 `.dot`，色值符合第 3.4 节色表；
- [ ] 论文页含 `.wm` 水印；
- [ ] 浏览器中实际点一遍：目录页 → 本页 → 上一篇 → 下一篇 → 目录，全部可达；
- [ ] 滚动页面：顶部进度条填充、右下角 ☰ 出现、目录高亮跟随章节、图表入场生长。

## 5. 其他约定

- 页面样式沿用现有模板（`.wrap` 最大宽 780px、IBM Plex Mono 强调），保持系列一致；
- 文件命名：`<arXiv编号>_<短名>_中文版.html`；
- `index.html` 的论文列表、第 2 节顺序表、第 3.4 节类别色表、README 表格四者保持同步。
