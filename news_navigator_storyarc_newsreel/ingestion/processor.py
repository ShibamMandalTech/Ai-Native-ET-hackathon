from db.db import get_connection
from ingestion.chunker import chunk_text
from ingestion.embedder import get_embedding
from vector.faiss_store import add_vector, save_index
from services.cluster_service import assign_cluster, merge_similar_clusters


# from services.cluster_service import assign_cluster, merge_similar_clusters

def process_news():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # cursor.execute("SELECT id, content, title, url FROM news")

    cursor.execute("""
SELECT id, content, deep_content, summary_points, title, url FROM news where embedded=0""")


    # print("updated")

    rows = cursor.fetchall()

    for row in rows:
        content = row.get("deep_content") or row.get("content")
        summary = row.get("summary_points")

        if not content and not summary:
            continue

        #  assign cluster automatically
        # cluster_id = assign_cluster(row.get("title", content[:100]))

        cluster_text = (row.get("title", "") + " " + (content[:500] if content else ""))

        cluster_id = assign_cluster(cluster_text)

        cursor.execute("""UPDATE news SET cluster_id = %s WHERE id = %s""", (cluster_id, row["id"]))
        print("Cluster assigned:", cluster_id)



        # chunks = chunk_text(content)
        chunks = []

        #  1. summary_points → highest priority
        if summary:
            # for point in summary.split("\n"):
            #     if point.strip():
            #         chunks.append(point.strip())

            # summary chunks
            for point in summary.split("\n"):
                if point.strip():
                    chunks.append((point.strip(), "summary"))



        #  2. deep content → detailed
        if content:
            for ch in chunk_text(content):
                chunks.append((ch, "deep"))

        for chunk , chunk_type in chunks:
            vec = get_embedding(chunk)

            add_vector(vec, {
                "news_id": row["id"],
                "cluster_id": cluster_id,
                "text": chunk,
                "type": chunk_type,
                "source": "Economic Times",
                "url": row.get("url"),
                "title": row.get("title")
            })

        cursor.execute("""UPDATE news SET embedded = 1 WHERE id = %s""", (row["id"],))
                
        # for chunk in chunks:
        #     vec = get_embedding(chunk)

        #     add_vector(vec, {
        #         "news_id": row["id"],
        #         "cluster_id": cluster_id,
        #         "text": chunk
        #     })
        # print("Cluster assigned:", cluster_id)

    conn.commit()

    save_index()

    merge_similar_clusters()

    cursor.close()
    conn.close()




