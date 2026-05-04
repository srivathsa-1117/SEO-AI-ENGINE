# Enterprise SEO AI Engine

**The most advanced AI-powered SEO operating system built for agencies, consultants, and growth teams.**

This system replaces an entire SEO team by combining deterministic Python data pipelines with the strategic intelligence of autonomous AI agents. Every audit, content brief, keyword cluster, and client report runs through a battle-tested architecture that eliminates guesswork and produces agency-grade deliverables in minutes — not days.

---

## Table of Contents

- [What This System Is](#what-this-system-is)
- [Why This Exists — The Problem It Solves](#why-this-exists)
- [WAT Architecture](#wat-architecture)
- [The 5 Master AI Agents](#the-5-master-ai-agents)
- [26+ Python Tools — Complete Reference](#python-tools-complete-reference)
- [24 Workflow SOPs](#24-workflow-sops)
- [MCP Servers — Supercharged Integrations](#mcp-servers)
- [Claude Code Skills](#claude-code-skills)
- [Schema Templates](#schema-templates)
- [Client Management System](#client-management-system)
- [SEO Health Scoring Formula](#seo-health-scoring-formula)
- [AI Search — GEO/AEO Engine](#ai-search-geoaeo-engine)
- [Framework Detection — The Critical Safety Net](#framework-detection)
- [Programmatic SEO Quality Gates](#programmatic-seo-quality-gates)
- [Platform Intelligence Gate](#platform-intelligence-gate)
- [Report Generation Pipeline](#report-generation-pipeline)
- [Quick Start Guide](#quick-start-guide)
- [Full File Structure](#full-file-structure)
- [API Integrations](#api-integrations)
- [System Effectiveness](#system-effectiveness)
- [Documentation Index](#documentation-index)
- [License](#license)

---

## What This System Is

The **Enterprise SEO AI Engine** is a complete, white-labeled AI operating system built to run inside Claude Code. It automates approximately 80% of the work an SEO agency does — from technical audits and keyword research to content writing, schema generation, and client reporting — through a coordinated stack of AI agents, Python scripts, and real-time API integrations.

This is not a chatbot wrapper or a prompt template collection. It is a production-grade software system with:

- **Deterministic data pipelines** — Python scripts handle all data collection, transformation, and file management. No hallucinated metrics.
- **Autonomous AI agents** — Five specialist modules that read workflows, execute tools, QA their own output, and synthesize findings.
- **Enterprise API integrations** — Google Search Console, Google PageSpeed Insights, DataForSEO, Hunter.io, and headless Playwright browsers.
- **White-label ready deliverables** — Every output is a branded Word document matching your agency's design system.
- **AI Search (GEO/AEO) built-in** — Dedicated tooling to track and improve visibility inside ChatGPT, Perplexity, and Google AI Overviews.

---

## Why This Exists

Traditional SEO work has three fundamental failure modes:

**1. Data fabrication** — AI agents left to reason without real data invent metrics, rankings, and scores. This system prevents this by separating data collection (deterministic Python) from data interpretation (AI reasoning). If a tool fails, the workflow fails loudly rather than silently hallucinating.

**2. Incomplete audits** — Most tools check one layer. A site can score 90/100 on PageSpeed and still be completely invisible to Google because it uses React CSR with no server-side rendering. This system's Framework Detection layer catches this before any other analysis runs, caps the technical score appropriately, and marks it as Issue #1.

**3. Unscalable delivery** — Producing a thorough SEO audit manually takes 8–12 hours per client. This system produces the same depth of analysis in 15–30 minutes, with a client-ready Word document ready for download immediately after approval.

---

## WAT Architecture

The system is organized in three layers. Each layer has a specific role, and the separation is intentional — it is what makes the system reliable at scale.

```
┌─────────────────────────────────────────────────────┐
│  LAYER 1 — WORKFLOWS                                 │
│  Markdown SOPs: objectives, inputs, outputs,         │
│  tool sequence, edge case handling                   │
└──────────────────────┬──────────────────────────────┘
                       │ reads
┌──────────────────────▼──────────────────────────────┐
│  LAYER 2 — AGENTS (You / Masterminds)                │
│  5 specialist AI modules: read workflows,            │
│  run tools, QA output, synthesize reports            │
└──────────────────────┬──────────────────────────────┘
                       │ executes
┌──────────────────────▼──────────────────────────────┐
│  LAYER 3 — TOOLS                                     │
│  26+ Python scripts: API calls, data transforms,     │
│  file operations, deterministic execution            │
└─────────────────────────────────────────────────────┘
```

**Why this matters:** If each AI step is 90% accurate, five chained AI steps yield only 59% reliability. By pushing execution to deterministic Python scripts, AI reasoning is reserved for interpretation and strategy — where it performs best.

---

## The 5 Master AI Agents

Each agent lives in `.agents/agents/` and operates as an autonomous specialist module. The SEO Director orchestrates the others.

### 1. SEO Director (`seo-director.md`)

The orchestrator and quality control layer. The SEO Director is your client-facing strategist.

**Responsibilities:**
- Reads brand kit and sets audit goals based on client context
- Delegates tasks to Audit Architect, Content Architect, and GEO Mastermind
- Reviews all sub-agent outputs for accuracy and internal consistency
- Synthesizes findings into an executive summary with a 90-day roadmap
- Handles client proposals, check-ins, and strategic communication
- Flags any hallucinated data before it reaches the client

**Key Outputs:** Executive summary, prioritized 90-day roadmap, client-ready proposals

---

### 2. Audit Architect (`audit-architect.md`)

The technical and on-page auditor. Runs the most tool-heavy workflows in the system.

**Responsibilities:**
- **Technical SEO:** crawlability, indexation, 404s, redirect chains, robots.txt, XML sitemaps, canonical tags
- **On-Page SEO:** title tag quality and length, meta description analysis, H1/H2/H3 hierarchy, keyword placement, internal linking structure
- **CRO & UX:** trust signal placement, CTA copy quality, above-the-fold analysis, mobile experience
- **Schema Markup:** validates all JSON-LD on the page, checks required fields, identifies missing entity connections
- **Core Web Vitals:** LCP, INP, CLS scoring with mobile and desktop breakdowns, improvement recommendations
- **Image SEO:** alt text coverage, file format audit (WebP/AVIF compliance), lazy loading, file size, filename quality

**Tools invoked:** `framework_detector.py`, `seo_crawler.py`, `on_page_analyzer.py`, `lighthouse_audit.py`, `schema_checker.py`

**Key Outputs:** Prioritized issue list by business impact, 5-section audit with weighted health score

---

### 3. Content Architect (`content-architect.md`)

Content strategist, writer, and QA editor. Handles everything from keyword research to final copy.

**Responsibilities:**
- **Topic Clusters:** Hub-and-spoke content architecture, cannibalization detection, topical authority mapping
- **Keyword Research:** Google Autosuggest mining, Google Trends integration, ML-based semantic clustering
- **Content Briefs:** Full briefs with keyword targets, outline structure, internal linking map, competitor analysis
- **Article Writing:** 2000+ word articles with E-E-A-T compliance, proper FAQ structure (5–8 questions max), mandatory conclusion format with CTA
- **Content Refresh:** Stat updates, new section additions, freshness signal optimization
- **QA Checklist:** 10-point verification gate before any content is delivered

**Tools invoked:** `topic_graph_mapper.py`, `keyword_clusterer.py`, `competitor_gap.py`, `nlp_analyzer.py`, `aeo_grader.py`

**Key Outputs:** Keyword clusters, content briefs, full SEO-optimized articles, refresh recommendations

---

### 4. GEO Mastermind (`geo-mastermind.md`)

The AI Search specialist. Optimizes content and brand presence for ChatGPT, Perplexity, Google AI Overviews, and Gemini.

**Responsibilities:**
- **AI Citability Scoring:** 0–100 score across 5 dimensions — answer block quality, self-containment, structural readability, statistical density, and uniqueness
- **AI Crawler Access Audit:** analyzes `robots.txt` for GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, PerplexityBot, Google-Extended, CCBot, and 6+ more
- **llms.txt Analysis:** validates or generates the `llms.txt` governance file for AI crawler guidance
- **Brand Mention Scanning:** tracks brand presence across Wikipedia, Reddit, YouTube, LinkedIn, and industry sources
- **Platform-Specific Optimization:** tailored recommendations for each AI search platform

**AI Visibility Formula:**
```
AI_Visibility = (Citability × 0.35) + (Brand_Mentions × 0.30) + (Crawler_Access × 0.25) + (LLMS_TXT × 0.10)
```

**Tools invoked:** `aeo_grader.py`, `llmstxt_generator.py`, `brand_mention_tracker.py`, `geo_monitor/` scrapers

**Key Outputs:** AI Visibility Score (0–100), platform readiness matrix, prioritized GEO action plan

---

### 5. Report Architect (`report-architect.md`)

The output specialist. Takes approved markdown from chat and converts it into polished, client-ready Word documents with zero recalculation.

**Responsibilities:**
- Converts approved chat markdown directly to `.docx`
- Applies agency branding: Navy `#1B3A6B`, Orange `#E8671A`, White
- Structures: Cover page → Executive Summary → Section Banners → Issue Tables → 90-Day Action Plan
- Supports 5 document types: Full Audit, GEO Report, Content Strategy, Monthly Report, Proposal
- Never recalculates scores — outputs exactly what the agents surfaced and the user approved

**Tool invoked:** `chat_to_report.py`

**Key Outputs:** Professionally branded `.docx` files matching your agency template

---

## Python Tools — Complete Reference

All 26+ tools live in `tools/`. They are deterministic execution scripts — no AI reasoning inside them. They collect, transform, and validate data, then write structured JSON to `.tmp/`.

### Crawling & Analysis

| Tool | What It Does |
|------|-------------|
| `seo_crawler.py` | Full site crawl with JS rendering via Playwright. Extracts status codes, canonicals, H1s, meta descriptions, internal links, schema, redirect chains. `--no-js` flag for Google's perspective. Max 50 pages per run. |
| `framework_detector.py` | **Critical first step.** Dual-pass crawl (no-JS vs. JS-rendered) to detect React CRA, Vue SPA, Angular CSR, Next.js SSR, Gatsby SSG, and static HTML. Calculates `content_ratio` (Google's word count vs. user's word count). Applies score caps for CSR/SPA sites. |
| `on_page_analyzer.py` | Page-by-page on-page analysis. Title tag length and keyword placement, meta description quality, heading hierarchy, keyword density, internal linking, canonical presence, robots meta, image alt text coverage. |
| `fetch_page.py` | Single-page fetcher with dynamic rendering detection and prerender service support. Used for targeted page analysis. |

### Performance & Speed

| Tool | What It Does |
|------|-------------|
| `lighthouse_audit.py` | Runs Google Lighthouse locally via Playwright. Returns LCP, INP, CLS scores with mobile/desktop breakdown. Fallback when PageSpeed MCP is unavailable. 120-second timeout. |

### Schema & Structured Data

| Tool | What It Does |
|------|-------------|
| `schema_checker.py` | Validates all JSON-LD on a page. Checks `@context`, `@type`, required fields, entity connections (`sameAs`, `@id`). Identifies missing Organization, BreadcrumbList, and Product schemas. |
| `schema_gen.py` | Generates production-ready JSON-LD for 6 schema types: Organization, LocalBusiness, Article/BlogPosting, Product, SoftwareApplication, WebSite + SearchAction. Pre-wired to brand kit data. |

### Keyword & Content Research

| Tool | What It Does |
|------|-------------|
| `serp_scraper.py` | Multi-mode SERP tool. Modes: `autosuggest` (Google Suggest API), `trends` (Google Trends via pytrends), `serp_top10` (top 10 organic results), `competitor_gap` (keyword gap analysis). 10-second rate-limit delay built in. |
| `keyword_clusterer.py` | ML-based keyword grouping using `sentence-transformers`. Groups keywords by semantic similarity into hub-and-spoke clusters. Requires `torch` + `sentence-transformers`. |
| `competitor_gap.py` | Identifies keywords competitors rank for that the client does not. Powered by DataForSEO enterprise API. Outputs low-hanging fruit keyword list with difficulty and volume. |
| `nlp_analyzer.py` | NLP content analysis. Modes: `gap` (content gap vs. SERP top 10), `readability` (Flesch-Kincaid), `keyword_density`, `content_ratio`. Uses `textstat` for readability scoring. |
| `topic_graph_mapper.py` | Maps semantic entities and Wikipedia relationships for a topic. Identifies subtopics, related entities, and cluster architecture. Powers content architect's hub-and-spoke strategy. |

### AI Search (GEO/AEO)

| Tool | What It Does |
|------|-------------|
| `aeo_grader.py` | Answer Engine Optimization grader. Detects answer blocks at H2 starts, listicle formatting, FAQ schema, statistical citations, and platform-specific patterns. Returns 0–100 citability score per platform. |
| `llmstxt_generator.py` | Creates and validates the `llms.txt` governance file for AI crawler guidance. Checks existing file for completeness and generates optimized versions. |
| `geo_monitor/google_ai_overview.py` | Playwright-based scraper. Checks if the client brand appears in Google AI Overviews / SGE results for target keywords. No API key required. |
| `geo_monitor/perplexity.py` | Playwright-based scraper. Checks if the client is cited in Perplexity Sonar results. No API key required. |
| `geo_monitor/chatgpt_search.py` | Playwright-based scraper. Checks if the client appears in ChatGPT web search results. No API key required. |

### Entity & Brand

| Tool | What It Does |
|------|-------------|
| `entity_auditor.py` | Full Knowledge Graph audit. Checks Wikipedia presence, Wikidata entity existence, Google Knowledge Panel eligibility, NAP consistency. Returns 0–100 entity strength score. |
| `brand_mention_tracker.py` | Scans Reddit, YouTube, LinkedIn, and industry sources for brand mentions. Tracks mention velocity, sentiment context, and platform coverage for E-E-A-T brand signal assessment. |

### Reporting & Output

| Tool | What It Does |
|------|-------------|
| `chat_to_report.py` | The report engine. Converts approved markdown to a `.docx` file matching the agency template. Colors: Navy `#1B3A6B`, Orange `#E8671A`. Input: `.tmp/approved_report.md`. Output: `reports/{client}_Audit_{date}.docx`. |
| `build_playbook_docx.py` | Converts agency playbook and SOP markdown files into Word documents for client or team distribution. |

### Programmatic SEO

| Tool | What It Does |
|------|-------------|
| `programmatic_quality_scorer.py` | Validates programmatic page templates. Calculates boilerplate ratio — must be under 40%. Flags templates that would trigger Google's doorway page filter. |
| `indexing_monitor.py` | GSC integration for bulk page indexation tracking. Monitors "Crawled — currently not indexed" signals. Triggers rollout pause if >20% fail the doorway test. |

### Data & Infrastructure

| Tool | What It Does |
|------|-------------|
| `dataforseo_client.py` | Wrapper for the DataForSEO enterprise API. Handles authentication, rate limiting, and response normalization for keyword difficulty, search volume, and competitor ranking data. |
| `fastmcp_server.py` | Exposes Python tools as typed MCP services. Adds strict argument validation to prevent malformed tool calls. Currently wraps `seo_crawler.py`. |
| `health_check.py` | System diagnostics. Validates Python version, all `requirements.txt` dependencies, environment variable presence, and API connectivity before any workflow runs. |
| `utils.py` | Centralized utility functions. Key function: `url_to_slug()` — the canonical URL-to-filename converter used by every tool to prevent file naming collisions and the false 10/10 score bug. |
| `cleanup_tmp.py` | Manages the `.tmp/` directory. Removes or archives files older than a configurable number of days. |
| `deps_manager.py` | Centralized import error handler. Provides clear, actionable error messages when optional heavy dependencies (`torch`, `sentence-transformers`) are missing. |

---

## 24 Workflow SOPs

Workflows live in `workflows/` as markdown files. They are the instructions agents read before executing. They define objectives, required inputs, tool sequence, expected outputs, and edge case handling.

### Audit Workflows

| Workflow | Purpose |
|----------|---------|
| `audit.md` | Full SEO audit V2.1. Orchestrates framework detection → crawl → on-page → CWV → schema → CRO → report generation. |
| `on_page.md` | Single or multi-page on-page optimization. Title, meta, headings, keyword targeting, internal linking. |
| `topical_audit.md` | Content cluster and topical authority audit. Identifies gaps, cannibalization, and pillar-spoke structure. |
| `entity_audit.md` | E-E-A-T and entity audit. Author credentials, brand authority signals, Knowledge Graph presence. |
| `page_analysis.md` | Deep single-page dive. On-page + technical + schema + CRO analysis for one URL. |

### Content Workflows

| Workflow | Purpose |
|----------|---------|
| `content_draft.md` | Full article writing. 2000+ words, E-E-A-T compliance, platform modes (educational/commercial/comparison). |
| `content_brief.md` | Content brief creation. Keyword research, outline, competitor analysis, internal linking map. |
| `content_refresh.md` | Existing content update. Stat updates, new sections, freshness signals, structural improvements. |
| `cluster.md` | Topic cluster strategy. Hub-and-spoke architecture, cannibalization check, content calendar. |
| `rewrite.md` | Content rewriting while preserving ranking signals. Structural improvements without losing backlink equity. |
| `scrub.md` | Content quality improvement. Thin content consolidation, duplicate detection, content audit clean-up. |

### Research Workflows

| Workflow | Purpose |
|----------|---------|
| `keyword_research.md` | Keyword discovery and clustering. Google Autosuggest, Google Trends, ML semantic grouping. |
| `competitor_gap.md` | Competitive keyword gap analysis. Low-hanging fruit identification with difficulty/volume context. |
| `research-gaps.md` | Content gap analysis against competitors. Identifies topics competitors cover that the client doesn't. |
| `research-serp.md` | SERP analysis for a target keyword. Top 10 ranking page analysis, intent mapping, format patterns. |
| `research-topics.md` | Topic discovery via semantic entity mapping. Identifies subtopics and related entity clusters. |

### Optimization Workflows

| Workflow | Purpose |
|----------|---------|
| `aeo_optimize.md` | Answer Engine Optimization. AI citability scoring, answer block creation, platform-specific rewrites. |
| `optimize.md` | Optimization planning. Action prioritization by business impact and effort, 90-day roadmapping. |
| `link_building.md` | Link opportunity discovery and outreach. Hunter.io email discovery, personalized outreach templates. |
| `programmatic_seo.md` | Programmatic page generation at scale. 50+ pages from data sources, quality gate enforcement. |

### Reporting & Management Workflows

| Workflow | Purpose |
|----------|---------|
| `monthly_report.md` | Monthly performance report. GSC keyword data, GA4 traffic trends, progress tracking, next month priorities. |
| `client_management.md` | Client onboarding. Brand kit intake, folder creation, first audit setup. |

---

## MCP Servers

Three MCP (Model Context Protocol) servers are configured to give the AI agents direct, real-time access to external APIs without manual credential handling or CSV exports.

### 1. PageSpeed Insights MCP

**Package:** `@ruslanlap/pagespeed-insights-mcp` v1.1.1  
**Config location:** `tools/pagespeed-mcp/dist/index.js`

The fastest way to get Core Web Vitals data. Streams results directly from Google's PageSpeed Insights API, analyzing mobile and desktop in parallel.

**What it returns:**
- LCP, INP, CLS scores with pass/fail against Google's thresholds
- Lighthouse scores for Performance, Accessibility, SEO, and Best Practices
- Field data (CrUX) — real-world user experience data, not just lab scores
- Image optimization details: file sizes, format compliance, lazy loading
- Specific improvement recommendations for each failed metric

**When to use:** Any Core Web Vitals check, performance audit, quick speed verification during client calls. 7.5x faster than running `lighthouse_audit.py` locally.

**Important limitation:** PageSpeed MCP analyzes one page at a time and always renders JavaScript. It cannot detect framework rendering issues (a React CRA site will appear to score normally). Always run `framework_detector.py` first.

---

### 2. Google Search Console MCP

**Location:** `tools/mcp-gsc/gsc_server.py`  
**Auth:** OAuth2 token stored at `tools/mcp-gsc/token.pickle`

Direct API access to Google Search Console — no CSV exports, no manual downloads, fresh data every call.

**Available tools:**
```python
# Query keyword performance
mcp__gsc.query_search_analytics(
    site_url="https://example.com",
    start_date="2026-02-01",
    end_date="2026-05-01",
    dimensions=["query", "page"]
)

# Get top keywords by impressions
mcp__gsc.get_top_keywords(
    site_url="https://example.com",
    limit=50
)

# Inspect URL indexation status
mcp__gsc.inspect_url(
    site_url="https://example.com",
    url="https://example.com/target-page"
)
```

**When to use:** Monthly reports (pulls last 30 days automatically), CTR optimization (finds high-impression/low-CTR keywords), index status checks, keyword gap analysis comparing periods.

---

### 3. AIOS Governance MCP

**Location:** `tools/fastmcp_server.py`

A type-safe wrapper around core Python tools that adds strict argument validation. Prevents malformed tool calls that could cause runaway crawls or corrupted output files.

**Available tools:**
```python
# Type-validated site crawl
mcp__aios.run_seo_crawler(
    url="https://example.com",
    max_pages=100  # Validated: cannot be infinite or negative
)
```

**When to use:** When running automated crawls where argument safety matters. Will expand to wrap additional tools as the system scales.

---

### MCP Tool Coverage Matrix

| Task | MCP Available | Coverage | Fallback |
|------|--------------|----------|---------|
| Core Web Vitals | PageSpeed MCP | 100% | `lighthouse_audit.py` |
| GSC Keyword Data | GSC MCP | 100% | Manual CSV export |
| Accessibility Audit | PageSpeed MCP | 100% | Manual check |
| On-Page SEO Analysis | None | 0% | `on_page_analyzer.py` (required) |
| Multi-Page Crawl | AIOS Governance | Wrapped | `seo_crawler.py` (required) |
| Framework Detection | None | 0% | `framework_detector.py` (required) |
| Schema Validation | None | 0% | `schema_checker.py` (required) |
| Content Quality | None | 0% | `nlp_analyzer.py` (required) |
| Competitor Analysis | None | 0% | `serp_scraper.py` (required) |
| AEO/GEO Scoring | None | 0% | `aeo_grader.py` (required) |

---

## Claude Code Skills

The system ships with 20+ Claude Code skills (slash commands) that map directly to workflows. Each skill loads the corresponding workflow and configures the active agent persona.

### Core Workflow Skills

| Skill | Command | What It Runs |
|-------|---------|-------------|
| Full Audit | `/audit` | Complete technical + on-page + CRO + schema + CWV audit |
| Client Onboarding | `/add_client <name>` | Brand kit intake, folder creation, first audit setup |
| Keyword Research | `/keyword_research` | Autosuggest + trends + ML clustering |
| Content Brief | `/content_brief` | Full brief with keyword targets, outline, internal links |
| Content Draft | `/content_draft` | 2000+ word E-E-A-T article from approved brief |
| On-Page Analysis | `/on_page` | Title, meta, headings, keyword optimization |
| Page Deep-Dive | `/page` | Single-page analysis with E-E-A-T + image SEO |
| Competitor Gap | `/competitor_gap` | Low-hanging fruit keywords from competitor analysis |
| AEO Optimize | `/aeo_optimize` | AI citability scoring + platform-specific rewrites |
| Entity Audit | `/entity_audit` | Wikipedia, Wikidata, Knowledge Panel, NAP audit |
| Brand Monitor | `/brand_monitor` | Reddit, YouTube, LinkedIn, industry mention tracking |
| Monthly Report | `/monthly_report` | GSC data + GA4 + progress tracking + next priorities |
| Programmatic SEO | `/programmatic_seo` | 50+ page architecture with quality gate validation |
| Link Building | `/link_building` | Opportunity discovery + Hunter.io outreach drafts |

### Specialized Skills

| Skill | Command | What It Runs |
|-------|---------|-------------|
| Full Audit (parallel) | `/seo-audit` | Multi-agent parallel audit delegation |
| GEO Analysis | `/seo-geo` | AI search optimization across all platforms |
| Technical SEO | `/seo-technical` | 9-category technical analysis |
| Schema Generation | `/seo-schema` | Detect, validate, generate JSON-LD |
| Local SEO | `/seo-local` | GBP, NAP, citations, local schema |
| Content Quality | `/seo-content` | E-E-A-T + citability assessment |
| Competitor Pages | `/seo-competitor-pages` | "vs" and "alternatives" page templates |
| Hreflang Audit | `/seo-hreflang` | International SEO validation |

---

## Schema Templates

Six production-ready JSON-LD schema templates live in `.agents/schema/`. Each is pre-wired to pull from the client's `brand_kit.json`.

| Template | Schema Type | Use Case |
|----------|------------|---------|
| `organization.json` | Organization | Any brand establishing Knowledge Graph entity. Includes `@id`, `address`, `contactPoint`, `sameAs` to Wikidata/Wikipedia. |
| `local-business.json` | LocalBusiness | Service area businesses and brick-and-mortar. Includes geo coordinates, opening hours, service area. |
| `article-author.json` | BlogPosting + Person | Blog content with named author entities. E-E-A-T author credentials wired in. |
| `product-ecommerce.json` | Product + Offer + AggregateRating | E-commerce product pages with pricing, availability, and review data. |
| `software-saas.json` | SoftwareApplication | SaaS product pages with pricing tiers, trial CTAs, and platform requirements. |
| `website-searchaction.json` | WebSite + SearchAction | Sitelinks search box eligibility for the entire domain. |

**Schema standards enforced:**
- Every Organization includes `@id`, `address`, `contactPoint`, and `sameAs` to Wikidata/Wikipedia
- FAQPage and HowTo schemas are explicitly excluded (deprecated/restricted since 2023)
- INP replaces FID in all CWV references (FID was retired March 12, 2024)

---

## Client Management System

Every client gets a dedicated folder under `clients/` with a complete brand kit that drives every subsequent workflow.

### Brand Kit Structure

`clients/_template/brand_kit.json` defines the full intake schema:

```
client_info        → name, website, industry, location, onboarding date
brand_voice        → tone, persona, writing style, CTA style
target_audience    → primary persona, pain points, demographics, platforms
seo_settings       → primary keywords, negative keywords, target locations, language, content pillars
competitors        → top 3 competitors with names and URLs
technical_settings → CMS type, GSC connected flag, GA4 connected flag, sitemap URL, robots.txt URL
reporting          → frequency, report recipients, custom template override
```

### Per-Client Folder Layout

```
clients/
├── _template/
│   └── brand_kit.json
├── client-name/
│   ├── brand_kit.json          ← filled during /add_client onboarding
│   ├── reports/
│   │   ├── Audit_2026-05-01.docx
│   │   └── MonthlyReport_2026-05-01.docx
│   └── briefs/
│       ├── keyword-research.md
│       └── content-calendar.md
```

### File Naming Convention

All tool outputs use `url_to_slug()` from `tools/utils.py` to prevent file collisions:

```python
from utils import url_to_slug

url_to_slug("https://metalbarns.in")      → "metalbarns"
url_to_slug("https://www.example.com")    → "exampleclient"
url_to_slug("http://example.org/about")   → "example"

# File naming pattern:
.tmp/{slug}_{file_type}.json
# Examples:
.tmp/metalbarns_framework.json
.tmp/metalbarns_crawl_nojs.json
.tmp/metalbarns_lighthouse.json
```

This prevents the false 10/10 score bug that occurred when raw URLs were used as file identifiers, causing data from one client to overwrite another.

---

## SEO Health Scoring Formula

Every audit produces a weighted health score. The formula is consistent across all agents and cannot be overridden.

| Category | Weight | Tools Used |
|----------|--------|-----------|
| Technical SEO (crawlability, indexation, speed) | 25% | `seo_crawler.py`, `framework_detector.py` |
| Content Quality (depth, E-E-A-T, thin content) | 25% | `nlp_analyzer.py`, `aeo_grader.py` |
| On-Page SEO (titles, metas, headings) | 20% | `on_page_analyzer.py` |
| Schema / Structured Data | 10% | `schema_checker.py` |
| Core Web Vitals (LCP, INP, CLS) | 10% | PageSpeed MCP, `lighthouse_audit.py` |
| Image SEO (alt text, compression, filenames) | 5% | `seo_crawler.py` image pass |
| AI Search Readiness (AEO/GEO signals) | 5% | `aeo_grader.py`, `llmstxt_generator.py` |

**Score targets:**
- LCP: < 2.5 seconds
- INP: < 200ms (replaces deprecated FID as of March 12, 2024)
- CLS: < 0.1

Reports always show the score breakdown as a table with the current score per category, not just a total.

---

## AI Search — GEO/AEO Engine

Google AI Overviews, ChatGPT web search, Perplexity, and Gemini use different citability signals than traditional Google rankings. This system has dedicated tooling for all four platforms.

### AI Visibility Scoring Formula

```
AI_Visibility = (Citability × 0.35) + (Brand_Mentions × 0.30) + (Crawler_Access × 0.25) + (LLMS_TXT × 0.10)
```

### Citability Dimensions (35% weight)

| Dimension | Weight | What It Checks |
|-----------|--------|---------------|
| Answer Block Quality | 25% | 50–75 word answer block at the start of each H2 |
| Self-Containment | 20% | Can each section be understood without context? |
| Structural Readability | 20% | Headers, bullets, numbered lists, tables |
| Statistical Density | 20% | Absolute citations ("A 2025 study by X..." not "recently") |
| Uniqueness | 15% | Original data, proprietary research, first-person experience |

### Brand Mention Scoring (30% weight)

| Source | Points |
|--------|--------|
| Wikipedia | 40 max |
| Industry sources | 25 max |
| Reddit | 20 max |
| YouTube | 15 max |
| LinkedIn | 10 max |

### AI Crawler Access Scoring (25% weight)

The system checks `robots.txt` for every major AI crawler. Blocking critical crawlers directly reduces AI visibility:

**Critical crawlers:** GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, PerplexityBot  
**Secondary:** Google-Extended, Applebot-Extended  
**Low priority:** CCBot, Bytespider

### Platform-Specific Optimization

| Platform | Key Signals | Unique Factor |
|----------|-------------|---------------|
| Google AI Overviews | Structured data, E-E-A-T, position zero | Schema quality is primary signal |
| ChatGPT Web Search | Freshness, authority, answer blocks | Citation format heavily weighted |
| Perplexity Sonar | Freshness (+20 boost), numbered format | Recency is the #1 ranking factor |
| Gemini | Schema quality, heading hierarchy, comparison tables | Structured comparison content preferred |

### GEO Monitoring Tools (No API Key Required)

All three GEO monitoring scrapers use headless Playwright browsers — no paid API keys needed:

```
tools/geo_monitor/google_ai_overview.py  → Google AI Overviews/SGE
tools/geo_monitor/perplexity.py          → Perplexity Sonar
tools/geo_monitor/chatgpt_search.py      → ChatGPT Web Search
```

---

## Framework Detection — The Critical Safety Net

Framework detection is mandatory Step 0 of every audit. It is the most important safety check in the system.

**The problem it solves:** A React CRA site may score 95/100 on PageSpeed because PageSpeed always renders JavaScript. But Google's crawler sees almost nothing — 2 words instead of 343 words. Without framework detection, the audit would report 10/10 technical SEO and completely miss the most critical issue on the site.

### Detection Logic

```
python tools/framework_detector.py --url {url} --output .tmp/framework.json
```

The detector runs two crawl passes:
1. **No-JS pass** — simulates Google's perspective (JavaScript disabled)
2. **JS pass** — simulates the user's perspective (full rendering)

It calculates `content_ratio = nojs_word_count / js_word_count`.

### Score Capping Rules

| Framework Detected | Action |
|-------------------|--------|
| React CRA (CSR) | CRITICAL — cap technical score at 2/10, recommend Next.js migration |
| Vue SPA (CSR) | CRITICAL — cap technical score at 2/10, recommend Nuxt.js migration |
| Angular CSR | CRITICAL — cap technical score at 2/10, recommend SSR migration |
| Next.js (SSR/SSG) | GOOD — proceed normally |
| Gatsby (SSG) | GOOD — proceed normally |
| Static HTML | GOOD — proceed normally |

**If `content_ratio < 0.1`** (less than 10% of content visible to Google), this is flagged as a CRITICAL issue and becomes Issue #1 in the audit. All subsequent issues are marked: "Blocked by architecture — fix framework first before addressing this issue."

---

## Programmatic SEO Quality Gates

The system enforces three quality gates before any programmatic page generation is approved.

### Gate 1: 3-Variable Minimum

Every programmatic template must provide at least 3 distinct, semantically unique variables per page. Simply swapping `[City]` into a template fails this gate. Rejected.

### Gate 2: Boilerplate Ratio < 40%

```bash
python tools/programmatic_quality_scorer.py --template template.html --data data.csv
```

The boilerplate ratio — the percentage of text that is identical across all generated pages — must be under 40%. Pages over 40% risk triggering Google's doorway page filter.

### Gate 3: Phased Rollout for Bulk Generation

For any generation of more than 50 pages:
1. Generate 10 pilot pages first
2. Monitor indexation status via `tools/indexing_monitor.py`
3. If more than 20% of pilot pages receive "Crawled — currently not indexed" status, the template failed the doorway test. Stop and redesign.
4. Only proceed to full rollout if pilot passes.

---

## Platform Intelligence Gate

Before any technical analysis, the system fingerprints the CMS and applies platform-specific checks.

### Shopify

- Check Liquid code repetition in headers and ticker bars
- Audit canonical behavior on collection and pagination pages (Shopify frequently self-canonicalizes incorrectly)
- Shopify Markets + Hreflang audit for international targeting
- App bloat audit: list all `<head>` scripts, flag duplicates and performance killers
- Default `robots.txt` check — Shopify often blocks crawlable paths unintentionally

### WordPress

- Verify Yoast or RankMath is installed and configured (not just active)
- Plugin count vs. Core Web Vitals correlation analysis
- Permalink structure check — must be `/%postname%/`
- XML sitemap generation verification and GSC submission status

### B2B / Custom / Headless (React, Next.js, etc.)

- Entity Graphing priority: Organization, Service, and Person schema are the foundation
- Whitepaper and case study topic cluster prioritization
- JavaScript rendering audit: can Googlebot render the framework? Verify via GSC URL Inspection
- CSR detection: does `content_ratio < 0.1`? If yes, escalate to CRITICAL framework issue

---

## Report Generation Pipeline

Every report follows the same approval-before-generation workflow. The Report Architect never generates a document from unreviewed data.

### Step-by-Step Flow

```
1. All agents surface findings in the chat
2. SEO Director synthesizes into structured report markdown
3. User reads and approves the markdown in the chat
4. Report Architect writes approved markdown to .tmp/approved_report.md
5. chat_to_report.py converts markdown → .docx
6. Download link is generated automatically
```

### Report Format

```
Download: [ClientName_Audit_2026-05-01.docx](file:///full/path/to/report.docx)
```

### Document Template

All documents follow the Example Brand template:
- **Colors:** Navy `#1B3A6B`, Orange `#E8671A`, White
- **Structure:** Cover Page → Executive Summary → Section Banners → Issue Tables → 90-Day Action Plan → "How Example Brand Adds Value"
- **Minimum length:** 4,000 words of actual content (not counting tables or headers)
- **Roadmap structure:** Phase 1 Quick Wins → Phase 2 Authority → Phase 3 Scale

---

## Quick Start Guide

### Prerequisites

- Python 3.10+
- Node.js 18+ (for Playwright)
- Claude Code CLI or Claude Desktop

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
npm install
```

### Step 2: Configure Environment

```bash
cp .env.example .env
```

Open `.env` and fill in your API keys:

```env
# Required — Google APIs
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_PROJECT_ID=your_project_id
GOOGLE_API_KEY=your_api_key

# Optional — Enhanced Features
DATAFORSEO_LOGIN=your_login
DATAFORSEO_PASSWORD=your_password
HUNTER_API_KEY=your_key

# Report Output
REPORT_OUTPUT=local
GOOGLE_DRIVE_FOLDER_ID=your_folder_id
```

Missing API keys cause workflows to fail gracefully — never to hallucinate data.

### Step 3: Verify System Health

```bash
python tools/health_check.py
```

This validates Python version, all dependencies, environment variables, and API connectivity.

### Step 4: Configure MCP Servers (for Claude Desktop)

Edit `C:\Users\HP\AppData\Roaming\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "pagespeed": {
      "command": "node",
      "args": ["path/to/tools/pagespeed-mcp/dist/index.js"],
      "env": {"GOOGLE_API_KEY": "your_google_api_key"}
    },
    "gsc": {
      "command": "python",
      "args": ["path/to/tools/mcp-gsc/gsc_server.py"],
      "env": {
        "GSC_TOKEN_PATH": "path/to/tools/mcp-gsc/token.pickle",
        "GSC_CREDENTIALS_PATH": "path/to/tools/mcp-gsc/gsc_credentials.json"
      }
    },
    "aios-governance": {
      "command": "python",
      "args": ["path/to/tools/fastmcp_server.py"]
    }
  }
}
```

Restart Claude Desktop to activate MCP servers.

### Step 5: Run Your First Audit

Open Claude Code and type:

```
/audit https://yoursite.com
```

Or onboard a client first:

```
/add_client YourClientName
```

The system will walk you through brand kit collection, then run the full audit automatically.

---

## Full File Structure

```
SEO AI ENGINE/
│
├── .agents/
│   ├── agents/
│   │   ├── seo-director.md          ← Orchestrator agent
│   │   ├── audit-architect.md       ← Technical + on-page auditor
│   │   ├── content-architect.md     ← Content strategist + writer
│   │   ├── geo-mastermind.md        ← AI Search specialist
│   │   └── report-architect.md      ← Document generation specialist
│   ├── skills/
│   │   ├── geo/                     ← GEO-first analysis skill
│   │   ├── seo-audit/               ← Full audit skill
│   │   ├── content-strategy/        ← Topic clusters + keyword maps
│   │   ├── entity-building/         ← Knowledge Graph + brand authority
│   │   ├── brand-monitoring/        ← Mention tracking
│   │   ├── geo-audit/               ← AI-specific audit framework
│   │   ├── geo-citability/          ← Citability scoring
│   │   ├── geo-content/             ← Content quality for AI search
│   │   ├── geo-technical/           ← Technical SEO for AI crawlers
│   │   ├── geo-brand-mentions/      ← Platform-specific mention tracking
│   │   ├── geo-crawlers/            ← AI bot access analysis
│   │   ├── geo-llmstxt/             ← llms.txt validation + generation
│   │   ├── geo-platform-optimizer/  ← ChatGPT, Perplexity, Gemini, AIO
│   │   ├── geo-compare/             ← Month-to-month delta reports
│   │   ├── geo-proposal/            ← Client proposal generation
│   │   ├── geo-prospect/            ← CRM pipeline management
│   │   ├── geo-report/              ← Client-ready report generation
│   │   ├── geo-report-pdf/          ← PDF report generation with charts
│   │   ├── competitor-alternatives/ ← "vs" and alternatives pages
│   │   ├── programmatic-seo/        ← 50+ page generation
│   │   ├── seo-competitor-pages/    ← Competitor comparison pages
│   │   ├── seo-hreflang/            ← International SEO + hreflang
│   │   └── seo-images/              ← Image optimization analysis
│   └── schema/
│       ├── organization.json         ← Organization + Knowledge Graph
│       ├── local-business.json       ← LocalBusiness + service area
│       ├── article-author.json       ← BlogPosting + author entity
│       ├── product-ecommerce.json    ← Product + Offer + Reviews
│       ├── software-saas.json        ← SoftwareApplication + trials
│       └── website-searchaction.json ← WebSite + Sitelinks search
│
├── tools/
│   ├── seo_crawler.py
│   ├── framework_detector.py        ← CRITICAL — run first always
│   ├── on_page_analyzer.py
│   ├── lighthouse_audit.py
│   ├── schema_checker.py
│   ├── schema_gen.py
│   ├── serp_scraper.py
│   ├── keyword_clusterer.py
│   ├── competitor_gap.py
│   ├── nlp_analyzer.py
│   ├── topic_graph_mapper.py
│   ├── aeo_grader.py
│   ├── llmstxt_generator.py
│   ├── entity_auditor.py
│   ├── brand_mention_tracker.py
│   ├── programmatic_quality_scorer.py
│   ├── indexing_monitor.py
│   ├── chat_to_report.py
│   ├── dataforseo_client.py
│   ├── fastmcp_server.py
│   ├── utils.py                     ← url_to_slug() lives here
│   ├── health_check.py
│   ├── cleanup_tmp.py
│   ├── deps_manager.py
│   ├── fetch_page.py
│   ├── review_aggregator.py
│   ├── geospatial_search.py
│   ├── ai_governance_gen.py
│   ├── outreach_sender.py
│   ├── build_playbook_docx.py
│   ├── mcp-gsc/
│   │   └── gsc_server.py            ← GSC MCP server
│   ├── pagespeed-mcp/
│   │   └── dist/index.js            ← PageSpeed MCP server
│   └── geo_monitor/
│       ├── google_ai_overview.py    ← Google AIO Playwright scraper
│       ├── perplexity.py            ← Perplexity Playwright scraper
│       └── chatgpt_search.py        ← ChatGPT Playwright scraper
│
├── workflows/
│   ├── audit.md
│   ├── on_page.md
│   ├── topical_audit.md
│   ├── entity_audit.md
│   ├── aeo_optimize.md
│   ├── content_draft.md
│   ├── content_brief.md
│   ├── content_refresh.md
│   ├── cluster.md
│   ├── keyword_research.md
│   ├── competitor_gap.md
│   ├── link_building.md
│   ├── monthly_report.md
│   ├── page_analysis.md
│   ├── programmatic_seo.md
│   ├── optimize.md
│   ├── rewrite.md
│   ├── scrub.md
│   ├── client_management.md
│   ├── research-gaps.md
│   ├── research-serp.md
│   ├── research-topics.md
│   └── [+ additional SOPs]
│
├── clients/
│   ├── _template/
│   │   └── brand_kit.json
│   └── {client-name}/
│       ├── brand_kit.json
│       ├── reports/
│       └── briefs/
│
├── templates/
│   └── Example template.pdf         ← Brand design reference
│
├── .tmp/                            ← Auto-generated, disposable cache
│   └── {slug}_{file_type}.json
│
├── reports/                         ← Final client deliverables
│   └── {Client}_Audit_YYYY-MM-DD.docx
│
├── .env                             ← API keys — never committed
├── .env.example                     ← Template for setup
├── requirements.txt
├── package.json
├── CLAUDE.md                        ← AI system instructions (200+ lines)
├── AGENCY_PLAYBOOK.md
├── GOOGLE_API_SETUP.md
├── MCP_SETUP.md
├── DATAFORSEO_INTEGRATION_COMPLETE.md
├── SYSTEM_RELIABILITY.md
└── README.md
```

---

## API Integrations

| Integration | Purpose | Required |
|------------|---------|---------|
| Google PageSpeed Insights | Core Web Vitals, Lighthouse scores, field data | Yes (for MCP) |
| Google Search Console | Keyword rankings, CTR, index status | Yes (for GSC MCP) |
| Google OAuth2 | Authentication for GSC access | Yes |
| DataForSEO | Enterprise keyword difficulty, volume, competitor rankings | Optional (strongly recommended) |
| Hunter.io | Email discovery for link building outreach | Optional |
| Playwright / Chromium | Headless browser for JS rendering and GEO monitoring | Yes |
| Google Drive (via API) | Remote report delivery | Optional |

---

## System Effectiveness

**Time savings vs. manual SEO work:**

| Task | Manual Time | With This System | Time Saved |
|------|------------|-----------------|------------|
| Full technical audit | 6–8 hours | 20–30 minutes | ~95% |
| Keyword research + clustering | 3–4 hours | 15–20 minutes | ~92% |
| Content brief creation | 1.5–2 hours | 5–8 minutes | ~94% |
| Monthly client report | 3–4 hours | 10–15 minutes | ~93% |
| Schema markup audit + generation | 1–2 hours | 3–5 minutes | ~97% |
| Competitor gap analysis | 2–3 hours | 10–15 minutes | ~92% |
| GEO/AEO audit | 2–3 hours | 15–20 minutes | ~90% |

**Accuracy advantages over single-tool solutions:**

- **Framework detection prevents false positives** — A CSR/SPA site cannot receive an inflated technical score. Score caps are enforced automatically.
- **No-JS crawl as authoritative source** — Audits reflect what Google actually sees, not what the browser renders.
- **Zero hallucination on metrics** — Tool failures are loud errors, not fabricated data. Every metric has a source.
- **2026-current schema standards** — INP (not FID), no FAQPage/HowTo recommendations, entity schema with `sameAs` wired to Wikidata.
- **Platform-aware recommendations** — Shopify clients get Shopify-specific checks. WordPress clients get Yoast/RankMath checks. CSR sites get framework migration as Issue #1.

---

## Documentation Index

| Document | Purpose |
|----------|---------|
| `CLAUDE.md` | Complete AI system instructions — 20 global rules governing every agent behavior |
| `AGENCY_PLAYBOOK.md` | Master operations manual for running an SEO agency on this system |
| `GOOGLE_API_SETUP.md` | Step-by-step setup for Google Search Console and PageSpeed APIs |
| `MCP_SETUP.md` | Claude Desktop MCP server configuration and troubleshooting |
| `DATAFORSEO_INTEGRATION_COMPLETE.md` | Enterprise DataForSEO pipeline documentation |
| `SYSTEM_RELIABILITY.md` | Error handling, fallback protocols, and data freshness rules |

---

## License

This is proprietary commercial software. See [LICENSE.md](./LICENSE.md) for usage rights, white-labeling permissions, and distribution restrictions.
