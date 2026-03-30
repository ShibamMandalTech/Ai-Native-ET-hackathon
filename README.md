#  NewsNavigator System (ET AI Hackathon)

Welcome to the **NewsNavigator** and **StoryArc** ecosystem! This multi-agent AI system crawls, categorizes, and serves high-quality financial & news insights. It features a robust multi-LLM architecture, a dynamic Flask web dashboard, automated video generation pipelines, and local FAISS vector store searching.

---

## 🛠 Prerequisites

Before running the project natively, ensure your machine meets the following environment requirements:

1. **Python 3.8+**: Make sure Python is added to your Windows `PATH`.
2. **MySQL Server**: Ensure you have a local or hosted MySQL instance running, as the application relies on an active SQL database to store incoming news and system metadata.
3. **Ollama (Optional but Recommended)**: If you intend to use local LLM fallback mechanisms when cloud models fail (as defined in the code), you need the [Ollama local server](https://ollama.com/) running on port `11434`.

---
### File Structure
ET Ai Hackathon/
│
├── cluster_state.json
├── faiss_index.bin
├── metadata.pkl
├── requirements.txt
├── requirments.txt
├── run_all.bat
├── extra/
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
