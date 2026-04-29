---
description: /keyword_research - Discover and cluster high-intent keywords for a client
---

# Workflow: Keyword Research

## Trigger
```
/keyword_research <client_name> "<seed_keyword>" [--depth broad|deep]
```
**Example:** `/keyword_research acme_corp "project management software" --depth deep`

## Objective
Build a complete keyword map with search intent labels, difficulty estimates (without paid tools), and trend data. Pause for user approval before proceeding to content brief.

## Required Inputs
1. `<client_name>` — loads brand_kit.json for negative keywords and target location
2. `<seed_keyword>` — the starting topic

## Step-by-Step Instructions

### Step 1: Load Client Context
- Read `clients/<client_name>/brand_kit.json`
- Extract: `negative_keywords`, `target_locations`, `language`, `content_pillars`

### Step 2: Google Autosuggest Scraping
- Run: `tools/serp_scraper.py --mode autosuggest --keyword "<seed_keyword>" --location <target_location>`
- Extracts all A-Z suffix suggestions (e.g. "project management software a...", "...b")
- Also scrapes: People Also Ask (PAA) questions for question-based keywords
- Output: `.tmp/<client_name>_autosuggest.json`

### Step 3: Google Trends Analysis
- Run: `tools/serp_scraper.py --mode trends --keywords <autosuggest_list>`
- Validates which keywords are rising vs. declining in interest
- Flags seasonal keywords with peak months
- Output: `.tmp/<client_name>_trends.json`

### Step 4: Competitor Keyword Gap Analysis
- Read `competitors.top_3_competitors` from brand_kit.json
- Run: `tools/serp_scraper.py --mode competitor_gap --competitors <urls> --client-url <website_url>`
- Finds keywords competitors rank for (via scraping their top pages) that the client does NOT rank for
- Output: `.tmp/<client_name>_keyword_gaps.json`

### Step 5: Filter & Cluster
- Remove all `negative_keywords` from the list
- Group keywords by search intent:
  - **Informational** (how, what, why, guide, tips)
  - **Commercial** (best, top, review, vs, compare)
  - **Transactional** (buy, price, hire, get, book)
  - **Navigational** (brand + product specific)
- Assign estimated difficulty: Low/Medium/High based on: SERP result count + presence of big-brand domains on page 1
- Output: `.tmp/<client_name>_keyword_clusters.json`

### Step 6: Present Results & Wait for Approval
Display a structured summary in chat:

```
📊 Keyword Research Complete for: <client_name>
Seed: "<seed_keyword>"

TOP OPPORTUNITIES:
┌─────────────────────────────────┬──────────┬────────────┬───────────┐
│ Keyword                         │ Intent   │ Difficulty │ Trend     │
├─────────────────────────────────┼──────────┼────────────┼───────────┤
│ best project mgmt for remote... │ Comm.    │ Low        │ Rising ↑  │
│ how to manage remote teams...   │ Info.    │ Low        │ Stable →  │
│ project management software...  │ Trans.   │ Medium     │ Stable →  │
└─────────────────────────────────┴──────────┴────────────┴───────────┘

Total keywords found: X | Filtered out (negatives): Y | Clusters: Z
```

Then ask: **"Do these keyword clusters look good? Should I build a Content Brief for the top opportunity, or do you want to make changes first?"**

### Step 7: Save Results (After Approval)
- Save approved cluster to: `clients/<client_name>/active_campaigns/keyword_clusters_<date>.json`

## Edge Cases
- If Google rate-limits the scraper: add a 5-second delay between requests and retry automatically (document this in the workflow if it happens).
- If there are fewer than 10 keywords found: broaden the search by trying 3 related seed keywords automatically.
