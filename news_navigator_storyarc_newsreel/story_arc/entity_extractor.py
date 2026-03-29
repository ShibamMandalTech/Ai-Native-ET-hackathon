from llm.groq_client import call_groq

def extract_entities(chunks):

    context = "\n".join([c["text"][:300] for c in chunks])

    prompt = f"""
    Extract key companies, people, and organizations.

    Context:
    {context}

    Return JSON list.
    """

    return call_groq(prompt)