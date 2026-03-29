# agents/response_agent.py

class ResponseAgent:

    def run(self, results):
        if not results:
            return "No news found."

        response = "\n\n".join(
            [f"{n['title']}\n{n['url']}" for n in results[:5]]
        )

        return response