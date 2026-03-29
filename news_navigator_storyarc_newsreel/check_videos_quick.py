from db.db import get_connection
import os

app_root = r"E:\ET Ai Hackathon - Copy\news_navigator"

conn = get_connection()
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT id, title, video_path, video_status FROM news WHERE video_status='VIDEO_CREATED' AND video_path IS NOT NULL ORDER BY id DESC LIMIT 10")
rows = cursor.fetchall()
print(f"Root path: {app_root}")
print("---")
for r in rows:
    path = r.get("video_path")
    full_path = os.path.join(app_root, path) if path else "None"
    exists = os.path.exists(full_path) if path else False
    print(f"ID: {r['id']} | DB: {path} | Exists: {exists} | Full: {full_path}")

cursor.close()
conn.close()
