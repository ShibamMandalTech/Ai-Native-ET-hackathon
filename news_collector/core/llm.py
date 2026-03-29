

import requests
import json
import re
import time

# 🔐 API KEYS (use env in real project)
GROQ_API_KEY = "apikey"
GEMINI_API_KEY = "apikey"

OLLAMA_URL = "http://localhost:11434/api/generate"


# =========================
# 🔥 GROQ
# =========================
def call_groq(prompt):
    print("\n🚀 [Groq] Sending request...")
    print("📩 Prompt:", prompt[:100])

    # (rate control)
    time.sleep(3)

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",  # hide full key
        "Content-Type": "application/json"
    }

    data = {
        # "model": "llama3-70b-8192",
        # "model": "mixtral-8x7b-32768",
        # "model": "llama3-8b-8192",
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data, timeout=10)

    print("📡 Status Code:", response.status_code)

    if response.status_code != 200:
        print("❌ Groq Error:", response.text)
        raise Exception("Groq API failed")

    result = response.json()

    output = result["choices"][0]["message"]["content"]
    print("✅ Groq Response:", output[:100])

    return output


# =========================
# 🌐 GEMINI
# =========================
def call_gemini(prompt):
    print("\n🌐 [Gemini] Sending request...")
    print("📩 Prompt:", prompt[:100])

    # url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"
    # url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.0-pro:generateContent?key={GEMINI_API_KEY}"
    # url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    # url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"




    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    response = requests.post(url, json=data, timeout=10)

    print("📡 Status Code:", response.status_code)

    if response.status_code != 200:
        print("❌ Gemini Error:", response.text)
        raise Exception("Gemini API failed")

    result = response.json()

    output = result["candidates"][0]["content"]["parts"][0]["text"]
    print("✅ Gemini Response:", output[:100])

    return output


# =========================
# 🖥️ OLLAMA
# =========================
def call_ollama(prompt, model="mistral"):
    print("\n🖥️ [Ollama] Sending request...")
    print("📩 Prompt:", prompt[:100])
    print("🤖 Model:", model)

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=10
        )

        print("📡 Status Code:", response.status_code)

        if response.status_code != 200:
            print("❌ Ollama Error:", response.text)
            raise Exception("Ollama error")

        result = response.json()
        output = result.get("response", "")

        print("✅ Ollama Response:", output[:100])

        return output

    except Exception as e:
        print("❌ Ollama Exception:", str(e))
        raise Exception("Ollama not available")


# =========================
# 🧠 MAIN ROUTER
# =========================
def ask_llm(prompt, mode="auto"):
    print("\n==============================")
    print("🧠 LLM REQUEST START")
    print("⚙️ Mode:", mode)
    print("==============================")

    # 🔥 MANUAL CONTROL
    if mode == "groq":
        print("➡️ Using Groq (manual)")
        return call_groq(prompt)

    if mode == "gemini":
        print("➡️ Using Gemini (manual)")
        return call_gemini(prompt)

    if mode == "ollama":
        print("➡️ Using Ollama (manual)")
        return call_ollama(prompt)

    # 🔥 AUTO MODE
    try:
        print("➡️ Trying Groq...")
        return call_groq(prompt)

    except Exception as e:
        print("⚠️ Groq failed → Gemini")
        print("🔍 Error:", str(e))

        try:
            return call_gemini(prompt)

        except Exception as e:
            print("⚠️ Gemini failed → Ollama")
            print("🔍 Error:", str(e))

            try:
                return call_ollama(prompt)

            except Exception as e:
                print("❌ All LLMs failed")
                print("🔍 Final Error:", str(e))
                return "❌ All LLMs failed"


# =========================
# 🧹 JSON CLEANER
# =========================
def clean_json(text):
    print("\n🧹 Cleaning JSON...")

    try:
        parsed = json.loads(text)
        print("✅ Direct JSON parsed")
        return parsed
    except:
        print("⚠️ Direct parse failed, trying extraction...")

    matches = re.findall(r"\{.*?\}|\[.*?\]", text, re.DOTALL)

    for match in matches:
        try:
            cleaned = match.replace("\\", "\\\\")
            parsed = json.loads(cleaned)
            print("✅ Extracted JSON parsed")
            return parsed
        except:
            continue

    print("❌ JSON parsing failed")
    print("📄 Raw:", text[:200])

    return {}


# # core/llm.py

# import requests
# import json
# import re

# OLLAMA_URL = "http://localhost:11434/api/generate"

# def ask_llm(prompt, model="mistral"):
#     response = requests.post(
#         OLLAMA_URL,
#         json={
#             "model": model,
#             "prompt": prompt,
#             "stream": False
#         }
#     )

#     result = response.json()
#     return result["response"]



# def clean_json(text):
#     try:
#         return json.loads(text)
#     except:
#         pass

#     # 🔥 Step 1: Extract JSON block
#     matches = re.findall(r"\{.*?\}|\[.*?\]", text, re.DOTALL)

#     for match in matches:
#         try:
#             # 🔥 Fix invalid escapes
#             cleaned = match.replace("\\", "\\\\")

#             return json.loads(cleaned)
#         except:
#             continue

#     # 🔥 Step 2: fallback
#     print("⚠️ JSON parsing failed. Raw output:\n", text[:300])
#     return []


# # # 🔥 ADD THIS HERE
# # def clean_json(text):
# #     try:
# #         return json.loads(text)
# #     except:
# #         match = re.search(r"\{.*\}", text, re.DOTALL)
# #         if match:
# #             return json.loads(match.group())
# #         return {}