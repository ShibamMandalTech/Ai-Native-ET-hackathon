from apscheduler.schedulers.blocking import BlockingScheduler
from core.agent_manager import AgentManager

manager = AgentManager()

def job():
    print("🚀 Running news ingestion...")
    manager.ingest()
    print("✅ Completed\n")

scheduler = BlockingScheduler()

# Run every 10 minutes
scheduler.add_job(job, 'interval', minutes=10)

print("🟢 Scheduler started...")
scheduler.start()


# # main.py

# from core.agent_manager import AgentManager

# manager = AgentManager()

# # Step 1: Collect + classify news
# manager.ingest()

# # Step 2: User query
# # while True:
# #     q = input("\nAsk something: ")
# #     print("\n", manager.handle_query(q))