# AGENT.md — 论文 HTML 页面编写规范 v6

本目录（multi-agent-article）是论文中文编译版的静态站点：`index.html` 为目录页，每篇论文一个独立 HTML，另有 `glossary.html`（术语表）、`about.html`（关于）、`covers/`（期刊封面）、404 等站点文件；**v6 起每页带 giscus 评论区与「选中即批注」交互**。**任何 Agent / 人在新增或修改页面时必须遵守本规范**，否则会出现「页面之间无法互相跳转」「组件版本落后」等回归问题（历史上发生过：① 导航被写成 GitHub blob 绝对链接导致全站跳转失效；② 增强组件版本不一致；③ 引用条注入多出游离 `</div>`；④ index 页脚检测逻辑误判注入失败；⑤ v5 注入在带旧 og:image 的页面上留下两条 og:image）。

---

## 0. 站点文件清单与页面类型

| 页面 | 类型 | 说明 |
|------|------|------|
| index.html | 目录页 | 论文列表（每项带 `data-cat`）+ 横向对比表 + 趋势 + 阅读顺序 + `#fltbar` 筛选检索 + v5 三视图（`.viewbar`：列表/画廊/星图）与已读藏书章 |
| `<arXiv号>_<短名>_中文版.html`（11 篇） | 论文页 | 属于导航链（见 §2）；v5 起带 `.pubmeta`、`.epigraph`、`body.page-paper`；**v5 后续：`.mnotes` 旁注栏与 `.paper-main` 双栏均已移除，回到单栏正文** |
| glossary.html | 术语表 | 不属于导航链；词条 `id` 供各页 `.gloss` 链接（见 §4.6） |
| about.html | 关于 | 不属于导航链；维护信息、收录标准、更新记录、许可措辞 |
| covers/ | 期刊封面 | 14 张 1200×630 PNG（11 论文 + index/glossary/about），每页 `og:image` 指向自己的那张；**新增论文须补一张同规格、同风格的封面**（双层红框 + 纸本横纹 + 幽灵编号 + 拓扑点线，见 §4.11） |
| 404.html | 错误页 | 统一图元（红框 404 印章），含回首页/术语表/关于/GitHub 链接 |
| LICENSE | 许可 | 原创内容 CC BY-NC 4.0 + 第三方论文版权声明（见 about.html 引用措辞） |
| robots.txt | SEO | `Allow: /` + Sitemap 指向 |
| sitemap.xml | SEO | 14 条 URL（index/glossary/about + 11 论文，含 lastmod/priority），**新增论文须追加** |
| favicon.svg | 站身份 | 所有页面 `<head>` 必须引用 |
| apple-touch-icon.png | 站身份 | 180×180 红底 planner→agents 点线图标；所有页面 `<head>` 引用 |
| hero.svg / *.pdf | 资源 | hero 仅作 index 编排插画素材（不再作 og:image，og:image 一律用 covers PNG）；PDF 见 §1 链接规则 |

特殊页（glossary / about）底部导航写法：
```html
<div class="nav"><a href="index.html">← 返回目录</a><a href="about.html">关于本站</a></div>
```
左侧可含 `←`（返回目录），但**右侧禁止**放以 `→` 结尾的链接（否则键盘翻页会把「右箭头」误解为下一篇并跳回同一页）。

## 1. 链接：必须用相对路径

**规则：站内页面之间的所有 `<a href>` 一律使用相对路径，禁止任何形式的绝对 URL。**

```html
<!-- ✅ 正确 -->
<a href="index.html">目录</a>
<a href="2603.11445_VMAO_中文版.html">← 上一篇：VMAO</a>
<a href="glossary.html#dag">DAG</a>
<a href="2603.11445_VMAO_Verified-Multi-Agent-Orchestration.pdf">PDF</a>

<!-- ❌ 禁止 -->
<a href="https://github.com/1parado/multi-agent-article/blob/main/index.html">目录</a>
```

原因：相对路径在本地双击打开、GitHub Pages、任何静态托管下都能跳转；`github.com/.../blob/...` 指向代码查看页，点击后**不会渲染 HTML**。

允许使用绝对 URL 的场景：站外资源（arXiv、GitHub 仓库本身 `https://github.com/1parado/multi-agent-article`、og:image 的 Pages 地址）。

PDF 链接规则：本目录存在对应 PDF 文件的用相对路径（当前仅 VMAO / AdaptOrch / NLAH / Meta-Harness / MUSE 五篇有本地 PDF）；不存在的用 `https://arxiv.org/pdf/<id>.pdf`。**README 表格中的 PDF 链接必须与之一致**（历史上 MoRe/SoK/MAS² 曾误写成本地 raw 链接导致死链）。

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

注意：「上一篇」文案必须以 `←` 开头、「下一篇」以 `→` 结尾——键盘翻页脚本靠这两个字符识别方向。页首 `.links` 行中的「目录」链接同样必须指向 `index.html`（相对路径）。

**新增论文的必做步骤**：
1. 在 `index.html` 论文列表末尾追加条目（并补 `data-cat` 属性，见 §5 色表映射）；
2. 新页面 `.nav` 指向 `index.html`，并回写当前末篇页面的「下一篇」；
3. 更新本文件的顺序表、色表、`README` 表格、`about.html` 收录说明与篇数文案；
4. 补上 `.pubmeta`（arXiv 号 / 投稿月份 / 收录日）与 `.epigraph`（一句话导读），写法见 §4.9；并按 §4.2 补齐 head 的 canonical / JSON-LD / og 三连对；
5. 补一张 `covers/<arXiv号>.png`（1200×630，风格见 §4.11），并让本页 `og:image` 指向它；
6. 在 `sitemap.xml` 末尾追加该页 `<url>`；
7. 页面内所有站内链接逐条自检（见 §8 自检清单）；

## 3. 页面增强组件 v1–v3 — 论文页与 index 必须包含

**实现方式：固定的代码块，原样复制，不做改写。** 组件历史：v1 TOC / v2（进度条、色签、reveal、水印、Hero）/ v3（返回顶部、章节编号、锚点复制、键盘翻页、对比表升级、移动端）/ v5（封面、pubmeta/epigraph、JSON-LD、三视图、站身份；**后续：旁注栏 + 双栏均移除**）。全部页面已内置，逐项核验标准：

- `<head>` 含 **v4 字体异步块**（见 §4.1）；
- `</head>` 前依次为：样式块 A（TOC widget + v2 增强）、样式块 B（v3 增强）、样式块 C（v4 增强，见 §4.3）、样式块 D（v5 增强，搜索 `v5 enhancements`）；
- `</body>` 前依次为：增强脚本 v3（搜索 `page enhancements v3`）、脚本 v4（搜索 `page enhancements v4`）、脚本 v5（搜索 `page enhancements v5`，见 §4.10）；
- 类别色签（§5）、GitHub 图标（`.ghlink`）、论文页水印 `.wm`、对比表 `table.cmp`、Hero SVG 等 v2/v3 细节以现有页面为准。

检查方法：源码含 `page enhancements v3`、`page enhancements v4`、`page enhancements v5`、`#pbar {`、`#totop {`、`#fltbar`（index）/`#cite-json`（论文页）、`favicon.svg`、`property="og:title"` 即合格。

## 4. 页面增强组件 v4 — 全部页面必须包含

### 4.1 字体异步加载（替换旧的同步 `<link>`）

旧写法 `<link href="...css2?family=IBM+Plex+Mono..." rel="stylesheet">` **已废弃**，一律使用（防 Google Fonts 阻塞渲染，境内网络友好）：

```html
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet"></noscript>
```

### 4.2 favicon、OG/Twitter 分享 meta 与站身份/结构化数据

**og:image 一律指向本页专属的 `covers/` PNG（1200×630），不再用 hero.svg。** 映射：论文页 → `covers/<arXiv号>.png`；index → `covers/index.png`；glossary → `covers/glossary.png`；about → `covers/about.png`。

`<head>` 中「字体块之后」的基础 OG 块（v4，每页一份）：

```html
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<meta property="og:type" content="article"> <!-- index/glossary/about 用 website -->
<meta property="og:site_name" content="Multi-Agent Paper Digest 2026">
<meta property="og:title" content="<中文标题>">
<meta property="og:description" content="<一句话介绍，<150 字>">
<meta property="og:url" content="https://1parado.github.io/multi-agent-article/<percent-encoded文件名>">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<同 og:title>">
<meta name="twitter:description" content="<同 og:description>">
<meta name="description" content="<同 og:description>">
```

`</head>` 前的 **v5 追加块**（在样式块 D 之后，全站各页保持一致，勿手改；og:image 三连对必须相邻且全页唯一——历史 dup 教训）：

```html
<meta name="theme-color" content="#A02C2C">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="canonical" href="https://1parado.github.io/multi-agent-article/<percent-encoded文件名>">
<meta property="og:image" content="https://1parado.github.io/multi-agent-article/covers/<本页>.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:image" content="https://1parado.github.io/multi-agent-article/covers/<本页>.png">
<script type="application/ld+json">…</script>
```

JSON-LD 类型：论文页 `ScholarlyArticle`（headline/name/alternativeHeadline/url/datePublished/dateModified/isPartOf/description/keywords/publisher）；index `WebSite`；glossary/about `WebPage`。新增论文的 og:title / og:description 素材直接取自 index 列表的 h3 与 p 描述。

### 4.3 v4 样式块（`</head>` 前的最后一个 `<style>`）

```css
/* ---- v4 enhancements (spec: AGENT.md): print / focus / cite / filter / footlinks / gloss ---- */
a:focus-visible, button:focus-visible, input:focus-visible { outline:2px solid var(--red); outline-offset:2px; }
.gloss { color:inherit; text-decoration:underline; text-decoration-style:dotted; text-decoration-color:var(--sage); text-underline-offset:4px; cursor:help; }
.gloss:hover { color:var(--red); text-decoration-color:var(--red); }
.citebar { display:flex; align-items:center; gap:10px; margin:0 0 2px; flex-wrap:wrap; }
.citecap { font-family:"IBM Plex Mono",Consolas,monospace; font-size:11px; letter-spacing:2px; color:var(--soft); }
.citebtn { font-family:"IBM Plex Mono",Consolas,monospace; font-size:11.5px; letter-spacing:1px; color:var(--red); background:none; border:1px solid var(--line); border-radius:99px; padding:3px 12px; cursor:pointer; transition:border-color .2s, background .2s, color .2s; }
.citebtn:hover { border-color:var(--red); background:#fbf7f4; }
.citebtn.ok { color:#fff; background:var(--red); border-color:var(--red); }
footer a { color:var(--soft); text-decoration:none; }
footer a:hover { color:var(--red); text-decoration:underline; }
.sitefoot { text-align:center; color:var(--soft); font-size:12.5px; margin-top:70px; font-family:"IBM Plex Mono",Consolas,monospace; }
.sitefoot .fl1 { margin-bottom:10px; letter-spacing:1px; }
.sitefoot .fl1 .ghlink { color:inherit; }
.sitefoot .fl1 .ghlink:hover { color:var(--red); }
.sitefoot .fl2 { font-size:11.5px; letter-spacing:1.5px; }
.sitefoot .fl2 a { color:var(--soft); text-decoration:none; margin:0 8px; }
.sitefoot .fl2 a:hover { color:var(--red); text-decoration:underline; }
.fltbar { display:flex; flex-wrap:wrap; align-items:center; gap:10px 12px; margin:2px 0 30px; }
.flt { display:flex; flex-wrap:wrap; gap:8px; }
.chip { font-family:"IBM Plex Mono",Consolas,monospace; font-size:11px; letter-spacing:1.2px; color:var(--gray); background:#fff; border:1px solid var(--line); border-radius:99px; padding:4px 12px; cursor:pointer; transition:color .2s, border-color .2s, box-shadow .2s, background .2s; }
.chip .dot { width:6px; height:6px; margin-right:7px; vertical-align:1px; }
.chip:hover { color:var(--ink); border-color:var(--cat,var(--red)); }
.chip.on { color:var(--cat,var(--red)); border-color:var(--cat,var(--red)); box-shadow:0 0 0 1px var(--cat,var(--red)) inset; background:#fdfaf7; }
.q { flex:1 1 200px; min-width:170px; font:14px -apple-system,"Segoe UI","Microsoft YaHei",system-ui,sans-serif; color:var(--ink); background:#fdfcfb; border:1px solid var(--line); border-radius:8px; padding:7px 12px; }
.q:focus { outline:none; border-color:var(--red); background:#fff; }
.fltstat { width:100%; font-family:"IBM Plex Mono",Consolas,monospace; font-size:11px; letter-spacing:1.5px; color:var(--soft); }
.fltnone { font-size:14px; color:var(--gray); }
@media (max-width:640px) { .citecap { display:none; } .fltbar { gap:8px; } }
@media print {
  #pbar, #toc-btn, #toc-panel, #totop, .wm, .hlink, #fltbar, .fltnone, .fltstat, #q { display:none !important; }
  .reveal { opacity:1 !important; transform:none !important; }
  body { font-size:12px; line-height:1.7; }
  .wrap { padding-top:24px; }
  h2 { page-break-after:avoid; }
  .contrib, .chart, table.cmp, .paper, .trend, .term { page-break-inside:avoid; }
  .bar, .bar.red, .bar.sage, .dot { print-color-adjust:exact; -webkit-print-color-adjust:exact; }
}
```

### 4.4 v4 脚本（`</body>` 前，紧随 v3 脚本之后）

```html
<script>
/* ---- page enhancements v4 (spec: AGENT.md): print-prep + cite + index filter/search ---- */
(function () {
  /* 打印前把未滚动到的入场动效/条形图展开为最终态 */
  function expandAll() {
    [].slice.call(document.querySelectorAll(".reveal:not(.in)")).forEach(function (el) { el.classList.add("in"); });
    [].slice.call(document.querySelectorAll(".bar")).forEach(function (b) { if (b.dataset.h) b.style.height = b.dataset.h; });
  }
  if (window.matchMedia) {
    var mq = window.matchMedia("print");
    if (mq.addEventListener) mq.addEventListener("change", function (m) { if (m.matches) expandAll(); });
    else if (mq.addListener) mq.addListener(function (m) { if (m.matches) expandAll(); });
  }
  document.addEventListener("beforeprint", expandAll);

  /* 论文页：引用复制（BibTeX / APA） */
  var cd = document.getElementById("cite-json");
  if (cd) {
    var data = {};
    try { data = JSON.parse(cd.textContent); } catch (e) {}
    function copyText(txt, ok) {
      function fallback() {
        var ta = document.createElement("textarea");
        ta.value = txt; document.body.appendChild(ta); ta.select();
        try { document.execCommand("copy"); } catch (e) {}
        document.body.removeChild(ta); ok();
      }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(ok, fallback);
      else fallback();
    }
    [].slice.call(document.querySelectorAll("[data-cite]")).forEach(function (b) {
      b.addEventListener("click", function () {
        var k = b.getAttribute("data-cite");
        if (!data[k]) return;
        var old = b.textContent;
        copyText(data[k], function () {
          b.textContent = "✓ 已复制";
          b.classList.add("ok");
          setTimeout(function () { b.textContent = old; b.classList.remove("ok"); }, 1600);
        });
      });
    });
  }

  /* index：分类筛选 + 关键词检索 */
  var bar = document.getElementById("fltbar");
  if (bar) {
    var cards = [].slice.call(document.querySelectorAll(".wrap > .paper"));
    var chips = [].slice.call(bar.querySelectorAll(".chip"));
    var q = document.getElementById("q");
    var stat = document.getElementById("fltstat");
    var none = document.getElementById("fltnone");
    var cat = "*", query = "";
    function cardText(c) {
      var parts = c.querySelectorAll(".idx, h3, .en, p");
      var s = "";
      [].slice.call(parts).forEach(function (el) { s += " " + (el.textContent || ""); });
      return s.toLowerCase();
    }
    function apply() {
      var shown = 0;
      cards.forEach(function (c) {
        var okc = (cat === "*" || c.getAttribute("data-cat") === cat);
        var okq = true;
        if (query) okq = cardText(c).indexOf(query) !== -1;
        var show = okc && okq;
        c.style.display = show ? "" : "none";
        if (show) shown++;
      });
      if (stat) stat.textContent = "SHOWING " + shown + " / " + cards.length;
      if (none) none.hidden = shown !== 0;
    }
    chips.forEach(function (ch) {
      ch.addEventListener("click", function () {
        cat = ch.getAttribute("data-cat") || "*";
        chips.forEach(function (x) { x.classList.toggle("on", x === ch); });
        apply();
      });
    });
    if (q) q.addEventListener("input", function () { query = q.value.trim().toLowerCase(); apply(); });
    apply();
  }
})();
</script>
```

### 4.5 论文页引用条（仅论文页）

`.links` 行之后、`.tldr` 之前，紧跟以下结构（**注意只保留一个 `</div>` 闭合 `.links`，勿多加游离闭合标签**——历史 bug）：

```html
</div>

<div class="citebar"><span class="citecap">CITE</span><button type="button" class="citebtn" data-cite="bib">BibTeX</button><button type="button" class="citebtn" data-cite="apa">APA</button></div>
<script type="application/json" id="cite-json">{"bib":"@misc{<key>,\n  title={...},\n  ...}","apa":"<APA 一行引用>"}</script>

<div class="tldr">
```

`cite-json` 生成规则：`bib` 为 BibTeX（字段 title/author/year/eprint/archiveprefix/url，`@misc`；作者缺失时用机构并注明「作者详见 arXiv」）；`apa` 为 `作者标注（年份）. 英文标题. arXiv:<id>. https://arxiv.org/abs/<id>`。新增论文须在**页内 `#cite-json`** 中登记 key/title/auth/year/venue/og/desc/cat 元数据。

### 4.6 术语链（正文 → glossary.html）

- 论文页正文（`.tldr` 起至 `.nav` 止，且**不进入 h2/h3 标题内部**）将核心概念首次出现处包成 `<a class="gloss" href="glossary.html#<id>">词</a>`，点状下划线视觉；
- 每个论文页保留 3–5 个术语链即可（当前映射以现有页面为准，别名按出现偏好排列；**注入时必须屏蔽 h2/h3 与已有标签内部**，否则会污染标题与既有 `<a>`——历史教训）；
- **新增术语**必须三步同步：glossary.html 增加 `<div class="term" id="<id>">` 词条 → 本文件 §6 的术语 id 目录 → 需要链接它的页面正文注入 `.gloss`；
- 术语 alias 不得与其他已注入锚点词重叠（避免嵌套链接）。

### 4.7 index 筛选与检索（仅 index.html）

`<h2>论文列表</h2>` 之后紧跟 `#fltbar`：7 个类别 chip + 检索框 `#q` + 状态行 `#fltstat` + 空态 `#fltnone`（完整 markup 见 index.html，新增论文时只需给新卡片补 `data-cat`）。chip 类别与颜色必须与 §5 色表一致。

### 4.8 页脚

- index：`<footer class="sitefoot">` 两行（fl1 GitHub 链接、fl2 首页/术语表/关于/反馈/版权）——见 index.html 现状，勿回退为单行；
- 论文页：既有单行 footer 内容后追加 ` · <a href="glossary.html">术语表</a> · <a href="about.html">关于</a>`；
- glossary / about：自带 footer（返回目录 + 链接）。

### 4.9 v5 论文页增强（仅 11 篇论文页）

论文页 `<body class="page-paper">`，正文包在 `<div class="wrap">…</div>` 内，**单栏，无右侧 sidebar**。必备两个元素：

- **`.pubmeta`**：紧跟在 `.meta` 之后的一行（`.meta` 的 `</p>` 后）：`arXiv <号> · 投稿 <年-月> [· venue] · 中文版收录 2026-09-03`；
- **`.epigraph`**：`.tldr` 之前的一条 `blockquote` 引语（红左边线、斜体），内容是该篇的「一句话导读」，`cite` 落款「— 本站导读」。

**已移除的元素（按用户反馈，勿再加回）**：

- 「馆藏信息」旁注卡片（arXiv/投稿/收录日）——与 `.pubmeta` 行完全重复。
- 整个 `<aside class="mnotes">` 旁注栏（分类 / 核心术语 / 阅读顺序）与 `.paper-main` 双栏包裹：
  - **分类**——已直接在正文 `.meta` 行中给出，并可由 index 横向对比表跳转；
  - **核心术语**——已用 `.gloss` 点线样式在正文中给出，悬停即跳 glossary；
  - **阅读顺序**——footer 的 ←/→ 键盘翻页链接 + index 横向对比表已经承载；
  - 因此 sidebar 没有额外价值，保持单栏正文、版心更舒展。

正文 h2 之前的头部信息区也可视情况补充收录时间戳。

### 4.10 v5 index 三视图 + 已读藏书章（index + 论文页共用脚本）

- **index**：`#fltbar` 之后插入 `.viewbar`（列表/画廊/星图三按钮 + `#vhint` 提示 + `#vhint-r` 已读数）+ `#gallery` + `#star` 容器。v5 脚本按需构建：画廊 = `covers/<arxiv>.png` 封面卡片网格；星图 = SVG 时间序点线（11 节点、类别色、悬停浮层）；列表/画廊/星图三视图与 `#fltbar` 筛选、`#q` 检索联动，且把 `?cat=&q=&view=` 同步进 URL（`history.replaceState`）。样式块 D 已含 `.viewbar/.vbtn/.gallery/#star` 等样式；
- **已读藏书章**：localStorage 键 `mpa-read`（`{arxiv: 时间戳}`）。论文页滚动超过 85% 或停留 30s 记为本篇已读（`body[data-read]`）；index 列表卡片滚动到「已读」的卡片右上角显示红底 `.readmark` 印章，`#vhint-r` 实时显示 `已读 n / 11`；
- **404.html**：红框 404 印章图元风格，独立轻量页，不参与导航链。

### 4.11 SEO / 许可 / 站身份文件

- `robots.txt`：`User-agent: *` + `Allow: /` + `Sitemap:` 指向 `sitemap.xml`；
- `sitemap.xml`：14 条 URL（index/glossary/about 带 lastmod/changefreq/priority，11 论文带 lastmod），论文 URL 用 percent-encoded 文件名；**新增论文必须追加**；
- `LICENSE`：原创内容 CC BY-NC 4.0 + 第三方论文版权声明双段式，非 MIT；
- `about.html`：含与 LICENSE 一致的许可措辞；收录标准、维护者、时间表；
- `apple-touch-icon.png`：180×180，红底白线 planner→agents 图元，与 favicon 呼应。

### 4.12 v6 目录移到左上角（替代 v1 的右下角浮钮）

v6 样式块（`</head>` 前最后一个 `<style>`，含 `v6 enhancements` 注释）把 `#toc-btn` 定位改为 `fixed left:14px top:14px`、`#toc-panel` 改为 `top:66px left:14px` 下拉；`@media (min-width:1040px)` 下用 `opacity/pointer-events !important` 压过 v1 的「滚动 >180px 才显示」逻辑使其**桌面常显**，移动端仍保持滚动后出现（避免遮挡正文）。`#totop` 仍在右下，不受影响。

### 4.13 v6 giscus 评论区（全部 14 个内容页，404 除外）

每页 `</body>` 前注入 `.giscwrap#giscus` 容器 + v6 懒加载脚本：`IntersectionObserver`（rootMargin 1400px）接近视口才把 `giscus.app/client.js` 注入 `.gismount`。**giscus 配置写在 `.giscwrap` 的 `data-*` 属性上，全站 14 页必须一致**，当前值（2026-09-03 实测）：

| 属性 | 值 |
|------|------|
| data-repo | `1parado/multi-agent-article` |
| data-repo-id | `R_kgDOUK42-A` |
| data-category | `General` |
| data-category-id | `DIC_kwDOUK42-M4DExUU` |
| data-mapping | `og:title`（14 页 og:title 全站唯一 → 本地 / 预览 / Pages 均落同一讨论串） |
| data-theme / data-lang | `light` / `zh-CN` |
| data-input-position | `top`（配合批注复制后粘贴） |

注意事项：
- 仓库须启用 **Discussions**（已启用）；giscus **App 需仓库管理员到 github.com/apps/giscus 安装一次**，未安装时评论区显示错误提示，安装后无需改代码；
- 若仓库迁移/换分类，须同步修改**全部 14 页** `.giscwrap` 的 `data-repo` / `data-repo-id` / `data-category-id`，勿只改一页；
- `.giscwrap` 打印时隐藏；`.gistitle` 里的引导文案提示「选中正文 → ✎ 批注」。

### 4.14 v6 WPS 式批注（选中文字 → 引用评论）

v6 脚本实现「选中即批注」：在正文（`.wrap` 内）用鼠标划选文字后，选区上方浮现 `.annbar` 工具条（✎ 写批注 / 复制引用）；「✎ 写批注」弹出 `.annmask` 弹层，展示被引原文（`.annq`，自动截断 300 字）、出处（`.pos`：所在章节 + 页面 og:title），用户在 textarea 写下批注后点「复制批注 · 去评论区」——脚本把「Markdown 引用块 + 出处 + 批注 + via 落款」复制到剪贴板，并滚动到 `.giscwrap` 闪烁提示，用户粘贴到 giscus 输入框发布（需 GitHub 登录，全员可见）。限制：选区须落在 `.wrap` 内（排除评论区/弹层/工具条自身）；<4 字不触发；键盘 ←/→ 在有非空选区或工具条显示时被拦截，避免误触翻页；Esc 关闭弹层。

## 5. 类别色签（分类色）

每个类别一个专属色，用于论文页 eyebrow、index `.idx` 行、index 筛选 chip（`--cat`）与 `data-cat`：

| data-cat / 类别 | 色值 | 论文 |
|------|------|------|
| FRAMEWORK（MULTI-AGENT FRAMEWORK） | `#A02C2C` | VMAO、AdaptOrch |
| HARNESS（AGENT HARNESS / 多模态 / TOOL USE） | `#9C6B1E` | NLAH、Meta-Harness、MUSE、HEART |
| ACTIVATION（ACTIVATION STEERING） | `#6B4FA0` | MoRe |
| SECURITY（SECURITY SoK） | `#2E7D74` | SoK |
| SELF-GENERATIVE | `#A34A7D` | MAS² |
| ROUTING（MODEL ROUTING） | `#3E6FA3` | OI-MAS |
| DECENTRALIZED | `#557B3F` | Symphony-Coord |

论文页 eyebrow 写法：`<div class="eyebrow" style="--cat:#9C6B1E"><span class="dot"></span>PAPER 03 · AGENT HARNESS</div>`；
index 条目写法：`<div class="idx" style="--cat:#9C6B1E"><span class="dot"></span>03 · AGENT HARNESS</div>`，且外层 `<div class="paper" data-cat="HARNESS">`。

## 6. glossary.html 术语 id 目录（当前已建 31 词条，按分组）

- 基础与训练：`llm` `mllm` `token` `sft` `grpo` `moe` `benchmark` `sota`
- 多智能体与编排：`agent` `mas` `framework` `orchestration` `dag` `planner` `router` `verifier` `harness`
- 路由、学习与效率：`model-routing` `confidence` `calibration` `codebook` `steering` `scaling-law` `pareto`
- 在线决策与理论保证：`bandit` `linucb` `regret`
- 安全、工具与接口：`prompt-injection` `asr` `schema` `semantic-search`

glossary / about 两页与普通页同构（含 §3 样式块 A/B、§4.3 C、样式块 D、v3+v4+v5 脚本、§4.1 字体、§4.2 favicon/OG/JSON-LD；v5 脚本在这两页为空操作只返回）；其 nav 遵循 §0 特殊页写法，不进 §2 顺序表。

## 7. 全站一致性

本规范描述的是**成品页面应有的样子**，不依赖任何批量脚本。新增或修改内容时，手工保证下列七处同步：

1. index 论文列表（`.paper` 卡片，含 `data-cat`）；
2. §2 顺序表（论文页「← / →」导航的依据）；
3. §5 类别色表（eyebrow 的 `--cat` 与 `.dot` 取值）；
4. README 论文表格；
5. `about.html` 的收录说明；
6. `sitemap.xml`；
7. `covers/` 下每篇论文的 1200×630 封面 PNG（页内 `og:image` 指向它）。

改动落地后用 §8 自检清单逐项 grep 验证；文件保持 LF 换行、UTF-8 无 BOM。

## 8. 完成前的自检清单

新增或修改页面后，逐项确认：

- [ ] 页内没有任何 `github.com/.../blob/main/` 或 `github.com/.../raw/main/` 形式的站内链接；
- [ ] `.nav` 与 §2 顺序表一致，「← / →」齐全，文件名与磁盘一一对应；特殊页 nav 右端不以 `→` 结尾；
- [ ] 页首 `.links` 含「目录」与 GitHub 图标；论文页 `.links` 后是 `.citebar`（**仅一个** `</div>` 闭合 links）且含 `cite-json`；
- [ ] 源码同时含 `page enhancements v3`、`page enhancements v4`、`page enhancements v5`、`#pbar {`、`#totop {`、`rel="preload" as="style"`（字体）、`favicon.svg`、`property="og:title"`；
- [ ] 论文页 eyebrow 带 `--cat` 与 `.dot`；正文含 3–5 个 `class="gloss"` 且锚点 id 存在于 glossary.html；index 每个 `.paper` 带 `data-cat`，`#fltbar` 含 8 个 chip（全部+7 类）；
- [ ] index footer 为 `.sitefoot` 两行结构；论文页 footer 含术语表/关于链接；
- [ ] 每页恰好一条 `og:image` 且紧跟 `og:image:width(1200)/height(630)` 三连对、指向本页 `covers/` PNG；每页恰好一条 `canonical`/`apple-touch-icon`/`theme-color`/`application/ld+json`（论文 `ScholarlyArticle`、index `WebSite`、glossary/about `WebPage`）；
- [ ] 论文页含 `page-paper`/`.pubmeta`/`.epigraph` 各一；**不得含 `.mnotes`/`.paper-main`（v5 后续已移除）**；
- [ ] index 含 `#viewbar`+`#gallery`+`#star`；`covers/` 每张 1200×630 与引用一致；新论文已进 `sitemap.xml`；
- [ ] 浏览器实测：目录筛选 chip 过滤、检索框过滤、空态提示；论文页点 BibTeX/APA 复制成功；Ctrl+P 打印预览无悬浮控件、条形图高度完整；术语点状下划线可跳到 glossary 对应词条；分享链接在微信/浏览器显示本页专属封面与标题；列表/画廊/星图切换、URL 带 `?view=` 刷新后保持视图、读完一篇后 index 出现红色藏书章；**论文页正文回到单栏，无右侧 sidebar**；
- [ ] 全站点一遍：index → 论文页 → 上一篇/下一篇 → 术语表 → 关于 → 404，全部可达。

## 9. 其他约定

- 样式沿用现有模板（`.wrap` 780px 单栏正文、IBM Plex Mono 强调、红 `#A02C2C` 主色 + 类别色签），系列一致；**论文页不再有旁注栏或双栏网格**；
- 文件命名：`<arXiv编号>_<短名>_中文版.html`；
- 各处的同步关系见 §7。
