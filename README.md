<div align="center">
  <img src="hero.svg" width="880" alt="Multi-Agent Framework / Harness · 2026 论文导读"/>

  # Multi-Agent Framework / Harness · 2026 论文导读

  **11 篇 multi-agent 代表性论文（arXiv 2025-09 ~ 2026-09）· 中文编译 + 原文链接**

  [📖 在线阅读](https://github.com/1parado/multi-agent-article/blob/main/index.html)
</div>

---

## 背景

当各家大模型在基准上的分数挤进 2–5% 的窄带，模型之外的结构设计成为新的性能主战场。

- **multi-agent framework** —— 协调多个 LLM agent 协作的结构：怎么拆任务、怎么并行、怎么合并、何时停止；
- **agent harness** —— 包裹在模型外围的执行系统：决定模型每一步看到什么、用什么工具、状态存哪里、何时验证、何时停止；
- **自生成 / 安全** —— 系统能否为自己设计系统、以及多主体交互下的系统级安全。

本仓库收录 arXiv 2025-09 至 2026-09 间具代表性的 **11 篇论文**，每篇提供中文编译页（解决什么问题 → 创新点 → 关键结果 → 局限）与原文 PDF / arXiv 链接（VMAO、AdaptOrch、NLAH、Meta-Harness、MUSE 五篇附本地 PDF，其余指向 arXiv 原文）。

## 论文一览

| # | 论文 | 机构 / 发表 | 一句话 | 资料 |
|---|------|------------|--------|------|
| 01 | **VMAO** 验证式多智能体编排 | AWS + HSBC · ICLR 2026 WS | 把「验证」提升为编排层的一等协调信号：DAG 并行执行 → 独立检查员评估完整性 → 自动重规划补漏 | [中文版](https://github.com/1parado/multi-agent-article/blob/main/2603.11445_VMAO_中文版.html) · [PDF](https://github.com/1parado/multi-agent-article/raw/main/2603.11445_VMAO_Verified-Multi-Agent-Orchestration.pdf) · [arXiv](https://arxiv.org/abs/2603.11445) |
| 02 | **AdaptOrch** 任务自适应拓扑编排 | 韩国国民大学 | 证明模型趋同时「拓扑比选模型重要」（Var τ/Var M ≥ Ω(1/ε²)），线性时间算法按任务 DAG 自动选编排拓扑 | [中文版](https://github.com/1parado/multi-agent-article/blob/main/2602.16873_AdaptOrch_中文版.html) · [PDF](https://github.com/1parado/multi-agent-article/raw/main/2602.16873_AdaptOrch_Task-Adaptive-Multi-Agent-Orchestration.pdf) · [arXiv](https://arxiv.org/abs/2602.16873) |
| 03 | **NLAH** 自然语言 Agent Harness | 清华深研院 + 哈工大（深圳） | 把埋在控制器代码里的 harness 策略外化为可执行的自然语言文档，由共享运行时解释执行；策略层 60K → 2.9K token | [中文版](https://github.com/1parado/multi-agent-article/blob/main/2603.25723_NLAH_中文版.html) · [PDF](https://github.com/1parado/multi-agent-article/raw/main/2603.25723_Natural-Language-Agent-Harnesses.pdf) · [arXiv](https://arxiv.org/abs/2603.25723) |
| 04 | **Meta-Harness** harness 自动优化 | 斯坦福 + MIT + KRAFTON | 用 coding agent 经文件系统翻阅全部历史源码 / 分数 / 执行轨迹，自动搜索超越人类手工设计的 harness | [中文版](https://github.com/1parado/multi-agent-article/blob/main/2603.28052_Meta-Harness_中文版.html) · [PDF](https://github.com/1parado/multi-agent-article/raw/main/2603.28052_Meta-Harness_End-to-End-Optimization-of-Model-Harnesses.pdf) · [arXiv](https://arxiv.org/abs/2603.28052) |
| 05 | **MUSE** 多模态统一 Harness | 东北大学 + 北京大学 | 首个面向冻结 MLLM 的统一 harness：感知工具 + 确定性验证器 + 修复循环；GPT-4o 找字任务 3% → 21% | [中文版](https://github.com/1parado/multi-agent-article/blob/main/2606.03005_MUSE_中文版.html) · [PDF](https://github.com/1parado/multi-agent-article/raw/main/2606.03005_MUSE_Unified-Agentic-Harness-for-MLLMs.pdf) · [arXiv](https://arxiv.org/abs/2606.03005) |
| 06 | **MoRe** 角色混合（激活空间协同） | UIUC + Amazon · 2026-08 | 把多种角色学成 codebook，查询感知路由器在单次前向中混合；性能逼近 MAS，token 约降 20× | [中文版](https://github.com/1parado/multi-agent-article/blob/main/2608.27338_MoRe_中文版.html) · [PDF](https://arxiv.org/pdf/2608.27338.pdf) · [arXiv](https://arxiv.org/abs/2608.27338) |
| 07 | **SoK** 多智能体安全系统化 | 2026-09 | 197 篇执行中心分析；A-I-R 攻击框架 + 五部分防御契约；审计 44 项评测 | [中文版](https://github.com/1parado/multi-agent-article/blob/main/2609.00595_SoK_中文版.html) · [PDF](https://arxiv.org/pdf/2609.00595.pdf) · [arXiv](https://arxiv.org/abs/2609.00595) |
| 08 | **MAS²** 自生成多智能体系统 | NTU 等 · ICLR 2026 | Generator–Implementer–Rectifier 递归定制目标 MAS 并运行时纠偏；最高约 +19.6% | [中文版](https://github.com/1parado/multi-agent-article/blob/main/2509.24323_MAS2_中文版.html) · [PDF](https://arxiv.org/pdf/2509.24323.pdf) · [arXiv](https://arxiv.org/abs/2509.24323) |
| 09 | **OI-MAS** 跨多尺度模型置信感知路由 | 哈尔滨工业大学 · 2026-01 | 角色与模型规模两级状态依赖动态路由；置信度作为成本惩罚权重；准确率最高 +12.88%，成本最高 −79.78% | [中文版](https://github.com/1parado/multi-agent-article/blob/main/2601.04861_OI-MAS_中文版.html) · [PDF](https://arxiv.org/pdf/2601.04861.pdf) · [arXiv](https://arxiv.org/abs/2601.04861) |
| 10 | **Symphony-Coord** 去中心化涌现协调 | NUS + NYU + Gradient 等 · 2026-02 | agent 选择 = 在线上下文多臂老虎机；Beacon 筛选 + LinUCB 路由；次线性 regret 界，agent 失效下自愈 | [中文版](https://github.com/1parado/multi-agent-article/blob/main/2602.00966_Symphony-Coord_中文版.html) · [PDF](https://arxiv.org/pdf/2602.00966.pdf) · [arXiv](https://arxiv.org/abs/2602.00966) |
| 11 | **HEART** 自然语言工具原语 Harness | 2026-09 | Tool Primitive 用 LLM 包装工具、自然语言为接口；ToolFace 检索 25,519 个函数；8B 骨干超商用模型 6%、成本最高 −85%、免疫 prompt injection | [中文版](https://github.com/1parado/multi-agent-article/blob/main/2609.01736_HEART_中文版.html) · [PDF](https://arxiv.org/pdf/2609.01736.pdf) · [arXiv](https://arxiv.org/abs/2609.01736) |

## 共同趋势

1. **性能瓶颈正在从模型转移到模型外围** —— AdaptOrch 给出「模型趋同 → 编排主导」的定量证明；MUSE 证明多数多模态失败是 harness 层缺陷；Meta-Harness 实测 harness 差异可达 6 倍。
2. **「验证」是被反复确认的最有价值组件** —— VMAO 的编排层验证器带来 +35% 完整性；MUSE 的外置确定性验证器是修复循环的地基。共同原则：把生成与评估解耦，用模型外的信号判定成败。
3. **更多调用 ≠ 更好** —— MUSE 的等预算自一致性对照几乎无提升；NLAH 的多候选搜索分支翻倍却拖累成绩；MoRe 用激活混合替代多轮文本，约 20× 更省。
4. **从静态编排到自生成与可恢复安全** —— MAS² 打破 generate-once；SoK 强调路径闭合与恢复，而非仅局部检查。

## 建议阅读顺序

**Meta-Harness**（harness 是什么）→ **NLAH** / **MUSE**（harness 工程）→ **AdaptOrch** / **VMAO**（编排）→ **MAS²**（自生成）→ **MoRe**（激活空间协同）→ **SoK**（安全系统化）→ **OI-MAS** / **Symphony-Coord**（路由与去中心化协调）→ **HEART**（工具使用 harness）

## 站点功能

纯静态、零构建依赖（双击 `index.html` 即可浏览）。阅读侧提供：分类色签与类别筛选 / 关键词检索、随文术语链（点状下划线 → [术语表](glossary.html)）、悬浮章节目录 + 滚动高亮、阅读进度条、标题锚点复制、键盘 ←/→ 翻页、一键复制 BibTeX / APA 引用、打印导出（自动隐藏悬浮控件）、返回顶部与移动端适配；站点侧提供 [关于页](about.html)（收录标准 / 更新记录 / 反馈）与 GitHub Pages 分享预览（OG / favicon）。

## 仓库结构

```
.
├── README.md
├── AGENT.md            # 页面编写规范（链接/导航/组件 v1-v4，新页面必读）
├── hero.svg
├── favicon.svg
├── index.html          # 目录：筛选 + 对比表 + 阅读顺序
├── glossary.html       # 术语表（30 词条，供正文 gloss 链）
├── about.html          # 关于 / 收录标准 / 更新记录
├── 2603.11445_VMAO_中文版.html
├── 2602.16873_AdaptOrch_中文版.html
├── 2603.25723_NLAH_中文版.html
├── 2603.28052_Meta-Harness_中文版.html
├── 2606.03005_MUSE_中文版.html
├── 2608.27338_MoRe_中文版.html
├── 2609.00595_SoK_中文版.html
├── 2509.24323_MAS2_中文版.html
├── 2601.04861_OI-MAS_中文版.html
├── 2602.00966_Symphony-Coord_中文版.html
├── 2609.01736_HEART_中文版.html
└── *.pdf
```

## 本地浏览

```bash
git clone https://github.com/1parado/multi-agent-article.git
```

克隆后直接用浏览器打开 `index.html` 即可（页面内链接指向 GitHub，联网时点击可跳转）。

---

> 论文版权归原作者与出版方所有；中文内容为学习交流整理，引用请以英文原文为准。
