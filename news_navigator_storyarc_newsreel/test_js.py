import re

def formatDataPoints(text):
    html = re.sub(r'\*\*(.*?)\*\*', r'<span class="highlight-data">\1</span>', text)
    html = re.sub(r'(^|<li>|<br>|\s)([A-Z][\w\s]+):', r'\1<span class="highlight-data">\2:</span>', html)
    html = re.sub(r'(^|\s)(\+?\-?[$₹£€]\s?\d+(?:,\d{3})*(?:\.\d+)?(?:[kKMBT]|Cr|Lakh)?)(?=[.,\s]|$)', r'\1<span class="highlight-data">\2</span>', html, flags=re.IGNORECASE)
    html = re.sub(r'(^|\s)(\+?\-?\d+(?:\.\d+)?%)(?=[.,\s]|$)', r'\1<span class="highlight-data">\2</span>', html)
    html = re.sub(r'<span class="highlight-data">\s*<span class="highlight-data">(.*?)</span>\s*</span>', r'<span class="highlight-data">\1</span>', html)
    return html

sample = """**Summary**
This is a test summary with a - bullet point that shouldn't match.
- **Market Impact:** Massive $1.5M and 15% increase.
"""
for line in sample.split("\n"):
    print(repr(line))
    l = line.strip()
    if l.startswith("-") or l.startswith("*") or l.startswith("•") or re.match(r'^\d+\.', l):
        print(f"DATA-POINT: {formatDataPoints(l)}")
    else:
        print(f"P: {formatDataPoints(l)}")
