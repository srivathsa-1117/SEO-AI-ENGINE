---
description: /content_refresh - Automated content freshness tracking and update workflow
---

# Workflow: Content Refresh & Freshness Automation (2026 Standards)

## Trigger
```
/content_refresh <client_name> [--age-threshold 90] [--auto-update]
```

**Examples:**
- `/content_refresh acme_corp` — Scan all content, flag articles >90 days old
- `/content_refresh acme_corp --age-threshold 60` — Flag articles >60 days old (stricter)
- `/content_refresh acme_corp --auto-update` — Auto-update flagged articles (use with caution)

## Objective
Track content age and automate freshness updates. AI search engines (especially Perplexity) heavily favor fresh content: **46.7% of Perplexity citations come from content <90 days old**. This workflow identifies stale content and provides update templates to maintain high AI citability.

## Tools Used in This Workflow
- **`tools/content_age_scanner.py`** - Scans sitemap or crawl data to identify content age
- **`tools/freshness_updater.py`** - Generates update templates for stale content
- **`tools/aeo_grader.py`** - Re-scores content after updates (check if freshness improved AEO score)

## Success Metrics
- **Content Freshness:** ≥70% of content updated within last 90 days
- **Update Frequency:** High-traffic pages updated every 30-60 days
- **AI Citation Rate:** Articles <90 days old get 2-3x more AI citations
- **Organic CTR Boost:** Fresh dates in SERP snippets increase CTR by 15-25%
- **Perplexity Citation Rate:** Target 46.7% citation rate by maintaining <90 day freshness

---

## CRITICAL AWARENESS: CONTENT FRESHNESS IN 2026

**Why This Matters:**
- **Perplexity AI:** 46.7% of citations come from content <90 days old
- **ChatGPT:** Prefers content with "Updated: [Month] 2026" indicators
- **Google:** Freshness is a ranking factor for query-deserves-freshness (QDF) topics
- **SERP CTR:** Articles showing "Updated 3 days ago" get 15-25% higher CTR

**Stale Content Impact:**
- Content >180 days old: 70% drop in AI citations
- Content >365 days old: 85% drop in AI citations
- No update indicator: Perceived as outdated, even if accurate

---

## The 5-Step Content Refresh Process

### Step 1: Scan Content for Age

**Tool:** `tools/content_age_scanner.py`

**Execute:**
```bash
python tools/content_age_scanner.py \
  --client "{client_name}" \
  --source sitemap \
  --age-threshold 90 \
  --output ".tmp/{client}_content_age.json"
```

**What This Checks:**
- `datePublished` from Article schema (if present)
- `dateModified` from Article schema (if present)
- `lastmod` from sitemap.xml
- Git commit history (if available)
- Page HTML meta tags (`article:published_time`, `article:modified_time`)

**Output Format:**
```json
{
  "scan_date": "2026-03-20",
  "total_articles": 87,
  "age_breakdown": {
    "0-30_days": 12,
    "31-60_days": 18,
    "61-90_days": 25,
    "91-180_days": 20,
    "180+_days": 12
  },
  "stale_content": [
    {
      "url": "https://acmecorp.com/blog/remote-teams",
      "title": "How to Manage Remote Teams",
      "age_days": 157,
      "last_modified": "2025-10-15",
      "traffic_last_30d": 1250,
      "priority": "HIGH"
    },
    {
      "url": "https://acmecorp.com/blog/slack-tips",
      "title": "10 Slack Tips for Productivity",
      "age_days": 245,
      "last_modified": "2025-07-18",
      "traffic_last_30d": 450,
      "priority": "MEDIUM"
    }
  ],
  "fresh_content": [
    {
      "url": "https://acmecorp.com/blog/ai-tools-2026",
      "title": "Best AI Tools for 2026",
      "age_days": 12,
      "last_modified": "2026-03-08",
      "traffic_last_30d": 3200
    }
  ]
}
```

**Priority Calculation:**
```python
# High priority = High traffic + Stale
if age_days > 90 and traffic_last_30d > 500:
    priority = "HIGH"
elif age_days > 180:
    priority = "HIGH"  # Very stale, regardless of traffic
elif age_days > 90 and traffic_last_30d > 100:
    priority = "MEDIUM"
else:
    priority = "LOW"
```

**Flag Issues:**
- Content >90 days old with >500 visits/month → "HIGH: Update this article ASAP for AI citability"
- Content >180 days old → "HIGH: Severely stale, likely losing rankings"
- Content >365 days old → "CRITICAL: Update immediately or consider deleting"

**Save to:**
`.tmp/{client}_content_age.json`

---

### Step 2: Prioritize Updates by Traffic & Age

**Sort stale content by priority:**
1. **Tier 1 (Update This Week):**
   - Age >90 days AND traffic >500/month
   - Age >180 days (regardless of traffic)
   - Commercial pages (pricing, features, comparison)

2. **Tier 2 (Update This Month):**
   - Age >90 days AND traffic 100-500/month
   - Age >120 days AND traffic <100/month
   - Blog posts ranking positions 5-15 (opportunity to move up)

3. **Tier 3 (Update This Quarter):**
   - Age >90 days AND traffic <100/month
   - Informational content with low search volume

**Execute:**
```bash
python tools/content_age_scanner.py \
  --client "{client_name}" \
  --prioritize \
  --output ".tmp/{client}_refresh_priority.json"
```

**Output Example:**
```json
{
  "tier_1_urgent": [
    {
      "url": "https://acmecorp.com/blog/remote-teams",
      "age_days": 157,
      "traffic": 1250,
      "action": "UPDATE_NOW"
    }
  ],
  "tier_2_this_month": [...],
  "tier_3_this_quarter": [...]
}
```

---

### Step 3: Generate Update Templates

**Tool:** `tools/freshness_updater.py`

**Execute:**
```bash
python tools/freshness_updater.py \
  --url "https://acmecorp.com/blog/remote-teams" \
  --mode quick_refresh \
  --output ".tmp/{client}_update_template.md"
```

**Update Modes:**

#### **Mode 1: Quick Refresh (30 minutes)**
For articles that are still accurate but need freshness signals:

**What to Update:**
- Add "**Updated: March 2026**" at the top (above H1)
- Update `dateModified` in Article schema to today
- Add 1-2 new statistics from 2026 sources
- Update any "in 2025" references to "in 2026"
- Add 1-2 new screenshots if applicable
- Refresh image alt text with current year
- Check all external links still work (replace dead links)

**Template Output:**
```markdown
## Quick Refresh Checklist for: [Article Title]

**Original Publish Date:** 2025-10-15
**Current Age:** 157 days
**Target:** <90 days

### Required Updates:

1. **Add Freshness Indicator (Top of Article):**
   ```markdown
   **Updated: March 20, 2026** — _Reviewed and updated with the latest 2026 data and best practices._
   ```

2. **Update Schema `dateModified`:**
   ```json
   "dateModified": "2026-03-20"
   ```

3. **Add New 2026 Statistics:**
   - Find 1-2 new stats from last 6 months
   - Replace oldest stat with new one
   - Example: "In 2026, 73% of companies use hybrid work models (up from 62% in 2025)"

4. **Update Year References:**
   - Find/Replace: "in 2025" → "in 2026"
   - Find/Replace: "for 2025" → "for 2026"

5. **Check External Links:**
   - Run link checker
   - Replace any dead links (404s)
   - Update links to latest versions of referenced tools

6. **Refresh Images (Optional but Recommended):**
   - Add 1 new screenshot showing current tool UI
   - Update image filenames: `remote-team-tools-2026.png`
```

---

#### **Mode 2: Deep Refresh (2-3 hours)**
For articles that need significant updates due to industry changes:

**What to Update:**
- All Quick Refresh items PLUS:
- Add new H2 section: "What's New in 2026?"
- Add comparison table: "2025 vs 2026 Best Practices"
- Update entire "Best X" rankings (if applicable)
- Add new case study or example from last 90 days
- Refresh FAQ section with current questions
- Add new internal links to recently published articles

**Template Output:**
```markdown
## Deep Refresh Checklist for: [Article Title]

**Original Publish Date:** 2025-10-15
**Current Age:** 157 days
**Industry Changes:** Significant (AI tools evolved rapidly)

### Required Updates:

1. **All Quick Refresh Items** (see Mode 1)

2. **Add New Section: "What's New in 2026?"**
   ```markdown
   ## What's New in Remote Team Management (2026 Update)

   Since we first published this guide in October 2025, several major developments have changed how teams collaborate:

   1. **AI Meeting Assistants:** Tools like [X] now auto-generate action items
   2. **Async Video Messaging:** Platforms like [Y] gained 200% adoption
   3. **Compliance Changes:** New EU regulations for remote work monitoring
   ```

3. **Add Comparison Table:**
   ```markdown
   | Best Practice | 2025 | 2026 |
   |---------------|------|------|
   | Daily standups | Zoom calls | Async Loom videos |
   | Project management | Trello/Asana | AI-powered [Tool] |
   | Time tracking | Manual logs | Automated activity tracking |
   ```

4. **Update Rankings (if "Best X" article):**
   - Re-test all ranked products
   - Add new entries if superior products launched
   - Remove discontinued products
   - Update pricing (often changes)

5. **Add Fresh Case Study:**
   - Replace oldest example with new one from 2026
   - Include specific metrics and timeframe
   - Add screenshot or data visualization

6. **Refresh FAQ Section:**
   - Check Google "People Also Ask" for current questions
   - Add 2-3 new FAQs addressing 2026 concerns
   - Remove outdated FAQs

7. **Update Internal Links:**
   - Link to 3-5 articles published in last 90 days
   - Remove links to deleted/redirected pages
   ```

---

#### **Mode 3: Complete Rewrite (6-8 hours)**
For articles where the topic has fundamentally changed or original content is now incorrect:

**When to Use:**
- Topic has evolved >50% since original publish
- Original advice is now outdated or incorrect
- Competitor content is significantly better
- Article is >365 days old with declining traffic

**Action:**
- Use `/content_brief` workflow to create new brief
- Use `/content_draft` workflow to rewrite from scratch
- 301 redirect old URL to new version
- Preserve any backlinks by keeping URL structure

---

### Step 4: Execute Updates & Validate

**After updating content:**

1. **Validate Freshness Signals:**
   ```bash
   python tools/schema_checker.py --url "{updated_url}"
   ```
   - Verify `dateModified` updated in schema
   - Verify "Updated: [Date]" visible on page

2. **Re-run AEO Grader:**
   ```bash
   python tools/aeo_grader.py \
     --url "{updated_url}" \
     --mode perplexity \
     --output ".tmp/{client}_aeo_after.json"
   ```
   - Compare before/after scores
   - Fresh content should score 10-15 points higher

3. **Request Re-indexing:**
   ```bash
   # Submit to Google Search Console
   # Or use GSC MCP: "Request indexing for {url}"
   ```

4. **Track Results:**
   ```json
   {
     "url": "https://acmecorp.com/blog/remote-teams",
     "before_update": {
       "age_days": 157,
       "aeo_score": 68,
       "traffic_30d": 1250
     },
     "after_update": {
       "age_days": 0,
       "aeo_score": 82,
       "traffic_30d": "tracking..."
     },
     "update_type": "deep_refresh",
     "time_spent": "2.5 hours"
   }
   ```

---

### Step 5: Automate Freshness Monitoring

**Set up recurring scans:**

```bash
# Run monthly content age scan
# Add to cron job or GitHub Actions workflow

python tools/content_age_scanner.py \
  --client "{client_name}" \
  --age-threshold 90 \
  --prioritize \
  --notify \
  --output ".tmp/{client}_refresh_priority.json"
```

**Notification Triggers:**
- ≥5 articles crossed 90-day threshold
- ≥1 high-traffic article (>1000 visits/month) is >90 days old
- ≥10 articles are >180 days old

**Monthly Report Section:**
```markdown
## Content Freshness Report (March 2026)

**Overall Freshness Score:** 68/100 (Target: ≥70)

**Age Breakdown:**
-  0-90 days: 45 articles (52%)
-  91-180 days: 28 articles (32%)
-  180+ days: 14 articles (16%)

**Action Required:**
- Update 8 high-priority articles this month
- Schedule deep refresh for "Remote Teams" guide (157 days old, 1250 visits/month)

**AI Citation Impact:**
- Articles <90 days: 22% Perplexity citation rate
- Articles >90 days: 8% Perplexity citation rate
- **Opportunity:** Update 14 stale articles → estimated +42 AI citations/month
```

---

## Edge Cases & Troubleshooting

### 1. **Evergreen Content That Doesn't Need Updates**

**Scenario:** "What is SEO?" article from 2023 is still 100% accurate

**Solution:**
- Still add "**Reviewed: March 2026**" indicator (shows diligence)
- Update `dateModified` in schema
- Add 1-2 new examples from 2026
- Check all links still work
- Takes 15 minutes, maintains freshness signals

---

### 2. **No Traffic Data Available**

**Scenario:** Client doesn't have GA4 or GSC connected

**Solution:**
- Prioritize by topic type instead:
  - Commercial pages (pricing, features): Update every 60 days
  - "Best X" listicles: Update every 90 days
  - How-to guides: Update every 120 days
  - Evergreen definitions: Update every 180 days

---

### 3. **Too Many Stale Articles (>100 flagged)**

**Scenario:** Large blog with years of content, all stale

**Solution:**
- Focus on 80/20 rule: Update top 20% by traffic first
- Use Quick Refresh mode (30 min each) instead of Deep Refresh
- Batch updates: 10 articles per week for 10 weeks
- Consider deleting bottom 20% (no traffic, no rankings) and 301 redirecting

---

### 4. **Content Updated But Still Not Cited by AI**

**Scenario:** Refreshed article, added "Updated 2026", but no AI citations

**Solution:**
- Check AEO score with `tools/aeo_grader.py`
- Ensure numbered list format (#1, #2, #3)
- Add comparison table or data table
- Increase depth (add 500+ words of new content)
- Add answer blocks after H2s (50-75 words)
- Submit to Perplexity Pages or ChatGPT index (if available)

---

## File Outputs

This workflow generates:

1. `.tmp/{client}_content_age.json` — Full age analysis
2. `.tmp/{client}_refresh_priority.json` — Prioritized update list
3. `.tmp/{client}_update_template.md` — Update checklist for each article
4. `.tmp/{client}_aeo_before.json` — AEO score before update
5. `.tmp/{client}_aeo_after.json` — AEO score after update

---

## Validation Checklist

Before marking an article as "refreshed":

- [ ] "Updated: [Month] 2026" visible at top of article
- [ ] `dateModified` in Article schema = today's date
- [ ] At least 1 new statistic from 2026 added
- [ ] All external links checked (no 404s)
- [ ] Year references updated (2025 → 2026)
- [ ] Re-submitted to Google Search Console for indexing
- [ ] AEO score re-run (should be +10-15 points higher)
- [ ] Article age reset to 0 days in tracking spreadsheet

---

## Expected Impact

**Before Content Refresh Workflow:**
- 40% of content <90 days old
- 8% AI citation rate
- Manual tracking in spreadsheets
- Updates happen reactively (when traffic drops)

**After Content Refresh Workflow:**
- 70% of content <90 days old
- 22% AI citation rate (2.75x increase)
- Automated tracking with alerts
- Updates happen proactively (before traffic drops)

**ROI:**
- 30 minutes per Quick Refresh
- +15% organic CTR boost from fresh dates
- +10-15 point AEO score increase
- 2-3x more AI citations (Perplexity, ChatGPT)

---

## Related Workflows

- `/content_draft` — Create new content with proper freshness indicators
- `/aeo_optimize` — Optimize content for AI search citability
- `/monthly_report` — Include content freshness metrics in client reports

---

## Notes

- **Freshness ≠ Quality:** Don't just change dates. Add real value.
- **Perplexity Prefers <90 Days:** But ChatGPT also looks at depth. Prioritize both.
- **Schema Matters:** Google reads `dateModified`, not just page text.
- **Quick Wins:** 30-minute quick refreshes work for 70% of content.
- **Traffic Tracking:** Monitor 30-day traffic before/after updates to measure impact.
