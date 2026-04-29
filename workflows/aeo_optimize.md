---
description: /aeo_optimize - Transform content for maximum AI search citability (ChatGPT, Perplexity, Gemini)
---

# Workflow: AEO/GEO Content Optimization

## Trigger
```
/aeo_optimize <url_or_topic> [--mode url|draft|topic]
```
**Examples:**
- `/aeo_optimize https://example.com/blog/seo-guide` - Optimize existing page
- `/aeo_optimize "growth marketing strategies" --mode topic` - Generate from scratch
- `/aeo_optimize .tmp/draft.md --mode draft` - Optimize draft content

---

## Objective

Transform content into **AI-search-optimized format** to maximize citability in:
- **ChatGPT Search** (300M+ weekly users, 70% AI search market share)
- **Perplexity** (15M+ daily users, research-focused)
- **Gemini** (fastest growing, Google Knowledge Graph integration)

**Success Metric**: AEO score ≥70/100 (use `tools/aeo_grader.py`)

**Expected Timeline**:
- First AI citation: 3-5 business days after publish
- Measurable traffic: 2-3 weeks
- Conversion uplift: 9x higher for AI-cited content vs uncited

---

## Prerequisites

**Before starting:**
1. Understand target query: What question will users ask AI engines?
2. Identify content type:
   - Informational (how-to, guides) → PERFECT for AEO
   - Comparison (vs, best) → GOOD for AEO
   - Transactional (pricing, buy) → NOT suitable for AEO
3. Have source content OR topic brief

**When NOT to use this workflow:**
- Product pages (focus on traditional SEO)
- Local business pages (use Entity SEO instead)
- Brand new sites (<3 months old - build traditional SEO first)
- Very niche topics (AI training data may be limited)

---

## Step-by-Step Execution

### Step 1: Fetch & Analyze Existing Content (if URL mode)

**If --mode url:**
```bash
# Fetch content
python tools/fetch_page.py --url {url} --output .tmp/aeo_original.html

# Run initial AEO score
python tools/aeo_grader.py --url {url} --output .tmp/aeo_score_before.json
```

**Validate score:**
```bash
cat .tmp/aeo_score_before.json | python -m json.tool | grep "overall_score"
```

**If score ≥70**: Content is already optimized, minimal changes needed
**If score <70**: Full optimization required

---

### Step 2: Extract Key Entities & Topics

**Purpose**: Identify core concepts to preserve during optimization

```bash
python tools/nlp_analyzer.py \
  --mode entities \
  --input .tmp/aeo_original.html \
  --output .tmp/entities.json
```

**Output format:**
```json
{
  "main_topic": "growth marketing",
  "entities": ["SEO", "conversion rate", "A/B testing"],
  "key_terms": ["funnel optimization", "customer acquisition"]
}
```

**Use entities to**:
- Maintain topical relevance
- Ensure schema markup accuracy
- Guide listicle/FAQ generation

---

### Step 3: Apply AEO Optimization Transformations

**Transform content using these 7 techniques:**

#### Transformation 1: Listicle Formatting

**Before:**
```
There are several strategies for growth marketing. Content marketing is important.
Paid advertising can accelerate results. Email nurturing keeps prospects engaged.
```

**After:**
```
## 5 Proven Growth Marketing Strategies

1. **Content Marketing** - Build organic traffic through blog posts, guides, and case studies
2. **Paid Advertising** - Accelerate customer acquisition with targeted Meta/Google ads
3. **Email Nurturing** - Convert prospects with automated drip campaigns
4. **Product-Led Growth** - Let the product sell itself with free trials
5. **Referral Programs** - Turn customers into advocates with incentive structures
```

**Rule**: Convert ≥3 sections to numbered lists where applicable

---

#### Transformation 2: Concise Answer Blocks

**AI engines prefer 50-75 word direct answers at the start of sections**

**Before:**
```
## What is Growth Marketing?

Growth marketing is an approach that many modern companies are using. It involves
testing different channels and tactics to find what works best. Companies that use
growth marketing often see better results than those using traditional marketing.
The key is to be data-driven and focus on the entire funnel, not just acquisition.
```

**After:**
```
## What is Growth Marketing?

Growth marketing is a data-driven approach that optimizes the entire customer journey—
from acquisition to retention—using rapid experimentation across channels. Unlike
traditional marketing's focus on top-of-funnel awareness, growth marketing tests and
scales tactics that impact every funnel stage, from signup to referral.

[Then continue with detailed explanation...]
```

**Rule**: Every H2 section starts with a 50-75 word answer block

---

#### Transformation 3: FAQ Schema with Prompt-Matched Questions

**Critical for Gemini and voice search**

**Identify common questions users ask AI:**
```
User asks ChatGPT: "How long does SEO take to work?"
User asks Perplexity: "What's the difference between SEO and SEM?"
User asks Gemini: "Is SEO worth it for small businesses?"
```

**Generate FAQ section:**
````markdown
## Frequently Asked Questions

### How long does SEO take to work?

SEO typically shows initial results in 3-6 months for new websites, with significant
traffic growth at 6-12 months. Established sites may see improvements in 4-8 weeks.
Timeline depends on competition, domain authority, and content quality.

### What's the difference between SEO and SEM?

SEO (Search Engine Optimization) is organic, unpaid ranking through content and
technical optimization. SEM (Search Engine Marketing) includes paid ads like Google Ads.
SEO has long-term ROI but slower results; SEM delivers immediate traffic but stops when
you stop paying.

### Is SEO worth it for small businesses?

Yes—small businesses with local focus can rank for "near me" and city-specific searches
within 3-6 months. Local SEO costs $500-$2,000/month vs $3,000-$10,000/month for paid ads
with equivalent traffic, making SEO more cost-effective long-term.

[Continue with 2-5 more FAQs...]
````

**Then generate FAQ schema:**
```bash
python tools/schema_gen.py \
  --type FAQPage \
  --data .tmp/faq_data.json \
  --output .tmp/faq_schema.json
```

**[WARNING] FAQPage schema is RESTRICTED** to government/healthcare since Aug 2023
**Use instead**: Article schema with "hasPart" for Q&A sections

**Rule**: Include 5-8 FAQs with prompt-matched questions

---

#### Transformation 4: Structured Comparison Tables

**AI engines cite tables heavily**

**Example: Tool comparison**
````markdown
## Best Growth Marketing Tools Comparison

| Tool | Best For | Pricing | Key Feature | Integration |
|------|----------|---------|-------------|-------------|
| HubSpot | All-in-one marketing | $800/mo | CRM + automation | Native to 500+ apps |
| Mailchimp | Email marketing | $20/mo | Email builder | Zapier |
| Google Analytics | Traffic analysis | Free | User behavior | Universal |
| Hotjar | UX optimization | $39/mo | Heatmaps + recordings | Tag Manager |
| SEMrush | SEO + content | $119/mo | Keyword research | API |
````

**Rule**: Include ≥2 structured tables per article

---

#### Transformation 5: Data Attribution & Citations

**AI engines value attributable data**

**Before:**
```
Most marketers see good results from content marketing.
```

**After:**
```
According to Content Marketing Institute's 2025 report, 72% of B2B marketers
rate content marketing as "effective" or "very effective," with the top 10%
seeing 7.8x higher ROI than average performers [1].

[1] https://contentmarketinginstitute.com/research/2025-benchmarks
```

**Rule**: Cite ≥3 data sources with attribution

---

#### Transformation 6: Clear Heading Hierarchy

**Structure for AI parsing**

````markdown
# Main Title (H1) - One per page

## Main Sections (H2) - 5-8 per article
Use for primary topics

### Subsections (H3) - 2-4 per H2
Use for supporting points

#### Detailed Points (H4) - Sparingly
Only when absolutely needed for clarity
````

**Rule**: Minimum 5 H2 headings with logical flow

---

#### Transformation 7: Freshness Signals

**AI engines prefer recent content**

**Add year mentions:**
```
- "Best Growth Marketing Strategies for 2026"
- "Updated March 2026"
- "2025-2026 industry benchmarks show..."
- "As of Q1 2026, the latest data indicates..."
```

**Rule**: Mention current year (2026) at least 3 times

---

### Step 4: Generate Optimized Version

**Apply all transformations to create AEO-optimized version**

**Save as:**
- `.tmp/aeo_optimized.md` (markdown)
- `.tmp/aeo_optimized.html` (HTML for CMS)

**Checklist before proceeding:**
- [CHECKLIST] ≥3 numbered lists or step-by-step sections
- [CHECKLIST] Every H2 starts with 50-75 word answer block
- [CHECKLIST] 5-8 FAQs with prompt-matched questions
- [CHECKLIST] ≥2 structured comparison tables
- [CHECKLIST] ≥3 data citations with sources
- [CHECKLIST] 5+ clear H2 headings
- [CHECKLIST] Current year mentioned ≥3 times
- [CHECKLIST] ≥2 images or multimedia elements

---

### Step 5: Re-Score with AEO Grader

**Run grader on optimized version:**
```bash
python tools/aeo_grader.py \
  --file .tmp/aeo_optimized.md \
  --output .tmp/aeo_score_after.json
```

**Compare before vs after:**
```bash
echo "Before: $(cat .tmp/aeo_score_before.json | python -m json.tool | grep overall_score | awk '{print $2}')"
echo "After: $(cat .tmp/aeo_score_after.json | python -m json.tool | grep overall_score | awk '{print $2}')"
```

**Quality Gates:**
- [CRITICAL] Overall score must be ≥70
- [CRITICAL] Improvement must be ≥20 points (if optimizing existing)
- [CRITICAL] ChatGPT score ≥70
- [CRITICAL] Perplexity score ≥65
- [CRITICAL] Gemini score ≥70

**If score <70**: Review recommendations and apply missing transformations

---

### Step 6: Generate Schema Markup

**Create Article schema with AEO enhancements:**

```bash
# Prepare metadata
cat > .tmp/article_metadata.json << EOF
{
  "headline": "Complete Guide to Growth Marketing in 2026",
  "author": {
    "name": "Expert Name",
    "url": "https://example.com/author/expert"
  },
  "datePublished": "2026-03-17",
  "dateModified": "2026-03-17",
  "publisher": {
    "name": "The Example Brand",
    "logo": "https://example.com/logo.png"
  },
  "mainEntity": {
    "@type": "FAQPage",
    "questions": [
      {
        "question": "How long does SEO take to work?",
        "answer": "SEO typically shows initial results in 3-6 months..."
      }
    ]
  }
}
EOF

# Generate schema
python tools/schema_gen.py \
  --type Article \
  --data .tmp/article_metadata.json \
  --output .tmp/article_schema.json
```

**[WARNING] Article Schema Requirements 2026:**
- **author** with name + URL (for E-E-A-T)
- **datePublished** + **dateModified** (for freshness)
- **publisher** with logo (for brand recognition)
- **mainEntity** for FAQ/Q&A integration
- **image** with ImageObject (for rich results)

---

### Step 7: Create Improvement Report

**Generate human-readable report for client:**

````markdown
# AEO Optimization Report

**Content**: {title}
**URL**: {url}
**Optimized**: {date}

## Results

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Overall AEO Score | 42 | 78 | +36 |
| ChatGPT Score | 38 | 82 | +44 |
| Perplexity Score | 35 | 75 | +40 |
| Gemini Score | 50 | 77 | +27 |

## Transformations Applied

1. [OK] Converted 4 sections to numbered lists
2. [OK] Added 50-75 word answer blocks to 6 H2 sections
3. [OK] Created FAQ section with 7 prompt-matched questions
4. [OK] Added 3 structured comparison tables
5. [OK] Cited 5 data sources with attribution
6. [OK] Improved heading hierarchy (8 H2 headings)
7. [OK] Added 2026 freshness signals (mentioned 4 times)
8. [OK] Added 3 images with descriptive alt text

## Expected Impact

- **First AI Citation**: 3-5 business days after publish
- **Citation Rate Estimate**: 25-35% (based on 78/100 score)
- **Conversion Uplift**: 7-9x higher vs uncited content
- **Organic Traffic**: +15-25% within 8 weeks

## Next Steps

1. Publish optimized version to CMS
2. Add Article schema to <head>
3. Submit to Google Search Console for re-indexing
4. Monitor AI citations:
   - ChatGPT: Search "[topic]" and check if cited
   - Perplexity: Ask question, check sources
   - Gemini: Check AI Overview in Google

5. Track AI referral traffic:
   - Direct traffic spike (AI engines don't pass referrer)
   - Monitor bounce rate (AI traffic = 40-60% lower bounce)
   - Track conversions (AI traffic converts 9x better)

## Maintenance

- Update content every 3-6 months to maintain freshness
- Re-run AEO grader quarterly
- Monitor citation rate monthly
- Add new FAQs based on search queries
````

**Save as**: `reports/{client}_AEO_Report_{date}.md`

---

## Edge Cases & Handling

### Edge Case 1: Content is Already AEO-Optimized

**Scenario**: Initial score ≥70

**Action**:
- Run optimization anyway (marginal gains)
- Focus on freshness updates (new year, new data)
- Add emerging FAQs from search trends
- Enhance existing tables with new comparisons

**Output**: "Content already well-optimized. Applied freshness updates and marginal improvements. Score improved from 72 → 79."

---

### Edge Case 2: Content is Too Short (<500 words)

**Scenario**: Original content <500 words

**Action**:
1. STOP optimization
2. Alert user: "[WARNING] Content too short for effective AEO. Minimum 500 words required."
3. Recommend:
   - Expand with detailed examples
   - Add case studies
   - Include step-by-step tutorials
   - Incorporate data/statistics

**Do not proceed until content ≥800 words**

---

### Edge Case 3: Highly Technical/Niche Topic

**Scenario**: Topic with limited AI training data (e.g., "Kubernetes ingress controllers")

**Action**:
1. Optimize anyway (future-proofing)
2. Add extra data citations (AI engines rely on these for niche topics)
3. Include comparison tables (helps AI structure knowledge)
4. Lower score expectations (60-70 vs 70-80)
5. Alert user: "[INFO] Niche topic may have lower initial citation rate. Focus on traditional SEO + AEO hybrid strategy."

---

### Edge Case 4: Transactional Content (Pricing, Product Pages)

**Scenario**: User tries to optimize product page

**Action**:
1. STOP workflow
2. Alert: "[ERROR] Transactional content not suitable for AEO. AI engines cite informational content, not sales pages."
3. Recommend alternative:
   - Create informational blog post about the product category
   - Link from blog post to product page
   - Example: Instead of optimizing "/pricing", create "/blog/best-crm-pricing-models" that links to pricing

**Do not optimize transactional pages**

---

### Edge Case 5: Local Business Content

**Scenario**: Content about local services (e.g., "plumbers in Austin")

**Action**:
1. Alert: "[WARNING] Local business content should use Entity SEO workflow, not AEO."
2. Recommend: Run `/entity_audit` instead
3. If user insists: Optimize with local data focus
   - Add local statistics
   - Include city-specific FAQs
   - Mention local landmarks
   - Cite local regulations/laws

---

### Edge Case 6: No FAQ Candidates Identified

**Scenario**: Content topic doesn't have obvious FAQs

**Action**:
1. Search "[topic] questions" on Google
2. Check "People Also Ask" box
3. Use `tools/serp_scraper.py --mode autosuggest --keyword "{topic}"`
4. Generate 3-5 FAQs from search suggest ions
5. If still no FAQs: Use "Common Misconceptions" section instead

---

### Edge Case 7: Client Doesn't Have Data to Cite

**Scenario**: No original research or data

**Action**:
1. Find industry reports (free: HubSpot, Gartner, Forrester)
2. Use tools/serp_scraper.py to find competitor data
3. Cite government statistics (census.gov, bls.gov)
4. Quote academic research (Google Scholar)
5. Reference platform data (Google Trends, Similar Web)

**Minimum**: Cite 3 external authoritative sources

---

### Edge Case 8: Content Updated Frequently (News/Trends)

**Scenario**: Content about rapidly changing topics

**Action**:
1. Optimize as normal
2. Add "Last Updated: {date}" at top
3. Set calendar reminder for monthly updates
4. Create reusable template for quick updates
5. Focus on evergreen FAQs vs time-sensitive data

**Recommendation**: Don't AEO-optimize time-sensitive news (focus on speed over optimization)

---

## Quality Gates Checklist

Before marking workflow complete, verify ALL of these:

**Content Structure:**
- [CHECKLIST] Word count ≥800
- [CHECKLIST] ≥5 H2 headings
- [CHECKLIST] ≥3 numbered lists or step-by-step sections
- [CHECKLIST] All H2 sections start with 50-75 word answer block

**AEO Elements:**
- [CHECKLIST] FAQ section with 5-8 questions
- [CHECKLIST] ≥2 structured comparison tables
- [CHECKLIST] ≥3 data citations with source attribution
- [CHECKLIST] Current year (2026) mentioned ≥3 times

**Technical:**
- [CHECKLIST] AEO score ≥70/100
- [CHECKLIST] Article schema generated
- [CHECKLIST] Images have descriptive alt text
- [CHECKLIST] All links open in new tab (external) or same tab (internal)

**Quality:**
- [CHECKLIST] Content reads naturally (not over-optimized)
- [CHECKLIST] Human review completed (not 100% AI-generated)
- [CHECKLIST] Matches brand voice (check `clients/{client}/brand_kit.json`)
- [CHECKLIST] CTA included (book call, download guide, etc.)

---

## Output Deliverables

**For every `/aeo_optimize` execution, deliver:**

1. **Optimized Content** - `.tmp/aeo_optimized.md` + `.tmp/aeo_optimized.html`
2. **AEO Score Report** - `.tmp/aeo_score_after.json`
3. **Before/After Comparison** - `.tmp/aeo_comparison.json`
4. **Schema Markup** - `.tmp/article_schema.json`
5. **Improvement Report** - `reports/{client}_AEO_Report_{date}.md`

**Present to user:**
```
[OK] AEO Optimization Complete

Overall Score: 42 → 78 (+36 points)

Platform Scores:
- ChatGPT:    38 → 82 (+44)
- Perplexity: 35 → 75 (+40)
- Gemini:     50 → 77 (+27)

Transformations Applied:
- 4 listicle sections
- 7 FAQs with prompt matching
- 3 comparison tables
- 5 data citations
- Freshness signals added

Expected Impact:
- First citation: 3-5 days
- Citation rate: 25-35%
- Traffic uplift: +15-25% (8 weeks)
- Conversion: 7-9x higher

[FILE] Optimized content: .tmp/aeo_optimized.md
[FILE] Schema markup: .tmp/article_schema.json
[FILE] Report: reports/{client}_AEO_Report_{date}.md

Next: Publish to CMS and monitor AI citations.
```

---

## Monitoring & Measurement

**How to track AEO success:**

### Week 1-2: Citation Detection
```bash
# Manual check
1. Ask ChatGPT: "[topic question]"
2. Check if your content is cited
3. Ask Perplexity: "[topic question]"
4. Check "Sources" section for your URL
5. Google search: "[topic]"
6. Check if AI Overview cites you
```

### Week 3-4: Traffic Analysis
```bash
# GSC check
python tools/mcp-gsc/gsc_server.py \
  --function get_search_analytics \
  --site "https://example.com" \
  --start-date "2026-03-01" \
  --end-date "2026-03-31"

# Look for:
# - Direct traffic spike (AI engines don't pass referrer)
# - Lower bounce rate on AEO-optimized pages
# - Higher time on page
# - Better conversion rate
```

### Month 2-3: ROI Calculation
```
Citation Rate = (Pages cited / Total pages optimized) × 100
Traffic Uplift = (Post-AEO traffic - Pre-AEO traffic) / Pre-AEO traffic × 100
Conversion Uplift = (Post-AEO conversions / Pre-AEO conversions) - 1
ROI = (Revenue from AI traffic / Cost to optimize) × 100
```

**Benchmark targets:**
- Citation rate: 20-30% (good), 30-40% (excellent)
- Traffic uplift: +15-25% (8-12 weeks)
- Conversion uplift: 5-9x vs uncited
- ROI: 300-500% (first year)

---

## Integration with Other Workflows

**This workflow integrates with:**

### `/content_draft`
- Run AEO optimization on all new content before publish
- Add to content brief: "Must achieve AEO score ≥70"

### `/audit`
- Audit existing content for AEO readiness
- Prioritize low-score pages for optimization
- Include AEO section in audit reports

### `/monthly_report`
- Track citation rate month-over-month
- Report AI traffic separately from organic
- Include AI platform breakdown (ChatGPT vs Perplexity vs Gemini)

### `/keyword_research`
- Identify FAQ-worthy questions for AEO
- Find "People Also Ask" queries
- Generate prompt-matched question list

---

## Tools Used in This Workflow

| Tool | Purpose | Required |
|------|---------|----------|
| `tools/aeo_grader.py` | Score content for AI citability | YES |
| `tools/fetch_page.py` | Retrieve existing content | Optional |
| `tools/nlp_analyzer.py` | Extract entities and topics | Optional |
| `tools/schema_gen.py` | Generate Article/FAQ schema | YES |
| `tools/serp_scraper.py` | Find FAQ questions | Optional |

---

## Maintenance Schedule

**How often to re-optimize:**

| Content Type | Update Frequency | Reason |
|--------------|------------------|--------|
| Evergreen guides | Every 6 months | Refresh data, add new FAQs |
| Industry trends | Every 3 months | Stay current, update stats |
| Tool comparisons | Every quarter | New tools, pricing changes |
| How-to tutorials | Annually | Process improvements |
| News/timely | Weekly/daily | Freshness critical |

**Trigger re-optimization if:**
- AEO score drops below 65
- Competitor content outranks you in AI citations
- Major platform change (new AI engine launches)
- Significant topic evolution (new best practices)

---

## Success Stories (Example Benchmarks)

**Case Study 1: SaaS Company - CRM Guide**
- Before AEO: 42/100 score, 0 citations
- After AEO: 81/100 score
- Results: Cited in ChatGPT within 4 days, Perplexity within 7 days
- Traffic: +38% in 6 weeks
- Conversions: 11x higher from AI traffic vs organic

**Case Study 2: Agency - Growth Marketing Guide**
- Before AEO: 35/100 score, 0 citations
- After AEO: 76/100 score
- Results: Cited in Gemini AI Overview within 3 days
- Traffic: +22% in 8 weeks
- Lead generation: 7x higher close rate from AI referrals

**Case Study 3: E-commerce - Product Category Guide**
- Before AEO: 28/100 score (pure product descriptions)
- After AEO: Created informational guide (68/100 score)
- Results: Cited in ChatGPT Shopping recommendations
- Traffic: +31% to category pages (via blog link)
- Revenue: +$42K in 3 months from AI-driven traffic

---

**END OF WORKFLOW**

**Expected Execution Time**: 45-90 minutes per article (depending on length and complexity)

**Skill Level Required**: Intermediate (understanding of SEO + content optimization)

**Prerequisites**: AEO grader tool, schema generator, basic content writing skills
