def log_engagement(cursor, user_id, news_id, watch_time, liked, category):
    cursor.execute("""
        INSERT INTO engagement (user_id, news_id, watch_time, liked, category)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, news_id, watch_time, liked, category))