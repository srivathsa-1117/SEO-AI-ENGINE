---
description: /content_draft - Write a full SEO-optimized article from an approved content brief
---

# Workflow: Content Draft Generation (100% Humanized & Ranking-Optimized)

## Trigger
```
/content_draft <client_name> [--brief <path_to_brief>] [--word-count <target>] [--aeo-mode chatgpt|perplexity|gemini]
```
**Examples:**
- `/content_draft acme_corp --brief clients/acme_corp/briefs/remote-teams.md --word-count 2000`
- `/content_draft acme_corp --brief clients/acme_corp/briefs/best-tools.md --aeo-mode chatgpt`
- `/content_draft acme_corp --brief clients/acme_corp/briefs/comparison.md --aeo-mode perplexity`

## Objective
Generate a fully SEO-optimized, AEO/GEO-ready article that ranks #1 and passes all AI detection tools. The output MUST bypass AI detectors (100% humanized) through high burstiness, varied sentence lengths, and the absolute elimination of standard AI jargon. Includes exact Titles, Metas, Schema markup, and CMS-ready formatting.

---

## AI SEARCH OPTIMIZATION MODES (2026)

**NEW:** If `--aeo-mode` flag is provided, apply platform-specific optimizations:

### Mode 1: ChatGPT Optimization (70% AI Search Market Share)
**When:** `--aeo-mode chatgpt`

**Requirements:**
- **Word count:** 2000+ words minimum (comprehensive depth)
- **Citations:** Minimum 5 external authoritative sources with hyperlinks
- **Author bio:** Place at TOP (above H1) AND bottom (after conclusion)
- **Expertise signals:** Case studies, specific data points, "We tested 47 variations" (not "many")
- **Structure:** Deep sections with 3-4 sub-levels (H2 → H3 → H4)
- **Format:** How-to guides, comprehensive tutorials, comparison articles

**Author Bio Format (Top):**
```markdown
**By [Author Name], [Title] at [Company]**
*[2-sentence expertise summary with specific credentials]*
```

---

### Mode 2: Perplexity Optimization (Citation-Heavy, Fresh Content)
**When:** `--aeo-mode perplexity`

**Requirements:**
- **Freshness indicator:** "**Updated: March 2026**" at very top (above H1)
- **Tone:** Reddit-style discussion (conversational, opinionated, direct)
- **Citations:** Clear source citations with publication dates
  - Format: "According to a March 2026 study by Stanford ([source](link))..."
- **Comparison tables:** Side-by-side feature/pricing comparisons
- **Numbered lists:** Use #1, #2, #3 format for rankings
- **Recent data:** All statistics <12 months old
- **Format:** "Best X" rankings, product comparisons, vs. articles

**Freshness Format:**
```markdown
**Updated: March 20, 2026** | Reading time: 8 minutes

# [Article Title]
```

---

### Mode 3: Gemini Optimization (Google Knowledge Graph Integration)
**When:** `--aeo-mode gemini`

**Requirements:**
- **Triple schema stacking:** Organization + Article + BreadcrumbList (already in Step 4)
- **Entity linking:** Strong @id and sameAs properties in Organization schema
  - Link to Wikidata/Wikipedia if brand has entry
  - Format: `"sameAs": ["https://www.wikidata.org/wiki/Q12345"]`
- **Structured data tables:** Pricing tables, feature matrices, comparison charts
- **Clear hierarchy:** Proper breadcrumb implementation
- **Internal linking:** Rich anchor text linking to related content
- **Knowledge Graph entities:** Mention related entities (people, companies, concepts)
- **Format:** Informational articles, guides, entity-rich content

**Entity Schema Example:**
```json
{
  "@type": "Organization",
  "@id": "https://acmecorp.com/#organization",
  "name": "Acme Corp",
  "sameAs": [
    "https://www.wikidata.org/wiki/Q12345",
    "https://en.wikipedia.org/wiki/Acme_Corporation"
  ]
}
```

---

### Mode 4: Default (No --aeo-mode flag)
**When:** No flag provided

**Use:** Generic best practices (current workflow behavior)
- Answer blocks after H2s (50-75 words)
- FAQ section
- Standard schema
- E-E-A-T phrasing

---

## ARTICLE TEMPLATES BY TYPE (2026 Best Practices)

### Template 1: "Best X" / Numbered Ranking Articles

**When to Use:**
- Keywords containing: "best", "top", "alternatives", "vs", "comparison"
- AI engines cite numbered rankings **3.2x more** than unstructured lists
- ChatGPT and Perplexity heavily favor this format

**MANDATORY FORMAT:**

```markdown
## The [Number] Best [Category] in 2026

### #1. [Product/Service Name] — Best Overall
**Quick Take:** [50-75 word summary of what it is, why it's #1, and who it's for]

**Key Features:**
- [Feature 1 with specific detail]
- [Feature 2 with specific detail]
- [Feature 3 with specific detail]

**Pros:**
- [Specific advantage]
- [Specific advantage]
- [Specific advantage]

**Cons:**
- [Specific limitation]
- [Specific limitation]

**Best For:** [Specific use case or user type]

**Pricing:** [Exact price with plan details, e.g., "$49/month (Pro plan) or $99/month (Enterprise)"]

**Our Experience:** [First-hand take with proof - "We tested this for 90 days with 15 clients and saw..." OR "Based on 50+ user reviews, the most common feedback is..."]

---

### #2. [Product/Service Name] — Best for [Specific Category]
**Quick Take:** [50-75 word summary]

[Repeat same structure as #1]

---

### #3. [Product/Service Name] — Best Budget Option
**Quick Take:** [50-75 word summary]

[Repeat same structure as #1]

---

[Continue for all rankings - typically 5-10 items maximum]
```

**CRITICAL RULES:**
- **Use numbered format:** #1, #2, #3 (not "First", "Second", "Third")
- **Category tags:** Each item gets a specific "Best for X" designation (never repeat categories)
- **Specific pricing:** Exact numbers with plan names, not "affordable" or "expensive"
- **Proof required:** Every "Our Experience" section needs either:
  - Specific data ("increased conversions by 23%")
  - Timeline ("used it for 6 months")
  - Sample size ("tested with 47 clients")
  - Screenshot/image showing actual results
- **Balanced pros/cons:** Minimum 3 pros, minimum 2 cons (shows objectivity)
- **Quick comparison table:** Add this AFTER all individual rankings:

```markdown
## Quick Comparison Table

| Rank | Product | Best For | Pricing | Rating |
|------|---------|----------|---------|--------|
| #1 | [Name] | [Category] | $X/mo | (4.8/5) |
| #2 | [Name] | [Category] | $X/mo | (4.5/5) |
| #3 | [Name] | [Category] | $X/mo | (4.6/5) |
```

**AI Search Optimization Notes:**
- **ChatGPT:** Prefers comprehensive depth (500+ words per ranked item for top 3)
- **Perplexity:** Prefers concise summaries (200-300 words per item) with clear citations
- **Gemini:** Requires strong schema markup (ItemList + Product schema for each ranked item)

---

### Template 2: Comparison Articles ("X vs Y")

**When to Use:**
- Keywords: "[Product A] vs [Product B]", "[Solution] alternative", "better than [X]"

**MANDATORY FORMAT:**

```markdown
## [Product A] vs [Product B]: Which is Better in 2026?

**TL;DR:** [One-sentence verdict - e.g., "Product A wins for enterprises, Product B for startups"]

### Side-by-Side Comparison

| Feature | Product A | Product B | Winner |
|---------|-----------|-----------|--------|
| Pricing | $99/mo | $49/mo |  Product B |
| Ease of Use | 4.2/5 | 4.8/5 |  Product B |
| Integrations | 150+ | 50+ |  Product A |
| Support | Email only | 24/7 live chat |  Product B |
| Advanced Features | Yes | Limited |  Product A |

### When to Choose Product A
- [Specific use case 1]
- [Specific use case 2]
- [Specific use case 3]

### When to Choose Product B
- [Specific use case 1]
- [Specific use case 2]
- [Specific use case 3]

### Our Recommendation
[Neutral, data-driven recommendation based on user type]
```

**CRITICAL RULES:**
- **Winner column:** Declare clear winner per category (shows objectivity)
- **No bias:** If sponsored/affiliate, disclose at top: "**Disclosure:** This article contains affiliate links."
- **Use case clarity:** Each product gets specific scenarios where it wins

---

## CRITICAL RULE: The "100% Human" Writing Guidelines

You must write like a Senior Subject Matter Expert, not an AI.

**1. BANNED AI VOCABULARY:**
Do NOT use these words under any circumstances: *delve, moreover, furthermore, tapestry, paramount, seamless, dynamic, robust, landscape, testament, elevate, unleash, unlock, navigate, symphony, beacon, in today's digital age, in conclusion, to summarize, myriad, plethora, dive deep, game-changer, cutting-edge, revolutionary, synergy, holistic.*

**2. Burstiness & Perplexity:**
- Vary your sentence lengths drastically. Use very short, punchy sentences (3-5 words). Follow them with longer, descriptive sentences.
- Avoid perfectly symmetrical paragraph lengths. Humans write in asymmetrical blocks.
- Use sentence length distribution: 30% short (5-10 words), 50% medium (11-20 words), 20% long (21+ words)

**3. Tone & Voice:**
- Use active voice only (90%+ of sentences). Avoid passive voice.
- Limit transition words (like "however," "therefore"). Humans use them sparingly (< 30% of sentences).
- Sound opinionated, authoritative, and direct. Get straight to the point. No fluff.
- Write like you're explaining to a colleague, not lecturing to students.

**4. E-E-A-T Elements (Experience & Expertise):**
- Phrase concepts using first-hand terminology where appropriate to the brand: *"In our experience,"* *"When we tested this,"* *"What we usually see is..."*
- Include specific data points, real examples, and concrete numbers (not vague "many" or "several")
- Reference authoritative sources with hyperlinks (minimum 3-5 external links)
- Show expertise through nuanced takes, not just surface-level information

**5. VISUAL PROOF REQUIREMENTS (2026 E-E-A-T):**
**CRITICAL:** Content MUST include minimum 2 of these visual proof elements:

**Screenshots of actual results**
  - Before/after comparisons
  - Dashboard screenshots showing real metrics
  - Analytics data (with sensitive info redacted)
  - Example: "seo-audit-results-before-after-2026.png"

**Original data tables/charts**
  - Survey results with sample size
  - Case study metrics (conversion rates, traffic growth)
  - A/B test results
  - Benchmark data you collected

**Process screenshots/walkthroughs**
  - Step-by-step tool usage with actual screenshots
  - Configuration screenshots
  - Example: "google-search-console-setup-step3.png"

**Team/author photos**
  - Author headshot with bio
  - Team working on project
  - Behind-the-scenes of service delivery

**Client logos/testimonials**
  - Recognizable brand logos (with permission)
  - Screenshot of review/testimonial
  - Video thumbnail of client interview

**Image Format Rules:**
- **NEVER:** Generic stock photos, image001.png, placeholder images
- **ALWAYS:** Descriptive filenames with keywords
  - Good: `remote-team-slack-integration-dashboard-2026.png`
  - Bad: `image001.png`, `screen-shot-2026.png`
- **Alt text:** Detailed description (50-125 chars) with primary keyword
  - Example: `alt="Remote team management dashboard showing Slack integration metrics and productivity scores"`
- **Caption:** Context below image explaining what's shown
- **Frequency:** Minimum 1 image every 300 words (aim for 1 per 200 words)

**Where Visual Proof Goes:**
1. Right after H2 introducing new section (context-setting image)
2. During process explanations (step-by-step screenshots)
3. When citing data/results (chart, table, or screenshot)
4. In case study sections (before/after, client results)
5. Author bio section (headshot)

---

## Required Inputs

1. **`<client_name>`** — Client folder name (loads brand_kit.json)
2. **`--brief <path>`** — Path to content brief markdown file (required)
3. **`--word-count <target>`** — Target word count (defaults to brief's recommendation or 2000)

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
  "tone": "professional, authoritative, conversational",
  "brand_voice": "We are experts in remote team management. We speak from experience, not theory.",
  "target_audience": "HR managers at mid-size companies (50-500 employees)",
  "primary_cta": "Book a Demo",
  "cta_url": "https://acmecorp.com/demo",
  "content_preferences": {
    "banned_words": ["synergy", "revolutionary"],
    "preferred_examples": "Real case studies from our clients",
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
- `tone` — Writing style to use
- `brand_voice` — How the brand speaks
- `target_audience` — Who you're writing for
- `primary_cta` — Call to action text
- `cta_url` — CTA destination URL
- `content_preferences.banned_words` — Client-specific words to avoid (add to global banned list)
- `content_preferences.internal_link_priority` — Pages to link to first

---

### Step 2: Load Content Brief

**Tool:** Read tool

**Execute:**
```bash
# Read content brief
Read: {brief_path}
```

**Expected brief structure:**
```markdown
---
title: "How to Manage Remote Teams Effectively in 2025"
primary_keyword: "remote team management"
secondary_keywords: ["managing remote employees", "remote work best practices", "virtual team collaboration"]
target_word_count: 2000
search_intent: informational
target_audience: "HR managers, team leads"
---

# Content Brief

## Target Keyword: remote team management
- Search Volume: 2,400/month
- Keyword Difficulty: 45 (Medium)
- Current Top 3 Competitors: [list URLs]

## Outline (H2/H3 Structure):
1. What is Remote Team Management? (H2)
2. 7 Challenges of Managing Remote Teams (H2)
   - Communication gaps (H3)
   - Time zone differences (H3)
   - ...
3. Best Practices for Remote Team Management (H2)
4. Tools for Managing Remote Teams (H2)
5. FAQ (H2)
6. Conclusion (H2)

## Must-Include Points:
- Mention time zone management tools
- Include statistics on remote work growth (cite sources)
- Compare async vs sync communication
- Recommend specific collaboration tools

## Competitor Analysis:
- Competitor 1: 2,500 words, includes case studies, ranks #2
- Competitor 2: 1,800 words, strong FAQ section, ranks #3
- Competitor 3: 3,000 words, very comprehensive, ranks #1

## Internal Links to Include:
- /features (remote team features)
- /case-studies/remote-teams
- /blog/async-communication
```

**Validate brief:**
```bash
# Check brief file exists
if [ ! -f "{brief_path}" ]; then
  echo "[ERROR] Content brief not found: {brief_path}"
  echo "Run /content_brief to generate one first"
  exit 1
fi

# Check required fields exist
required_fields=("primary_keyword" "target_word_count" "outline")
for field in "${required_fields[@]}"; do
  if grep -q "$field" "{brief_path}"; then
    echo "[OK] $field found"
  else
    echo "[ERROR] Missing required field: $field"
    exit 1
  fi
done
```

**Extract key info:**
- `primary_keyword` — Main keyword to target
- `secondary_keywords` — Related keywords to naturally weave in
- `target_word_count` — Length target
- `outline` — H2/H3 structure to follow
- `must_include_points` — Critical elements to cover
- `internal_links` — Pages to link to

**If brief is missing fields:**
- Warning: "[WARNING] Brief is incomplete — missing {field}"
- Recommend: "Run /content_brief {client_name} --keyword '{keyword}' to generate complete brief"
- Continue with available data (use defaults)

---

### Step 3: Research & Data Validation

**Check if SERP analysis exists:**
```bash
# Look for cached SERP data from brief generation
Glob: .tmp/{client_name}_serp_{primary_keyword}.json
```

**If SERP data exists:**
```bash
Read: .tmp/{client_name}_serp_{primary_keyword}.json
```

**Parse competitor content intelligence:**
```json
{
  "top_competitors": [
    {
      "url": "competitor1.com/article",
      "word_count": 2500,
      "h2_headings": ["What is...", "How to...", "Best practices"],
      "h3_headings": ["Communication", "Tools", "Processes"],
      "faq_questions": ["What tools...", "How do you..."],
      "unique_angles": ["Case study from Fortune 500 company", "Remote team framework diagram"]
    }
  ],
  "avg_word_count": 2300,
  "common_topics": ["communication", "tools", "best practices", "challenges"],
  "missing_topics": ["security considerations", "performance reviews"]
}
```

**Use this to:**
- Beat average word count (target: +10-20% above avg)
- Cover all common topics
- Add unique angles competitors are missing
- Structure FAQ based on competitor FAQ patterns

**If SERP data doesn't exist:**
- Warning: "[WARNING] No SERP analysis found — using brief outline only"
- Recommend: "For best results, run /content_brief with SERP analysis first"
- Continue with brief outline only

---

### Step 4: Generate SEO Package (CMS Metadata)

**Before writing the article, generate the exact metadata for CMS:**

#### **1. Title Tag**

**Rules:**
- Length: 50-60 characters (strict)
- Primary keyword at the front (first 3-5 words)
- Include year if content is time-sensitive (2025, 2026)
- Include power words: Best, Ultimate, Complete, Essential, Proven
- Avoid clickbait: No "You Won't Believe" or "Mind-Blowing"

**Tool:** Character counter

**Execute:**
```python
title_tag = "Remote Team Management: 7 Proven Strategies for 2025"

# Validate
if len(title_tag) < 50 or len(title_tag) > 60:
  echo "[WARNING] Title tag length: {len(title_tag)} chars (target: 50-60)"
  # Adjust and retry
fi
```

**Output:**
```html
<title>Remote Team Management: 7 Proven Strategies for 2025</title>
```

---

#### **2. Meta Description**

**Rules:**
- Length: 120-160 characters (strict)
- Include primary keyword (at least once)
- End with clear CTA (Learn, Discover, Get, Download, Start)
- Make it compelling (benefit-focused, not feature-focused)

**Tool:** Character counter

**Execute:**
```python
meta_desc = "Master remote team management with 7 proven strategies. Boost productivity, improve communication, and build stronger virtual teams. Get the complete guide."

# Validate
if len(meta_desc) < 120 or len(meta_desc) > 160:
  echo "[WARNING] Meta description length: {len(meta_desc)} chars (target: 120-160)"
  # Adjust and retry
fi
```

**Output:**
```html
<meta name="description" content="Master remote team management with 7 proven strategies. Boost productivity, improve communication, and build stronger virtual teams. Get the complete guide.">
```

---

#### **3. URL Slug**

**Rules:**
- Format: `primary-keyword-format`
- Include primary keyword exactly as it appears
- Maximum 5-7 words
- No stop words (a, the, of, for) unless part of exact keyword match
- Use hyphens, not underscores

**Generate:**
```bash
url_slug = primary_keyword.replace(" ", "-").lower()
# Example: "remote-team-management-strategies-2025"
```

**Output:**
```
URL: /blog/remote-team-management-strategies-2025
```

---

#### **4. JSON-LD Schema Markup**

**Tool:** Schema generator

**Generate consolidated `@graph` JSON-LD block:**
```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "headline": "Remote Team Management: 7 Proven Strategies for 2025",
      "description": "Master remote team management with 7 proven strategies...",
      "image": "https://acmecorp.com/images/remote-team-management.jpg",
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
      "datePublished": "2025-03-16",
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
            "text": "Remote team management is the practice of leading and coordinating employees who work from different locations..."
          }
        }
      ]
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://acmecorp.com"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "Blog",
          "item": "https://acmecorp.com/blog"
        },
        {
          "@type": "ListItem",
          "position": 3,
          "name": "Remote Team Management",
          "item": "https://acmecorp.com/blog/remote-team-management-strategies-2025"
        }
      ]
    }
  ]
}
</script>
```

**Validate schema:**
```bash
# Validate JSON structure
if ! jq empty <<< "$schema_json" 2>/dev/null; then
  echo "[ERROR] Invalid JSON in schema markup"
  # Fix JSON syntax
fi

# Check required fields
required=("@type" "headline" "author" "publisher" "datePublished")
# Verify all present
```

**Instructions for user:**
```
 **Schema Markup Instructions:**
1. Copy the entire <script> block above
2. Paste into your CMS:
   - WordPress: Yoast SEO → Schema tab OR custom HTML block in <head>
   - Shopify: Theme → Edit code → theme.liquid <head> section
   - Webflow: Page Settings → Custom Code → Head Code
3. Replace {image_url} with actual article featured image URL
4. Update {datePublished} to actual publish date
5. Test with Google Rich Results Test: https://search.google.com/test/rich-results
```

---

### Step 5: Write the Draft (Section by Section)

**Target word count calculation:**
```python
# Beat competitors by 10-20%
if serp_data exists:
  target_wc = serp_data["avg_word_count"] * 1.15
else:
  target_wc = brief["target_word_count"] or 2000

# Round to nearest 100
target_wc = round(target_wc / 100) * 100
```

---

#### **5.1: The TL;DR / Key Takeaways**

**Placement:** Immediately after the introduction (before H2 sections)

**Format:**
```markdown
> **Key Takeaways:**
> - [Bullet 1: Main insight in 10-15 words]
> - [Bullet 2: Specific benefit or strategy]
> - [Bullet 3: Surprising statistic or fact]
> - [Bullet 4: Actionable tip]
> - [Bullet 5: Bottom-line recommendation]
```

**Rules:**
- Exactly 3-5 bullets (never more than 6)
- Each bullet: 10-20 words maximum
- Focus on what the reader will *learn* or *gain*, not what the article *covers*
- Scannable format (use blockquote > for visual distinction)

**Example:**
```markdown
> **Key Takeaways:**
> - Remote teams are 13% more productive when using async communication tools.
> - Time zone overlaps must have at least 3 hours for effective collaboration.
> - Weekly 1-on-1s reduce remote employee turnover by 25%.
> - Document everything—remote teams rely on written communication.
> - Tools alone don't work; you need clear processes and accountability.
```

---

#### **5.2: The Table of Contents**

**Generate linked TOC from H2/H3 structure:**
```markdown
## Table of Contents
1. [What is Remote Team Management?](#what-is-remote-team-management)
2. [7 Challenges of Managing Remote Teams](#challenges)
   - [Communication Gaps](#communication-gaps)
   - [Time Zone Differences](#time-zones)
   - [Lack of Accountability](#accountability)
3. [Best Practices for Remote Team Management](#best-practices)
4. [Tools for Managing Remote Teams](#tools)
5. [FAQ](#faq)
6. [Conclusion](#conclusion)
```

**Tool:** Anchor link generator

**Execute:**
```python
# For each H2/H3 heading
heading = "What is Remote Team Management?"
anchor = heading.lower().replace(" ", "-").replace("?", "")
# Output: "what-is-remote-team-management"
```

**Validate:**
```bash
# Ensure all TOC links match actual H2/H3 headings
# Check for broken anchors
```

---

#### **5.3: The Body (Main Content)**

**Follow outline from brief, structured by H2 sections:**

**Writing rules:**
1. **Natural keyword integration:**
   - Primary keyword: 1-2% density (5-10 times in 2000-word article)
   - Secondary keywords: Naturally weave in (don't force)
   - LSI keywords: Include variations (e.g., "managing remote employees" = "leading distributed teams")

2. **Comparison tables** (if applicable):
   - Format as Markdown tables
   - Example: "Async vs Sync Communication"
   ```markdown
   | Async Communication | Sync Communication |
   |---------------------|---------------------|
   | Emails, Slack messages | Video calls, meetings |
   | Flexible timing | Requires everyone online |
   | Better for deep work | Better for brainstorming |
   ```

3. **Formatting best practices:**
   - Paragraph length: 2-4 sentences (50-100 words max)
   - Use bullet points for lists (3+ items)
   - Bold key terms and important statements (< 5% of total text)
   - Use subheadings (H3) every 300-400 words
   - Include images/diagrams: [Image description] (placeholder) every 500-700 words

4. **Links (mandatory):**
   - **Internal links:** 3-5 links to client's own pages
     - Link to pages in `brand_kit["content_preferences"]["internal_link_priority"]`
     - Use natural anchor text (not "click here")
   - **External links:** 3-5 links to authoritative sources
     - Statistics must be hyperlinked to source
     - Tools/products mentioned should link to official sites
     - Research findings should link to original study

5. **E-E-A-T elements:**
   - Include first-hand experience phrases: "In our experience managing 50+ remote teams..."
   - Cite specific data: "We surveyed 200 remote team managers and found..."
   - Show expertise: "After testing 15 collaboration tools, here's what actually works..."
   - Add concrete examples: "For instance, when we helped [Client X] transition to remote work, we..."

**Tool:** NLP analyzer (for keyword density check)

**Execute after each section:**
```bash
python tools/nlp_analyzer.py \
  --mode keyword_density \
  --text "{section_text}" \
  --keyword "{primary_keyword}" \
  --output ".tmp/{client}_density_check.json"
```

**Validate:**
```json
{
  "primary_keyword_density": 1.8,  // Target: 1-2%
  "secondary_keywords_found": ["managing remote employees", "remote work best practices"],
  "over_optimized_keywords": [],  // Should be empty
  "passive_voice_percentage": 12,  // Target: < 20%
  "transition_word_percentage": 28  // Target: < 30%
}
```

**If keyword density > 2.5%:**
- Warning: "[WARNING] Keyword stuffing detected ({density}%) — reduce primary keyword usage"
- Rewrite section to use synonyms and variations

**If passive voice > 20%:**
- Warning: "[WARNING] High passive voice ({percentage}%) — convert to active voice"
- Identify passive sentences and rewrite

---

#### **5.4: The FAQ Section**

**CRITICAL FAQ RULES (Non-Negotiable):**
- **Maximum:** 5-8 FAQs per article (never exceed 10)
- **Answer length:** 50-150 words per answer (2-3 sentences maximum)
- **Focus:** High-intent, conversion-driving questions only
- **Format:** Scannable and direct—no fluff or repetition
- **No redundancy:** If main content already covered it thoroughly, DO NOT repeat it in FAQs

**FAQ structure:**
```markdown
## FAQ

### What is remote team management?
Remote team management is the practice of leading and coordinating employees who work from different locations, often across time zones. It requires different tools and processes than traditional in-office management.

### How do you track productivity for remote teams?
Use output-based metrics (deliverables completed) rather than time-based metrics (hours logged). Tools like Asana, Monday.com, and Jira help track task completion without micromanaging.

### What are the best tools for managing remote teams?
The top tools are: Slack (communication), Zoom (video meetings), Asana (project management), and Notion (documentation). Choose based on your team size and workflow needs.

[... 2-5 more FAQs]
```

**Tool:** FAQ generator validation

**Execute:**
```bash
# Count FAQ questions
faq_count=$(grep -c "^### " faq_section)

# Validate count
if [ $faq_count -gt 8 ]; then
  echo "[ERROR] Too many FAQs: $faq_count (max 8)"
  echo "Remove lowest-value questions"
  exit 1
fi

# Check answer length
for answer in faq_answers; do
  word_count=$(echo "$answer" | wc -w)
  if [ $word_count -gt 150 ]; then
    echo "[WARNING] FAQ answer too long: $word_count words (max 150)"
    echo "Shorten answer: $answer"
  fi
done
```

**FAQ Schema integration:**
- FAQs automatically become FAQPage schema (already in SEO Package Step 4)
- Each question/answer pair maps to schema.org Question/Answer entity

---

#### **5.5: The Conclusion**

**MANDATORY CONCLUSION STRUCTURE (Non-Negotiable):**

**Length:** 100-150 words exactly (strict limit)

**Structure:**
1. **Sentence 1:** One-sentence recap of core value/insight
2. **Sentence 2:** Why it matters (benefit or consequence)
3. **Sentence 3:** Clear next action step (what reader should do now)
4. **Sentence 4:** Strong CTA with specific action verb + hyperlink

**Example format:**
```markdown
## Conclusion

Remote team management isn't about control—it's about trust, clarity, and the right systems. When you prioritize async communication, document everything, and invest in the right tools, your distributed team will outperform any in-office setup.

Ready to transform your remote team's productivity? Start by implementing one strategy from this guide this week—we recommend beginning with weekly 1-on-1s.

**[Book a Free Remote Team Audit](https://acmecorp.com/demo)** — We'll analyze your current setup and show you exactly where to improve.
```

**DO NOT:**
- Write a summary of the article (reader already read it)
- Use "In conclusion" or "To summarize"
- End without a clear, clickable CTA
- Make it longer than 150 words
- Use vague CTAs like "learn more" or "contact us"

**Tool:** Word counter validation

**Execute:**
```bash
conclusion_word_count=$(echo "$conclusion" | wc -w)

if [ $conclusion_word_count -lt 100 ] || [ $conclusion_word_count -gt 150 ]; then
  echo "[ERROR] Conclusion length: $conclusion_word_count words (target: 100-150)"
  exit 1
fi

# Check for CTA link
if ! grep -q "](http" "$conclusion"; then
  echo "[ERROR] No hyperlinked CTA found in conclusion"
  exit 1
fi
```

**CTA must link to:**
- `brand_kit["cta_url"]` if specified
- Conversion page (/demo, /pricing, /contact, /download)
- NOT blog posts or other articles (conversion-focused only)

---

#### **5.6: The Glossary (Optional)**

**Only add if:**
- Article uses 3+ technical terms that need definition
- Target audience may not know the terms (check brand_kit["target_audience"])

**Format:**
```markdown
## Glossary

**Async Communication:** Communication that doesn't require real-time responses (e.g., email, Slack).

**Synchronous Communication:** Real-time communication requiring all participants to be online simultaneously (e.g., video calls).

**OKRs (Objectives and Key Results):** A goal-setting framework used to define and track objectives and their outcomes.
```

**Placement:** BEFORE the conclusion (not after)

**Rules:**
- Each definition: 1 sentence maximum (15-25 words)
- Alphabetical order
- Bold the term, regular text for definition

---

### Step 6: SEO Final Checking & Validation

**Tool:** Multi-check validation script

**Execute comprehensive checks:**

#### **6.1: Banned Word Scanner**

**Tool:** Text scanner

**Execute:**
```bash
# Combine global banned words + client-specific banned words
banned_words=("delve" "moreover" "furthermore" "tapestry" "paramount" "seamless" "dynamic" "robust" "landscape" "testament" "elevate" "unleash" "unlock" "navigate" "symphony" "beacon" "in today's digital age" "in conclusion" "to summarize" "myriad" "plethora" "dive deep" "game-changer" "cutting-edge" "revolutionary" "synergy" "holistic")

# Add client-specific banned words
if brand_kit["content_preferences"]["banned_words"] exists:
  banned_words+=("${brand_kit["content_preferences"]["banned_words"][@]}")
fi

# Scan article
for word in "${banned_words[@]}"; do
  if grep -qi "$word" article.md; then
    echo "[ERROR] BANNED WORD FOUND: $word"
    echo "Remove or replace with human alternative"
    exit 1
  fi
done
```

**If banned words found:**
- Highlight locations (line numbers)
- Suggest alternatives:
  - "moreover" → "also", "and"
  - "furthermore" → "plus", "additionally"
  - "robust" → "strong", "powerful", "effective"
  - "delve" → "explore", "examine", "look at"

---

#### **6.2: Keyword Optimization Check**

**Tool:** `nlp_analyzer.py`

**Execute:**
```bash
python tools/nlp_analyzer.py \
  --mode full_analysis \
  --text article.md \
  --keyword "{primary_keyword}" \
  --output ".tmp/{client}_final_check.json"
```

**Validate:**
```json
{
  "primary_keyword_in_h1": true,
  "primary_keyword_in_url": true,
  "primary_keyword_in_title": true,
  "primary_keyword_in_meta": true,
  "primary_keyword_density": 1.6,  // Target: 1-2%
  "secondary_keywords_used": 5,  // Target: 3-5
  "internal_links_count": 4,  // Target: 3-5
  "external_links_count": 5,  // Target: 3-5
  "all_stats_linked": true,
  "passive_voice_percentage": 15,
  "avg_sentence_length": 16,
  "burstiness_score": 0.72  // Target: > 0.65 (high variation in sentence length)
}
```

**Thresholds:**
- [OK] `primary_keyword_density`: 1.0-2.5%
- [OK] `internal_links_count`: 3-5
- [OK] `external_links_count`: 3-5
- [OK] `passive_voice_percentage`: < 20%
- [OK] `burstiness_score`: > 0.65

**If any check fails:**
- Warning: "[WARNING] SEO check failed: {issue}"
- Provide specific fix: "Add 2 more internal links to {pages}"

---

#### **6.3: AI Detection Check**

**Tool:** AI detector (optional, if tool available)

**Execute:**
```bash
# Use GPTZero, Originality.ai, or similar
# For now, use proxy checks:

# 1. Banned word check (already done)
# 2. Burstiness check (sentence length variation)
# 3. Transition word density check
# 4. Passive voice check

# Calculate AI detection probability
ai_score = (
  (banned_words_found * 20) +
  ((1 - burstiness_score) * 30) +
  (transition_word_percentage * 0.5) +
  (passive_voice_percentage * 0.5)
)

# Lower score = more human
# Target: < 20 (considered human-written)
```

**If AI score > 30:**
- Warning: "[WARNING] High AI detection score: {ai_score} (target: < 20)"
- Recommend:
  - Vary sentence lengths more (add very short sentences)
  - Reduce transition words
  - Convert passive to active voice
  - Add more first-person experience phrases

---

#### **6.4: LLM Citability / AEO Check**

**Agent Persona:** `content-architect.md`

**Validate Natively (No External Tool Required):**
- Ensure all major H2s have a 50-75 word direct answer block underneath them.
- Ensure the article includes at least one structured markdown table.
- Verify strict data attribution ("According to a 2026 study by...") instead of loose claims.
- **Fail condition:** If the article lacks these elements, the Content Architect must rewrite the failing sections before presenting to the user.

---

#### **6.5: Structural Validation**

**Checklist (automated):**
```bash
# Check required sections exist
- [ ] TL;DR / Key Takeaways section present
- [ ] Table of Contents with linked anchors
- [ ] All H2/H3 headings from brief included
- [ ] FAQ section with 5-8 questions
- [ ] Conclusion section with 100-150 words
- [ ] CTA link in conclusion pointing to {cta_url}

# Check formatting
- [ ] All statistics have hyperlinks to sources
- [ ] Internal links use natural anchor text (not "click here")
- [ ] External links open in new tab (if HTML output)
- [ ] All headings use proper hierarchy (H2 → H3, not H2 → H4)

# Check metadata
- [ ] Title tag: 50-60 characters
- [ ] Meta description: 120-160 characters
- [ ] URL slug contains primary keyword
- [ ] JSON-LD schema includes Article + FAQPage + BreadcrumbList
```

**Auto-validation script:**
```python
validation_results = {
  "tldr_present": check_section_exists("Key Takeaways"),
  "toc_present": check_section_exists("Table of Contents"),
  "faq_count": count_faqs(),
  "conclusion_length": count_words_in_section("Conclusion"),
  "cta_link_present": check_link_in_section("Conclusion", cta_url),
  "title_length": len(title_tag),
  "meta_length": len(meta_desc),
  "schema_valid": validate_json_ld(schema_markup)
}

# Flag failures
for check, result in validation_results.items():
  if not result:
    echo "[ERROR] Failed: {check}"
```

---

### Step 7: Output Generation

**Format:** Clean Markdown ready for copy/paste into CMS

**Structure the output:**
```markdown
# CMS PACKAGE — Copy & Paste Ready

## Meta Data (Paste into CMS fields)

**Title Tag:**
```
Remote Team Management: 7 Proven Strategies for 2025
```

**Meta Description:**
```
Master remote team management with 7 proven strategies. Boost productivity, improve communication, and build stronger virtual teams. Get the complete guide.
```

**URL Slug:**
```
/blog/remote-team-management-strategies-2025
```

---

## Schema Markup (Paste into <head> or Schema plugin)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [...]
}
</script>
```

**Instructions:**
1. Copy the entire <script> block above
2. Paste into:
   - WordPress: Yoast SEO → Schema tab OR custom HTML block in <head>
   - Shopify: Theme → Edit code → theme.liquid <head> section
   - Webflow: Page Settings → Custom Code → Head Code
3. Replace {image_url} with actual featured image URL
4. Update {datePublished} to today's date
5. Test: https://search.google.com/test/rich-results

---

## Article Content (Paste into WordPress/Shopify editor)

[Full article in Markdown format]

---

# QUALITY METRICS

- **Word Count:** 2,150 words (target: 2,000)
- **Primary Keyword Density:** 1.6%
- **Burstiness Score:** 0.74 (high variation)
- **AI Detection Score:** 15 (human-level)
- **Internal Links:** 4
- **External Links:** 5
- **FAQ Count:** 7
- **Conclusion Length:** 142 words

[OK] All quality checks passed
```

**Ask user:**
```
Here is the 100% human-optimized draft and CMS package.

Would you like me to:
1. Save to client folder (clients/{client_name}/published/{date}_{slug}.md)
2. Refine the tone or adjust word count
3. Export to Google Docs for client review

Type 1, 2, or 3.


---

## Expected Outputs

### Files Created:
1. [OK] **`.tmp/{client}_density_check.json`** — Keyword density validation results
2. [OK] **`.tmp/{client}_final_check.json`** — Comprehensive SEO validation results
3. [OK] **`clients/{client}/published/{date}_{slug}.md`** — Final article markdown (if saved)
4. [OK] **`clients/{client}/published/{date}_{slug}_metadata.json`** — Title, meta, schema, metrics

### User-Facing Deliverables:
1. [OK] **CMS Package** — Title, meta, URL, schema (copy/paste ready)
2. [OK] **Full article in Markdown** — Ready for WordPress/Shopify
3. [OK] **Quality metrics summary** — Word count, keyword density, AI score, validation results

---

## Quality Gates (Check Before Delivery)

Before presenting the article to the user, verify:

- [ ] Brand kit loaded successfully
- [ ] Content brief exists and has all required fields (primary_keyword, outline, target_word_count)
- [ ] Title tag: 50-60 characters with primary keyword at front
- [ ] Meta description: 120-160 characters with CTA
- [ ] URL slug contains primary keyword
- [ ] JSON-LD schema valid (Article + FAQPage + BreadcrumbList)
- [ ] TL;DR section: 3-5 bullets, each 10-20 words
- [ ] Table of Contents: All links match actual H2/H3 headings
- [ ] Article follows brief outline exactly (all H2/H3 sections included)
- [ ] Primary keyword density: 1.0-2.5%
- [ ] Secondary keywords naturally integrated (3-5 uses)
- [ ] Internal links: 3-5 links to priority pages
- [ ] External links: 3-5 links to authoritative sources, all stats linked
- [ ] FAQ section: 5-8 questions, each answer 50-150 words
- [ ] Conclusion: 100-150 words with hyperlinked CTA to {cta_url}
- [ ] No banned words found (global + client-specific)
- [ ] Burstiness score > 0.65 (varied sentence lengths)
- [ ] Passive voice < 20%
- [ ] AI detection score < 30 (human-level)
- [ ] Word count within ±10% of target
- [ ] All validation checks passed

---

## Edge Cases

### 1. **Brief file not found**
**Scenario:** `--brief` path doesn't exist

**Handling:**
- Error: "[ERROR] Content brief not found: {brief_path}"
- Recommend: "Run /content_brief {client_name} --keyword '{keyword}' to generate brief first"
- Do NOT proceed without brief
- Exit with error code 1

---

### 2. **Brief missing required fields**
**Scenario:** Brief exists but lacks `primary_keyword`, `outline`, or `target_word_count`

**Handling:**
- Warning: "[WARNING] Brief is incomplete — missing: {missing_fields}"
- Use defaults:
  - `primary_keyword`: Extract from title or ask user
  - `outline`: Generate basic structure (Intro, Main Points, FAQ, Conclusion)
  - `target_word_count`: 2000 words (industry standard)
- Flag in output: "[WARNING] Generated with incomplete brief — review carefully"
- Continue with available data

---

### 3. **Client brand kit missing tone/voice**
**Scenario:** Brand kit exists but `tone` or `brand_voice` fields are empty

**Handling:**
- Warning: "[WARNING] Brand voice not defined in brand_kit.json"
- Use default tone: "professional, authoritative, conversational"
- Flag in output: "[WARNING] Generic tone used — define brand voice in brand_kit for better results"
- Continue with generic tone

---

### 4. **Keyword density too low (< 1%)**
**Scenario:** Primary keyword appears only 2-3 times in 2000-word article

**Handling:**
- Warning: "[WARNING] Low keyword density: {density}% (target: 1-2%)"
- Automatically add primary keyword to:
  - First paragraph (if not already there)
  - At least one H2 heading
  - Conclusion
- Re-check density after additions
- Flag if still < 1%: "[WARNING] Very low keyword density — may not rank"

---

### 5. **Keyword density too high (> 2.5%)**
**Scenario:** Keyword stuffing detected

**Handling:**
- Error: "[ERROR] Keyword stuffing: {density}% (max: 2.5%)"
- Automatically replace some instances with:
  - Synonyms (e.g., "remote team management" → "managing distributed teams")
  - Pronouns ("it", "this approach", "these strategies")
  - Variations ("remote work", "virtual teams")
- Re-check density after replacements
- Exit if still > 2.5% (manual review required)

---

### 6. **Too many FAQs (> 10)**
**Scenario:** Brief suggests 12+ FAQ questions

**Handling:**
- Warning: "[WARNING] Too many FAQs in brief: {count} (max: 8)"
- Automatically filter to top 8 most valuable:
  - Prioritize questions with high search volume
  - Focus on conversion-driving questions ("How much", "What tools", "How to start")
  - Remove redundant questions (already covered in main content)
- Flag: "[INFO] Filtered {count} FAQs to top 8 most valuable"

---

### 7. **Conclusion too long (> 150 words)**
**Scenario:** Generated conclusion is 200+ words

**Handling:**
- Warning: "[WARNING] Conclusion too long: {word_count} words (max: 150)"
- Automatically trim:
  - Remove any summary sentences (recap already done in one sentence)
  - Remove extra fluff or transition phrases
  - Keep only: recap sentence + why it matters + action step + CTA
- Re-check length
- Exit if still > 150 words (manual rewrite required)

---

### 8. **No CTA link in conclusion**
**Scenario:** Conclusion written but no hyperlink found

**Handling:**
- Error: "[ERROR] No CTA link found in conclusion"
- Automatically add CTA:
  - Use `brand_kit["cta_url"]` if exists
  - Default: "**[Get Started](https://domain.com/contact)**"
- Flag: "[INFO] CTA added automatically — verify link points to correct page"

---

### 9. **Banned words found**
**Scenario:** AI jargon detected in article

**Handling:**
- Error: "[ERROR] BANNED WORDS FOUND: {words}"
- List all occurrences with line numbers
- Suggest replacements:
  - "delve" → "explore", "examine"
  - "robust" → "strong", "powerful"
  - "leverage" → "use", "apply"
- Automatically replace if possible
- Exit if manual review needed for context-sensitive words

---

### 10. **High AI detection score (> 30)**
**Scenario:** Article flagged as likely AI-written

**Handling:**
- Warning: "[WARNING] High AI detection score: {score} (target: < 20)"
- Automatically adjust:
  - Add 5-10 very short sentences (3-5 words) throughout
  - Reduce transition words (remove "however", "therefore", "moreover")
  - Convert passive to active voice
  - Add first-person experience phrases ("In our experience...", "We've found...")
- Re-check score
- Flag if still > 30: "[WARNING] Manual humanization needed — review and rewrite flagged sections"

---

### 11. **No SERP data available**
**Scenario:** `.tmp/{client}_serp_{keyword}.json` doesn't exist

**Handling:**
- Warning: "[WARNING] No SERP analysis found — using brief outline only"
- Use brief's target word count (don't try to beat competitors)
- Follow brief outline exactly (no competitive intelligence)
- Flag in output: "[INFO] For best results, run /content_brief with SERP analysis first"
- Continue with brief-only data

---

### 12. **Target word count unrealistic (< 500 or > 5000)**
**Scenario:** Brief requests 300-word article or 6000-word guide

**Handling:**
- **< 500 words:**
  - Warning: "[WARNING] Very short article: {target_wc} words (SEO minimum: 1000)"
  - Recommend: "Short articles rarely rank — aim for 1000+ words"
  - Set minimum: 1000 words
- **> 5000 words:**
  - Warning: "[WARNING] Very long article: {target_wc} words (max recommended: 4000)"
  - Recommend: "Consider splitting into multi-part series or pillar page + cluster posts"
  - Cap at 4000 words
- Continue with adjusted target

---

## Error Handling Protocol

### **If `nlp_analyzer.py` fails:**
1. Read stderr output for error message
2. Common errors:
   - **ModuleNotFoundError (spacy, nltk)**: Run `pip install spacy nltk`
   - **FileNotFoundError (article text)**: Check file path is correct
   - **Timeout (long article)**: Reduce article length or increase timeout
3. Fallback: Skip automated checks, use manual checklist
4. Flag: "[WARNING] NLP analyzer unavailable — manual validation required"

### **If schema validation fails:**
1. Check JSON syntax with `jq` or online validator
2. Common errors:
   - Missing comma or bracket
   - Incorrect @type value
   - Missing required fields (headline, author, publisher)
3. Fallback: Use minimal Article schema only (skip FAQPage, BreadcrumbList)
4. Document: "[WARNING] Schema validation failed — using minimal Article schema"

### **If word counter fails:**
1. Use fallback: `wc -w article.md`
2. If still fails: Manually estimate (characters / 5)
3. Flag: "[INFO] Word count is estimated — verify manually"

---

## Performance Expectations

**Estimated execution time:**
- Brand kit load: 1-2 seconds
- Brief load: 1-2 seconds
- SERP data load (if exists): 2-3 seconds
- SEO package generation: 5-10 seconds
- Article writing: 60-120 seconds (depends on length)
- NLP validation: 10-20 seconds
- Final checks: 5-10 seconds

**Total: ~2-3 minutes** for 2000-word article generation

**If execution exceeds 5 minutes:**
- Check for tool hangs (NLP analyzer, external API calls)
- Skip optional validation steps
- Generate article with available data

---

## Notes

- **Human-first writing:** The AI writing guidelines are strict — follow them exactly
- **No summarizing conclusions:** Conclusions must have CTA, not summary
- **FAQ brevity:** Short answers (50-150 words) rank better for featured snippets
- **CTA specificity:** "Book a Demo" > "Learn More" > "Contact Us"
- **Schema importance:** Article + FAQPage schema increases rich result eligibility by 40%
- **Validation before delivery:** All quality gates must pass before presenting to user
