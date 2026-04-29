---
description: /content_brief - Generate a detailed SEO content brief from approved keywords with full tool orchestration
---

# Workflow: Content Brief Generation

## Trigger
```
/content_brief <client_name> "<target_keyword>" [--cluster-file <path>]
```
**Example:** `/content_brief acme_corp "best project management software for remote teams"`

---

## Objective
Analyze competitor content and produce a detailed, actionable content brief with optimized structure, LSI keywords, schema requirements, and internal link targets. Pause for user approval before drafting.

---

## Required Inputs
1. `<client_name>` — loads `clients/<client_name>/brand_kit.json`
2. `<target_keyword>` — the primary keyword to target
3. `[--cluster-file]` — Optional: Path to keyword cluster file from `/keyword_research`

---

## Step-by-Step Execution

### Step 1: Load Client Context

**Execute:**
```bash
# Read brand kit
Read: clients/<client_name>/brand_kit.json
```

**Extract required fields:**
```json
{
  "tone": "professional | conversational | authoritative | casual",
  "persona": "who the brand speaks as",
  "cta_style": "Book a Call | Download Guide | Get Started",
  "content_pillars": ["pillar1", "pillar2", "pillar3"],
  "target_audience": "who we're writing for",
  "primary_keywords": ["keyword1", "keyword2"],
  "secondary_keywords": ["keyword3", "keyword4"]
}
```

**Validate:**
```bash
# Check if brand_kit.json exists
if [ ! -f "clients/{client}/brand_kit.json" ]; then
  echo "[ERROR] Client not found. Run /add_client first."
  exit 1
fi
```

**If field is missing:**
- `tone` → default to "professional"
- `cta_style` → default to "Learn More"
- `content_pillars` → use primary_keywords as pillars

---

### Step 2: SERP Analysis — Competitor Research

**Tool:** `serp_scraper.py` (mode: serp_top10)

**Execute:**
```bash
python tools/serp_scraper.py \
  --mode serp_top10 \
  --keyword "{target_keyword}" \
  --output ".tmp/{client}_serp.json"
```

**What this does:**
- Fetches top 10 organic results for the keyword (skips ads/maps)
- For each URL, scrapes: word count, H2/H3 structure, main entities, FAQ questions
- Returns JSON with competitor content intelligence

**Validate output:**
```bash
# Check file exists
if [ ! -f ".tmp/{client}_serp.json" ]; then
  echo "[ERROR] SERP scrape failed"
  # Fallback: WebSearch for manual analysis
fi

# Check has minimum 3 results
# Use Read tool to parse JSON:
# if len(data["results"]) < 3:
#   Fallback: WebSearch + manual parse
```

**Parse results:**
```json
{
  "keyword": "best project management software",
  "results": [
    {
      "url": "https://competitor1.com/article",
      "title": "...",
      "word_count": 2500,
      "h2_headings": ["What is...", "Top 10 tools", "How to choose"],
      "h3_headings": ["Asana", "Monday.com", "Trello"],
      "entities_mentioned": ["Asana", "project management", "team collaboration"],
      "faq_questions": ["What is the best free PM tool?", "How much does Asana cost?"]
    },
    ...
  ]
}
```

**If tool fails (rate limited or blocked):**
1. Wait 30 seconds, retry once
2. If still fails: Use WebSearch tool, manually fetch top 5 URLs
3. Use WebFetch on each URL to extract H2/H3 structure manually
4. Document: "[WARNING] SERP scraper unavailable, used manual analysis"

**Analyze competitors:**
- Average word count (median of top 5)
- Common H2 patterns (what topics they all cover)
- Unique angles (what only 1-2 competitors cover)
- FAQ patterns (common questions asked)

---

### Step 3: NLP Gap Analysis — Find Content Opportunities

**Tool:** `nlp_analyzer.py` (mode: gap)

**Execute:**
```bash
python tools/nlp_analyzer.py \
  --mode gap \
  --serp-data ".tmp/{client}_serp.json" \
  --output ".tmp/{client}_content_gaps.json"
```

**What this does:**
- Identifies LSI keywords present in top 3 results but NOT in client's existing content
- Finds unanswered PAA (People Also Ask) questions we can own
- Extracts semantic keyword clusters

**Validate output:**
```bash
# Check file exists
if [ ! -f ".tmp/{client}_content_gaps.json" ]; then
  echo "[ERROR] NLP analysis failed"
  # Fallback: Manual keyword extraction from SERP data
fi
```

**Parse results:**
```json
{
  "lsi_keywords": [
    "team collaboration tools",
    "remote work software",
    "project tracking",
    "kanban boards"
  ],
  "unanswered_paa": [
    "What is the easiest project management tool?",
    "Can you use PM software for free?"
  ],
  "semantic_clusters": {
    "features": ["kanban", "gantt chart", "time tracking"],
    "use_cases": ["remote teams", "agencies", "startups"]
  }
}
```

**If tool fails:**
- Fallback: Manually extract keywords from SERP data
- Use WebSearch for "people also ask {target_keyword}" and scrape questions
- Document: "[WARNING] NLP tool unavailable, manually identified LSI keywords"

---

### Step 4: Internal Link Opportunities

**Tool:** `nlp_analyzer.py` (mode: internal_links)

**Execute:**
```bash
python tools/nlp_analyzer.py \
  --mode internal_links \
  --client "{client}" \
  --keyword "{target_keyword}" \
  --output ".tmp/{client}_internal_links.json"
```

**What this does:**
- Scans client's sitemap and existing content
- Finds relevant pages to link to from the new article
- Suggests anchor text based on keyword relevance

**Validate output:**
```bash
if [ ! -f ".tmp/{client}_internal_links.json" ]; then
  echo "[WARNING] No existing content found for internal links"
  # This is OK for new clients
fi
```

**Parse results:**
```json
{
  "internal_links": [
    {
      "target_url": "/blog/agile-project-management",
      "anchor_text": "agile project management methodology",
      "relevance_score": 0.85
    },
    {
      "target_url": "/services/team-collaboration",
      "anchor_text": "team collaboration solutions",
      "relevance_score": 0.72
    }
  ]
}
```

**If no internal links found:**
- This is normal for new clients or new content pillars
- Note in brief: "This article will start a new content cluster"
- Recommend creating 2-3 supporting articles after this pillar piece

---

### Step 5: AEO/GEO Structure Requirements

**Reference:** Rule 16 from CLAUDE.md (FAQ & Conclusion Standards)

**Determine required structural blocks:**

**5a. TL;DR / Key Takeaways**
- Identify 3-5 punchy insights from competitor analysis
- Place at top of article (before TOC)
- Format: Bulleted list, 1 sentence each
- Purpose: Helps AI extract quick answers

**5b. Table of Contents Anchors**
- Define exact jump-link IDs for each H2/H3
- Format: `#what-is-project-management` (lowercase, hyphenated)
- Ensures users can jump to sections (UX + SEO)

**5c. FAQ Section Requirements**
**Reference Rule 16 from CLAUDE.md:**
- **Maximum 5-8 FAQs** (never exceed 10)
- Each answer: **50-150 words** (2-3 sentences max)
- Focus on **high-intent, conversion-driving** questions
- DO NOT repeat content already thoroughly covered in main article
- Questions should come from PAA (People Also Ask) or real user searches

**5d. Conclusion Requirements**
**Reference Rule 16 from CLAUDE.md:**
- Length: **100-150 words exactly**
- Structure:
  1. One-sentence recap of core value
  2. Clear next action step
  3. Strong CTA with action verb (Book, Download, Start, Get, Schedule)
  4. Hyperlinked CTA pointing to conversion page
- **NEVER:**
  - Summarize the article (reader already read it)
  - Use "In conclusion" or "To summarize"
  - End without a clear, clickable CTA
  - Make it longer than 150 words

**5e. Schema Type Selection**
- Article schema (MANDATORY for all blog posts)
- FAQ schema (ONLY if we have FAQ section)
- [ERROR] NEVER HowTo schema (deprecated Sept 2023)
- [ERROR] NEVER FAQPage schema for commercial sites (restricted to gov/healthcare)

**Determine schema as JSON-LD @graph:**
```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "headline": "{title}",
      "author": {"@type": "Person", "name": "..."},
      "datePublished": "{date}",
      "description": "{meta_description}"
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "...",
          "acceptedAnswer": {"@type": "Answer", "text": "..."}
        }
      ]
    }
  ]
}
```

---

### Step 6: Assemble Content Brief

**Aggregate all data:**
```json
{
  "client": "{client_name}",
  "target_keyword": "{keyword}",
  "suggested_title": "{H1 under 60 chars}",
  "meta_description": "{120-160 chars with CTA}",
  "url_slug": "{primary-keyword-format}",
  "estimated_word_count": "{median of competitors + 10%}",
  "secondary_keywords": [...],
  "lsi_keywords": [...],
  "content_structure": {
    "h1": "...",
    "h2_sections": [
      {
        "heading": "What is {keyword}?",
        "purpose": "Covers competitor gap + PAA question",
        "word_count_target": 300
      },
      ...
    ]
  },
  "faq_section": [...],
  "internal_links": [...],
  "external_sources": [...],
  "schema_requirements": {...},
  "tone_notes": "Write as {persona}. Use {tone} voice."
}
```

**Save to:**
```bash
Write: .tmp/{client}_brief_{slug}.json
```

---

### Step 7: Present Brief to User

**Output in chat:**

```markdown
CONTENT BRIEF: "{target_keyword}"
Client: {client_name} | Est. Word Count: {X-Y} words

PRIMARY KEYWORD: {target_keyword}
SECONDARY KEYWORDS: {keyword2}, {keyword3}, {keyword4}
LSI KEYWORDS: {lsi1}, {lsi2}, {lsi3}

SUGGESTED TITLE: {H1 under 60 chars with primary keyword}
META DESCRIPTION: {120-160 chars with CTA}
URL SLUG: /blog/{primary-keyword-format}

---

CONTENT STRUCTURE:

H1: {title}

  TL;DR / Key Takeaways (Required at top):
    • {Insight 1 in 1 sentence}
    • {Insight 2 in 1 sentence}
    • {Insight 3 in 1 sentence}

  Table of Contents (Required - anchor-linked)

  H2: {Section 1 heading — covers competitor gap + PAA #1}
    Word target: ~{N} words
    Cover: {what this section answers}

  H2: {Section 2 heading — covers competitor gap + PAA #2}
    H3: {Subsection 2a}
    H3: {Subsection 2b}
    Word target: ~{N} words

  H2: {Section 3 heading}
    Word target: ~{N} words

  H2: FAQ Section (triggers FAQ Schema)
    **FAQ REQUIREMENTS:**
    • Max 5-8 questions (never exceed 10)
    • Each answer: 50-150 words (2-3 sentences)
    • High-intent, conversion-focused questions only
    • DO NOT repeat content from main article

    H3: {Q1 from PAA}
    H3: {Q2 from PAA}
    H3: {Q3 from PAA}
    H3: {Q4 from PAA}
    H3: {Q5 from PAA}

  H2: Conclusion + CTA: "{cta_style from brand_kit}"
    **CONCLUSION REQUIREMENTS:**
    • Length: 100-150 words exactly
    • Must include: (1) Core insight recap, (2) Next action step, (3) Strong CTA with hyperlink
    • DO NOT summarize the article
    • DO NOT use "In conclusion" or "To summarize"
    • Example format:
      ```
      {Core insight}. {Why it matters}.

      Ready to {desired outcome}? {Action step with urgency}.

       [{CTA Button Text}]({conversion-page-link})
      ```

---

INTERNAL LINKS TO INCLUDE:
  1. [{anchor_text}]({url}) — Relevance: {score}
  2. [{anchor_text}]({url}) — Relevance: {score}
  3. [{anchor_text}]({url}) — Relevance: {score}

EXTERNAL LINKS TO CITE:
  1. {Authoritative source for statistic #1}
  2. {Industry report for data point}
  3. {Expert quote source}

---

ELITE SEO COMPONENTS:

  [OK] TL;DR / Key Takeaways Box (Required at top)
  [OK] Table of Contents (Required - anchor-linked)
  [OK] Comparison Table (Required if comparing tools/methods)
  [WARNING] Glossary of Terms (Optional - only if 3+ technical terms need definition)
  [OK] JSON-LD Schema Script (Article + FAQ)

---

SCHEMA REQUIREMENTS:

Article + FAQ schema as @graph JSON-LD
**Note for writer:** Copy this block into CMS <head> section or dedicated Schema field:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "headline": "{title}",
      "author": {"@type": "Person", "name": "{author_name}"},
      "datePublished": "{YYYY-MM-DD}",
      "description": "{meta_description}",
      "image": "{featured_image_url}"
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {"@type": "Question", "name": "{Q1}", "acceptedAnswer": {"@type": "Answer", "text": "{A1}"}},
        {"@type": "Question", "name": "{Q2}", "acceptedAnswer": {"@type": "Answer", "text": "{A2}"}}
      ]
    }
  ]
}
```

---

TONE NOTES:

Write as "{persona from brand_kit}". Use {tone} voice.

Example sentence in brand voice:
"{Example sentence showing tone}"

**Banned AI vocabulary (NEVER use):**
delve, moreover, furthermore, tapestry, paramount, seamless, dynamic, robust, landscape, testament, elevate, unleash, unlock, navigate, symphony, beacon, "in today's digital age", "in conclusion", "to summarize"

**Writing style:**
• Vary sentence lengths drastically (mix 3-word punchy sentences with longer descriptive ones)
• Use active voice only
• Sound opinionated, authoritative, and direct
• Get straight to the point — no fluff

---

COMPETITOR BENCHMARKS:

Average word count: {median} words
Our target: {median + 10%} words (must be better, not just longer)

Top competitor strengths:
  • Competitor 1: {what they do well}
  • Competitor 2: {what they do well}

Our unique angle:
  {What makes our article different/better than competitors}

---
```

**Then ask:**

```
Does this brief look good?

Options:
1. "Looks good, start writing" → I'll proceed to /content_draft
2. "Change {specific thing}" → I'll update the brief
3. "Save this for later" → I'll save to clients/{client}/active_campaigns/
```

---

### Step 8: Save Brief (After User Approval)

**Execute:**
```bash
Write: clients/{client}/active_campaigns/{slug}_brief.md
```

**File format:** Markdown (so user can read/edit easily)

**Validate:**
```bash
if [ ! -f "clients/{client}/active_campaigns/{slug}_brief.md" ]; then
  echo "[ERROR] Failed to save brief"
  # Retry once
fi
```

**Notify user:**
```
[OK] Brief saved to: clients/{client}/active_campaigns/{slug}_brief.md

Next steps:
1. Run /content_draft {client} --brief {path} to write the article
2. Or: Edit the brief manually and come back
```

---

## Error Handling & Fallback Logic

**If SERP scraper fails (429 rate limit):**
1. Wait 30 seconds
2. Retry once
3. If still fails: Use WebSearch + manual parsing
4. Document: "[WARNING] SERP scraper rate-limited, used manual analysis"

**If NLP analyzer fails:**
1. Extract LSI keywords manually from SERP data (look for common terms in top 3 results)
2. Use WebSearch for "people also ask {keyword}" to find FAQ questions
3. Continue with degraded data

**If no internal links found:**
- This is normal for new clients or new content pillars
- Note in brief: "This article will start a new content cluster"
- Suggest creating 2-3 supporting articles after this one

**If brand_kit.json is incomplete:**
- Use defaults: tone = "professional", cta_style = "Learn More"
- Flag to user: "[WARNING] Brand kit incomplete, using defaults. Update with /add_client?"

**If competitor pages are behind paywall:**
- Skip that URL, use next organic result
- Need minimum 3 competitors for valid analysis
- If < 3 available: Expand search to related keywords

---

## Expected Outputs

**Files Created:**
- `.tmp/{client}_serp.json` — SERP analysis data
- `.tmp/{client}_content_gaps.json` — LSI keywords and PAA questions
- `.tmp/{client}_internal_links.json` — Internal linking opportunities
- `.tmp/{client}_brief_{slug}.json` — Structured brief data
- `clients/{client}/active_campaigns/{slug}_brief.md` — **User-facing brief** (after approval)

**User-Facing Deliverable:**
Formatted brief in chat (Markdown) + saved file for editing

**Next Action:**
User chooses: (1) Write the article now, (2) Edit brief first, (3) Save for later

---

## Quality Gates

**Before presenting brief:**
- [ ] Primary keyword appears in: suggested title, meta, URL slug, H1
- [ ] Secondary + LSI keywords integrated into H2/H3 structure
- [ ] FAQ section has 5-8 questions max, answers are 50-150 words
- [ ] Conclusion structure is 100-150 words with clear CTA
- [ ] Schema is Article + FAQ (NOT HowTo, NOT FAQPage for commercial sites)
- [ ] All statistics have external source links identified
- [ ] Internal links are relevant (relevance score > 0.6)
- [ ] Tone notes include brand voice example and banned words list
- [ ] TL;DR has 3-5 key takeaways
- [ ] Table of Contents has anchor links for all H2/H3

---

## Edge Cases

**Scenario: Top-ranking pages are behind paywall**
- Skip that URL and use the next one
- Need minimum 3 competitors for analysis
- If < 3 available, expand search to related keywords

**Scenario: No internal links found**
- Normal for new clients or new content pillars
- Note: "This article could be the start of a new content cluster"
- Recommend creating 2-3 supporting articles

**Scenario: User wants to target multiple keywords**
- Create separate briefs for each keyword
- Or: Choose one primary keyword, others become secondary
- Never try to optimize one article for multiple unrelated keywords (causes dilution)

**Scenario: Keyword has no search volume data**
- Proceed anyway if it's strategically important
- Label as "Strategic content (no volume data available)"
- Focus on conversion quality over traffic quantity

---

## Related Workflows

- `/keyword_research` — Discover keywords before briefing
- `/content_draft` — Write the full article from this brief
- `/competitor_gap` — Find keyword opportunities first
- `/on_page` — Optimize existing content (no brief needed)

---

## Notes

**This workflow is deterministic:**
- Every tool call has explicit syntax + validation
- Every failure has a fallback method
- Every brief includes FAQ/Conclusion requirements from Rule 16
- Schema recommendations follow Rule 7 (no deprecated types)

**The brief is a contract:**
- Writer knows exactly what to write
- Client knows exactly what to expect
- No ambiguity, no guesswork
