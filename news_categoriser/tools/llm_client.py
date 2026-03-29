import requests
import json
import re
import time


0

# 🔐 KEYS (move to config if needed)
GROQ_API_KEY = "apikey"
GROQ_API_KEY2 = "apikey"
GEMINI_API_KEY = "apikey"

OLLAMA_URL = "http://localhost:11434/api/generate"


# =========================
# 🚀 GROQ
# =========================
def call_groq(prompt):
    print("🚀 Using Groq")

    time.sleep(3)

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}]
    }

    delay=2

    
    for i in range(3):  # 🔥 retry loop
        res = requests.post(url, headers=headers, json=data, timeout=10)

        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"]

        if "rate_limit" in res.text:
            print("⏳ Rate limit hit, waiting...")
            # time.sleep(3)   # 🔥 wait before retry
            time.sleep(delay)
            delay*=2
            continue

        raise Exception(res.text)

    raise Exception("Groq failed after retries")


def call_groq2(prompt):
    print("🚀 Using Groq2")

    time.sleep(3)

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY2}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}]
    }

    delay=2

    
    for i in range(3):  # 🔥 retry loop
        res = requests.post(url, headers=headers, json=data, timeout=10)

        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"]

        if "rate_limit" in res.text:
            print("⏳ Rate limit hit, waiting...")
            # time.sleep(3)   # 🔥 wait before retry
            time.sleep(delay)
            delay*=2
            continue

        raise Exception(res.text)

    raise Exception("Groq failed after retries")

    
    
    # res = requests.post(url, headers=headers, json=data, timeout=10)

    # if res.status_code != 200:
    #     print("❌ Groq Error:", res.text)
    #     raise Exception("Groq failed")

    # return res.json()["choices"][0]["message"]["content"]


# =========================
# 🌐 GEMINI
# =========================
def call_gemini(prompt):
    print("🌐 Using Gemini")

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    res = requests.post(url, json=data, timeout=10)

    if res.status_code != 200:
        print("❌ Gemini Error:", res.text)
        raise Exception("Gemini failed")

    return res.json()["candidates"][0]["content"]["parts"][0]["text"]


# =========================
# 🖥️ OLLAMA
# =========================
def call_ollama(prompt, model="phi3"):
    print("🖥️ Using Ollama")

    try:
        res = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 200
                }
            },
            timeout=120
        )

        if res.status_code != 200:
            print("❌ Ollama Error:", res.text)
            raise Exception("Ollama failed")

        return res.json().get("response", "")

    except Exception as e:
        print("❌ Ollama Exception:", str(e))
        raise Exception("Ollama not available")


# =========================
# 🧠 MAIN ROUTER
# =========================
def call_llm(prompt, mode="auto"):
    print("\n🧠 LLM CALL START")

    # 🔥 MANUAL MODE
    if mode == "groq":
        return call_groq(prompt)

    # if mode == "groq":
    #     return call_groq2(prompt)

    if mode == "gemini":
        return call_gemini(prompt)

    if mode == "ollama":
        return call_ollama(prompt)

    # 🔥 AUTO MODE (fallback chain)
    try:
        return call_groq(prompt)

    except Exception:
        print("⚠️ Groq failed → Groq2")

        try:
            return call_groq2(prompt)
        
        except Exception:
            print("⚠️ Groq failed → Gemini")

            try:
                return call_gemini(prompt)

            except Exception:
                print("⚠️ Gemini failed → Ollama")

                try:
                    return call_ollama(prompt)

                except Exception:
                    print("❌ All LLMs failed")
                    return "❌ All LLMs failed"


# =========================
# 🧹 JSON CLEANER
# =========================
def clean_json(text):
    try:
        return json.loads(text)
    except:
        pass

    matches = re.findall(r"\{.*?\}|\[.*?\]", text, re.DOTALL)

    for match in matches:
        try:
            return json.loads(match)
        except:
            continue

    return {}







# import requests
# from config import LLM_PROVIDER, OPENAI_API_KEY


# def call_llm(prompt):
#     url = "https://api.openai.com/v1/chat/completions"

#     headers = {
#         "Authorization": f"Bearer {OPENAI_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     data = {
#         "model": "gpt-4o-mini",
#         "messages": [
#             {"role": "system", "content": "You are a news analyst."},
#             {"role": "user", "content": prompt}
#         ],
#         "temperature": 0.3
#     }

#     response = requests.post(url, headers=headers, json=data)
#     return response.json()["choices"][0]["message"]["content"]


# def call_openai(prompt):
#     url = "https://api.openai.com/v1/chat/completions"

#     headers = {
#         "Authorization": f"Bearer {OPENAI_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     data = {
#         "model": "gpt-4o-mini",
#         "messages": [
#             {"role": "system", "content": "You are a news analyst."},
#             {"role": "user", "content": prompt}
#         ],
#         "temperature": 0.3
#     }

#     response = requests.post(url, headers=headers, json=data)
#     return response.json()["choices"][0]["message"]["content"]


# def mock_llm(prompt):
#     return "• Point 1\n• Point 2\n• Point 3"