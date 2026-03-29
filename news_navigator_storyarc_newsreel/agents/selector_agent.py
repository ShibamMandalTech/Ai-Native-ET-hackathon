from retrieval.video_retriever import retrieve_video_chunks, group_chunks_by_news
from agents.personalization_agent import get_user_preferences

def build_dynamic_query(base_query, preferences):
    if not preferences:
        return base_query

    pref_text = ", ".join(preferences)

    return f"""
    {base_query}
    Focus more on: {pref_text}
    Prioritize engaging and high-retention content.
    """

def build_persona_query(base_query, persona):
    if not persona or persona == "General Audience":
        return base_query
    
    return f"""
    {base_query}
    Specifically tailored and extremely relevant for: {persona}.
    Identify stories, trends, or updates this specific demographic would find most compelling.
    """

def select_video_news(cursor, user_id=None, top_k=3, cluster_id=None, user_type="General Audience"):
    from config import VIDEO_QUERY
    dyn_query = build_persona_query(VIDEO_QUERY, user_type)
    
    chunks = retrieve_video_chunks(top_k=20, cluster_id=cluster_id, dynamic_query=dyn_query)
    articles = group_chunks_by_news(chunks)

    articles.sort(key=lambda x: x["score"], reverse=True)

    # ✅ Filter out successfully created videos to prioritize new/failed ones
    valid_articles = []
    for art in articles:
        cursor.execute("SELECT video_status FROM news WHERE id=%s", (art["news_id"],))
        row = cursor.fetchone()
        if not row:
            continue
            
        # Accommodate db setups where dict cursor is or isn't used
        status = row["video_status"] if isinstance(row, dict) else (row[0] if type(row) is tuple else None)
        
        # Prioritize anything that hasn't successfully finished (PENDING, FAILED, crashed mid-way)
        if status != 'VIDEO_CREATED':
            valid_articles.append(art)
            
    # Fallback: if all retrieved articles were already generated, let's just regenerate them 
    # so the app ALWAYS produces a video when the user clicks 'Generate'!
    if not valid_articles:
        valid_articles = articles
            
    selected = valid_articles[:top_k]

    # ✅ mark as SELECTED so they aren't simultaneously picked by another thread
    for article in selected:
        cursor.execute(
            "UPDATE news SET video_status='SELECTED' WHERE id=%s",
            (article["news_id"],)
        )

    return selected