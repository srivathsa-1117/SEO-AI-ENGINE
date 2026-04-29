# SEO AI OS — Instruction Audit & Improvement Report

**Date:** 2026-03-16
**Auditor:** Claude (Sonnet 4.5)
**Objective:** Ensure all instructions, workflows, and skills are crystal clear for AI execution and optimized for tool usage

---

## Executive Summary

### Overall Assessment: **Good Foundation, Needs Clarity Enhancement**

**Strengths:**
- [OK] Clear WAT architecture (Workflows → Agents → Tools)
- [OK] Comprehensive global rules in CLAUDE.md
- [OK] Well-structured tool scripts with proper error handling
- [OK] Good separation of concerns between skills and workflows
- [OK] Strong content writing standards (human voice, banned AI words)

**Critical Gaps:**
- [ERROR] Workflows lack explicit tool call syntax and parameters
- [ERROR] Ambiguous "Use X tool" instructions without execution details
- [ERROR] Missing error handling protocols in workflows
- [ERROR] Inconsistent tool naming (mcp-gsc vs gsc_server.py)
- [ERROR] No clear MCP vs Python tool decision tree
- [ERROR] Skills are high-level frameworks, not execution blueprints

---

## 🔴 Critical Issues (Fix Immediately)

### Issue 1: Vague Tool Execution Instructions

**Problem:**
Workflows say "Use X tool" but don't specify:
- Exact command syntax
- Required vs optional parameters
- Expected output location
- What to do if tool fails

**Example from `workflows/audit.md`:**
```markdown
[ERROR] BAD (Current):
2. Use the `seo-audit` skill to perform a comprehensive Technical, Content, and Schema audit.

[OK] GOOD (Should be):
2. Run SEO Technical Audit
   - Execute: `python tools/seo_crawler.py --url {URL} --max-pages 50 --output .tmp/{client}_crawl.json`
   - Expected output: `.tmp/{client}_crawl.json`
   - Success check: File exists and contains `pages_crawled` > 0
   - If fails: Fallback to WebFetch for homepage only, note limitation in report
```

**Impact:**
AI agent has to guess tool syntax, leading to execution failures.

**Files Affected:**
- `workflows/audit.md`
- `workflows/content_brief.md`
- `workflows/competitor_gap.md`
- `workflows/keyword_research.md`
- `workflows/monthly_report.md`

---

### Issue 2: Skills vs. Workflows Confusion

**Problem:**
Skills (`.agents/skills/*/SKILL.md`) read like **conceptual frameworks**, not execution instructions. They tell "what to check" but not "how to execute with tools."

**Example from `.agents/skills/seo-audit/SKILL.md`:**
```markdown
[ERROR] BAD (Current):
**Crawlability**
- Check for unintentional blocks
- Verify important pages allowed
- Check sitemap reference

[OK] GOOD (Should be):
**Crawlability Audit**
1. Fetch robots.txt:
   - Use WebFetch: `{url}/robots.txt`
   - Parse for `Disallow:` directives
   - Flag if `/` or `/blog` are blocked for Googlebot
2. Verify sitemap:
   - Use WebFetch: `{url}/sitemap.xml`
   - Parse for `<url>` count
   - If 0 URLs → Critical issue
   - If > 50,000 URLs → Recommend sitemap index
```

**Impact:**
AI doesn't know whether to use WebFetch, Bash, Read, or a custom tool.

**Files Affected:**
- All 18 skills in `.agents/skills/`

---

### Issue 3: No MCP vs Python Tool Decision Tree

**Problem:**
The system has both MCP servers and Python tools for similar functions (e.g., PageSpeed MCP vs `lighthouse_audit.py`). No instructions on which to prefer or when to fallback.

**Missing Logic:**
```markdown
[OK] SHOULD ADD TO CLAUDE.md:

## Tool Selection Hierarchy

**Rule: Always prefer MCP tools when available, fallback to Python**

### PageSpeed / Core Web Vitals
1st choice: MCP `pagespeed_analyze` (if configured)
2nd choice: `python tools/lighthouse_audit.py --url {url} --strategy both`
3rd choice: WebFetch PageSpeed Insights URL and parse HTML

### Google Search Console Data
1st choice: MCP `gsc` server (if authenticated)
2nd choice: Manual export → Read CSV
3rd choice: Infer from industry benchmarks + note limitation

### SERP Scraping
1st choice: `python tools/serp_scraper.py --mode {mode} --keyword "{kw}"`
2nd choice: WebSearch for manual analysis
3rd choice: DuckDuckGo AI chat for quick validation
```

**Impact:**
AI wastes time trying wrong tools or doesn't know fallback options.

---

### Issue 4: Missing Tool Output Validation

**Problem:**
Workflows assume tools succeed. No validation steps like "check if output file exists" or "verify JSON has expected keys."

**Example from `workflows/content_brief.md`:**
```markdown
[ERROR] BAD (Current):
### Step 2: SERP Analysis (Competitor Research)
- Run: `tools/serp_scraper.py --mode serp_top10 --keyword "<target_keyword>"`
- Output: `.tmp/<client_name>_serp_analysis.json`

[OK] GOOD (Should be):
### Step 2: SERP Analysis (Competitor Research)
**Execute:**
```bash
python tools/serp_scraper.py --mode serp_top10 --keyword "<target_keyword>" --output .tmp/{client}_serp.json
```

**Validate Output:**
- Check: `.tmp/{client}_serp.json` exists
- Check: JSON contains `results` array with len ≥ 3
- If validation fails:
  - Retry once with 10-second delay (rate limit)
  - If still fails: Use WebSearch as fallback, manually parse top 5 results
  - Document in brief: "[WARNING] SERP data from manual search (tool unavailable)"
```

**Impact:**
Silent failures. AI proceeds with corrupted/empty data.

---

### Issue 5: Ambiguous "Use Skill X" References

**Problem:**
Workflows reference skills like "use the seo-audit skill" but skills are frameworks, not executable tools.

**Example from `workflows/audit.md`:**
```markdown
[ERROR] BAD (Current):
2. Use the `seo-audit` skill to perform a comprehensive Technical, Content, and Schema audit.

[OK] GOOD (Should be):
2. Technical SEO Audit (using seo-audit framework)
   **Phase 1: Crawl Site**
   - Execute: `python tools/seo_crawler.py --url {url} --max-pages 50 --timeout 120`
   - Wait for completion (may take 2-5 min)
   - Output: `.tmp/{client}_crawl.json`

   **Phase 2: Analyze Crawl Data**
   - Read: `.tmp/{client}_crawl.json`
   - Extract: page count, 404s, redirect chains, missing canonicals
   - Reference: `.agents/skills/seo-audit/SKILL.md` for issue severity classification

   **Phase 3: Check Core Web Vitals**
   - Execute: `python tools/lighthouse_audit.py --url {url} --strategy both`
   - Parse: LCP, INP, CLS scores
   - Flag if any metric exceeds threshold (LCP > 2.5s, INP > 200ms, CLS > 0.1)
```

**Impact:**
AI doesn't know skills are reference docs, not executable scripts.

---

## 🟡 High Priority Issues

### Issue 6: No Error Recovery Protocols

**Problem:**
Workflows don't specify what to do when tools fail due to rate limits, blocked IPs, or missing dependencies.

**Should Add to Each Workflow:**
```markdown
## Error Handling Protocol

**If tool returns 429 (Rate Limited):**
- Wait 30 seconds
- Retry once
- If still fails: Proceed with degraded data, flag in report

**If tool returns 403 (Blocked):**
- Check if User-Agent header is set
- If SERP scraper: Switch to WebSearch + manual parsing
- Document limitation: "[WARNING] Direct scraping blocked, using alternative method"

**If tool crashes (exit code ≠ 0):**
- Read error trace from stderr
- Check if dependency missing (pip install needed)
- If unfixable: Ask user for manual data export OR skip section

**If output JSON is malformed:**
- Try to parse with error tolerance (json.loads with catch)
- If unrecoverable: Use empty dict {}, log warning
- Continue workflow with degraded data
```

---

### Issue 7: Inconsistent File Naming Conventions

**Problem:**
Workflows reference `.tmp/{client}_serp_analysis.json` but tools output `.tmp/serp_results_{timestamp}.json`

**Examples:**
- `workflows/content_brief.md` expects `.tmp/<client_name>_serp_analysis.json`
- `tools/serp_scraper.py` actually creates `.tmp/serp_top10_results.json` (no client name)

**Fix:**
Standardize all tool outputs to include client name or require `--client` flag:
```bash
python tools/serp_scraper.py --mode serp_top10 --keyword "X" --client acme_corp --output .tmp/acme_corp_serp.json
```

---

### Issue 8: Missing Tool Parameter Defaults

**Problem:**
Workflows don't specify what to pass when optional parameters are unclear.

**Example from `workflows/keyword_research.md`:**
```markdown
[ERROR] BAD (Current):
- Run: `tools/serp_scraper.py --mode autosuggest --keyword "<seed_keyword>" --location <target_location>`

[OK] GOOD (Should be):
**Execute:**
```bash
python tools/serp_scraper.py \
  --mode autosuggest \
  --keyword "{seed_keyword}" \
  --location "{brand_kit.target_locations[0] OR 'us'}" \
  --output ".tmp/{client}_autosuggest.json"
```

**Parameter Notes:**
- `--location`: Use first item from `brand_kit.target_locations`, default to 'us' if empty
- `--output`: Always include client name for multi-client workflows
```

---

## 🟢 Medium Priority Issues

### Issue 9: Skills Lack "When NOT to Use This" Section

**Problem:**
Skills describe when to use them but not when to avoid them or use a different skill instead.

**Fix for `.agents/skills/programmatic-seo/SKILL.md`:**
```markdown
## When NOT to Use This Skill

[ERROR] Don't use programmatic-seo if:
- Client has < 5,000 monthly organic traffic (focus on core pages first)
- Fewer than 20 target keywords (write individual pages instead)
- No unique data source (will create thin content)
- Industry has no pattern-based searches (e.g., highly custom B2B services)

[OK] Use instead:
- For individual articles → **copywriting** skill
- For technical fixes → **seo-audit** skill
- For keyword strategy → **content-strategy** skill
```

---

### Issue 10: No Tool Timeout Guidance

**Problem:**
Some tools (like `seo_crawler.py`) can run for 10+ minutes. Workflows don't set expectations or max timeouts.

**Fix:**
Add to each tool call:
```markdown
**Execute:**
```bash
timeout 300 python tools/seo_crawler.py --url {url} --max-pages 50
```
(5-minute max timeout)

**If timeout occurs:**
- Use partial results if `.tmp/{client}_crawl_partial.json` exists
- Reduce `--max-pages` to 25 and retry
- If still fails: Crawl homepage only, note limitation
```

---

### Issue 11: CLAUDE.md Rule 13 (Growth Innovation) Too Vague

**Problem:**
```markdown
[ERROR] CURRENT:
### Rule 13: Growth Innovation — Brand-Specific Only
Never give generic growth ideas...

[OK] SHOULD BE MORE SPECIFIC:
### Rule 13: Growth Innovation — Brand-Specific Only

**Bad Example:**
"Start a blog and post consistently."

**Good Example:**
"Create 'The Saree Encyclopedia' — a 50-page glossary of saree terms (Bandhani, Patola, Maheshwari, etc.) with origin stories, weaving techniques, and regional variations. Each term page targets long-tail searches like 'what is Maheshwari saree' (1,200 monthly searches). Link opportunities: Wikipedia citations, fashion school resources, cultural heritage sites."

**How to Generate Good Ideas:**
1. Read brand_kit.json industry + competitors
2. Search "[industry] content ideas" and "[competitor] blog"
3. Identify the gap: what exists vs. what's missing
4. Propose 3 ideas with:
   - **What:** Specific content type with title
   - **Why:** Search volume OR backlink potential
   - **How:** Execution plan (effort level, resources needed)
   - **When:** Time to first result (weeks/months)
```

---

## 🟣 Low Priority Issues (Polish)

### Issue 12: No "Quick Syntax Reference" Section

**Fix:**
Add to CLAUDE.md:
```markdown
## Quick Tool Syntax Reference

**Web Scraping:**
```bash
python tools/fetch_page.py --url {url} --output .tmp/{client}_page.html
```

**SERP Analysis:**
```bash
python tools/serp_scraper.py --mode serp_top10 --keyword "{kw}" --output .tmp/{client}_serp.json
```

**Keyword Clustering:**
```bash
python tools/keyword_clusterer.py --input .tmp/keywords.txt --output .tmp/clusters.json
```

**Report Generation:**
```bash
python tools/chat_to_report.py --input .tmp/{client}_report.md --output "reports/{client}_audit_{date}.docx"
```

**Schema Generation:**
```bash
python tools/schema_gen.py --type Article --data .tmp/{client}_metadata.json
```

**NLP Analysis:**
```bash
python tools/nlp_analyzer.py --mode gap --serp-data .tmp/{client}_serp.json
```

**Lighthouse Audit:**
```bash
python tools/lighthouse_audit.py --url {url} --strategy both --output .tmp/{client}_cwv.json
```
```

---

### Issue 13: Workflow Outputs Not Specified

**Problem:**
Workflows describe steps but not final deliverables.

**Fix Pattern:**
```markdown
## Expected Outputs

**Files Created:**
- `.tmp/{client}_keyword_clusters.json` — Clustered keywords with intent labels
- `clients/{client}/active_campaigns/keyword_research_{date}.md` — Human-readable report

**User-Facing Deliverable:**
Markdown table in chat:
| Keyword | Intent | Difficulty | Trend |
|---------|--------|------------|-------|
| ...     | ...    | ...        | ...   |

**Next Action Prompt:**
"Do these keyword clusters look good? Should I build a Content Brief for the top opportunity?"
```

---

### Issue 14: No Data Freshness Protocol

**Problem:**
Should the AI reuse `.tmp/` files from yesterday or regenerate?

**Fix:**
Add to CLAUDE.md:
```markdown
## Temporary File Freshness Rules

**Reuse if:**
- File is < 24 hours old
- Client hasn't changed brand_kit.json since file creation
- User explicitly says "use previous data"

**Regenerate if:**
- File is > 24 hours old
- Workflow is /audit or /monthly_report (always fresh data)
- File size is 0 bytes (failed previous run)

**Check freshness:**
```python
from datetime import datetime, timedelta
from pathlib import Path

file = Path(f".tmp/{client}_serp.json")
if file.exists() and (datetime.now() - datetime.fromtimestamp(file.stat().st_mtime)) < timedelta(hours=24):
    print("[OK] Using cached data from", file.stat().st_mtime)
else:
    print("🔄 Data is stale, regenerating...")
```
```

---

## 📋 Rewrite Priority List

### Phase 1: Critical Fixes (Do First)
1. [OK] Rewrite `workflows/audit.md` with explicit tool calls
2. [OK] Rewrite `workflows/content_brief.md` with tool validation
3. [OK] Rewrite `workflows/competitor_gap.md` with error handling
4. [OK] Add "Tool Selection Hierarchy" section to CLAUDE.md
5. [OK] Add "Error Handling Protocol" template to CLAUDE.md

### Phase 2: High Priority
6. [OK] Standardize all tool output file naming (`--client` flag)
7. [OK] Add "Expected Outputs" section to all workflows
8. [OK] Rewrite `.agents/skills/seo-audit/SKILL.md` as execution blueprint
9. [OK] Rewrite `.agents/skills/geo-audit/SKILL.md` with tool orchestration
10. [OK] Add timeout guidance to tool-heavy workflows

### Phase 3: Medium Priority
11. Add "When NOT to Use" to all skills
12. Add "Quick Tool Syntax Reference" to CLAUDE.md
13. Improve Rule 13 examples in CLAUDE.md
14. Add data freshness protocol to CLAUDE.md

---

## Methodology for AI-Clear Instructions

### [OK] Do This:
```markdown
**Step 3: Fetch Competitor Content**

Execute:
```bash
python tools/fetch_page.py --url "{competitor_url}" --output ".tmp/{client}_comp1.html"
```

Validate:
- Check file exists: `[ -f .tmp/{client}_comp1.html ]`
- Check file size > 1KB (not empty)

Parse:
- Read file with Read tool
- Extract: H1, H2, word count, meta description
- Store in: `.tmp/{client}_comp_analysis.json`

If fetch fails (403/404):
- Try WebFetch as fallback
- If still fails: Skip this competitor, note in report: "[WARNING] {competitor_url} blocked crawlers"
```

### [ERROR] Don't Do This:
```markdown
**Step 3: Analyze Competitors**
- Use the competitor analysis tool
- Look at their content structure
- Note what they do well
```

---

## Next Steps

**Option 1: Automated Rewrite**
I can systematically rewrite all flagged files using the patterns above.

**Option 2: Template + Manual**
I create rewrite templates for workflows/skills, you review, then I execute.

**Option 3: Selective Fix**
You tell me which files/issues to prioritize, I fix those first.

**Recommendation:** Option 1 (Automated Rewrite) — I rewrite Phase 1 Critical Fixes now, you review, then we proceed to Phase 2.

---

**What would you like me to do?**
