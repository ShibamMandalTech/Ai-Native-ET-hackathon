from agents.decision_agent import decide
from agents.short_agent import run_short_agent
from agents.deep_agent import run_deep_agent
from agents.summary_agent import generate_summary

import time

from db.queries import update_field, increment_retry


def run_agent(row):
    action = decide(row)

    print(f"ID {row['id']} | content={bool(row['content'])} | deep={bool(row['deep_content'])}| summary={bool(row['summary_points'])}")
    print(f"→ ACTION: {action}")

    try:
        # 🔹 SHORT STAGE
        if action == "short":
            short = run_short_agent(row["url"])

            print(f"Short result: {short}")

            if not short:
                raise Exception("Short content failed")

            update_field(row["id"], "content", short)
            update_field(row["id"], "processing_stage", "short_done")

        # 🔹 DEEP STAGE
        elif action == "deep":
            # deep = run_deep_agent(row["url"])
            print(f"🔵 DEEP → {row['url']}")

            # 🔥 EXTRA SAFETY
            if not row["content"]:
                print("⚠️ Skipping deep (no short content)")
                return "skip"

            deep = run_deep_agent(row["url"])

            if not deep:
                raise Exception("Deep content failed")

            update_field(row["id"], "deep_content", deep)
            update_field(row["id"], "processing_stage", "deep_done")

            

        # 🔹 SUMMARY STAGE (LLM)
        elif action == "summary":
            print(f"🟣 SUMMARY → ID {row['id']}")

            if not row["deep_content"]:
                print("⚠️ Skipping summary (no deep content)")
                return "skip"

            summary = generate_summary(row["deep_content"])
            # time.sleep(2)

            if not summary:
                raise Exception("Summary failed")

            update_field(row["id"], "summary_points", summary)
            update_field(row["id"], "processing_stage", "summary_done")

        # 🔹 COMPLETE
        elif action == "complete":
            print(f"✅ COMPLETE → ID {row['id']}")

            update_field(row["id"], "status", "complete")
            update_field(row["id"], "processing_stage", "complete")

        return action

    except Exception as e:
        print(f"❌ Error on ID {row['id']}: {e}")

        increment_retry(row["id"])

        # 🔥 VERY IMPORTANT FIX
        if row["retries"] >= 3:
            update_field(row["id"], "processing_stage", "failed")
            update_field(row["id"], "status", "failed")

        return "error"




# from agents.decision_agent import decide
# from agents.short_agent import run_short_agent
# from agents.deep_agent import run_deep_agent
# from agents.summary_agent import run_summary_agent
# from db.queries import update_field

# def run_agent(row):
#     action = decide(row)

#     if action == "short":
#         short = run_short_agent(row["url"])
#         update_field(row["id"], "content", short)

#     elif action == "deep":
#         deep = run_deep_agent(row["url"])   # 🔥 FROM URL AGAIN
#         update_field(row["id"], "deep_content", deep)

#     elif action == "summary":
#         summary = run_summary_agent(row["deep_content"])
#         update_field(row["id"], "summary_points", summary)

#     elif action == "complete":
#         update_field(row["id"], "status", "complete")

#     return action