---
description: /monthly_report - Generate a complete monthly SEO performance report for a client
---

# Workflow: Monthly Report Generation

## Trigger
```
/monthly_report <client_name> [--month YYYY-MM] [--format markdown|pdf|docx]
```
**Example:** `/monthly_report acme_corp --month 2025-02 --format docx`

## Objective
Pull all available data sources (GSC, GA4, crawl history, content publishing, link building) and generate a comprehensive, beautifully formatted monthly SEO report. Deliver to the client or save locally.

---

## Required Inputs

1. **`<client_name>`** — Client folder name (loads brand_kit.json and historical data)
2. **`--month`** — Target month in YYYY-MM format (defaults to last full calendar month)
3. **`--format`** — Output format: `markdown`, `pdf`, or `docx` (defaults to `docx`)

---

## Step-by-Step Instructions

### Step 1: Load Client Context

**Tool:** Read tool (file system access)

**Execute:**
```bash
# Read brand kit
Read: clients/{client_name}/brand_kit.json
```

**Parse required fields:**
```json
{
  "client_name": "Acme Corp",
  "website_url": "https://acmecorp.com",
  "primary_keywords": ["project management", "team collaboration"],
  "gsc_connected": true,
  "ga4_connected": true,
  "reporting": {
    "custom_report_template": "templates/acme_monthly_template.md",
    "report_delivery_method": "google_drive"
  }
}
```

**Validate:**
```bash
# Check file exists
if [ ! -f "clients/{client_name}/brand_kit.json" ]; then
  echo "[ERROR] Client not found: {client_name}"
  echo "Run /add_client {client_name} first"
  exit 1
fi
```

**Extract key info:**
- `client_name` (for display)
- `website_url` (for crawl data lookups)
- `primary_keywords` (for ranking tracking)
- `gsc_connected` (determines if we can pull GSC data)
- `ga4_connected` (determines if we can pull GA4 data)
- `reporting.custom_report_template` (use if exists, else default template)

**If brand_kit.json is missing fields:**
- Use defaults: `gsc_connected: false`, `ga4_connected: false`
- Flag in report: "[WARNING] GSC/GA4 not connected — manual data entry required"

---

### Step 2: Determine Target Month

**Logic:**
```python
# If --month not provided, use last complete month
from datetime import datetime, timedelta

if not args.month:
    today = datetime.now()
    # Get first day of current month, then subtract 1 day to get last month
    first_of_this_month = today.replace(day=1)
    last_month = first_of_this_month - timedelta(days=1)
    target_month = last_month.strftime("%Y-%m")
else:
    target_month = args.month

# Validate format (YYYY-MM)
if not re.match(r"^\d{4}-\d{2}$", target_month):
    echo "[ERROR] Invalid month format. Use YYYY-MM (e.g., 2025-02)"
    exit 1
```

**Calculate date ranges:**
```python
# Example: 2025-02
start_date = f"{target_month}-01"  # 2025-02-01
end_date = f"{target_month}-28"    # 2025-02-28 (adjust for month length)

# For comparison (previous month)
prev_month_start = calculate_previous_month(start_date)
prev_month_end = last_day_of_previous_month(start_date)
```

---

### Step 3: Pull Google Search Console (GSC) Data

**Check if GSC is connected:**
```bash
# From brand_kit.json
if brand_kit["gsc_connected"] == false:
  # Skip GSC pull, use manual entry later
  gsc_data = null
fi
```

---

### TOOL SELECTION HIERARCHY (2026 - MCP First)

**1st Choice: GSC MCP Server** (if configured in Claude Desktop)
- **Real-time API access** to Google Search Console
- **No CSV exports needed** (fully automated)
- **Fresh data** always (no stale cached files)
- **Date range filtering** built-in
- **OAuth 2.0 authenticated** (secure)

**Execute:**
```
Ask Claude: "Get top keywords from GSC for {website_url} from {start_date} to {end_date}"
```

**Available MCP Commands:**
1. **Get top keywords:**
   - "Get top 50 keywords from GSC for metalbarns.in for last 30 days"
   - Returns: query, clicks, impressions, CTR, position

2. **Get top pages:**
   - "Get top 20 pages from GSC for acmecorp.com for last month"
   - Returns: URL, clicks, impressions, CTR

3. **Query search analytics:**
   - "Query GSC analytics for {site_url} from 2026-02-01 to 2026-02-28"
   - Returns: total clicks, impressions, CTR, avg position

4. **URL inspection:**
   - "Check index status for {url} in GSC"
   - Returns: indexed status, last crawl date, coverage issues

**Save Results:**
When MCP returns data, save to `.tmp/{client}_gsc_{month}.json`:
```json
{
  "period": "{start_date} to {end_date}",
  "total_clicks": 12450,
  "total_impressions": 345000,
  "avg_ctr": 3.6,
  "avg_position": 12.4,
  "top_queries": [...],
  "top_pages": [...],
  "source": "mcp_gsc"
}
```

---

**2nd Choice: Manual CSV Export** (fallback if MCP unavailable)

**If MCP not configured:**
```
1. Inform user: "[WARNING] GSC MCP not configured. Please export CSV from Search Console:"
2. Instructions:
   - Go to Google Search Console → Performance
   - Date range: {start_date} to {end_date}
   - Export as CSV
   - Save to: `.tmp/{client_name}_gsc_{month}.csv`
3. Read the CSV and parse manually
```

---

### Data Validation (Same for Both Methods)

**Validate GSC output:**
```bash
# Check data is not empty
if gsc_data["total_clicks"] == 0 and gsc_data["total_impressions"] == 0:
  echo "[WARNING] GSC returned zero data — check date range or site verification"
  # Use placeholder values
fi

# Check for minimum data quality
if len(gsc_data["top_queries"]) < 3:
  echo "[WARNING] Insufficient query data (< 3 queries)"
  # Flag in report
fi
```

**Save to cache:**
```bash
# Write to .tmp/ for reuse
Write: .tmp/{client_name}_gsc_{month}.json
Content: gsc_data (JSON)
```

**If GSC pull fails entirely:**
1. Check authentication (GSC credentials valid?)
2. Check site ownership (client's site verified in GSC?)
3. Fallback: Generate report with "[ERROR] GSC Data Unavailable" section
4. Provide manual entry template:
   - Total clicks: _____
   - Total impressions: _____
   - Top 5 queries: _____

---

### Step 4: Pull Google Analytics 4 (GA4) Data

**Check if GA4 is connected:**
```bash
# From brand_kit.json
if brand_kit["ga4_connected"] == false:
  # Skip GA4 pull, use manual entry later
  ga4_data = null
fi
```

**Tool Option 1 (Preferred): MCP `mcp__ga4` (if configured)**

**Execute:**
```bash
# Check if MCP GA4 server is available
# User will ask: "Get GA4 organic traffic for {website_url} from {start_date} to {end_date}"
```

**MCP will return:**
```json
{
  "organic_users": 8450,
  "organic_sessions": 12300,
  "organic_pageviews": 34500,
  "avg_session_duration": 145,
  "bounce_rate": 52.3,
  "top_landing_pages": [
    {"page": "/features", "sessions": 2100},
    {"page": "/pricing", "sessions": 1850},
    {"page": "/blog/remote-teams", "sessions": 1200}
  ],
  "goal_completions": 245
}
```

**Tool Option 2 (Fallback): Manual Export**

If MCP not available:
```
1. Inform user: "[WARNING] GA4 MCP not configured. Please export data from Google Analytics:"
2. Instructions:
   - Go to GA4 → Reports → Acquisition → Traffic Acquisition
   - Filter by: Source = "google" AND Medium = "organic"
   - Date range: {start_date} to {end_date}
   - Export as CSV
   - Save to: `.tmp/{client_name}_ga4_{month}.csv`
3. Read the CSV and parse manually
```

**Validate GA4 output:**
```bash
# Check data is not empty
if ga4_data["organic_users"] == 0:
  echo "[WARNING] GA4 returned zero organic users — check filters or tracking code"
  # Use placeholder values
fi

# Check for minimum data quality
if ga4_data["avg_session_duration"] < 10:
  echo "[WARNING] Suspicious session duration (< 10 seconds) — possible tracking issue"
  # Flag in report
fi
```

**Save to cache:**
```bash
Write: .tmp/{client_name}_ga4_{month}.json
Content: ga4_data (JSON)
```

**If GA4 pull fails entirely:**
1. Check authentication (GA4 credentials valid?)
2. Check property access (client's GA4 property accessible?)
3. Fallback: Generate report with "[ERROR] GA4 Data Unavailable" section
4. Provide manual entry template:
   - Organic users: _____
   - Organic sessions: _____
   - Top landing pages: _____

---

### Step 5: Pull Technical Health Snapshot

**Check for previous month's crawl data:**
```bash
# Look for most recent crawl in audit_history/
Glob: clients/{client_name}/audit_history/{year}-{month}*_crawl.json

# If found, compare with current month
if previous_crawl exists:
  Read: clients/{client_name}/audit_history/{prev_month}_crawl.json
fi
```

**Tool:** `seo_crawler.py` (light crawl mode)

**Execute:**
```bash
python tools/seo_crawler.py \
  --url "{website_url}" \
  --max-pages 25 \
  --timeout 120 \
  --output ".tmp/{client_name}_crawl_{month}.json"
```

**What this does:**
- Quick crawl of up to 25 key pages
- Checks for new 404s, redirect chains, broken links
- Validates schema markup still present
- Checks page speed (LCP, INP, CLS) on homepage

**Validate output:**
```bash
# Check file exists
if [ ! -f ".tmp/{client_name}_crawl_{month}.json" ]; then
  echo "[WARNING] Crawl failed, skipping technical health section"
  technical_health = null
fi
```

**Compare with previous month (if available):**
```python
current_crawl = read_json(f".tmp/{client_name}_crawl_{month}.json")
previous_crawl = read_json(f"clients/{client_name}/audit_history/{prev_month}_crawl.json")

technical_changes = {
  "new_404s": current_crawl["404_count"] - previous_crawl["404_count"],
  "new_redirects": current_crawl["redirect_count"] - previous_crawl["redirect_count"],
  "index_count_change": current_crawl["indexable_pages"] - previous_crawl["indexable_pages"],
  "page_speed_change": current_crawl["avg_lcp"] - previous_crawl["avg_lcp"]
}
```

**If no previous crawl exists:**
- This is the baseline month
- Flag: "[WARNING] First technical snapshot — no comparison data available"
- Save current crawl to `audit_history/{month}_crawl.json` for next month

---

### Step 6: Content & Link Building Summary

**Content Published This Month:**

**Tool:** File system scan

**Execute:**
```bash
# Look for published content in content_calendar or blog posts
Glob: clients/{client_name}/content_calendar/{month}*.md
Glob: clients/{client_name}/published/{month}*.md
```

**Parse each file:**
```markdown
# Extract from frontmatter:
- title: "How to Manage Remote Teams"
- published_date: 2025-02-15
- target_keyword: "remote team management"
- url: https://acmecorp.com/blog/remote-teams
```

**Compile list:**
```python
published_content = [
  {"title": "...", "date": "...", "keyword": "...", "url": "..."},
  {"title": "...", "date": "...", "keyword": "...", "url": "..."}
]

total_articles_published = len(published_content)
```

**If no content found:**
- Set `total_articles_published = 0`
- Flag: "[WARNING] No content published this month"

---

**Link Building This Month:**

**Tool:** File system scan + backlink tracker

**Execute:**
```bash
# Look for link building tracking file
Read: clients/{client_name}/link_building/{month}_links.json
```

**Expected structure:**
```json
{
  "links_built": [
    {"source": "example.com", "target_url": "https://acmecorp.com/features", "dr": 45, "date": "2025-02-10"},
    {"source": "industry-blog.com", "target_url": "https://acmecorp.com/blog/remote-teams", "dr": 38, "date": "2025-02-22"}
  ],
  "outreach_sent": 25,
  "responses_received": 8,
  "links_acquired": 2
}
```

**If file not found:**
- Set `links_built = 0`
- Flag: "[WARNING] No link building tracked this month"

**Validate:**
```bash
# Check for minimum data
if len(link_data["links_built"]) == 0 and link_data["outreach_sent"] == 0:
  echo "[WARNING] No link building activity recorded"
  # Use placeholder
fi
```

---

### Step 7: AEO/GEO Status (AI Search Visibility)

**Check for featured snippets and AI overview appearances:**

**Tool:** SERP scraper + manual check

**Execute:**
```bash
# For each primary keyword, check if client appears in:
# - Featured snippet
# - People Also Ask
# - AI Overview (ChatGPT, Perplexity, Claude)

python tools/serp_scraper.py \
  --mode serp_features \
  --keywords "{primary_keywords}" \
  --output ".tmp/{client_name}_serp_features_{month}.json"
```

**Expected output:**
```json
{
  "featured_snippets": [
    {"keyword": "project management software", "appears": true, "url": "https://acmecorp.com/features"}
  ],
  "paa_appearances": 3,
  "ai_overview_mentions": [
    {"keyword": "best project management tools", "mentioned": true, "position": 2}
  ]
}
```

**If tool fails:**
- Manual check: Search primary keywords in Google
- Note any featured snippets or AI overviews manually
- Document: "[WARNING] Automated SERP scraper unavailable, used manual check"

---

**Assess Fresh Brand Mentions (The AI Citability Pulse):**

**Tool:** `brand_mention_tracker.py`

**Execute:**
```bash
python tools/brand_mention_tracker.py \
  --brand "{client_name}" \
  --domain "{website_url}" \
  --timeframe "pm" \
  --output ".tmp/{client_name}_brand_mentions_{month}.json"
```

**What this does:**
- Tracks new mentions on platforms AI engines heavily scrape (Reddit, Quora, News).
- Summarizes Tier-1 Authority mentions.
- High velocity of high-authority mentions correlates directly with ranking improvements in Gemini/ChatGPT.

**Parse results:**
- Total mentions.
- Tier-1 Mentions count.

---

### Step 8: Calculate Month-over-Month (MoM) Changes

**Compare current month vs. previous month:**

**Metrics to compare:**
```python
mom_changes = {
  "clicks": {
    "current": gsc_data["total_clicks"],
    "previous": prev_gsc_data["total_clicks"],
    "change_pct": ((current - previous) / previous) * 100
  },
  "impressions": {...},
  "organic_users": {...},
  "avg_position": {...}
}
```

**Format for display:**
```
Total Clicks: 12,450 (↑ 15.3% from last month)
Total Impressions: 345,000 (↑ 8.2% from last month)
Organic Users: 8,450 (↑ 12.7% from last month)
Avg Position: 12.4 (↑ 1.2 positions from last month)
```

**If no previous month data exists:**
- Skip MoM calculations
- Display absolute values only
- Note: "[WARNING] First month report — baseline established"

---

### Step 9: Compile Report Structure

**Agent Persona:** `seo-director.md`
**Tool:** `tools/chat_to_report.py`

**Process:**
1. The SEO Director agent reads all the JSON files in `.tmp/` and compiles a beautiful Markdown report in the chat.
2. The user approves the report.
3. The agent saves the approved text to `.tmp/{client_name}_{month}_report.md` and generates the DOCX:

```bash
python tools/chat_to_report.py \
  --input ".tmp/{client_name}_{month}_report.md" \
  --output "clients/{client_name}/reports/{month}_report.docx"
```

**Parameters:**
- `--client`: Client name (for loading brand_kit)
- `--type`: Report type (`monthly`, `audit`, `content_brief`)
- `--month`: Target month (YYYY-MM)
- `--format`: Output format (`markdown`, `pdf`, `docx`)
- `--output`: Full path to save report

**What this tool does:**
1. Reads all cached data files:
   - `.tmp/{client_name}_gsc_{month}.json`
   - `.tmp/{client_name}_ga4_{month}.json`
   - `.tmp/{client_name}_crawl_{month}.json`
   - `clients/{client_name}/content_calendar/{month}*.md`
   - `clients/{client_name}/link_building/{month}_links.json`

2. Loads template:
   - Check if `brand_kit["reporting"]["custom_report_template"]` exists
   - If yes: Use custom template
   - If no: Use default `templates/monthly_report_template.md`

3. Fills template with data:
   - Executive Summary (auto-generated highlights)
   - Traffic Overview (GSC + GA4 charts)
   - Rankings & Visibility (top queries, position changes)
   - Technical Health (crawl comparison)
   - Content Published (list of articles)
   - Links Built (backlinks acquired)
   - AEO/GEO Status (featured snippets, AI mentions)
   - Next Month Priorities (auto-generated recommendations)

4. Renders output:
   - If `markdown`: Save as .md file
   - If `docx`: Generate .docx with Example Brand branding
   - If `pdf`: Generate PDF (requires docx → pdf conversion)

**Validate output:**
```bash
# Check file was created
if [ ! -f "clients/{client_name}/reports/{month}_report.{format}" ]; then
  echo "[ERROR] Report generation failed"
  # Check stderr for errors
  exit 1
fi

# Check file is not empty
if [ ! -s "clients/{client_name}/reports/{month}_report.{format}" ]; then
  echo "[ERROR] Report file is empty"
  exit 1
fi

# Check minimum file size (reports should be > 50KB)
file_size=$(stat -f%z "clients/{client_name}/reports/{month}_report.{format}")
if [ $file_size -lt 50000 ]; then
  echo "[WARNING] Report seems too small (< 50KB) — may be incomplete"
fi
```

**Report Sections (Detailed):**

**1. Executive Summary**
- 3-5 bullet highlights (biggest wins, concerns, trends)
- Auto-generated based on data:
  - If clicks up > 10%: "[OK] Organic traffic increased 15.3% month-over-month"
  - If new featured snippet: "[OK] Gained featured snippet for 'project management software'"
  - If avg position improved: "[OK] Average ranking position improved by 1.2 spots"
  - If technical issues found: "[WARNING] 5 new 404 errors detected, requiring immediate fix"

**2. Traffic Overview (GSC + GA4)**
- Total clicks, impressions, CTR, avg position
- Month-over-month change (percentage + absolute)
- Top 10 queries by clicks (with position trend)
- Top 10 landing pages by sessions

**3. Rankings & Visibility**
- Keywords that entered top 10 this month (new wins)
- Keywords that dropped out of top 10 (losses)
- Biggest position gainers (e.g., moved from #15 → #8)
- Biggest position losers (e.g., moved from #5 → #12)

**4. Technical Health**
- Crawl health summary (pages crawled, 404s, redirects)
- Index count change (gained or lost indexed pages)
- Page speed change (LCP, INP, CLS trends)
- New technical issues discovered (broken links, missing canonical, etc.)

**5. Content Published**
- List of articles published this month
- For each: title, publish date, target keyword, URL
- Performance snapshot (if published > 2 weeks ago):
  - Clicks from GSC
  - Impressions from GSC
  - Avg position

**6. Links Built**
- Total backlinks acquired this month
- Breakdown by DR (Domain Rating):
  - DR 50+: X links
  - DR 30-49: Y links
  - DR < 30: Z links
- Top 3 best links (highest DR or most relevant)
- Outreach summary: sent, responded, converted

**7. AEO/GEO Status (AI Search Visibility)**
- Featured snippets owned (current month)
- Featured snippets lost (if any)
- People Also Ask appearances
- AI Overview mentions (ChatGPT, Perplexity, Claude)
- Schema markup status (valid, warnings, errors)

**8. Next Month Priorities**
- 3-5 recommended actions based on data:
  - If technical issues: "Fix 5 new 404 errors"
  - If content gap: "Publish 2 articles targeting [keywords]"
  - If position drop: "Optimize [page] to recover lost rankings"
  - If no featured snippets: "Target featured snippet for [keyword]"
  - If link building low: "Increase outreach to 50 prospects"

---

### Step 10: Format & Deliver Report

**Check format requested:**

**If `--format docx` (default):**
```bash
# Report is already generated as .docx
# Provide download link
echo " Download: [clients/{client_name}/reports/{month}_report.docx](file:///full/path/to/report.docx)"
```

**If `--format markdown`:**
```bash
# Report is generated as .md
# Display in chat or provide link
echo " Report saved: clients/{client_name}/reports/{month}_report.md"
```

**If `--format pdf`:**
```bash
# Convert .docx to .pdf using pandoc or libreoffice
if command -v pandoc &> /dev/null; then
  pandoc clients/{client_name}/reports/{month}_report.docx -o clients/{client_name}/reports/{month}_report.pdf
elif command -v libreoffice &> /dev/null; then
  libreoffice --headless --convert-to pdf clients/{client_name}/reports/{month}_report.docx --outdir clients/{client_name}/reports/
else
  echo "[WARNING] PDF conversion unavailable (install pandoc or libreoffice)"
  echo "Delivering as .docx instead"
fi
```

---

### Step 11: Present Summary to User

**Display executive summary in chat:**

```markdown
# Monthly SEO Report — {Client Name} ({Month})

## Key Highlights

[OK] **Traffic Up 15.3%** — 12,450 clicks this month (vs. 10,780 last month)
[OK] **New Featured Snippet** — Now ranking for "project management software"
[OK] **2 High-Quality Backlinks** — Acquired from DR 50+ sites
[WARNING] **5 New 404 Errors** — Require immediate fix

## Metrics Summary

| Metric | This Month | Last Month | Change |
|--------|------------|------------|--------|
| Clicks | 12,450 | 10,780 | ↑ 15.3% |
| Impressions | 345,000 | 318,000 | ↑ 8.5% |
| Avg Position | 12.4 | 13.6 | ↑ 1.2 |
| Organic Users | 8,450 | 7,490 | ↑ 12.8% |

## Next Month Priorities

1. Fix 5 new 404 errors (Technical)
2. Publish 2 articles targeting "remote team management" and "async collaboration" (Content)
3. Optimize /features page to recover position for "project management software" (On-Page)

 **Full Report:** [Download {month}_report.docx](file:///path/to/report.docx)
```

**Ask for delivery preference:**
```
Monthly report is ready!

Would you like me to:
1. Keep it local (already saved to clients/{client_name}/reports/)
2. Upload to Google Drive (if configured in brand_kit)
3. Email to client (requires email config)

Type 1, 2, or 3, or just say "done" to finish.
```

---

## Expected Outputs

### Files Created:
1. **`.tmp/{client_name}_gsc_{month}.json`** — GSC data cache
2. **`.tmp/{client_name}_ga4_{month}.json`** — GA4 data cache
3. **`.tmp/{client_name}_crawl_{month}.json`** — Technical crawl snapshot
4. **`clients/{client_name}/reports/{month}_report.{format}`** — Final report (docx/pdf/md)
5. **`clients/{client_name}/audit_history/{month}_crawl.json`** — Archived for next month comparison

### User-Facing Deliverables:
1. **Executive summary in chat** — Key highlights, metrics, priorities
2. **Downloadable report** — Professionally formatted .docx or .pdf
3. **Actionable next steps** — 3-5 specific recommendations

---

## Quality Gates (Check Before Delivery)

Before presenting the report to the user, verify:

- [ ] Brand kit loaded successfully
- [ ] Target month calculated correctly (YYYY-MM format)
- [ ] GSC data pulled OR marked as unavailable with manual entry template
- [ ] GA4 data pulled OR marked as unavailable with manual entry template
- [ ] Technical crawl completed OR skipped with note
- [ ] Content publishing summary included (even if zero articles)
- [ ] Link building summary included (even if zero links)
- [ ] MoM changes calculated OR noted as first month baseline
- [ ] Executive summary has 3-5 bullet highlights
- [ ] Next month priorities has 3-5 specific actions
- [ ] Report file exists and is > 50KB
- [ ] Report file opens without errors
- [ ] All data sections have real data OR clearly marked placeholders
- [ ] Download link is clickable and uses `file://` protocol
- [ ] No tool errors left unhandled

---

## Edge Cases

### 1. **Neither GSC nor GA4 connected**
**Scenario:** `gsc_connected: false` AND `ga4_connected: false`

**Handling:**
- Generate report with manual entry template
- Flag loudly in executive summary: "[ERROR] GSC and GA4 not connected — manual data entry required"
- Provide instructions:
  ```
  To connect GSC: Run `python tools/mcp-gsc/auth.py`
  To connect GA4: Add GA4 property ID to brand_kit.json
  ```
- Fill report with placeholder values:
  - Total clicks: _____ (enter manually)
  - Total impressions: _____ (enter manually)
  - Organic users: _____ (enter manually)

---

### 2. **First month report (no comparison data)**
**Scenario:** No previous month's data exists in `audit_history/`

**Handling:**
- Skip all MoM change calculations
- Display absolute values only (no percentage changes)
- Note in executive summary: "[WARNING] First month report — baseline established for future comparisons"
- Save current month's data to `audit_history/{month}_crawl.json` for next month
- Flag in Next Month Priorities: "Establish tracking baselines for accurate MoM comparisons next month"

---

### 3. **Partial data available (GSC yes, GA4 no)**
**Scenario:** `gsc_connected: true` but `ga4_connected: false`

**Handling:**
- Pull GSC data normally
- Skip GA4 section
- Flag in report: "[WARNING] GA4 not connected — traffic data from GSC only"
- Still generate complete report with available data
- Recommend in Next Month Priorities: "Connect GA4 for deeper traffic insights"

---

### 4. **Tool failures (GSC pull times out, crawl blocked)**
**Scenario:** GSC API returns 429 (rate limit) or crawl returns 403 (blocked)

**Handling:**
- **GSC timeout:**
  1. Wait 30 seconds, retry once
  2. If still fails: Use cached data from previous month (if exists)
  3. Flag: "[WARNING] GSC data unavailable — using last month's cached data as reference"
  4. If no cache: Generate manual entry template

- **Crawl blocked:**
  1. Reduce `--max-pages` to 10 and retry
  2. If still fails: Skip technical health section entirely
  3. Flag: "[WARNING] Technical crawl blocked by site — skipping technical health section"
  4. Recommend: "Check robots.txt for crawler blocking"

---

### 5. **Zero traffic (new site or penalty)**
**Scenario:** GSC returns `total_clicks: 0`, `total_impressions: 0`

**Handling:**
- Check if site is indexed: `site:domain.com` search
- If not indexed:
  - Flag: "[ERROR] CRITICAL: Site not indexed by Google"
  - Recommend: "Check robots.txt, noindex tags, and GSC coverage report"
- If indexed but zero traffic:
  - Flag: "[WARNING] Zero organic traffic — possible penalty or new site"
  - Recommend: "Check GSC for manual actions and ranking drops"
- Still generate report with diagnostic section

---

### 6. **Month not yet complete (running report mid-month)**
**Scenario:** User runs `/monthly_report --month 2025-03` on March 15, 2025

**Handling:**
- Detect incomplete month (current date < end of target month)
- Warning: "[WARNING] Month not yet complete — data is partial"
- Note in executive summary: "Report generated on {current_date} — data through {current_date} only"
- Recommend: "Run full report after {last_day_of_month} for complete data"
- Still generate report with available data

---

### 7. **Custom template missing**
**Scenario:** `brand_kit["reporting"]["custom_report_template"]: "templates/custom.md"` but file doesn't exist

**Handling:**
- Check if custom template path exists
- If missing:
  - Warning: "[WARNING] Custom template not found at {path}"
  - Fallback: Use default `templates/monthly_report_template.md`
  - Note in report: "Using default template (custom template not found)"
- Still generate report successfully

---

### 8. **No content or link building activity**
**Scenario:** Zero articles published, zero links built

**Handling:**
- Don't skip sections — show zeros
- Executive summary highlight: "[WARNING] No content published this month"
- Executive summary highlight: "[WARNING] No link building activity this month"
- Next Month Priorities: "Publish 2-3 articles targeting [keywords]"
- Next Month Priorities: "Launch link building outreach campaign (target: 50 prospects)"

---

### **If `chat_to_report.py` fails:**
1. Read stderr output for error message
2. Common errors:
   - **ModuleNotFoundError (python-docx)**: Run `pip install python-docx`
   - **PermissionError (can't write)**: Check folder permissions on `clients/{client_name}/reports/`
3. If error persists: The raw markdown file generated in `.tmp/` is perfectly usable as a fallback.

### **If MCP GSC/GA4 fails:**
1. Check authentication (credentials valid?)
2. Check network connectivity
3. Fallback to manual CSV export method
4. Document: "[WARNING] Automated data pull failed — manual export used"

### **If crawl fails:**
1. Check site accessibility (is site live?)
2. Check robots.txt (is crawler blocked?)
3. Reduce `--max-pages` and retry
4. If still fails: Skip technical section, flag in report

---

## Performance Expectations

**Estimated execution time:**
- GSC data pull: 10-20 seconds
- GA4 data pull: 10-20 seconds
- Technical crawl (25 pages): 30-60 seconds
- Content/link scanning: 5-10 seconds
- Report generation: 15-30 seconds

**Total: ~2-3 minutes** for complete report generation

**If execution exceeds 5 minutes:**
- Check for tool hangs (crawl timeout, API rate limits)
- Reduce crawl pages, skip optional sections
- Generate report with available data

---

## Notes

- **Data freshness:** GSC and GA4 data may lag 24-48 hours
- **Comparison accuracy:** MoM changes are only accurate if both months have complete data
- **Manual verification:** Always spot-check key metrics (clicks, impressions) against GSC UI
- **Client delivery:** Prefer .docx format (universally compatible, professional formatting)
- **Automation:** This workflow can be scheduled monthly via cron job or GitHub Actions
