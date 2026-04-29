---
description: /page - Deep single-page SEO analysis with E-E-A-T, image SEO, and fix suggestions
---

# Workflow: Single-Page Deep Analysis

## Trigger
```
/page <url> [--keyword "primary keyword"]
```
**Examples:**
- `/page https://example.com/blog/best-sarees` — full page analysis
- `/page https://example.com/about --keyword "handloom brand India"` — keyword-focused

---

## When to Use This vs /audit
- Use `/audit` for a **full site overview** across many pages
- Use `/page` for **deep analysis of one specific page** — faster, more actionable for content teams

---

## Step-by-Step Instructions

### Step 1: Fetch & Parse the Page
- Run: `python tools/on_page_analyzer.py --url <url>`
- Extract: title, meta description, H1-H6 structure, word count, internal links, canonical, schema types, all images with alt attributes

### Step 2: Detect Industry Type
Check the page/site for signals (see CLAUDE.md Rule 5) and note the site type. Adjust recommendations accordingly.

### Step 3: On-Page Technical Checks

**Title Tag:**
- Length: 50-60 characters (flag if outside range)
- Primary keyword in title? (within first 60 chars)
- Unique across the site?

**Meta Description:**
- Length: 120-160 characters
- Contains a compelling CTA or value statement?
- Primary keyword present?

**Heading Structure:**
- Exactly 1 H1? Contains primary keyword?
- H2s cover key subtopics with LSI terms?
- No heading hierarchy jumps (e.g. H1 → H3 skipping H2)?

**Word Count:**
- Compare to top 3 competitors for the primary keyword
- Flag if < 50% of the top competitor's word count

**Internal Links:**
- How many internal links does this page have?
- How many internal links point TO this page from the rest of the site?
- Suggest 3 pages that should link to this one with suggested anchor text

**Canonical Tag:**
- Present? Self-referential? No canonical loops?

### Step 4: Image SEO Audit

For every image on the page check:
| Check | Pass/Fail |
|---|---|
| Has descriptive `alt` attribute | [OK] / [ERROR] |
| Served in WebP or AVIF format | [OK] / [ERROR] |
| Has `loading="lazy"` attribute | [OK] / [ERROR] |
| File size < 100KB (estimate by URL) | [OK] / [ERROR] |
| Filename is descriptive (not `img_001.jpg`) | [OK] / [ERROR] |

### Step 5: E-E-A-T Assessment
Score each dimension 1-3:
- **Experience (1-3):** First-hand knowledge signals — photos, case studies, real examples on this page
- **Expertise (1-3):** Author byline visible? Credentials mentioned? Data cited?
- **Authoritativeness (1-3):** Is content cited/linked-to from external sources?
- **Trustworthiness (1-3):** Clear author, publishing date, contact info accessible from page?

### Step 6: Schema Check
- What schema is present on this page?
- What schema is missing and appropriate for this page type?
  - Article pages → Article schema
  - Product pages → Product schema
  - Service pages → Service schema
  - Local pages → LocalBusiness schema
  - **Note:** FAQPage schema ONLY for government/healthcare sites (restricted Aug 2023)
  - **Note:** HowTo schema is deprecated (Sept 2023) — do not recommend

### Step 7: AEO/GEO Readiness (AI Search)
- Does the page answer a clear question in the first 100 words?
- Is there a direct, quotable answer to the target query?
- Does the page have an author entity clearly identified?
- Is the page likely to be cited in AI Overviews based on these signals?

### Step 8: Competitor Comparison
- Find top 3 Google results for the `--keyword` (or infer keyword from title)
- Run: `python tools/serp_scraper.py --mode top10 --keyword "<keyword>"`
- Compare: word count, H2 count, schema used, FAQ presence, estimated DA

### Step 9: Output — Prioritised Fix List

Present as a clean table:

| Priority | Item | Current State | Recommended Fix |
|---|---|---|---|
| Critical | ... | ... | ... |
| High | ... | ... | ... |
| Medium | ... | ... | ... |
| Low | ... | ... | ... |

Then generate suggested replacement title, meta description, and H1 if any need changing.

Ask: **"Want me to implement any of these fixes directly, or save this as a task list?"**

---

## Edge Cases
- If page is JavaScript-rendered (SPA/React): note that DOM analysis may be incomplete. Recommend Playwright MCP for full rendering.
- If page returns 404: flag immediately, don't continue analysis.
- If no `--keyword` is provided: infer from the page's H1 or `<title>` tag.
