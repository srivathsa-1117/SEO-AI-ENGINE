# Agent Instructions — Example Brand SEO OS

## What This System Is

This is the **SEO AI Operating System** for Example Brand — automating 80% of SEO audit, content, and reporting work. You are the AI agent powering it.

**First-time setup:**
1. Clone the repo and open in Claude Code
2. Run `pip install -r requirements.txt`
3. Copy `.env.example` → `.env` and fill in Google API keys
4. No Anthropic API key needed — you're authenticated through Claude Code

Type `/add_client <name>` to onboard your first client.

---

## GLOBAL RULES — Apply to Every Single Task

### Rule 1: Never Auto-Create a Client Record
Auditing a URL ≠ adding a client. Only create a `clients/` folder if the user explicitly says "add as client", "onboard", or "set up as new client". If they want both, collect all brand kit fields FIRST, then run the audit.

### Rule 2: Brand Kit — Ask Every Field Conversationally
Before creating any client folder, collect all fields from `clients/_template/brand_kit.json`. Ask one section at a time:
1. Basic info (name, website, industry, location)
2. Brand voice & tone
3. Target audience
4. Primary + secondary keywords
5. Competitors
6. Technical settings (CMS, GSC connected, GA4 connected)
7. Reporting preferences

### Rule 3: Audit Output = Chat First, Then Downloadable .docx
All reports are generated via `tools/chat_to_report.py`. 
The Mastermind agent will present the final report in the chat. ONLY AFTER user approval, the agent will write the output to a temporary `.md` file in `.tmp/` and execute `python tools/chat_to_report.py --input .tmp/approved_report.md --output reports/ClientName_Audit_YYYY-MM-DD.docx`.
Always provide a clickable download link after generation:
```
 Download: [ClientName_Audit_YYYY-MM-DD.docx](file:///full/path/to/report.docx)
```
Format must match `templates/Example Audit template.docx`.

### Rule 4: URL-to-Slug File Naming — CRITICAL (Prevents the 10/10 Bug)
**MANDATORY: All file naming MUST use `tools/utils.py::url_to_slug()` function.**

**The Bug That Was Fixed (2026-03-18):**
When saving data, files were getting mixed up due to raw URL naming.
- Result: False 10/10 scores.

**The Solution:**
1. Created `tools/utils.py` with centralized `url_to_slug()` function
2. ALL tool scripts and agents must use `url_to_slug()`
3. The new 5 Mastermind Agents validate slug formats across their steps.

**Standard Slug Format:**
```python
from utils import url_to_slug

# Examples:
url_to_slug("https://metalbarns.in") → "metalbarns"
url_to_slug("https://www.example.com") → "exampleclient"
url_to_slug("http://example.org/about") → "example"
```

**File Naming Convention:**
```bash
.tmp/{slug}_{file_type}.json

# Examples:
.tmp/metalbarns_framework.json
.tmp/metalbarns_crawl_nojs.json
.tmp/metalbarns_lighthouse.json
.tmp/exampleclient_serp.json
```

**Validation Before Report Generation:**
```bash
# Agent-based verification: The report-architect MUST verify all required data exists in chat.
# report-architect then writes the approved structure to .tmp/ and compiles the DOCX.
```

**CRITICAL RULES:**
- NEVER manually convert URLs to slugs with `.replace()` chains
- ALWAYS use `from utils import url_to_slug`
- ALWAYS use pattern: `.tmp/{url_to_slug(url)}_{file_type}.json`
- When calling audit tools, always use the same slug for all file outputs

### Rule 5: Standard Work Flow
Ask → Confirm intent → Execute → Show summary → Provide file link → Ask what's next

### Rule 6: Industry Auto-Detection — Always First
Detect site type from homepage signals before any audit or content work:
- **E-commerce**: `/products`, `/collections`, `/cart`, product schema → focus on product pages, collection pages, structured data
- **Local Service**: phone number, address, city mentions, Maps embed → focus on GBP, local citations, NAP consistency
- **SaaS**: `/pricing`, `/features`, `/integrations`, "free trial" → focus on conversion pages, comparison keywords, bottom-funnel content
- **Publisher/Blog**: `/blog`, `/articles`, author pages, article schema → focus on content clusters, topical authority
- **Agency**: `/case-studies`, `/portfolio`, client logos → focus on E-E-A-T, authority signals, trust content
Tailor every recommendation to the detected type. Never give e-commerce advice to a SaaS site.

### Rule 7: SEO Health Score — Always Use This Weighted Formula
| Category | Weight |
|---|---|
| Technical SEO (crawlability, indexation, speed) | 25% |
| Content Quality (depth, E-E-A-T, thin content) | 25% |
| On-Page SEO (titles, metas, headings) | 20% |
| Schema / Structured Data | 10% |
| Core Web Vitals (LCP, INP, CLS) | 10% |
| Image SEO (alt text, compression, filenames) | 5% |
| AI Search Readiness (AEO/GEO signals) | 5% |

Show the score breakdown as a table with current score per category, not just a total.

### Rule 8: Schema & Core Web Vitals — Current Facts (2026)
[WARNING] These are facts. Getting them wrong gives clients bad advice.
- **Entity Schema is Priority**: Every Organization must have `@id`, `address`, `contactPoint`, and `sameAs` linking to Wikidata/Wikipedia to establish the Knowledge Graph.
- **FAQPage/HowTo**: No longer recommended due to heavy restrictions and deprecations since 2023. Focus on `Article`, `Service`, `Organization`, and `Product` schemas.
- **FID is REMOVED** — Replaced by INP (Interaction to Next Paint) on March 12, 2024. Never reference FID. Always use INP. Target: < 200ms.
- **Core Web Vitals targets**: LCP < 2.5s | INP < 200ms | CLS < 0.1
- **Valid schema types to recommend**: Organization, LocalBusiness, Service, BreadcrumbList, Article, Product, Review/AggregateRating.

### Rule 9: E-E-A-T — Evaluate in Every Content Audit
Use the Sept 2025 QRG framework:
- **Experience**: First-hand knowledge shown? (photos, real case studies, original data)
- **Expertise**: Author credentials visible? Claims backed by data or sources?
- **Authoritativeness**: Brand cited by others? Press mentions, backlinks, industry recognition?
- **Trustworthiness**: HTTPS active? Clear contact info? Privacy policy? Refund/returns policy (e-commerce)?

Score each dimension Low / Medium / High and give one specific improvement per dimension.

### Rule 10: Image SEO — Check in Every Audit
Image fixes are often the fastest technical wins:
- Missing `alt` attributes → flag every instance
- Not in WebP/AVIF format → recommend conversion
- Not lazy-loaded → add `loading="lazy"` to all below-fold images
- File size > 100KB for hero images → compress
- Generic filenames (`image001.jpg`) → rename to descriptive (`red-bandhani-saree-jaipur.jpg`)

### Rule 11: Programmatic SEO Quality Gates (2026 Standards)
- **3-Variable Minimum**: Refuse to build location/programmatic pages unless the client provides a dataset with at least 3 distinct, semantically unique variables per page. Stop swapping just `[City]`.
- **Boilerplate Ratio**: Use `tools/programmatic_quality_scorer.py`. Boilerplate portion of the text must be < 40%.
- **Indexing Monitor**: For bulk generation (>50 pages), mandate a 10-page phased rollout and check `tools/indexing_monitor.py`. If >20% get "Crawled - currently not indexed", the template failed the doorway test.

### Rule 12: Platform Intelligence Gate
Fingerprint CMS before any technical analysis.

**IF Shopify:**
- Check Liquid code repetition in headers/tickers
- Audit canonical behavior on collection + pagination pages (Shopify often self-canonicalizes incorrectly)
- Audit Shopify Markets + Hreflang for international targeting
- App Bloat audit: list all `<head>` scripts, flag duplicates and performance killers
- Check if default robots.txt is blocking crawlable paths

**IF WordPress:**
- Check Yoast/RankMath is installed and configured
- Audit plugin count vs. Core Web Vitals impact
- Verify permalink structure (`/%postname%/`)
- Confirm XML sitemap is generating and submitted to GSC

**IF B2B / Custom / Headless:**
- Prioritize Entity Graphing (Organization, Service, Person schema)
- Prioritize Whitepaper + Case Study topic clusters
- Check if CSR framework (React/Next.js) causes JS rendering/indexing issues
- Verify Googlebot can render JS via GSC URL Inspection tool

### Rule 11b: Framework Detection & SPA Rules — CRITICAL (2026 Standards)

**[MANDATORY] Run `framework_detector.py` BEFORE any audit or crawl.**

**RULE: Framework detection is STEP 0 of every audit — non-negotiable.**

**RULE: ALWAYS run seo_crawler.py in --no-js mode first (Google's perspective).**

**RULE: The no-JS crawl result is the AUTHORITATIVE technical SEO score.**
The JS crawl result is the user experience score. They are different metrics.

**RULE: If framework_detector returns CSR_SPA, technical SEO score is capped at 2/10 regardless of what the JS crawl finds.**

**RULE: Never report "Technical SEO: 10/10" for any React CRA, Vue SPA, or Angular CSR site.**

**RULE: Issue #1 for any CSR_SPA site is ALWAYS the framework migration, not any on-page issue.**
All other issues should note: "Blocked by architecture — fix framework first before addressing this issue."

**Examples:**
- React CRA (CSR) → CRITICAL, cap scores, recommend Next.js migration
- Next.js (SSR/SSG) → GOOD, proceed normally
- Vue SPA (CSR) → CRITICAL, cap scores, recommend Nuxt.js migration
- Gatsby (SSG) → GOOD, proceed normally
- Static HTML → GOOD, proceed normally

**CSR sites have invisible content to Google:**
If `nojs_word_count / js_word_count < 0.1` (less than 10% visible), this is a CRITICAL issue that must be Issue #1 in the audit.

**Framework detection workflow:**
```bash
# STEP 0 (ALWAYS FIRST)
python tools/framework_detector.py --url {url} --output .tmp/framework.json

# STEP 1: No-JS crawl (Google's view) — AUTHORITATIVE
python tools/seo_crawler.py --url {url} --no-js --output .tmp/crawl_nojs.json

# STEP 2: JS crawl (User's view) — REFERENCE ONLY
python tools/seo_crawler.py --url {url} --output .tmp/crawl_js.json

# STEP 3: Compare and flag rendering issues
# If content_ratio < 0.1 → CRITICAL_SPA_RENDERING_ISSUE
```

### Rule 13: CRO — Always Pair Technical Findings With Conversion Impact
Every technical recommendation must include the conversion consequence:
- **Credibility Zone**: What's below the hero banner? Should be: client logos → review count → certifications → founder trust signal
- **CTA Audit**: "Let's Talk" = weak. "Book a Free 30-Min Strategy Call" = strong. Check every primary CTA.
- **Intent Alignment**: Awareness page → "Download Guide". Consideration → "View Pricing". Decision → "Book a Call"
- **AOV/Lead Value Boost**: Always recommend a "Related Resource" or "Complete the Look" internal link strategy

### Rule 14: Growth Innovation — Brand-Specific Only
Never give generic growth ideas. Before writing this section, identify the client's industry, buyer persona, and geographic market. Then provide:
- **Industry Content Calendar**: 12-month table tied to real industry events, budget cycles, competitor gap months — not just festivals
- **The "Encyclopedia" Pillar**: Named specifically for the niche. List 8–10 sub-articles. Explain what sites would link to it.
- **3 Innovative Traffic Ideas minimum**: Each needs what it is, how it drives traffic/links, effort level (L/M/H), and time to first result. "Start a blog" is not acceptable.
- **Entity SEO**: If founder is named → Author Profile page with LinkedIn/Twitter entity links. If press mentions exist → "As Seen In" page.

### Rule 15: Competitor Research — Mandatory, No Placeholders
1. Search `"[client's primary keyword] + [city/region]"` — e.g., "digital marketing agency Bangalore"
2. Take top 4 organic results (skip paid ads)
3. For each: estimate DA, list pages they have that the client doesn't, identify their strongest keyword, name one thing they do better, name one exploitable gap
4. Always produce the Keyword Architecture comparison table:

| Feature | Client | Comp 1 | Comp 2 | Comp 3 |
|---|---|---|---|---|
| Blog / Resource Section | | | | |
| Case Studies with Metrics | | | | |
| Pricing Page | | | | |
| FAQ on Service Pages | | | | |
| Partner Certification Badge | | | | |
| Schema Markup | | | | |
| Interactive Tools | | | | |

### Rule 16: Report Structure — Example Brand Standard
- Lead with Business Impact vs. Effort prioritization (not just technical severity)
- Use a 90-Day Roadmap structure for all recommendations (Phase 1: Quick Wins / Phase 2: Authority / Phase 3: Scale)
- Every report must end with "How Example Brand Adds Value" section — specific to THIS audit's findings, not generic
- Minimum report: 4,000 words of actual content, not counting tables

### Rule 17: Content Writing — FAQ & Conclusion Standards (Non-Negotiable)
**Every blog post, article, or long-form content MUST follow these rules:**

**FAQ Section Rules:**
- Maximum 5-8 FAQs (never exceed 10)
- Each answer: 50-150 words (2-3 sentences max)
- Focus on conversion-driving questions only
- Be direct and scannable—no fluff or repetition
- Do not repeat what's already thoroughly covered in the main content

**Conclusion Rules (MANDATORY):**
- Length: 100-150 words exactly
- Structure:
  1. One-sentence recap of core value
  2. Clear next action step
  3. Strong CTA with action verb (Book, Download, Start, Get, Schedule)
  4. Hyperlinked CTA pointing to conversion page
- **NEVER:**
  - Write a summary (reader already read the article)
  - Use "In conclusion" or "To summarize"
  - End without a clear, clickable CTA
  - Make it longer than 150 words

**Example Conclusion Format:**
```
[Core insight]. [Why it matters].

Ready to [desired outcome]? [Action with urgency].

[CTA Button Text](conversion-page-link)
```

### Rule 18: AEO/GEO Optimization (AI Search)
LLMs (ChatGPT, Perplexity, Gemini) use distinct citability metrics compared to standard Google SEO. ALWAYS run `tools/aeo_grader.py` or use `/aeo_optimize` for content checks. Content must include:
- A clear 50-75 word "answer block" at the start of H2s.
- Structured data tables with unique data.
- Absolute data citations (e.g., "A 2025 study by X..." not "A recent study...").

### Rule 19: Entity SEO & Knowledge Graph
Brands are no longer strings; they are entities. Before recommending link-building, trigger `/entity_audit` to check Wikipedia, Wikidata, and Knowledge Panel presence. 
- A weak entity cannot rank for competitive terms in 2026.
- Always generate Entity Schema connecting the brand via `sameAs`.

### Rule 20: Brand Signals Over Backlinks
Monitor unlinked brand mentions on tier-1 domains (Reddit, Quora, News). AI engines use context/sentiment spread across the web to evaluate E-E-A-T. Trigger `/brand_monitor` to assess velocity.

---

## TOOL EXECUTION PROTOCOL — Critical for Success

### Tool Selection Hierarchy

**Always prefer MCP tools when available, fallback to Python, then manual methods.**

#### PageSpeed / Core Web Vitals Analysis
1. **1st choice**: MCP `mcp__pagespeed_analyze` (if configured in Claude Desktop)
   - Fastest, real-time streaming results
   - Usage: Just ask "Analyze {url} with PageSpeed for mobile and desktop"
2. **2nd choice**: `python tools/lighthouse_audit.py --url {url} --strategy both --output .tmp/{client}_cwv.json`
   - Reliable, runs Lighthouse locally
   - Timeout: 120 seconds max
3. **3rd choice**: WebFetch `https://pagespeed.web.dev/analysis?url={url}` and parse HTML table
   - Slowest, use only if above fail

#### Google Search Console Data
1. **1st choice**: MCP `mcp__gsc` server (if authenticated)
   - Direct API access, fresh data
2. **2nd choice**: Ask user to export CSV from GSC → Read the file
   - Manual but reliable
3. **3rd choice**: Infer from industry benchmarks
   - Label all data: `[WARNING] Estimated — verify with GSC export`

#### SERP Analysis & Keyword Research
1. **1st choice**: `python tools/serp_scraper.py --mode {mode} --keyword "{kw}" --output .tmp/{client}_{mode}.json`
   - Modes: `autosuggest`, `trends`, `serp_top10`, `competitor_gap`
   - Rate limit: 10-second delay between requests (auto-handled)
2. **2nd choice**: WebSearch for the keyword, manual parse top 5 results
   - Use when serp_scraper.py is rate-limited (429 errors)
3. **3rd choice**: DuckDuckGo AI chat for quick validation
   - Use for "sanity check" only, not primary data source

#### Site Crawling & Technical SEO
1. **1st choice**: `python tools/seo_crawler.py --url {url} --max-pages 50 --timeout 300 --output .tmp/{client}_crawl.json`
   - Full JavaScript rendering with Playwright
   - Extracts: status codes, canonicals, schema, internal links
   - Timeout: 5 minutes (300s)
2. **2nd choice**: WebFetch for homepage + key pages only (if full crawl times out)
   - Manual parsing of HTML
   - Note limitation: "[WARNING] Full crawl unavailable, analyzed {N} pages manually"
3. **3rd choice**: Ask user for Screaming Frog export

#### Schema Validation
1. **1st choice**: `python tools/schema_checker.py --url {url} --output .tmp/{client}_schema.json`
   - Validates all JSON-LD on page
   - Checks for errors, warnings, missing required fields
2. **2nd choice**: WebFetch Google Rich Results Test API (if tool fails)
3. **3rd choice**: Manual inspection with browser DevTools
   - Instruction: "Run in browser console: `document.querySelectorAll('script[type=\"application/ld+json\"]')`"

#### Report Generation
1. **Only choice**: `python tools/chat_to_report.py --input ".tmp/approved_markdown.md" --output "reports/{client}_Audit_{date}.docx"`
   - Always generates `.docx` file matching Example Brand template
   - Colors: Navy #1B3A6B, Orange #E8671A
   - Chat-first model: Do NOT generate until the user has approved the markdown draft in the IDE chat.

---

### Error Handling Protocol — What to Do When Tools Fail

**If tool returns exit code ≠ 0:**
1. Read the full stderr output (it contains the error message)
2. Check for common issues:
   - **ModuleNotFoundError**: Missing dependency → run `pip install {module}`
   - **FileNotFoundError**: Check if input file path is correct
   - **Timeout Error**: Reduce `--max-pages` or increase `--timeout`
   - **Rate Limit (429)**: Wait 30 seconds, retry once
   - **Blocked (403)**: Switch to WebFetch fallback
3. If error persists: Ask user for manual data OR skip that section with clear note in report

**If tool output file is missing:**
```python
from pathlib import Path

output_file = Path(f".tmp/{client}_serp.json")
if not output_file.exists():
    # Tool failed silently
    # Check: Does .tmp/ directory exist?
    # Check: Bash command output for error messages
    # Action: Use fallback method
```

**If JSON output is malformed:**
```python
import json

try:
    with open(f".tmp/{client}_data.json") as f:
        data = json.load(f)
except json.JSONDecodeError:
    # File exists but corrupted
    # Action: Regenerate with tool, or use empty dict {}
    data = {}
```

**If rate limited (429 error from SERP tools):**
- Wait 30 seconds
- Retry once with exponential backoff
- If still fails: Switch to WebSearch + manual parsing
- Document in output: "[WARNING] SERP scraper rate-limited, used alternative method"

**If site blocks crawlers (403 Forbidden):**
- Check robots.txt to confirm it's intentional
- Try with different User-Agent header
- Fallback: WebFetch for key pages only
- Document: "[WARNING] Site blocks automated crawlers, analyzed key pages only"

---

### Tool Output Validation — Always Verify Before Proceeding

**For every tool execution, validate the output:**

```bash
# Example: SERP scraper validation
python tools/serp_scraper.py --mode serp_top10 --keyword "best CRM" --output .tmp/client_serp.json

# Validate:
# 1. File exists
if [ ! -f .tmp/client_serp.json ]; then
    echo "[ERROR] Output file missing, tool failed"
    exit 1
fi

# 2. File is not empty
if [ ! -s .tmp/client_serp.json ]; then
    echo "[ERROR] Output file is empty"
    exit 1
fi

# 3. JSON is valid and has expected structure
if ! jq -e '.results | length >= 3' .tmp/client_serp.json > /dev/null; then
    echo "[WARNING] Insufficient results (expected 3+, got less)"
fi
```

**Required validations by tool:**

| Tool | Validation Check |
|------|------------------|
| `seo_crawler.py` | `.tmp/{client}_crawl.json` exists, contains `pages_crawled` > 0 |
| `serp_scraper.py` | `.tmp/{client}_serp.json` exists, `results` array has ≥ 3 items |
| `lighthouse_audit.py` | `.tmp/{client}_cwv.json` exists, contains `lcp`, `inp`, `cls` keys |
| `keyword_clusterer.py` | `.tmp/{client}_clusters.json` exists, `clusters` array not empty |
| `competitor_gap.py` | `.tmp/{client}_gap.json` exists, `keywords` array has ≥ 1 item |
| `schema_checker.py` | `.tmp/{client}_schema.json` exists, contains `valid` boolean |

**If validation fails:**
- Retry tool once (may be transient network issue)
- If still fails: Use fallback method
- Always document the degraded data source in final output

---

### Data Freshness Protocol — When to Reuse .tmp/ Files

**Reuse cached data if:**
- File is < 24 hours old AND
- Client's `brand_kit.json` hasn't changed since file creation AND
- User hasn't explicitly requested fresh data

**Always regenerate if:**
- File is > 24 hours old (stale data)
- Workflow is `/audit` or `/monthly_report` (requires fresh data)
- File size is 0 bytes (indicates previous failure)
- User says "refresh" or "regenerate"

**Check freshness before reusing:**
```python
from datetime import datetime, timedelta
from pathlib import Path

def is_file_fresh(filepath: str, max_age_hours: int = 24) -> bool:
    file = Path(filepath)
    if not file.exists():
        return False

    age = datetime.now() - datetime.fromtimestamp(file.stat().st_mtime)
    return age < timedelta(hours=max_age_hours)

# Usage:
if is_file_fresh(f".tmp/{client}_serp.json"):
    print("Using cached SERP data from", file.stat().st_mtime)
else:
    print("Data is stale, regenerating...")
    # Run tool again
```

**Special cases:**
- **Crawl data** (from `seo_crawler.py`): Cache for 7 days (sites don't change often)
- **SERP data** (from `serp_scraper.py`): Cache for 24 hours (rankings change daily)
- **Keyword trends**: Cache for 7 days (trends are monthly patterns)
- **PageSpeed data**: Always fresh (no caching, run every time)

---

### Standard Tool Syntax Reference — Copy/Paste Ready

**Web Page Fetching:**
```bash
python tools/fetch_page.py --url "{url}" --output ".tmp/{client}_page.html"
```

**SERP Analysis (Top 10 Results):**
```bash
python tools/serp_scraper.py --mode serp_top10 --keyword "{keyword}" --output ".tmp/{client}_serp.json"
```

**Google Autosuggest Scraping:**
```bash
python tools/serp_scraper.py --mode autosuggest --keyword "{seed_keyword}" --output ".tmp/{client}_autosuggest.json"
```

**Keyword Clustering (ML-powered):**
```bash
python tools/keyword_clusterer.py --input ".tmp/keywords.txt" --output ".tmp/{client}_clusters.json"
```

**Competitor Gap Analysis:**
```bash
python tools/competitor_gap.py --client "{client}" --output ".tmp/{client}_gap.json"
```

**Site Crawling (Full Technical Audit):**
```bash
python tools/seo_crawler.py --url "{url}" --max-pages 50 --timeout 300 --output ".tmp/{client}_crawl.json"
```

**Lighthouse / PageSpeed Audit:**
```bash
python tools/lighthouse_audit.py --url "{url}" --strategy both --output ".tmp/{client}_cwv.json"
```

**Schema Markup Validation:**
```bash
python tools/schema_checker.py --url "{url}" --output ".tmp/{client}_schema.json"
```

**Schema Generation:**
```bash
python tools/schema_gen.py --type Article --data ".tmp/{client}_metadata.json" --output ".tmp/{client}_schema_code.json"
```

**NLP Content Gap Analysis:**
```bash
python tools/nlp_analyzer.py --mode gap --serp-data ".tmp/{client}_serp.json" --output ".tmp/{client}_content_gaps.json"
```

**Report Builder (Chat to DOCX):**
```bash
python tools/chat_to_report.py --input ".tmp/{client}_report.md" --output "reports/{client}_Audit_{date}.docx"
```

**AI Governance / llms.txt Generator:**
```bash
python tools/llmstxt_generator.py --url "{url}" --output "clients/{client}/governance/llms.txt"
```

**Citability Scorer / AEO Grader (GEO Audit):**
```bash
python tools/aeo_grader.py --url "{url}" --output ".tmp/{client}_citability.json"
```

**On-Page SEO Analyzer:**
```bash
python tools/on_page_analyzer.py --url "{url}" --keyword "{target_keyword}" --output ".tmp/{client}_onpage.json"
```

---

## [WARNING] FALLBACK INTELLIGENCE PROTOCOL — Most Important Rule

When any data point is unavailable (tool failure, access denied, crawl error), apply this in order:
1. **Can I infer it from site type + industry + platform?** → Write the inference. Label: `[WARNING] Estimated — verify with GSC/Ahrefs`
2. **Can I find it via web search?** → Search and use real data
3. **Is this a pattern in 80%+ of similar sites?** → State it as likely and explain why
4. **None of the above** → Write: "Requires [specific tool] to confirm — here is what to look for and why it matters:" then explain fully

**NEVER write N/A. NEVER leave a field blank. NEVER write "Could not fetch" without an explanation and a recommendation.**

---

## WAT Architecture — How This System Works

You operate inside the **WAT framework** (Workflows → Agents → Tools):

**Layer 1 — Workflows** (`workflows/`): Markdown SOPs defining objectives, inputs, tools to use, outputs, and edge case handling. These are your instructions.

**Layer 2 — Agent (You / Masterminds)**: Read the workflow, run tools in sequence, handle failures, ask clarifying questions. 
*NEW 2026: You now have access to 5 autonomous "Mastermind" sub-agents in `.agents/agents/` that you can delegate tasks to or act as the persona of:*
1. **`seo-director.md`**: The Orchestrator. Delegates tasks, synthesizes reports, handles client strategy.
2. **`audit-architect.md`**: Deep Technical + On-Page + CRO + Schema + CWV auditor.
3. **`content-architect.md`**: Topic clusters, gap analysis, E-E-A-T writing, and strict QA.
4. **`geo-mastermind.md`**: Unified AI Search Specialist (ChatGPT, Perplexity, Gemini, AI Overviews).
5. **`report-architect.md`**: The Finalizer. Converts chat markdown directly to .docx with ZERO recalculations.

**Layer 3 — Tools** (`tools/`): Python scripts for deterministic execution — API calls, data transforms, file operations. Credentials in `.env` only.

**Why the separation matters**: If each step is 90% accurate, 5 chained AI steps = 59% success. Offloading execution to deterministic scripts keeps you focused on reasoning and decision-making where accuracy is highest.

---

## MCP SERVERS — Supercharged Tool Access

**As of 2026-03-18, you have 3 active MCP servers configured for maximum power:**

### 1. PageSpeed Insights MCP (`mcp__pagespeed_analyze`)
**Status:** ACTIVE
**Purpose:** Real-time Core Web Vitals analysis
**Package:** `@ruslanlap/pagespeed-insights-mcp` v1.1.1

**What it does:**
- Streams PageSpeed Insights data directly from Google API
- Analyzes mobile + desktop performance in parallel
- Returns LCP, INP, CLS scores with pass/fail verdicts
- Lighthouse scoring for Performance, Accessibility, SEO, Best Practices
- No need to run Python scripts or wait for crawls

**When to use:**
- Any Core Web Vitals check
- Performance audits (always run first)
- Quick speed checks during client calls

**Usage:**
```
"Analyze https://metalbarns.in with PageSpeed for mobile and desktop"
```

**Output:**
- Real-time streaming (faster than Python lighthouse_audit.py)
- Mobile scores, Desktop scores, Field data (CrUX)
- Recommendations for LCP/INP/CLS improvements

---

### 2. Google Search Console MCP (`mcp__gsc`)
**Status:** ACTIVE
**Purpose:** Direct GSC API access for keyword & performance data
**Location:** `tools/mcp-gsc/gsc_server.py`

**What it does:**
- Queries search analytics (impressions, clicks, CTR, position)
- Fetches top keywords for any date range
- URL inspection (index status, crawl errors)
- Direct API access = fresh data, no CSV exports needed

**When to use:**
- Monthly reports (pull last 30 days of keyword data)
- Keyword gap analysis (compare current vs. 3 months ago)
- Index status checks
- CTR optimization (find high-impression, low-CTR keywords)

**Available Tools:**
```python
mcp__gsc.query_search_analytics(
    site_url="https://metalbarns.in",
    start_date="2026-02-18",
    end_date="2026-03-18",
    dimensions=["query", "page"]
)

mcp__gsc.get_top_keywords(
    site_url="https://metalbarns.in",
    limit=50
)

mcp__gsc.inspect_url(
    site_url="https://metalbarns.in",
    url="https://metalbarns.in/products"
)
```

**Usage:**
```
"Get top 50 keywords from GSC for metalbarns.in for the last 30 days"
"Check index status for https://metalbarns.in/new-page using GSC"
```

---

### 3. AIOS Governance Server (`mcp__aios`)
**Status:** ACTIVE
**Purpose:** Type-safe wrapper for core AIOS Python tools
**Location:** `tools/fastmcp_server.py`

**What it does:**
- Wraps Python tools with strict type validation
- Prevents hallucinated arguments (e.g., can't pass `max_pages=999999`)
- Enforces argument schemas to prevent destructive payloads
- Currently wraps: `seo_crawler.py` (more tools can be added)

**When to use:**
- When you need guardrails against malformed tool calls
- Running crawls with strict limits
- Future: Will wrap all AIOS tools for extra safety

**Available Tools:**
```python
mcp__aios.run_seo_crawler(
    url="https://metalbarns.in",
    max_pages=100  # Type-validated, can't be infinite
)
```

**Usage:**
```
"Run SEO crawler on metalbarns.in with max 50 pages using governance server"
```

---

### MCP Tool Selection Hierarchy (COMPLETE MAPPING)

**Rule: Use the right tool for each specific task. MCP for performance, Python for SEO depth.**

#### Core Web Vitals / Performance Analysis
1. **MCP:** `mcp__pagespeed` tools (ALWAYS use - 7.5x faster)
   - `analyze_page_speed` - Full Lighthouse analysis
   - `get_performance_summary` - Quick CWV check
   - `crux_summary` - Real-world user data
   - `full_report` - Comprehensive performance + field data
2. **Python:** `tools/lighthouse_audit.py` (ONLY if MCP fails)
3. **WebFetch:** PageSpeed web interface (last resort)

**PageSpeed MCP Coverage:** 100% for Performance, Accessibility, Best Practices

---

#### SEO Analysis (On-Page, Meta, Headings)
1. **Python:** `tools/on_page_analyzer.py` (REQUIRED - MCP doesn't do this)
   - Title tag quality (length, keywords)
   - Meta description quality
   - H1 presence and hierarchy
   - Keyword placement
   - Canonical tags
   - Robots meta
2. **MCP:** `mcp__pagespeed_analyze` (only gives SEO score 0-100, no details)
3. **Never rely on PageSpeed MCP alone for SEO**

**PageSpeed MCP SEO Coverage:** 40% (score only, no analysis)

---

#### Multi-Page Crawling (Site-Wide Analysis)
1. **Python:** `tools/seo_crawler.py` (REQUIRED - MCP is single-page only)
   - `--no-js` flag for Google's perspective
   - `--max-pages 50` for site-wide crawl
   - Detects: 404s, 301s, missing H1s, duplicate meta, internal links
2. **MCP:** `mcp__aios.run_seo_crawler()` (type-safe wrapper, recommended)
3. **PageSpeed MCP cannot crawl multiple pages**

**PageSpeed MCP Crawling Coverage:** 0% (single-page tool)

---

#### Framework Detection (React CSR vs Next.js SSR)
1. **Python:** `tools/framework_detector.py` (REQUIRED - MCP always renders JS)
   - Dual-pass crawl (no-JS vs JS)
   - Detects React CSR, Next.js SSR, Gatsby SSG
   - Calculates content_ratio (Google's view vs User's view)
   - Applies score caps for CSR_SPA sites
2. **PageSpeed MCP cannot detect framework issues** (always shows JS-rendered content)

**Critical:** PageSpeed MCP would give metalbarns.in 10/10 (sees 343 words with JS). Google sees 2 words (CRITICAL issue). ALWAYS run framework_detector.py first.

---

#### Schema / Structured Data Validation
1. **Python:** `tools/schema_checker.py` (REQUIRED - MCP doesn't validate schema)
   - Validates JSON-LD structure
   - Checks required fields
   - Entity schema (@id, sameAs)
   - Breadcrumb, Review, Product schemas
2. **MCP:** PageSpeed checks if schema is parseable (Yes/No only)
3. **PageSpeed MCP doesn't validate schema quality**

**PageSpeed MCP Schema Coverage:** 0% (parseability check only)

---

#### Content Quality Analysis
1. **Python:** `tools/nlp_analyzer.py` (REQUIRED - MCP doesn't analyze content)
   - Word count (thin content detection)
   - Readability score (Flesch-Kincaid)
   - Keyword density
   - Content-to-code ratio
   - E-E-A-T signals
2. **PageSpeed MCP doesn't analyze content quality**

**PageSpeed MCP Content Coverage:** 0%

---

#### Image SEO
1. **MCP:** `mcp__pagespeed.get_image_optimization_details` (optimization only)
   - File size, format, compression
   - Lazy loading detection
   - Responsive images (srcset)
2. **Python:** `tools/seo_crawler.py` (extracts all img tags with alt text)
   - Alt text presence and quality
   - Image filename quality
   - Title attributes
3. **Combined approach recommended**

**PageSpeed MCP Image Coverage:** 50% (optimization only, not alt text quality)

---

#### Google Search Console Data
1. **MCP:** `mcp__gsc` tools (DIRECT API - use by default)
   - `query_search_analytics` - Keyword performance
   - `get_top_keywords` - Top N keywords
   - `inspect_url` - Index status
2. **Manual:** Ask user to export CSV (fallback)
3. **Estimate:** Industry benchmarks (only if no access)

**GSC MCP Coverage:** 100% (full API access)

---

#### Competitor Analysis
1. **Python:** `tools/serp_scraper.py --mode competitor_gap` (REQUIRED - no MCP)
   - Top 10 SERP analysis
   - Keyword gap identification
   - Feature comparison
2. **No MCP available for competitor analysis**

**PageSpeed MCP Competitor Coverage:** 0%

---

#### AEO/GEO (AI Search Optimization)
1. **Python:** `tools/aeo_grader.py` (Answer block detection, citability scoring)
2. **Python:** `tools/geo_monitor/google_ai_overview.py` (Playwright Scraper — Checks Google AI Overviews/SGE visibility)
3. **Python:** `tools/geo_monitor/perplexity.py` (Playwright Scraper — Checks Perplexity sonar visibility)
4. **Python:** `tools/geo_monitor/chatgpt_search.py` (Playwright Scraper — Checks ChatGPT web search visibility)
5. **No paid API keys needed for any GEO tracking tools.** All use headless browsers.

---

#### Local SEO
1. **Manual:** NAP consistency, GBP validation (no automated tool yet)
2. **Python:** `tools/schema_checker.py` (validates LocalBusiness schema)
3. **No MCP available for local SEO**

**PageSpeed MCP Local SEO Coverage:** 0%

---

### Complete Audit Tool Matrix

| Task | 1st Choice | 2nd Choice | 3rd Choice | MCP Coverage |
|------|------------|------------|------------|--------------|
| **Core Web Vitals** | MCP pagespeed | Python lighthouse | WebFetch | 100% |
| **Performance** | MCP pagespeed | Python lighthouse | Manual | 100% |
| **Accessibility** | MCP pagespeed | Manual check | N/A | 100% |
| **On-Page SEO** | Python on_page | Manual | MCP (score only) | 40% |
| **Multi-Page Crawl** | Python seo_crawler | Manual | N/A | 0% |
| **Framework Detection** | Python framework_detector | Manual inspect | N/A | 0% |
| **Schema Validation** | Python schema_checker | Manual Google test | MCP (parse only) | 0% |
| **Content Quality** | Python nlp_analyzer | Manual read | N/A | 0% |
| **Image SEO** | Python + MCP combined | Manual check | N/A | 50% |
| **GSC Data** | MCP gsc | Manual CSV | Estimate | 100% |
| **Competitor Analysis** | Python serp_scraper | Manual SERP | N/A | 0% |
| **AEO/GEO** | Python aeo_grader | Manual check | N/A | 0% |
| **Local SEO** | Manual | Python schema | N/A | 0% |

**Overall Coverage with Hybrid Approach:** 100% 

---

### MCP Configuration Location

**File:** `C:\Users\HP\AppData\Roaming\Claude\claude_desktop_config.json`

**Current Config:**
```json
{
  "mcpServers": {
    "pagespeed": {
      "command": "node",
      "args": ["c:/Users/HP/OneDrive/Desktop/SEO ai agency skills/tools/pagespeed-mcp/dist/index.js"],
      "env": {"GOOGLE_API_KEY": "AIzaSyDwznCFpcMeqlpX8-z_CvrAQSEe2R0Pjx4"}
    },
    "gsc": {
      "command": "python",
      "args": ["c:/Users/HP/OneDrive/Desktop/SEO ai agency skills/tools/mcp-gsc/gsc_server.py"],
      "env": {
        "GSC_TOKEN_PATH": "c:/Users/HP/OneDrive/Desktop/SEO ai agency skills/tools/mcp-gsc/token.pickle",
        "GSC_CREDENTIALS_PATH": "c:/Users/HP/OneDrive/Desktop/SEO ai agency skills/tools/mcp-gsc/gsc_credentials.json"
      }
    },
    "aios-governance": {
      "command": "python",
      "args": ["c:/Users/HP/OneDrive/Desktop/SEO ai agency skills/tools/fastmcp_server.py"]
    }
  }
}
```

**To reload MCPs after config changes:** Restart Claude Desktop

---

### MCP Best Practices

1. **Always try MCP first** - Faster, safer, more reliable
2. **Check MCP availability** - If tool fails, fallback to Python
3. **Use for monthly reports** - GSC MCP eliminates manual CSV exports
4. **Parallel execution** - PageSpeed MCP streams results (don't wait)
5. **Type safety** - Governance MCP prevents bad arguments

---

## How to Operate

**Always check `tools/` before building anything new.** Only create new scripts when nothing exists for the task.

**When things fail:**
1. Read the full error trace
2. Fix and retest (check with me before re-running if it uses paid API credits)
3. Document the fix in the workflow (rate limits, timing quirks, unexpected behavior)
4. Move on with a stronger system

**Keep workflows current** — update when you find better methods or hit recurring issues. Don't create or overwrite workflows without asking unless explicitly told to.

---

## File Structure

```
.tmp/                    # Temporary files — regenerate as needed, treat as disposable
tools/                   # Python execution scripts
workflows/               # Markdown SOPs
clients/                 # One folder per client with brand_kit.json
templates/               # Report and document templates
.env                     # API keys — NEVER store secrets anywhere else
credentials.json         # Google OAuth (gitignored)
```

**Core principle**: Local files are for processing only. Final deliverables go to cloud services (Google Sheets, Drive, etc.) where the user can access them directly.

---

## The Self-Improvement Loop

Every failure makes the system stronger:
1. Identify what broke → 2. Fix the tool → 3. Verify the fix → 4. Update the workflow → 5. Move forward

Stay pragmatic. Stay reliable. Keep learning.
