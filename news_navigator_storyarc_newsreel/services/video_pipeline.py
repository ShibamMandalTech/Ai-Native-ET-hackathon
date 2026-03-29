from agents.selector_agent import select_video_news
from agents.script_agent import generate_script
from agents.voice_agent import generate_voice
from agents.visual_agent import generate_visuals
from agents.video_agent import create_video
from agents.engagement_agent import log_engagement


def run_pipeline(cursor, conn, user_id=1, user_type="General Audience"):
    articles = select_video_news(cursor=cursor, user_id=user_id, top_k=5, user_type=user_type)
    conn.commit()  # <--- CRITICAL: Release the row locks from the SELECT stage immediately before launching the heavy 15-second LLM processing, avoiding thread deadlock!

    for article in articles:
        try:
            news_id = article["news_id"]
            print(f"Processing ({user_type}):", article["title"])

            #  SCRIPT
            script = generate_script(article, is_live=True, user_type=user_type)

            cursor.execute(
                "UPDATE news SET video_status='SCRIPTED' WHERE id=%s",
                (news_id,)
            )
            conn.commit()

            #  AUDIO
            audio = generate_voice(script, str(news_id))

            cursor.execute(
                "UPDATE news SET video_status='AUDIO_DONE' WHERE id=%s",
                (news_id,)
            )
            conn.commit()

            #  VISUALS
            images = generate_visuals(script, news_id)

            cursor.execute(
                "UPDATE news SET video_status='VISUAL_DONE' WHERE id=%s",
                (news_id,)
            )
            conn.commit()

            #  VIDEO
            video = create_video(images, audio, news_id)

            #  IMPORTANT FIX: SAVE video_path
            cursor.execute(
                "UPDATE news SET video_status='VIDEO_CREATED', video_path=%s WHERE id=%s",
                (video, news_id)
            )
            conn.commit()

            #  ENGAGEMENT
            log_engagement(cursor, user_id, news_id, 60, True, article.get("category", "General"))
            conn.commit()

            print(" Video created:", video)

        except Exception as e:
            print(" Error:", e)

            cursor.execute(
                "UPDATE news SET video_status='FAILED' WHERE id=%s",
                (article["news_id"],)
            )
            conn.commit()