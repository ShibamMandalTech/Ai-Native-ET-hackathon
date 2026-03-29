# core/agent_manager.py

from agents.collector_agent import CollectorAgent
from agents.classifier_agent import ClassifierAgent
from agents.search_agent import SearchAgent
from agents.query_agent import QueryAgent
from agents.planner_agent import PlannerAgent
from agents.response_agent import ResponseAgent

from tools.storage import save_news, get_news_by_category, get_all_news

class AgentManager:

    def __init__(self):
        self.collector = CollectorAgent()
        self.classifier = ClassifierAgent()
        self.search = SearchAgent()
        self.query = QueryAgent()
        self.planner = PlannerAgent()
        self.response = ResponseAgent()

    # def ingest(self):
    #     articles = self.collector.run()
    #     articles=articles[:100]
    #     classified = self.classifier.run(articles)
    #     save_news(classified)

    def ingest(self):
        articles = self.collector.run()

        print(f"⚡ Saving {len(articles)} raw articles...")

        save_news(articles)   # no classification

        print("✅ Stored raw news (fast)")

    # def ingest(self):
    #     articles = self.collector.run()

    #     total = len(articles)
    #     batch_size = 50   # 🔥 you control this

    #     print(f"\n📦 Total articles: {total}")
    #     print(f"⚡ Processing in batches of {batch_size}\n")

    #     for i in range(0, total, batch_size):
    #         batch = articles[i:i + batch_size]

    #         print(f"\n🚀 Processing batch {i//batch_size + 1} ({len(batch)} articles)")

    #         classified = self.classifier.run(batch)

    #         save_news(classified)

    #         print(f"✅ Batch {i//batch_size + 1} done\n")

    def handle_query(self, query):
        intent = self.query.run(query)
        plan = self.planner.run(intent)

        results = []

        if "fetch_category" in plan:
            results = get_news_by_category(intent["category"])

        elif "search" in plan:
            results = self.search.run(intent["keyword"])

        elif "fetch_all" in plan:
            results = get_all_news()

        return self.response.run(results)