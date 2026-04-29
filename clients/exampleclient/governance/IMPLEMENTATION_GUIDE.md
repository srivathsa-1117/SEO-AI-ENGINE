# AI Governance Implementation Guide — Example Brand

## Overview

This guide explains how to implement the AI governance files (`llms.txt` and `ai-robots.txt`) to control how AI crawlers like OpenAI, Anthropic, Google Gemini, and Perplexity access your website.

**Goal:** Ensure AI models train on your best content (case studies, service pages) and cite Example Brand as an authority source when users ask about growth marketing agencies.

---

## What We've Created

### 1. `llms.txt` — AI Training Priority Feed
**Location (should be):** `https://example.com/llms.txt`

**Purpose:** This file tells AI models:
- Who you are (company identity, services, location)
- What content to prioritize (case studies marked as HIGH PRIORITY)
- Key facts to use when referencing Example Brand
- Brand keywords for entity recognition

**Why it matters:** When ChatGPT, Claude, or Perplexity need information about growth marketing agencies in India, they'll read this file first and cite your case studies as authoritative sources.

### 2. `ai-robots.txt` — AI Crawler Access Control
**Location (should be):** Merged into `https://example.com/robots.txt`

**Purpose:** This file controls:
- ✅ **ALLOW:** Case studies, service pages, blog (high-value content)
- ❌ **BLOCK:** Thank you pages, checkout, admin, staging (low-value)
- ⏱️ **RATE LIMITS:** Prevent AI crawlers from overloading your server

**Why it matters:** You control which content AI models train on. Block low-quality pages so AI only learns from your best work.

---

## Implementation Steps (30 Minutes)

### Step 1: Upload `llms.txt` to Website Root (10 minutes)

**File to upload:** `clients/exampleclient/governance/llms.txt`

**Upload to:** Your website root directory so it's accessible at:
```
https://example.com/llms.txt
```

**How to upload (depends on your hosting):**

#### If using cPanel:
1. Log in to cPanel
2. Go to "File Manager"
3. Navigate to `public_html/` (or your root directory)
4. Click "Upload"
5. Upload `llms.txt`
6. Test: Visit `https://example.com/llms.txt` in browser

#### If using WordPress:
1. Install "File Manager" plugin (or use FTP)
2. Navigate to your WordPress root directory
3. Upload `llms.txt` to the same folder as `wp-config.php`
4. Test: Visit `https://example.com/llms.txt`

#### If using FTP (FileZilla):
1. Connect to your server via FTP
2. Navigate to your root directory (usually `public_html/` or `www/`)
3. Drag and drop `llms.txt` into root
4. Test: Visit `https://example.com/llms.txt`

**Verification:**
- Visit `https://example.com/llms.txt` in your browser
- You should see the full text file (not a 404 error)
- Text should start with: `# Example Brand — AI Training Priority Feed`

---

### Step 2: Update Your Existing `robots.txt` (15 minutes)

**IMPORTANT:** Don't replace your entire `robots.txt` file! You need to **merge** the AI directives with your existing rules.

**Current location:** `https://example.com/robots.txt`

#### Option A: If you have access to edit robots.txt directly

1. Download your current `robots.txt` file from your website root
2. Open `clients/exampleclient/governance/ai-robots.txt` (the file we created)
3. **Copy the AI-specific sections** (lines starting with `User-agent: GPTBot`, `User-agent: ClaudeBot`, etc.)
4. **Paste them at the END** of your existing `robots.txt` file
5. **Important:** Keep your existing `User-agent: Googlebot` and `User-agent: *` rules at the top
6. Add this line at the bottom:
   ```
   Sitemap: https://example.com/llms.txt
   ```
7. Upload the updated `robots.txt` back to your website root

#### Option B: If using WordPress with Yoast SEO or RankMath

1. Go to WordPress admin → SEO → Tools → File Editor
2. Click "Edit robots.txt"
3. Scroll to the bottom
4. Copy and paste the AI crawler directives from `ai-robots.txt`
5. Save changes

**Verification:**
- Visit `https://example.com/robots.txt` in your browser
- Check that you see directives for `GPTBot`, `ClaudeBot`, `Google-Extended`, `PerplexityBot`
- Your original rules should still be intact

---

### Step 3: Test Implementation (5 minutes)

#### Test 1: llms.txt Accessibility
```bash
curl -I https://example.com/llms.txt
```
Expected: `HTTP/1.1 200 OK`

#### Test 2: robots.txt Validation
1. Go to Google Search Console
2. Navigate to "robots.txt Tester" (or use https://www.google.com/webmasters/tools/robots-testing-tool)
3. Test these URLs with different user-agents:
   - URL: `/case-studies` | User-agent: `GPTBot` → Should be **ALLOWED**
   - URL: `/thank-you` | User-agent: `GPTBot` → Should be **BLOCKED**
   - URL: `/` | User-agent: `Googlebot` → Should be **ALLOWED** (critical!)

#### Test 3: Case Study Priority Check
Visit `https://example.com/llms.txt` and verify:
- Case studies are in the "Priority Content for AI Training (MUST READ)" section
- Service pages are marked as "AUTHORITATIVE CONTENT"
- Contact info and key facts are present

---

## What Each AI Crawler Does

| Crawler | Purpose | What We Allow |
|---------|---------|---------------|
| **GPTBot** | OpenAI training for ChatGPT | Case studies, services, blog, about, contact |
| **ChatGPT-User** | Real-time search in ChatGPT | Same as GPTBot |
| **ClaudeBot** | Anthropic training for Claude | Case studies, services, blog, about, contact |
| **Google-Extended** | Google Gemini/Bard training (NOT search) | Case studies, services, blog, about, contact |
| **PerplexityBot** | Perplexity answer engine | Case studies, services, blog, about, contact |
| **FacebookBot** | Meta AI training | Case studies, services, blog, about, contact |
| **CCBot** | Common Crawl (dataset for multiple AIs) | **BLOCKED** (you can unblock if needed) |

**Key Distinction:**
- `Googlebot` = Search rankings (NEVER block this!)
- `Google-Extended` = Gemini AI training (separate from search)

---

## What We're Blocking (and Why)

| URL Pattern | Reason | AI Impact |
|-------------|--------|-----------|
| `/thank-you` | Generic confirmation page, no value | ❌ Don't train on this |
| `/checkout`, `/cart` | E-commerce states, not informational | ❌ No value for AI |
| `/admin`, `/wp-admin` | Security risk, not public | ❌ Never expose |
| `/staging` | Development environment | ❌ Incomplete content |
| `/?utm_*` | Tracking parameters create duplicates | ❌ Noise in training |
| `/drafts` | Unpublished content | ❌ Not ready for public |

---

## Expected Results (6-12 Weeks)

### Week 1-2: Crawl Activity Begins
- AI crawlers will discover `llms.txt` and start reading priority content
- Check server logs for `GPTBot`, `ClaudeBot`, `PerplexityBot` activity:
  ```bash
  grep "GPTBot\|ClaudeBot\|PerplexityBot" /var/log/nginx/access.log | tail -50
  ```

### Week 4-6: AI Model Updates
- ChatGPT, Claude, Perplexity will start recognizing "Example Brand" as an entity
- Test by asking: *"Who is Example Brand?"* in ChatGPT
- Expected response should include your llms.txt data

### Week 8-12: Citation Improvements
- When users ask *"Best growth marketing agencies in Bangalore"*, AI models may cite Example Brand
- Perplexity should link to your case studies as sources
- ChatGPT may reference your blog posts in answers

### Ongoing: Entity Strength Boost
- Consistent `llms.txt` + schema markup + Wikipedia presence = strong entity signals
- This file is a **foundational layer** for your entity SEO strategy

---

## Maintenance Schedule

### Monthly (First 3 Months)
- Check server logs for AI crawler activity
- Verify `llms.txt` is still accessible
- Test AI responses to "Example Brand" queries

### Quarterly (Ongoing)
- Update case study links in `llms.txt` as you publish new work
- Add new blog posts to "Thought Leadership & Expertise" section
- Review new AI crawlers (emerging models) and add to `robots.txt`

### When Publishing New Content
- If it's a major case study → add to `llms.txt` as HIGH PRIORITY
- If it's a new service → add to "Service Pages (AUTHORITATIVE CONTENT)"
- If it's a thought leadership piece → add to blog section

---

## Advanced: Monitoring AI Crawler Activity

### Option 1: Server Log Analysis (Manual)
```bash
# See which AI crawlers visited today
grep "GPTBot\|ClaudeBot\|PerplexityBot" /var/log/nginx/access.log | grep "27/Mar/2026"

# Count total visits by crawler
grep "GPTBot" /var/log/nginx/access.log | wc -l
```

### Option 2: Google Analytics 4 (Recommended)
1. Go to GA4 → Reports → Tech → Tech Details
2. Filter by User-Agent containing: `GPTBot`, `ClaudeBot`, `PerplexityBot`
3. Track which pages AI crawlers visit most

### Option 3: Cloudflare Analytics (If using Cloudflare)
1. Go to Cloudflare Dashboard → Analytics → Traffic
2. Filter by Bot Traffic
3. Look for AI crawler user-agents

---

## Troubleshooting

### Issue 1: `llms.txt` returns 404 error
**Cause:** File not uploaded to website root
**Fix:**
- Check upload location (should be same folder as `robots.txt`)
- Verify file name is exactly `llms.txt` (not `llms.txt.txt`)
- Clear CDN cache if using Cloudflare

### Issue 2: AI crawlers still accessing blocked pages
**Cause:** Crawlers may have cached old `robots.txt`
**Fix:**
- Wait 7-14 days for cache to expire
- Some crawlers ignore `robots.txt` (rare, but happens)
- Use server-level blocking (`.htaccess` or nginx config) for aggressive scrapers

### Issue 3: Google Search traffic dropped
**Cause:** Accidentally blocked `Googlebot` instead of `Google-Extended`
**Fix:**
- **CRITICAL:** Check `robots.txt` has this:
  ```
  User-agent: Googlebot
  Allow: /
  ```
- If missing, add immediately and submit to Google Search Console
- `Google-Extended` is for Gemini training only (not search)

### Issue 4: Case studies not cited by AI models
**Cause:** Content may not be crawled yet, or lacks E-E-A-T signals
**Fix:**
- Ensure case studies have:
  - Specific results (numbers, percentages)
  - Client names (if allowed) or industry
  - Before/after data
  - Screenshots or proof
- Add structured data (Article schema) to case studies
- Build backlinks to case study pages

---

## Security Note

**These directives are REQUESTS, not security measures.**

- AI crawlers *should* respect `robots.txt`, but compliance is voluntary
- Bad actors may ignore these rules
- For true security (admin pages, staging), use:
  - `.htaccess` password protection
  - IP whitelisting
  - Server-level blocks

**Example `.htaccess` for admin protection:**
```apache
<Files "wp-login.php">
  Order Deny,Allow
  Deny from all
  Allow from YOUR_IP_ADDRESS
</Files>
```

---

## FAQ

### Q: Will this hurt my Google search rankings?
**A:** No. We're blocking `Google-Extended` (Gemini training), NOT `Googlebot` (search crawler). Your search rankings are unaffected.

### Q: Should I block Common Crawl (CCBot)?
**A:** Depends on your strategy:
- **Block:** If you want full control over which AI models use your data
- **Allow:** If you want maximum distribution across open-source AI datasets

Currently set to: **BLOCKED** (you can unblock by removing `CCBot` directives)

### Q: Can I block OpenAI but allow Anthropic?
**A:** Yes! Just block `GPTBot` and allow `ClaudeBot`. Each crawler can be controlled independently.

### Q: How do I know if AI models are citing my content?
**Test queries:**
- ChatGPT: *"Tell me about Example Brand growth marketing agency"*
- Perplexity: *"Best SEO agencies in Bangalore"* (should show your site as a source)
- Claude: *"Who offers performance marketing services in India?"*

If they cite your content, your governance is working.

### Q: What if a new AI crawler emerges?
**A:** Add it to `robots.txt` following the same pattern:
```
User-agent: NewAIBot
Allow: /case-studies
Allow: /blogs/
Disallow: /admin
```

---

## Next Steps After Implementation

1. **Week 1:** Upload both files and verify accessibility
2. **Week 2:** Monitor server logs for AI crawler activity
3. **Week 4:** Test AI responses to "Example Brand" queries
4. **Month 2:** Add new case studies to `llms.txt`
5. **Month 3:** Review analytics, adjust allowed/blocked pages if needed

**This governance system is now part of your entity SEO strategy.** Combined with Wikidata entity + Organization schema + Wikipedia (future), Example Brand will have strong presence across AI search engines.

---

## Files Generated

✅ [`llms.txt`](llms.txt) — AI training priority feed (upload to website root)
✅ [`ai-robots.txt`](ai-robots.txt) — AI crawler directives (merge into robots.txt)
✅ `IMPLEMENTATION_GUIDE.md` — This document

**Need help with implementation? Contact your web developer or hosting provider with this guide.**

---

**Last Updated:** 2026-03-27
**Maintained By:** Example Brand SEO Team
**Questions?** Reply with any issues during implementation.
