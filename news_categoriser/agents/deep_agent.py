# agents/deep_agent.py

from tools.scraper import fetch_article


def run_deep_agent(url):
    print(f"🔵 DEEP: Fetching URL → {url}")

    text = fetch_article(url)

    # ❌ No data fetched
    if not text:
        print("❌ Deep agent: No text fetched")
        return None

    # ❌ Too small (likely failure page)
    if len(text) < 200:
        print(f"❌ Deep agent: Text too small ({len(text)} chars)")
        return None

    print(f"✅ Deep agent: Fetched {len(text)} characters")

    # Limit size (important for DB + LLM)
    return text[:5000]



# from tools.scraper import fetch_article

# def run_deep_agent(url):
#     text = fetch_article(url)  # FULL scrape

#     if not text:
#         return None

#     # clean or structure if needed
#     return text[:5000]   # limit to avoid huge storage