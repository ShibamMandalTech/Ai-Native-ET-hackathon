



from apscheduler.schedulers.background import BackgroundScheduler
from services.cluster_insight_service import generate_cluster_insights
import time


def start_scheduler():
    scheduler = BackgroundScheduler()

    # 🔥 run every 10 minutes
    scheduler.add_job(generate_cluster_insights, 'interval', minutes=10)

    scheduler.start()

    print("🚀 Cluster Intelligence Scheduler Started")

    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == "__main__":
    start_scheduler()