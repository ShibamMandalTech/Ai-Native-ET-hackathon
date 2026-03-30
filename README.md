#  NewsNavigator System (ET AI Hackathon)

Welcome to the **NewsNavigator ,** **StoryArc** **and NewsReels**ecosystem! This multi-agent AI system crawls, categorizes, and serves high-quality financial & news insights. It features a robust multi-LLM architecture, a dynamic Flask web dashboard, automated video generation pipelines, and local FAISS vector store searching.

##### We built an AI-native news intelligence system that transforms fragmented articles into evolving story narratives, personalized insights, and automated video briefings
#### This is NOT just News app - It's an AI-native way to understand information and personalise intelligently for user.
This is not just a news application — it is an AI-native intelligence system that transforms fragmented information into evolving story narratives, delivering personalized insights tailored to each user’s context, interests, and intent.





---
## Project Summary: News Navigator Ecosystem

The News Navigator Ecosystem is an AI-powered, multi-agent system designed to transform raw news into structured intelligence, interactive insights, and engaging multimedia experiences. Instead of treating news as isolated articles, the system organizes information into context-aware story flows, interactive briefings, and visual narratives.

The architecture is modular and distributed, with specialized agents handling collection, classification, clustering, insight generation, and content rendering.

### 1. News Navigator (Interactive News Briefings)

The News Navigator module focuses on delivering interactive and query-driven news exploration. It enables users to:
```
Perform semantic search using FAISS-based embeddings
Retrieve context-aware results instead of keyword matches
Explore news through interactive briefings, where multiple related articles are summarized and presented dynamically
```
This transforms traditional news reading into a conversational and exploratory experience, allowing users to quickly understand topics without reading dozens of articles.
- ![WebPage](/news_brief1.jpeg)
![WebPage](/news_brief2.jpeg)
- ![WebPage](/news_brief3.jpeg)
![WebPage](/news_brief4.jpeg)

---
### 2. StoryArc (Cluster Intelligence Engine)

StoryArc is the intelligence layer responsible for identifying and tracking evolving news stories.
```
Groups related articles into semantic clusters
Maintains cluster state over time (story evolution)
Generates:
Summaries
Timelines
Key insights
```
Unlike simple aggregation, StoryArc provides a holistic view of an event, showing how a story develops across sources and time.
- ![WebPage](/Story_arc1.jpeg)
![WebPage](/Story_arc2.jpeg)

---
### 3. Video Intelligence Pipeline

The Video Intelligence module converts structured news clusters into AI-generated videos:
```
Selects important clusters
Generates scripts using LLMs
Produces voiceovers via TTS
Creates visuals using image APIs
Combines everything using FFmpeg/MoviePy
```
This enables automated, scalable news storytelling in video format, making content more engaging and accessible.
- ![WebPage](/News_Reels.jpeg)

---
### Unique Data Storage Architecture

A key innovation of the system is its hybrid storage design, optimized for AI workloads:
```
MySQL (Relational Layer)
    Stores structured entities like articles, clusters, insights, and video metadata.
FAISS (Vector Layer)
    Stores embeddings for semantic similarity search, enabling fast and intelligent retrieval.
State Files (JSON)
    Tracks cluster evolution (cluster_state.json), allowing incremental updates without recomputation.
Filesystem (Media Storage)
    Handles large video/audio/image files efficiently without overloading the database.
```
---
### Why This Architecture is Powerful
```
⚡ Combines SQL + Vector Search → hybrid intelligence
🔄 Supports real-time incremental processing
🧠 Built for AI-native workflows (embeddings, clustering)
📊 Enables both structured queries and semantic exploration
🎥 Efficient handling of large-scale media generation
🌍 Vision
```
---
### The system redefines news consumption by moving from article-based reading to:

Interactive briefings (News Navigator)
Story-level understanding (StoryArc)
Multimedia storytelling (Video Intelligence)

Together, these create a complete AI-driven news experience that is intelligent, contextual, and engaging.

## 🛠 Prerequisites

Before running the project natively, ensure your machine meets the following environment requirements:

1. **Python 3.8+**: Make sure Python is added to your Windows `PATH`.
2. **MySQL Server**: Ensure you have a local or hosted MySQL instance running, as the application relies on an active SQL database to store incoming news and system metadata.
3. **Ollama (Optional but Recommended)**: If you intend to use local LLM fallback mechanisms when cloud models fail (as defined in the code), you need the [Ollama local server](https://ollama.com/) running on port `11434`.

---
### File Structure
# 🧠 NewsNavigator & StoryArc System  
### AI-Powered Multi-Agent News Intelligence & Storytelling Platform

---

## 🚀 Overview

**NewsNavigator & StoryArc** is a modular, multi-agent AI system that:
- Collects real-time news from multiple sources  
- Categorizes and clusters similar news articles  
- Generates summaries (short, deep, timeline-based)  
- Converts news into interactive stories, scripts, and videos  

The system is designed for scalability, automation, and intelligent storytelling.

---

## 🏗️ System Architecture

The system is divided into three core subsystems:

### 1️⃣ News Collector (Data Ingestion)
- Scrapes news from sources  
- Uses AI agents to classify and plan queries  
- Stores raw data  

### 2️⃣ News Categoriser (Processing & Intelligence)
- Clusters similar articles  
- Generates summaries (short, deep, structured)  
- Uses FAISS for similarity search  

### 3️⃣ News Navigator & StoryArc (Output Generation)
- Creates scripts, audio, and visuals  
- Generates story timelines  
- Produces video/news reels

- ![System Architecture](/architecture1.png)
- ![News_Processing_Pipeline](/News_processing_pipeline.png)
- ![Deployment Architecture](/Deployment_architecture.png)
- ![Error handling](/Error_handling.png)

---

## 📁 Project Structure

```
ET Ai Hackathon/
│
├── cluster_state.json
├── faiss_index.bin
├── metadata.pkl
├── requirements.txt
├── requirments.txt
├── run_all.bat
├── extra/
│
├── news_categoriser/
│   ├── categoriser_main.py
│   ├── config.py
│   ├── requirments.txt
│   │
│   ├── agents/
│   │   ├── cluster_agent.py
│   │   ├── decision_agent.py
│   │   ├── deep_agent.py
│   │   ├── short_agent.py
│   │   ├── summary_agent.py
│   │
│   ├── db/
│   │   ├── connection.py
│   │   ├── queries.py
│   │
│   ├── services/
│   │   ├── error_handler.py
│   │   ├── executor.py
│   │
│   ├── tools/
│       ├── llm_client.py
│       ├── scraper.py
│
├── news_collector/
│   ├── collector_main.py
│   ├── worker.py
│   │
│   ├── agents/
│   │   ├── classifier_agent.py
│   │   ├── collector_agent.py
│   │   ├── planner_agent.py
│   │   ├── query_agent.py
│   │   ├── response_agent.py
│   │   ├── search_agent.py
│   │
│   ├── core/
│   │   ├── agent_manager.py
│   │   ├── llm.py
│   │
│   ├── tools/
│       ├── db.py
│       ├── scraper.py
│       ├── storage.py
│
├── news_navigator_storyarc_newsreel/
│   ├── app.py
│   ├── config.py
│   ├── scheduler.py
│   ├── scheduler2.py
│   ├── run_processor.py
│   ├── run_cluster_insights.py
│   ├── test.py
│   ├── test_js.py
│   ├── test_pipeline.py
│   ├── check_videos.py
│   ├── check_videos_quick.py
│   │
│   ├── cluster_state.json
│   ├── faiss_index.bin
│   ├── metadata.pkl
│   ├── requirments.txt
│   │
│   ├── agents/
│   │   ├── engagement_agent.py
│   │   ├── personalization_agent.py
│   │   ├── script_agent.py
│   │   ├── selector_agent.py
│   │   ├── video_agent.py
│   │   ├── visual_agent.py
│   │   ├── voice_agent.py
│   │
│   ├── db/
│   │   └── db.py
│   │
│   ├── ingestion/
│   │   ├── chunker.py
│   │   ├── embedder.py
│   │   ├── processor.py
│   │
│   ├── llm/
│   │   └── groq_client.py
│   │
│   ├── output/
│       ├── audio/
│       ├── images/
│
└── .vscode/
    └── settings.json
```

---

## 🤖 Multi-Agent Architecture

The system uses specialized AI agents:

### Collector Agents
- Query generation  
- Search & scraping  
- Response validation  

### Categoriser Agents
- Clustering articles  
- Generating summaries  
- Decision making  

### StoryArc Agents
- Script generation  
- Voice synthesis  
- Visual generation  
- Engagement optimization  

---

## 🔄 Workflow Pipeline

```
News Sources
   ↓
Collector Agents
   ↓
Raw Articles Database
   ↓
Categoriser Agents
   ↓
Clustered + Summarized Data
   ↓
StoryArc Agents
   ↓
Scripts → Audio → Visuals
   ↓
Final News Reel / Insights
```

---

## 🛠️ Technologies Used

- Python  
- FAISS  
- LLMs (Groq / OpenAI-compatible)  
- Web Scraping  
- Flask / Scheduler  
- Multi-Agent Systems  

---

## ⚙️ Installation

```bash
git clone <your-repo-url>
cd ET Ai Hackathon
pip install -r requirements.txt
```

Also install:
```
news_categoriser/requirments.txt
news_navigator_storyarc_newsreel/requirments.txt
```

---

## ▶️ Running the Project

### Run Full Pipeline
```bash
run_all.bat
```

### Run Individually

Collector:
```bash
cd news_collector
python collector_main.py
```

Categoriser:
```bash
cd news_categoriser
python categoriser_main.py
```

StoryArc:
```bash
cd news_navigator_storyarc_newsreel
python app.py
```

---

## 📊 Features

- Multi-agent AI architecture  
- News clustering using embeddings  
- FAISS-based similarity search  
- Short + deep summaries  
- Timeline-based storytelling  
- Audio + visual generation  
- Automated scheduling  

---

## ⚠️ Known Issues

- Duplicate requirements file naming  
- Temporary audio files not cleaned  
- .pyc files should be ignored  

---

## 🔮 Future Improvements

- Docker support  
- Real-time dashboard  
- Personalization engine  
- Microservices architecture  

---



## ⭐ Contributing

Feel free to fork and contribute!
---

##  Installation & Setup

### 1. Install Dependencies
Open standard Terminal / Command Prompt in the project's root directory:
```bash
# It is recommended to create a virtual environment first, but not strictly required
python -m venv venv
venv\Scripts\activate

# Install the dependencies from the requirements file
pip install -r requirments.txt 
```
*(Note the exact spelling of `requirments.txt` native to the repository).*

### 2. Configure API Keys
You **must** configure your API keys for the LLMs to function properly. The codebase uses hardcoded keys which are currently sanitized as `"apikey"`.
Please hunt down the following files and replace `"apikey"` with your valid **Groq** and **Gemini** credentials:
* `news_categoriser/tools/llm_client.py`
* `news_collector/core/llm.py`
* `news_navigator_storyarc_newsreel/llm/groq_client.py`
* `news_navigator_storyarc_newsreel/config.py`

### 3. Database Configuration
Make sure your MySQL server is running. Ensure you have the corresponding database and tables created as expected by the `db_config` in the respective `db/connection.py` modules.

---

##  Running the Application (Windows)

The simplest and most effective way to start the entire ecosystem is utilizing the provided Batch script. Since the architecture utilizes multiple disconnected processing loops (collectors, categorisers, schedulers, UI), the `.bat` file handles spawning concurrent terminal windows automatically.

1. Navigate to the root folder: `e:\ET Ai Hackathon\`
2. Double-click the **`run_all.bat`** file from File Explorer, or run it through the command line:
   ```cmd
   .\run_all.bat
   ```

### What `run_all.bat` Does:
The batch script will launch 7 independent CMD windows running the following micro-services in parallel:
- **News Collector**: `collector_main.py` & `worker.py` (Scrapes and queues news)
- **News Categoriser**: `categoriser_main.py` (Parses structure and inserts into the vector DB)
- **StoryArc Scheduler**: `run_processor.py`, `scheduler.py`, & `scheduler2.py` (Maintains vector embeddings and automated triggers)
- **Flask Application**: `app.py` (The main webserver!)

### Accessing the UI
Once the components are running, the web frontend will be served locally. 
- Open your browser and navigate to: **`http://127.0.0.1:5000`** 
- *Note: `app.py` is configured to attempt auto-launching this URL in your default browser once initialized.*

---

##  Stopping the Application
Because `run_all.bat` spawns multiple independent CMD instances, stopping the project requires you to **close all 7 popup CMD windows** manually. Do not leave the schedulers or workers running silently in the background if you are actively editing SQLite/FAISS DB files.

---
## 👨‍💻 Author

Shibam Mandal  
B.Tech Computer Science and Engineering (Internet of Things and Cybersecurity including Blockchain Technology) | AI Systems Developer  


