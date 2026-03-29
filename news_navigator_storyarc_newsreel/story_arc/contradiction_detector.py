from llm.groq_client import call_groq

def detect_contradictions(chunks):

    context = "\n".join([c["text"][:300] for c in chunks])

    prompt = f"""
    Identify conflicting opinions in the following news.

    {context}
    """

    return call_groq(prompt)