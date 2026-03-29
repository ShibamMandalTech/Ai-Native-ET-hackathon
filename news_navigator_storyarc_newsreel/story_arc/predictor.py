from llm.groq_client import call_groq

def generate_predictions(chunks):

    context = "\n".join([c["text"][:300] for c in chunks])

    prompt = f"""
    Based on this news, predict what to watch next.

    Give 5 points.
    """

    return call_groq(prompt)