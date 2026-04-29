---
description: /entity_audit - Assess brand entity recognition and Knowledge Graph eligibility
---

# Workflow: Entity SEO Audit & Knowledge Graph Strategy

## Trigger
```
/entity_audit <brand_name> --website <url> [--output-report]
```
**Examples:**
- `/entity_audit "The Example Brand" --website https://example.com`
- `/entity_audit "Acme Corp" --website https://acme.com --output-report`

---

## Objective

Assess brand's **entity recognition strength** and create roadmap to achieve **Google Knowledge Panel**.

**Entity = Brand recognized by search engines as a distinct, verifiable "thing" (not just keywords)**

**Success Metrics**:
- Entity strength score ≥60 → Knowledge Panel eligible
- Wikipedia article → 40-point boost
- Timeline: 1-3 months (with Wikipedia) or 6-18 months (without)

**Why This Matters (2026)**:
- AI Overviews only cite recognized entities
- Knowledge Panels capture 30-40% of brand search clicks
- Entity status required for Local Pack (local businesses)
- Voice search heavily favors entities

---

## Prerequisites

**Required Information**:
1. Official brand name (exact match critical)
2. Primary website URL
3. Business category/industry
4. Physical address (if local business)
5. Social media profiles (LinkedIn, Twitter, Facebook)

**When to Use This Workflow**:
- Local businesses (GBP optimization dependency)
- Brand awareness campaigns
- Competing for Knowledge Panel
- AI Overviews strategy
- Voice search optimization

**When NOT to Use**:
- Brand new companies (<6 months old - build SEO first)
- Pure e-commerce (focus on product entity, not brand entity)
- Niche B2B with no Wikipedia notability (focus on industry registries instead)

---

## Step-by-Step Execution

### Step 1: Run Entity Auditor Tool

```bash
python tools/entity_auditor.py \
  --brand "{brand_name}" \
  --website {url} \
  --output .tmp/{slug}_entity_audit.json
```

**Tool checks**:
1. Wikipedia presence
2. Wikidata entity
3. Google Knowledge Panel
4. NAP (Name, Address, Phone) consistency
5. Schema markup (@id, sameAs)
6. Authority site mentions
7. Crunchbase profile

**Output**:
```json
{
  "entity_strength_score": 42,
  "checks": {...},
  "timeline_estimate": "12-18 months",
  "roadmap": [...]
}
```

---

### Step 2: Interpret Entity Strength Score

| Score Range | Status | Meaning | Timeline to Knowledge Panel |
|-------------|--------|---------|----------------------------|
| **80-100** | [OK] Strong | Panel likely exists or imminent | Already qualified |
| **60-79** | [OK] Good | Panel eligible with minor work | 3-6 months |
| **30-59** | [WARNING] Moderate | Significant work needed | 6-12 months |
| **0-29** | [CRITICAL] Weak | Major effort required | 12-18+ months |

**Present to user**:
```
Entity Strength Score: 42/100

Status: [WARNING] Moderate entity strength
Timeline: 12-18 months to Knowledge Panel eligibility
Recommendation: Focus on Wikipedia submission + NAP consistency
```

---

### Step 3: Deep Dive - Wikipedia Eligibility Check

**Wikipedia is the #1 entity signal** (+40 points)

#### Check Notability Criteria

Wikipedia requires **multiple independent, reliable sources** covering the subject.

**Notability checklist for organizations**:
- [ ] Coverage in national/international media (newspapers, magazines)
- [ ] Industry awards or recognition
- [ ] Published books/academic papers about the organization
- [ ] Government recognition or contracts
- [ ] Significant social/economic impact

**Minimum**: 3-5 independent sources (not press releases, not self-published)

**Tool to find sources**:
```bash
# Search for press mentions
python tools/brand_mention_tracker.py \
  --brand "{brand_name}" \
  --min-domain-authority 50 \
  --output .tmp/{slug}_press_mentions.json
```

**If 3+ high-authority mentions found**:
→ Eligible for Wikipedia (proceed to Step 4)

**If <3 mentions found**:
→ Not eligible yet (build press coverage first)
→ Alternative: Focus on Wikidata + schema (Step 5-6)

---

### Step 4: Wikipedia Article Creation (If Eligible)

**[WARNING] Do NOT create spammy/promotional Wikipedia articles**
- Wikipedia is an encyclopedia, not a marketing platform
- Promotional articles get deleted within hours
- Neutral tone mandatory

#### Wikipedia Creation Process

**Option A: Hire Wikipedia editor** ($500-$2,000)
- Services: WikiExperts, Beutler Ink, Freeman Spokesperson
- They handle notability verification, writing, submission
- Timeline: 4-8 weeks
- Success rate: 70-80% (if truly notable)

**Option B: DIY approach** (free, but risky)

1. **Create Wikipedia account** (free)
   - https://en.wikipedia.org/w/index.php?title=Special:CreateAccount
   - Build edit history on other articles (10-20 edits over 2-4 weeks)
   - Avoid "new account" flag

2. **Draft article in sandbox**
   - https://en.wikipedia.org/wiki/Special:MyPage/sandbox
   - Use neutral, encyclopedic tone
   - Cite all claims with reliable sources
   - Follow manual of style: https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style

3. **Article structure template**:
````markdown
== [Company Name] ==

[Company Name] is a [category] company based in [location], founded in [year].

== History ==
[Factual history with citations]

== Products/Services ==
[Neutral description]

== Recognition ==
[Awards, press coverage - ALL CITED]

== References ==
<references />

== External links ==
* [Official website]
````

4. **Submit for review**
   - Move from sandbox to mainspace
   - Add to "Articles for Creation" queue
   - Wait 2-8 weeks for review

5. **Common rejection reasons**:
   - Promotional tone (fix: rewrite neutrally)
   - Insufficient sourcing (fix: add 2-3 more independent sources)
   - Non-notable subject (fix: wait until you are notable)

**Success rate DIY**: 30-50% (high rejection risk)

**Recommendation**: Hire professional if budget allows

---

### Step 5: Wikidata Entity Creation (MANDATORY, even without Wikipedia)

**Wikidata = Free, easy, high-value entity signal** (+15 points)

**Anyone can create Wikidata entities** (no notability requirement)

#### Wikidata Creation Process (10-15 minutes)

1. **Create Wikidata account**
   - https://www.wikidata.org/w/index.php?title=Special:CreateAccount

2. **Create new item**
   - https://www.wikidata.org/wiki/Special:NewItem
   - Click "Create a new item"

3. **Fill required fields**:
```
Label (en): The Example Brand
Description (en): Digital marketing agency based in Bengaluru, India
Also known as: Example Brand, exampleclient

Statements:
- instance of (P31): business (Q4830453)
- country (P17): India (Q668)
- headquarters location (P159): Bengaluru (Q1355)
- inception (P571): [founding year]
- official website (P856): https://example.com
- industry (P452): digital marketing (Q1323528)
```

4. **Add identifier links**:
```
- LinkedIn company ID (P4264): [your LinkedIn company URL slug]
- Twitter username (P2002): [your Twitter handle without @]
- Facebook ID (P2013): [your Facebook page ID]
- official website (P856): [your URL]
```

5. **Publish**
   - Click "Publish"
   - Get Wikidata ID (e.g., Q12345678)
   - **SAVE THIS ID** for schema markup

**Verification**:
```bash
# Check your entity was created
curl "https://www.wikidata.org/wiki/Q12345678"
```

**Value**: Wikidata entity = +15 entity score + schema sameAs target

---

### Step 6: Schema Markup with @id and sameAs

**Critical for entity validation**

Update website schema to include entity signals:

```bash
# Generate entity-aware Organization schema
python tools/schema_gen.py \
  --type Organization \
  --entity-mode \
  --data .tmp/{slug}_entity_data.json \
  --output .tmp/{slug}_organization_schema.json
```

**Entity data JSON**:
```json
{
  "name": "The Example Brand",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "description": "Digital marketing agency based in Bengaluru, India",
  "wikidata_id": "Q12345678",
  "wikipedia_url": "https://en.wikipedia.org/wiki/The_Dare_Network",
  "social_profiles": {
    "linkedin": "https://www.linkedin.com/company/exampleclient",
    "twitter": "https://twitter.com/exampleclient",
    "facebook": "https://www.facebook.com/exampleclient"
  },
  "address": {
    "streetAddress": "123 MG Road",
    "addressLocality": "Bengaluru",
    "addressRegion": "Karnataka",
    "postalCode": "560001",
    "addressCountry": "IN"
  },
  "contact": {
    "telephone": "+91-80-12345678",
    "email": "hello@example.com"
  }
}
```

**Generated schema (example)**:
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://example.com/#organization",
  "name": "The Example Brand",
  "url": "https://example.com",
  "logo": {
    "@type": "ImageObject",
    "url": "https://example.com/logo.png"
  },
  "description": "Digital marketing agency based in Bengaluru, India",
  "sameAs": [
    "https://www.wikidata.org/wiki/Q12345678",
    "https://en.wikipedia.org/wiki/The_Dare_Network",
    "https://www.linkedin.com/company/exampleclient",
    "https://twitter.com/exampleclient",
    "https://www.facebook.com/exampleclient"
  ],
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 MG Road",
    "addressLocality": "Bengaluru",
    "addressRegion": "Karnataka",
    "postalCode": "560001",
    "addressCountry": "IN"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+91-80-12345678",
    "email": "hello@example.com",
    "contactType": "customer service"
  }
}
```

**Key elements**:
- `@id`: Unique identifier for this entity
- `sameAs`: Array of entity verification URLs (Wikidata, Wikipedia, social)
- Complete NAP data (Name, Address, Phone)

**Implementation**:
1. Add to website `<head>` section
2. Validate: https://validator.schema.org/
3. Test: Google Rich Results Test

---

### Step 7: NAP Consistency Audit (Critical for Local Businesses)

**NAP = Name, Address, Phone**

Google validates entities by checking consistency across multiple sources.

#### Sources to Audit (Minimum 10)

**Tier 1: Must-Have**
1. Own website
2. Google Business Profile
3. Facebook Business Page
4. LinkedIn Company Page

**Tier 2: High-Value**
5. Yelp
6. Bing Places
7. Apple Maps
8. Yellow Pages (local directories)

**Tier 3: Industry-Specific**
9. Crunchbase (B2B/startups)
10. Industry associations
11. Chamber of Commerce
12. BBB (Better Business Bureau)

#### NAP Audit Process

```bash
# Manual check (tool not built yet)
# For each source, verify:
# 1. Business name EXACTLY matches
# 2. Address EXACTLY matches (including suite #, formatting)
# 3. Phone number EXACTLY matches (including country code)
# 4. Website URL EXACTLY matches
```

**Common NAP inconsistencies**:
- "The Example Brand" vs "Example Brand" (drop "The")
- "+91 80 1234 5678" vs "+91-80-1234-5678" (formatting)
- "Suite 301" vs "Ste 301" vs "#301" (abbreviations)
- Old phone number not updated everywhere

**Fix process**:
1. Choose canonical version (e.g., full legal name, formatted phone)
2. Update ALL sources to match exactly
3. Re-check after 2 weeks

**Tool for tracking** (create spreadsheet):
| Source | Name Match | Address Match | Phone Match | URL Match | Status |
|--------|------------|---------------|-------------|-----------|--------|
| Website | ✓ | ✓ | ✓ | ✓ | [OK] |
| Google Business | ✓ | ✗ (old) | ✓ | ✓ | [ERROR] Fix needed |
| Facebook | ✓ | ✓ | ✗ (old #) | ✓ | [ERROR] Fix needed |

**Value**: 100% NAP consistency = +10 entity score

---

### Step 8: Build Authority Mentions (Hardest, Highest Value)

**Goal**: Get mentioned on 10+ high-authority sites (DA 50+)

**Why**: Google validates entities through third-party mentions

#### Strategies to Build Mentions

**Strategy 1: Press Releases** (Medium difficulty)
- Use PRWeb, PRNewswire, BusinessWire
- Cost: $100-$500 per release
- Success: 3-5 pickups per release
- Timeline: 1-2 weeks per release
- ROI: Medium (some are low-quality syndication)

**Strategy 2: Guest Posts** (High difficulty)
- Pitch industry blogs (Search Engine Land, Moz, HubSpot)
- Author bio includes brand mention
- Cost: Free (time investment)
- Success: 1-2 accepted per 10 pitches
- Timeline: 4-8 weeks per post
- ROI: High (editorial links, brand authority)

**Strategy 3: Industry Awards** (Medium difficulty)
- Apply for "Best [Category] Company" awards
- Many free to enter
- Winning = automatic press mention
- Timeline: Annual cycles
- ROI: High (credibility + mention)

**Strategy 4: Podcast Appearances** (Low-Medium difficulty)
- Pitch industry podcasts
- Show notes often link to company
- Cost: Free
- Success: 3-5 accepted per 10 pitches
- Timeline: 2-4 weeks per podcast
- ROI: High (brand building + link)

**Strategy 5: HARO (Help A Reporter Out)** (Low difficulty)
- Sign up: https://www.helpareporter.com/
- Answer journalist queries
- Get quoted in articles
- Cost: Free
- Success: 1-3 mentions per month (if active)
- Timeline: Ongoing
- ROI: High (editorial mentions)

**Strategy 6: Wikipedia Citations** (High value if you have article)
- Once Wikipedia article exists, get cited by others
- Industry blogs often cite Wikipedia as source
- Creates citation loop (Wikipedia ← Industry site → Your brand)

**Minimum target**: 10 mentions within 6 months

---

### Step 9: Monitor Knowledge Panel Status

**How to check if Knowledge Panel exists**:

1. **Manual Google search**:
   - Search exact brand name in Google
   - Check right sidebar for Knowledge Panel
   - Check mobile results (often shows sooner)

2. **Google Knowledge Graph API** (if available):
```bash
# Requires Google Cloud API key
# Check GOOGLE_API_KEY in .env

curl "https://kgsearch.googleapis.com/v1/entities:search?query={brand_name}&key={api_key}&limit=1"
```

**If Knowledge Panel exists**:
```json
{
  "itemListElement": [{
    "result": {
      "@type": "Thing",
      "name": "The Example Brand",
      "description": "Digital marketing agency",
      ...
    }
  }]
}
```

**If no panel yet**:
```json
{
  "itemListElement": []
}
```

**Monitoring frequency**:
- Weeks 1-4: Check weekly
- Months 2-6: Check bi-weekly
- Months 6+: Check monthly

**Typical timeline**:
- With Wikipedia: Panel appears in 4-12 weeks
- Without Wikipedia: Panel appears in 6-18 months (if ever)

---

### Step 10: Generate Entity Audit Report

**Create client-friendly report**:

````markdown
# Entity SEO Audit Report

**Brand**: {brand_name}
**Website**: {url}
**Audit Date**: {date}

## Executive Summary

Entity Strength Score: **42/100** [WARNING] Moderate

**Status**: Your brand has moderate entity recognition. Google does not yet
recognize you as a distinct entity eligible for a Knowledge Panel.

**Timeline**: 12-18 months to Knowledge Panel eligibility with recommended actions.

**Critical Gap**: No Wikipedia article (worth +40 points)

## Detailed Findings

### 1. Wikipedia Presence: [ERROR] Not Found
- **Impact**: -40 points
- **Status**: No Wikipedia article exists
- **Eligibility**: Checking notability criteria...
  - Press mentions: 2 found (need 3-5)
  - Industry recognition: Limited
  - **Recommendation**: Build 1-3 more high-authority press mentions, then create article

### 2. Wikidata Entity: [WARNING] Not Found
- **Impact**: -15 points
- **Status**: No Wikidata entity
- **Action**: CREATE NOW (takes 10 minutes, free, no approval needed)
- **Instructions**: See Step 5 of entity_audit.md workflow

### 3. Google Knowledge Panel: [ERROR] Not Present
- **Impact**: -20 points
- **Status**: No Knowledge Panel when searching "{brand_name}"
- **Why**: Entity score too low (<60 required)
- **Timeline**: 12-18 months with roadmap implementation

### 4. NAP Consistency: [WARNING] 60% Consistent
- **Impact**: +6 points (out of 10 possible)
- **Issues**:
  - Google Business Profile: Old phone number
  - Facebook: Missing street address
  - Yelp: Name shows "Example Brand" not "The Example Brand"
- **Action**: Fix all 3 sources within 1 week

### 5. Schema Markup: [WARNING] Basic
- **Impact**: +2 points (out of 5 possible)
- **Current**: Has Organization schema
- **Missing**: @id and sameAs properties
- **Action**: Update schema (see generated code in .tmp/)

### 6. Authority Mentions: [ERROR] Insufficient
- **Impact**: 0 points (out of 5 possible)
- **Found**: 2 mentions (need 10+)
- **Quality**: Both DA <40
- **Action**: Build 8 more high-DA mentions (see strategies)

### 7. Crunchbase: [OK] Present
- **Impact**: +5 points
- **URL**: https://www.crunchbase.com/organization/example-brand
- **Status**: Profile exists and is current

## Improvement Roadmap

### Phase 1: Quick Wins (Week 1-2)
**Priority 1: Create Wikidata Entity**
- Time: 10-15 minutes
- Impact: +15 points
- Difficulty: Low
- Instructions: [Link to Step 5]

**Priority 2: Fix NAP Inconsistencies**
- Time: 2-3 hours
- Impact: +4 points (from 6 → 10)
- Difficulty: Low
- Action items:
  1. Update Google Business Profile phone number
  2. Add complete address to Facebook
  3. Change Yelp name to include "The"

**Priority 3: Update Schema Markup**
- Time: 30 minutes
- Impact: +3 points (from 2 → 5)
- Difficulty: Low (if developer available)
- File: .tmp/{slug}_organization_schema.json

**Total Quick Wins**: +22 points (42 → 64) → **Knowledge Panel eligible!**

### Phase 2: Medium-Term (Months 1-6)
**Priority 4: Build Authority Mentions**
- Time: 4-6 months ongoing
- Impact: +5 points + authority boost
- Difficulty: Medium
- Tactics:
  - HARO: 2-3 responses per week
  - Guest posts: 1 per month
  - Podcasts: 1 per month
  - Press releases: 1 per quarter

**Priority 5: Pursue Wikipedia Article**
- Time: 2-4 months
- Impact: +40 points (64 → 104, capped at 100)
- Difficulty: High
- Prerequisites: 3-5 high-authority press mentions first
- Options:
  - Hire professional: $500-$2,000
  - DIY: Free but 30-50% success rate

### Phase 3: Monitoring (Ongoing)
- Check Knowledge Panel status weekly
- Monitor entity score monthly
- Update schema when social profiles change
- Maintain NAP consistency

## Expected Timeline

**Optimistic** (if Wikipedia approved quickly):
- Week 1-2: Wikidata + NAP + Schema → Score 64
- Month 2-3: Wikipedia article submitted
- Month 4-5: Wikipedia approved → Score 100+
- Month 5-6: Knowledge Panel appears

**Realistic** (typical path):
- Month 1-2: Quick wins → Score 64 (Panel eligible)
- Month 3-8: Build press mentions + authority
- Month 8-12: Wikipedia submission
- Month 12-18: Knowledge Panel appears

**Conservative** (if Wikipedia rejected):
- Month 1-2: Quick wins → Score 64
- Month 3-12: Build authority mentions → Score 69
- Month 12-18: Continue building signals
- Month 18-24: Knowledge Panel appears (without Wikipedia)

## ROI Analysis

### Benefits of Knowledge Panel

**Brand Search Dominance**:
- Knowledge Panel captures 30-40% of clicks
- Reduces competitor visibility
- Builds instant credibility

**AI Search Visibility**:
- Entities get cited in AI Overviews
- Required for voice search results
- ChatGPT/Perplexity prefer recognized entities

**Local SEO (if local business)**:
- Required for consistent Local Pack appearance
- Improves Google Business Profile authority
- Boosts "near me" rankings

### Investment vs Return

**Investment**:
- Time: 20-30 hours over 12 months (if DIY)
- Cost: $0-$2,000 (free if DIY, up to $2K if hiring Wikipedia editor)

**Return**:
- Brand search traffic: +30-40%
- AI citation rate: +15-25%
- Local Pack visibility: +50% (if local)
- Voice search results: 10x increase
- Long-term brand equity: Immeasurable

**Payback**: 6-12 months for most businesses

## Next Steps

1. **This Week**: Create Wikidata entity (10 min) + Fix NAP (2 hrs)
2. **This Month**: Update schema + Start HARO responses
3. **Month 2-3**: Secure 2-3 guest post placements
4. **Month 3-6**: Build to 10+ authority mentions
5. **Month 6+**: Evaluate Wikipedia eligibility, submit if ready
6. **Month 12+**: Monitor for Knowledge Panel appearance

## Appendix: Resources

- Wikidata creation guide: https://www.wikidata.org/wiki/Help:Items
- Wikipedia notability guidelines: https://en.wikipedia.org/wiki/Wikipedia:Notability
- Schema validator: https://validator.schema.org/
- HARO signup: https://www.helpareporter.com/
- Knowledge Graph API: https://developers.google.com/knowledge-graph/

---

**Report Generated**: {timestamp}
**Auditor**: SEO AIOS Entity Audit Workflow
````

**Save as**: `reports/{client}_Entity_Audit_{date}.md`

---

## Quality Gates

Before completing workflow, verify:

- [CHECKLIST] Entity auditor tool ran successfully
- [CHECKLIST] All 7 checks completed (Wikipedia, Wikidata, Panel, NAP, Schema, Mentions, Crunchbase)
- [CHECKLIST] Entity score calculated (0-100)
- [CHECKLIST] Roadmap generated with priorities
- [CHECKLIST] Timeline estimated
- [CHECKLIST] Report created and saved
- [CHECKLIST] Next steps clearly defined
- [CHECKLIST] Client understands quick wins (Wikidata + NAP + Schema)

---

## Edge Cases

### Edge Case 1: Entity Score Already High (≥80)

**Scenario**: Brand already has strong entity presence

**Action**:
1. Confirm Knowledge Panel exists
2. If yes: Focus on optimization (update schema, improve panel data)
3. If no: Investigate why (possible: wrong name variation, disambiguation needed)
4. Report: "[OK] Strong entity. Focus on maintenance and AI search optimization."

### Edge Case 2: Brand Name Disambiguation Issue

**Scenario**: Multiple entities with same name (e.g., "Phoenix" = city, band, mythical bird)

**Action**:
1. Check if Wikipedia article needs disambiguation (e.g., "Phoenix (band)")
2. Use full legal name in schema (@id)
3. Add industry clarification in Wikidata description
4. Expect longer timeline (12-18 months vs 6-12)

### Edge Case 3: Local Business Chain (Multiple Locations)

**Scenario**: Business has 5+ locations

**Action**:
1. Create entity for parent brand (Organization schema)
2. Create entity for each location (LocalBusiness schema with @id)
3. Link locations to parent via "branchOf" property
4. NAP consistency CRITICAL for each location
5. Expect: Brand panel + location-specific panels

### Edge Case 4: Wikipedia Rejection

**Scenario**: Submitted article rejected as "non-notable"

**Action**:
1. DO NOT resubmit immediately (will get blocked)
2. Build 3-5 more high-authority press mentions
3. Wait 6-12 months
4. Resubmit with improved sourcing
5. Alternative: Focus on Wikidata + schema + mentions (can still reach 60-70 score)

### Edge Case 5: Startup/New Brand (<2 Years Old)

**Scenario**: Very new company, no press history

**Action**:
1. Acknowledge: "Entity building takes time"
2. Start with quick wins (Wikidata + NAP + schema) → Score 20-30
3. Focus on traditional SEO while building entity
4. Revisit entity strategy in 12 months
5. Set expectations: 18-24 month timeline

---

## Integration with Other Workflows

### With `/audit`
- Include entity score in technical audits
- Flag low entity strength as technical issue
- Recommend entity workflow if score <60

### With `/content_draft`
- Mention entity-building content ideas
- Create "About Us" page optimized for entity recognition
- Add founder bios (Person entities linked to Organization entity)

### With `/monthly_report`
- Track entity score month-over-month
- Monitor Knowledge Panel appearance
- Report authority mention count

### With `/aeo_optimize`
- Entities get cited more in AI search
- High entity score = 2x citation rate vs non-entities

---

**END OF WORKFLOW**

**Expected Execution Time**: 30-60 minutes for audit, 10-30 hours for full implementation
**Skill Level**: Intermediate (understanding of Wikipedia + schema markup)
**ROI**: Very high (Knowledge Panel = 30-40% brand search traffic)
