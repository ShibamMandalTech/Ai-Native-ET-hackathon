import requests
import time
from config import GROQ_API_KEY

GROQ_API_KEY2 = "apikey"

GROQ_KEYS = [GROQ_API_KEY, GROQ_API_KEY2]

cache = {}

#  Adjust this based on your use case
MAX_PROMPT_CHARS = 12000   # prevents TPM overflow


def trim_prompt(prompt):
    if len(prompt) > MAX_PROMPT_CHARS:
        print("⚠️ Prompt too large, trimming...")
        return prompt[:MAX_PROMPT_CHARS]
    return prompt


def call_groq(prompt, retries=3, is_live=False):

    #  Cache check
    if prompt in cache:
        return cache[prompt]

    #  Trim prompt to avoid token limit crash
    prompt = trim_prompt(prompt)

    url = "https://api.groq.com/openai/v1/chat/completions"

    def make_request(api_key):
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 3000 # MAX allowed for output (leaves 5000+ for the prompt)
        }

        return requests.post(url, headers=headers, json=data, timeout=10)

    #  Loop through all keys
    for key_index, api_key in enumerate(GROQ_KEYS):

        print(f"\n Using API KEY #{key_index+1}")

        for attempt in range(retries):

            print(f" Attempt {attempt+1}")

            try:
                response = make_request(api_key)

                #  SUCCESS
                if response.status_code == 200:
                    output = response.json()["choices"][0]["message"]["content"]
                    cache[prompt] = output
                    print(" Success:", output[:100])
                    return output

                #  RATE LIMIT
                elif response.status_code == 429:
                    if is_live:
                        wait_time = 2  # Live users get a fast flat retry
                    else:
                        wait_time = 20 * (attempt + 1)  # Background tasks get exponential
                        
                    print(f" Rate limited, cooling down for {wait_time}s...")
                    time.sleep(wait_time)

                #  TOKEN TOO LARGE (YOUR MAIN ISSUE)
                elif "Requested" in response.text and "tokens" in response.text:
                    print(" Token limit exceeded, reducing prompt...")

                    # shrink prompt more aggressively
                    prompt = prompt[:int(len(prompt) * 0.7)]

                #  OTHER ERRORS
                else:
                    print(f" Error (key {key_index+1}):", response.text)
                    break  # move to next key

            except Exception as e:
                print(f" Exception (key {key_index+1}):", str(e))
                break  # move to next key

    raise Exception(" All Groq API keys failed")



