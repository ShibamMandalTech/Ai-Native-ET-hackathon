# tools/scraper.py

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "https://economictimes.indiatimes.com"

SECTIONS = [
    "/markets",
    "/tech",
    "/industry",
    "/news/economy",
    "/news/education",
    "/news/politics-nation",
    "/news/politics",
    "/markets",
    "/news/defence",
    "/news/elections",
    "/news/newsblogs",
    "/prime/economy-and-policy",
    "/prime/corporate-governance",
    "/prime/environment",
    "/prime/pharma-and-healthcare",
    "/prime/energy",
    "/markets/expert-views",
    "/prime/investment-ideas",
    "/news/economy/policy",
    "/news/sports",
    "/industry/healthcare",
    "/ai/ai-insights"
    "/prime",
    "/jobs"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


# 🔹 FETCH HTML (REUSABLE)
def fetch_page(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)

        if res.status_code == 404:
            print(f"⚠️ Skipping (404): {url}")
            return None
            
        res.raise_for_status()
        return res.text
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return ""


# 🔹 SCRAPE SECTION (MULTI-PAGE)
def scrape_section(section, pages=6):
    articles = []

    for page in range(1, pages + 1):
        url = f"{BASE_URL}{section}?page={page}"
        print(f"🔍 Fetching: {url}")

        html = fetch_page(url)
        if html is None:
            break   # 🔥 STOP further pages (IMPORTANT)

        soup = BeautifulSoup(html, "html.parser")

        for a in soup.find_all("a", href=True):
            title = a.get_text(strip=True)
            link = a["href"]

            if title and "/articleshow" in link:
                full_link = BASE_URL + link if link.startswith("/") else link

                articles.append({
                    "title": title,
                    "url": full_link
                })

    return articles


# 🔹 SCRAPE ARTICLE CONTENT
def scrape_article_content(url, max_len=1500):
    html = fetch_page(url)
    if not html:
        return ""

    try:
        soup = BeautifulSoup(html, "html.parser")

        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs)

        return text[:max_len]

    except Exception as e:
        print(f"❌ Error parsing article {url}: {e}")
        return ""


# 🔹 PARALLEL CONTENT FETCH (FAST 🔥)
def enrich_with_content(articles, max_workers=5):
    def process(article):
        article["content"] = scrape_article_content(article["url"])
        return article

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(process, articles))


# 🔹 MAIN SCRAPER
def scrape_news(pages=1, with_content=False):
    all_articles = []

    for section in SECTIONS:
        print(f"\n📂 Scraping section: {section}")
        section_articles = scrape_section(section, pages)

        all_articles.extend(section_articles)

    # 🔥 REMOVE DUPLICATES
    unique = {a["url"]: a for a in all_articles}
    articles = list(unique.values())

    print(f"\n✅ Total unique articles: {len(articles)}")

    # 🔥 OPTIONAL: FETCH CONTENT (SLOW → USE ONLY WHEN NEEDED)
    if with_content:
        print("\n⚡ Fetching article content in parallel...")
        articles = enrich_with_content(articles)

    return articles