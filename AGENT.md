# AGENT.md — 论文 HTML 页面编写规范

本目录（multi-agent-article）是论文中文编译版的静态站点：`index.html` 为目录页，每篇论文一个独立 HTML。**任何 Agent / 人在新增或修改页面时必须遵守本规范**，否则会出现「页面之间无法互相跳转」等回归问题（历史上发生过：① 导航被写成 GitHub blob 绝对链接导致全站跳转失效；② TOC/增强组件版本落后）。

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

允许使用绝对 URL 的场景：站外资源（arXiv、GitHub 仓库本身 `https://github.com/1parado/multi-agent-article`）。

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

注意：「上一篇」文案必须以 `←` 开头、「下一篇」以 `→` 结尾——键盘翻页脚本靠这两个字符识别方向。

另外，页首 `.links` 行中的「目录」链接同样必须指向 `index.html`（相对路径）。

**新增论文的必做步骤**：
1. 在 `index.html` 论文列表末尾追加条目；
2. 新页面 `.nav` 指向 `index.html`，并回写当前末篇页面的「下一篇」；
3. 更新本文件的顺序表与第 3.4 节类别色表；index 的横向对比表、阅读顺序、篇数、README 表格同步更新；
4. 页面内所有站内链接逐条自检（见第 4 节）。

## 3. 页面增强组件 v3 — 必须包含

每篇论文页与 index.html 必须包含以下组件。**实现方式：固定的代码块，原样复制，不做改写。**

### 3.1 `<head>` 内：字体链接（在 viewport meta 之后）

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

### 3.2 `</head>` 前的两个样式块

**样式块 A**：TOC 组件基础样式（`#toc-btn` / `#toc-panel` 系列，见现有页面）+ v2 增强样式（`#pbar`、`.dot`、`.eyebrow` 色签、`.reveal`、`.wm` 水印、`.bar` 过渡，见现有页面）。

**样式块 B（v3，紧跟 A 之后、`</head>` 之前）**：

```html
<style>
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
```

### 3.3 `</body>` 前：增强脚本 v3

完整脚本见现有任意页面（搜索 `page enhancements v3`）。功能清单（勿删减）：
- **阅读进度条** `#pbar`：顶部 3px 随滚动填充；
- **返回顶部** `#totop`：滚动 >600px 出现 ↑ 按钮；
- **标题 TOC + scroll-spy**：右下角 ☰ 面板列出 h1/h2，滚动自动高亮当前章节；
- **章节编号 + 锚点链接**：脚本为每个 h2 自动加 `.secno` 编号（01/02…）与 `.hlink` 悬浮 `#`（点击复制章节直链）——因此 TOC 构建必须发生在编号注入**之前**；
- **键盘翻页**：← / → 跳上一篇 / 下一篇（仅存在 `.nav` 的页面生效，靠箭头字符识别方向）；
- **滚动显现 + 图表生长**：IntersectionObserver 淡入上移、`.bar` 从 0 生长；全部尊重 `prefers-reduced-motion`。

检查方法：源码含 `page enhancements v3`、`#pbar {`、`#totop {`、`scroll-spy` 即合格。

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

### 3.5 GitHub 图标链接

每篇论文页 `.links` 行中 `arXiv</a>` 之后、index 页脚，必须有指向仓库的 GitHub 图标链接：

```html
<a class="ghlink" href="https://github.com/1parado/multi-agent-article" target="_blank" rel="noopener"><svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>GitHub</a>
```

### 3.6 论文页水印 / index Hero / 页脚

- 论文页：`<div class="wrap">` 后紧跟 `<div class="wm">arXiv <编号></div>`（右上角超大淡色水印，<700px 自动隐藏）；
- index：intro 段后紧跟 `.hero` SVG 插画（编排流水线示意，动画线尊重 reduced-motion）；阅读顺序段后 `<footer>` 含 GitHub 图标链接；
- 对比表（index）：保持 `table.cmp` 结构（首行 `<th>` 表头 + 数据行），v3 样式自动提供斑马纹 / hover / 首列强调。

## 4. 完成前的自检清单

新增或修改页面后，逐项确认：

- [ ] 页内没有任何 `github.com/.../blob/main/` 或 `github.com/.../raw/main/` 形式的站内链接；
- [ ] `.nav` 中「上一篇 / 下一篇」与第 2 节顺序表一致，「← / →」箭头字符齐全（键盘翻页依赖），文件名与磁盘实际文件一一对应；
- [ ] 页首 `.links` 的「目录」指向 `index.html`，且含 GitHub 图标链接；
- [ ] 源码包含 `page enhancements v3`、`#pbar {`、`#totop {`、`fonts.googleapis.com`；
- [ ] eyebrow 带 `--cat` 与 `.dot`，色值符合第 3.4 节色表；
- [ ] 论文页含 `.wm` 水印；
- [ ] 浏览器中实际点一遍：目录页 → 本页 → 上一篇 → 下一篇 → 目录，全部可达；
- [ ] 滚动页面：进度条填充、☰ 与 ↑ 按钮出现、目录高亮跟随、图表入场生长；h2 悬停出现 `#` 且点击复制链接；← / → 键翻页正常。

## 5. 其他约定

- 页面样式沿用现有模板（`.wrap` 最大宽 780px、IBM Plex Mono 强调、红 `#A02C2C` 主色 + 类别色签），保持系列一致；
- 文件命名：`<arXiv编号>_<短名>_中文版.html`；
- `index.html` 的论文列表、第 2 节顺序表、第 3.4 节类别色表、README 表格四者保持同步。
