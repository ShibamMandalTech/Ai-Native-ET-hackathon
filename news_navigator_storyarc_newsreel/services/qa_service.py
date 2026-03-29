from retrieval.retriever import retrieve_chunks
from llm.groq_client import call_groq
from services.angle_classifier import detect_angle
from ingestion.embedder import get_embedding
import numpy as np

from story_arc.story_arc_service import generate_story_arc

#  CONFIG
TOP_K_PER_ANGLE = 3

def generate_timeline(context):
    prompt = f"""
    Extract a chronological timeline of events from the following news.

    Format:
    - Date/Event → Description

    If no clear timeline, summarize key sequence of events.

    Context:
    {context}
    """

    return call_groq(prompt)

def generate_followups(question, context):
    prompt = f"""
    Based on the question and context, suggest 3 to 5 intelligent follow-up questions.

    Keep them short and useful.

    Return as bullet points like :
- Question 1
- Question 2
- Question 3

    Question:
    {question}

    Context:
    {context}
    """

    return call_groq(prompt)

def detect_contradictions(context):
    prompt = f"""
    Analyze the following news statements.

    Identify if there are conflicting or opposing viewpoints.

    If yes, summarize the contradiction clearly.
    If no, return "No major contradictions found."

    Context:
    {context}
    """

    return call_groq(prompt)


def compute_confidence(chunks):
    sources = set()

    for c in chunks:
        if c.get("source"):
            sources.add(c.get("source"))

    count = len(sources)

    if count >= 5:
        return "High"
    elif count >= 3:
        return "Medium"
    else:
        return "Low"


#  Semantic re-ranking
def rerank_chunks(query, chunks, top_k=3):
    if not chunks:
        return []

    q_vec = get_embedding(query)

    scored = []

    for c in chunks:
        c_vec = get_embedding(c["text"])

        # cosine similarity
        denom = (np.linalg.norm(q_vec) * np.linalg.norm(c_vec))
        score = np.dot(q_vec, c_vec) / denom if denom != 0 else 0

        scored.append((score, c))

    # sort by similarity
    scored.sort(reverse=True, key=lambda x: x[0])

    return [c for _, c in scored[:top_k]]


#  Build structured context
def build_context(chunks):
    context = ""

    for i, c in enumerate(chunks, 1):
        context += f"""
[{i}] ({c.get('type', 'content').upper()})
Source: {c.get('source', 'Unknown')}
Title: {c.get('title', 'N/A')}
Content: {c.get('text')}
"""

    return context


#  MAIN FUNCTION
def answer_question(question, cluster_id=None):
    chunks = retrieve_chunks(question, cluster_id)
    

    if not chunks:
        return "No relevant information found."

    full_context = build_context(chunks)
    timeline = generate_timeline(full_context)
    followups = generate_followups(question, full_context)

    #  Step 1: Group by angle
    grouped = {
        "macro": [],
        "sectors": [],
        "experts": [],
        "general": []
    }

    for c in chunks:
        angle = detect_angle(c["text"])
        grouped[angle].append(c)

    #  Step 2: Semantic re-ranking per angle
    for key in grouped:
        grouped[key] = rerank_chunks(question, grouped[key], TOP_K_PER_ANGLE)

    #  Step 3: Fallback if empty
    for key in ["macro", "sectors", "experts"]:
        if not grouped[key]:
            grouped[key] = grouped["general"][:2]

    responses = {}

    angle_contexts = {}

    #  Step 4: Generate responses per angle


    for angle in ["macro", "sectors", "experts"]:

        if grouped[angle]:
            context = build_context(grouped[angle])

            angle_contexts[angle] = context

            if angle == "experts":
                contradiction = detect_contradictions(context)
            else:
                contradiction = "No major contradictions found."

            confidence = compute_confidence(grouped[angle])

            prompt = f"""
    You are an expert news analyst. Prioritize: 1st SUMMARY points for key facts. 2nd - DEEP content for detailed explanation

    ONLY discuss in depth the {angle} perspective.
    DO NOT mention or mix other aspects. Strictly stay within this aspect.

Create a full depth discussion about it and also create points.
    If information is insufficient, say:
    "Limited data available for this aspect."

    Use ONLY the context below.
    Avoid repetition.
    Mention sources when relevant.

    Context:
    {context}

    Question:
    {question}
    """

            answer = call_groq(prompt)

        else:
            #  THIS WAS MISSING (CRITICAL)
            answer = "Limited data available for this aspect."
            contradiction = ""
            confidence = "Low"

        # ALWAYS assign
        responses[angle] = {
            "answer": answer,
            "contradiction": contradiction,
            "confidence": confidence
        }
#     for angle in ["macro", "sectors", "experts"]:
#         if grouped[angle]:
#             context = build_context(grouped[angle])
#             # contradiction = detect_contradictions(context)
#             if angle == "experts":
#                 contradiction = detect_contradictions(context)
#             else:
#                 contradiction = "No major contradictions found."

#             confidence = compute_confidence(grouped[angle])

#             prompt = f"""
# You are an expert news analyst.

# ONLY discuss the {angle} perspective.
# DO NOT mention or mix other aspects. Strictly stay with aspect.

# If information is insufficient, say:
# "Limited data available for this aspect."

# Use ONLY the context below.
# Avoid repetition.
# Mention sources when relevant.

# Context:
# {context}

# Question:
# {question}
# """

#             # responses[angle] = call_groq(prompt)
#             responses[angle] = {
#                 "answer": call_groq(prompt),
#                 "contradiction": contradiction,
#                 "confidence": confidence
#             }

    #  Step 5: Combine outputs
    # final_answer = ""

    # if "macro" in responses:
    #     final_answer += f"\n Macro Impact:\n{responses['macro']}\n"

    # if "sectors" in responses:
    #     final_answer += f"\n Sector Impact:\n{responses['sectors']}\n"

    # if "experts" in responses:
    #     final_answer += f"\n Expert Opinions:\n{responses['experts']}\n"

    final_answer = ""

    for angle, emoji, title in [
        ("macro", "", "Macro Impact"),
        ("sectors", "", "Sector Impact"),
        ("experts", "", "Expert Opinions")
    ]:
        if angle in responses:
            data = responses[angle]

            final_answer += f"\n{emoji} {title}:\n{data['answer']}\n"

            #  show contradiction only if meaningful
            if data.get("contradiction") and data["contradiction"] != "No major contradictions found.":
                final_answer += f"\n Contradictions:\n{data['contradiction']}\n"

            # final_answer += f"\n Contradictions:\n{data['contradiction']}\n"

            final_answer += f" Confidence: {data['confidence']}\n"

            final_answer += "\n" + "-"*50 + "\n"

    final_answer += f"\n Timeline:\n{timeline}\n"
    final_answer += f"\n Follow-up Questions:\n{followups}\n"

    #  NEW: story arc
    story_arc = generate_story_arc(cluster_id)

    # return {
    #     "answer": final_answer.strip(),
    #     "contexts": angle_contexts,
    #     "timeline": timeline,
    #     "followups": followups,
    #     "story_arc": story_arc   #  NEW
    # } 

    return {
        "answer": final_answer.strip(),
        "contexts": angle_contexts,   
        "timeline": timeline,
        "followups": followups,
        "story_arc": story_arc #  NEW
    }
    
    # return final_answer.strip()
    

# for story arc tracker
# from story_arc.story_arc_service import generate_story_arc


# def answer_question(question, cluster_id):

#     main_answer = generate_multi_angle_answer(question, cluster_id)

#     story_arc = generate_story_arc(cluster_id)

#     return {
#         "answer": main_answer,
#         "story_arc": story_arc
#     }

        
