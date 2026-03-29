import numpy as np
from db.db import get_connection
from ingestion.embedder import get_embedding

# THRESHOLD = 0.75  # similarity

# def cosine_sim(a, b):
#     return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def cosine_sim(a, b):
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def get_clusters():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM clusters")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def merge_clusters(main_id, duplicate_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Move news to main cluster
    cursor.execute("""
        UPDATE news SET cluster_id = %s WHERE cluster_id = %s
    """, (main_id, duplicate_id))

    # Delete duplicate cluster
    cursor.execute("""
        DELETE FROM clusters WHERE id = %s
    """, (duplicate_id,))

    conn.commit()
    cursor.close()
    conn.close()

def merge_similar_clusters():
    clusters = get_clusters()

    for i in range(len(clusters)):
        for j in range(i + 1, len(clusters)):

            if clusters[i]["id"] == clusters[j]["id"]:
                continue

            emb1 = np.frombuffer(clusters[i]["embedding"], dtype=np.float32)
            emb2 = np.frombuffer(clusters[j]["embedding"], dtype=np.float32)

            sim = cosine_sim(emb1, emb2)

            if sim > 0.95:
                print(f"Merging cluster {clusters[j]['id']} → {clusters[i]['id']}")
                merge_clusters(clusters[i]["id"], clusters[j]["id"])


def assign_cluster(text):
    emb = get_embedding(text)

    clusters = get_clusters()

    best_id = None
    best_score = -1

    for c in clusters:
        c_emb = np.frombuffer(c["embedding"], dtype=np.float32)

        score = cosine_sim(emb, c_emb)

        if score > best_score:
            best_score = score
            best_id = c["id"]

    # If similar → use cluster
    THRESHOLD = get_threshold(len(clusters))

    if best_score > THRESHOLD:
        print(f" Joining existing cluster {best_id} (Score: {best_score:.3f} > Threshold: {THRESHOLD})")
        return best_id

    if best_score > 0.5:
        print(f" Joining existing cluster {best_id} (Score: {best_score:.3f} > 0.5 Fallback Threshold)")
        return best_id

    print(f" Creating NEW cluster! (Best Score: {best_score:.3f} missed Threshold: {THRESHOLD}, Close to ID: {best_id})")

    #  Else create new cluster
    conn = get_connection()
    cursor = conn.cursor()

    name = generate_cluster_name(text)

    cursor.execute("""
        INSERT INTO clusters (name, embedding)
        VALUES (%s, %s)
    """, (
        # text[:100],  # simple name
        
        name,
        emb.tobytes()
            ))

    conn.commit()
    new_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return new_id


from llm.groq_client import call_groq
import time

def generate_cluster_name(text):
    prompt = f"""
    Generate a short 3-5 word topic name for this news:

    {text}

    Only return the topic name.
    """

    while True:
        try:
            return call_groq(prompt).strip()
        except Exception as e:
            if " All Groq API keys failed" in str(e):
                print(" All Groq API keys failed. Retrying in 10 minutes...")
                time.sleep(600)
            else:
                raise e


def get_threshold(num_clusters):
    return 0.58
    # if num_clusters < 10:
    #     return 0.58
    # elif num_clusters < 50:
    #     return 0.6
    # else:
    #     return 0.62

def detect_cluster_from_query(question):
    emb = get_embedding(question)

    clusters = get_clusters()

    best_id = None
    best_score = -1

    for c in clusters:
        c_emb = np.frombuffer(c["embedding"], dtype=np.float32)

        score = cosine_sim(emb, c_emb)

        if score > best_score:
            best_score = score
            best_id = c["id"]

    print(f" Query matched cluster {best_id} with score {best_score}")

    return best_id




#  NEW: MULTI-CLUSTER DETECTION
def detect_top_clusters(question, top_k=3, min_threshold=0.5):
    emb = get_embedding(question)

    clusters = get_clusters()

    scored = []

    for c in clusters:
        c_emb = np.frombuffer(c["embedding"], dtype=np.float32)
        score = cosine_sim(emb, c_emb)

        scored.append((score, c["id"]))

    #  sort by similarity
    scored.sort(reverse=True, key=lambda x: x[0])

    #  filter top clusters
    top_clusters = []

    for score, cid in scored[:top_k]:
        if score >= min_threshold:
            top_clusters.append((cid, score))

    print(f"🔍 Top clusters: {top_clusters}")

    return [cid for cid, _ in top_clusters]

