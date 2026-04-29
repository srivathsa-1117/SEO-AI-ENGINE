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

## Step-by-Step Instructions

### Step 1: Load Context
- Read `clients/<client_name>/brand_kit.json`
- Extract: `industry`, `content_pillars`, `website_url`, `competitors`

### Step 2A: Find Opportunities (Guest Posts Mode)
- Run: `tools/serp_scraper.py --mode link_prospects --industry "<industry>" --mode guest_post`
- Uses advanced Google Search operators automatically:
  - `"<industry>" + "write for us"`
  - `"<industry>" + "guest post guidelines"`
  - `"<industry>" + "submit an article"`
  - `"<content_pillar>" + inurl:guest-post`
- Filters results: removes big-brand sites (Forbes, HuffPost) that don't accept outreach
- Output: `.tmp/<client_name>_guest_post_prospects.json`

### Step 2B: Find Opportunities (Unlinked Brand Mentions)
- Run: `tools/serp_scraper.py --mode unlinked_mentions --brand "<client_name>" --url "<website_url>"`
- Searches for: mentions of the brand name online that don't link back to the site
- Output: `.tmp/<client_name>_unlinked_mentions.json`

### Step 2C: Find Opportunities (Resource Links)
- Run: `tools/serp_scraper.py --mode resource_pages --industry "<industry>" --content-pillars <pillars>`
- Finds: "Best Resources for [topic]" and "Tools for [topic]" pages that could list the client
- Output: `.tmp/<client_name>_resource_prospects.json`

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
