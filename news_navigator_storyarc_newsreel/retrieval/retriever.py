from ingestion.embedder import get_embedding
from vector.faiss_store import search
from config import TOP_K

def rerank_with_priority(results):
        def score(item):
            base = 1
            if item.get("type") == "summary":
                base += 2   #  boost
            return base

        return sorted(results, key=score, reverse=True)

def retrieve_chunks(query, cluster_id=None):
    q_vec = get_embedding(query)
    results = search(q_vec, TOP_K, cluster_id)

    result = rerank_with_priority(results)
    
    return results





# too Persistent FAISS + Cluster Filtering

# def retrieve_chunks(query):
#     q_vec = get_embedding(query)
#     results = search(q_vec, TOP_K)
#     return results