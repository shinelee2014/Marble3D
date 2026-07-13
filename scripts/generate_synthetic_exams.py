#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_synthetic_exams.py
小升初/分班考 2025-2026 仿真真题智能生成器
=================================================
功能：
  1. 扫描 topics_cn.json，过滤出六年级核心节点 (ageRangeStart >= 11)。
  2. 调用本地 LM Studio 针对每个节点生成 1 道 2025 年和 1 道 2026 年的小升初/分班考仿真真题。
  3. 将题目及标准答案直接注入 examQuestions 数组，并写回 topics_cn.json。
"""

import os
import re
import json
import socket
import urllib.request as urlreq
from pathlib import Path
from datetime import datetime

# ─── 路径与配置 ─────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TOPICS_JSON  = PROJECT_ROOT / "data" / "topics_cn.json"
LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"

def check_lm_studio() -> bool:
    try:
        with socket.create_connection(("127.0.0.1", 1234), timeout=1):
            return True
    except Exception:
        return False

def call_lm_studio(prompt: str, max_tokens: int = 800) -> str | None:
    payload = json.dumps({
        "model": "local-model",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
        "max_tokens": max_tokens,
    }).encode("utf-8")
    req = urlreq.Request(
        LM_STUDIO_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urlreq.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"  [AI 错误] {e}")
        return None

# ─── 核心 Prompt 模板 ────────────────────────────────────────────────────────
PROMPT_TEMPLATE = """\
你是一位精通中国江苏省小升初与重点初中分班考试的命题专家（针对苏教版数学、部编版语文、译林版英语）。

当前知识点：
- 学科: {subject}
- 节点名称: {name}
- 节点描述: {description}

请为这个知识点，出1道仿真【{year}年】江苏省（如南京、苏州、无锡等）重点中学小升初毕业调研卷或分班考的真题。

要求：
1. 题目质量极高，难度符合小升初/分班考选拔水准。
2. 严禁使用任何 LaTeX 或美元符号（不要写 $...$ ），公式和变量一律写成普通文本，如 x、y、3/4、3.14。
3. 请以简洁的 JSON 格式输出，不要包含 Markdown 代码块或多余文字。

输出 JSON 格式：
{{
  "year": "{year}",
  "origin": "2025年南京玄武区毕业联考" 或 "2026年苏州立达中学分班测验" (依年份设计一个合理的江苏名校/地区来源),
  "questionType": "计算题/应用题/填空题/阅读理解/语法选择/古诗词鉴赏",
  "difficulty": "基础/中等/提高/竞赛 (根据命题难度选择)",
  "questionText": "在这里写题目题干（要求描述清晰、格式规整）",
  "answer": "在这里写解题步骤与标准答案"
}}
"""

def generate_exam_for_topic(topic: dict, year: str) -> dict | None:
    prompt = PROMPT_TEMPLATE.format(
        subject=topic.get("subject", ""),
        name=topic.get("name", ""),
        description=topic.get("description", ""),
        year=year
    )
    resp = call_lm_studio(prompt)
    if not resp:
        return None
    
    # 提取 JSON
    json_match = re.search(r"\{.*\}", resp, re.DOTALL)
    if not json_match:
        return None
    try:
        data = json.loads(json_match.group())
        # 添加辅助元数据
        data["id"] = f"eq_synthetic_{year}_{topic['id']}"
        data["matchConfidence"] = "high"
        data["matchReason"] = "AI 考纲定向合成"
        data["importedAt"] = datetime.now().strftime("%Y-%m-%d")
        return data
    except Exception as e:
        print(f"解析 AI JSON 失败: {e}")
        return None

def main():
    print("=" * 60)
    print("  小升初 2025-2026 仿真真题智能生成器")
    print("=" * 60)

    if not check_lm_studio():
        print("[错误] LM Studio 未启动（1234 端口未监听），请先开启并加载模型。")
        return

    # 读取 topics
    with open(TOPICS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    topics = data.get("topics", [])
    
    # 筛选六年级核心节点
    target_topics = [t for t in topics if t.get("ageRangeStart", 0) >= 11]
    print(f"[✓] 筛选出 {len(target_topics)} 个六年级核心知识点。")

    success_count = 0

    for idx, t in enumerate(target_topics, 1):
        print(f"\n[{idx}/{len(target_topics)}] 正在为【{t.get('subject')} · {t.get('name')}】生成仿真题...")
        
        if "examQuestions" not in t:
            t["examQuestions"] = []

        # 检查是否已经有了 2025/2026 的仿真题，避免重复生成
        has_2025 = any(eq.get("year") == "2025" for eq in t["examQuestions"])
        has_2026 = any(eq.get("year") == "2026" for eq in t["examQuestions"])

        if not has_2025:
            print("  -> 生成 2025 年真题...", end=" ")
            eq_25 = generate_exam_for_topic(t, "2025")
            if eq_25:
                t["examQuestions"].append(eq_25)
                print("成功")
                success_count += 1
            else:
                print("失败")

        if not has_2026:
            print("  -> 生成 2026 年真题...", end=" ")
            eq_26 = generate_exam_for_topic(t, "2026")
            if eq_26:
                t["examQuestions"].append(eq_26)
                print("成功")
                success_count += 1
            else:
                print("失败")
        
        # 每生成一个就保存一次，防止中途中断导致前功尽弃
        if success_count > 0:
            data["topics"] = topics
            data["topicCount"] = len(topics)
            with open(TOPICS_JSON, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n[✓] 生成完成！共成功注入了 {success_count} 道仿真真题到 data/topics_cn.json。")

if __name__ == "__main__":
    main()
