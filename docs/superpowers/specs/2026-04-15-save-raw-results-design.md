# Design: Save Firecrawl Results as Markdown Files

**Date:** 2026-04-15
**Status:** Approved

## Goal

After the Firecrawl search in `scrape_pipeline.py`, save each result as a markdown file in `knowledge/raw/` so the raw content is persisted locally for downstream use.

## Approach

Inline save logic inside the existing `for r in results:` loop. No new functions, no new modules.

## Filename Format

```
knowledge/raw/YYYY-MM-DD_<url-slug>.md
```

- Date: today's date at script run time (`datetime.date.today()`)
- URL slug: derived from `r['url']` by stripping the scheme, replacing `.` and `/` with `-`, collapsing repeated dashes, and truncating to 80 characters

Example: `https://ir.chipotle.com/news-releases` → `2026-04-15_ir-chipotle-com-news-releases.md`

## File Content

| Condition | Content written |
|---|---|
| `markdown` present and non-empty | Raw markdown string as-is |
| `markdown` absent or empty string | `Source: <url>` (single line stub) |

## Directory Creation

`knowledge/raw/` is created with `Path.mkdir(parents=True, exist_ok=True)` before the loop, so the script is safe to run multiple times and on a fresh clone.

## Dependencies

No new packages. Uses only stdlib (`datetime`, `re`) and `pathlib.Path`, both already available in the script.

## What Is Not In Scope

- Deduplication (re-running will overwrite files with the same date + URL)
- Subdirectory organization by date or source
- Any metadata header in the file content
