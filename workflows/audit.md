---
description: /audit - Run a complete SEO audit with framework detection, dual-pass crawl, competitor analysis, and local SEO (V2.1 - 2026 Standards)
---

# Workflow: SEO Audit V2.1 (2026 Standards)

## Trigger
```
/audit <client_name_or_url> [--competitors domain1.com,domain2.com] [--local] [--output path]
```

**Examples:**
- `/audit metalbarns.in --competitors epack.in,kaizenpeb.com --local`
- `/audit acme_corp`
- `/audit https://example.com --output .tmp/example_audit.docx`

---

## Objective
Perform a comprehensive SEO audit that:
1. **Detects SPA/CSR issues FIRST** (React CRA, Vue without SSR, etc.)
2. **Compares Google's perspective (no-JS) vs User perspective (JS)**
3. **Benchmarks against competitors**
4. **Includes local SEO if applicable**
5. **Produces a 4,000+ word, actionable report with 90-day roadmap**

---

## Quality Gates (Check BEFORE Report Generation)

Before generating the final DOCX via `chat_to_report.py`, verify:

- [ ] `framework_detector.py` was run and result is in `.tmp/framework.json`
- [ ] No-JS crawl was run and result is in `.tmp/crawl_nojs.json`
- [ ] If site is CSR_SPA: Issue #1 is framework migration (not on-page issue)
- [ ] Competitor section exists (if `--competitors` flag was passed)
- [ ] Strategic insights section has at least 4 industry-specific points (not generic "start a blog" advice)
- [ ] 90-day plan is in 3 phases (Foundation / Build-Out / Authority)
- [ ] AEO/GEO readiness section exists

**If any check fails:** Do NOT generate report yet. Collect missing data first.

---

## STEP 0: Framework Detection (CRITICAL - ALWAYS FIRST)

**Tool:** `tools/framework_detector.py`

**Purpose:** Detect if site uses client-side rendering (CSR) which makes content invisible to Google.

**Execute:**
```bash
python tools/framework_detector.py \
  --url "{url}" \
  --output ".tmp/{client}_framework.json"
```

**What this detects:**
- React CRA (CSR) vs Next.js (SSR/SSG)
- Vue SPA vs Nuxt.js
- Angular vs Angular Universal
- Content ratio: what % of content Google can actually see

**Parse result:**
```json
{
  "framework": "React CRA | Next.js | Gatsby | Vue | Nuxt | Static HTML",
  "render_mode": "CSR_SPA | SSR | SSG | STATIC",
  "seo_verdict": "CRITICAL | WARNING | GOOD",
  "nojs_word_count": 150,
  "js_word_count": 2500,
  "content_ratio": 0.06,
  "score_cap": {
    "technical_seo": 2,
    "reason": "Content invisible to Google due to CSR rendering"
  }
}
```

**Decision Tree:**
- **If `render_mode == "CSR_SPA"`:**
  - Set `technical_seo_max = 2/10`
  - Set `on_page_seo_max = 3/10`
  - Flag Issue #1 as: "CRITICAL — Client-Side React SPA: Site content is invisible to Google. Migrate to Next.js with SSR or SSG."
  - **Continue audit anyway** — document ALL issues so client knows full scope
  - Note in every section: "Blocked by architecture — fix framework first"

- **If `render_mode == "SSR" or "SSG" or "STATIC"`:**
  - Proceed normally
  - No score caps

- **If framework detection fails:**
  - Use fallback: assume worst-case (CSR_SPA)
  - Flag: "[WARNING] Framework detection failed — assuming CSR for safety"

**Save to:**
`.tmp/{client}_framework.json`

---

## STEP 1: Identity Baseline

**Goal:** Load client context to tailor audit findings.

**If client folder exists (`clients/{client_name}/`):**

```bash
# Read brand_kit.json
cat clients/{client_name}/brand_kit.json
```

**Extract:**
- Industry (e.g., "E-commerce", "Local Service", "SaaS", "B2B Agency")
- Services offered
- Target locations (for local SEO)
- Competitors listed
- Primary keywords

**If only URL provided (no client folder):**
- Detect industry from homepage signals:
  - `/products`, `/cart` → E-commerce
  - Phone number, address, Maps embed → Local Service
  - `/pricing`, `/integrations`, "free trial" → SaaS
  - `/case-studies`, client logos → Agency
- Note: "Standalone audit — no brand kit available"

**Industry detection matters because:**
- E-commerce = focus on product schema, collection pages, image SEO
- Local Service = focus on GBP, NAP consistency, LocalBusiness schema
- SaaS = focus on conversion pages, comparison keywords, bottom-funnel content
- Agency = focus on E-E-A-T, case studies, trust signals

---

## STEP 2: Site Architecture — Dual-Pass Crawl

**Goal:** Compare what Google sees (no-JS) vs what users see (JS).

### STEP 2A: No-JS Crawl (Google's Perspective) — AUTHORITATIVE

**Tool:** `tools/seo_crawler.py --no-js`

**Execute:**
```bash
python tools/seo_crawler.py \
  --url "{url}" \
  --max-pages 50 \
  --no-js \
  --output ".tmp/{client}_crawl_nojs.json"
```

**What this does:**
- Fetches pages using `requests` library (no JavaScript execution)
- This is what Googlebot sees if JS fails to render
- Extracts: titles, meta, H1s, canonicals, internal links, schema, word count

**THIS IS THE AUTHORITATIVE TECHNICAL SCORE.**

### STEP 2B: JS Crawl (User's Perspective) — REFERENCE ONLY

**Tool:** `tools/seo_crawler.py` (default mode with Playwright)

**Execute:**
```bash
python tools/seo_crawler.py \
  --url "{url}" \
  --max-pages 50 \
  --output ".tmp/{client}_crawl_js.json"
```

**What this does:**
- Renders JavaScript with Playwright (headless Chrome)
- Shows what users see in their browser
- This is NOT what Google reliably sees

### STEP 2C: Compare and Flag Critical Rendering Issues

**Logic:**
```python
for page in crawl_nojs["pages"]:
    page_url = page["url"]
    js_page = find_matching_page(crawl_js["pages"], page_url)

    if js_page:
        nojs_wc = page["word_count"]
        js_wc = js_page["word_count"]

        if nojs_wc > 0 and js_wc > 0:
            ratio = nojs_wc / js_wc

            if ratio < 0.1:
                flag_critical_issue({
                    "page": page_url,
                    "issue": "CRITICAL_SPA_RENDERING_ISSUE",
                    "nojs_words": nojs_wc,
                    "js_words": js_wc,
                    "ratio": ratio,
                    "recommendation": "Page has <10% content visible to Google. Implement SSR."
                })
```

**Save to:**
- `.tmp/{client}_crawl_nojs.json`
- `.tmp/{client}_crawl_js.json`
- `.tmp/{client}_rendering_comparison.json`

---

## STEP 3: Core Web Vitals & Performance

### 🚀 TOOL SELECTION HIERARCHY (2026 - MCP First)

**1st Choice: PageSpeed MCP** (if configured in Claude Desktop)
- **7.5x faster** than Python Lighthouse (5-8 seconds vs 45-60 seconds)
- Real-time streaming results
- Direct Google PageSpeed API access
- Parallel mobile + desktop analysis

**Execute:**
```
Ask Claude: "Analyze {url} with PageSpeed for mobile and desktop"
```

**What the MCP returns:**
- LCP, INP, CLS scores (mobile + desktop)
- Performance score (0-100)
- Accessibility score (0-100)
- Best Practices score (0-100)
- SEO score (0-100)
- List of opportunities (image optimization, render-blocking, etc.)
- List of diagnostics (critical request chains, JavaScript execution time, etc.)

**Save results:**
When MCP completes, manually save key metrics to `.tmp/{client}_cwv.json`:
```json
{
  "url": "https://example.com",
  "mobile": {
    "lcp": 2.3,
    "inp": 180,
    "cls": 0.08,
    "performance_score": 87,
    "opportunities": [...]
  },
  "desktop": {
    "lcp": 1.8,
    "inp": 120,
    "cls": 0.05,
    "performance_score": 92,
    "opportunities": [...]
  }
}
```

---

**2nd Choice: Python Lighthouse Tool** (fallback if MCP unavailable)

**Tool:** `tools/lighthouse_audit.py`

**Execute:**
```bash
python tools/lighthouse_audit.py \
  --url "{url}" \
  --strategy both \
  --output ".tmp/{client}_cwv.json"
```

**Note:** Takes 45-60 seconds per URL. Use MCP when possible for faster results.

---

### Performance Metrics (Same for Both Methods)

**What this checks:**
- **LCP** (Largest Contentful Paint): target < 2.5s
- **INP** (Interaction to Next Paint): target < 200ms — **NOT FID** (deprecated March 2024)
- **CLS** (Cumulative Layout Shift): target < 0.1
- Render-blocking scripts
- Unoptimized images
- Missing lazy loading

**Flag issues:**
- LCP > 2.5s → "HIGH: LCP is {lcp}ms, target < 2500ms. Optimize images and server response time."
- INP > 200ms → "HIGH: INP is {inp}ms, target < 200ms. Reduce JavaScript execution time."
- CLS > 0.1 → "HIGH: CLS is {cls}, target < 0.1. Add width/height to images and reserve space for ads."

**Run on top 5 pages:**
- Homepage
- Top service/product page
- Top blog post
- Contact page
- Pricing/conversion page

**Save to:**
`.tmp/{client}_cwv.json`

---

## STEP 4: On-Page SEO & E-E-A-T

**Tool:** `tools/on_page_analyzer.py`

**Execute:**
```bash
python tools/on_page_analyzer.py \
  --client "{client}" \
  --top 10 \
  --keyword "{primary_keyword}" \
  --output ".tmp/{client}_onpage.json"
```

**What this checks:**
- Title tags (50-60 chars, keyword present)
- Meta descriptions (120-160 chars, keyword present)
- H1 (exactly one per page, keyword present)
- H2/H3 hierarchy
- Image alt tags
- Internal linking
- Canonical tags
- Noindex tags

**E-E-A-T Scan:**
- Author bios present?
- Phone numbers visible?
- Trust signals (testimonials, certifications, badges)?
- Policy links (Privacy, Terms, Refund)?
- External citations to .edu/.gov/.org sources?

**CRO Analysis:**
- Contact info visible?
- CTAs clear and action-oriented?
- Credibility zone below hero (logos, reviews, certifications)?

**Save to:**
`.tmp/{client}_onpage.json`

## STEP 5: Schema & AEO Readiness

### STEP 5A: Schema Validation

**Tool:** `tools/schema_checker.py`

**Execute:**
```bash
python tools/schema_checker.py \
  --url "{url}" \
  --output ".tmp/{client}_schema.json"
```

**What this checks:**
- JSON-LD schema blocks present
- Valid schema types: Organization, LocalBusiness, Service, Article, Product, BreadcrumbList
- **WARNING:** Do NOT recommend FAQPage (restricted since Aug 2023) or HowTo (deprecated)
- Entity linking: `sameAs` pointing to Wikidata/Wikipedia?
- Required fields present (address, contactPoint for Organization)

**Flag missing schema:**
- No Organization schema → "MEDIUM: Add Organization schema to homepage with entity linking"
- No BreadcrumbList → "LOW: Add BreadcrumbList schema for better navigation understanding"
- Organization missing `sameAs` → "MEDIUM: Add entity validation via Wikipedia/Wikidata links"

### STEP 5B: AEO/GEO Readiness

**Check for AI citability:**

1. **Direct answer blocks:**
   - Does each key page have a 50-75 word answer block in the first 100 words?
   - Example: "What is {topic}? {clear 2-sentence answer with context}"

2. **llms.txt exists?**
   ```bash
   curl {url}/llms.txt
   ```
   - If 404: Recommend creating `/llms.txt` with site purpose, expertise, key content

3. **AI Share of Voice (manual check):**
   - Search primary keyword in ChatGPT, Perplexity, Claude
   - Is the client cited?
   - Position (1st, 2nd, 3rd mention, or not cited)?

4. **Structured data tables:**
   - Are there comparison tables, pricing tables, feature matrices?
   - AI engines prioritize tables with unique data

**Score AEO 0-10:**
- Direct answer blocks: 3 points
- llms.txt exists: 2 points
- AI citations found: 3 points
- Structured tables present: 2 points

**Save to:**
`.tmp/{client}_aeo.json`

### STEP 5C: Competitor Benchmarking (if `--competitors` flag)

**For each competitor domain:**

1. **Run framework detection:**
   ```bash
   python tools/framework_detector.py --url "{competitor_url}" --output ".tmp/{competitor}_framework.json"
   ```

2. **Check robots.txt and sitemap:**
   - Accessible?
   - How many URLs in sitemap?

3. **Count indexed pages:**
   ```
   site:competitor.com
   ```
   Note approximate count

4. **Check blog/content presence:**
   - Do they have a blog?
   - How many posts?
   - Post frequency?

5. **Check schema types:**
   ```bash
   python tools/schema_checker.py --url "{competitor_url}"
   ```

6. **Score them on same 9 dimensions as client:**
   - Technical SEO (framework, indexability)
   - On-Page SEO
   - Content Volume
   - Backlinks (estimated via domain metrics)
   - Portfolio/Social Proof
   - CTAs & Conversion Design
   - Mobile Experience
   - Blog/Content Marketing
   - Schema Implementation

8. **Write competitive insights:**
   - 3 bullets: "What {competitor} does better than {client}"
   - 1 bullet: "What {client} can replicate first (fastest win)"

**Competitor Scorecard Format:**

| Dimension | Client | Comp 1 | Comp 2 | Comp 3 |
|-----------|--------|--------|--------|--------|
| Technical SEO | 4/10 | 7/10 | 6/10 | 8/10 |
| On-Page SEO | 6/10 | 8/10 | 7/10 | 9/10 |
| Content Volume | 3/10 | 9/10 | 5/10 | 7/10 |
| Schema Markup | 2/10 | 6/10 | 4/10 | 7/10 |
| Blog Activity | 1/10 | 8/10 | 3/10 | 6/10 |
| Mobile Experience | 6/10 | 9/10 | 7/10 | 8/10 |
| E-E-A-T Signals | 4/10 | 7/10 | 6/10 | 8/10 |
| CTA Quality | 5/10 | 8/10 | 6/10 | 7/10 |
| Overall | 4.0 | 7.6 | 5.8 | 7.2 |

**Save to:**
`.tmp/{client}_competitors.json`

---

## STEP 6: Report Synthesis

**Agent Persona:** `report-architect.md`
**Tool:** `tools/chat_to_report.py`

**Process:**
1. The Audit Architect compiles all JSON finding summaries and writes the final Markdown report to the IDE chat.
2. The user reads the chat and approves it.
3. The report-architect saves the approved markdown to `.tmp/{client}_approved_audit.md`.
4. The report-architect runs the formatter:

```bash
python tools/chat_to_report.py --input ".tmp/{client}_approved_audit.md" --output "reports/{client}_Audit_{date}.docx"
```

**What this does:**
1. Eliminates math hallucinations (chat_to_report does absolutely zero math).
2. Uses template Example Brand styling.
3. Outputs `.docx` immediately for the client.

**Report MUST contain these sections in this order:**

### 1. Cover Page
- Client name
- Audit date
- 4 headline scores:
  - Technical SEO: X/10
  - On-Page SEO: X/10
  - Content Quality: X/10
  - Overall SEO Health: X/100

### 2. Executive Summary (3 paragraphs max)
- Paragraph 1: The #1 problem (framework/architecture if CSR, else biggest technical issue)
- Paragraph 2: The opportunity (what can be achieved if fixed)
- Paragraph 3: The first action (specific, measurable, achievable in 30 days)

**Example:**
```
Your website is built with Create React App (CSR), rendering all content via JavaScript.
This means Google sees an empty page with ~150 words, while users see 2,500+ words.
Your technical SEO score is capped at 2/10 until this is resolved.

Migrating to Next.js with SSR would make all content visible to Google, unlocking
ranking potential for 50+ keywords currently invisible to search engines. Competitors
using SSR rank 3-5 positions higher for the same keywords.

FIRST ACTION: Migrate homepage and top 5 service pages to Next.js SSR within 30 days.
Expected result: 200-300% increase in indexed content and improved crawl efficiency.
```

### 3. Company & Website Overview
- Industry
- Services
- Target audience
- Current tech stack (from framework detection)
- Render mode verdict

### 4. Full Audit Findings — ALL Issues Sorted by Severity

**Format:**
```
CRITICAL ISSUES (Fix immediately)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Issue #1: Client-Side React SPA Architecture
 Impact: 95% of content invisible to Google
 Fix: Migrate to Next.js with SSR or SSG
 Effort: 40 hours (2-3 weeks with developer)
 Business Impact: Unlocks ranking for 50+ keywords

Issue #2: Missing H1 Tags on 12/50 Pages
 Impact: Confuses Google about page topic
 Fix: Add exactly one H1 per page with target keyword
 Effort: 2 hours
 Business Impact: Improves ranking signals for affected pages

HIGH ISSUES (Fix within 30 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

...

MEDIUM ISSUES (Fix within 60 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

...

LOW ISSUES (Fix within 90 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

...
```

### 5. Competitor Analysis & Benchmarking Scorecard (if data exists)

**Include:**
- Side-by-side scorecard table
- For each competitor: "What they do better" (3 bullets)
- "What we can replicate first" (1 bullet per competitor)

### 6. Prioritized 90-Day Action Plan (3 Phases)

**Phase 1 (Days 1-30): Foundation**
- Fix CRITICAL issues
- Example tasks:
  - Migrate framework to Next.js SSR
  - Fix all missing H1s
  - Add Organization schema with entity linking
**Phase 2 (Days 31-60): Content Build-Out**
- Fix HIGH issues
- Example tasks:
  - Publish 4 articles targeting keyword gaps
  - Optimize top 10 pages for target keywords
  - Implement image lazy loading

**Phase 3 (Days 61-90+): Authority Building**
- Fix MEDIUM/LOW issues
- Off-page activities
- Example tasks:
  - Launch link building outreach (target 50 prospects)
  - Create llms.txt for AI engines
  - Add FAQ schema to top 5 pages
  - Set up monthly reporting automation

### 7. Keyword Strategy Map

**Format:**

| Keyword | Search Intent | Volume | Difficulty | Priority | Target Page |
|---------|---------------|--------|------------|----------|-------------|
| peb structure manufacturer nagpur | Transactional | 880 | 32 | HIGH | /peb-manufacturer-nagpur |
| pre engineered buildings cost | Commercial | 1200 | 45 | MEDIUM | /pricing |
| metal building suppliers india | Informational | 720 | 28 | MEDIUM | /blog/metal-building-suppliers |

**Include:**
- 20-30 keywords
- Mapped to specific URLs
- Prioritized by: (Volume × Intent Match) / Difficulty

### 8. Strategic Insights (4-6 INDUSTRY-SPECIFIC points)

**NOT GENERIC. Examples of GOOD strategic insights:**

**For PEB manufacturer:**
```
1. Target Infrastructure Projects: Government's ₹111 lakh crore National Infrastructure
   Pipeline includes 7,000+ projects requiring PEB structures for warehousing, logistics
   hubs, and industrial parks. Create location pages for each NIP project cluster.

2. Founder Credentials as Differentiation: Highlight 22 years of experience and ISO 9001
   certification prominently. Competitors lack this trust signal. Add founder bio page
   with entity linking.

3. Video SEO Gap: Zero competitors produce YouTube content. Create "PEB Structure
   Installation Timelapse" videos. These rank #1 on YouTube with minimal competition
   and build trust.

4. Pricing Content Gap: "peb structure cost per sq ft" has 1,200 monthly searches,
   zero good answers. Create detailed pricing guide with real project examples and ROI
   calculator.
```

**For SaaS:**
```
1. Bottom-of-Funnel Content Gap: Competitors rank for "[tool] vs [tool]" comparison
   keywords. You don't. Create 10 comparison pages targeting your top competitors.

2. Free Tool Strategy: Build a simple ROI calculator for [your niche]. Ranks for
   "calculator" queries, builds backlinks naturally, generates leads.

3. G2/Capterra Reviews: You have 8 reviews, competitors have 200+. Launch review
   campaign (target 50 reviews in 60 days). G2 badges boost conversion by 30%.
```

### 9. AEO/GEO Readiness — AI Search Optimization

**Include:**
- Current AI Share of Voice (cited in ChatGPT/Perplexity?)
- Missing schema for AI citability
- Direct answer block templates for top 3 queries
- llms.txt recommendation

**Example:**
```
Current AI Share of Voice: NOT CITED

When we searched ChatGPT for "best peb structure manufacturer in india", you were
not mentioned. Competitors Epack and Tata BlueScope were cited.

FIXES:
1. Create llms.txt at /llms.txt with:
   - Company expertise (ISO 9001, 22,000 sq ft facility)
   - Manufacturing capabilities
   - Key differentiators

2. Add direct answer blocks to top 3 pages:
   Page: /peb-structures
   Add: "What is a PEB structure? Pre-Engineered Buildings (PEB) are steel structures
   fabricated at a factory and assembled on-site, reducing construction time by 40%
   and costs by 30% compared to conventional construction."

3. Add comparison tables:
   Create "PEB vs Conventional Construction" table with hard data (time, cost,
   durability metrics). AI engines prioritize tables.
```

---

## Expected Outputs

### Files Created:
1. `.tmp/{client}_framework.json` — Framework detection result
2. `.tmp/{client}_crawl_nojs.json` — No-JS crawl (Google's view)
3. `.tmp/{client}_crawl_js.json` — JS crawl (User's view)
4. `.tmp/{client}_rendering_comparison.json` — Comparison
5. `.tmp/{client}_cwv.json` — Core Web Vitals
6. `.tmp/{client}_onpage.json` — On-page analysis
7. `.tmp/{client}_schema.json` — Schema validation
8. `.tmp/{client}_aeo.json` — AEO/GEO readiness
9. `.tmp/{client}_competitors.json` — Competitor benchmarking (if applicable)
11. `.tmp/reports/{client}_Audit_{date}.docx` — Final report

### User-Facing Deliverables:
1. Executive summary in chat (key highlights, top 3 issues, first action)
2. Downloadable .docx report (4,000+ words, professionally formatted)
3. Clickable download link: `📄 Download: [ClientName_Audit_YYYY-MM-DD.docx](file:///path/to/report.docx)`

---

## Error Handling

### If `framework_detector.py` fails:
- Assume worst-case: CSR_SPA
- Cap technical scores
- Flag: "[WARNING] Framework detection failed — assuming CSR for safety"
- Continue audit

### If no-JS crawl fails (403 Forbidden):
- Check robots.txt
- Try with different User-Agent
- Fallback: Use JS crawl only, note limitation
- Flag: "[WARNING] Site blocks Googlebot user-agent — may impact indexing"

### If lighthouse fails (no GOOGLE_API_KEY):
- Skip CWV section
- Flag: "[WARNING] Core Web Vitals unavailable — requires GOOGLE_API_KEY in .env"
- Recommend manual check via PageSpeed Insights

### If competitor URLs fail:
- Skip competitor section
- Note: "Competitor analysis unavailable — provide valid competitor domains for future audits"

---

## Performance Expectations

**Estimated execution time:**
- Framework detection: 30-45 seconds
- No-JS crawl (50 pages): 30-60 seconds
- JS crawl (50 pages): 60-120 seconds
- On-page analysis: 30-60 seconds
- Schema check: 10-15 seconds
- Lighthouse (5 pages): 60-90 seconds
- Competitor analysis (3 competitors): 120-180 seconds
- Report generation: 30-60 seconds

**Total: 6-10 minutes** for complete audit with competitors

**If execution exceeds 15 minutes:**
- Reduce `--max-pages` to 25
- Skip competitor analysis
- Generate report with available data

---

## Notes

- **Framework detection is NON-NEGOTIABLE** — must run first, always
- **No-JS crawl is authoritative** — this is what Google sees
- **JS crawl is reference only** — this is what users see
- **CSR sites get capped scores** — no exceptions, no matter how good on-page is
- **Competitor analysis is valuable** — provides context and benchmarks
- **Strategic insights must be specific** — no generic "start a blog" advice
- **90-day plan must be phased** — not a flat list of issues
