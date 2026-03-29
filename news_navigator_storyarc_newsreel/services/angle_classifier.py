from llm.groq_client import call_groq

angle_cache = {}

def detect_angle(text):
    prompt = f"""
    Classify the following news content into ONE category:

    Categories:
    - macro (economy, GDP, inflation, policy)
    - sectors (industry, IT, banking, stocks)
    - experts (opinions, analysts, economists)
    - general (none of above)

    Text:
    {text[:500]}

    Only return one word: macro / sectors / experts / general
    """

    if text in angle_cache:
        return angle_cache[text]
    
    result = call_groq(prompt).strip().lower()

    # if result not in ["macro", "sectors", "experts", "general"]:
    #     return "general"

    angle_cache[text] = result

    return result