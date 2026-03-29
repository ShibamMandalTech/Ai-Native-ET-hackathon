from db.connection import get_connection


# def get_next_news():
#     conn = get_connection()
#     if not conn:
#         return None

#     cursor = conn.cursor(dictionary=True)

#     cursor.execute("""
#         SELECT * FROM news
#         WHERE status != 'complete'
#         ORDER BY retries ASC, created_at ASC
#         LIMIT 1
#     """)

#     row = cursor.fetchone()

#     cursor.close()
#     conn.close()

#     return row

# for batch + decision agent get_next_news replaced with get_batch

def get_batch(limit=20):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM news
        WHERE status != 'complete'
        ORDER BY 
            (content IS NULL) DESC,
            (deep_content IS NULL) DESC,
            retries ASC,
            created_at ASC
        LIMIT %s
    """, (limit,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


def update_field(news_id, field, value):
    conn = get_connection()
    cursor = conn.cursor()

    query = f"UPDATE news SET {field} = %s WHERE id = %s"
    cursor.execute(query, (value, news_id))

    conn.commit()
    cursor.close()
    conn.close()


def mark_complete(news_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE news
        SET status = 'complete',
            processing_stage = 'complete'
        WHERE id = %s
    """, (news_id,))

    conn.commit()
    cursor.close()
    conn.close()


def increment_retry(news_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE news
        SET retries = retries + 1
        WHERE id = %s
    """, (news_id,))

    conn.commit()
    cursor.close()
    conn.close()


def mark_failed(news_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE news
        SET processing_stage = 'failed'
        WHERE id = %s
    """, (news_id,))

    conn.commit()
    cursor.close()
    conn.close()



def get_rows_by_ids(ids):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    format_strings = ','.join(['%s'] * len(ids))

    cursor.execute(f"""
        SELECT * FROM news
        WHERE id IN ({format_strings})
    """, tuple(ids))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows