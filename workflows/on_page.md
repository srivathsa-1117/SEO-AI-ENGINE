---
description: /on_page - Analyze and fix on-page SEO issues for specific pages
---

# Workflow: On-Page Optimization

## Trigger
```
/on_page <client_name> [--url <specific_page_url>] [--top <N>] [--output-format checklist|detailed]
```
**Example:** `/on_page acme_corp --url https://acme.com/blog/remote-teams`
**Example:** `/on_page acme_corp --top 10 --output-format detailed`

## Objective
Analyze and generate a prioritized list of specific, actionable on-page SEO fixes for one page or the client's top N pages by traffic/importance. Deliver a comprehensive fix list with before/after suggestions, implementation instructions, and expected impact.

---

## Required Inputs

1. **`<client_name>`** — Client folder name (loads brand_kit.json)
2. **`--url <url>`** — Specific page URL to analyze (optional, mutually exclusive with --top)
3. **`--top <N>`** — Analyze top N pages from last crawl (optional, mutually exclusive with --url)
4. **`--output-format`** — Output format: `checklist` (simple task list) or `detailed` (full analysis with examples)

---

## Step-by-Step Instructions

### Step 1: Load Client Context

**Tool:** Read tool (file system access)

**Execute:**
```bash
# Read brand kit
Read: clients/{client_name}/brand_kit.json
```

**Parse required fields:**
```json
{
  "client_name": "Acme Corp",
  "website_url": "https://acmecorp.com",
  "primary_keywords": ["project management", "team collaboration"],
  "target_audience": "HR managers at mid-size companies",
  "content_preferences": {
    "internal_link_priority": ["/features", "/pricing", "/case-studies"]
  }
}
```

**Validate:**
```bash
# Check file exists
if [ ! -f "clients/{client_name}/brand_kit.json" ]; then
  echo "[ERROR] Client not found: {client_name}"
  echo "Run /add_client {client_name} first"
  exit 1
fi
```

**Extract key info:**
- `website_url` — Base domain for URL validation
- `primary_keywords` — Keywords to check for in titles/metas
- `target_audience` — Context for content relevance checks
- `internal_link_priority` — Pages that should be linked to

---

### Step 2: Determine Target URLs

**Two modes:**

#### **Mode 1: Single URL Analysis** (if `--url` provided)

**Validate URL:**
```bash
# Check URL is accessible
if ! curl -I "{url}" 2>/dev/null | grep -q "200 OK"; then
  echo "[ERROR] URL not accessible: {url}"
  echo "Check if URL is correct and site is live"
  exit 1
fi

# Check URL belongs to client domain
if ! echo "{url}" | grep -q "{website_url}"; then
  echo "[WARNING] URL doesn't match client domain"
  echo "URL: {url}"
  echo "Expected domain: {website_url}"
  # Continue but flag as potential issue
fi
```

**Set target URLs:**
```python
target_urls = [url]
```

---

#### **Mode 2: Top N Pages Analysis** (if `--top` provided)

**Check for recent crawl data:**
```bash
# Look for most recent crawl file
Glob: .tmp/{client_name}_crawl*.json

# Sort by date, get most recent
latest_crawl=$(ls -t .tmp/{client_name}_crawl*.json | head -1)
```

**Validate crawl data exists:**
```bash
if [ -z "$latest_crawl" ]; then
  echo "[ERROR] No crawl data found for {client_name}"
  echo "Run /audit {client_name} first to generate crawl data"
  exit 1
fi
```

**Parse crawl data and extract top N URLs:**
```bash
Read: $latest_crawl
```

**Extract URLs by priority:**
```python
# Priority order:
# 1. Pages with most organic traffic (from GSC if available)
# 2. Pages with most internal links pointing to them
# 3. Pages at depth level 0-2 (closer to homepage)
# 4. Pages with existing rankings (from SERP data if available)

crawl_data = read_json(latest_crawl)

# Filter out non-content pages
excluded_patterns = ["/wp-admin/", "/cart", "/checkout", "/account", ".pdf", ".jpg", ".png"]
content_pages = [
  page for page in crawl_data["pages"]
  if not any(pattern in page["url"] for pattern in excluded_patterns)
]

# Sort by priority score
sorted_pages = sorted(content_pages, key=lambda p: calculate_priority_score(p), reverse=True)

# Take top N
target_urls = [page["url"] for page in sorted_pages[:N]]
```

**If crawl data has < N pages:**
- Warning: "[WARNING] Only {count} pages found in crawl (requested {N})"
- Continue with available pages

---

### Step 3: Page DOM Analysis

**Tool:** `on_page_analyzer.py`

**Execute:**
```bash
python tools/on_page_analyzer.py \
  --urls "{target_urls}" \
  --client "{client_name}" \
  --output ".tmp/{client_name}_onpage_analysis.json"
```

**Parameters:**
- `--urls`: Comma-separated list of URLs to analyze
- `--client`: Client name (for loading brand_kit context)
- `--output`: JSON file to save analysis results

**What this tool does:**
- Fetches each URL and parses HTML DOM
- Extracts all on-page SEO elements:
  - `<title>` tag content and length
  - `<meta name="description">` content and length
  - H1 tag (existence, uniqueness, content)
  - H2/H3 structure (count, content, hierarchy)
  - Image `alt` attributes (count missing, keyword stuffing check)
  - Word count (visible text only, excluding nav/footer)
  - Internal links (count, anchor text, destination pages)
  - External links (count, anchor text, domains)
  - Canonical tag (existence, self-referential check, correct target)
  - Schema markup (JSON-LD presence, types found, validation)
  - Open Graph tags (og:title, og:description, og:image)
  - Twitter Card tags
  - Page load time (basic timing)

**Validate output:**
```bash
# Check file was created
if [ ! -f ".tmp/{client_name}_onpage_analysis.json" ]; then
  echo "[ERROR] On-page analysis failed"
  # Check stderr for errors
  exit 1
fi

# Check file is not empty
if [ ! -s ".tmp/{client_name}_onpage_analysis.json" ]; then
  echo "[ERROR] Analysis file is empty"
  exit 1
fi

# Check JSON structure
if ! jq empty < ".tmp/{client_name}_onpage_analysis.json" 2>/dev/null; then
  echo "[ERROR] Invalid JSON in analysis file"
  exit 1
fi
```

**Expected output structure:**
```json
{
  "analyzed_at": "2025-03-16T14:30:00Z",
  "total_pages": 5,
  "pages": [
    {
      "url": "https://acmecorp.com/blog/remote-teams",
      "status_code": 200,
      "title": {
        "content": "Remote Work Tools",
        "length": 17,
        "has_keyword": false,
        "issues": ["too_short", "missing_keyword"]
      },
      "meta_description": {
        "content": null,
        "length": 0,
        "has_keyword": false,
        "issues": ["missing"]
      },
      "h1": {
        "content": "Best Remote Work Tools for Teams",
        "count": 1,
        "has_keyword": true,
        "issues": []
      },
      "h2_structure": {
        "count": 5,
        "headings": ["What is Remote Work?", "Top 7 Tools", "How to Choose", "Pricing", "FAQ"],
        "issues": ["missing_conclusion_heading"]
      },
      "h3_structure": {
        "count": 12,
        "issues": []
      },
      "images": {
        "total": 8,
        "missing_alt": 3,
        "alt_keyword_stuffed": 0,
        "issues": ["missing_alt_text"]
      },
      "word_count": 1850,
      "internal_links": {
        "count": 4,
        "links": [
          {"url": "/features", "anchor": "See our features"},
          {"url": "/pricing", "anchor": "Check pricing"},
          {"url": "/blog", "anchor": "blog"},
          {"url": "/contact", "anchor": "click here"}
        ],
        "issues": ["generic_anchor_text"]
      },
      "external_links": {
        "count": 2,
        "issues": ["low_external_links"]
      },
      "canonical": {
        "present": true,
        "url": "https://acmecorp.com/blog/remote-teams",
        "self_referential": true,
        "issues": []
      },
      "schema": {
        "present": false,
        "types": [],
        "issues": ["missing_schema"]
      },
      "open_graph": {
        "present": true,
        "og_title": "Remote Work Tools",
        "og_description": "Discover the best remote work tools...",
        "og_image": "https://acmecorp.com/images/remote-work.jpg",
        "issues": []
      },
      "load_time_ms": 1250
    }
  ]
}
```

**If analysis fails for specific URLs:**
- Log failed URLs separately
- Continue with successful analyses
- Flag failed URLs in final report with reason (404, timeout, blocked)

---

### Step 4: Competitor Benchmark Analysis

**For each target URL, identify its primary keyword:**

**Method 1:** Extract from existing data
```python
# Check if page already has a target keyword defined
# Look in: content briefs, crawl data, GSC data

if page_has_defined_keyword:
  primary_keyword = page["target_keyword"]
else:
  # Infer from title tag or H1
  primary_keyword = extract_main_keyword_from_title(page["title"])
```

**Method 2:** Manual specification
```bash
# If keyword can't be inferred, ask user
echo "[WARNING] Primary keyword not found for {url}"
echo "Suggested keywords from title: {suggestions}"
# User provides keyword
```

---

**Find top 3 Google competitors:**

**Tool:** `serp_scraper.py`

**Execute:**
```bash
python tools/serp_scraper.py \
  --mode serp_top10 \
  --keyword "{primary_keyword}" \
  --output ".tmp/{client_name}_serp_top3.json"
```

**Parse top 3 organic results:**
```json
{
  "keyword": "remote team management",
  "results": [
    {"url": "competitor1.com/article", "position": 1},
    {"url": "competitor2.com/guide", "position": 2},
    {"url": "competitor3.com/blog", "position": 3}
  ]
}
```

**Filter out client's own URL:**
```python
top_3_competitors = [
  result for result in results[:5]  # Get top 5, then filter
  if client_domain not in result["url"]
][:3]  # Take top 3 after filtering
```

---

**Benchmark competitor pages:**

**Tool:** `nlp_analyzer.py` (benchmark mode)

**Execute:**
```bash
python tools/nlp_analyzer.py \
  --mode benchmark \
  --urls "{client_url},{competitor1_url},{competitor2_url},{competitor3_url}" \
  --keyword "{primary_keyword}" \
  --output ".tmp/{client_name}_benchmark.json"
```

**What this tool does:**
- Fetches all URLs (client + competitors)
- Extracts and compares:
  - Word count
  - H2/H3 count
  - Keyword density
  - Entity coverage (named entities mentioned)
  - FAQ presence and count
  - Image count
  - Internal link count
  - External link count
  - Schema types present
  - Content depth score

**Expected output:**
```json
{
  "keyword": "remote team management",
  "benchmark_data": {
    "client": {
      "url": "acmecorp.com/blog/remote-teams",
      "word_count": 1850,
      "h2_count": 5,
      "h3_count": 12,
      "keyword_density": 1.2,
      "entities": ["Slack", "Zoom", "Asana"],
      "faq_count": 0,
      "schema_types": [],
      "content_depth_score": 65
    },
    "competitors": [
      {
        "url": "competitor1.com/article",
        "word_count": 3200,
        "h2_count": 8,
        "h3_count": 18,
        "keyword_density": 1.8,
        "entities": ["Slack", "Zoom", "Asana", "Monday.com", "Notion", "Trello"],
        "faq_count": 7,
        "schema_types": ["Article", "FAQPage"],
        "content_depth_score": 88
      },
      {
        "url": "competitor2.com/guide",
        "word_count": 2800,
        "h2_count": 7,
        "h3_count": 15,
        "keyword_density": 1.5,
        "entities": ["Slack", "Zoom", "Microsoft Teams"],
        "faq_count": 5,
        "schema_types": ["Article"],
        "content_depth_score": 82
      },
      {
        "url": "competitor3.com/blog",
        "word_count": 2200,
        "h2_count": 6,
        "h3_count": 10,
        "keyword_density": 1.4,
        "entities": ["Slack", "Zoom"],
        "faq_count": 0,
        "schema_types": [],
        "content_depth_score": 72
      }
    ],
    "averages": {
      "word_count": 2733,
      "h2_count": 7,
      "h3_count": 14,
      "keyword_density": 1.6,
      "entity_count": 4,
      "faq_count": 4,
      "content_depth_score": 81
    },
    "gaps": {
      "word_count_gap": -883,  // Client is 883 words behind average
      "h2_gap": -2,
      "h3_gap": -2,
      "missing_entities": ["Monday.com", "Notion", "Trello", "Microsoft Teams"],
      "faq_gap": -4,
      "schema_gap": ["Article", "FAQPage"]
    }
  }
}
```

**Validate benchmark output:**
```bash
# Check file exists
if [ ! -f ".tmp/{client_name}_benchmark.json" ]; then
  echo "[WARNING] Benchmark failed, skipping competitor comparison"
  # Continue without benchmark data
fi

# Check if at least 1 competitor was benchmarked
competitor_count=$(jq '.benchmark_data.competitors | length' ".tmp/{client_name}_benchmark.json")
if [ $competitor_count -lt 1 ]; then
  echo "[WARNING] No competitors benchmarked, skipping comparison"
fi
```

**If benchmark fails:**
- Continue with on-page analysis only
- Flag: "[INFO] Competitor benchmark unavailable — recommendations based on best practices only"

---

### Step 5: Generate Prioritized Fix List

**Analyze findings and categorize issues by severity:**

**Severity calculation:**
```python
def calculate_severity(issue_type, context):
    # CRITICAL: Blocking indexation or causing major ranking harm
    critical_issues = [
        "missing_h1",
        "duplicate_title_across_pages",
        "no_meta_description",
        "canonical_loop",
        "404_error",
        "noindex_tag_on_important_page",
        "redirect_chain"
    ]

    # HIGH: Significant ranking impact, should fix within 1 week
    high_issues = [
        "title_too_short",  # < 30 chars
        "title_too_long",  # > 60 chars
        "primary_keyword_missing_from_title",
        "images_missing_alt",  # > 20% of images
        "word_count_below_competitor_average",  # < 50% of avg
        "no_internal_links_to_page"
    ]

    # MEDIUM: Moderate impact, fix within 1 month
    medium_issues = [
        "h2_structure_weak",
        "meta_description_missing_keyword",
        "no_schema_markup",
        "low_keyword_density",  # < 0.5%
        "generic_anchor_text",  # "click here", "read more"
        "no_external_links"
    ]

    # LOW: Nice to have, optimize when possible
    low_issues = [
        "h3_structure_improvements",
        "add_faq_section",
        "improve_anchor_text_diversity",
        "add_open_graph_tags",
        "optimize_images_for_speed"
    ]

    if issue_type in critical_issues:
        return "CRITICAL"
    elif issue_type in high_issues:
        return "HIGH"
    elif issue_type in medium_issues:
        return "MEDIUM"
    else:
        return "LOW"
```

**Generate fix list:**
```python
fix_list = {
  "critical": [],
  "high": [],
  "medium": [],
  "low": []
}

for page in analysis_data["pages"]:
  for issue in page["title"]["issues"]:
    fix_list[calculate_severity(issue, page)].append({
      "page": page["url"],
      "issue_type": issue,
      "current_state": page["title"]["content"],
      "suggested_fix": generate_fix_suggestion(issue, page),
      "expected_impact": "Improve CTR by 15-25%",
      "implementation": "Update <title> tag in CMS"
    })

  # Repeat for all issue types...
```

---

### Step 6: Generate Updated Tags & Content Recommendations

**For critical title/meta issues, generate replacement suggestions:**

#### **Title Tag Suggestions**

**Rules:**
- Length: 50-60 characters (strict)
- Primary keyword at front (first 3-5 words)
- Compelling and click-worthy
- Include year if relevant (2025, 2026)
- Avoid keyword stuffing

**Generate:**
```python
def generate_title_suggestion(page, keyword):
    current = page["title"]["content"]

    # If title is too short (< 30 chars)
    if len(current) < 30:
        # Expand with keyword + benefit + year
        suggestion = f"{keyword}: Ultimate Guide for 2025"

    # If title is too long (> 60 chars)
    elif len(current) > 60:
        # Trim while keeping keyword
        suggestion = truncate_with_keyword(current, keyword, max_length=60)

    # If keyword missing
    elif keyword.lower() not in current.lower():
        # Prepend keyword
        suggestion = f"{keyword} - {current}"
        # Ensure still < 60 chars
        if len(suggestion) > 60:
            suggestion = f"{keyword}: {shorten(current, 60 - len(keyword) - 2)}"

    return suggestion

# Example output:
# Current: "Remote Work" (11 chars — TOO SHORT)
# Suggested: "Remote Team Management: 7 Proven Strategies for 2025" (54 chars ✓)
```

---

#### **Meta Description Suggestions**

**Rules:**
- Length: 120-160 characters (strict)
- Include primary keyword (at least once)
- End with clear CTA
- Benefit-focused, not feature-focused

**Generate:**
```python
def generate_meta_suggestion(page, keyword):
    current = page["meta_description"]["content"]

    # If missing entirely
    if current is None:
        # Generate from H1 + first paragraph
        suggestion = f"{keyword} explained. {extract_value_prop(page)}. {generate_cta(keyword)}."

    # If too short (< 120 chars)
    elif len(current) < 120:
        # Expand with benefit + CTA
        suggestion = f"{current} {generate_benefit(keyword)}. {generate_cta(keyword)}."

    # If too long (> 160 chars)
    elif len(current) > 160:
        # Trim to 160 chars at sentence boundary
        suggestion = truncate_at_sentence(current, max_length=160)

    # If keyword missing
    elif keyword.lower() not in current.lower():
        # Prepend keyword
        suggestion = f"{keyword}: {current}"
        # Trim if necessary
        if len(suggestion) > 160:
            suggestion = truncate_at_sentence(suggestion, max_length=160)

    return suggestion

# Example output:
# Current: [missing]
# Suggested: "Master remote team management with 7 proven strategies. Boost productivity, improve communication, and build stronger virtual teams. Get the complete guide." (158 chars ✓)
```

---

#### **Content Recommendations**

**Word Count:**
```python
if page["word_count"] < benchmark["averages"]["word_count"] * 0.5:
    recommendation = {
        "issue": "Content too thin",
        "current": f"{page['word_count']} words",
        "target": f"{benchmark['averages']['word_count']} words (competitor average)",
        "action": f"Add {benchmark['averages']['word_count'] - page['word_count']} more words",
        "suggestions": [
            "Expand on existing H2 sections (add 200-300 words each)",
            "Add FAQ section (7-10 questions, 100-150 words each = ~1000 words)",
            "Include comparison table or case study (300-500 words)",
            f"Cover missing topics: {', '.join(benchmark['gaps']['missing_entities'])}"
        ]
    }
```

**H2/H3 Structure:**
```python
if page["h2_structure"]["count"] < benchmark["averages"]["h2_count"]:
    recommendation = {
        "issue": "Weak heading structure",
        "current": f"{page['h2_structure']['count']} H2 headings",
        "target": f"{benchmark['averages']['h2_count']} H2 headings (competitor average)",
        "action": f"Add {benchmark['averages']['h2_count'] - page['h2_structure']['count']} more H2 sections",
        "suggestions": [
            "Add 'FAQ' H2 section",
            "Add 'Conclusion' H2 section",
            "Split long sections into subsections",
            f"Cover competitor topics: {list_missing_h2_topics(page, benchmark)}"
        ]
    }
```

**FAQ Section:**
```python
if page["benchmark"]["faq_count"] == 0 and benchmark["averages"]["faq_count"] > 0:
    recommendation = {
        "issue": "Missing FAQ section",
        "current": "No FAQ",
        "target": f"{benchmark['averages']['faq_count']} FAQs (competitor average)",
        "action": "Add FAQ section with 5-8 questions",
        "suggestions": [
            "Extract common questions from People Also Ask (PAA)",
            "Review competitor FAQ questions and create better answers",
            "Add FAQPage schema markup",
            "Keep answers short (50-150 words each)"
        ],
        "example_questions": generate_faq_questions(keyword)
    }
```

**Schema Markup:**
```python
if not page["schema"]["present"]:
    recommendation = {
        "issue": "Missing schema markup",
        "current": "No schema",
        "target": "Article + FAQPage + BreadcrumbList schema",
        "action": "Implement JSON-LD schema",
        "schema_code": generate_schema_markup(page, keyword)
    }
```

---

### Step 7: Format Output

**Two output formats:**

#### **Format 1: Checklist** (simple task list for quick implementation)

````markdown
# On-Page SEO Fixes — {Client Name}

**Page:** {url}
**Analyzed:** {date}
**Total Issues:** {count}

---

## [ERROR] CRITICAL (Fix Immediately)

- [ ] **Fix title tag** — Current: "{current_title}" (11 chars, too short)
  - Replace with: "{suggested_title}" (54 chars ✓)
  - Impact: Improve CTR by 15-25%

- [ ] **Add meta description** — Currently missing
  - Add: "{suggested_meta}" (158 chars ✓)
  - Impact: Improve SERP snippet appearance

---

## [WARNING] HIGH (Fix This Week)

- [ ] **Fix missing alt text on 3 images** — 37% of images missing alt
  - Image 1: /images/remote-work.jpg → Alt: "Remote team using video conferencing for collaboration"
  - Image 2: /images/tools.png → Alt: "Project management tool dashboard showing team tasks"
  - Image 3: /images/tips.jpg → Alt: "Remote work best practices checklist"
  - Impact: Improve image SEO and accessibility

- [ ] **Increase word count to 2,700 words** — Currently 1,850 words (32% below competitor average)
  - Add FAQ section (~1,000 words)
  - Expand existing H2 sections (~850 words)
  - Impact: Match competitor content depth

---

##  MEDIUM (Fix This Month)

- [ ] **Add schema markup** — Currently missing
  - Implement Article + FAQPage schema
  - Copy/paste code: [see schema_code.json]
  - Impact: Increase rich snippet eligibility

- [ ] **Improve internal linking** — Only 4 internal links (target: 5-7)
  - Add links to: /features, /case-studies, /pricing
  - Use natural anchor text (not "click here")
  - Impact: Improve crawlability and PageRank flow

---

##  LOW (Nice to Have)

- [ ] **Add FAQ section** — Competitors average 4 FAQs
  - Add 7-10 FAQ questions
  - Keep answers short (50-150 words)
  - Impact: Potential featured snippet opportunity

- [ ] **Improve anchor text diversity** — 2 out of 4 links use generic "click here"
  - Replace with descriptive anchors
  - Impact: Better SEO and user experience
````

---

#### **Format 2: Detailed** (full analysis with examples and benchmarks)

````markdown
# On-Page SEO Analysis — {Client Name}

**Page:** {url}
**Analyzed:** {date}
**Primary Keyword:** {keyword}

---

##  Page Performance Summary

| Metric | Current | Competitor Avg | Gap | Status |
|--------|---------|----------------|-----|--------|
| Word Count | 1,850 | 2,733 | -883 | [WARNING] Behind |
| H2 Headings | 5 | 7 | -2 | [WARNING] Behind |
| H3 Headings | 12 | 14 | -2 | [WARNING] Behind |
| Keyword Density | 1.2% | 1.6% | -0.4% | [WARNING] Low |
| FAQs | 0 | 4 | -4 | [ERROR] Missing |
| Schema Types | 0 | 2 | -2 | [ERROR] Missing |
| Internal Links | 4 | 6 | -2 | [WARNING] Low |
| External Links | 2 | 5 | -3 | [WARNING] Low |
| Images with Alt | 5 / 8 (63%) | ~95% | -32% | [WARNING] Low |

**Overall SEO Health:** 58/100 (Fair)
**Competitor Average:** 81/100

---

## [ERROR] CRITICAL ISSUES (4)

### 1. Title Tag Too Short
**Current:** "Remote Work" (11 chars)
**Issue:** Title is too short and missing primary keyword
**Suggested:** "Remote Team Management: 7 Proven Strategies for 2025" (54 chars ✓)
**Impact:** Improve CTR by 15-25%
**Implementation:**
```html
<title>Remote Team Management: 7 Proven Strategies for 2025</title>
```

---

### 2. Missing Meta Description
**Current:** [none]
**Issue:** No meta description defined (Google will auto-generate poor snippet)
**Suggested:** "Master remote team management with 7 proven strategies. Boost productivity, improve communication, and build stronger virtual teams. Get the complete guide." (158 chars ✓)
**Impact:** Improve SERP snippet appearance, increase CTR by 10-20%
**Implementation:**
```html
<meta name="description" content="Master remote team management with 7 proven strategies. Boost productivity, improve communication, and build stronger virtual teams. Get the complete guide.">
```

---

## [WARNING] HIGH PRIORITY ISSUES (3)

### 3. 37% of Images Missing Alt Text
**Current:** 3 out of 8 images missing alt attributes
**Issue:** Hurts image SEO and accessibility
**Suggested Alt Text:**
```html
<!-- Image 1: /images/remote-work.jpg -->
<img src="/images/remote-work.jpg" alt="Remote team using video conferencing for daily collaboration">

<!-- Image 2: /images/tools.png -->
<img src="/images/tools.png" alt="Project management tool dashboard showing team tasks and progress">

<!-- Image 3: /images/tips.jpg -->
<img src="/images/tips.jpg" alt="Remote work best practices checklist for distributed teams">
```
**Impact:** Improve image SEO, accessibility, potential image search rankings

---

### 4. Content Too Thin (32% Below Competitor Average)
**Current:** 1,850 words
**Competitor Average:** 2,733 words
**Gap:** -883 words (32% behind)
**Suggested Actions:**
1. **Add FAQ section** (~1,000 words)
   - 7-10 questions, 100-150 words per answer
   - Focus on high-intent questions: "What tools...", "How to...", "How much..."

2. **Expand existing H2 sections** (~850 words)
   - "Top 7 Tools" section: Add 150-200 words per tool (benefits, pricing, use cases)
   - "How to Choose" section: Add decision framework table + 200 words

3. **Add missing topics** (from competitor gap analysis)
   - Cover: Monday.com, Notion, Trello, Microsoft Teams
   - Add comparison table: Async vs Sync Communication Tools

**Impact:** Match competitor content depth, improve rankings by 3-5 positions

---

##  MEDIUM PRIORITY ISSUES (4)

### 5. Missing Schema Markup
**Current:** No schema present
**Competitor Benchmark:** 2/3 competitors have Article + FAQPage schema
**Suggested Schema:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "headline": "Remote Team Management: 7 Proven Strategies for 2025",
      "description": "Master remote team management...",
      "image": "https://acmecorp.com/images/remote-work.jpg",
      "author": {
        "@type": "Organization",
        "name": "Acme Corp"
      },
      "publisher": {
        "@type": "Organization",
        "name": "Acme Corp",
        "logo": {
          "@type": "ImageObject",
          "url": "https://acmecorp.com/logo.png"
        }
      },
      "datePublished": "2024-06-15",
      "dateModified": "2025-03-16"
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "What is remote team management?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Remote team management is..."
          }
        }
      ]
    }
  ]
}
</script>
```
**Implementation:** Copy/paste into CMS <head> section
**Impact:** Increase rich snippet eligibility by 40%, potential FAQ rich results

---

### 6. Low Internal Linking (Only 4 Links)
**Current:** 4 internal links
**Target:** 5-7 internal links
**Current Links:**
- /features → Anchor: "See our features" ✓
- /pricing → Anchor: "Check pricing" ✓
- /blog → Anchor: "blog" [ERROR] (too generic)
- /contact → Anchor: "click here" [ERROR] (generic)

**Suggested Additions:**
````markdown
Add these internal links:
1. Link to /case-studies/remote-teams → Anchor: "how we helped 50+ remote teams scale"
2. Link to /features/time-tracking → Anchor: "time zone management features"
3. Link to /blog/async-communication → Anchor: "asynchronous communication best practices"
````
**Impact:** Improve internal PageRank flow, better crawlability

---

## [OK] LOW PRIORITY OPTIMIZATIONS (3)

### 7. Add FAQ Section for Featured Snippet Opportunity
**Current:** No FAQ section
**Competitor Benchmark:** 2/3 competitors have FAQ sections (avg 4 FAQs)
**Suggested FAQ Questions:**
1. What is remote team management?
2. How do you track productivity for remote teams?
3. What are the best tools for managing remote teams?
4. How do you communicate effectively with remote employees?
5. What are the biggest challenges of managing remote teams?
6. How do you onboard new remote employees?
7. How much does remote team management software cost?

**Implementation:**
- Add H2 section titled "FAQ" before conclusion
- Use H3 for each question
- Keep answers 50-150 words (scannable, direct)
- Add FAQPage schema (see Issue #5)

**Impact:** Potential featured snippet, answer box, or PAA inclusion

---

##  Expected Impact Summary

**If all CRITICAL + HIGH issues are fixed:**
- **Estimated ranking improvement:** +3-7 positions
- **Estimated CTR improvement:** +20-35%
- **Estimated organic traffic increase:** +40-60% within 60-90 days

**Implementation Timeline:**
- **Week 1:** Fix CRITICAL issues (title, meta) — 2 hours
- **Week 2:** Fix HIGH issues (images, word count) — 6-8 hours
- **Month 1:** Fix MEDIUM issues (schema, links) — 3-4 hours
- **Ongoing:** LOW priority optimizations (FAQ, anchor text) — 2-3 hours

**Total Effort:** ~15-20 hours for complete optimization

---

##  Next Steps

1.  Review this analysis
2.  Prioritize issues (start with CRITICAL)
3.  Implement fixes in CMS
4.  Test changes:
   - Google Rich Results Test (schema)
   - SERP preview (title/meta)
   - Accessibility check (alt text)
5.  Monitor results in GSC after 2-4 weeks

**Need help implementing? I can:**
- Generate complete schema markup code
- Write FAQ section content
- Rewrite title/meta for all pages
- Audit entire site (not just one page)

Type "help" to continue or "done" to finish.


---

## Expected Outputs

### Files Created:
1. **`.tmp/{client_name}_onpage_analysis.json`** — Raw on-page analysis data
2. **`.tmp/{client_name}_serp_top3.json`** — Top 3 competitor URLs
3. **`.tmp/{client_name}_benchmark.json`** — Competitor benchmark comparison
4. **`clients/{client_name}/on_page_fixes_{date}.md`** — Prioritized fix list (saved if requested)

### User-Facing Deliverables:
1. **Fix list** — Prioritized by severity (CRITICAL → HIGH → MEDIUM → LOW)
2. **Before/after suggestions** — Updated title tags, meta descriptions, alt text
3. **Content recommendations** — Word count targets, H2 additions, FAQ suggestions
4. **Schema markup code** — Copy/paste ready JSON-LD
5. **Impact estimates** — Expected ranking/CTR improvements per fix
6. **Implementation timeline** — Effort estimates for each issue

---

## Quality Gates (Check Before Delivery)

Before presenting the analysis to the user, verify:

- [ ] Brand kit loaded successfully
- [ ] Target URLs determined (either --url or --top N from crawl)
- [ ] On-page analysis completed for all URLs (or failures logged)
- [ ] Competitor benchmark attempted (or skipped with note if failed)
- [ ] All issues categorized by severity (CRITICAL/HIGH/MEDIUM/LOW)
- [ ] Title tag suggestions: 50-60 characters with keyword
- [ ] Meta description suggestions: 120-160 characters with CTA
- [ ] Alt text suggestions: descriptive, keyword-natural, no stuffing
- [ ] Word count gap calculated vs competitor average
- [ ] Schema markup code generated (if missing)
- [ ] Internal link suggestions reference brand_kit priority pages
- [ ] Impact estimates provided for high-priority fixes
- [ ] Implementation instructions clear and actionable
- [ ] No broken URLs in analysis (404s flagged separately)
- [ ] Output format matches user request (checklist or detailed)

---

## Edge Cases

### 1. **Page returns 404 during analysis**
**Scenario:** Target URL is not accessible (404 Not Found)

**Handling:**
- Error: "[ERROR] Page not found: {url} (404 error)"
- Flag as CRITICAL issue in fix list
- Recommended actions:
  1. If page should exist → Fix broken URL or restore page
  2. If page was deleted → Set up 301 redirect to relevant page
  3. If URL is typo → Correct URL and re-run analysis
- Skip on-page analysis for this URL
- Continue with remaining URLs if analyzing multiple pages

---

### 2. **Page uses JavaScript rendering (SPA)**
**Scenario:** Page content is loaded via JavaScript (React, Vue, Angular)

**Handling:**
- Warning: "[WARNING] Page uses JavaScript rendering — analysis may be incomplete"
- `on_page_analyzer.py` should use Playwright (renders JS), but still flag:
  - "[INFO] Ensure server-side rendering (SSR) or pre-rendering for SEO"
  - "[WARNING] Googlebot may not render all content — verify with GSC URL Inspection"
- Recommend:
  - Implement SSR (Next.js, Nuxt.js) or static site generation
  - Use pre-rendering service (Prerender.io, Rendertron)
  - Verify rendering with Google Search Console

---

### 3. **No crawl data available** (for --top N mode)
**Scenario:** User requests --top 10 but no crawl data exists

**Handling:**
- Error: "[ERROR] No crawl data found for {client_name}"
- Recommend: "Run /audit {client_name} first to generate crawl data"
- Alternative: "Use --url to analyze a specific page instead"
- Exit with error code 1

---

### 4. **Competitor benchmark fails** (SERP scraper blocked or rate limited)
**Scenario:** Can't fetch top 3 competitor URLs

**Handling:**
- Warning: "[WARNING] Competitor benchmark failed — using best practice recommendations only"
- Skip benchmark comparison section
- Use generic best practice targets:
  - Word count: 2,000+ words (industry standard)
  - H2 count: 6-8 headings
  - FAQ count: 5-8 questions
  - Schema: Article + FAQPage minimum
- Flag in output: "[INFO] Competitor data unavailable — targets based on SEO best practices"
- Continue with on-page analysis

---

### 5. **Primary keyword can't be determined**
**Scenario:** Page has no clear target keyword

**Handling:**
- Warning: "[WARNING] Primary keyword not found for {url}"
- Infer from:
  1. Title tag (extract main phrase)
  2. H1 content (extract main phrase)
  3. URL slug (convert hyphens to spaces)
- If still unclear:
  - Ask user: "What's the primary keyword for {url}?"
  - Provide suggestions based on extracted phrases
  - User provides keyword
- Continue with provided keyword

---

### 6. **Page has multiple H1 tags**
**Scenario:** Page has 2+ H1 tags (SEO anti-pattern)

**Handling:**
- Flag as HIGH priority issue
- Issue: "Multiple H1 tags found ({count})"
- Current H1s:
  ```
  H1 #1: "Remote Team Management"
  H1 #2: "Best Practices for Remote Teams"
  ```
- Recommended fix:
  - Keep only 1 H1 (usually the first one)
  - Convert additional H1s to H2 tags
  - Implementation: Update HTML tags from `<h1>` to `<h2>`
- Impact: Improve heading structure clarity, avoid SEO confusion

---

### 7. **Canonical tag points to different URL**
**Scenario:** Page's canonical tag points to a different page (not self-referential)

**Handling:**
- Flag as CRITICAL or HIGH depending on whether it's intentional
- Check if canonical target is valid:
  - If canonical = homepage or main category page → Likely intentional (thin content page)
  - If canonical = 404 or redirect chain → CRITICAL issue (broken canonical)
  - If canonical = duplicate content page → Intentional (consolidating duplicates)
- Recommended actions:
  1. **If intentional:** No action needed (correctly consolidating duplicates)
  2. **If broken canonical:** Fix to point to correct URL
  3. **If unintentional:** Make canonical self-referential
- Flag: "[INFO] Verify canonical is intentional — this page won't rank (passes authority to {canonical_url})"

---

### 8. **Word count extremely low** (< 300 words)
**Scenario:** Page has very little content

**Handling:**
- Flag as CRITICAL issue
- Issue: "Thin content ({word_count} words)"
- Recommended actions:
  1. **If intentional thin page (e.g., product landing page):**
     - Add more value: benefits, FAQs, testimonials
     - Target: 800-1,000 words minimum
  2. **If low-value page:**
     - Consider noindex or 301 redirect to more valuable page
     - Consolidate with related page
  3. **If important page:**
     - Expand to 1,500-2,000 words
     - Add comprehensive content: guides, examples, case studies
- Impact: Thin pages rarely rank — aim for 1,000+ words minimum

---

### 9. **Title/meta exactly match competitor** (plagiarism concern)
**Scenario:** Client's title tag is identical or near-identical to competitor

**Handling:**
- Flag as HIGH priority issue
- Issue: "Title matches competitor {competitor_url}"
- Warning: "[WARNING] Potential plagiarism or duplicate content issue"
- Recommended action:
  - Generate unique title that's differentiated from competitor
  - Add brand name: "{Keyword}: {Unique Angle} | {Brand Name}"
  - Add unique value prop: "{Keyword} for {Audience} - {Unique Benefit}"
- Example:
  - Competitor: "Remote Team Management Best Practices"
  - Unique: "Remote Team Management: 7 Strategies Used by 10,000+ Teams | Acme"
- Impact: Avoid duplicate content penalties, improve brand differentiation

---

### 10. **All images already have alt text** (no issues found)
**Scenario:** All images have descriptive alt attributes

**Handling:**
- Flag as "[OK] No issues found"
- Still provide optimization suggestion:
  - "[INFO] All images have alt text — verify they're descriptive and keyword-natural"
  - Check for keyword stuffing: Alt text shouldn't repeat exact keyword multiple times
  - Check for generic alts: "image", "photo", "picture" → make descriptive
- If alt text is perfect:
  - "[OK] Image SEO: Excellent (all images have descriptive, keyword-natural alt text)"

---

### 11. **Page is password-protected or requires login**
**Scenario:** Page content can't be fetched (requires authentication)

**Handling:**
- Error: "[ERROR] Page requires authentication: {url}"
- Recommended actions:
  1. Provide temporary access for analysis (disable login requirement)
  2. Export page HTML manually and provide to analyzer
  3. Skip this page and analyze other pages
- Flag: "[WARNING] Could not analyze {url} — requires authentication"
- Continue with other pages

---

### 12. **Schema markup exists but has validation errors**
**Scenario:** JSON-LD is present but fails validation

**Handling:**
- Flag as MEDIUM priority issue
- Issue: "Schema validation errors ({error_count} errors)"
- Parse validation errors from Google Rich Results Test
- Common errors:
  - Missing required field (e.g., `datePublished` in Article schema)
  - Invalid @type value
  - Malformed JSON (missing comma, bracket)
- Recommended fix:
  - Fix validation errors (provide corrected schema code)
  - Test with: https://search.google.com/test/rich-results
- Impact: Fix errors to maintain rich snippet eligibility

---

## Error Handling Protocol

### **If `on_page_analyzer.py` fails:**
1. Read stderr output for error message
2. Common errors:
   - **ModuleNotFoundError (playwright)**: Run `pip install playwright` + `playwright install`
   - **Timeout**: Increase timeout or reduce page count
   - **403 Forbidden**: Site blocking automated crawlers (use different user agent)
   - **SSL Certificate Error**: Use `--ignore-https-errors` flag
3. Fallback: Use WebFetch for basic analysis (limited data)
4. Document: "[WARNING] On-page analyzer unavailable — using basic analysis"

### **If `nlp_analyzer.py` fails:**
1. Check dependencies (spacy, nltk installed?)
2. Fallback: Skip benchmark comparison, use best practice targets
3. Document: "[WARNING] NLP analyzer unavailable — competitor benchmark skipped"

### **If SERP scraper fails:**
1. Wait 30 seconds, retry once
2. Fallback: Manual competitor identification (ask user for competitor URLs)
3. Document: "[WARNING] SERP scraper unavailable — using manual competitor list"

---

## Performance Expectations

**Estimated execution time:**
- Brand kit load: 1-2 seconds
- Target URL determination: 2-5 seconds
- On-page analysis (1 page): 5-10 seconds
- On-page analysis (10 pages): 30-60 seconds
- Competitor benchmark (3 competitors): 15-30 seconds
- Fix list generation: 5-10 seconds
- Output formatting: 5-10 seconds

**Total (1 page):** ~30-60 seconds
**Total (10 pages):** ~2-3 minutes

**If execution exceeds 5 minutes:**
- Check for tool hangs (timeout issues, blocked requests)
- Reduce page count or skip benchmark
- Generate analysis with available data

---

## Notes

- **Prioritization:** Always fix CRITICAL issues first (blocking indexation or causing major harm)
- **Impact estimates:** Based on industry averages — actual results may vary
- **Implementation order:** Title/meta fixes are fastest (2 hours), content additions take longest (6-8 hours)
- **Re-analysis:** Run this workflow again after fixes to measure improvement
- **Tracking:** Use GSC to monitor CTR and ranking changes after implementation (allow 2-4 weeks for Google to re-crawl)
