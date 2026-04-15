# Save Raw Firecrawl Results Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** After the Firecrawl search, save each result as a dated markdown file in `knowledge/raw/`.

**Architecture:** Extend the existing `for r in results:` loop in `scrape_pipeline.py` with inline file-write logic. Create `knowledge/raw/` before the loop. Filename is `YYYY-MM-DD_<url-slug>.md`; content is raw markdown or a `Source:` stub when markdown is absent.

**Tech Stack:** Python stdlib only — `datetime`, `re`, `pathlib.Path` (all already imported or available).

---

### Task 1: Verify slug logic with a quick inline test

**Files:**
- Create: `test_slug.py` (throw-away verification script, deleted after use)

- [ ] **Step 1: Write the slug test**

Create `test_slug.py` at the project root:

```python
import re

def url_to_slug(url: str) -> str:
    slug = re.sub(r'^https?://', '', url)
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug[:80]

cases = [
    ("https://ir.chipotle.com/news-releases",   "ir-chipotle-com-news-releases"),
    ("https://newsroom.chipotle.com/press-releases", "newsroom-chipotle-com-press-releases"),
    ("https://ir.chipotle.com/sec-filings",      "ir-chipotle-com-sec-filings"),
]

for url, expected in cases:
    result = url_to_slug(url)
    assert result == expected, f"FAIL: {url!r} → {result!r}, expected {expected!r}"
    print(f"PASS: {result}")
```

- [ ] **Step 2: Run the test**

```bash
venv/bin/python test_slug.py
```

Expected output:
```
PASS: ir-chipotle-com-news-releases
PASS: newsroom-chipotle-com-press-releases
PASS: ir-chipotle-com-sec-filings
```

- [ ] **Step 3: Delete the test file**

```bash
rm test_slug.py
```

---

### Task 2: Implement file saving in scrape_pipeline.py

**Files:**
- Modify: `scrape_pipeline.py`

- [ ] **Step 1: Replace the contents of scrape_pipeline.py**

```python
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
```

- [ ] **Step 2: Run the script**

```bash
venv/bin/python scrape_pipeline.py
```

Expected output (dates and slugs will match today + actual URLs):
```
Firecrawl returned 5 results
  - News Releases - Chipotle Mexican Grill
    https://ir.chipotle.com/news-releases
    markdown length: 6315 chars
    saved → knowledge/raw/2026-04-15_ir-chipotle-com-news-releases.md
  ...
```

- [ ] **Step 3: Verify files exist and content looks right**

```bash
ls knowledge/raw/
```

Expected: 5 `.md` files named `2026-04-15_*.md`

```bash
head -5 knowledge/raw/2026-04-15_ir-chipotle-com-news-releases.md
```

Expected: starts with markdown content (a heading or paragraph), not a `Source:` stub.

- [ ] **Step 4: Commit**

```bash
git add scrape_pipeline.py knowledge/raw/
git commit -m "feat: save Firecrawl results as markdown files in knowledge/raw/"
```
