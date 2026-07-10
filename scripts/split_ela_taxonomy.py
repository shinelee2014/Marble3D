import json
import os
import re
import sys

# Configure stdout/stderr encoding for Windows
if sys.stdout is not None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DATA_DIR = r"d:\antigravity\app\Taxonomy\data"
topics_cn_file = os.path.join(DATA_DIR, "topics_cn.json")

if not os.path.exists(topics_cn_file):
    print("Error: data/topics_cn.json does not exist!")
    exit(1)

with open(topics_cn_file, "r", encoding="utf-8") as f:
    topics_data = json.load(f)

# English keywords that signify English language specific concepts
english_keywords = [
    r"\ba\b", r"\ban\b", r"\bthe\b", r"\bverb", r"\btens", r"\bpronoun", 
    r"\bplural", r"\bdeterminer", r"\badverb", r"\badject", r"\bcapital",
    r"\bspell", r"\bapostroph", r"\bphonic", r"\balphabet", r"\bletter", 
    r"\bvowel", r"\bconsonant", r"\bprefix", r"\bsuffix", r"\bhomophon", 
    r"\bsyllabl", r"\bcontraction", r"\bclause", r"\bgerund", r"\bsubjun",
    r"\bpassive\b", r"\bmodal\b", r"\bpreposition", r"\bconjunction", r"\bdeterminer"
]

# Chinese keywords that signify English grammar or spelling
english_cn_keywords = [
    "冠词", "代词", "时态", "过去式", "过去时", "现在时", "进行时", "将来时", "完成时", 
    "音素", "音节", "拼写", "英文", "字母", "元音", "辅音", "撇号", "不规则", 
    "主谓一致", "形容词顺序", "单复数", "大写字母", "连词", "介词", "前缀", "后缀", "同音词", "词汇库"
]

modified_count = 0
chinese_count = 0
english_count = 0

for t in topics_data["topics"]:
    # Since we might have already split some into '语文' or '英语', let's check for '语文与英语', '语文' and '英语'
    # Actually, ELA was originally "English" in subjects, so if it is '语文' or '英语' or '语文与英语', we can re-evaluate them
    if t["subject"] in ["语文与英语", "语文", "英语"]:
        name_lower = t["name"].lower()
        desc_lower = t["description"].lower()
        
        is_english = False
        
        for kw in english_keywords:
            if re.search(kw, name_lower) or re.search(kw, desc_lower):
                is_english = True
                break
                
        if not is_english:
            for kw in english_cn_keywords:
                if kw in t["name"] or kw in t["description"]:
                    is_english = True
                    break
                    
        if is_english:
            t["subject"] = "英语"
            english_count += 1
        else:
            t["subject"] = "语文"
            chinese_count += 1
            
        modified_count += 1

with open(topics_cn_file, "w", encoding="utf-8") as f:
    json.dump(topics_data, f, indent=2, ensure_ascii=False)

print("==================================================")
print("Finished ELA splitting successfully!")
print(f"  - Total classified ELA: {modified_count}")
print(f"  - Classified as Chinese (语文): {chinese_count}")
print(f"  - Classified as English (英语): {english_count}")
print("==================================================")
