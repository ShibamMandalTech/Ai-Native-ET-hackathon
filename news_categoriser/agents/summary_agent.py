from tools.llm_client import call_llm

def generate_summary(deep_text):
    if not deep_text:
        return None

    prompt = f"""
    Analyze the following news deeply and generate structured bullet points.
    Act as a senior news analyst.

    Break down the news into deep insights.

    Focus on:
    1. What happened
    2. Why it happened
    3. Who is affected
    4. What changes next

    Requirements:
    - Give minimum 3-5 detailed points in 1500 characters
    - Include key facts, background, impact, and future implications
    - Each point should be meaningful (not generic)
    - Use bullet format

    News:
    {deep_text[:3000]}
    """

    # return call_llm(prompt)
    try:
        result = call_llm(prompt)

        if not result or len(result.strip()) == 0:
            return None

        return result.strip()

    except Exception as e:
        print("LLM Error:", e)
        return None