# -*- coding: utf-8 -*-
"""v4 术语链接预扫描：统计各论文页（tldr..nav 段）候选术语的出现情况，用于确定每页要链接的术语。"""
import re, glob, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

FILES = sorted(glob.glob("D:/multi-agent-article/*_中文版.html"))

# 候选术语：id -> 该术语在正文中的可能写法（按优先顺序）
CANDS = {
    "dag":            ["DAG"],
    "verifier":       ["Verifier", "验证器", "检查员"],
    "orchestration":  ["orchestration", "编排"],
    "framework":      ["framework", "multi-agent framework"],
    "mas":            ["多智能体系统（MAS）", "多智能体系统", "MAS"],
    "harness":        ["agent harness", "harness"],
    "planner":        ["Planner", "规划器", "规划器模块"],
    "router":         ["Router", "路由器", "路由模块"],
    "model-routing":  ["模型路由", "跨模型路由", "置信感知路由"],
    "codebook":       ["codebook", "Codebook"],
    "steering":       ["steering vector", "激活引导", "Steering"],
    "grpo":           ["GRPO"],
    "sft":            ["SFT", "监督微调"],
    "linucb":         ["LinUCB"],
    "bandit":         ["contextual bandit", "多臂老虎机", "bandit"],
    "regret":         ["regret", "遗憾"],
    "prompt-injection": ["prompt injection", "提示注入", "Prompt Injection"],
    "asr":            ["ASR"],
    "schema":         ["API schema", "schema"],
    "semantic-search":["语义检索", "semantic search"],
    "scaling-law":    ["缩放定律", "scaling law"],
    "confidence":     ["置信度", "confidence"],
    "pareto":         ["Pareto", "帕累托"],
    "calibration":    ["校准", "calibration"],
    "llm":            ["LLM"],
    "mllm":           ["MLLM", "多模态大语言模型"],
    "token":          ["token", "词元"],
    "moe":            ["MoE", "混合专家"],
    "sota":           ["SOTA", "state-of-the-art"],
    "benchmark":      ["benchmark", "基准"],
    "agent":          ["agent", "Agent"],
    "routing":        ["路由"],
}

def body_seg(text):
    s = text.find('<div class="tldr">')
    e = text.find('<div class="nav">')
    if s == -1 or e == -1 or e < s:
        return None
    return text[s:e]

for f in FILES:
    txt = open(f, encoding="utf-8").read()
    seg = body_seg(txt)
    if seg is None:
        print("!! 无 tldr..nav 段:", f)
        continue
    # 屏蔽 <h3>..</h3> 内部
    masked = re.sub(r"<h3.*?</h3>", lambda m: " " * len(m.group(0)), seg, flags=re.S)
    found = []
    for tid, al in CANDS.items():
        best = None
        for a in al:
            i = masked.find(a)
            if i != -1 and (best is None or i < best[1]):
                best = (a, i)
        if best:
            found.append((best[1], tid, best[0]))
    found.sort()
    name = f.split("\\")[-1].split("/")[-1][:12]
    print(name, "->", ", ".join(t for _, t, _ in found))
