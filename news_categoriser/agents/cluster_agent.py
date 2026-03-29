from db.connection import get_connection

def assign_cluster(short_text):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, content, cluster_id FROM news
        WHERE content IS NOT NULL AND cluster_id IS NOT NULL
    """)

    rows = cursor.fetchall()

    for row in rows:
        if row["content"] and short_text[:50] in row["content"]:
            return row["cluster_id"]

    cursor.execute("SELECT MAX(cluster_id) as max_id FROM news")
    max_id = cursor.fetchone()["max_id"] or 0

    return max_id + 1