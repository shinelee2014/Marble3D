import json
import os
import sys

# Reconfigure stdout/stderr to UTF-8 to prevent encoding crashes on Windows terminal
if sys.stdout is not None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if sys.stderr is not None:
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

def load_topic(topic_id):
    topics_file = os.path.join(DATA_DIR, "topics.json")
    if not os.path.exists(topics_file):
        print(f"Error: {topics_file} not found.")
        return None
        
    with open(topics_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    for t in data["topics"]:
        if t["id"] == topic_id:
            return t
    return None

def create_prompt(topic):
    prompt_template = f"""你是一位资深小学金牌教师与教育科普视频制作人。
请针对以下小学知识点，设计一份面向 8-12 岁儿童的【30秒趣味微视频解说词与脚本】。

【知识点详情】
- 学科：{topic['subject']}
- 领域：{topic.get('domain', '默认')}
- 年龄段：{topic.get('ageRangeStart', '?')}-{topic.get('ageRangeEnd', '?')} 岁
- 核心概念：{topic['name']}
- 教学目标（概念说明）：{topic['description']}
- 学生掌握标准（Evidence Criteria）：
{chr(10).join(['  * ' + e for e in topic.get('evidence', [])])}

【解说词脚本格式要求】
1. **开场（0-5秒）**：用一个生活中的有趣现象或提问切入，抓住孩子注意力。
2. **知识讲解（5-20秒）**：用最浅显、形象的白话（例如使用比喻）讲解该概念，绝对不要念经式的定义。
3. **互动测试（20-30秒）**：给出一个简单的互动小问答（可参考下方家校提问模板），让孩子在视频前进行思考。
4. **视频画面指示**：每一句解说词后面，用方括号 [画面：...] 标注视频画面的视觉变化，以便自动生成动画。

【家校提问参考模板】
{topic.get('assessmentPrompt', '无')}

请直接输出剧本，不要有多余的客套话。
"""
    return prompt_template

def main():
    if len(sys.argv) < 2:
        print("使用方法: python generate_lesson.py [Topic_ID]")
        print("例如: python generate_lesson.py mt_N8CpN1EJrP")
        print("\n--- 常用 Topic IDs 推荐 ---")
        print("mt_N8CpN1EJrP - 句子构建 (English)")
        print("mt_WcfaSfVT33 - 一对一计数 (Math)")
        print("mt_v3Vz_Pgjjv - 动物分布 (Science)")
        print("mt_B1LdSGMP66 - 埃及考古学伦理 (History)")
        return
        
    topic_id = sys.argv[1]
    topic = load_topic(topic_id)
    
    if not topic:
        print(f"未找到 ID 为 {topic_id} 的知识点。")
        return
        
    print(f"==================================================")
    print(f"Topic: {topic['name']} ({topic['subject']})")
    print(f"==================================================")
    
    prompt = create_prompt(topic)
    print("\n[AI 视频脚本生成 Prompt 已构建]:\n")
    print(prompt)
    
    print("-" * 50)
    print("💡 下一步建议: 您可以将此 Prompt 传入大模型 (OpenAI / Ollama / Claude) 获取定制解说脚本。")
    print("结合 TTS (如 Edge TTS) 和 Whisper，可将此脚本自动转化为音画同步科普视频大纲！")

if __name__ == "__main__":
    main()
