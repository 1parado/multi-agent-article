# -*- coding: utf-8 -*-
"""beautify_v4.py — 全站 PM 视角增强注入（阅读体验优先 + 保持美观）。

处理对象：index.html + 11 篇论文页（*.html 中以 *_中文版.html 结尾且非 glossary/about）。
注入内容：
  1) Google Fonts 异步加载（preload + noscript 降级，防渲染阻塞）
  2) favicon + OG/Twitter 分享 meta（每页标题/描述不同）
  3) v4 样式块：print 打印适配 / :focus-visible / .gloss 术语链 / .citebar 引用 /
     index 筛选检索 / footer 链接样式
  4) v4 脚本：打印前展开动效内容、引用复制、index 筛选+检索
  5) 论文页：引用按钮 + JSON 数据、正文术语 → glossary.html 链接、footer 增补链接
  6) index：筛选 chips + 检索框、data-cat、页脚重建、intro 文案修正
"""
import re, io, sys, json
from urllib.parse import quote
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BASE = "D:/multi-agent-article/"
PAGES = [
    "index.html",
    "2603.11445_VMAO_中文版.html", "2602.16873_AdaptOrch_中文版.html",
    "2603.25723_NLAH_中文版.html", "2603.28052_Meta-Harness_中文版.html",
    "2606.03005_MUSE_中文版.html", "2608.27338_MoRe_中文版.html",
    "2609.00595_SoK_中文版.html", "2509.24323_MAS2_中文版.html",
    "2601.04861_OI-MAS_中文版.html", "2602.00966_Symphony-Coord_中文版.html",
    "2609.01736_HEART_中文版.html",
]

SITE = "https://1parado.github.io/multi-agent-article"

# ---------- 每篇论文的元数据 ----------
PAPER = {
    "2603.11445": dict(key="vmao2026", name="VMAO",
        og="VMAO：验证式多智能体编排",
        desc="把「验证」提升为编排层的一等协调信号：DAG 分解并行执行，独立 LLM 检查员评估完整性，发现缺口自动重规划补漏。",
        title="Verified Multi-Agent Orchestration", auth="Xing Zhang and others",
        year=2026, venue="ICLR 2026 Workshop", cat="FRAMEWORK"),
    "2602.16873": dict(key="adaptorch2026", name="AdaptOrch",
        og="AdaptOrch：任务自适应拓扑编排",
        desc="证明模型趋同时「拓扑比选模型重要」（缩放定律 Ω(1/ε²)），线性时间算法按任务 DAG 自动选择四种编排拓扑。",
        title="Task-Adaptive Multi-Agent Orchestration", auth="Geunbin Yu",
        year=2026, venue="", cat="FRAMEWORK"),
    "2603.25723": dict(key="nlah2026", name="NLAH",
        og="NLAH：自然语言 Agent Harness",
        desc="把埋在控制器代码里的 harness 策略外化为可编辑的自然语言文档，由共享运行时解释执行；策略层 60K→2.9K token。",
        title="Natural-Language Agent Harnesses",
        auth="Linyue Pan, Hai-Tao Zheng and others", year=2026, venue="", cat="HARNESS"),
    "2603.28052": dict(key="metaharness2026", name="Meta-Harness",
        og="Meta-Harness：自动搜索最优 harness",
        desc="用 coding agent 经文件系统翻阅全部历史候选的源码、分数与执行轨迹，自动发现超越人类手工设计的 harness。",
        title="End-to-End Optimization of Model Harnesses",
        auth="Yoonho Lee, Chelsea Finn and others", year=2026, venue="", cat="HARNESS"),
    "2606.03005": dict(key="muse2026", name="MUSE",
        og="MUSE：面向多模态大模型的统一 Harness",
        desc="首个面向冻结多模态大模型的统一 harness：感知工具 + 确定性验证器 + 修复循环；GPT-4o 找字任务 3%→21%。",
        title="MUSE: A Unified Agentic Harness for MLLMs",
        auth="Jianglin Lu, Yun Fu and others", year=2026, venue="", cat="HARNESS"),
    "2608.27338": dict(key="more2026", name="MoRe",
        og="MoRe：把多角色协同压进单次推理",
        desc="把多种角色学成可组合的激活引导向量，查询感知路由器在单次前向中动态混合；性能逼近 MAS，token 成本约降 20×。",
        title="MoRe: Mixture of Roles", auth="UIUC + Amazon（作者详见 arXiv）",
        year=2026, venue="", cat="ACTIVATION"),
    "2609.00595": dict(key="sok2026", name="SoK",
        og="SoK：安全的智能体也可能一起失败",
        desc="对 197 篇工作做执行中心分析，提出 A-I-R 攻击框架与五部分防御契约；审计 44 项评测。",
        title="SoK: When Safe Agents Fail Together",
        auth="SoK 作者团队（详见 arXiv）", year=2026, venue="", cat="SECURITY"),
    "2509.24323": dict(key="mas2", name="MAS²",
        og="MAS²：自生成、自配置、自纠偏的多智能体系统",
        desc="用 generator–implementer–rectifier 三元 meta-agent 递归定制目标 MAS 并在运行中纠偏；相对 SOTA 最高约 +19.6%。",
        title="Self-Generative Multi-Agent Systems",
        auth="NTU / ZJU / NUS 等（作者详见 arXiv）", year=2025, venue="ICLR 2026 Poster",
        cat="SELF-GENERATIVE"),
    "2601.04861": dict(key="oimas2026", name="OI-MAS",
        og="OI-MAS：跨多尺度模型的置信感知路由",
        desc="把「选 agent 角色」和「选模型规模」统一为两级动态路由，用校准后的模型置信度作为成本惩罚的自适应权重。",
        title="OI-MAS: Confidence-Aware Routing across Multi-Scale Models",
        auth="Jingbo Wang and others", year=2026, venue="", cat="ROUTING"),
    "2602.00966": dict(key="symphony2026", name="Symphony-Coord",
        og="Symphony-Coord：去中心化的涌现式协调",
        desc="把 agent 选择建模为在线上下文多臂老虎机：Beacon 筛选 Top-L 候选，LinUCB 按任务与 agent 状态路由，次线性 regret 保证。",
        title="Symphony-Coord: Adaptive Routing for Multi-Agent LLM Systems",
        auth="Zhaoyang Guan and others", year=2026, venue="", cat="DECENTRALIZED"),
    "2609.01736": dict(key="heart2026", name="HEART",
        og="HEART：自然语言工具原语 + 2.5 万函数仓库",
        desc="Tool Primitive 以自然语言为工具接口，ToolFace 语义检索 25,519 个函数；8B 骨干超三个商用模型 6%、成本最高降 85%。",
        title="HEART: Harness Engineering via Agent-Native Reusable Tool Primitives",
        auth="Haibo Jin and others", year=2026, venue="", cat="HARNESS"),
}

# ---------- 术语链接（页面 id 列表；aliases 按偏好顺序，取第一个在正文出现的） ----------
TERM_LINKS = {
    "2603.11445": ["dag", "verifier", "mas"],
    "2602.16873": ["scaling-law", "dag", "benchmark"],
    "2603.25723": ["harness", "verifier", "benchmark"],
    "2603.28052": ["harness", "benchmark", "sota"],
    "2606.03005": ["harness", "verifier", "mllm"],
    "2608.27338": ["codebook", "steering", "router", "grpo"],
    "2609.00595": ["mas", "benchmark", "llm"],
    "2509.24323": ["mas", "sota", "pareto"],
    "2601.04861": ["model-routing", "confidence", "calibration"],
    "2602.00966": ["bandit", "linucb", "regret"],
    "2609.01736": ["schema", "semantic-search", "prompt-injection", "asr"],
}
ALIASES = {
    "dag": ["DAG"],
    "verifier": ["验证器", "Verifier", "检查员"],
    "mas": ["多智能体系统（MAS）", "多智能体系统", "MAS"],
    "harness": ["harness"],
    "benchmark": ["benchmark", "基准"],
    "sota": ["SOTA", "state-of-the-art"],
    "mllm": ["MLLM", "多模态大语言模型"],
    "llm": ["LLM"],
    "codebook": ["codebook"],
    "steering": ["激活引导", "steering vector", "Steering"],
    "router": ["路由器", "Router"],
    "grpo": ["GRPO"],
    "scaling-law": ["缩放定律", "scaling law"],
    "pareto": ["Pareto", "帕累托"],
    "model-routing": ["模型路由", "跨模型路由", "置信感知路由"],
    "confidence": ["置信度", "confidence"],
    "calibration": ["校准", "calibration"],
    "bandit": ["多臂老虎机", "bandit", "contextual bandit"],
    "linucb": ["LinUCB"],
    "regret": ["regret", "遗憾界", "遗憾"],
    "schema": ["schema"],
    "semantic-search": ["语义检索", "semantic search"],
    "prompt-injection": ["prompt injection", "提示注入"],
    "asr": ["ASR"],
}

CAT_COLOR = {
    "FRAMEWORK": "#A02C2C", "HARNESS": "#9C6B1E", "ACTIVATION": "#6B4FA0",
    "SECURITY": "#2E7D74", "SELF-GENERATIVE": "#A34A7D",
    "ROUTING": "#3E6FA3", "DECENTRALIZED": "#557B3F",
}
CAT_CN = {
    "FRAMEWORK": "编排框架", "HARNESS": "Harness 执行系统", "ACTIVATION": "激活协同",
    "SECURITY": "安全", "SELF-GENERATIVE": "自生成", "ROUTING": "路由",
    "DECENTRALIZED": "去中心化",
}

FONT_OLD = '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">'
FONT_NEW = ('<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap" onload="this.onload=null;this.rel=\'stylesheet\'">\n'
            '<noscript><link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet"></noscript>')

V4_STYLE = """
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
  .q::-webkit-search-cancel-button { -webkit-appearance:none; }
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
"""

V4_SCRIPT = """
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
"""

CITEBAR_HTML = """
</div>

<div class="citebar"><span class="citecap">CITE</span><button type="button" class="citebtn" data-cite="bib">BibTeX</button><button type="button" class="citebtn" data-cite="apa">APA</button></div>
<script type="application/json" id="cite-json">{json}</script>
"""

INDEX_FILTER = """<div class="fltbar" id="fltbar">
  <div class="flt" role="group" aria-label="按类别筛选论文">
    <button type="button" class="chip on" data-cat="*">全部</button>
    <button type="button" class="chip" data-cat="FRAMEWORK" style="--cat:#A02C2C" title="编排框架：VMAO / AdaptOrch"><span class="dot"></span>FRAMEWORK</button>
    <button type="button" class="chip" data-cat="HARNESS" style="--cat:#9C6B1E" title="Harness 执行系统：NLAH / Meta-Harness / MUSE / HEART"><span class="dot"></span>HARNESS</button>
    <button type="button" class="chip" data-cat="ACTIVATION" style="--cat:#6B4FA0" title="激活协同：MoRe"><span class="dot"></span>ACTIVATION</button>
    <button type="button" class="chip" data-cat="SECURITY" style="--cat:#2E7D74" title="安全：SoK"><span class="dot"></span>SECURITY</button>
    <button type="button" class="chip" data-cat="SELF-GENERATIVE" style="--cat:#A34A7D" title="自生成：MAS²"><span class="dot"></span>SELF-GENERATIVE</button>
    <button type="button" class="chip" data-cat="ROUTING" style="--cat:#3E6FA3" title="模型路由：OI-MAS"><span class="dot"></span>ROUTING</button>
    <button type="button" class="chip" data-cat="DECENTRALIZED" style="--cat:#557B3F" title="去中心化协调：Symphony-Coord"><span class="dot"></span>DECENTRALIZED</button>
  </div>
  <input class="q" id="q" type="search" placeholder="检索标题 / 关键词 / 机构 / arXiv 编号" aria-label="检索论文">
  <div class="fltstat" id="fltstat" aria-live="polite"></div>
  <p class="fltnone" id="fltnone" hidden>没有匹配的论文——换个关键词，或点「全部」清空筛选。</p>
</div>
"""

INDEX_FOOTER = """<footer class="sitefoot">
  <div class="fl1"><a class="ghlink" href="https://github.com/1parado/multi-agent-article" target="_blank" rel="noopener"><svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>GitHub · 1parado/multi-agent-article</a></div>
  <div class="fl2"><a href="index.html">首页</a><a href="glossary.html">术语表</a><a href="about.html">关于</a><a href="https://github.com/1parado/multi-agent-article/issues" target="_blank" rel="noopener">反馈</a><a href="about.html">© 2026 Paradox</a></div>
</footer>"""

INDEX_INTRO_OLD = '<p class="intro">11 篇经核验的 arXiv 论文（多智能体编排 / harness / 自生成 / 安全），PDF 与中文版均在本目录。</p>'
INDEX_INTRO_NEW = '<p class="intro">11 篇经核验的 arXiv 论文（多智能体编排 / harness / 自生成 / 安全）：每篇一页中文编译 + 原文对照；前五篇附本地 PDF，其余直链 arXiv 原文。正文带点状下划线的词可在<a class="gloss" href="glossary.html" style="color:inherit;">术语表</a>中查看。</p>'


def make_meta(name):
    """构造 favicon + og 头插入块。name: index.html 或论文文件名"""
    m = re.match(r"(\d{4}\.\d+)", name)
    if m and m.group(1) in PAPER:
        p = PAPER[m.group(1)]
        otitle = p["og"]
        odesc = p["desc"]
        page = SITE + "/" + quote(name)
        return ('<link rel="icon" type="image/svg+xml" href="favicon.svg">\n'
                '<meta property="og:type" content="article">\n'
                '<meta property="og:site_name" content="Multi-Agent Paper Digest 2026">\n'
                '<meta property="og:title" content="' + otitle + '">\n'
                '<meta property="og:description" content="' + odesc + '">\n'
                '<meta property="og:url" content="' + page + '">\n'
                '<meta property="og:image" content="' + SITE + '/hero.svg">\n'
                '<meta name="twitter:card" content="summary_large_image">\n'
                '<meta name="twitter:title" content="' + otitle + '">\n'
                '<meta name="twitter:description" content="' + odesc + '">\n'
                '<meta name="description" content="' + odesc + '">')
    return ('<link rel="icon" type="image/svg+xml" href="favicon.svg">\n'
            '<meta property="og:type" content="website">\n'
            '<meta property="og:site_name" content="Multi-Agent Paper Digest 2026">\n'
            '<meta property="og:title" content="Multi-Agent Framework / Harness · 2026 论文中文导读">\n'
            '<meta property="og:description" content="11 篇 multi-agent 代表性论文中文编译：framework / harness / 自生成 / 安全，含对比表、术语表与阅读顺序。">\n'
            '<meta property="og:url" content="' + SITE + '/">\n'
            '<meta property="og:image" content="' + SITE + '/hero.svg">\n'
            '<meta name="twitter:card" content="summary_large_image">\n'
            '<meta name="twitter:title" content="Multi-Agent Framework / Harness · 2026 论文中文导读">\n'
            '<meta name="twitter:description" content="11 篇 multi-agent 代表性论文中文编译：framework / harness / 自生成 / 安全。">\n'
            '<meta name="description" content="11 篇 multi-agent 代表性论文的中文导读与对比：multi-agent framework / agent harness / 自生成 / 安全。">')


def bibtex(p, arx):
    venue = ("  note          = {" + p["venue"] + "，中文编译见 multi-agent-article},\n") if p["venue"] else ""
    return (
        "@misc{" + p["key"] + ",\n"
        "  title         = {" + p["title"] + "},\n"
        "  author        = {" + p["auth"] + "},\n"
        "  year          = {" + str(p["year"]) + "},\n"
        "  eprint        = {" + arx + "},\n"
        "  archiveprefix = {arXiv},\n"
        "  url           = {https://arxiv.org/abs/" + arx + "},\n"
        + venue +
        "}")


def apa(p, arx):
    label = p["auth"].split(",")[0].strip().replace(" and others", "").replace("（作者详见 arXiv）", "").replace("等（作者详见 arXiv）", "")
    if label.endswith("others") or p["name"] in ("SoK", "MAS²", "MoRe"):
        label = p["name"]
    return label + " (" + str(p["year"]) + "). " + p["title"] + ". arXiv:" + arx + ". https://arxiv.org/abs/" + arx


def nl(eol):
    return "\r\n" if eol == "crlf" else "\n"


def main():
    for name in PAGES:
        path = BASE + name
        txt = open(path, encoding="utf-8").read()
        n = "\n"
        orig = txt
        assert "page enhancements v4" not in txt, name + " 已含 v4，跳过"

        # 1) 字体异步
        assert FONT_OLD in txt, name + " 字体链接未找到"
        txt = txt.replace(FONT_OLD, FONT_NEW, 1)

        # 2) favicon + OG（插在 noscript 之后）
        meta = make_meta(name)
        assert "<noscript><link href=\"https://fonts.googleapis.com" in txt
        txt = txt.replace("</noscript>", "</noscript>\n" + meta, 1)

        # 3) v4 样式块（</head> 前）
        txt = txt.replace("</head>", "<style>" + V4_STYLE + "</style>\n</head>", 1)

        is_paper = name != "index.html"
        arx = re.match(r"(\d{4}\.\d+)", name).group(1) if is_paper else None

        if is_paper:
            p = PAPER[arx]
            # 4) 引用条 + JSON
            data = {"bib": bibtex(p, arx), "apa": apa(p, arx)}
            cite_html = CITEBAR_HTML.format(json=json.dumps(data, ensure_ascii=False))
            marker = "</div>\n\n<div class=\"tldr\">"
            assert txt.count(marker) == 1, name + " tldr marker 异常: " + str(txt.count(marker))
            txt = txt.replace(marker, "</div>\n\n" + cite_html.strip() + "\n\n<div class=\"tldr\">", 1)

            # 5) 术语 → glossary 链接（仅 tldr..nav 区间，屏蔽 h2/h3 与标签）
            for tid in TERM_LINKS.get(arx, []):
                seg_s = txt.find('<div class="tldr">')
                seg_e = txt.find('<div class="nav">')
                if seg_s == -1 or seg_e == -1 or seg_e < seg_s:
                    print("  !!", name, "缺 tldr/nav 段"); break
                seg = txt[seg_s:seg_e]
                masked = re.sub(r"<h[23][^>]*>.*?</h[23]>", lambda m: " " * len(m.group(0)), seg, flags=re.S)
                masked = re.sub(r"<[^>]+>", lambda m: " " * len(m.group(0)), masked)
                alias = None
                for a in ALIASES[tid]:
                    if masked.find(a) != -1:
                        alias = a; break
                if not alias:
                    print("  --", name, "术语缺失:", tid); continue
                idx = masked.find(alias)
                g = seg_s + idx
                link = '<a class="gloss" href="glossary.html#' + tid + '">' + alias + "</a>"
                txt = txt[:g] + link + txt[g + len(alias):]

            # 6) footer 增补术语表/关于
            def foot_repl(m):
                return m.group(0)[:-9] + n + '  <a href="glossary.html">术语表</a> · <a href="about.html">关于</a>' + m.group(0)[-9:]
            txt = re.sub(r"<footer>.*?</footer>", foot_repl, txt, count=1, flags=re.S)
        else:
            # ---- index ----
            # intro 文案修正
            assert INDEX_INTRO_OLD in txt, "index intro 文案未找到"
            txt = txt.replace(INDEX_INTRO_OLD, INDEX_INTRO_NEW, 1)
            # 筛选条插到论文列表标题下
            m = re.search(r"(<h2>论文列表</h2>\n<div class=\"hline\"></div>\n)", txt)
            assert m, "index 论文列表标题未找到"
            txt = txt[:m.end()] + INDEX_FILTER + txt[m.end():]
            # 每张卡片加 data-cat
            def cat_repl(mm):
                head = mm.group(0)
                if "data-cat" in head:
                    return head
                tail = txt[mm.end():mm.end() + 600]
                hm = re.search(r'href="(\d{4}\.\d+)_', tail)
                if not hm:
                    return head
                ar = hm.group(1)
                if ar not in PAPER:
                    return head
                return head[:-1] + ' data-cat="' + PAPER[ar]["cat"] + '">'
            txt = re.sub(r'<div class="paper">', cat_repl, txt)
            # 页脚重建
            txt = re.sub(r"<footer>.*?</footer>", INDEX_FOOTER, txt, count=1, flags=re.S)

        # 7) v4 脚本（</body> 前）
        bi = txt.rfind("</body>")
        assert bi != -1
        txt = txt[:bi] + V4_SCRIPT + "\n" + txt[bi:]

        open(path, "w", encoding="utf-8", newline="\n").write(txt)
        # 统计报告
        stat = {
            "font-async": txt.count("onload=\"this.onload=null;this.rel='stylesheet'\""),
            "favicon": txt.count('href="favicon.svg"'),
            "og": txt.count('property="og:title"'),
            "v4-style": txt.count("/* ---- v4 enhancements"),
            "v4-script": txt.count("page enhancements v4"),
            "gloss": txt.count('class="gloss"'),
            "cite": txt.count('id="cite-json"'),
            "fltbar": txt.count('id="fltbar"'),
            "sitefoot": txt.count('class="sitefoot"'),
        }
        print(name, stat)


if __name__ == "__main__":
    main()
