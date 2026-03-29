# agents/query_agent.py

import json
from core.llm import ask_llm

class QueryAgent:

    def run(self, query):
        prompt = f"""
You are an API that returns structured JSON.

Query: {query}

Return ONLY JSON:
{{
  "intent": "category/search/general",
  "category": "finance/technology/election/scam/war/politics/education/general/defence/investment/pharma/sports/null",
  "keywords": ["..."]
}}
"""

        res = ask_llm(prompt)
        data = clean_json(res)

        return {
            "intent": data.get("intent", "general"),
            "category": data.get("category"),
            "keywords": data.get("keywords", [])
        }

        # try:
        #     return json.loads(res)
        # except:
        #     return {
        #         "intent": "general",
        #         "category": None,
        #         "keywords": []
        #     }