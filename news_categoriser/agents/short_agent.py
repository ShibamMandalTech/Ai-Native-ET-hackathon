from tools.scraper import fetch_article

def run_short_agent(url):
    print(f"Fetching URL: {url}")   # DEBUG

    text = fetch_article(url, limit=10)

    if not text:
        print("❌ No text fetched")
        return None

    short = text[:400] + "..."

    print("✅ Short generated")

    return short

# def run_short_agent(url):
#     text = fetch_article(url, limit=10)  # small scrape

#     if not text:
#         return None

#     # lightweight summary
#     return text[:400] + "..."