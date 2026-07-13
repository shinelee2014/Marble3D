#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
import_and_align_exams.py
江苏小升初 / 分班考真题智能融合脚本
===========================================
功能：
  1. 扫描 Y: 盘中 2025 / 2026 年江苏各科真题文件（.docx / .txt）
  2. 按题号正则切分题目文本
  3. 调用本地 LM Studio（OpenAI兼容 API）将题目对齐至 topics_cn.json 节点
  4. 若题目考察内容超出当前 175 个节点，AI 将建议新增高阶知识点
  5. 将对齐结果写回 data/topics_cn.json 的 examQuestions 字段

用法:
  python scripts/import_and_align_exams.py [--dry-run] [--year 2025] [--subject 数学]

依赖:
  pip install python-docx tqdm
"""

import os
import re
import json
import socket
import argparse
import urllib.request as urlreq
from pathlib import Path
from datetime import datetime

# ─── 路径配置 ───────────────────────────────────────────────────────────────
EXAM_ROOT = Path(r"Y:\doc\study\小学辅导\05_升学与小升初\小升初历年真题\4.江苏")

SUBJECT_DIRS = {
    "数学": "江苏数学小升初-144套（更新至2024年）",
    "英语": "江苏英语小升初-82套（更新至2024年）",
    "语文": "江苏语文小升初-98套（更新至2024年）",
}

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TOPICS_JSON  = PROJECT_ROOT / "data" / "topics_cn.json"
LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"

# ─── 题号正则（支持：1. / (1) / 一、/ 第1题 等常见格式）────────────────────
Q_PATTERN = re.compile(
    r"(?:^|\n)\s*"
    r"(?:\d{1,3}[\.\、\)\．]|（\d{1,3}）|第\s*\d{1,3}\s*题)"
    r"\s*(.+?)(?=\n\s*(?:\d{1,3}[\.\、\)\．]|（\d{1,3}）|第\s*\d{1,3}\s*题)|\Z)",
    re.DOTALL
)


# ─── 工具函数 ────────────────────────────────────────────────────────────────

def check_lm_studio() -> bool:
    """检查 LM Studio 是否在 1234 端口监听。"""
    try:
        with socket.create_connection(("127.0.0.1", 1234), timeout=1):
            return True
    except Exception:
        return False


def call_lm_studio(prompt: str, max_tokens: int = 600) -> str | None:
    """发送 prompt 至 LM Studio，返回文本或 None。"""
    payload = json.dumps({
        "model": "local-model",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
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
        print(f"  [LM Studio 错误] {e}")
        return None


def read_docx(path: Path) -> str:
    """读取 .docx 文件，返回纯文本。"""
    try:
        from docx import Document
        doc = Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except ImportError:
        print("  [警告] python-docx 未安装，跳过 .docx 文件。请运行: pip install python-docx")
        return ""
    except Exception as e:
        print(f"  [读取错误] {path.name}: {e}")
        return ""


def read_txt(path: Path) -> str:
    """读取 .txt 文件，尝试多种编码。"""
    for enc in ("utf-8", "gbk", "utf-8-sig", "gb2312"):
        try:
            return path.read_text(encoding=enc)
        except Exception:
            continue
    return ""


def extract_questions(text: str) -> list[str]:
    """从试卷文本中抽取题目列表。"""
    matches = Q_PATTERN.findall(text)
    # 清理空白并过滤过短内容（<10 字符）
    questions = [m.strip() for m in matches if len(m.strip()) >= 10]
    return questions


def load_topics() -> tuple[dict, list]:
    """加载 topics_cn.json，返回 (raw_data, topics_list)。"""
    with open(TOPICS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    topics = data.get("topics", [])
    return data, topics


def save_topics(data: dict):
    """将修改后的 data 写回 topics_cn.json（带格式化缩进）。"""
    with open(TOPICS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  [已保存] {TOPICS_JSON}")


def build_topic_index(topics: list) -> dict[str, dict]:
    """构建 id -> topic 的快速索引。"""
    return {t["id"]: t for t in topics}


def build_topic_summary(topics: list, subject_filter: str | None = None) -> str:
    """生成简洁的知识点列表供 AI 参考（id: 年级 学科 名称）。"""
    lines = []
    for t in topics:
        if subject_filter and t.get("subject", "") != subject_filter:
            continue
        grade_start = t.get("ageRangeStart", 0) - 5  # 6岁=1年级
        grade_end   = t.get("ageRangeEnd", 0) - 5
        grade_str   = f"{grade_start}" if grade_start == grade_end else f"{grade_start}-{grade_end}"
        lines.append(f'{t["id"]}: [{grade_str}年级] [{t.get("subject","?")}] {t.get("name","?")}')
    return "\n".join(lines)


# ─── AI 对齐核心逻辑 ─────────────────────────────────────────────────────────

ALIGN_PROMPT_TEMPLATE = """\
你是一位专业的中国小学课程分析专家。

以下是一道来自【{year}年{origin}】的小升初/分班考试真题：
---题目---
{question}
---结束---

以下是当前课程图谱中的知识点列表（格式：节点ID: [年级] [学科] 节点名称）：
{topic_list}

请分析该题目考察的核心知识点，并按以下 JSON 格式输出（只输出 JSON，不要其他说明）：

{{
  "matched_topic_id": "节点ID 或 null（如果没有合适的匹配）",
  "match_confidence": "high/medium/low",
  "match_reason": "简短说明为什么匹配该节点（中文，20字以内）",
  "question_type": "选择题/填空题/计算题/应用题/判断题/其他",
  "difficulty": "基础/中等/提高/竞赛",
  "new_node_suggestion": {{
    "needed": false,
    "name": "新节点名称（如果 matched_topic_id 为 null）",
    "subject": "学科",
    "grade": "6",
    "description": "新节点描述",
    "parent_id": "建议的父节点ID"
  }}
}}
"""


def align_question_with_ai(
    question: str,
    year: str,
    origin: str,
    topic_summary: str,
    subject: str,
) -> dict | None:
    """调用 LM Studio 将单道题目对齐到知识点节点。"""
    prompt = ALIGN_PROMPT_TEMPLATE.format(
        year=year,
        origin=origin,
        question=question[:800],   # 截断避免超 token
        topic_list=topic_summary,
    )
    response = call_lm_studio(prompt, max_tokens=400)
    if not response:
        return None
    # 提取 JSON 块
    json_match = re.search(r"\{.*\}", response, re.DOTALL)
    if not json_match:
        print(f"  [警告] AI 返回内容无法解析为 JSON: {response[:100]}")
        return None
    try:
        return json.loads(json_match.group())
    except json.JSONDecodeError as e:
        print(f"  [解析错误] {e}: {json_match.group()[:100]}")
        return None


# ─── 新节点创建逻辑 ──────────────────────────────────────────────────────────

def create_new_topic(suggestion: dict, topics: list, topic_index: dict) -> str | None:
    """
    根据 AI 建议的 new_node_suggestion 在 topics 列表中创建新节点。
    返回新节点的 ID，或 None（如果创建失败）。
    """
    name    = suggestion.get("name", "").strip()
    subject = suggestion.get("subject", "").strip()
    grade   = int(suggestion.get("grade", 6))
    desc    = suggestion.get("description", "")
    parent  = suggestion.get("parent_id", "")

    if not name or not subject:
        return None

    # 生成唯一 ID
    subj_map = {"数学": "math", "语文": "chin", "英语": "eng",
                "科学": "sci",  "道德与法治": "morality"}
    subj_en = subj_map.get(subject, "misc")
    existing_ids = [t["id"] for t in topics if t["id"].startswith(f"sz_{subj_en}_{grade}")]
    suffix = len(existing_ids) + 100  # 从 100 起以区分人工创建
    new_id = f"sz_{subj_en}_{grade}_{suffix}"

    age_start = grade + 5
    age_end   = grade + 6

    new_topic = {
        "id": new_id,
        "type": "CONCEPTUAL",
        "subject": subject,
        "domain": "竞赛/高阶",
        "name": name,
        "description": desc,
        "ageRangeStart": age_start,
        "ageRangeEnd": age_end,
        "centrality": 0.05,
        "evidence": [],
        "assessmentPrompt": f"{{{{name}}}}，请解答这道关于{name}的题目。",
        "standards": [],
        "examQuestions": [],
        "isExamDerived": True,     # 标记来源于真题分析
        "parentSuggestion": parent,
    }

    topics.append(new_topic)
    topic_index[new_id] = new_topic
    print(f"  [新节点] 已创建: {new_id} — {name}")
    return new_id


# ─── 主流程 ──────────────────────────────────────────────────────────────────

def process_file(
    filepath: Path,
    year: str,
    subject: str,
    origin: str,
    topics: list,
    topic_index: dict,
    topic_summary: str,
    dry_run: bool,
) -> int:
    """处理单个试卷文件，返回成功对齐的题目数。"""
    ext = filepath.suffix.lower()
    if ext == ".docx":
        text = read_docx(filepath)
    elif ext == ".txt":
        text = read_txt(filepath)
    else:
        return 0

    if not text.strip():
        print(f"  [跳过] 空文件: {filepath.name}")
        return 0

    questions = extract_questions(text)
    if not questions:
        print(f"  [提示] 未能从 {filepath.name} 中切分到题目（可能格式特殊）")
        return 0

    print(f"  → 检测到 {len(questions)} 道题目，开始 AI 对齐…")
    aligned_count = 0

    for i, q in enumerate(questions, 1):
        print(f"    [{i}/{len(questions)}] {q[:50]}…", end=" ")
        result = align_question_with_ai(q, year, origin, topic_summary, subject)
        if not result:
            print("跳过（AI 无响应）")
            continue

        matched_id  = result.get("matched_topic_id")
        confidence  = result.get("match_confidence", "low")
        reason      = result.get("match_reason", "")
        q_type      = result.get("question_type", "其他")
        difficulty  = result.get("difficulty", "中等")
        new_sug     = result.get("new_node_suggestion", {})

        # 如果没有匹配且 AI 建议新建节点
        if not matched_id and new_sug.get("needed"):
            if not dry_run:
                matched_id = create_new_topic(new_sug, topics, topic_index)
            else:
                print(f"[DRY-RUN] 将新建节点: {new_sug.get('name')}")
                matched_id = None

        if matched_id and matched_id in topic_index:
            topic = topic_index[matched_id]
            # 确保 examQuestions 字段存在
            if "examQuestions" not in topic:
                topic["examQuestions"] = []

            # 避免重复插入（按年份+题干前30字去重）
            dup_key = f"{year}_{q[:30]}"
            existing_keys = [f"{eq.get('year','')}_{eq.get('questionText','')[:30]}"
                             for eq in topic["examQuestions"]]
            if dup_key in existing_keys:
                print(f"已存在，跳过重复题目")
                continue

            exam_entry = {
                "id": f"eq_{year}_{matched_id}_{i:03d}",
                "year": year,
                "origin": origin,
                "subject": subject,
                "questionType": q_type,
                "difficulty": difficulty,
                "questionText": q[:500],   # 最多 500 字
                "answer": "",              # 预留，后续可手动补充
                "matchConfidence": confidence,
                "matchReason": reason,
                "importedAt": datetime.now().strftime("%Y-%m-%d"),
            }

            if not dry_run:
                topic["examQuestions"].append(exam_entry)

            print(f"✓ → {matched_id} [{confidence}] {reason}")
            aligned_count += 1
        else:
            print(f"✗ 未匹配（{confidence}）")

    return aligned_count


def main():
    parser = argparse.ArgumentParser(description="江苏小升初真题智能融合工具")
    parser.add_argument("--dry-run", action="store_true", help="试运行，不修改任何文件")
    parser.add_argument("--year",    default=None, help="只处理指定年份 (如 2025 或 2026)")
    parser.add_argument("--subject", default=None, help="只处理指定学科 (数学/语文/英语)")
    args = parser.parse_args()

    print("=" * 60)
    print("  江苏小升初 2025-2026 真题智能融合工具")
    print("=" * 60)

    # 检查 LM Studio
    if not check_lm_studio():
        print("[错误] LM Studio 未启动（端口 1234 未响应）。请先启动 LM Studio 并加载模型。")
        return

    print("[✓] LM Studio 已连接")

    # 加载知识点图谱
    data, topics = load_topics()
    topic_index  = build_topic_index(topics)
    print(f"[✓] 已加载 {len(topics)} 个知识点节点")

    total_aligned = 0

    # 遍历学科
    subjects_to_process = [args.subject] if args.subject else list(SUBJECT_DIRS.keys())
    years_to_process    = [args.year] if args.year else ["2025", "2026"]

    for subject in subjects_to_process:
        subj_dir = EXAM_ROOT / SUBJECT_DIRS[subject]
        if not subj_dir.exists():
            print(f"\n[跳过] 目录不存在: {subj_dir}")
            continue

        # 预生成该学科的知识点摘要（避免多余 token）
        topic_summary = build_topic_summary(topics, subject_filter=subject)

        for year in years_to_process:
            year_dir = subj_dir / year
            if not year_dir.exists():
                print(f"\n[跳过] 目录不存在: {year_dir}")
                continue

            files = list(year_dir.glob("*.docx")) + list(year_dir.glob("*.txt"))
            if not files:
                print(f"\n[提示] {year_dir} 目录下暂无试卷文件（.docx/.txt）")
                continue

            print(f"\n── {year}年 {subject} ── {len(files)} 份试卷 ──")

            for filepath in sorted(files):
                origin = filepath.stem  # 用文件名作为来源标识
                print(f"\n  [文件] {filepath.name}")
                n = process_file(
                    filepath, year, subject, origin,
                    topics, topic_index, topic_summary,
                    args.dry_run
                )
                total_aligned += n
                print(f"  ✓ 本文件对齐 {n} 题")

    # 保存结果
    if total_aligned > 0 and not args.dry_run:
        data["topics"] = topics
        data["topicCount"] = len(topics)
        save_topics(data)
        print(f"\n[完成] 共对齐 {total_aligned} 道真题到图谱节点。")
    elif args.dry_run:
        print(f"\n[DRY-RUN 完成] 共扫描到 {total_aligned} 道可对齐题目（未写入文件）。")
    else:
        print("\n[完成] 未发现可对齐的题目，topics_cn.json 未修改。")


if __name__ == "__main__":
    main()
