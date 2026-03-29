@echo off
echo Starting all Python scripts in parallel...

start "collector_main" /D "E:\ET Ai Hackathon\news_collector" cmd /k python collector_main.py
start "worker" /D "E:\ET Ai Hackathon\news_collector" cmd /k python worker.py
start "categoriser_main" /D "E:\ET Ai Hackathon\news_categoriser" cmd /k python categoriser_main.py
start "run_processor" /D "E:\ET Ai Hackathon\news_navigator_storyarc_newsreel" cmd /k python run_processor.py
start "scheduler" /D "E:\ET Ai Hackathon\news_navigator_storyarc_newsreel" cmd /k python scheduler.py
start "scheduler2" /D "E:\ET Ai Hackathon\news_navigator_storyarc_newsreel" cmd /k python scheduler2.py
start "app" /D "E:\ET Ai Hackathon\news_navigator_storyarc_newsreel" cmd /k python app.py

echo All processes started!
