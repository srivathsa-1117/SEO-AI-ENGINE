---
description: /topical_audit - Topic coverage analyzer to identify gaps in your content entity graph
---

# Workflow: Topical Audit & Entity Gap Analysis (2026 Standards)

## Trigger
```
/topical_audit <core_topic> <client_domain>
```

## Objective
Identify where the client lacks "Topic Coverage." In 2026, Google evaluates Topical Authority via Knowledge Graph completion. If you are missing sub-topics that semantic search associates with `<core_topic>`, your authority score drops.

## Why Topical Authority Matters in 2026
**Keyword-centric SEO is dead. Entity-centric SEO is the standard.**

- Google's Hummingbird (2013) → Semantic search
- Google's BERT (2019) → Context understanding
- Google's MUM (2021) → Multimodal understanding
- Google's SGE/AI Overviews (2024-2026) → Entity graph completion

**The Shift:**
- **Old SEO:** Rank for "CRM software" → write one page targeting that keyword
- **New SEO:** Rank for "CRM software" → cover the entire CRM topic cluster (sales pipeline, lead scoring, data integrations, customer retention, reporting dashboards, mobile access, API capabilities, etc.)

**Proof:**
- Sites with 80%+ topic coverage rank in top 3 positions 67% more often than sites with <40% coverage (Ahrefs 2025 study)
- AI search engines (ChatGPT, Perplexity) only cite sources that demonstrate "comprehensive knowledge" = topical authority

## Tools Used in This Workflow
- **`tools/topic_graph_mapper.py`** - Builds semantic knowledge graph using Wikipedia API to identify related entities
- **`tools/seo_crawler.py`** - Crawls client website to extract existing content topics (H1s, H2s, titles)
- **`tools/keyword_clusterer.py`** - Groups keywords by semantic similarity to identify content themes

## Success Metrics
- **Topic Coverage Score:** ≥70% (client covers ≥70% of entities in the semantic graph)
- **Missing Pillar Pages:** ≤3 (maximum 3 major sub-topics missing)
- **Content Depth Score:** ≥1,500 words average per pillar page
- **Internal Linking Density:** ≥5 contextual links between related topic pages
- **Ranking Improvement:** +5-10 positions for core topic keyword within 90 days of completing topic cluster

---

## The 4-Step Topical Audit Process

### Step 1: Build the Target Semantic Graph
Run `tools/topic_graph_mapper.py` to pull the actual Wikipedia-backed entity associations for the user's core topic.

```bash
python tools/topic_graph_mapper.py --topic "Your Core Topic"
```

Save the output to `.tmp/topic_graph.json`. 
*This file now represents the "Semantic Perimeter" needed to rank for this topic.*

### Step 2: Crawl Client Content
Use the existing `tools/seo_crawler.py` to extract all indexable URLs and primary H1/H2s from the client's blog or domain.

```bash
python tools/seo_crawler.py --start-url "https://client-domain.com/blog/"
```

### Step 3: Run the Gap Analysis
Cross-reference the entities returned by the Topic Graph Mapper (Step 1) against the H1/H2s extracted from the client's site (Step 2).

For example, if the Core Topic is "CRM":
- The Topic Graph dictates you MUST have pages covering: "Sales pipeline", "Customer retention", "Lead generation", "Data integration".
- The AI OS must output a list of **Missing Pillars** and **Missing Leaves**.

### Step 4: Calculate Topic Coverage Score

**Formula:**
```
Topic Coverage Score = (Entities Covered by Client / Total Entities in Graph) × 100
```

**Process:**
1. Extract all H1s and H2s from client site (from Step 2 crawl)
2. Normalize text (lowercase, remove special characters)
3. For each entity in the topic graph (from Step 1):
   - Check if entity appears in any H1/H2 on client site
   - If yes → mark as "Covered"
   - If no → mark as "Missing"
4. Calculate coverage percentage

**Scoring Interpretation:**
- **≥80%:** Excellent topical authority — client is comprehensive
- **60-79%:** Good coverage — fill remaining gaps for competitive edge
- **40-59%:** Moderate gaps — prioritize high-value missing pillars
- **<40%:** Critical deficiency — major authority weakness, create 90-day content plan

### Step 5: Identify Content Gaps

**Gap Types:**

**1. Missing Pillar Pages (Level 1 Gaps)**
- Core sub-topics completely absent from client site
- Example: CRM topic cluster missing "Sales Pipeline Management" page
- **Priority:** HIGH — these are table stakes for topic authority

**2. Missing Supporting Articles (Level 2 Gaps)**
- Pillar exists, but supporting content is thin
- Example: "Sales Pipeline" page exists, but no articles on "Pipeline Stages", "Conversion Rate Optimization", "Deal Forecasting"
- **Priority:** MEDIUM — build after pillars are complete

**3. Shallow Existing Content (Depth Gaps)**
- Page exists but word count <800 words or lacks semantic depth
- Example: "Lead Scoring" page is 300 words with no examples or case studies
- **Priority:** MEDIUM — expand existing content before creating new pages

**4. Poor Internal Linking (Connection Gaps)**
- Content exists but pages aren't linked together in hub-and-spoke structure
- Example: "CRM" pillar doesn't link to "Lead Scoring" supporting page
- **Priority:** LOW — fix with internal linking audit

**Output JSON Structure:**
```json
{
  "topic_coverage_score": 65,
  "total_entities": 40,
  "covered_entities": 26,
  "missing_entities": 14,
  "gaps": {
    "missing_pillars": [
      {"entity": "Sales Pipeline Management", "priority": "HIGH", "search_volume": 2400},
      {"entity": "Customer Data Integration", "priority": "HIGH", "search_volume": 1900}
    ],
    "missing_supporting": [
      {"entity": "Pipeline Stages", "parent": "Sales Pipeline Management", "priority": "MEDIUM"},
      {"entity": "Deal Forecasting", "parent": "Sales Pipeline Management", "priority": "MEDIUM"}
    ],
    "shallow_content": [
      {"url": "/blog/lead-scoring", "current_words": 450, "target_words": 1500, "priority": "MEDIUM"}
    ],
    "internal_linking_gaps": [
      {"from": "/crm-software", "missing_links_to": ["Lead Scoring", "Sales Pipeline", "Data Integration"]}
    ]
  }
}
```

### Step 6: Generate Topical Audit Report

Save a comprehensive markdown report to `clients/<client_name>/reports/topical_audit_<topic>_YYYY_MM_DD.md`.

**Report Template:**

````markdown
# Topical Authority Audit — [Core Topic]
**Client:** [Client Name]
**Domain:** [client.com]
**Audit Date:** [YYYY-MM-DD]
**Core Topic:** [e.g., "CRM Software"]

---

## Executive Summary

**Topic Coverage Score:** [X]% ([Interpretation: Excellent/Good/Moderate/Critical])

**Key Findings:**
- [X] entities mapped in semantic graph
- [X] entities covered by existing content ([X]%)
- [X] critical pillar gaps identified
- [X] supporting article opportunities identified
- **Estimated Effort:** [X] new pages + [X] content expansions = [X-X hours]
- **Expected Impact:** +[X-X] positions for core keyword within 90 days

**Recommendation:** [One-sentence strategic recommendation, e.g., "Focus on creating 3 missing pillar pages before expanding supporting content."]

---

## 1. Semantic Topic Graph

### Core Hub: [Core Topic]

### Sub-Pillars (Level 1 Entities):
| Entity | Status | Client Coverage | Priority |
|--------|--------|-----------------|----------|
| [Sub-topic 1] | Covered | [URL] | - |
| [Sub-topic 2] | Missing | None | HIGH |
| [Sub-topic 3] | Shallow | [URL] (450 words) | MEDIUM |
| [Sub-topic 4] | Covered | [URL] | - |
| [Sub-topic 5] | Missing | None | HIGH |

### Supporting Content (Level 2 Entities):
| Parent Pillar | Supporting Entity | Status |
|---------------|-------------------|--------|
| [Sub-topic 1] | [Supporting topic 1a] | Covered |
| [Sub-topic 1] | [Supporting topic 1b] | Missing |
| [Sub-topic 2] | [Supporting topic 2a] | Missing (Parent Missing) |
| [Sub-topic 3] | [Supporting topic 3a] | Covered |

---

## 2. Coverage Analysis

### What's Working (Covered Entities):
1. **[Entity 1]** - [URL] ([X] words, published [date])
   - Content depth: Good ([X] words)
   - Internal links: [X] contextual links
   - Schema: Article schema present
   - Performance: [X] monthly visitors

2. **[Entity 2]** - [URL]
   - [Similar analysis]

[Continue for all covered entities]

### Critical Gaps (Missing Pillars):
1. **[Missing Entity 1]** — Priority: HIGH
   - **Why it matters:** [Semantic importance, e.g., "Core component of CRM functionality, searched 2,400 times/month"]
   - **Competitor coverage:** [X]/3 top competitors have dedicated pages on this
   - **Recommended action:** Create pillar page ([1,500-2,000 words])
   - **Estimated traffic potential:** [X-X] monthly visitors

2. **[Missing Entity 2]** — Priority: HIGH
   - [Similar analysis]

[Continue for all critical gaps]

### Moderate Gaps (Shallow Content):
1. **[Existing page]** — [URL]
   - **Current state:** [X] words, published [date]
   - **Gap:** Lacks depth on [specific sub-topics]
   - **Recommended action:** Expand to [1,500-2,000 words], add sections on:
     - [Sub-topic 1]
     - [Sub-topic 2]
     - [Sub-topic 3]
   - **Estimated effort:** [X] hours

[Continue for all shallow content]

### Internal Linking Gaps:
1. **Hub page [URL]** is missing links to:
   - [Spoke page 1]
   - [Spoke page 2]
   - [Spoke page 3]
   - **Fix:** Add contextual links in [specific section]

[Continue for all linking gaps]

---

## 3. Competitive Topical Comparison

| Entity | [Client] | Competitor 1 | Competitor 2 | Competitor 3 |
|--------|----------|--------------|--------------|--------------|
| [Sub-topic 1] | ✅ | ✅ | ✅ | ✅ |
| [Sub-topic 2] | ❌ | ✅ | ✅ | ❌ |
| [Sub-topic 3] | ⚠️ (450w) | ✅ (1.8K) | ✅ (2.1K) | ✅ (1.5K) |
| [Sub-topic 4] | ✅ | ❌ | ✅ | ✅ |
| [Sub-topic 5] | ❌ | ✅ | ✅ | ✅ |
| **Coverage Score** | **[X]%** | **[X]%** | **[X]%** | **[X]%** |

**Key Insight:** [e.g., "Competitors 1 and 2 both cover [Sub-topic 5] comprehensively — this is a strategic gap we must close."]

---

## 4. Content Roadmap (90-Day Plan)

### Phase 1: Fill Critical Pillar Gaps (Weeks 1-4)
**Goal:** Create missing high-priority pillar pages

| Content Piece | Word Count | Target Keyword | Assigned To | Due Date | Status |
|---------------|------------|----------------|-------------|----------|--------|
| [Pillar 1] | 1,800 | "[keyword]" | [Writer] | Week 2 | Pending |
| [Pillar 2] | 1,600 | "[keyword]" | [Writer] | Week 3 | Pending |
| [Pillar 3] | 1,500 | "[keyword]" | [Writer] | Week 4 | Pending |

**Deliverables:** 3 new pillar pages, each with:
- 1,500-2,000 words
- Schema markup (Article or HowTo)
- 3-5 internal links to related content
- Featured image + 2-3 supporting images
- FAQ section (5-8 questions)

### Phase 2: Expand Shallow Content (Weeks 5-7)
**Goal:** Strengthen existing content depth

| Existing Page | Current Words | Target Words | Sections to Add | Due Date |
|---------------|---------------|--------------|-----------------|----------|
| [Page 1] | 450 | 1,500 | [List specific sections] | Week 5 |
| [Page 2] | 680 | 1,500 | [List specific sections] | Week 6 |
| [Page 3] | 520 | 1,600 | [List specific sections] | Week 7 |

### Phase 3: Build Supporting Content (Weeks 8-12)
**Goal:** Create supporting articles for each pillar

| Pillar | Supporting Article | Word Count | Due Date |
|--------|-------------------|------------|----------|
| [Pillar 1] | [Supporting topic 1a] | 1,200 | Week 8 |
| [Pillar 1] | [Supporting topic 1b] | 1,000 | Week 9 |
| [Pillar 2] | [Supporting topic 2a] | 1,100 | Week 10 |
| [Pillar 3] | [Supporting topic 3a] | 1,300 | Week 11 |
| [Pillar 3] | [Supporting topic 3b] | 1,000 | Week 12 |

### Phase 4: Internal Linking Optimization (Week 13)
**Goal:** Connect all content in hub-and-spoke structure

**Tasks:**
1. Update hub page ([Core Topic]) to link to all pillars
2. Add contextual links from each pillar to 3-5 supporting articles
3. Add "Related Articles" sections to all supporting content
4. Create visual topic map for homepage or resources page
5. Update XML sitemap priority scores (hub = 1.0, pillars = 0.8, supporting = 0.6)

**Target Internal Linking Density:**
- Hub page: 8-12 outbound contextual links
- Pillar pages: 5-8 outbound contextual links
- Supporting articles: 3-5 outbound contextual links

---

## 5. Resource Requirements

### Content Creation:
- **New pillar pages:** [X] pages × 1,800 words avg = [X] hours writing ([X] hours @ $50-80/hr = $[X]-[X])
- **Content expansions:** [X] pages × 800 words added = [X] hours writing
- **Supporting articles:** [X] pages × 1,200 words avg = [X] hours writing
- **Total writing hours:** [X] hours
- **Total writing cost:** $[X]-[X]

### SEO Optimization:
- Keyword research: [X] hours
- Schema implementation: [X] hours
- Internal linking audit + fixes: [X] hours
- Image optimization: [X] hours
- **Total SEO hours:** [X] hours
- **Total SEO cost:** $[X]-[X] ([X] hours @ $75-100/hr)

### Project Management:
- Editorial calendar setup: 2 hours
- Writer briefings: [X] hours
- Content reviews: [X] hours
- **Total PM hours:** [X] hours

**Grand Total Investment:** $[X]-[X] | [X]-[X] hours | 90 days

---

## 6. Expected Outcomes

### 30 Days After Phase 1 Completion:
- **3 new pillar pages indexed** in Google
- **Topic coverage score:** +15-20% (from [X]% → [X]%)
- **Internal pages linking:** +25-40% (better crawlability)
- **Organic keywords ranking:** +10-15 new keywords in top 50

### 60 Days After Phase 2-3 Completion:
- **8-10 total new/expanded pages**
- **Topic coverage score:** +30-40% (from [X]% → [X]%)
- **Organic traffic:** +15-25% increase
- **Core topic keyword:** +5-8 position improvement
- **Featured snippet opportunity:** 2-3 pages eligible

### 90 Days After Full Roadmap Completion:
- **Topic coverage score:** ≥70% (competitive with top 3 sites)
- **Organic traffic:** +30-50% increase
- **Core topic keyword:** Top 5 position (if started from top 20)
- **Topic cluster pages:** Avg 3-5 minutes time on page (high engagement)
- **AI search citations:** Brand appears in 20-30% of relevant ChatGPT/Perplexity queries

**Revenue Impact (For E-commerce/SaaS):**
- 30% traffic increase × [X] monthly visitors = +[X] visitors
- Assuming [X]% conversion rate = +[X] conversions/month
- Assuming $[X] AOV/LTV = +$[X]-[X] monthly revenue

---

## 7. Next Steps

### Immediate Actions (This Week):
1. **Approve roadmap:** Review content titles and priorities with client
2. **Brief writers:** Provide content briefs for first 3 pillar pages (use `/content_brief` workflow)
3. **Set up editorial calendar:** Track all content pieces in Asana/Trello/Notion
4. **Assign responsibilities:** Who writes what and when

### Ongoing Monitoring:
- **Weekly:** Check indexing status of new pages (Google Search Console)
- **Bi-weekly:** Track keyword rankings for core topic and new pages (Ahrefs/Semrush)
- **Monthly:** Re-run topical audit to measure coverage score improvement
- **Quarterly:** Competitive analysis — are competitors filling their gaps too?

---

## 8. Quality Checklist

Before finalizing this audit, verify:
- [ ] Topic graph generated successfully via Wikipedia API
- [ ] Client site fully crawled (all blog/resource pages included)
- [ ] Gap analysis completed for all entities in graph
- [ ] Coverage score calculated and interpreted
- [ ] Competitive comparison includes ≥3 competitors
- [ ] 90-day roadmap is specific and time-bound
- [ ] Resource requirements estimated (hours + budget)
- [ ] Expected outcomes quantified (traffic, rankings, revenue)
- [ ] Report saved to `clients/<client>/reports/topical_audit_<topic>_YYYY_MM_DD.md`

---

**End of Report**
````

---

## Edge Cases & Handling

### Edge Case 1: Wikipedia Page Doesn't Exist for Core Topic
**Problem:** `topic_graph_mapper.py` returns empty results because the topic isn't well-defined on Wikipedia

**Solution:**
1. Try alternative phrasing (e.g., "Digital marketing" → "Online marketing" or "Internet marketing")
2. Use a broader topic (e.g., "CRM" → "Customer relationship management" → "Business software")
3. If still no results, manually create semantic graph:
   - Research top 10 Google results for core keyword
   - Extract common H2s/H3s from competitor sites
   - Use these as proxy entities
4. Document in report: "[WARNING] Wikipedia-based graph unavailable, using competitor-derived entity list"

### Edge Case 2: Client Has No Blog/Content Section
**Problem:** Client site is primarily product pages, no resource center

**Solution:**
1. **Option A:** Recommend creating `/resources/` or `/learn/` section for topic cluster
2. **Option B:** Integrate topical content into product pages:
   - Product page H2s should cover related entities
   - Add "How it Works" and "Use Cases" sections covering supporting topics
3. **Option C:** External content strategy:
   - Guest posts on industry blogs
   - Medium/LinkedIn articles linking back to product pages
   - YouTube videos covering topic cluster (with video schema on site)

### Edge Case 3: Topic Coverage Score Already High (>80%)
**Problem:** Client already has comprehensive coverage, topical audit shows few gaps

**Solution:**
1. **Celebrate!** Client is ahead of most competitors
2. Shift focus to **content depth** and **freshness**:
   - Expand existing pages to 2,000+ words
   - Add original data/case studies
   - Update statistics and examples (freshness signal)
3. **Advanced strategy:**
   - Create **ultimate guides** (5,000-10,000 word comprehensive resources)
   - Build **interactive tools** (calculators, assessments)
   - Launch **video content** covering same topics (multimodal signal)

### Edge Case 4: Overwhelming Gap Count (>50 Missing Entities)
**Problem:** Topic is too broad, graph returns 100+ entities, client coverage is <20%

**Solution:**
1. **Narrow the focus:**
   - Instead of "Marketing", focus on "Content Marketing" or "Email Marketing"
   - Instead of "Software Development", focus on "Web Development" or "Mobile App Development"
2. **Prioritize ruthlessly:**
   - Only create content for entities with >500 monthly search volume
   - Only create content for entities where competitors rank in top 3
   - Ignore obscure or low-value entities
3. **Set realistic expectations:**
   - 90-day plan can realistically deliver 10-15 new/expanded pages
   - Full topic coverage may take 6-12 months
   - Break into multiple quarterly roadmaps

### Edge Case 5: Client Content Exists but NOT Indexed
**Problem:** Crawl finds pages, but they aren't in Google's index (GSC shows "Crawled - currently not indexed")

**Solution:**
1. **Quality issue:** Content is too thin or duplicate
   - Expand pages to 1,200+ words
   - Add unique value (examples, case studies, original data)
2. **Technical issue:** Crawlability or canonicalization problem
   - Check robots.txt isn't blocking
   - Verify canonical tags aren't pointing elsewhere
   - Improve internal linking to these pages
3. **Authority issue:** Domain lacks trust signals
   - Build backlinks to hub page
   - Get entity established via `/entity_audit` workflow
   - Improve E-E-A-T signals (author bios, about page, social proof)

---

## Integration with Other Workflows

### After Topical Audit → Launch /content_cluster_architect:
Once gaps are identified, use the content cluster architect workflow to generate:
- Detailed content briefs for each missing piece
- Hub-and-spoke internal linking structure
- Schema templates for each page type

```bash
# Example integration
/content_cluster_architect --topic "CRM Software" --missing-pillars "Sales Pipeline,Lead Scoring,Data Integration"
```

### Combine with /competitor_gap:
Layer topical authority audit with keyword gap analysis:
1. Run topical audit (entity-based gaps)
2. Run competitor gap (keyword-based gaps)
3. Merge results: Entities + Keywords = Complete content strategy

### Include in /monthly_report:
Track topical authority improvement monthly:
- Coverage score: [X]% → [Y]% (+Z%)
- New pages published: [X]
- Ranking improvements: [X] keywords moved up
- Organic traffic from topic cluster pages: +[X]%

---

## Automation & Scaling

### Monthly Topical Authority Tracking:
Create a monitoring script that automatically:
1. Re-runs `topic_graph_mapper.py` (graph may expand as Wikipedia updates)
2. Re-crawls client site (detects new content automatically)
3. Recalculates coverage score
4. Sends email alert if score drops >5% (indicates competitor caught up)

### Multi-Topic Audits:
For clients with multiple service lines, run topical audits for each:
```bash
/topical_audit "CRM Software" client.com
/topical_audit "Marketing Automation" client.com
/topical_audit "Sales Enablement" client.com
```

Generate separate roadmaps, prioritize based on business goals.

---

**End of Workflow**
