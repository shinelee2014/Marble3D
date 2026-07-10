import json
import os

# 数据路径
DATA_DIR = r"d:\antigravity\app\Taxonomy\data"

# 1. 加载数据
with open(os.path.join(DATA_DIR, "topics.json"), "r", encoding="utf-8") as f:
    topics = json.load(f)["topics"]
with open(os.path.join(DATA_DIR, "dependencies.json"), "r", encoding="utf-8") as f:
    dependencies = json.load(f)["dependencies"]

topic_map = {t["id"]: t for t in topics}

# 2. 编写查询函数：查找某主题直接解锁的后置知识
def find_what_this_unlocks(topic_name_keyword):
    # 模糊匹配找到 topic
    matched = [t for t in topics if t["name"] and topic_name_keyword.lower() in t["name"].lower()]
    if not matched:
        print("未找到匹配的主题")
        return
    
    target = matched[0]
    print(f"🎯 目标概念: {target['name']} ({target['subject']} | Age: {target.get('ageRangeStart')}-{target.get('ageRangeEnd')})")
    print(f"📖 描述: {target['description']}\n")
    
    # 查找以 target['id'] 作为 prerequisiteId 的依赖关系
    unlocks = [d for d in dependencies if d["prerequisiteId"] == target["id"]]
    
    if not unlocks:
        print("💡 该概念是最顶层概念，暂无解锁的后置技能。")
    else:
        print(f"🚀 掌握该概念后，将解锁以下 {len(unlocks)} 个概念：")
        for u in unlocks:
            next_topic = topic_map.get(u["topicId"])
            if next_topic:
                print(f"  - [{next_topic['subject']}] {next_topic['name']} (原因: {u.get('reason')})")

# 3. 示例测试：看看学完“句子构建 (Building sentences)”后可以学什么
find_what_this_unlocks("Building sentences")