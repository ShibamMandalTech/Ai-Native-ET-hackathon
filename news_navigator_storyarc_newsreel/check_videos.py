from app import app
from db.db import get_connection
import os

conn = get_connection()
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT id, title, video_path, video_status FROM news WHERE video_status='VIDEO_CREATED' AND video_path IS NOT NULL ORDER BY id DESC LIMIT 10")
rows = cursor.fetchall()
print(f"Root path: {app.root_path}")
print("---")
for r in rows:
    path = r.get("video_path")
    full_path = os.path.join(app.root_path, path) if path else "None"
    exists = os.path.exists(full_path) if path else False
    print(f"ID: {r['id']} | DB Path: {path} | Exists: {exists} | Full: {full_path}")
cursor.close()
conn.close()
