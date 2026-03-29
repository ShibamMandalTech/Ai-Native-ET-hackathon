from llm.groq_client import call_groq

def analyze_sentiment_trend(chunks):

    context = "\n".join([c["text"][:300] for c in chunks])

    prompt = f"""
    Analyze sentiment trend over time.

    Return:
    Date → Sentiment (positive/negative/neutral)

    Context:
    {context}
    """

    return call_groq(prompt)


    #it has about 20 calls for each chunk

# def get_sentiment(text):

#     prompt = f"""
#     Classify sentiment: positive, negative or neutral.

#     Text:
#     {text}
#     """

#     return call_groq(prompt)


# def analyze_sentiment_trend(chunks):

#     trend = []

#     for c in chunks:
#         sentiment = get_sentiment(c["text"])

#         trend.append({
#             "date": c.get("created_at"),
#             "sentiment": sentiment
#         })

#     return trend