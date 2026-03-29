# tools/storage.py

from tools.db import get_connection


# 🔹 SAVE NEWS (BATCH INSERT - FAST)
def save_news(news_list):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT IGNORE INTO news (title, url, category, content, status)
    VALUES (%s, %s, %s, %s, %s)
    """

    data = [
        (
            n.get("title"),
            n.get("url"),
            None,
            n.get("content", ""),
            "pending"
        )
        for n in news_list
    ]

    try:
        before_count = len(data)

        cursor.executemany(query, data)
        conn.commit()

        inserted_count = cursor.rowcount  # 🔥 key line
        skipped_count = before_count - inserted_count

        print("\n📊 INSERT REPORT")
        print(f"Total Attempted : {before_count}")
        print(f"Inserted        : {inserted_count}")
        print(f"Skipped         : {skipped_count}")

    except Exception as e:
        print("❌ Error saving news:", e)

    finally:
        cursor.close()
        conn.close()

# def save_news(news_list):
#     conn = get_connection()
#     cursor = conn.cursor()

#     query = """
#     INSERT IGNORE INTO news (title, url, category, content, status)
#     VALUES (%s, %s, %s, %s, %s)
#     """

#     data = [
#         (
#             n.get("title"),
#             n.get("url"),
#             None,          # no category yet
#             n.get("content", ""),
#             "pending"      # 🔥 mark pending
#         )
#         for n in news_list
#     ]

#     cursor.executemany(query, data)
#     conn.commit()

#     cursor.close()
#     conn.close()

# def save_news(news_list):
#     if not news_list:
#         return

#     conn = get_connection()
#     cursor = conn.cursor()

#     query = """
#     INSERT IGNORE INTO news (title, url, category, content)
#     VALUES (%s, %s, %s, %s)
#     """

#     data = [
#         (
#             n.get("title"),
#             n.get("url"),
#             n.get("category"),
#             n.get("content", "")
#         )
#         for n in news_list
#     ]

#     try:
#         cursor.executemany(query, data)  # 🔥 MUCH FASTER
#         conn.commit()
#     except Exception as e:
#         print("❌ Error saving news:", e)
#     finally:
#         cursor.close()
#         conn.close()


# 🔹 GET ALL NEWS (PAGINATED)
def get_all_news(limit=20, offset=0):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT * FROM news
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """, (limit, offset))

        data = cursor.fetchall()
        return data

    finally:
        cursor.close()
        conn.close()


# 🔹 GET BY CATEGORY (FAST + PAGINATION)
def get_news_by_category(category, limit=20, offset=0):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT * FROM news
            WHERE category=%s
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """, (category, limit, offset))

        data = cursor.fetchall()
        return data

    finally:
        cursor.close()
        conn.close()


# 🔹 FULL-TEXT SEARCH (VERY FAST 🔥)
def search_news(keyword, limit=20):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT * FROM news
            WHERE MATCH(title, content)
            AGAINST(%s IN NATURAL LANGUAGE MODE)
            LIMIT %s
        """, (keyword, limit))

        data = cursor.fetchall()
        return data

    finally:
        cursor.close()
        conn.close()