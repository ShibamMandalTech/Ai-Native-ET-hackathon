# Modular architecture removed in favor of single-pass prompt

from retrieval.retriever import retrieve_chunks

from llm.groq_client import call_groq

def generate_story_arc(cluster_id, question=""):

    # Always search globally using FAISS to guarantee article extraction
    chunks = retrieve_chunks(question, None)[:15]
    
    if not chunks:
        return "Not enough relevant news data available in the database to compile a thorough Story Arc."

    context = "\n".join([c["text"][:300] for c in chunks])

    prompt = f"""
    Analyze this story and generate:

    1. In depth story decribing all the events in a narrative format with key players contribution.

    2. Timeline of events
    3. Sentiment trend over time
    4. Key players or entities
    5. Contradictions detected
    6. What to watch next (Provide 3 to 5 short, specific follow-up questions or clear search queries as bullet points)

    Return strictly structured output using EXACTLY these 6 section headers.

    Context:
    {context}
    """

    return call_groq(prompt, is_live=True)


# def generate_story_arc(cluster_id):

#     # Step 1: get relevant chunks
#     chunks = retrieve_chunks("", cluster_id=cluster_id)

#     # Step 2: timeline
#     timeline = build_timeline(chunks)

#     # Step 3: sentiment
#     sentiment = analyze_sentiment_trend(chunks)

#     # Step 4: key players
#     entities = extract_entities(chunks)

#     # Step 5: contradictions
#     contradictions = detect_contradictions(chunks)

#     # Step 6: future predictions
#     future = generate_predictions(chunks)

#     return {
#         "timeline": timeline,
#         "sentiment": sentiment,
#         "entities": entities,
#         "contradictions": contradictions,
#         "future": future
#     }