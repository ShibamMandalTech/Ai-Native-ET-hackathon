# agents/collector_agent.py

from tools.scraper import scrape_section, SECTIONS

class CollectorAgent:

    def run(self):
        all_articles = []

        for section in SECTIONS:
            articles = scrape_section(section)

            for a in articles:
                if not a.get("title") or not a.get("url"):
                    continue

                all_articles.append({
                    "title": a["title"],
                    "url": a["url"],
                    "content": None,
                    "status": "raw"
                })

        # remove duplicates
        unique = {a["url"]: a for a in all_articles}
        return list(unique.values())