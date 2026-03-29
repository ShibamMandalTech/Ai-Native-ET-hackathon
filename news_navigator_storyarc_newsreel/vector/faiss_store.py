import faiss
import numpy as np
import pickle
import os

INDEX_FILE = "faiss_index.bin"
META_FILE = "metadata.pkl"

dimension = 384

# Initialize
try:
    if os.path.exists(INDEX_FILE) and os.path.exists(META_FILE):
        index = faiss.read_index(INDEX_FILE)

        with open(META_FILE, "rb") as f:
            metadata = pickle.load(f)

        print("✅ FAISS loaded from disk")

    else:
        index = faiss.IndexFlatL2(dimension)
        metadata = []
        print("⚠️ New FAISS index created")
        
except (EOFError, pickle.UnpicklingError):
    print("⚠️ metadata.pkl is corrupted or empty. Creating new FAISS index to recover.")
    index = faiss.IndexFlatL2(dimension)
    metadata = []
    
    # try:
    #     from db.db import get_connection
    #     conn = get_connection()
    #     if conn:
    #         cursor = conn.cursor()
    #         cursor.execute("UPDATE news SET embedded = 0;")
    #         conn.commit()
    #         cursor.close()
    #         conn.close()
    #         print("🔄 Successfully triggered a full database re-embedding (set embedded = 0)!")
    # except Exception as e:
    #     print("⚠️ Auto-reset of database failed:", e)


def add_vector(vec, meta):
    """
    Inputs a numerical vector representing text (a semantic embedding) 
    and its associated origin data (metadata dictionary) into the live memory FAISS engine.
    """
    index.add(np.array([vec]).astype("float32"))
    metadata.append(meta)


def save_index():
    """
    Writes the currently populated FAISS index and the corresponding physical 
    Metadata array securely out to permanent local disk storage files. 
    This prevents data loss if the server restarts.
    """
    faiss.write_index(index, INDEX_FILE)

    with open(META_FILE, "wb") as f:
        pickle.dump(metadata, f)

    print("💾 FAISS saved to disk")


def search(query_vec, top_k=5, cluster_id=None):
    """
    Performs an ultra-fast nearest-neighbor similarity search.
    It takes an embedded concept (query_vec), compares it against all known vectors 
    in the database, and returns the 'top_k' most mathematically similar news clips.
    If 'cluster_id' is provided, it specifically filters to only return news from that exact topic grouping.
    """
    # Look for slightly more results than requested (top_k * 2) so we can filter later without falling short
    D, I = index.search(np.array([query_vec]).astype("float32"), top_k * 2)

    results = []

    for idx in I[0]:
        if idx == -1: # Invalid search return
            continue
        if idx >= len(metadata): # Precaution for corrupted or desynced database arrays
            continue

        meta = metadata[idx]

        # 🔥 Cluster filtering (Optional targeted search)
        if cluster_id is not None:
            if meta.get("cluster_id") != cluster_id:
                continue

        results.append(meta)

        # Break out early once we hit our precise limit
        if len(results) >= top_k:
            break

    return results




