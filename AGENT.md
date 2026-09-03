# AGENT.md — 论文 HTML 页面编写规范

本目录（multi-agent-article）是论文中文编译版的静态站点：`index.html` 为目录页，每篇论文一个独立 HTML。**任何 Agent / 人在新增或修改页面时必须遵守本规范**，否则会出现「页面之间无法互相跳转」的回归问题（该问题已发生过一次：所有内页导航曾被写成 GitHub blob 绝对链接，本地打开完全失效）。

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

PDF 链接规则：本目录存在对应 PDF 文件的用相对路径；不存在的（如 MoRe / SoK / MAS²）用 `https://arxiv.org/pdf/<id>.pdf`。

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
| 08 | 2509.24323_MAS2_中文版.html | SoK | —（只有目录） |

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
3. 更新本文件的顺序表；
4. 页面内所有站内链接逐条自检（见第 4 节）。

## 3. 标题锚点导航（TOC 悬浮按钮）— 必须包含

**规则：每篇论文页必须包含 TOC 悬浮组件：滚动超过约 180px 后右下角出现 ☰ 按钮，点击展开目录面板，列出页内所有 `h1` / `h2`，点击平滑滚动到对应标题。**

实现方式：固定的两段代码块，原样复制，不做改写。
- `<style>` 块粘贴在 `</head>` 之前；
- `<script>` 块粘贴在 `</body>` 之前。

```html
<style>
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
```

```html
<script>
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
```

要点：
- 组件从 `.wrap` 容器内收集 `h1` / `h2` 并自动生成锚点 id，**无需手写 id**；
- 脚本纯前端、零依赖，本地打开与托管环境均可用；
- 检查方法：页面源码中搜索 `toc-btn`，存在即合格。

## 4. 完成前的自检清单

新增或修改页面后，逐项确认：

- [ ] 页内没有任何 `github.com/.../blob/main/` 或 `github.com/.../raw/main/` 形式的站内链接；
- [ ] `.nav` 中「上一篇 / 下一篇」与第 2 节顺序表一致，文件名与磁盘上的实际文件一一对应（含中文字符完全一致）；
- [ ] 页首 `.links` 的「目录」指向 `index.html`；
- [ ] 源码包含 `toc-btn`（TOC 组件）；
- [ ] 浏览器中实际点一遍：目录页 → 本页 → 上一篇 → 下一篇 → 目录，全部可达；
- [ ] 滚动页面，右下角出现 ☰，展开后点击任一标题能跳转。

## 5. 其他约定

- 页面样式沿用现有模板（`--red:#A02C2C` 主题、`.wrap` 最大宽 780px），保持系列一致；
- 文件命名：`<arXiv编号>_<短名>_中文版.html`；
- `index.html` 的论文列表与第 2 节顺序表、README 表格三者保持同步。
