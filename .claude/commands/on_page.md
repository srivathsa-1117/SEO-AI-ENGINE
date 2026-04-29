---
description: /on_page - Analyze and fix on-page SEO issues for specific pages
---

# Workflow: On-Page Optimization

## Trigger
```
/on_page <client_name> [--url <specific_page_url>] [--top <N>]
```
**Example:** `/on_page acme_corp --url https://acme.com/blog/remote-teams`
**Example:** `/on_page acme_corp --top 10`

## Objective
Analyze and generate a prioritized list of specific, actionable on-page fixes for one page or the client's top N pages by traffic/importance.

## Step-by-Step Instructions

### Step 1: Load Context
- Read `clients/<client_name>/brand_kit.json`
- Get `website_url`, `primary_keywords`
- Determine target URLs: specific URL provided OR top N from last crawl in `.tmp/`

### Step 2: Page DOM Analysis
- Run: `tools/on_page_analyzer.py --urls <target_urls>`
- Extracts per page:
  - `<title>` tag (length, keyword presence)
  - `<meta name="description">` (length, keyword presence)
  - H1 tag (exists? unique? contains keyword?)
  - H2/H3 structure
  - Image `alt` attributes (missing? keyword-stuffed?)
  - Word count
  - Internal links on the page (count, anchor text variety)
  - Canonical tag (correct? self-referential?)
  - Schema markup presence (any JSON-LD found?)
- Output: `.tmp/<client_name>_onpage_analysis.json`

### Step 3: Competitor Benchmark
- For each target page, find the top 3 Google results for its primary keyword
- Run: `tools/nlp_analyzer.py --mode benchmark --urls <target_urls> --keyword <primary_keyword>`
- Compare: word count, H2 count, entity coverage, FAQ presence
- Output: `.tmp/<client_name>_benchmark.json`

### Step 4: Generate Fix List
Produce a prioritized fix list sorted by impact:

**CRITICAL (Fix immediately):**
- Missing H1 tag
- Duplicate title tags across multiple pages
- No meta description
- Canonical loop (Page A → Page B → Page A)

**HIGH (Fix this week):**
- Title tag too short/long
- Primary keyword missing from title
- Images missing alt text (>20% of images)
- Word count <50% of the top competitor

**MEDIUM (Fix this month):**
- H2 structure doesn't match search intent
- No internal links pointing to this page
- Meta description missing keyword
- No schema markup

**LOW (Nice to have):**
- H3 structure improvements
- Add FAQ section for AEO
- Improve anchor text diversity

### Step 5: Generate Updated Tags
For critical title/meta issues: generate replacement suggestions:
```
PAGE: /blog/remote-teams
CURRENT TITLE: "Remote Work" (10 chars — TOO SHORT)
SUGGESTED TITLE: "Best Remote Work Tools for Distributed Teams in 2025" (52 chars ✓)

CURRENT META: [missing]
SUGGESTED META: "Discover the top remote work tools trusted by 10,000+ distributed teams. Compare features, pricing, and integrations." (118 chars ✓)
```

### Step 6: Present & Get Approval
Display the fix list and generated tags in chat.
Ask: **"Here are all the on-page fixes. Want me to help implement any of these right now, or export this as a task list?"**

## Edge Cases
- If a page returns 404 during analysis: flag it immediately as a Critical issue and skip.
- If page uses JavaScript rendering (SPA): note that the analysis may be incomplete and recommend server-side rendering.
