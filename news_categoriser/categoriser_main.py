import time
from db.queries import get_batch, get_rows_by_ids
from services.executor import run_agent


def run_pipeline():
    while True:

        rows = get_batch(20)
        batch_ids = [row["id"] for row in rows]


        # ===== SHORT =====
        print("=== SHORT STAGE ===")
        rows = get_rows_by_ids(batch_ids)

        for row in rows:
            if not row["content"]:
                run_agent(row)


        # ===== DEEP =====
        print("=== DEEP STAGE ===")
        rows = get_rows_by_ids(batch_ids)

        for row in rows:
            if row["content"] and not row["deep_content"]:
                run_agent(row)


        # ===== SUMMARY =====
        print("=== SUMMARY STAGE ===")
        rows = get_rows_by_ids(batch_ids)

        count = 0

        for row in rows:
            if row["deep_content"] and not row["summary_points"]:
                run_agent(row)
                count += 1

                if count >= 20:
                    break
        # rows = get_batch(20)

        # if not rows:
        #     print("No data. Sleeping 40 min...")
        #     time.sleep(2400)
        #     continue

        # batch_ids = [row["id"] for row in rows]

        # print("=== SHORT STAGE ===")
        # rows = get_rows_by_ids(batch_ids)

        # for row in rows:
        #     if not row["content"]:
        #         run_agent(row)

        # print("=== DEEP STAGE ===")
        # rows = get_rows_by_ids(batch_ids)

        # for row in rows:
        #     if row["content"] and not row["deep_content"]:
        #         run_agent(row)

        # print("=== SUMMARY STAGE ===")
        # count = 0

        # for row in rows:
        #     if row["deep_content"] and not row["summary_points"]:
        #         run_agent(row)
        #         count += 1

        #     if count >= 5:   # 🔥 limit actual summary calls
        #         break
        
        
        # rows = get_rows_by_ids(batch_ids)

        # for row in rows:
        #     if row["deep_content"] and not row["summary_points"]:
        #         run_agent(row)

        print("=== COMPLETE ===\n")

        time.sleep(5)


if __name__ == "__main__":
    run_pipeline()



# import time
# from db.queries import get_batch
# from services.executor import run_agent
# from services.error_handler import handle_error


# def run_hybrid():
#     while True:
#         rows = get_batch(20)

#         batch_ids = [row["id"] for row in rows]

#         if not rows:
#             print("No data. Sleeping 40 min...")
#             time.sleep(2400)
#             continue

#         print(f"Processing batch of {len(rows)} rows...")

#         row_ids = [row["id"] for row in rows]

#         for row in rows:
#             try:
#                 action = run_agent(row)
#                 print(f"ID {row['id']} → {action}")

#             except Exception as e:
#                 handle_error(row["id"])
#                 print(f"Error on {row['id']}: {e}")

#         print("Batch done.\n")
#         time.sleep(5)  # small pause


# if __name__ == "__main__":
#     run_hybrid()


#changes for decision agent+ batch

# import time
# from db.queries import get_next_news
# from services.executor import run_agent
# from services.error_handler import handle_error

# def loop():
#     while True:
#         row = get_next_news()

#         if not row:
#             time.sleep(5)
#             continue

#         try:
#             action = run_agent(row)
#             print(f"{row['id']} → {action}")

#         except Exception as e:
#             handle_error(row["id"], str(e))

#         time.sleep(2)

# if __name__ == "__main__":
#     loop()