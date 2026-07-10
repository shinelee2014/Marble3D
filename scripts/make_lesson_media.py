import json
import os
import sys
import subprocess
import shutil

# Reconfigure console output for Windows terminal
if sys.stdout is not None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Subject HSL colors to map (background gradients)
SUBJECT_THEMES = {
    "数学": {"bg_start": (11, 23, 58), "bg_end": (19, 41, 95), "accent": (59, 130, 246)},
    "科学": {"bg_start": (41, 37, 13), "bg_end": (77, 65, 17), "accent": (202, 138, 4)},
    "语文与英语": {"bg_start": (41, 15, 33), "bg_end": (83, 23, 62), "accent": (219, 39, 119)},
    "历史与社会": {"bg_start": (28, 15, 51), "bg_end": (58, 23, 107), "accent": (147, 51, 234)},
    "道德与法治": {"bg_start": (11, 37, 35), "bg_end": (17, 74, 69), "accent": (13, 148, 136)},
    "生活技能": {"bg_start": (43, 13, 23), "bg_end": (90, 18, 36), "accent": (225, 29, 72)},
    "信息技术": {"bg_start": (10, 27, 43), "bg_end": (14, 58, 92), "accent": (2, 132, 199)},
    "学习方法": {"bg_start": (12, 33, 19), "bg_end": (22, 74, 38), "accent": (22, 163, 74)}
}
DEFAULT_THEME = {"bg_start": (11, 15, 25), "bg_end": (19, 27, 46), "accent": (59, 130, 246)}

def load_topic(topic_id):
    topics_file = os.path.join(DATA_DIR, "topics_cn.json")
    if not os.path.exists(topics_file):
        print(f"错误: {topics_file} 不存在。请先运行本地化脚本。")
        return None
        
    with open(topics_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    for t in data["topics"]:
        if t["id"] == topic_id:
            return t
    return None

def check_dependencies():
    """
    Checks if edge-tts and pillow are installed.
    """
    pillow_installed = True
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        pillow_installed = False
        
    edge_tts_cli = shutil.which("edge-tts")
    
    return pillow_installed, (edge_tts_cli is not None)

def draw_card(topic, file_path):
    """
    Draws a vertical high-definition learning card (1080x1920) for mobile.
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Pillow 库未安装，无法渲染卡片图片。请运行: pip install pillow")
        return False
        
    # Get Theme Colors
    theme = SUBJECT_THEMES.get(topic["subject"], DEFAULT_THEME)
    
    # 1. Create Gradient Background
    img = Image.new("RGB", (1080, 1920), color=theme["bg_start"])
    draw = ImageDraw.Draw(img)
    
    # Draw simple vertical gradient
    for y in range(1920):
        r = int(theme["bg_start"][0] + (theme["bg_end"][0] - theme["bg_start"][0]) * (y / 1920))
        g = int(theme["bg_start"][1] + (theme["bg_end"][1] - theme["bg_start"][1]) * (y / 1920))
        b = int(theme["bg_start"][2] + (theme["bg_end"][2] - theme["bg_start"][2]) * (y / 1920))
        draw.line([(0, y), (1080, y)], fill=(r, g, b))
        
    # Draw border accent line
    draw.rectangle([20, 20, 1060, 1900], outline=theme["accent"], width=4)
    
    # Load fonts - try standard Windows Chinese fonts
    font_paths = [
        "C:\\Windows\\Fonts\\msyh.ttc",  # Microsoft YaHei
        "C:\\Windows\\Fonts\\simhei.ttf",  # SimHei
        "C:\\Windows\\Fonts\\msyhbd.ttc", # Microsoft YaHei Bold
    ]
    
    font_title = None
    font_body = None
    font_small = None
    
    for fpath in font_paths:
        if os.path.exists(fpath):
            try:
                font_title = ImageFont.truetype(fpath, 60)
                font_body = ImageFont.truetype(fpath, 40)
                font_small = ImageFont.truetype(fpath, 32)
                break
            except:
                continue
                
    if not font_title:
        # Fallback to default
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_small = ImageFont.load_default()
        
    # 2. Draw Content
    # Header Info
    draw.text((100, 100), f"学科: {topic['subject']}  |  领域: {topic.get('domain', '默认')}", fill=(156, 163, 175), font=font_small)
    draw.text((100, 150), f"适合年龄: {topic.get('ageRangeStart', '?')}-{topic.get('ageRangeEnd', '?')} 岁", fill=(156, 163, 175), font=font_small)
    
    # Topic Name
    draw.text((100, 230), topic["name"], fill=(255, 255, 255), font=font_title)
    
    # Accent separator
    draw.line([(100, 320), (980, 320)], fill=theme["accent"], width=3)
    
    # 3. Description
    draw.text((100, 360), "💡 概念解释：", fill=theme["accent"], font=font_small)
    
    # Helper to wrap text
    def wrap_text(text, font, max_width):
        lines = []
        words = text
        # Since Chinese has no spaces, wrap by characters
        current_line = ""
        for char in words:
            test_line = current_line + char
            width = draw.textlength(test_line, font=font)
            if width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = char
        if current_line:
            lines.append(current_line)
        return lines
        
    desc_lines = wrap_text(topic["description"].replace("[尚未翻译] ", ""), font_body, 880)
    y_offset = 420
    for line in desc_lines:
        draw.text((100, y_offset), line, fill=(243, 244, 246), font=font_body)
        y_offset += 55
        
    # 4. Evidence
    y_offset += 40
    draw.text((100, y_offset), "✓ 掌握特征 (Evidence)：", fill=theme["accent"], font=font_small)
    y_offset += 60
    
    for ev in topic.get("evidence", []):
        ev_lines = wrap_text(f"• {ev}", font_body, 880)
        for line in ev_lines:
            draw.text((100, y_offset), line, fill=(209, 213, 219), font=font_body)
            y_offset += 55
        y_offset += 15
        
    # 5. Assessment Prompt
    if topic.get("assessmentPrompt"):
        y_offset += 40
        draw.text((100, y_offset), "💬 亲子诊断随口问：", fill=theme["accent"], font=font_small)
        y_offset += 60
        
        prompt_clean = topic["assessmentPrompt"].replace("{{name}}", "孩子")
        prompt_lines = wrap_text(prompt_clean, font_body, 840)
        
        # Draw background container for prompt
        box_height = len(prompt_lines) * 55 + 50
        draw.rectangle([80, y_offset - 20, 1000, y_offset - 20 + box_height], fill=(15, 23, 42), outline=(59, 130, 246), width=2)
        
        for line in prompt_lines:
            draw.text((120, y_offset), line, fill=(147, 197, 253), font=font_body)
            y_offset += 55
            
    # Footer
    draw.text((100, 1800), "© Marble Skill Taxonomy (v1) 本地适配版", fill=(107, 114, 128), font=font_small)
    
    # Save Image
    img.save(file_path)
    return True

def generate_audio(topic, file_path):
    """
    Generates high-quality Mandarin audio using edge-tts.
    """
    clean_desc = topic["description"].replace("[尚未翻译] ", "")
    # Add parent prompt to read for context
    speak_text = f"这里是小学{topic['subject']}微课。关于{topic['name']}。这个概念是指：{clean_desc}。"
    if topic.get("assessmentPrompt"):
        prompt_clean = topic["assessmentPrompt"].replace("{{name}}", "孩子")
        speak_text += f"家长可以在家这样提问测试：{prompt_clean}"
        
    print(f"正在转换语音，播报文本: {speak_text}")
    
    # edge-tts command line:
    # edge-tts --voice zh-CN-XiaoxiaoNeural --text "..." --write-media file_path
    cmd = [
        "edge-tts",
        "--voice", "zh-CN-XiaoxiaoNeural",
        "--text", speak_text,
        "--write-media", file_path
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception as e:
        print(f"生成语音出错 (请确保已安装 edge-tts: pip install edge-tts): {e}")
        return False

def combine_video(image_path, audio_path, output_path):
    """
    Combines PNG and MP3 into MP4 using ffmpeg.
    """
    ffmpeg_bin = shutil.which("ffmpeg")
    if not ffmpeg_bin:
        print("未在系统中找到 ffmpeg，无法渲染最终 MP4 视频。您可以通过 mp3 和 png 手工合成。")
        return False
        
    print("正在使用 ffmpeg 合成音画同步微视频...")
    
    # ffmpeg -loop 1 -i image -i audio -c:v libx264 -tune stillimage -c:a aac -pix_fmt yuv420p -shortest output
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", image_path,
        "-i", audio_path,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest", output_path
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception as e:
        print(f"FFmpeg 合成视频失败: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("使用方法: python make_lesson_media.py [Topic_ID]")
        print("例如: python make_lesson_media.py mt_WcfaSfVT33")
        return
        
    topic_id = sys.argv[1]
    topic = load_topic(topic_id)
    
    if not topic:
        print(f"未找到该知识点 ID: {topic_id}")
        return
        
    print(f"正在为《{topic['name']}》构建多媒体包...")
    
    pillow_ok, tts_ok = check_dependencies()
    
    image_name = f"{topic_id}_card.png"
    audio_name = f"{topic_id}_audio.mp3"
    video_name = f"{topic_id}_lesson.mp4"
    
    image_path = os.path.join(OUTPUT_DIR, image_name)
    audio_path = os.path.join(OUTPUT_DIR, audio_name)
    video_path = os.path.join(OUTPUT_DIR, video_name)
    
    # 1. Generate PNG Card
    if pillow_ok:
        print("1/3. 正在绘制高清科普卡片...")
        if draw_card(topic, image_path):
            print(f"   [成功] 卡片已保存到: {image_path}")
        else:
            print("   [失败] 绘制卡片失败。")
    else:
        print("1/3. ❌ [跳过] Pillow 库未安装，无法生成图片。请运行: pip install pillow")
        
    # 2. Generate MP3 Speech
    if tts_ok:
        print("2/3. 正在生成高音质教师配音...")
        if generate_audio(topic, audio_path):
            print(f"   [成功] 配音已保存到: {audio_path}")
        else:
            print("   [失败] 语音生成失败。")
    else:
        print("2/3. ❌ [跳过] edge-tts 工具未安装，无法生成音频。请运行: pip install edge-tts")
        
    # 3. Combine into MP4
    if pillow_ok and tts_ok and os.path.exists(image_path) and os.path.exists(audio_path):
        print("3/3. 正在合成为 30 秒垂直微课视频...")
        if combine_video(image_path, audio_path, video_path):
            print(f"\n🎉 恭喜！自动生成的视频文件已就绪: {video_path}")
        else:
            print("   [失败] FFmpeg 合成失败。")
    else:
        print("3/3. ❌ [跳过] 由于缺少图片/音频或 FFmpeg，无法生成 MP4 视频。")
        print("👉 请确保系统已安装: pip install pillow edge-tts 并在系统 Path 中配好 ffmpeg")

if __name__ == "__main__":
    main()
