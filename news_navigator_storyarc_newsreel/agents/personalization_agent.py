def get_user_preferences(cursor, user_id):
    cursor.execute("""
        SELECT category, AVG(watch_time) as avg_watch
        FROM engagement
        WHERE user_id = %s
        GROUP BY category
        ORDER BY avg_watch DESC
        LIMIT 3
    """, (user_id,))

    rows = cursor.fetchall()
    return [row['category'] for row in rows]