

from db.db import get_connection
from llm.groq_client import call_groq
from datetime import datetime
import json
import os

STATE_FILE = "cluster_state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def build_context(rows):
    context = ""
    for r in rows:
        deep_content = r.get("deep_content") or r.get("content") or ""
        summary_points = r.get("summary_points") or ""
        
        context += f"TITLE: {r.get('title')}\n"
        context += f"SUMMARY: {summary_points[:1500]}\n"
        context += f"CONTENT: {deep_content[:300]}\n\n"
    return context


def generate_cluster_insights():
    state = load_state()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    #  Only process clusters that have new articles
    cursor.execute("SELECT cluster_id, MAX(id) as max_id FROM news WHERE cluster_id IS NOT NULL GROUP BY cluster_id")

    cluster_updates = cursor.fetchall()

    if not cluster_updates:
        print("⚡ No clusters found in database")
        return

    clusters_to_process = []
    new_state = state.copy()

    for row in cluster_updates:
        cid = str(row["cluster_id"])
        max_id = row["max_id"]

        # Only process if max_id is strictly greater than the last recorded processed id
        if cid not in state or max_id > state[cid]:
            clusters_to_process.append(row["cluster_id"])
            new_state[cid] = max_id

    if not clusters_to_process:
        print("⚡ No new articles to summarize for any cluster. Sleeping...")
        return

    for cluster_id in clusters_to_process:

        cursor.execute("""
        SELECT title, content, deep_content, summary_points
        FROM news 
        WHERE cluster_id = %s
        """, (cluster_id,))

        rows = cursor.fetchall()

        if not rows:
            continue

        context = build_context(rows)

        prompt = f"""
You are a financial intelligence system.

Analyze the topic and return JSON ONLY:

{{
  "summary": "A clear in depth story with all events of about 100 words",
  "macro": "Global and National Context (Broad economic/market overview and country-specific impact in depth details of about 200 words each and 7 to 8 points)",
  "sectors": "Who is Affected? (create story of 6-7 points which include how public or citizen is affected and Sector-wise impact in depth with points also give companies name if possible) ",
  "experts": "Expert opinions and views (7 to 8 points)",
  "timeline": "Chronological sequence of events with recent dates and Historical Comparisons with past events",
  "sentiment": "Positive/Negative/Neutral"
}}

Rules:
- Be informative
- Avoid repetition
- Keep sections distinct

Context:
{context}
"""

        # result = call_groq(prompt)
        raw = call_groq(prompt)

        # remove markdown if present
        raw = raw.strip().replace("```json", "").replace("```", "").strip()

        try:
            data = json.loads(raw)
        except:
            print(" JSON parsing failed, fallback")
            data = {
                "summary": raw,
                "macro": "",
                "sectors": "",
                "experts": "",
                "timeline": "",
                "sentiment": "Neutral"
            }

        valid_sentiments = ["Positive", "Negative", "Neutral"]

        sentiment = data.get("sentiment", "Neutral")

        if sentiment not in valid_sentiments:
            sentiment = "Neutral"

        data["sentiment"] = sentiment

        print("FINAL SENTIMENT:", data["sentiment"])

        cursor.execute("""
            INSERT INTO cluster_insights 
            (cluster_id, summary, macro, sectors, experts, timeline, sentiment, last_updated)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                summary=%s,
                macro=%s,
                sectors=%s,
                experts=%s,
                timeline=%s,
                sentiment=%s,
                last_updated=%s
            """, (
                cluster_id,
                str(data.get("summary", "")),
                str(data.get("macro", "")),
                str(data.get("sectors", "")),
                str(data.get("experts", "")),
                str(data.get("timeline", "")),
                str(data.get("sentiment", "Neutral")),
                datetime.now(),

                str(data.get("summary", "")),
                str(data.get("macro", "")),
                str(data.get("sectors", "")),
                str(data.get("experts", "")),
                str(data.get("timeline", "")),
                str(data.get("sentiment", "Neutral")),
                datetime.now()
            ))

                #        cursor.execute("""
                # INSERT INTO cluster_insights 
                # (cluster_id, summary, macro, sectors, experts, timeline, sentiment, last_updated)
                # VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                # ON DUPLICATE KEY UPDATE
                #     summary=%s,
                #     macro=%s,
                #     sectors=%s,
                #     experts=%s,
                #     timeline=%s,
                #     sentiment=%s,
                #     last_updated=%s
                # """, (
                #     cluster_id,
                #     data.get("summary"),
                #     data.get("macro"),
                #     data.get("sectors"),
                #     data.get("experts"),
                #     data.get("timeline"),
                #     data.get("sentiment"),
                #     datetime.now(),

                #     data.get("summary"),
                #     data.get("macro"),
                #     data.get("sectors"),
                #     data.get("experts"),
                #     data.get("timeline"),
                #     data.get("sentiment"),
                #     datetime.now()
                # ))
                        
                        
                        # cursor.execute("""
                        # INSERT INTO cluster_insights (cluster_id, summary, last_updated)
                        # VALUES (%s, %s, %s)
                        # ON DUPLICATE KEY UPDATE 
                        #     summary=%s,
                        #     last_updated=%s
                        # """, (
                        #     cluster_id,
                        #     result,
                        #     datetime.now(),
                        #     result,
                        #     datetime.now()
                        # ))

        print(f" Updated cluster insight: {cluster_id}")

        #  CRITICAL: Save progress incrementally INSIDE the loop
        # so if the script crashes on Cluster #5, Clusters 1-4 are saved
        # and it won't repeat them next time!
        state[str(cluster_id)] = new_state[str(cluster_id)]
        save_state(state)
        conn.commit()

        import time
        time.sleep(3) # Give API a breather between clusters

    cursor.close()
    conn.close()