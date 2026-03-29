


from retrieval.retriever import retrieve_chunks
from llm.groq_client import call_groq
from services.cluster_service import detect_top_clusters
from db.db import get_connection


#  fetch cluster insight
def get_cluster_insight(cluster_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)


    cursor.execute("""SELECT summary, macro, sectors, experts, timeline, sentiment FROM cluster_insights WHERE cluster_id = %s""", (cluster_id,))

    # cursor.execute("""
    # SELECT summary FROM cluster_insights WHERE cluster_id = %s
    # """, (cluster_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    # return row["summary"] if row else ""
    if not row:
        return ""

    return f"""
    SUMMARY:
    {row.get('summary')}

    MACRO:
    {row.get('macro')}

    SECTORS:
    {row.get('sectors')}

    EXPERTS:
    {row.get('experts')}

    TIMELINE:
    {row.get('timeline')}

    SENTIMENT:
    {row.get('sentiment')}
    """


#  build live context
def build_live_context(chunks):
    context = ""

    for c in chunks:
        context += f"""
Source: {c.get('source')}
Title: {c.get('title')}
Content: {c.get('text')}
"""

    return context


#  MAIN FUNCTION
def hybrid_answer(question):

    # Step 1: detect multiple clusters
    cluster_ids = detect_top_clusters(question)

    if not cluster_ids:
        print("No strong cluster match, using global retrieval")

    # Step 2: fetch cluster intelligence
    cluster_context = ""

    for cid in cluster_ids:
        insight = get_cluster_insight(cid)

        if insight:
            cluster_context += f""" === CLUSTER {cid} === {insight} """

    # Step 3: live retrieval (multi-cluster)
    all_chunks = []

    for cid in cluster_ids:
        chunks = retrieve_chunks(question, cid)
        all_chunks.extend(chunks)

    # fallback if no cluster match
    if not all_chunks:
        all_chunks = retrieve_chunks(question, None)

    live_context = build_live_context(all_chunks)

    #  Step 4: combine context
    final_context = f""" === CLUSTER INTELLIGENCE === {cluster_context} === LIVE UPDATES ==={live_context} """

    # Prevent context from becoming too large and pushing the question out of the prompt limit
    MAX_CONTEXT_LEN = 10000
    if len(final_context) > MAX_CONTEXT_LEN:
        final_context = final_context[:MAX_CONTEXT_LEN] + "\n... [Context Truncated]"

    #  Step 5: final reasoning prompt
    prompt = f"""
You are an advanced financial intelligence system.

The question may involve multiple topics.

Use:
1. Cluster intelligence (deep understanding)
2. Live updates (latest developments)

Instructions:
- Synthesize all available context and provide an in-depth, comprehensive analysis.
- The 'Summary' section MUST be a massive, extensive journalistic report spanning multiple long paragraphs. You MUST deeply analyze and include:
  1. The core event, immediate aftermath, and primary driver.
  2. The hidden geopolitical, policy, or macroeconomic triggers involved.
  3. The long-term trajectory and systemic risks.
  4. A dense, rich bulleted list of "Key Data Points & Contextual Statistics".
  5. The overarching sentiment of the market.
ALWAYS use markdown bold (**text**) to highlight the most important lines, metrics, and key insights so they instantly stand out. Do not write short summaries under any circumstance. Write as much relevant, high-quality detail as possible!
- The 'Timeline' section MUST be highly precise, strictly chronological, and detail exact dates (or timeframes) mapped to highly specific events.
- Give highly detailed structured output using EXACTLY these section headers (do not use asterisks or other formatting on them):
"Summary"
"Global Context"
"National Context"
"Market Overview"
"Who is Affected?"
"Expert Opinions"
"Historical Comparison"
"Timeline"
"Follow-up (3-5 questions based on the topic)"
- Put relevant content under each header.
- For each section, write extensively. Provide long-form elaboration AND use standard bullet points (starting with exactly '-') for specific data points and insights. 
- ALWAYS use markdown bold (**text**) to emphasize crucial metrics, percentages, entities, and important insights throughout the entire text.
Context:
{final_context}

Question:
{question}
"""

    return call_groq(prompt, is_live=True)

