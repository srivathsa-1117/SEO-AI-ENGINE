---
description: /keyword_research - Discover and cluster high-intent keywords for a client with complete tool orchestration
---

# Workflow: Keyword Research

## Trigger
```
/keyword_research <client_name> "<seed_keyword>" [--depth broad|deep]
```
**Example:** `/keyword_research acme_corp "project management software" --depth deep`

---

## Objective
Build a complete keyword map with search intent labels, difficulty estimates (without paid tools), and trend data. Cluster keywords by topic using ML. Pause for user approval before proceeding to content brief.

---

## Required Inputs
1. `<client_name>` — loads `clients/<client_name>/brand_kit.json`
2. `<seed_keyword>` — the starting topic
3. `[--depth]` — Optional: `broad` (100-200 keywords) or `deep` (500+ keywords)

---

## Step-by-Step Execution

### Step 1: Load Client Context

**Execute:**
```bash
# Read brand kit
Read: clients/{client}/brand_kit.json
```

**Extract required fields:**
```json
{
  "negative_keywords": ["competitor names", "irrelevant terms"],
  "target_locations": ["United States", "United Kingdom"],
  "language": "en",
  "content_pillars": ["pillar1", "pillar2"],
  "website_url": "https://client-domain.com"
}
```

**Validate:**
```bash
# Check if client exists
if [ ! -f "clients/{client}/brand_kit.json" ]; then
  echo "[ERROR] Client not found. Run /add_client first."
  exit 1
fi
```

**If field is missing:**
- `negative_keywords` → default to empty array `[]`
- `target_locations` → default to `["us"]`
- `language` → default to `"en"`

---

### Step 2: Google Autosuggest Scraping

**Tool:** `serp_scraper.py` (mode: autosuggest)

**Execute:**
```bash
python tools/serp_scraper.py \
  --mode autosuggest \
  --keyword "{seed_keyword}" \
  --location "{target_locations[0]}" \
  --output ".tmp/{client}_autosuggest.json"
```

**What this does:**
- Extracts all A-Z suffix suggestions (e.g., "keyword a", "keyword b", ...)
- Scrapes People Also Ask (PAA) questions
- Returns 200-500 keyword variations

**Validate output:**
```bash
# Check file exists
if [ ! -f ".tmp/{client}_autosuggest.json" ]; then
  echo "[ERROR] Autosuggest scraping failed"
  # Fallback: Manual keyword brainstorming
fi

# Check has minimum 10 keywords
# Use Read tool to parse JSON
```

**Parse results:**
```json
{
  "seed_keyword": "project management software",
  "suggestions": [
    "project management software for small teams",
    "project management software free",
    "project management software comparison",
    ...
  ],
  "paa_questions": [
    "What is the best project management software?",
    "How much does project management software cost?",
    ...
  ],
  "total_keywords": 247
}
```

**If tool fails (rate limited):**
1. Wait 30 seconds, retry once with 10-second delay between requests
2. If still fails: Use WebSearch for "{seed_keyword}" and manually extract related queries
3. Document: "[WARNING] Autosuggest scraper rate-limited, using manual keyword expansion"

**If < 10 keywords found:**
- Broaden search automatically with 3 related seed keywords
- Example: "project management" → Try "team management", "task management", "workflow software"
- Combine results

---

### Step 3: Google Trends Analysis

**Tool:** `serp_scraper.py` (mode: trends)

**Prepare keyword list:**
```bash
# Extract keywords from autosuggest results
# Write to temporary file (comma-separated)
Write: .tmp/{client}_keywords_for_trends.txt
```

**Execute:**
```bash
python tools/serp_scraper.py \
  --mode trends \
  --keywords-file ".tmp/{client}_keywords_for_trends.txt" \
  --output ".tmp/{client}_trends.json"
```

**What this does:**
- Validates which keywords are rising vs declining in interest
- Flags seasonal keywords with peak months
- Returns trend direction for each keyword

**Validate output:**
```bash
# Check file exists
if [ ! -f ".tmp/{client}_trends.json" ]; then
  echo "[WARNING] Trends analysis failed (non-critical)"
  # Fallback: Skip trends, proceed with keywords
fi
```

**Parse results:**
```json
{
  "keywords": [
    {
      "keyword": "project management software",
      "trend": "stable",
      "direction": "flat",
      "seasonality": null
    },
    {
      "keyword": "remote work tools",
      "trend": "rising",
      "direction": "up",
      "growth_rate": "+15%"
    },
    {
      "keyword": "office management software",
      "trend": "declining",
      "direction": "down",
      "decline_rate": "-8%"
    }
  ]
}
```

**If trends fail:**
- This is non-critical, proceed without trend data
- Label all keywords as "trend: unknown" in final output
- Note: "[WARNING] Trend data unavailable, prioritizing by volume only"

---

### Step 4: Competitor Keyword Gap Analysis (Optional)

**Only if:** Client has competitors defined in brand_kit.json

**Tool:** `competitor_gap.py`

**Execute:**
```bash
python tools/competitor_gap.py \
  --client "{client}" \
  --output ".tmp/{client}_competitor_keywords.json"
```

**What this does:**
- Finds keywords competitors rank for that client doesn't
- Adds these to the keyword pool
- Enriches research with competitive intelligence

**Validate output:**
```bash
# Check file exists (optional, not critical)
if [ ! -f ".tmp/{client}_competitor_keywords.json" ]; then
  echo "[WARNING] Competitor analysis skipped (no competitors defined or tool unavailable)"
  # Proceed without competitor keywords
fi
```

**If competitors not defined:**
- Skip this step
- Proceed with autosuggest keywords only

---

### Step 5: Filter & Cluster Keywords

**Step 5a: Filter Out Negative Keywords**

```python
# Pseudocode for filtering
all_keywords = load_autosuggest_keywords() + load_competitor_keywords()
negative_keywords = load_from_brand_kit("negative_keywords")

filtered_keywords = [
    kw for kw in all_keywords
    if not any(neg in kw.lower() for neg in negative_keywords)
]
```

**Step 5b: Assign Search Intent**

**Intent classification rules:**
- **Informational**: Contains "how", "what", "why", "guide", "tips", "tutorial", "learn"
- **Commercial**: Contains "best", "top", "review", "vs", "compare", "alternative"
- **Transactional**: Contains "buy", "price", "cost", "hire", "get", "book", "order"
- **Navigational**: Contains brand names or specific product names

**Step 5c: Estimate Difficulty (Without Paid Tools)**

**Method:** Search Google for each keyword, analyze SERP:
1. Count total results (> 100M = High, 10M-100M = Medium, < 10M = Low)
2. Check page 1 domains (8+ big brands = High, 4-7 = Medium, < 4 = Low)
3. Combine scores

**Difficulty levels:**
- **Low**: Easy to rank (low competition, weak domains on page 1)
- **Medium**: Moderate competition (mix of strong/weak domains)
- **High**: Very competitive (dominated by high-DA sites)

**Step 5d: ML-Powered Clustering**

**Tool:** `keyword_clusterer.py`

**Prepare input:**
```bash
# Create text file with filtered keywords (one per line)
Write: .tmp/{client}_filtered_keywords.txt
```

**Execute:**
```bash
python tools/keyword_clusterer.py \
  --input ".tmp/{client}_filtered_keywords.txt" \
  --output ".tmp/{client}_keyword_clusters.json"
```

**What this does:**
- Uses NLP/ML (TF-IDF + cosine similarity)
- Groups semantically related keywords into topical clusters
- Assigns cluster names based on dominant terms

**Validate output:**
```bash
# Check file exists
if [ ! -f ".tmp/{client}_keyword_clusters.json" ]; then
  echo "[ERROR] Clustering failed"
  # Fallback: Manual grouping by first word
fi
```

**Parse results:**
```json
{
  "clusters": [
    {
      "cluster_name": "Project Management Tools",
      "keywords": [
        {"keyword": "best project management software", "intent": "commercial", "difficulty": "medium", "trend": "stable"},
        {"keyword": "project management tools for teams", "intent": "commercial", "difficulty": "low", "trend": "rising"}
      ],
      "keyword_count": 45,
      "avg_difficulty": "medium",
      "dominant_intent": "commercial"
    },
    {
      "cluster_name": "Project Management Guide",
      "keywords": [
        {"keyword": "how to manage projects", "intent": "informational", "difficulty": "low", "trend": "stable"},
        {"keyword": "project management tutorial", "intent": "informational", "difficulty": "low", "trend": "stable"}
      ],
      "keyword_count": 32,
      "avg_difficulty": "low",
      "dominant_intent": "informational"
    }
  ]
}
```

**If clustering fails:**
- Fallback: Group keywords manually by first 2 words
- Example: "best project ..." → "Project Management Tools" cluster
- Continue with manual clusters

---

### Step 6: Present Results to User

**Output in chat:**

```markdown
[OK] Keyword Research Complete: {client_name}

 Seed Keyword: "{seed_keyword}"
 Target Location: {location}
 Depth: {broad|deep}

---

 RESULTS SUMMARY:

  • Total keywords discovered: {total}
  • Filtered out (negatives): {filtered_count}
  • Final keyword pool: {final_count}
  • Grouped into {N} topical clusters

---

TOP 5 TOPICAL CLUSTERS:

**Cluster 1: {cluster_name}**
  • Keywords: {count}
  • Dominant intent: {intent}
  • Avg difficulty: {difficulty}
  • Top 3 keywords:
    1. {keyword} — {intent}, {difficulty}, {trend}
    2. {keyword} — {intent}, {difficulty}, {trend}
    3. {keyword} — {intent}, {difficulty}, {trend}

**Cluster 2: {cluster_name}**
  • Keywords: {count}
  • Dominant intent: {intent}
  • Avg difficulty: {difficulty}
  • Top 3 keywords:
    1. {keyword} — {intent}, {difficulty}, {trend}
    2. {keyword} — {intent}, {difficulty}, {trend}
    3. {keyword} — {intent}, {difficulty}, {trend}

**Cluster 3: {cluster_name}**
  [... same format ...]

**Cluster 4: {cluster_name}**
  [... same format ...]

**Cluster 5: {cluster_name}**
  [... same format ...]

---

 RECOMMENDED CONTENT STRATEGY:

Priority 1: {Cluster with most low-difficulty commercial keywords}
Priority 2: {Cluster with highest volume informational keywords}
Priority 3: {Cluster with rising trend keywords}

---

 Full data saved to:
  • .tmp/{client}_autosuggest.json
  • .tmp/{client}_trends.json
  • .tmp/{client}_keyword_clusters.json

---

 Next Steps:

Would you like me to:
1. Generate a Content Brief for Cluster 1? (Recommended)
2. Export this to Google Sheets for the client?
3. Make changes to the keyword list or clustering?
```

---

### Step 7: Save Results (After User Approval)

**If user approves:**

**Execute:**
```bash
# Save approved clusters to client folder
Write: clients/{client}/active_campaigns/keyword_research_{date}.json

# Also save as readable Markdown
Write: clients/{client}/active_campaigns/keyword_research_{date}.md
```

**Validate:**
```bash
# Check both files saved successfully
if [ ! -f "clients/{client}/active_campaigns/keyword_research_{date}.json" ]; then
  echo "[ERROR] Failed to save keyword research"
  # Retry once
fi
```

**Notify user:**
```
[OK] Keyword research saved to:
  • clients/{client}/active_campaigns/keyword_research_{date}.json
  • clients/{client}/active_campaigns/keyword_research_{date}.md

Next steps:
1. Run /content_brief {client} "{top_keyword}" to create a content plan
2. Run /competitor_gap {client} to find more opportunities
3. Or: Edit the keywords manually and re-run clustering
```

---

## Error Handling & Fallback Logic

**If autosuggest scraping fails (429 rate limit):**
1. Wait 30 seconds
2. Retry once with 10-second delay between A-Z requests
3. If still fails: Use WebSearch "{seed_keyword}" and extract related queries manually
4. Document: "[WARNING] Autosuggest unavailable, used manual keyword expansion"

**If < 10 keywords found:**
1. Automatically broaden search with 3 related seed keywords
2. Example: "project management" → Try: "team management", "task management", "workflow software"
3. Combine results
4. If still < 10: Inform user seed keyword may be too niche

**If trends analysis fails:**
- Non-critical, proceed without trend data
- Label all keywords as "trend: unknown"
- Note in output: "[WARNING] Trend data unavailable"

**If competitor analysis fails:**
- Optional feature, skip if unavailable
- Proceed with autosuggest keywords only

**If clustering fails:**
- Fallback: Manual grouping by first 2 words
- Example: "best X" cluster, "how to X" cluster
- Continue with manual clusters

**If no negative_keywords defined:**
- Proceed with full keyword list
- May include competitor brand names (flag these manually)

---

## Expected Outputs

**Files Created:**
- `.tmp/{client}_autosuggest.json` — Raw autosuggest results
- `.tmp/{client}_keywords_for_trends.txt` — Keywords for trend analysis
- `.tmp/{client}_trends.json` — Trend direction per keyword (optional)
- `.tmp/{client}_competitor_keywords.json` — Competitor gap keywords (optional)
- `.tmp/{client}_filtered_keywords.txt` — Keywords after filtering
- `.tmp/{client}_keyword_clusters.json` — **ML-grouped clusters**
- `clients/{client}/active_campaigns/keyword_research_{date}.json` — **Final saved research**
- `clients/{client}/active_campaigns/keyword_research_{date}.md` — **User-readable format**

**User-Facing Deliverable:**
Formatted cluster analysis in chat + 2 saved files (JSON + Markdown)

**Next Action:**
User chooses: (1) Content brief for top cluster, (2) Export to Sheets, (3) Make changes

---

## Quality Gates

**Before presenting results:**
- [ ] Minimum 10 keywords found (or explain why fewer is OK)
- [ ] All keywords have intent labels (informational/commercial/transactional/navigational)
- [ ] All keywords have difficulty estimates (low/medium/high)
- [ ] Negative keywords filtered out (no competitor brand names unless intentional)
- [ ] Clusters are semantically meaningful (not random groupings)
- [ ] Top 5 clusters clearly identified and prioritized
- [ ] Each cluster shows keyword count + avg difficulty + dominant intent
- [ ] Clear content strategy recommendation provided

---

## Edge Cases

**Scenario: Seed keyword is too niche (< 10 results)**
- Broaden automatically with 3 related keywords
- Combine results
- If still < 10: Inform user and suggest broader seed

**Scenario: All keywords are "High" difficulty**
- Inform user: Seed is very competitive
- Recommend: Target long-tail variations (4+ word phrases)
- Or: Focus on informational content first, build authority

**Scenario: Negative keywords list is extensive**
- May filter out 50%+ of keywords
- This is OK if avoiding competitor brands
- Ensure final pool still has 20+ keywords

**Scenario: Competitor analysis returns 0 gaps**
- Means client ranks well vs competitors already
- This is good news
- Recommend: Focus on content depth vs new keywords

**Scenario: Rate limiting on multiple retries**
- Switch to manual keyword brainstorming
- Ask user: "Based on {seed_keyword}, what topics should we cover?"
- Continue workflow with manual list

**Scenario: --depth deep generates 1,000+ keywords**
- This is expected for deep research
- Clustering will organize them
- Filter to top 200 by priority (low difficulty + high intent match)

---

## Related Workflows

- `/competitor_gap` — Find keywords competitors rank for
- `/content_brief` — Generate brief for selected keyword
- `/audit` — Technical audit before content creation
- `/content_draft` — Write article from keyword research

---

## Notes

**Depth Recommendations:**
- **Broad** (100-200 keywords): Fast, good for initial research, 1 content pillar
- **Deep** (500+ keywords): Comprehensive, good for 6-12 month content calendar, multiple pillars

**Search Intent Matters:**
- **Informational**: Blog posts, guides, tutorials (awareness stage)
- **Commercial**: Comparison posts, "best X" listicles (consideration stage)
- **Transactional**: Pricing pages, product pages (decision stage)
- **Navigational**: Brand pages, product-specific pages

**Why Clustering Matters:**
Instead of 200 random keywords, you get 8-12 themed content clusters. Each cluster becomes a content pillar that ranks for 15-25 related keywords with one comprehensive guide.

**Difficulty Without Paid Tools:**
We estimate difficulty by:
1. SERP result count (proxy for competition)
2. Domain authority of page 1 results (detected from site age/brand recognition)
3. Intent match (if SERPs show e-commerce when you're a blog, difficulty increases)

This is 70-80% accurate vs paid tools like Ahrefs/SEMrush.
