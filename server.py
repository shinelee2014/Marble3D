import http.server
import socketserver
import json
import os
import urllib.parse
import sys
import sqlite3
import shutil
import threading
import datetime

# Reconfigure console output for Windows terminal UTF-8
if sys.stdout is not None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PORT = 8000
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
PROFILES_DB_PATH = os.path.join(DATA_DIR, "profiles_db.json")
MASTERY_DB_PATH = os.path.join(DATA_DIR, "mastery_db.json")

def get_db_connection():
    db_path = os.path.join(DATA_DIR, "taxonomy.db")
    conn = sqlite3.connect(db_path, timeout=30.0)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def migrate_legacy_data(conn):
    print("Migrating legacy JSON data to SQLite...")
    try:
        with open(PROFILES_DB_PATH, "r", encoding="utf-8") as f:
            profiles = json.load(f)
        with open(MASTERY_DB_PATH, "r", encoding="utf-8") as f:
            mastery = json.load(f)
            
        cursor = conn.cursor()
        
        # Start transaction
        conn.execute("BEGIN TRANSACTION;")
        
        for p in profiles:
            p_id = p.get("id")
            p_name = p.get("name")
            p_grade = p.get("grade", 1)
            cursor.execute("INSERT OR REPLACE INTO profiles (id, name, grade) VALUES (?, ?, ?)", (p_id, p_name, p_grade))
            
        active_profile_id = mastery.get("active_profile_id", "child_1")
        cursor.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", ("active_profile_id", active_profile_id))
        
        progress = mastery.get("progress", {})
        for profile_id, topics in progress.items():
            for topic_id, status in topics.items():
                cursor.execute("INSERT OR REPLACE INTO mastery (profile_id, topic_id, status) VALUES (?, ?, ?)", (profile_id, topic_id, status))
                
        conn.commit()
        print("Legacy JSON data migration successful.")
        
        # Rename to .bak
        try:
            bak_profiles = PROFILES_DB_PATH + ".bak"
            if os.path.exists(bak_profiles):
                os.remove(bak_profiles)
            os.rename(PROFILES_DB_PATH, bak_profiles)
            
            bak_mastery = MASTERY_DB_PATH + ".bak"
            if os.path.exists(bak_mastery):
                os.remove(bak_mastery)
            os.rename(MASTERY_DB_PATH, bak_mastery)
            print("Renamed legacy database files to .bak")
        except Exception as e:
            print(f"Error backing up legacy files: {e}")
            
    except Exception as e:
        conn.rollback()
        print(f"Failed to migrate legacy JSON data: {e}")

def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    conn = get_db_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                grade INTEGER NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS mastery (
                profile_id TEXT,
                topic_id TEXT,
                status TEXT NOT NULL,
                PRIMARY KEY (profile_id, topic_id),
                FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS translations (
                original_text TEXT PRIMARY KEY,
                translated_text TEXT NOT NULL
            )
        """)
        conn.commit()
        
        # Check if empty, prepopulate defaults if no legacy files
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM profiles")
        count = cursor.fetchone()[0]
        
        legacy_profiles_exists = os.path.exists(PROFILES_DB_PATH)
        legacy_mastery_exists = os.path.exists(MASTERY_DB_PATH)
        
        if count == 0 and not legacy_profiles_exists and not legacy_mastery_exists:
            conn.execute("INSERT INTO profiles (id, name, grade) VALUES (?, ?, ?)", ("child_1", "大宝", 2))
            conn.execute("INSERT INTO profiles (id, name, grade) VALUES (?, ?, ?)", ("child_2", "二宝", 1))
            conn.execute("INSERT INTO config (key, value) VALUES (?, ?)", ("active_profile_id", "child_1"))
            conn.commit()
            
        if legacy_profiles_exists and legacy_mastery_exists:
            migrate_legacy_data(conn)
            
    finally:
        conn.close()

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Disable caching for API responses and development
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query = urllib.parse.parse_qs(parsed_url.query)

        # Redirect root to explorer.html
        if path == "/":
            self.path = "/explorer.html"
            return super().do_GET()

        # API: Get Profiles
        if path == "/api/profiles":
            conn = get_db_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, grade FROM profiles")
                profiles = [{"id": r["id"], "name": r["name"], "grade": r["grade"]} for r in cursor.fetchall()]
                
                cursor.execute("SELECT value FROM config WHERE key = ?", ("active_profile_id",))
                row = cursor.fetchone()
                active_id = row["value"] if row else "child_1"
                
                response = {
                    "profiles": profiles,
                    "activeProfileId": active_id
                }
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_error(500, f"Database error: {e}")
            finally:
                conn.close()
            return

        # API: Get Mastery Progress for a profile
        if path == "/api/mastery":
            profile_id = query.get("profileId", [None])[0]
            if not profile_id:
                self.send_error(400, "Missing profileId")
                return

            conn = get_db_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT topic_id, status FROM mastery WHERE profile_id = ?", (profile_id,))
                progress = {r["topic_id"]: r["status"] for r in cursor.fetchall()}
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(progress, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_error(500, f"Database error: {e}")
            finally:
                conn.close()
            return

        # Fallback to serving static files
        return super().do_GET()

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        # Read POST body
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            req_data = json.loads(post_data.decode('utf-8')) if content_length > 0 else {}
        except Exception:
            self.send_error(400, "Invalid JSON body")
            return

        # API: Add Profile
        if path == "/api/profiles":
            name = req_data.get("name")
            if not name or name.strip() == "":
                self.send_error(400, "Missing child name")
                return

            new_id = f"profile_{int(time_time_ms())}"
            grade = req_data.get("grade", 1)
            
            conn = get_db_connection()
            try:
                # Use a transaction for atomic update
                conn.execute("BEGIN TRANSACTION;")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO profiles (id, name, grade) VALUES (?, ?, ?)", 
                               (new_id, name.strip(), int(grade) if grade else 1))
                cursor.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", 
                               ("active_profile_id", new_id))
                conn.commit()
                
                response = {
                    "id": new_id, 
                    "name": name.strip(),
                    "grade": int(grade) if grade else 1
                }
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                conn.rollback()
                self.send_error(500, f"Database error: {e}")
            finally:
                conn.close()
            return

        # API: Save Mastery Progress
        if path == "/api/mastery":
            profile_id = req_data.get("profileId")
            mastery_state = req_data.get("mastery") # dict of topicId -> state
            
            if not profile_id:
                self.send_error(400, "Missing profileId")
                return

            conn = get_db_connection()
            try:
                conn.execute("BEGIN TRANSACTION;")
                cursor = conn.cursor()
                
                # Check if profile exists
                cursor.execute("SELECT id FROM profiles WHERE id = ?", (profile_id,))
                if not cursor.fetchone():
                    # If the profile doesn't exist, we raise IntegrityError or return 400
                    raise sqlite3.IntegrityError("Profile does not exist")
                
                cursor.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", 
                               ("active_profile_id", profile_id))
                
                # Clear and rewrite mastery
                cursor.execute("DELETE FROM mastery WHERE profile_id = ?", (profile_id,))
                if mastery_state:
                    for topic_id, status in mastery_state.items():
                        cursor.execute("INSERT INTO mastery (profile_id, topic_id, status) VALUES (?, ?, ?)", 
                                       (profile_id, topic_id, status))
                conn.commit()
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}, ensure_ascii=False).encode("utf-8"))
            except sqlite3.IntegrityError as e:
                conn.rollback()
                self.send_error(400, f"Integrity error: {e}")
            except Exception as e:
                conn.rollback()
                self.send_error(500, f"Database error: {e}")
            finally:
                conn.close()
            return

        # API: Switch active profile
        if path == "/api/profiles/switch":
            profile_id = req_data.get("profileId")
            if not profile_id:
                self.send_error(400, "Missing profileId")
                return
                
            conn = get_db_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", 
                               ("active_profile_id", profile_id))
                conn.commit()
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_error(500, f"Database error: {e}")
            finally:
                conn.close()
            return

        # API: Delete Profile
        if path == "/api/profiles/delete":
            profile_id = req_data.get("profileId")
            if not profile_id:
                self.send_error(400, "Missing profileId")
                return

            conn = get_db_connection()
            try:
                cursor = conn.cursor()
                
                # Fetch profiles
                cursor.execute("SELECT id FROM profiles")
                profiles = [r["id"] for r in cursor.fetchall()]
                
                if len(profiles) <= 1:
                    self.send_error(400, "Cannot delete last profile")
                    return

                # Get active profile ID
                cursor.execute("SELECT value FROM config WHERE key = ?", ("active_profile_id",))
                active_row = cursor.fetchone()
                active_id = active_row["value"] if active_row else None

                conn.execute("BEGIN TRANSACTION;")
                
                # Delete profile (mastery deletes automatically due to foreign key with cascade)
                cursor.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
                
                if active_id == profile_id:
                    remaining = [p for p in profiles if p != profile_id]
                    if remaining:
                        cursor.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", 
                                       ("active_profile_id", remaining[0]))
                
                conn.commit()
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                conn.rollback()
                self.send_error(500, f"Database error: {e}")
            finally:
                conn.close()
            return

        # API: Manual backup trigger
        if path == "/api/backup":
            filename = do_backup()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            result = {"status": "success", "file": filename} if filename else {"status": "error"}
            self.wfile.write(json.dumps(result).encode("utf-8"))
            return

        # API: Generate AI questions (LM Studio proxy)
        if path == "/api/generate-questions":
            topic_name = req_data.get("topicName", "")
            subject = req_data.get("subject", "")
            profile_name = req_data.get("profileName", "孩子")
            grade = req_data.get("grade", 2)
            extra_context = req_data.get("extraContext", "")   # 真题参考上下文
            style_hint = req_data.get("styleHint", "")         # 风格提示（如"小升初考试风格"）

            # If there's a style hint (real-exam imitation mode), build a focused prompt
            if style_hint or extra_context:
                prompt = (
                    f"你是一位专业的中国小学{subject}教师，擅长出小升初/分班考真题风格的题目。\n"
                    f"请为{grade}年级学生{profile_name}出1道关于【{topic_name}】的题目。\n"
                    f"{style_hint}\n"
                    f"要求：\n"
                    f"1. 严格仿照小升初/分班考考试风格，题目有一定思维深度。\n"
                    f"2. 严禁使用任何 LaTeX 语法或美元符号，数学公式直接写成普通文本。\n"
                    f"3. 输出格式为 Markdown：包含题干、解题步骤和标准答案。\n"
                    f"{extra_context}\n\n"
                    f"请输出以下格式（只输出题目，不要其他多余说明）：\n\n"
                    f"### 🎯 仿真练习题：【题目名称】\n"
                    f"【题干】题目内容...\n"
                    f"【✍️ 解题步骤】\n"
                    f"1. ...\n"
                    f"【✅ 标准答案】...\n"
                    f"【💡 考点提示】...\n"
                )
            else:
                prompt = (
                    f"# 🍎 苏州小课堂·{subject}精讲\n\n"
                    f"你是苏州小学一位经验丰富的{subject}老师。请为{grade}年级的学生{profile_name}出3道关于【{topic_name}】的趣味练习题。\n"
                    f"要求：\n"
                    f"1. 贴近苏教版{grade}年级教材，内容生动有趣，难度适中。\n"
                    f"2. 严禁使用任何 LaTeX 语法或美元符号（如不要写 $x$，$y$），数学公式和变量一律直接写成普通文本，例如直接写 x、y、z 或 x + 8 = 25，确保不要出现任何 $ 符号。\n"
                    f"3. 对于数学中的代数/方程题目，未知数（变量）仅使用小学生最常用的 x、y、z（优先使用 x），不要使用 m、n 等非常用字母。\n\n"
                    f"请严格按照以下格式和排版输出 markdown，不要包裹 JSON 代码块，也不要输出任何多余的文字：\n\n"
                    f"## ✨ 教学目标设定\n"
                    f"1. 知识目标：学生能够...\n"
                    f"2. 能力目标：学生能够...\n"
                    f"3. 情感态度目标：培养学生...\n\n"
                    f"## 📝 趣味课后练习题（共3题）\n\n"
                    f"### 第 1 题：【写一个趣味题名】情境应用题（基础型/进阶型/挑战型）\n"
                    f"【题干】这里写详细的题目描述...\n"
                    f"【✍️ 解题步骤】\n"
                    f"1. 设未知数：...\n"
                    f"2. 列方程：...\n"
                    f"3. 解方程：...\n"
                    f"【✅ 参考答案】这里写答案内容...\n"
                    f"【💡 思考提示】给家长的讲解辅导要点/思考提示...\n\n"
                    f"### 第 2 题：...\n"
                )
            text, err = call_lm_studio(prompt)
            if err:
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": err, "fallback": True}, ensure_ascii=False).encode("utf-8"))
                return

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"markdown": text}, ensure_ascii=False).encode("utf-8"))
            return

        # API: Translate text
        if path == "/api/translate":
            texts = req_data.get("texts", [])
            results = {}
            if not texts:
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"translations": results}, ensure_ascii=False).encode("utf-8"))
                return

            conn = get_db_connection()
            try:
                cursor = conn.cursor()
                for t in texts:
                    t = t.strip()
                    if not t:
                        continue
                    # Check cache first
                    cursor.execute("SELECT translated_text FROM translations WHERE original_text = ?", (t,))
                    row = cursor.fetchone()
                    if row:
                        results[t] = row["translated_text"]
                    else:
                        # Call LM Studio to translate
                        translated = translate_text(t)
                        if translated and translated != t:
                            # Save to cache
                            try:
                                conn.execute("INSERT OR REPLACE INTO translations (original_text, translated_text) VALUES (?, ?)", (t, translated))
                                conn.commit()
                            except Exception:
                                pass
                            results[t] = translated
                        else:
                            results[t] = t
            except Exception as e:
                print("Translation error:", e)
            finally:
                conn.close()

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"translations": results}, ensure_ascii=False).encode("utf-8"))
            return

        self.send_error(404, "API Endpoint Not Found")

def time_time_ms():
    import time
    return int(time.time() * 1000)

# ─── Auto-Backup (F3) ────────────────────────────────────────────
BACKUP_DIR = os.path.join(DATA_DIR, "backups")
BACKUP_KEEP_DAYS = 30

def do_backup():
    """Copy taxonomy.db to data/backups/taxonomy_YYYYMMDD_HHMMSS.db"""
    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        db_path = os.path.join(DATA_DIR, "taxonomy.db")
        if not os.path.exists(db_path):
            print("[Backup] taxonomy.db not found, skipping.")
            return None
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = os.path.join(BACKUP_DIR, f"taxonomy_{ts}.db")
        shutil.copy2(db_path, dest)
        print(f"[Backup] Saved: {dest}")
        # Prune old backups older than BACKUP_KEEP_DAYS
        cutoff = datetime.datetime.now() - datetime.timedelta(days=BACKUP_KEEP_DAYS)
        for f in os.listdir(BACKUP_DIR):
            fpath = os.path.join(BACKUP_DIR, f)
            if os.path.isfile(fpath):
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(fpath))
                if mtime < cutoff:
                    os.remove(fpath)
                    print(f"[Backup] Pruned old backup: {f}")
        return os.path.basename(dest)
    except Exception as e:
        print(f"[Backup] Error: {e}")
        return None

def schedule_backup():
    """Schedule the next backup at 03:00 local time."""
    now = datetime.datetime.now()
    next_run = now.replace(hour=3, minute=0, second=0, microsecond=0)
    if next_run <= now:
        next_run += datetime.timedelta(days=1)
    delay = (next_run - now).total_seconds()
    print(f"[Backup] Next auto-backup in {delay/3600:.1f} hours ({next_run.strftime('%Y-%m-%d %H:%M')})")
    def run():
        do_backup()
        schedule_backup()  # reschedule for tomorrow
    t = threading.Timer(delay, run)
    t.daemon = True
    t.start()

def translate_text(text):
    """Call LM Studio to translate educational English text to kid-friendly Chinese."""
    import socket
    import urllib.request as urlreq
    
    # Fast TCP probe (0.5s)
    try:
        with socket.create_connection(("127.0.0.1", 1234), timeout=0.5):
            pass
    except Exception:
        return text

    prompt = (
        f"请把以下教育大纲中的英文短句翻译为地道、简练的小学中文，要求贴合中国小学的教学场景，并且翻译结果中不要带有任何美元符号或者 LaTeX 包裹。"
        f"只输出翻译后的中文，不要有任何多余的解释、标点或修饰。\n\n"
        f"英文短句：\"{text}\""
    )
    
    payload = json.dumps({
        "model": "local-model",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 100
    }).encode("utf-8")
    
    req = urlreq.Request(
        "http://127.0.0.1:1234/v1/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urlreq.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            translated = data["choices"][0]["message"]["content"].strip()
            translated = translated.replace('"', '').replace('“', '').replace('”', '')
            return translated
    except Exception as e:
        import sys
        print(f"Translation failed for '{text}': {e}", file=sys.stderr)
        return text


# ─── LM Studio AI Question Proxy (F4) ─────────────────────────────
LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"

def call_lm_studio(prompt_text):
    """Call LM Studio (OpenAI-compatible API) and return text response."""
    import socket
    import urllib.request as urlreq

    # Fast TCP probe: check if port 1234 is actually open (0.5s timeout)
    try:
        with socket.create_connection(("127.0.0.1", 1234), timeout=0.5):
            pass
    except Exception:
        return None, "LM Studio 未启动（端口 1234 未监听）"

    payload = json.dumps({
        "model": "local-model",
        "messages": [{"role": "user", "content": prompt_text}],
        "temperature": 0.7,
        "max_tokens": 1200
    }).encode("utf-8")
    req = urlreq.Request(
        LM_STUDIO_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urlreq.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"], None
    except Exception as e:
        return None, str(e)


if __name__ == "__main__":
    # Change working directory to file directory to correctly resolve relative paths
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Initialize SQLite database and perform migration if needed
    init_db()
    
    # Start daily auto-backup scheduler
    schedule_backup()
    
    # Allow address reuse to prevent "address already in use" on restarts
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("", PORT), CustomHandler) as httpd:
        print(f"==================================================")
        print(f"🏠 Marble NAS-Ready Local Server (SQLite Mode) is running!")
        print(f"🌐 Access URL: http://localhost:{PORT}")
        print(f"📂 Persistent DB saved in data/taxonomy.db")
        print(f"==================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.shutdown()
