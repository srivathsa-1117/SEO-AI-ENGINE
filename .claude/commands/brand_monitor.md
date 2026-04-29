---
description: /brand_monitor - Monitor high-quality brand mentions and reviews across the web
---

# /brand_monitor

Initiate the brand health workflow.

**Action**: When invoked, trigger the detailed process found in `workflows/brand_monitor.md`.

Use `tools/brand_mention_tracker.py` to crawl the web for recent unlinked and linked brand mentions (ignoring the brand's own domain).
Use `tools/review_aggregator.py` to pull review data, velocity, and sentiment analysis.
Compile the results into a structured brand health report for the client, detailing their AI Engine citability based on their presence on tier-1 domains (Reddit, Quora, News, etc.).
