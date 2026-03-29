import time
from services.video_pipeline import run_pipeline
from db.db import get_connection

while True:
    print("Running pipeline...")
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Run pipeline with default user_id=1 and user_type="General Audience"
        run_pipeline(cursor, conn, user_id=1, user_type="General Audience")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error running pipeline: {e}")
        
    time.sleep(1800)