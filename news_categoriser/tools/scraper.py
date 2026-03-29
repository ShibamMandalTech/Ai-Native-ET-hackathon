import requests
from bs4 import BeautifulSoup

def fetch_article(url, limit=None):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        res = requests.get(url, timeout=5, headers=headers)

        if res.status_code != 200:
            print("❌ Bad status:", res.status_code)
            return None

        soup = BeautifulSoup(res.text, "html.parser")

        paragraphs = [p.get_text().strip() for p in soup.find_all("p")]

        if limit:
            paragraphs = paragraphs[:limit]

        return " ".join(paragraphs)

    except Exception as e:
        print("❌ Scraper error:", e)
        return None



# import requests
# from bs4 import BeautifulSoup

# def fetch_article(url, limit=None):
#     try:
#         res = requests.get(url, timeout=5)
#         soup = BeautifulSoup(res.text, "html.parser")

#         paragraphs = [p.get_text().strip() for p in soup.find_all("p")]

#         if limit:
#             paragraphs = paragraphs[:limit]

#         return " ".join(paragraphs)

#     except Exception as e:
#         return None