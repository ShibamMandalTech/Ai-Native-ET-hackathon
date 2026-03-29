import time
from tools.db import get_connection
from agents.classifier_agent import ClassifierAgent

classifier = ClassifierAgent()


def fetch_pending(limit=50):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM news
        WHERE status='pending'
        LIMIT %s
    """, (limit,))

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


def update_news(news_list):
    conn = get_connection()
    cursor = conn.cursor()

    for n in news_list:
        category = n.get("category")

        # ✅ FIX 1: handle list
        if isinstance(category, list):
            category = ",".join(category)

        # ✅ FIX 2: handle None / empty
        if not category:
            category = "general"

        # ✅ FIX 3: ensure string
        category = str(category)

        # ✅ FIX 4: safety limit (no truncation error)
        category = category[:250]

        category = str(category)[:250]

        cursor.execute("""
            UPDATE news
            SET category=%s, status='done'
            WHERE id=%s
        """, (category, n["id"]))   # ✅ FIX: use processed category

    conn.commit()
    cursor.close()
    conn.close()


def run_worker():
    print("🚀 Worker started...")

    while True:
        batch = fetch_pending(20)

        if not batch:
            print("⏳ No pending news, waiting...")
        else:
            print(f"🧠 Classifying {len(batch)} articles...")
            classified = classifier.run(batch)
            update_news(classified)
            print("✅ Batch done\n")

        # ⏱️ Wait 40 minutes
        time.sleep(20*60)


if __name__ == "__main__":
    run_worker()

# from tools.db import get_connection
# from agents.classifier_agent import ClassifierAgent

# classifier = ClassifierAgent()


# def fetch_pending(limit=50):
#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True)

#     cursor.execute("""
#         SELECT * FROM news
#         WHERE status='pending'
#         LIMIT %s
#     """, (limit,))

#     data = cursor.fetchall()

#     cursor.close()
#     conn.close()

#     return data


# def update_news(news_list):
#     conn = get_connection()
#     cursor = conn.cursor()

#     for n in news_list:
#         category = n.get("category")

#         # ✅ FIX 1: handle list
#         if isinstance(category, list):
#             category = ",".join(category)

#         # ✅ FIX 2: handle None / empty
#         if not category:
#             category = "general"

#         # ✅ FIX 3: ensure string
#         category = str(category)

#         # ✅ FIX 4: safety limit (no truncation error)
#         category = category[:250]
        
#         cursor.execute("""
#             UPDATE news
#             SET category=%s, status='done'
#             WHERE id=%s
#         """, (n["category"], n["id"]))

#     conn.commit()
#     cursor.close()
#     conn.close()


# def run_worker():
#     print("🚀 Worker started...")

#     while True:
#         batch = fetch_pending(20)

#         if not batch:
#             print("✅ No pending news")
#             break

#         print(f"🧠 Classifying {len(batch)} articles...")

#         classified = classifier.run(batch)

#         update_news(classified)

#         print("✅ Batch done\n")


# if __name__ == "__main__":
#     run_worker()