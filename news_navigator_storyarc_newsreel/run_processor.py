import time
from ingestion.processor import process_news

while True:
    print("🚀 Processing new news...")

    process_news()

    print("✅ Done. Waiting...")
    
    time.sleep(60*4)  # every 4 minute

# from ingestion.processor import process_news

# process_news()
# print("✅ Vector index built")