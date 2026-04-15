import os
import re
import time
from datetime import date
from pathlib import Path
from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.getenv("FIRECRAWL_API_KEY")

# --- Step 01: Search + scrape with Firecrawl ---

api_url = "https://api.firecrawl.dev/v2/search"

headers = {
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "query": "Chipotle investor relations press releases",
    "limit": 5,
    "scrapeOptions": {"formats": ["markdown"]}
}

response = requests.post(api_url, headers=headers, json=payload)

data = response.json()
results = data["data"]["web"]
print(f"Firecrawl returned {len(results)} results")

# --- Step 02: Save results to knowledge/raw/ ---

raw_dir = Path("knowledge/raw")
raw_dir.mkdir(parents=True, exist_ok=True)

today = date.today().isoformat()

for r in results:
    print(f"  - {r['title']}")
    print(f"    {r['url']}")
    print(f"    markdown length: {len(r.get('markdown') or '')} chars")

    slug = re.sub(r'^https?://', '', r['url'])
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', slug)
    slug = slug.strip('-')[:80]

    filename = raw_dir / f"{today}_{slug}.md"
    content = r.get('markdown') or f"Source: {r['url']}"
    filename.write_text(content, encoding="utf-8")
    print(f"    saved → {filename}")