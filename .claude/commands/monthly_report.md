---
description: /monthly_report - Generate a complete monthly SEO performance report for a client
---

# Workflow: Monthly Report Generation

## Trigger
```
/monthly_report <client_name> [--month YYYY-MM] [--format markdown|pdf|slides]
```
**Example:** `/monthly_report acme_corp --month 2025-02 --format pdf`

## Objective
Pull all available data sources and generate a comprehensive, beautifully formatted monthly SEO report. Deliver to the client or save locally.

## Required Inputs
1. `<client_name>` — loads brand_kit and previous month's data
2. `--month` — defaults to last full calendar month
3. `--format` — defaults to `markdown`

## Step-by-Step Instructions

### Step 1: Load Context
- Read `clients/<client_name>/brand_kit.json`
- Confirm `gsc_connected` and `ga4_connected` status
- Check `reporting.custom_report_template` — use it if set, else use `templates/monthly_report_template.md`

### Step 2: Pull GA4 Data (if connected)
- Run: `tools/fetch_ga4_data.py --client <client_name> --month <YYYY-MM>`
- Pulls: Organic sessions, users, bounce rate, avg. session duration, top landing pages by organic traffic
- Calculates: Month-over-month % change
- Output: `.tmp/<client_name>_ga4_<month>.json`

### Step 3: Pull GSC Data (if connected)
- Run: `tools/fetch_gsc_data.py --client <client_name> --month <YYYY-MM>`
- Pulls: Total impressions, clicks, avg CTR, avg position
- Top 10 queries by clicks (with position change from last month)
- Top 10 pages by impressions
- New keywords ranking in top 10 this month
- Keywords that dropped out of top 10
- Output: `.tmp/<client_name>_gsc_<month>.json`

### Step 4: Technical Health Snapshot
- Compare latest crawl data with previous month's crawl (from `audit_history/`)
- Notes: New 404s found, New redirect issues, Index count change

### Step 5: Content & Link Building Summary
- Scan `clients/<client_name>/active_campaigns/` for:
  - Articles published this month
  - Links built / outreach sent this month

### Step 6: Compile Report
- The SEO Director agent uses all collected data to write a detailed markdown report in the chat.
- It covers Executive Summary, Traffic Overview, Rankings & Visibility, Technical Health, Content Published, Links Built, AEO/GEO Status, and Next Month Priorities.
- The user reviews and approves the report.

### Step 7: Format Output
- Save the approved chat output to `.tmp/<client_name>_<month>_approved.md`
- Run: `python tools/chat_to_report.py --input .tmp/<client_name>_<month>_approved.md --output clients/<client_name>/reports/<month>_report.docx`
- If `--format pdf` is requested, inform the user that DOCX is the standard native output now and provide the DOCX path.

### Step 8: Present Summary & Deliver
Display executive summary in chat.
Ask: **"Monthly report is ready! Shall I push this to Google Drive, or do you want to review it locally first?"**

## Edge Cases
- If neither GSC nor GA4 is connected: generate a "manual input" report template with empty fields and instructions on how to connect APIs. Flag this loudly.
- If it's the first month (no comparison data): skip MoM change calculations and note it's the baseline month.
