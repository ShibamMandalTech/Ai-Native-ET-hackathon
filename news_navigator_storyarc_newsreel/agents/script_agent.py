from llm.groq_client import call_groq
import re

def generate_script(article, is_live=False, user_type="General Audience"):
    summary = " ".join(article.get("summary", [])[:5])
    content = " ".join(article.get("content", [])[:3])

    prompt = f"""
Create a short vertical news video script.

Title: {article['title']}

Summary:
{summary}

Details:
{content}

Instructions:
- Write ONLY the exact spoken words for the voiceover.
- DO NOT INCLUDE any labels like "Narrator:", "Scene 1:", "Title:", "Host:", "Visuals:", "[Music]".
- Separate each slide's text with a double newline (a blank line).
- Keep it short, punchy, engaging, and Reels-style.
"""

    script = call_groq(prompt)
    
    # Fallback cleanup just in case LLM outputs the bad labels
    script = re.sub(r'\[.*?\]', '', script)
    script = re.sub(r'\(.*?\)', '', script)
    clean_lines = []
    for line in script.split('\n'):
        line = re.sub(r'^\*?\*?(Scene\s*\d+|Narrator|Voiceover|Title|Visuals?|Audio|Speaker|Host)\*?\*?\s*:\s*', '', line, flags=re.IGNORECASE)
        # Also strip leading numbers like '1:' that come after 'Scene'
        line = re.sub(r'^\s*\d+\s*:\s*', '', line)
        clean_lines.append(line)
        
    return '\n'.join(clean_lines).strip()