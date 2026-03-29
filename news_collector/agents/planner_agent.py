# agents/planner_agent.py

class PlannerAgent:

    def run(self, intent_data):
        intent = intent_data["intent"]

        if intent == "category":
            return ["fetch_category"]

        elif intent == "search":
            return ["search"]

        else:
            return ["fetch_all"]