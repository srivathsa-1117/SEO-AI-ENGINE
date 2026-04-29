---
name: entity-building
description: >
  When the user wants to build brand entity recognition in Google's Knowledge Graph,
  establish Wikipedia or Wikidata presence, fix NAP consistency, or implement entity
  schema markup. Also use when the user mentions "entity audit", "Knowledge Panel",
  "Knowledge Graph", "Wikipedia presence", "Wikidata", "branded search", "entity SEO",
  "sameAs schema", "brand not showing in Google", or "Knowledge Graph entry." Use when
  a client has weak brand recognition despite strong content, is not appearing for
  branded queries, or competitors have Knowledge Panels and they don't.
  Invoked by: /entity_audit command, /audit workflow, Rule 19 in CLAUDE.md.
allowed-tools: Read, Bash, Grep, Glob, WebFetch, Write
---

# Entity Building & Knowledge Graph Optimization Skill

## Core Capability
Build brand entity recognition in Google's Knowledge Graph through Wikipedia, Wikidata, schema markup, and NAP consistency. Required for competitive ranking in 2026.

---

## When to Use This Skill

**Trigger Conditions:**
- User says "entity audit", "Knowledge Panel", "Knowledge Graph", "Wikipedia presence"
- Client has weak brand recognition despite strong content
- Client is not appearing for branded queries
- Competitor analysis shows rivals have Knowledge Panels
- Monthly report shows declining branded search impressions
- New client onboarding for established brands (3+ years old)

**DO NOT use this skill if:**
- Brand is less than 1 year old (unlikely to meet Wikipedia notability guidelines)
- Client has zero press mentions or external coverage
- Client is individual freelancer (use Person schema instead, different workflow)

---

## Success Criteria

**Entity strength score ≥70/100 within 90 days**, measured by:
- Wikipedia article exists (40 points) OR Wikidata entity exists (15 points minimum)
- Knowledge Panel appears for branded queries (20 points)
- NAP consistency across 8+ sources (10 points)
- Entity schema with @id and sameAs implemented (5 points)
- 5+ authority mentions tracked (5 points)
- Crunchbase or similar profile (5 points)

**User receives:**
- Entity audit report (.docx)
- Specific action plan based on current score
- Schema code ready to implement
- Wikipedia draft (if eligible)
- Wikidata item created (mandatory, even if Wikipedia rejected)

---

## Pre-Execution Checklist

BEFORE running entity_auditor.py, verify:
- Client has brand_kit.json with complete NAP data (name, address, phone, website)
- Client has been in business for 1+ years (check brand_kit.json onboarding_date)
- Client has external mentions (press, industry blogs, podcasts)
- You have access to client's social profiles (LinkedIn, Twitter, Crunchbase)

**If any item fails:** Ask user to provide missing data before proceeding.

---

## Execution Protocol

### Step 1: Run Entity Auditor Tool

Expected output: JSON file with entity strength score (0-100) and check results.

If tool fails with ModuleNotFoundError, install: pip install requests beautifulsoup4 lxml

Validation:
- File exists at .tmp/{client}_entity_audit.json
- File contains "entity_score" key
- Score is between 0-100

### Step 2: Parse Results & Determine Path

Decision tree:
- **Score 0-30:** Start with Wikidata creation only
- **Score 31-60:** Create Wikidata + attempt Wikipedia if notability threshold met
- **Score 61-100:** Full optimization (Wikipedia, Wikidata, schema, NAP fixes)

### Step 3: Wikipedia Eligibility Assessment

Wikipedia has strict notability guidelines. A brand qualifies if it meets ANY of these:
1. **Multiple independent sources:** 3+ articles in major publications
2. **Industry recognition:** Won industry awards, featured in industry reports
3. **Significant impact:** Generated significant discussion/coverage in media
4. **Book coverage:** Mentioned in published books about the industry

Threshold:
- 3+ independent editorial sources → ELIGIBLE for Wikipedia
- 1-2 sources → NOT ELIGIBLE yet, focus on Wikidata
- 0 sources → Recommend PR campaign first

### Step 4: Create Wikidata Entity (MANDATORY)

Even if Wikipedia is rejected, Wikidata is essential. Anyone can create Wikidata entities.

**Process:**
1. Create Wikidata account: https://www.wikidata.org/w/index.php?title=Special:CreateAccount
2. Create new item: https://www.wikidata.org/wiki/Special:NewItem

**Minimum required statements:**
- Label (English): The Example Brand
- Description (English): Digital marketing agency in India
- instance of (P31): business (Q4830453) OR company (Q783794)
- country (P17): India (Q668)
- headquarters location (P159): Bengaluru (Q1355)
- inception (P571): [founding year]
- official website (P856): https://example.com

**Recommended additional statements:**
- industry (P452): advertising (Q37038) OR marketing (Q39809)
- founder (P112): [founder name]
- email address (P968)
- phone number (P1329)
- LinkedIn company ID (P4264)
- X username (P2002)

After creation, note the Wikidata Q-ID (e.g., Q123456789). You will need this for schema markup.

### Step 5: Implement Entity Schema Markup

Use schema_gen.py with --entity-mode flag to generate Organization schema with @id and sameAs properties.

Implementation instructions for client:
- Add script to <head> section of homepage
- Also add to About Us page and Contact page
- Validate with Google Rich Results Test

### Step 6: NAP Consistency Audit & Fixes

NAP (Name, Address, Phone) must match EXACTLY across all platforms.

Check 12 sources: Website, Google Business Profile, Bing Places, Yelp, LinkedIn, Crunchbase, Facebook, Industry directories, BBB, Chamber of Commerce, local directories.

Expected improvement: +5 to +10 points.

### Step 7: Build Authority Mentions

Target platforms: Wikipedia mentions, news sites, podcasts, industry reports, Reddit/Quora, YouTube.

Target: 3-5 new authority mentions per month.

### Step 8: Monitor Knowledge Panel Status

Check weekly if Knowledge Panel appears for branded searches.

Timeline expectations:
- Wikidata created: 2-4 weeks
- Wikipedia approved: 1-2 weeks after approval
- Schema + NAP fixes: 4-8 weeks

### Step 9: Generate Entity Audit Report

Create comprehensive report with entity audit data and 90-day implementation roadmap.

---

## Edge Cases & Error Handling

**Brand Name Conflict:** Use disambiguated Wikidata label.
**Wikipedia Deleted:** Keep Wikidata, build coverage, retry in 6 months.
**Multiple Locations:** Separate LocalBusiness schemas for each.
**No Physical Address:** Use country only in Wikidata, email contactPoint.
**Tool Timeout:** Wait 60s, retry, or check manually.

---

## Quality Gates Checklist

**Wikidata:**
- Wikidata item created with Q-ID
- Minimum 6 statements added
- No duplicate items exist

**Schema Markup:**
- Organization schema includes @id
- sameAs array includes Wikidata URL
- Schema validates with no errors

**NAP Consistency:**
- Canonical NAP format documented
- Checked 8+ sources
- Mismatch rate < 20%

**Documentation:**
- Entity audit report generated
- Wikidata Q-ID documented in brand_kit.json
- Schema code saved
- Implementation instructions provided

---

## Success Metrics

**Primary:**
- Entity strength score (target: +20 points in 90 days)
- Knowledge Panel appearance (target: visible within 60 days if Wikipedia approved)

**Secondary:**
- Branded search impressions (target: +15% increase)
- Position for branded keywords (target: #1 with sitelinks)
- Authority mentions (target: 3-5 new/month)

---

## Tool Dependencies

**Required:** tools/entity_auditor.py, tools/schema_gen.py, tools/report_builder.py

**Optional:** tools/brand_mention_tracker.py, tools/serp_scraper.py

**Manual steps:** Wikidata creation (10-15 min), Wikipedia AfC submission (30-45 min if eligible), NAP corrections (1-3 hours)

---

## Integration Points

**Invoked by:** /entity_audit slash command, /audit workflow, /monthly_report workflow

**Invokes:** schema_gen.py (entity mode), entity_auditor.py (scoring), report_builder.py (deliverable)

**Outputs used by:** /monthly_report (track entity score), /audit (flag missing signals), CLAUDE.md Rule 19

---

## Final Notes

**Entity SEO is not optional in 2026.** Brands without Knowledge Graph presence will struggle to rank competitively.

**Timeline:** Full optimization takes 60-90 days. Wikidata + schema: 1-2 days.

**Cost:** Zero. Time: 4-6 hours initial, 1-2 hours/month ongoing.

**ROI:** 15-25% increase in branded search CTR and improved rankings for non-branded terms.

**When in doubt:** Create Wikidata entity even if Wikipedia is rejected. Wikidata alone provides significant entity signal value.
