---
description: /competitor_gap - Find low-hanging fruit keywords that competitors rank for but the client doesn't
---

# Workflow: Competitor Keyword Gap Analysis

## Trigger
```
/competitor_gap <client_name>
```
**Example:** `/competitor_gap acme_corp`

## Objective
Identify high-value, "low-hanging fruit" keywords. These are keywords where top competitors are getting organic traffic, but the client's website does not currently rank in the top 100 results. 

## When to Use
Use this in Month 2+ of a client engagement to build the content calendar. It removes guesswork by writing content the market is actively searching for.

---

## Step-by-Step Instructions

### Step 1: Load Competitors
- Read `clients/<client_name>/brand_kit.json`
- Extract the client's `website_url` and the list of `competitors`.
- If no competitors are listed, ask the user: *"I need at least 2 competitor URLs to run a gap analysis. Who are their main organic competitors?"*

### Step 2: Run Gap Analysis
- Run: `python tools/competitor_gap.py --client <client_name>`
- This script simulates pulling search data (or uses the DataForSEO MCP if configured) and identifies keywords with Volume > 1000 and Keyword Difficulty (KD) < 35.

### Step 3: Present Findings
Structure the output elegantly in a Markdown table.
Only show the **"Low-Hanging Fruit"** in the chat summary.

| Target Keyword | Monthly Volume | KD (Difficulty) | Competitor Rank |
|---|---|---|---|
| {keyword} | {volume} | {kd} | {comp_rank} |

### Step 4: Topic Clustering
- Output the top 50 keywords from the gap analysis into a temporary text file: `.tmp/keywords_to_cluster.txt`.
- Run: `python tools/keyword_clusterer.py --input .tmp/keywords_to_cluster.txt --output .tmp/clusters.json`
- This uses NLP machine learning to group the random keywords into **Topical Clusters** (e.g., all "silk" keywords grouped, all "sustainable" keywords grouped).

### Step 5: Actionable Recommendation
Show the user the detected Topical Clusters from Step 4.

Ask the user: 
**"Here is the keyword gap analysis and the recommended Topical Clusters to attack. Should I generate a Content Brief (`/content_brief`) for the first cluster, or save this list to their reports folder?"**

---

## Edge Cases
- **No Data:** If the gap analysis finds zero keywords (often true for strictly local brick-and-mortar stores), inform the user that a Competitor Gap is the wrong strategy for this client. Recommend Local SEO and Google Business Profile (GBP) posting instead.
