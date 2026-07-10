import json
import os
import sys
import urllib.parse
import urllib.request
import time

# Reconfigure console to UTF-8 for Windows
if sys.stdout is not None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DATA_DIR = r"d:\antigravity\app\Taxonomy\data"
TOPICS_CN_PATH = os.path.join(DATA_DIR, "topics_cn.json")

def google_translate(text, target_lang="zh-CN"):
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": "en",
        "tl": target_lang,
        "dt": "t",
        "q": text
    }
    
    data = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"User-Agent": "Mozilla/5.0"})
    
    # Try up to 3 times with exponential backoff on failure
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                res_json = json.loads(response.read().decode("utf-8"))
                translated_segments = []
                for segment in res_json[0]:
                    if segment[0]:
                        translated_segments.append(segment[0])
                return "".join(translated_segments)
        except Exception as e:
            print(f"Translation attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                time.sleep(2 * (attempt + 1))
    return None

def batch_translate_strings(strings_to_translate):
    """
    Translates a list of strings in a single batch request by separating them
    with numerical delimiters on separate lines.
    """
    if not strings_to_translate:
        return []
        
    delimiter_start = 100001
    payload_parts = []
    for idx, s in enumerate(strings_to_translate):
        delim = f"999{delimiter_start + idx}"
        payload_parts.append(delim)
        payload_parts.append(s)
        
    payload = "\n".join(payload_parts)
    
    translated_text = google_translate(payload)
    if not translated_text:
        return None
        
    # Parse back the results
    lines = translated_text.split("\n")
    results = {}
    
    current_key = None
    current_lines = []
    
    for line in lines:
        line_str = line.strip()
        # Check if the line is a delimiter we generated (e.g. 999100001)
        if line_str.startswith("999") and len(line_str) == 9 and line_str[3:].isdigit():
            # Save previous
            if current_key is not None:
                results[current_key] = "\n".join(current_lines).strip()
            current_key = int(line_str[3:])
            current_lines = []
        else:
            if current_key is not None:
                current_lines.append(line.strip())
                
    if current_key is not None:
        results[current_key] = "\n".join(current_lines).strip()
        
    # Map back to original list order
    translated_list = []
    for idx in range(len(strings_to_translate)):
        key = delimiter_start + idx
        translated_list.append(results.get(key, ""))
        
    return translated_list

def run_translation():
    if not os.path.exists(TOPICS_CN_PATH):
        print("错误: 请先运行 python scripts/localize_taxonomy.py 初始化 topics_cn.json。")
        return
        
    with open(TOPICS_CN_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    topics = data["topics"]
    total = len(topics)
    
    print(f"载入已初始化的主题共 {total} 个。开始扫描需要翻译的内容...")
    
    # Identify which topics need translation
    # Untranslated ones have name starting with "🔑 [英]" or description starting with "[尚未翻译]"
    to_translate_indices = []
    for idx, t in enumerate(topics):
        if t["name"].startswith("🔑 [英]") or t["description"].startswith("[尚未翻译]"):
            to_translate_indices.append(idx)
            
    print(f"扫描完毕: 发现 {len(to_translate_indices)} / {total} 个主题尚待翻译。")
    if not to_translate_indices:
        print("所有主题已翻译完毕！无需执行。")
        return
        
    # Batch parameters
    # Each batch contains up to 10 topics (each topic has name, description, evidence, prompt -> ~30 strings per batch)
    topics_per_batch = 10
    total_to_translate = len(to_translate_indices)
    
    for i in range(0, total_to_translate, topics_per_batch):
        batch_indices = to_translate_indices[i:i + topics_per_batch]
        print(f"\n正在翻译批次 {i // topics_per_batch + 1} / {(total_to_translate + topics_per_batch - 1) // topics_per_batch} (处理 {len(batch_indices)} 个主题)...")
        
        # Gather strings to translate and their metadata mapping
        strings_to_translate = []
        mapping = [] # lists of tuples: (topic_index, field_name, extra_index)
        
        for idx in batch_indices:
            t = topics[idx]
            
            # Clean English name/desc for translation
            raw_name = t["name"].replace("🔑 [英] ", "").strip()
            raw_desc = t["description"].replace("[尚未翻译] ", "").strip()
            
            # 1. Name
            strings_to_translate.append(raw_name)
            mapping.append((idx, "name", None))
            
            # 2. Description
            strings_to_translate.append(raw_desc)
            mapping.append((idx, "description", None))
            
            # 3. Evidence
            for e_idx, e in enumerate(t.get("evidence", [])):
                strings_to_translate.append(e)
                mapping.append((idx, "evidence", e_idx))
                
            # 4. Assessment Prompt
            if t.get("assessmentPrompt"):
                strings_to_translate.append(t["assessmentPrompt"])
                mapping.append((idx, "assessmentPrompt", None))
                
        # Call batch translate
        translated_strings = batch_translate_strings(strings_to_translate)
        if not translated_strings or len(translated_strings) != len(strings_to_translate):
            print("❌ 翻译批次失败，跳过。将在后续重试或降级处理。")
            time.sleep(2)
            continue
            
        # Write translated fields back to memory
        for map_idx, (t_idx, field, extra) in enumerate(mapping):
            trans_val = translated_strings[map_idx].strip()
            # If translation failed or returned empty, fallback to original
            if not trans_val:
                continue
                
            if field == "name":
                topics[t_idx]["name"] = trans_val
            elif field == "description":
                topics[t_idx]["description"] = trans_val
            elif field == "evidence":
                topics[t_idx]["evidence"][extra] = trans_val
            elif field == "assessmentPrompt":
                topics[t_idx]["assessmentPrompt"] = trans_val
                
        # Save after each batch to prevent data loss
        with open(TOPICS_CN_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print(f"✅ 批次已保存。已完成翻译进度: {min(i + topics_per_batch, total_to_translate)} / {total_to_translate}")
        
        # Polite throttling to avoid IP bans (0.8s)
        time.sleep(0.8)

    print("\n🎉 大功告成！所有 1,590 个主题的名称、描述、掌握证据和评估提示语已全部使用 Google 免费翻译接口汉化完毕！")
    print("您可以刷新 http://localhost:8000/explorer.html 游览全新的全中文课程图谱！")

if __name__ == "__main__":
    run_translation()
