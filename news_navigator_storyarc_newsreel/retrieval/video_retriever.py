from ingestion.embedder import get_embedding
from vector.faiss_store import search
from config import EMBED_MODEL
from config import VIDEO_QUERY

def retrieve_video_chunks(top_k=20, cluster_id=None, dynamic_query=None):
    query_text = dynamic_query if dynamic_query else VIDEO_QUERY
    query_vec = get_embedding(query_text)
    results = search(query_vec, top_k=top_k, cluster_id=cluster_id)
    return results


def group_chunks_by_news(chunks):
    articles = {}

    for chunk in chunks:
        nid = chunk["news_id"]

        if nid not in articles:
            articles[nid] = {
                "news_id": nid,
                "title": chunk.get("title"),
                "summary": [],
                "content": [],
                "score": 0,
                "cluster_id": chunk.get("cluster_id")
            }

        if chunk.get("type") == "summary":
            articles[nid]["summary"].append(chunk["text"])
            articles[nid]["score"] += 2
        else:
            articles[nid]["content"].append(chunk["text"])
            articles[nid]["score"] += 1

    return list(articles.values())