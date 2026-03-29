from db.db import get_connection
from services.video_pipeline import run_pipeline

conn = get_connection()
cursor = conn.cursor(dictionary=True)

try:
    print("Starting pipeline test...")
    run_pipeline(cursor, conn, user_id=1, user_type="General Audience")
    print("Pipeline finished successfully.")
except Exception as e:
    print(f"Pipeline crashed catastrophically: {e}")
finally:
    cursor.close()
    conn.close()
