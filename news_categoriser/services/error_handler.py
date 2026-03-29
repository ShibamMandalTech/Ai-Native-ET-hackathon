from db.queries import increment_retry, mark_failed

def handle_error(news_id):
    increment_retry(news_id)

    # if too many retries → mark failed
    if news_id:
        mark_failed(news_id)