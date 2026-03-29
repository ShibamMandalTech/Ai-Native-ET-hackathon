from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import threading

# 🔹 Existing services (UNCHANGED)
from services.qa_service import answer_question
from services.hybrid_service import hybrid_answer
from services.cluster_service import detect_top_clusters
from story_arc.story_arc_service import generate_story_arc

# 🔹 Video pipeline
from services.video_pipeline import run_pipeline

# 🔹 DB
from db.db import get_connection

app = Flask(__name__, template_folder='template')
CORS(app)


# =========================
# 📰 TOP STORIES (UNCHANGED)
# =========================
@app.route("/top_stories", methods=["GET"])
def top_stories():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT title FROM news 
            WHERE title IS NOT NULL AND title != '' 
            ORDER BY id DESC LIMIT 3
        """)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        stories = [row["title"] for row in rows]

        if not stories:
            stories = ["Union Budget", "Latest Market Trends", "Global Event"]

        return jsonify({"top_stories": stories})

    except Exception as e:
        print("Database fetch error for top stories:", e)
        return jsonify({
            "top_stories": ["Stock Market", "Economy Updates", "Technology Innovations"]
        })


# =========================
# 🤖 ASK (UNCHANGED)
# =========================
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data["question"]

    answer = hybrid_answer(question)

    return jsonify({"answer": answer})


# =========================
# 📊 STORY ARC (UNCHANGED)
# =========================
@app.route("/story_arc", methods=["POST"])
def story_arc_api():
    data = request.json
    question = data.get("question", "")

    cluster_ids = detect_top_clusters(question)

    if cluster_ids:
        arc = generate_story_arc(cluster_ids[0], question)
    else:
        arc = generate_story_arc(None, question)

    return jsonify({"story_arc": arc})


# =========================
# 🎥 GENERATE VIDEOS (FIXED - NON BLOCKING)
# =========================
is_generating = False

@app.route("/generate_videos", methods=["POST"])
def generate_videos():
    global is_generating
    try:
        data = request.json or {}
        user_type = data.get("user_type", "General Audience")

        def background_task():
            global is_generating
            try:
                is_generating = True
                conn = get_connection()
                cursor = conn.cursor(dictionary=True)

                run_pipeline(cursor, conn, user_id=1, user_type=user_type)

                cursor.close()
                conn.close()

                print("✅ Video pipeline completed")

            except Exception as e:
                print("❌ Background video error:", e)
            finally:
                is_generating = False

        if not is_generating:
            threading.Thread(target=background_task).start()
            return jsonify({"status": "Video generation started in background"})
        else:
            return jsonify({"status": "Generation already in progress"})

    except Exception as e:
        print("Video pipeline error:", e)
        return jsonify({"error": str(e)})


# =========================
# 📱 GET VIDEOS (FIXED PATH)
# =========================
@app.route("/get_videos", methods=["GET"])
def get_videos():
    global is_generating
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, title, video_path
            FROM news
            WHERE video_status='VIDEO_CREATED'
            AND video_path IS NOT NULL
            ORDER BY id DESC
            LIMIT 100
        """)

        videos = cursor.fetchall()

        # ✅ FIX VIDEO PATH FOR FRONTEND
        valid_videos = []
        for v in videos:
            if v["video_path"]:
                file_path = os.path.join(app.root_path, v["video_path"])
                if os.path.exists(file_path):
                    filename = os.path.basename(v["video_path"])
                    v["video_path"] = f"/videos/{filename}"
                    valid_videos.append(v)
            if len(valid_videos) >= 10:
                break

        cursor.close()
        conn.close()

        return jsonify({"videos": valid_videos, "is_generating": is_generating})

    except Exception as e:
        print("Fetch videos error:", e)
        return jsonify({"videos": []})


# =========================
# 🎬 SERVE VIDEO FILES (CRITICAL)
# =========================
@app.route('/videos/<path:filename>')
def serve_video(filename):
    video_dir = os.path.join(app.root_path, 'output', 'videos')
    return send_from_directory(video_dir, filename)


# =========================
# 🖥️ FRONTEND
# =========================
@app.route("/")
def home():
    return render_template("index_main.html")

@app.route("/videos")
def videos_page():
    return render_template("index.html")

@app.route("/story_arc")
def story_arc_page():
    return render_template("story_arc.html")


# =========================
# 🚀 RUN APP
# =========================
if __name__ == "__main__":
    import os
    import threading
    import webbrowser
    import time
    import urllib.request

    def open_browser():
        # Wait until the Flask server is fully up and responding
        while True:
            try:
                urllib.request.urlopen("http://127.0.0.1:5000")
                break
            except Exception:
                time.sleep(0.5)
        
        print("\n🌍 Flask and Debugger are initialized! Opening browser...\n")
        webbrowser.open("http://127.0.0.1:5000")

    # Run the browser-opening thread only in the master process
    # so it doesn't open a new tab every time you save a file and it autoreloads
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        threading.Thread(target=open_browser, daemon=True).start()

    app.run(debug=True)





# from flask import Flask, request, jsonify
# from services.qa_service import answer_question
# from flask_cors import CORS
# from services.hybrid_service import hybrid_answer
# from services.cluster_service import detect_top_clusters
# from story_arc.story_arc_service import generate_story_arc

# # from My_ET.routes import my_et_bp

# app = Flask(__name__)
# CORS(app)

# # app.register_blueprint(my_et_bp, url_prefix='/my_et')

# from db.db import get_connection

# @app.route("/top_stories", methods=["GET"])
# def top_stories():
#     """
#     Fetches the 3 most recently added news article titles from the MySQL database.
#     This is used by the frontend to dynamically populate the 'TOP STORIES' quick-search buttons
#     on the main UI, ensuring the user always sees the most current events available.
#     """
#     try:
#         # 1. Establish database connection
#         conn = get_connection()
#         cursor = conn.cursor(dictionary=True)
        
#         # 2. Query the database for the 3 most recent rows that have a valid title
#         cursor.execute("SELECT title FROM news WHERE title IS NOT NULL AND title != '' ORDER BY id DESC LIMIT 3")
#         rows = cursor.fetchall()
        
#         # 3. Cleanup DB connections
#         cursor.close()
#         conn.close()
        
#         # 4. Extract just the title strings into a list
#         stories = [row["title"] for row in rows]
        
#         # 5. Provide fallback hardcoded stories if the database happens to be completely empty
#         if not stories:
#             stories = ["Union Budget", "Latest Market Trends", "Global Event"]
            
#         return jsonify({"top_stories": stories})
#     except Exception as e:
#         print("Database fetch error for top stories:", e)
#         # Fallback mechanism in case the database connection completely fails
#         return jsonify({"top_stories": ["Stock Market", "Economy Updates", "Technology Innovations"]})

# @app.route("/ask", methods=["POST"])
# def ask():
#     """
#     Handles standard Q&A queries from the frontend.
#     It takes a user's typed question and utilizes a Hybrid RAG (Retrieval-Augmented Generation)
#     approach to search both the Semantic Vector Database (FAISS) and standard Database 
#     to retrieve relevant context, then passes it to an LLM to generate a conversational answer.
#     """
#     # 1. Extract the JSON payload question sent by the frontend interface
#     data = request.json
#     question = data["question"]

#     # 2. Pass the question into the core hybrid_answer service logic
#     answer = hybrid_answer(question)

#     # 3. Return the AI-generated answer back to the frontend
#     return jsonify({"answer": answer})

# @app.route("/story_arc", methods=["POST"])
# def story_arc_api():
#     """
#     Handles the generation of deep, multi-dimensional 'Story Arcs'.
#     Rather than a simple answer, this endpoint groups multiple related news articles 
#     (a cluster) to formulate a comprehensive timeline, sentiment, and summary narrative.
#     """
#     data = request.json
#     question = data.get("question", "")

#     # 1. Identify which mathematical cluster of news articles best matches the user's question
#     cluster_ids = detect_top_clusters(question)

#     if cluster_ids:
#         # 2. If a specific cluster perfectly matches, generate an arc based specifically on that cluster's context
#         arc = generate_story_arc(cluster_ids[0], question)
#     else:
#         # 3. Fallback: If no single cluster dominates the match, perform a broad global vector search across all data
#         arc = generate_story_arc(None, question)
        
#     return jsonify({"story_arc": arc})



# if __name__ == "__main__":
#     app.run(debug=True)



# from flask import Flask, request, jsonify
# from services.qa_service import answer_question
# from flask_cors import CORS
# from services.hybrid_service import hybrid_answer
# from services.cluster_service import detect_top_clusters
# from story_arc.story_arc_service import generate_story_arc

# from My_ET.routes import my_et_bp

# app = Flask(__name__)
# CORS(app)

# app.register_blueprint(my_et_bp, url_prefix='/my_et')

# @app.route("/ask", methods=["POST"])
# def ask():
#     data = request.json
#     question = data["question"]
#     # cluster_id = data.get("cluster_id")  # optional

#     # answer = answer_question(question, cluster_id)

#     answer = hybrid_answer(question)

#     return jsonify({"answer": answer})

# @app.route("/story_arc", methods=["POST"])
# def story_arc_api():
#     data = request.json
#     question = data.get("question", "")

#     cluster_ids = detect_top_clusters(question)

#     if cluster_ids:
#         arc = generate_story_arc(cluster_ids[0], question)
#     else:
#         # Fallback to pure global vector retrieval if no specific cluster matches
#         arc = generate_story_arc(None, question)
        
#     return jsonify({"story_arc": arc})


# # too Persistent FAISS + Cluster Filtering

# # @app.route("/ask", methods=["POST"])
# # def ask():
# #     data = request.json
# #     question = data["question"]

# #     answer = answer_question(question)

# #     return jsonify({"answer": answer})

# if __name__ == "__main__":
#     app.run(debug=True)