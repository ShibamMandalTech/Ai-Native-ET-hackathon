# agents/search_agent.py

from tools.storage import get_all_news

class SearchAgent:

    def run(self, keyword):
        news = get_all_news()

        return [
            n for n in news
            if keyword.lower() in n["title"].lower()
        ]