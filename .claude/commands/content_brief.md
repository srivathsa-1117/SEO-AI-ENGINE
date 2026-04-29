---
description: /content_brief - Generate a detailed SEO content brief from approved keywords
---

# Workflow: Content Brief Generation

## Trigger
```
/content_brief <client_name> "<target_keyword>" [--cluster-file <path>]
```
**Example:** `/content_brief acme_corp "best project management software for remote teams"`

## Objective
Analyze competitor content and produce a detailed, actionable content brief with optimized structure, LSI keywords, schema requirements, and internal link targets. Pause for user approval before drafting.

## Required Inputs
1. `<client_name>` — loads brand_kit.json
2. `<target_keyword>` — the primary keyword to target

## Step-by-Step Instructions

### Step 1: Load Context
- Read `clients/<client_name>/brand_kit.json`
- Extract: `tone`, `persona`, `cta_style`, `content_pillars`

### Step 2: SERP Analysis (Competitor Research)
- Run: `tools/serp_scraper.py --mode serp_top10 --keyword "<target_keyword>"`
- Fetches the top 5 organic ranking URLs (skipping ads and maps)
- For each URL, scrapes: word count, H2/H3 structure, main entities mentioned, FAQ questions
- Output: `.tmp/<client_name>_serp_analysis.json`

### Step 3: NLP Gap Analysis
- Run: `tools/nlp_analyzer.py --mode gap --serp-data .tmp/<client_name>_serp_analysis.json`
- Identifies: LSI keywords present in top 3 results but not in client's existing content
- Finds: Unanswered PAA questions that we can own
- Output: `.tmp/<client_name>_content_gaps.json`

### Step 4: Internal Link Opportunities
- Run: `tools/nlp_analyzer.py --mode internal_links --client <client_name> --keyword "<target_keyword>"`
- Scans the client's sitemap and existing content for relevant anchor text opportunities
- Suggests 3-5 internal links to include in the new article
- Output: `.tmp/<client_name>_internal_links.json`

### Step 5: AEO/GEO Structure Requirements
- Based on search intent (question-based = FAQ schema, guide = Article schema)
- Determine required JSON-LD schema types
- Identify 3-5 "direct answer" opportunities: short, quotable answers that LLMs will extract

### Step 6: Assemble & Present Content Brief
Present the brief in chat in this format:

```
📋 CONTENT BRIEF: "<target_keyword>"
Client: <client_name> | Est. Word Count: X-Y words

PRIMARY KEYWORD: <target_keyword>
SECONDARY KEYWORDS: [list from NLP analysis]

SUGGESTED TITLE: <H1 under 60 chars>
META DESCRIPTION: <120-160 chars>

STRUCTURE:
H1: [title]
  H2: [section 1 — covers competitor gap + PAA #1]
  H2: [section 2 — covers competitor gap + PAA #2]
    H3: [subsection]
    H3: [subsection]
  H2: [FAQ Section] — (triggers FAQ Schema)
    H3: Q1...
    H3: Q2...
  H2: [Conclusion + CTA: "<cta_style from brand_kit>"]

REQUIRED SCHEMA: Article + FAQ
INTERNAL LINKS TO INCLUDE: [3-5 links with anchor text]
EXTERNAL LINKS TO CITE: [2-3 authoritative sources]

TONE NOTES: Write as "<persona>". Use <tone> voice.
```

Then ask: **"Does this brief look good? Should I make any changes, or shall I start writing the full draft now?"**

### Step 7: Save Brief (After Approval)
- Save to: `clients/<client_name>/active_campaigns/<slug>_brief.md`

## Edge Cases
- If top-ranking pages are behind a paywall: skip that URL and use the next one.
- If no internal links are found: note it in the brief and suggest this article could be the start of a new content cluster.
