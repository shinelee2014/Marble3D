import http.server
import socketserver
import json
import os
import urllib.parse

# Reconfigure console output for Windows terminal UTF-8
import sys
if sys.stdout is not None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PORT = 8000
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
PROFILES_DB_PATH = os.path.join(DATA_DIR, "profiles_db.json")
MASTERY_DB_PATH = os.path.join(DATA_DIR, "mastery_db.json")

# Ensure database files exist
if not os.path.exists(PROFILES_DB_PATH):
    with open(PROFILES_DB_PATH, "w", encoding="utf-8") as f:
        json.dump([
            {"id": "child_1", "name": "大宝"},
            {"id": "child_2", "name": "二宝"}
        ], f, indent=2, ensure_ascii=False)

if not os.path.exists(MASTERY_DB_PATH):
    with open(MASTERY_DB_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "active_profile_id": "child_1",
            "progress": {}
        }, f, indent=2, ensure_ascii=False)

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
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            with open(PROFILES_DB_PATH, "r", encoding="utf-8") as f:
                profiles_data = json.load(f)
            with open(MASTERY_DB_PATH, "r", encoding="utf-8") as f:
                mastery_data = json.load(f)
            
            response = {
                "profiles": profiles_data,
                "activeProfileId": mastery_data.get("active_profile_id", "child_1")
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode("utf-8"))
            return

        # API: Get Mastery Progress for a profile
        if path == "/api/mastery":
            profile_id = query.get("profileId", [None])[0]
            if not profile_id:
                self.send_error(400, "Missing profileId")
                return

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            
            with open(MASTERY_DB_PATH, "r", encoding="utf-8") as f:
                mastery_data = json.load(f)
            
            # Read progress of profile_id, default to empty dict
            progress = mastery_data.get("progress", {}).get(profile_id, {})
            self.wfile.write(json.dumps(progress, ensure_ascii=False).encode("utf-8"))
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
            
            # Read and append to profiles
            with open(PROFILES_DB_PATH, "r", encoding="utf-8") as f:
                profiles = json.load(f)
            
            profiles.append({
                "id": new_id, 
                "name": name.strip(),
                "grade": int(grade) if grade else 1
            })
            with open(PROFILES_DB_PATH, "w", encoding="utf-8") as f:
                json.dump(profiles, f, indent=2, ensure_ascii=False)
                
            # Set active in mastery
            with open(MASTERY_DB_PATH, "r", encoding="utf-8") as f:
                mastery = json.load(f)
            mastery["active_profile_id"] = new_id
            if "progress" not in mastery:
                mastery["progress"] = {}
            mastery["progress"][new_id] = {}
            with open(MASTERY_DB_PATH, "w", encoding="utf-8") as f:
                json.dump(mastery, f, indent=2, ensure_ascii=False)

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"id": new_id, "name": name.strip(), "grade": int(grade) if grade else 1}, ensure_ascii=False).encode("utf-8"))
            return

        # API: Save Mastery Progress
        if path == "/api/mastery":
            profile_id = req_data.get("profileId")
            mastery_state = req_data.get("mastery") # dict of topicId -> state
            
            if not profile_id:
                self.send_error(400, "Missing profileId")
                return

            # Read and update mastery
            with open(MASTERY_DB_PATH, "r", encoding="utf-8") as f:
                mastery = json.load(f)
                
            mastery["active_profile_id"] = profile_id
            if "progress" not in mastery:
                mastery["progress"] = {}
            mastery["progress"][profile_id] = mastery_state or {}
            
            with open(MASTERY_DB_PATH, "w", encoding="utf-8") as f:
                json.dump(mastery, f, indent=2, ensure_ascii=False)

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}, ensure_ascii=False).encode("utf-8"))
            return

        # API: Switch active profile
        if path == "/api/profiles/switch":
            profile_id = req_data.get("profileId")
            if not profile_id:
                self.send_error(400, "Missing profileId")
                return
                
            with open(MASTERY_DB_PATH, "r", encoding="utf-8") as f:
                mastery = json.load(f)
            mastery["active_profile_id"] = profile_id
            with open(MASTERY_DB_PATH, "w", encoding="utf-8") as f:
                json.dump(mastery, f, indent=2, ensure_ascii=False)
                
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}, ensure_ascii=False).encode("utf-8"))
            return

        # API: Delete Profile
        if path == "/api/profiles/delete":
            profile_id = req_data.get("profileId")
            if not profile_id:
                self.send_error(400, "Missing profileId")
                return

            with open(PROFILES_DB_PATH, "r", encoding="utf-8") as f:
                profiles = json.load(f)
                
            if len(profiles) <= 1:
                self.send_error(400, "Cannot delete last profile")
                return

            # Remove from list
            profiles = [p for p in profiles if p["id"] != profile_id]
            with open(PROFILES_DB_PATH, "w", encoding="utf-8") as f:
                json.dump(profiles, f, indent=2, ensure_ascii=False)

            # Update mastery
            with open(MASTERY_DB_PATH, "r", encoding="utf-8") as f:
                mastery = json.load(f)
            
            # Remove progress
            if "progress" in mastery and profile_id in mastery["progress"]:
                del mastery["progress"][profile_id]
                
            # If deleted was active, switch to first remaining
            if mastery.get("active_profile_id") == profile_id:
                mastery["active_profile_id"] = profiles[0]["id"]
                
            with open(MASTERY_DB_PATH, "w", encoding="utf-8") as f:
                json.dump(mastery, f, indent=2, ensure_ascii=False)

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}, ensure_ascii=False).encode("utf-8"))
            return

        self.send_error(404, "API Endpoint Not Found")

def time_time_ms():
    import time
    return int(time.time() * 1000)

if __name__ == "__main__":
    # Change working directory to file directory to correctly resolve relative paths
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Allow address reuse to prevent "address already in use" on restarts
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"==================================================")
        print(f"🏠 Marble NAS-Ready Local Server is running!")
        print(f"🌐 Access URL: http://localhost:{PORT}")
        print(f"📂 Persistent DBs saved in data/ folder")
        print(f"==================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.shutdown()
