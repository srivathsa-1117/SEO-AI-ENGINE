# SEO Audit Report Template — Example Brand Standard

Use this structure for every audit report generated via chat_to_report.py.
All behavior rules are in CLAUDE.md. This file defines sections and format only.

---

## Required Section Order

### 1. Cover Page
- Client name, website, audit date, "Prepared by Example Brand"
- 4 stat boxes: Issues Found | Audit Sections | Schema Status | Growth Actions

### 2. Executive Summary
- 2–3 paragraph overview of overall site health
- Overall SEO Health Score table (use Rule 6 weighted formula from CLAUDE.md)
- Top 3 critical findings called out explicitly by name

### 3. Platform & Technical Audit
- CMS detected (from Rule 11 fingerprinting in CLAUDE.md)
- Core Web Vitals: LCP / INP / CLS scores and fixes (never reference FID)
- Crawlability: robots.txt, sitemap, canonicals, redirect chains
- URL structure: before/after table (current pattern vs. recommended)
- Schema markup: status per type (Present / Missing / Needs Improvement), JSON-LD template for top 2 missing types
- HTTPS & security: mixed content, www/non-www redirect, canonical version

### 4. On-Page SEO Audit
- Title tags & meta descriptions:

| Page | Current Title (Likely) | Recommended Title | Recommended Meta (140–160 chars) | Status |
|---|---|---|---|---|
| Homepage | | | | |
| Service Page 1 | | | | |
| Service Page 2 | | | | |

- Heading structure: H1 → H2 → H3 per main page with keyword rationale for each level
- Content depth: word count category per page vs. top-ranking competitor (show the gap)
  - Under 300 words = Thin (Critical)
  - 300–800 = Shallow (High Priority)
  - 800–1,500 = Moderate (Medium)
  - 1,500+ = Adequate (Low Priority)
- Keyword strategy — 3 separate tables:

**Primary Keywords (5):**
| Keyword | Est. Monthly Volume | Difficulty | Target Page |
|---|---|---|---|

**Long-Tail Keywords (5):**
| Keyword | Est. Monthly Volume | Difficulty | Target Page |
|---|---|---|---|

**Question-Based Keywords (5):**
| Keyword | Est. Monthly Volume | Difficulty | Target Page |
|---|---|---|---|

- Internal linking: name the exact pillar page URL + 4–5 cluster article titles that link to it

### 5. Image SEO Audit
Checklist — mark each Present / Missing / Needs Fix:
- [ ] Alt attributes on all images
- [ ] Images served in WebP or AVIF format
- [ ] Below-fold images have loading="lazy"
- [ ] Hero images under 100KB
- [ ] Descriptive filenames (not image001.jpg)

Flag every image issue found with the page URL and the specific fix.

### 6. Off-Page & Authority Audit
- Backlink profile: Domain Rating, referring domains, top linking pages
  - If tools unavailable: State that data is currently unavailable via API/Tools.
- Link building opportunities (always include all 4):
  - 3 Digital PR media targets (real publication names + DA)
  - 3 Guest post targets (real blogs in the industry)
  - 2 Free high-value directory listings (e.g., Clutch.co, GoodFirms)
  - 1 Resource link-building idea specific to this client's niche
- Google Business Profile: claimed status + 5 most important fields to complete + review acquisition script

### 7. E-E-A-T Assessment
Score each dimension and provide one specific improvement action:

| Dimension | Rating (Low/Med/High) | Evidence Found | Improvement Action |
|---|---|---|---|
| Experience | | | |
| Expertise | | | |
| Authoritativeness | | | |
| Trustworthiness | | | |

### 8. CRO Audit
- Credibility Zone: describe what is below the hero banner → recommend exact elements in order
- CTA audit: current CTA text → recommended CTA text → intent match (Yes/No) per page
- Lead capture: form field count, multi-step form present, lead magnet offered, post-submit confirmation
- Trust signal checklist:
  - [ ] Client logo strip
  - [ ] Named testimonials with photo + company
  - [ ] Clutch / GoodFirms / Google review badges
  - [ ] Google / Meta Partner certification
  - [ ] Case study with specific metrics
  - [ ] Team page with individual profiles
  - [ ] Pricing page or starting price range
- Intent-to-CTA alignment per page:
  - Awareness stage → "Download Guide" or "Read Case Study"
  - Consideration stage → "See Our Process" or "View Pricing"
  - Decision stage → "Book a Call" or "Get a Custom Quote"

### 9. Competitor Analysis
4 real competitors found via search — no placeholders ever.

Per competitor block:
- **Name (URL)**
- Domain Authority
- Pages they have that the client doesn't
- Their strongest target keyword
- One thing they do better (be direct)
- One exploitable gap

Keyword Architecture Comparison Table:

| Feature | Client | Comp 1 | Comp 2 | Comp 3 |
|---|---|---|---|---|
| Blog / Resource Section | | | | |
| Case Studies with Metrics | | | | |
| Pricing Page | | | | |
| FAQ on Service Pages | | | | |
| Partner Certification Badge | | | | |
| Schema Markup | | | | |
| Interactive Tools / Calculators | | | | |
| Video Content | | | | |

### 10. AI Search Readiness (AEO / GEO)
- Is content structured for featured snippets? (40–60 word answer blocks)
- Are common questions answered directly and concisely on relevant pages?
- Is the brand cited or mentioned in ways LLMs would reference?
- Does the site have clear entity signals (About page, founder profiles, consistent NAP)?
- Recommendation: conversational query targeting strategy for this client's niche

### 11. Growth Innovation Module
All ideas must be specific to this client's industry and buyer persona.

**Industry Content Calendar** (12 months):
| Month | Content Theme | Article Title | Target Keyword | Business Reason |
|---|---|---|---|---|

**The "Encyclopedia" Authority Pillar:**
- Name it specifically for this niche (not just "resource hub")
- List 8–10 sub-articles it should contain
- Explain what type of sites would naturally link to it

**3 Innovative Traffic Ideas (minimum):**
Each must include: what it is | how it drives traffic or links | Effort (L/M/H) | Time to first result

Minimum quality bar:
- ✓ "Free [Industry] ROI Calculator — ranks for '[industry] ROI calculator India', captures emails, earns links from finance blogs. Effort: Medium. Time: 2–3 months."
- ✗ "Start a blog" or "Be active on social media" — not acceptable

**Entity & Author SEO:**
- If founder is named → recommend Author Profile page with LinkedIn/Twitter entity links
- If press mentions exist → "As Seen In" page linked to press entities
- Recommend 2–3 specific outbound authority links to add to high-traffic pages

### 12. 90-Day Roadmap
Sort all tasks by: High Business Impact + Low Effort first (Quick Wins).

**Phase 1 — Quick Wins (Days 1–30):**
| Task | Owner | Business Impact | Effort | Expected Result |
|---|---|---|---|---|

**Phase 2 — Authority Building (Days 31–60):**
| Task | Owner | Business Impact | Effort | Expected Result |
|---|---|---|---|---|

**Phase 3 — Scale & Convert (Days 61–90):**
| Task | Owner | Business Impact | Effort | Expected Result |
|---|---|---|---|---|

**Expected Results Projection:**
| Metric | Month 0 (Baseline) | Month 6 (Target) | Month 12 (Target) |
|---|---|---|---|
| Organic Monthly Traffic | | 2x baseline | 4–5x baseline |
| Keywords in Top 20 | | 10–15 | 25–40 |
| Domain Rating | | +8–12 pts | +20–25 pts |
| Inbound Leads (Organic) | | 8–15/month | 25–40/month |

### 13. How Example Brand Adds Value
Reference specific findings from THIS report only — never use generic statements.

| Gap Found in This Audit | Example Brand Service | Specific Outcome We Deliver |
|---|---|---|
| | | |
| | | |
| | | |

Close with:
> "The next step is a 30-minute strategy call where we walk through the top 3 quick wins from this audit — actions that can show measurable results within 30 days. [Book here / Contact us]"

---

## Formatting Rules

- Every section heading needs 2 sentences of context before any bullets or tables
- No section can be purely a list — all lists must be preceded by a paragraph
- Every table needs a caption or intro sentence
- Minimum report length: 4,000 words of actual content (not counting tables)
- Tone: second person directed at the client ("Your homepage..." not "The homepage...")
- Confident language: "This is missing" not "This may be missing"
- Translate every technical issue into business language in the same paragraph

## Fallback Rule (Applies to Every Field in This Template)

If data is unavailable for any field: state that the data is unavailable. Never guess data or provide placeholder 'Estimated' values. If a section cannot be completed without data, omit the section and explain why.
