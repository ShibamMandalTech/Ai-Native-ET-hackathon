


# # agents/classifier_agent.py


# agents/classifier_agent.py

from tqdm import tqdm

from core.llm import ask_llm, clean_json

from concurrent.futures import ThreadPoolExecutor, as_completed

import time
import threading

def fallback_category(title):
    t = title.lower()

    if "job" in t or "hiring" in t:
        return ["job"]
    if "law" in t or "court" in t:
        return ["law"]
    if "research" in t or "study" in t:
        return ["research"]
    if "education" in t or "study" in t:
        return ["education"]
    if "technology" in t or "tech" in t:
        return ["tecnology"]
    if "investor" in t or "finance" in t:
        return ["research"]

    return ["general"]

class ClassifierAgent:

    def classify_batch(self, articles, retries=2):
        titles = [a["title"] for a in articles]

        prompt = f"""
You are a strict JSON generator.

Classify each news title into ONE OR MORE categories.

Allowed categories:
finance, research, technology, politics, investment,scam,sports,defence,pharma,election,entertainment, education, law, job, general

Rules:
- Multiple categories allowed
- Return as a LIST
- If unsure → general

Return ONLY JSON:
[
  {{"title": "...", "category": ["finance", "technology"]}}
]

Titles:
{titles}
"""
        
#         prompt = f"""
# You are a strict JSON generator.

# RULES:
# - Return ONLY valid JSON
# - No explanation
# - No extra text
# - No comments

# Format:
# [
#   {{"title": "...", "category": "..."}}
# ]

# Titles:
# {titles}
# """
        
#         prompt = f"""
# Classify these news titles into categories:
# finance, technology, politics, education, general

# Return ONLY JSON list:
# [
#   {{"title": "...", "category": "..."}}
# ]

# Titles:
# {titles}
# """

        # res = ask_llm(prompt)
        # data = clean_json(res)

        # return data

        for attempt in range(retries + 1):
            res = ask_llm(prompt)
            data = clean_json(res)

            # ✅ valid result
            if isinstance(data, list) and len(data) > 0:
                return data

            print(f"⚠️ Retry {attempt+1} failed...")

        # ❌ fallback
        # return []
        # ❌ ALL RETRIES FAILED → USE FALLBACK
        print("❌ LLM failed → using fallback")

        fallback_results = []

        for a in articles:
            fallback_results.append({
                "title": a["title"],
                "category": fallback_category(a["title"])
            })

        return fallback_results

    

    def run(self, articles):
        print(f"\n🧠 Classifying {len(articles)} articles...\n")

        total = len(articles)   # 🔥 ADD THIS LINE

        chunk_size = 15
        max_workers = 2   # 🔥 parallel threads

        # 🔹 split into batches
        batches = [
            articles[i:i + chunk_size]
            for i in range(0, len(articles), chunk_size)
        ]

        results_all = []

        # 🔥 progress bar (article-based, not chunk-based)
        pbar = tqdm(total=total, desc="Classifying", ncols=100)

        def process_batch(batch):
            # time.sleep(1)
            

            print(f"Running in thread: {threading.current_thread().name}")
            results = self.classify_batch(batch)
            tqdm.write(f"LLM OUTPUT: {results}")

            # map results
            for a in batch:
                match = next(
                    (
                        r for r in results
                        if isinstance(r, dict)
                        and r.get("title")
                        and any(word in a["title"] for word in r.get("title").split()[:5])
                    ),
                    None
                )
                
                # match = next
                #     (r for r in results if isinstance(r, dict) and r.get("title") and any(word in a["title"] for word in r.get("title").split()[:5]),
                #     None
                # )

                if match and isinstance(match.get("category"), list):
                    a["category"] = ",".join(match["category"])   # store as string
                else:
                    a["category"] = "general"
                
                # a["category"] = match.get("category", "general") if match else "general"


            return batch

        # 🔥 PARALLEL EXECUTION
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(process_batch, b) for b in batches]

            for f in as_completed(futures):
                batch_result = f.result()
                results_all.extend(batch_result)

                # 🔥 update progress safely
                pbar.update(len(batch_result))

        pbar.close()

        print("\n✅ Classification complete!\n")
        return results_all
            
        #     for f in as_completed(futures):
        #         results_all.extend(f.result())

        # print("\n✅ Classification complete!\n")
        # return results_all
    
    
    # def run(self, articles):
    #     print(f"\n🧠 Classifying {len(articles)} articles...\n")

    #     # 🔥 split into chunks (IMPORTANT)
    #     chunk_size = 20

    #     # chunk_size = min(5, len(articles))

    #     # max_workers = 5   # 🔥 parallel threads

    #     # 🔹 split into batches
    #     batches = [
    #         articles[i:i + chunk_size]
    #         for i in range(0, len(articles), chunk_size)
    #     ]

    #     total_chunks = (len(articles) + chunk_size - 1) // chunk_size

    #     for i in tqdm(range(0, len(articles), chunk_size), desc="Classifying"):
    #         chunk = articles[i:i+chunk_size]

    #         results = self.classify_batch(chunk)

    #         # 🔥 DEBUG (optional)
    #         # print("RESULTS:", results)

    #         for a in chunk:
    #             match = next(
    #                 (r for r in results if isinstance(r, dict) and r.get("title") == a["title"]),
    #                 None
    #             )

    #             if match:
    #                 a["category"] = match.get("category", "general")
    #             else:
    #                 a["category"] = "general"

    #     print("\n✅ Classification complete!\n")
        

    #     # for i in range(0, len(articles), chunk_size):
    #     #     chunk = articles[i:i+chunk_size]

    #     #     results = self.classify_batch(chunk)
    #     #     print("RESULTS:", results)   # 🔥 DEBUG HERE

    #     #     # map results
    #     #     for a in chunk:
    #     #         match = next(
    #     #             (r for r in results if r.get("title") == a["title"]),
    #     #             None
    #     #         )

    #     #         if match:
    #     #             a["category"] = match.get["category","general"]
    #     #         else:
    #     #             a["category"] = "general"

    #     return articles


# import json
# from core.llm import ask_llm, clean_json

# class ClassifierAgent:

#     def classify(self, title):
#         prompt = f"""
# You are a strict JSON generator.

# Classify the news title into one category:
# finance, technology, politics, education, general

# Return ONLY JSON:
# {{"category": "..."}} 

# Title: {title}
# """

#         print(f"Classifying: {title}")

#         res = ask_llm(prompt)
#         data = clean_json(res)

#         return data.get("category", "general")

#         # try:
#         #     return json.loads(res)["category"]
#         # except:
#         #     return "general"

#     def run(self, articles):
#         for a in articles:
#             a["category"] = self.classify(a["title"])
#             a["status"] = "classified"

#         return articles