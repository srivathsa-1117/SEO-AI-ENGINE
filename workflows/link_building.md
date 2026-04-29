---
description: /link_building - Find link opportunities and draft outreach emails
---

# Workflow: Link Building & Outreach

## Trigger
```
/link_building <client_name> [--mode guest_post|unlinked_mentions|resource_links]
```
**Example:** `/link_building acme_corp --mode guest_post`

## Objective
Discover relevant, high-quality backlink opportunities using free tools and draft personalized outreach emails ready to send.

## Required Inputs
1. `<client_name>` — loads brand_kit for niche/industry
2. `--mode` — defaults to `guest_post` if not specified

## CRITICAL AWARENESS: 2026 Link Building Changes

**What Changed:**
- **AI Citations > Traditional Backlinks:** Being cited by ChatGPT/Perplexity/Gemini is now more valuable than a backlink from a DA50 blog
- **Unlinked Mentions Have 40-60% Conversion Rate:** Far better ROI than cold outreach
- **Reddit/Quora = Tier-1 Targets:** AI engines scrape these heavily for citations
- **Brand Signals > Link Juice:** Google's entity graph values brand discussion velocity over traditional link metrics

**New Priorities:**
1. **AI Citation Tracking** — Monitor if brand appears in AI search results
2. **Unlinked Mention Conversion** — 40-60% success rate (vs. 2-5% for cold outreach)
3. **Tier-1 Platform Seeding** — Reddit, Quora, GitHub discussions
4. **Resource Page Updates** — Quick wins (existing pages that need a link added)

---

## Step-by-Step Instructions

### Step 1: Load Context
- Read `clients/<client_name>/brand_kit.json`
- Extract: `industry`, `content_pillars`, `website_url`, `competitors`

---

### Step 1B: Track AI Citations (NEW 2026)

**Tool:** Manual search + brand monitor

**Execute:**
```bash
# Test if brand appears in AI search results
# Manual process (no API available yet):
# 1. Go to ChatGPT, Perplexity, Gemini
# 2. Search: "best [product category] 2026"
# 3. Search: "top [service] for [use case]"
# 4. Record if client brand is mentioned
```

**Track in spreadsheet:**
```
| Platform   | Query Tested                          | Brand Mentioned? | Position | Screenshot |
|------------|---------------------------------------|------------------|----------|------------|
| ChatGPT    | "best CRM for small business"         | ✅ Yes           | #3       | link       |
| Perplexity | "top project management tools 2026"   | ❌ No            | N/A      | -          |
| Gemini     | "best email marketing software"       | ✅ Yes           | #7       | link       |
```

**Goal:** Client should appear in ≥20% of relevant AI search queries.

**If brand is NOT appearing:**
- Run `/aeo_optimize` on top 5 pages
- Add numbered rankings (#1, #2, #3)
- Increase citations from 2 → 5+
- Update content to <90 days old
- Add comparison tables

**Save to:**
`.tmp/{client}_ai_citations.json`

---

### Step 2A: Find Opportunities (Unlinked Mention Conversion — HIGHEST PRIORITY 2026)

**Why This Is Priority #1:**
- **40-60% Conversion Rate** (vs. 2-5% for cold outreach)
- Site already mentioned you = they know your brand
- Easy ask: "Can you link to us?" vs. "Can we write for you?"
- No content creation needed

**Tool:** `tools/brand_mention_tracker.py` (from `/brand_monitor` workflow)

**Execute:**
```bash
python tools/brand_mention_tracker.py \
  --brand "{client_name}" \
  --domain "{website_url}" \
  --timeframe pm \
  --output ".tmp/{client}_unlinked_mentions.json"
```

**What This Finds:**
- Blog posts mentioning client but not linking
- Reddit/Quora discussions mentioning client
- News articles mentioning client without link
- "Best X" listicles that include client

**Prioritize by Platform:**

**Tier 1 (60-70% Conversion):**
- News sites & media mentions
- Industry publications
- Case study mentions

**Tier 2 (40-50% Conversion):**
- Blog posts & "Best X" listicles
- Review sites
- Resource pages

**Tier 3 (Indirect Value):**
- Reddit discussions (can't edit, but track for PR intelligence)
- Quora answers (can suggest edits via comments)
- Social media posts

**Output:** `.tmp/{client}_unlinked_mentions.json`

**Sample Outreach Email (Tier 1 - News/Media):**
```
Subject: Quick Follow-Up on Your [Article Title] Article

Hi [Name],

Thank you for mentioning [Client Brand] in your recent article "[Article Title]"!

We'd love to make it easy for your readers to learn more. Would you be open to linking to our [specific relevant page] where it mentions us?

Here's the suggested link: [URL]

Happy to provide any additional information or quotes for future articles.

Best,
[Name]
[Client Website]
```

**Sample Outreach Email (Tier 2 - Listicle/Blog):**
```
Subject: Great List! Quick Request for [Client Brand]

Hi [Name],

I came across your article "[Article Title]" and noticed you mentioned [Client Brand] — thank you!

Would you be open to adding a link to our [feature page] so readers can learn more? It would really help our readers find the full details.

Suggested link: [URL]

Really appreciate it!

[Name]
[Client Website]
```

**Conversion Tracking:**
```json
{
  "unlinked_mentions_found": 23,
  "outreach_sent": 20,
  "links_acquired": 12,
  "conversion_rate": "60%",
  "avg_response_time": "3 days"
}
```

---

### Step 2B: Find Opportunities (Tier-1 Platform Seeding — Reddit, Quora, GitHub)

**Why This Matters in 2026:**
- AI engines (Perplexity, ChatGPT) heavily scrape Reddit and Quora
- Appearing in Reddit threads = indirect AI citation boost
- Quora answers rank in Google for long-tail queries

**Strategy:**

**Reddit:**
- **Don't spam.** Find existing threads where client is relevant.
- Search: `site:reddit.com "[industry problem]"`
- Look for: "What's the best [tool] for [use case]?"
- Add thoughtful comment mentioning client (with context)
- Example: "We switched to [Client Brand] for this exact reason. The [feature] solved our [problem]."

**Quora:**
- Search: `site:quora.com "best [product category]"`
- Answer questions genuinely
- Mention client naturally (not every answer)
- Link to specific feature pages, not homepage

**GitHub Discussions/Issues:**
- For developer tools only
- Find: Issues mentioning client's use case
- Contribute helpful code snippets or solutions
- Mention client if it solves the problem

**Output:** Manual tracking (Reddit/Quora don't have APIs for this)

---

### Step 2C: Find Opportunities (Resource Page Updates)

**Why This Works:**
- Pages already exist = no content creation needed
- Quick ask: "Can you add us to this list?"
- Often updated annually ("Best Tools 2026")

**Execute:**
```bash
python tools/serp_scraper.py \
  --mode resource_pages \
  --industry "{industry}" \
  --content-pillars "{pillars}" \
  --output ".tmp/{client}_resource_prospects.json"
```

**Search Operators Used:**
- `"best [industry] tools 2026"`
- `"[topic] resources" + "[year]"`
- `"tools for [use case]"`
- `"[topic] directory"`

**Outreach Email:**
```
Subject: Suggestion for Your "[Page Title]" Resource List

Hi [Name],

I came across your "[Page Title]" resource list and found it really helpful!

I noticed you included [Competitor 1] and [Competitor 2]. You might also want to consider adding [Client Brand] — we specialize in [unique differentiator].

Here's a quick overview: [1-2 sentence value prop]
Link: [URL]

Would you be open to adding us to the list? Happy to provide any additional details.

Best,
[Name]
```

**Output:** `.tmp/{client}_resource_prospects.json`

---

### Step 2D: Find Opportunities (Guest Posts — Lower Priority)

**Note:** Guest posts are now **lower priority** in 2026 due to:
- 2-5% conversion rate (vs. 40-60% for unlinked mentions)
- Requires content creation (time-consuming)
- Many sites now charge for guest posts
- ROI is worse than other tactics

**Only pursue guest posts if:**
- Client has specific thought leadership goals
- Targeting niche publications (not general marketing blogs)
- Guest post would drive direct traffic/leads (not just SEO)

**Execute:**
```bash
python tools/serp_scraper.py \
  --mode link_prospects \
  --industry "{industry}" \
  --mode guest_post \
  --output ".tmp/{client}_guest_post_prospects.json"
```

**Search Operators:**
- `"{industry}" + "write for us"`
- `"{industry}" + "guest post guidelines"`
- `"{industry}" + "submit an article"`
- `"{content_pillar}" + inurl:guest-post`

**Filters:**
- Remove big-brand sites (Forbes, HuffPost) — they don't accept cold outreach
- Remove sites that charge for guest posts

**Output:** `.tmp/{client}_guest_post_prospects.json`

---

### Step 3: Qualify Prospects
- For each prospect URL: check Domain Authority equivalent (via free Moz bar API or manual check)
- Filter: Keep only prospects that appear relevant (niche match > 70%)
- Score each prospect: Relevance (1-10) + Estimated DA (Low/Medium/High)
- Output: `.tmp/<client_name>_qualified_prospects.json`

### Step 4: Find Contact Details
- Run: `tools/serp_scraper.py --mode find_email --urls <prospect_urls>`
- Method 1: Check `/contact`, `/about` pages for email addresses
- Method 2: Try Hunter.io free API lookup (if key configured in .env)
- Method 3: Find social profiles (Twitter/X, LinkedIn) as fallback
- Output: `.tmp/<client_name>_contacts.json`

### Step 5: Draft Outreach Emails
For each qualified prospect with contact info, draft a personalized email using brand voice:

**Template for Guest Post:**
```
Subject: Guest Post Idea for [Their Site Name]: "[Specific Article Title]"

Hi [Name],

I've been following [Site Name] for a while — your recent piece on [specific topic] was excellent.

I'm reaching out because I think your readers would find value in a piece on:
"[Article Title That Serves Their Audience]"

I write for [Client Name] in the [industry] space. Here's a recent example of my work:
→ [Link to a strong existing client article]

Happy to tailor the topic to fit your editorial calendar.

Best,
[Name]
[Client Website]
```

- Save all drafted emails to: `clients/<client_name>/active_campaigns/outreach_<date>.md`

### Step 6: Present Results & Wait for Approval
Display prospects table in chat:

```
🔗 Link Building Prospects Found: <N>

Top 10 Qualified Prospects:
┌─────────────────────────┬──────────┬──────────────┬────────────────────┐
│ Site                    │ DA       │ Contact      │ Mode               │
├─────────────────────────┼──────────┼──────────────┼────────────────────┤
│ blog.example.com        │ Medium   │ Found ✓      │ Guest Post         │
│ resources.niche.com     │ High     │ Social only  │ Resource Link      │
└─────────────────────────┴──────────┴──────────────┴────────────────────┘
```

Ask: **"Here are your outreach targets with drafted emails. Shall I format these as a send-ready list, or do you want to edit any of the email drafts first?"**

## Edge Cases
- If Hunter.io rate limit is reached: use contact page scraping only and flag which prospects have no email.
- If no guest post opportunities found: automatically switch to `resource_links` mode and inform the user.
