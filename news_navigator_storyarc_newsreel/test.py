from db.db import get_connection

conn = get_connection()
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT id, title, video_status, video_path FROM news WHERE video_status='VIDEO_CREATED'")
rows = cursor.fetchall()

print(f"Total videos: {len(rows)}")
for r in rows:
    print(r['id'], r['video_path'])

cursor.close()
conn.close()
