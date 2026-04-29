---
description: /audit - Run a full SEO audit for a client (Technical, On-Page, AEO/GEO scoring)
---

# Workflow: Full SEO Audit

## Trigger
```
/audit <website_url_or_client_name> [--type first_time|post_onboarding]
```
**Examples:**
- `/audit thedarenetwork.com` — quick audit, no client record created
- `/audit acme_corp --type first_time` — audit for an existing client in `clients/`

---

## [WARNING] CRITICAL RULE: Client List vs. Standalone Audit

> **DO NOT add a site to the client list just because someone asks for an audit.**

- If the user says **"run an audit on [site]"** or **"audit [site]"** → run the audit and output the report. Do NOT create a client folder or ask for brand kit details.
- If the user says **"add [name] as a client"** or **"onboard [name]"** → follow the `/add_client` workflow and collect all brand kit details first.
- If the user says **"run an audit for my client [name]"** and that client already exists in `clients/` → load the brand kit and run the audit using their stored details.
- If someone asks to do an audit AND add as a client in the same message → first collect all brand kit information (see `/add_client` workflow) before running the audit.

---

## Step-by-Step Instructions

### Step 1: Determine Mode

Check whether a client folder exists:
- `clients/<name>/brand_kit.json` exists → **Client Mode**: load brand kit, use stored `website_url`
- No client folder → **Standalone Mode**: use the URL directly, save output to `.tmp/reports/`

### Step 2: Site Crawl (Technical SEO)
- Run: `python tools/seo_crawler.py --url <website_url> --output .tmp/<slug>_crawl.json`
- Collects: all URLs, HTTP status codes (200, 301, 404, 500), canonical tags, hreflang, noindex tags, H1s, meta descriptions, schema types, internal link graph
- Output: `.tmp/<slug>_crawl.json`

### Step 3: On-Page Analysis (Top 10 Pages)
- Read top 10 URLs from crawl output (by internal link count = most important pages)
- Run: `python tools/on_page_analyzer.py --urls-file .tmp/<slug>_crawl.json --output .tmp/<slug>_onpage.json`
- Checks: H1 uniqueness, title tag length (50-60 chars), meta desc length (120-160 chars), keyword presence, image alt text, schema presence
- Output: `.tmp/<slug>_onpage.json`

### Step 4: AEO / GEO Schema Check
- Review crawl data for schema types found on each page
- Check for: FAQPage, Article, Organization, LocalBusiness, BreadcrumbList schemas
- Score AEO readiness 0–100 based on coverage

### Step 5: GSC Data (Client Mode Only)
- Only attempt if the client brand kit has GSC credentials configured
- If not connected: skip and note clearly in the report

### Step 6: Generate Word Report
- Wait for user approval of the chat output.
- Save the approved markdown to `.tmp/approved_audit.md`.
- Run: `python tools/chat_to_report.py --input .tmp/approved_audit.md --output clients/<name>/reports/<YYYY-MM-DD>_audit_report.docx`
  - **Standalone**: `... --output .tmp/reports/<YYYY-MM-DD>_audit_report.docx`

### Step 7: Present Summary + Download Link

Display the summary table in chat:

| Category | Score | Critical Issues |
|---|---|---|
| Technical SEO | /100 | e.g. 12 broken links |
| Core Web Vitals | /100 | e.g. LCP 4.2s (Poor) |
| On-Page | /100 | e.g. 5 missing H1s |
| AEO/GEO Readiness | /100 | e.g. No FAQ Schema |

Then provide the download link:
```
📄 Download Audit Report: [YYYY-MM-DD_audit_report.docx](file:///path/to/report.docx)
```

Then ask: **"Audit complete. Do you want me to start fixing the Critical Issues, or is there anything else?"**

---

## Edge Cases
- GSC not connected → skip GSC step, note in report
- Site has >500 pages → crawl up to 500 URLs, note the limit
- Lighthouse unavailable → skip CWV section, add manual Lighthouse instructions in report
- User asks to audit AND add client → collect brand kit details first via `/add_client`, then run audit
