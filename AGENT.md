# AGENT.md — 论文 HTML 页面编写规范 v4

本目录（multi-agent-article）是论文中文编译版的静态站点：`index.html` 为目录页，每篇论文一个独立 HTML，另有 `glossary.html`（术语表）、`about.html`（关于）、`favicon.svg`。**任何 Agent / 人在新增或修改页面时必须遵守本规范**，否则会出现「页面之间无法互相跳转」「组件版本落后」等回归问题（历史上发生过：① 导航被写成 GitHub blob 绝对链接导致全站跳转失效；② 增强组件版本不一致；③ 引用条注入多出游离 `</div>`；④ index 页脚检测逻辑误判注入失败）。

---

## 0. 站点文件清单与页面类型

| 页面 | 类型 | 说明 |
|------|------|------|
| index.html | 目录页 | 论文列表（每项带 `data-cat`）+ 横向对比表 + 趋势 + 阅读顺序 + `#fltbar` 筛选检索 |
| `<arXiv号>_<短名>_中文版.html`（11 篇） | 论文页 | 属于导航链（见 §2），带 `.links`、`.citebar`、正文 `.gloss` 术语链 |
| glossary.html | 术语表 | 不属于导航链；词条 `id` 供各页 `.gloss` 链接（见 §4.6） |
| about.html | 关于 | 不属于导航链；维护信息、收录标准、更新记录 |
| favicon.svg | 站身份 | 所有页面 `<head>` 必须引用 |
| hero.svg / *.pdf | 资源 | hero 作为 og:image；PDF 见 §1 链接规则 |

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
4. 页面内所有站内链接逐条自检（见 §8）。

## 3. 页面增强组件 v1–v3 — 论文页与 index 必须包含

**实现方式：固定的代码块，原样复制，不做改写。** 组件历史：v1 TOC / v2（进度条、色签、reveal、水印、Hero）/ v3（返回顶部、章节编号、锚点复制、键盘翻页、对比表升级、移动端）。全部页面已内置，逐项核验标准：

- `<head>` 含 **v4 字体异步块**（见 §4.1）；
- `</head>` 前依次为：样式块 A（TOC widget + v2 增强）、样式块 B（v3 增强）、样式块 C（v4 增强，见 §4.3）；
- `</body>` 前依次为：增强脚本 v3（搜索 `page enhancements v3`）与增强脚本 v4（搜索 `page enhancements v4`）；
- 类别色签（§5）、GitHub 图标（`.ghlink`）、论文页水印 `.wm`、对比表 `table.cmp`、Hero SVG 等 v2/v3 细节以现有页面为准。

检查方法：源码含 `page enhancements v3` 与 `page enhancements v4`、`#pbar {`、`#totop {`、`#fltbar`（index）/`#cite-json`（论文页）、`favicon.svg`、`property="og:title"` 即合格。

## 4. 页面增强组件 v4 — 全部页面必须包含

### 4.1 字体异步加载（替换旧的同步 `<link>`）

旧写法 `<link href="...css2?family=IBM+Plex+Mono..." rel="stylesheet">` **已废弃**，一律使用（防 Google Fonts 阻塞渲染，境内网络友好）：

```html
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet"></noscript>
```

### 4.2 favicon 与 OG / Twitter 分享 meta

每页 `<head>` 在字体块之后必须包含 favicon 与 OG meta。论文页按各自元数据填写（站点根 `SITE = https://1parado.github.io/multi-agent-article`，og:url 用 **percent-encoded** 文件名；og:image 统一指向 `SITE/hero.svg`）：

```html
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Multi-Agent Paper Digest 2026">
<meta property="og:title" content="<中文标题>">
<meta property="og:description" content="<一句话介绍，<150 字>">
<meta property="og:url" content="https://1parado.github.io/multi-agent-article/<percent-encoded文件名>">
<meta property="og:image" content="https://1parado.github.io/multi-agent-article/hero.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<同 og:title>">
<meta name="twitter:description" content="<同 og:description>">
<meta name="description" content="<同 og:description>">
```

index 用 `og:type=website`、`og:url=SITE/`。新增论文的 og:title / og:description 素材直接取自 index 列表的 h3 与 p 描述。

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

`cite-json` 生成规则：`bib` 为 BibTeX（字段 title/author/year/eprint/archiveprefix/url，`@misc`；作者缺失时用机构并注明「作者详见 arXiv」）；`apa` 为 `作者标注（年份）. 英文标题. arXiv:<id>. https://arxiv.org/abs/<id>`。新增论文须在 `.workbuddy/beautify_v4.py` 的 `PAPER` 表中登记 key/title/auth/year/venue/og/desc/cat。

### 4.6 术语链（正文 → glossary.html）

- 论文页正文（`.tldr` 起至 `.nav` 止，且**不进入 h2/h3 标题内部**）将核心概念首次出现处包成 `<a class="gloss" href="glossary.html#<id>">词</a>`，点状下划线视觉；
- 每个论文页保留 3–5 个术语链即可（当前映射见 `.workbuddy/beautify_v4.py` 的 `TERM_LINKS`/`ALIASES`，别名按出现偏好排列，注入脚本会自动屏蔽 h2/h3 与标签内部）；
- **新增术语**必须三步同步：glossary.html 增加 `<div class="term" id="<id>">` 词条 → 本文件 §6 的术语 id 目录 → 需要链接它的页面正文注入 `.gloss`；
- 术语 alias 不得与其他已注入锚点词重叠（避免嵌套链接）。

### 4.7 index 筛选与检索（仅 index.html）

`<h2>论文列表</h2>` 之后紧跟 `#fltbar`：7 个类别 chip + 检索框 `#q` + 状态行 `#fltstat` + 空态 `#fltnone`（完整 markup 见 index.html，新增论文时只需给新卡片补 `data-cat`）。chip 类别与颜色必须与 §5 色表一致。

### 4.8 页脚

- index：`<footer class="sitefoot">` 两行（fl1 GitHub 链接、fl2 首页/术语表/关于/反馈/版权）——见 index.html 现状，勿回退为单行；
- 论文页：既有单行 footer 内容后追加 ` · <a href="glossary.html">术语表</a> · <a href="about.html">关于</a>`；
- glossary / about：自带 footer（返回目录 + 链接）。

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

## 6. glossary.html 术语 id 目录（当前已建 30 词条，按分组）

- 基础与训练：`llm` `mllm` `token` `sft` `grpo` `moe` `benchmark` `sota`
- 多智能体与编排：`agent` `mas` `framework` `orchestration` `dag` `planner` `router` `verifier` `harness`
- 路由、学习与效率：`model-routing` `confidence` `calibration` `codebook` `steering` `scaling-law` `pareto`
- 在线决策与理论保证：`bandit` `linucb` `regret`
- 安全、工具与接口：`prompt-injection` `asr` `schema` `semantic-search`

glossary / about 两页与普通页同构（含 §3 样式块 A/B、§4.3 C、v3+v4 脚本、§4.1 字体、§4.2 favicon/OG）；其 nav 遵循 §0 特殊页写法，不进 §2 顺序表。

## 7. 批量脚本（.workbuddy/）

| 脚本 | 用途 |
|------|------|
| beautify_v4.py | v4 全站注入（字体异步/OG/样式/脚本/引用/术语链/筛选/页脚/文案修正），内含 PAPER 元数据表与 TERM_LINKS 术语映射，**新增论文时在此登记并重跑其「全站自检」逻辑** |
| v4_scan.py / v4_fix_straydiv.py | 术语扫描 / 游离 `</div>` 修复（历史问题保留，勿重犯） |
| beautify_v2.py / v3.py / patch / remove_dropcap / fix_nav.py | 历史批次，仅存档 |

批量修改一律：先断言 v4 标记不存在再注入（防重复）；改完全站用 §8 清单 grep 自检；保持 LF 换行、UTF-8 无 BOM。

## 8. 完成前的自检清单

新增或修改页面后，逐项确认：

- [ ] 页内没有任何 `github.com/.../blob/main/` 或 `github.com/.../raw/main/` 形式的站内链接；
- [ ] `.nav` 与 §2 顺序表一致，「← / →」齐全，文件名与磁盘一一对应；特殊页 nav 右端不以 `→` 结尾；
- [ ] 页首 `.links` 含「目录」与 GitHub 图标；论文页 `.links` 后是 `.citebar`（**仅一个** `</div>` 闭合 links）且含 `cite-json`；
- [ ] 源码同时含 `page enhancements v3`、`page enhancements v4`、`#pbar {`、`#totop {`、`rel="preload" as="style"`（字体）、`favicon.svg`、`property="og:title"`；
- [ ] 论文页 eyebrow 带 `--cat` 与 `.dot`；正文含 3–5 个 `class="gloss"` 且锚点 id 存在于 glossary.html；index 每个 `.paper` 带 `data-cat`，`#fltbar` 含 8 个 chip（全部+7 类）；
- [ ] index footer 为 `.sitefoot` 两行结构；论文页 footer 含术语表/关于链接；
- [ ] 浏览器实测：目录筛选 chip 过滤、检索框过滤、空态提示；论文页点 BibTeX/APA 复制成功；Ctrl+P 打印预览无悬浮控件、条形图高度完整；术语点状下划线可跳到 glossary 对应词条；分享链接在微信/浏览器有标题与描述；
- [ ] 全站点一遍：index → 论文页 → 上一篇/下一篇 → 术语表 → 关于，全部可达。

## 9. 其他约定

- 样式沿用现有模板（`.wrap` 780px、IBM Plex Mono 强调、红 `#A02C2C` 主色 + 类别色签），系列一致；
- 文件命名：`<arXiv编号>_<短名>_中文版.html`；
- index 论文列表、§2 顺序表、§5 色表、README 表格、about.html 收录说明五者同步。
