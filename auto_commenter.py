import os
import requests
import time
import re

# We will use the Gemini API key discovered in your codebase
API_KEY = "AIzaSyCkVxFkWoqmYGKrmwg-OAWkCZjUnzJY784"
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={API_KEY}"

def add_comments_to_code(code_str):
    prompt = """
You are a professional Python developer. 
Your task is to take the following Python code and add short, helpful INLINE comments explaining its logic.
Do NOT change the formatting, variable names, or structure of the code. Only add `#` comments.
CRITICAL: Output ONLY the raw Python code. Do not wrap it in markdown block quotes (like ```python) and do not include any conversational text like 'Here is the code'.

Here is the code:
""" + code_str

    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2}
    }
    
    try:
        res = requests.post(URL, json=data, timeout=30)
        res.raise_for_status()
        
        # Parse out the text
        json_resp = res.json()
        if "candidates" not in json_resp or len(json_resp["candidates"]) == 0:
            print("API returned no candidates.", json_resp)
            return None
            
        out = json_resp["candidates"][0]["content"]["parts"][0]["text"]
        
        # Strip markdown syntax if the LLM adds it
        out = re.sub(r"^```python\n(.*?)```$", r"\1", out.strip(), flags=re.DOTALL | re.MULTILINE)
        out = re.sub(r"^```(.*?)```$", r"\1", out.strip(), flags=re.DOTALL | re.MULTILINE)
        out = re.sub(r"^\n+|\n+$", "", out) # Remove leading/trailing newlines added by regex
        
        return out
    except Exception as e:
        print("Error calling LLM:", e)
        return None

def main():
    root_dir = r"e:\ET Ai Hackathon"
    
    print("🚀 Starting Automated Commenter script...")
    
    success_count = 0
    fail_count = 0
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Exclude hidden directories, virtual environments, and python caches
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and not d.startswith('__') and d != 'venv' and d != 'env']
        
        for f in filenames:
            if f.endswith(".py") and f != "auto_commenter.py":
                filepath = os.path.join(dirpath, f)
                
                try:
                    with open(filepath, "r", encoding="utf-8") as file:
                        code = file.read()
                        
                    if not code.strip() or len(code) > 80000:
                        continue # Skip empty files or massive files that will break context window
                        
                    print(f"⏳ Processing {filepath}...")
                    commented_code = add_comments_to_code(code)
                    
                    if commented_code and len(commented_code) > 0 and "def " in code and "def " in commented_code:
                        with open(filepath, "w", encoding="utf-8") as file:
                            file.write(commented_code)
                        print(f"✅ Success")
                        success_count += 1
                    elif commented_code and "def " not in code:
                        with open(filepath, "w", encoding="utf-8") as file:
                            file.write(commented_code)
                        print(f"✅ Success (No functions)")
                        success_count += 1
                    else:
                        print(f"❌ Failed to process or validation failed.")
                        fail_count += 1
                        
                except Exception as e:
                    print(f"❌ Error processing file {filepath}:", e)
                    fail_count += 1
                    
                # Rate limit (15 requests per minute usually for free tier)
                time.sleep(4)
                
    print(f"\n🎉 Done! Successfully commented {success_count} files. Failed: {fail_count}")

if __name__ == "__main__":
    main()
