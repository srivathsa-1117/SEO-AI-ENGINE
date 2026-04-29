---
description: /competitor_gap - Find low-hanging fruit keywords that competitors rank for but the client doesn't, with ML-powered clustering
---

# Workflow: Competitor Keyword Gap Analysis

## Trigger
```
/competitor_gap <client_name>
```
**Example:** `/competitor_gap exampleclient`

---

## Objective
Identify high-value, "low-hanging fruit" keywords where top competitors are getting organic traffic, but the client's website does not currently rank in the top 100 results. Cluster these keywords by topic using ML to build a strategic content calendar.

---

## When to Use
Use this in Month 2+ of a client engagement to build the content calendar. It removes guesswork by writing content the market is actively searching for.

---

## Step-by-Step Execution

### Step 1: Load Client Context & Competitors

**Execute:**
```bash
# Read brand kit
Read: clients/{client}/brand_kit.json
```

**Extract required fields:**
```json
{
  "website_url": "https://client-domain.com",
  "competitors": [
    "https://competitor1.com",
    "https://competitor2.com",
    "https://competitor3.com"
  ],
  "primary_keywords": ["keyword1", "keyword2"],
  "target_locations": ["city/region"]
}
```

**Validate:**
```bash
# Check if client exists
if [ ! -f "clients/{client}/brand_kit.json" ]; then
  echo "[ERROR] Client not found. Run /add_client first."
  exit 1
fi

# Check if competitors array has at least 2 items
# Use Read tool to parse JSON
```

**If no competitors are listed:**
Ask user:
```
[WARNING] No competitors found in brand_kit.json

I need at least 2 competitor URLs to run a gap analysis.
Who are {client}'s main organic search competitors?

Example:
- competitor1.com
- competitor2.com
```

Then update `clients/{client}/brand_kit.json` with competitors array.

---

### Step 2: Run Competitor Gap Analysis

**Tool:** `competitor_gap.py`

**Execute:**
```bash
python tools/competitor_gap.py \
  --client "{client}" \
  --output ".tmp/{client}_competitor_gap.json"
```

**What this does:**
- Reads client URL and competitors from brand_kit.json
- For each competitor, identifies keywords they rank for (top 20 positions)
- Checks if client ranks for those same keywords
- Filters for "gap keywords" where client is not in top 100
- Estimates difficulty, volume, and value
- Returns JSON with low-hanging fruit opportunities

**Validate output:**
```bash
# Check file exists
if [ ! -f ".tmp/{client}_competitor_gap.json" ]; then
  echo "[ERROR] Competitor gap analysis failed"
  # Fallback: Manual SERP research
fi

# Check has minimum 1 keyword
# Use Read tool to parse JSON:
# if len(data["keywords"]) < 1:
#   May indicate no gap exists (client already ranks well)
```

**Parse results:**
```json
{
  "client": "{client_name}",
  "client_url": "https://client-domain.com",
  "competitors_analyzed": ["competitor1.com", "competitor2.com"],
  "gap_keywords": [
    {
      "keyword": "best CRM for real estate agents",
      "monthly_volume": 1200,
      "difficulty": "Medium",
      "competitor_ranking": 3,
      "competitor_url": "https://competitor1.com/article",
      "client_ranking": null,
      "opportunity_score": 85
    },
    ...
  ],
  "total_gaps_found": 127
}
```

**If tool fails:**
1. **Fallback method:** Manual SERP research
   - For each primary_keyword from brand_kit, search Google using WebSearch
   - Note which competitors appear in top 10
   - Extract their target keywords from title tags
   - Manually check if client ranks for those keywords
2. **Document:** "[WARNING] Automated gap analysis unavailable, used manual research for top {N} keywords"

**If zero keywords found:**
- This can happen if client already ranks well vs competitors
- Inform user: "[OK] No major gaps found — client ranks competitively against these competitors"
- Recommend: Expand competitor list OR focus on content depth vs new keywords

---

### Step 3: Filter & Prioritize — Low-Hanging Fruit Only

**Apply filters:**

**Volume filter:**
- Minimum: 100 monthly searches (ignore ultra-long-tail)
- Maximum: No limit (even high-volume is valuable if competitor ranks)

**Difficulty filter:**
- **Low-hanging fruit** = Difficulty "Low" or "Medium"
- Exclude "High" difficulty (requires too much authority to rank)

**Opportunity score calculation:**
```python
opportunity_score = (
    (monthly_volume / 100) * 0.4 +  # Volume weight
    (100 - difficulty) * 0.3 +       # Difficulty weight (inverse)
    (competitor_position <= 5 ? 30 : 20) * 0.3  # Competitor strength
)
```

**Sort by opportunity_score descending**

**Select top 50 keywords** for clustering

---

### Step 4: Topic Clustering (ML-Powered)

**Tool:** `keyword_clusterer.py`

**Prepare input file:**
```bash
# Extract keywords from gap analysis JSON
# Write to text file (one keyword per line)
# Use Read tool to parse JSON, then Write to create text file

Write: .tmp/{client}_keywords_to_cluster.txt
```

**Content:**
```
best CRM for real estate agents
real estate CRM software
CRM for property managers
real estate lead management
...
```

**Execute:**
```bash
python tools/keyword_clusterer.py \
  --input ".tmp/{client}_keywords_to_cluster.txt" \
  --output ".tmp/{client}_clusters.json"
```

**What this does:**
- Uses NLP/ML (TF-IDF + cosine similarity) to group semantically related keywords
- Creates topical clusters (e.g., all "real estate" keywords together, all "CRM features" together)
- Assigns cluster names based on dominant terms

**Validate output:**
```bash
# Check file exists
if [ ! -f ".tmp/{client}_clusters.json" ]; then
  echo "[ERROR] Clustering failed"
  # Fallback: Manual grouping by first word
fi

# Check has at least 1 cluster
```

**Parse results:**
```json
{
  "clusters": [
    {
      "cluster_name": "Real Estate CRM Software",
      "keywords": [
        "best CRM for real estate agents",
        "real estate CRM software",
        "CRM for property managers"
      ],
      "keyword_count": 15,
      "total_monthly_volume": 8400,
      "avg_difficulty": "Medium"
    },
    {
      "cluster_name": "CRM Features & Integrations",
      "keywords": [
        "CRM with email automation",
        "CRM Zapier integration",
        "CRM mobile app"
      ],
      "keyword_count": 12,
      "total_monthly_volume": 3200,
      "avg_difficulty": "Low"
    }
  ]
}
```

**If clustering fails:**
- Fallback: Group keywords manually by first 2 words
- Example: "best CRM ..." → "CRM Software" cluster
- Document: "[WARNING] ML clustering unavailable, used manual grouping"

---

### Step 5: Present Findings to User

**Output in chat:**

```markdown
[OK] Competitor Gap Analysis Complete: {client_name}

Analyzed:
  • Client: {client_url}
  • Competitors: {comp1}, {comp2}, {comp3}

Results:
  • Total gap keywords found: {total}
  • Low-hanging fruit (Low/Medium difficulty): {count}
  • Grouped into {N} topical clusters

---

TOP 3 TOPICAL CLUSTERS TO TARGET:

**Cluster 1: {cluster_name}**
  • Keywords: {count}
  • Total monthly volume: {volume}
  • Avg difficulty: {difficulty}
  • Top keywords:
    1. {keyword} — {volume}/mo, {difficulty}
    2. {keyword} — {volume}/mo, {difficulty}
    3. {keyword} — {volume}/mo, {difficulty}

**Cluster 2: {cluster_name}**
  • Keywords: {count}
  • Total monthly volume: {volume}
  • Avg difficulty: {difficulty}
  • Top keywords:
    1. {keyword} — {volume}/mo, {difficulty}
    2. {keyword} — {volume}/mo, {difficulty}
    3. {keyword} — {volume}/mo, {difficulty}

**Cluster 3: {cluster_name}**
  • Keywords: {count}
  • Total monthly volume: {volume}
  • Avg difficulty: {difficulty}
  • Top keywords:
    1. {keyword} — {volume}/mo, {difficulty}
    2. {keyword} — {volume}/mo, {difficulty}
    3. {keyword} — {volume}/mo, {difficulty}

---

Full data saved to:
  • .tmp/{client}_competitor_gap.json
  • .tmp/{client}_clusters.json

---

Next Steps:

Would you like me to:
1. Generate a Content Brief for Cluster 1? (Recommended)
2. Save this to a Google Sheet for the client?
3. Create a 90-day content calendar based on these clusters?
```

---

### Step 6: Save Results (After User Decision)

**If user approves:**

**Option A: Save as Markdown report**
```bash
Write: clients/{client}/reports/competitor_gap_{date}.md
```

**Option B: Save as JSON for programmatic use**
```bash
# Already saved to .tmp/, copy to permanent location
Write: clients/{client}/data/competitor_gap_{date}.json
```

**Option C: Generate Content Brief for top cluster**
```
Trigger: /content_brief {client} "{top_keyword_from_cluster_1}"
```

---

## Error Handling & Fallback Logic

**If competitor_gap.py fails:**
1. Check if `clients/{client}/brand_kit.json` has valid competitors array
2. Retry once after 10-second delay (may be transient network issue)
3. **Fallback:** Manual SERP research
   - For each primary_keyword, WebSearch to see who ranks
   - Extract keywords from competitor title tags
   - Manually check if client ranks (use WebSearch "site:{client_url} {keyword}")
4. Document: "[WARNING] Automated tool unavailable, used manual research"

**If keyword_clusterer.py fails:**
1. **Fallback:** Manual grouping
   - Group keywords by first 2 words
   - Example: "best CRM" cluster, "CRM features" cluster
2. Continue with manually grouped clusters

**If no gap keywords found:**
- This means client already ranks competitively
- Inform user: "[OK] No major gaps found. Client has good keyword coverage vs competitors."
- **Recommend:**
  - Expand competitor list to include larger players
  - OR: Focus on content depth (improve existing rankings from position 5 → 1)
  - OR: Target adjacent markets (if SaaS, expand to new industries)

**If competitors array is empty:**
- Ask user to provide competitors
- Cannot proceed without competitor data
- Never guess competitors

---

## Expected Outputs

**Files Created:**
- `.tmp/{client}_competitor_gap.json` — Full gap analysis data
- `.tmp/{client}_keywords_to_cluster.txt` — Keyword list for clustering
- `.tmp/{client}_clusters.json` — ML-grouped topical clusters
- `clients/{client}/reports/competitor_gap_{date}.md` — **User-facing report** (optional)

**User-Facing Deliverable:**
Formatted cluster analysis in chat + saved JSON/Markdown files

**Next Action:**
User chooses: (1) Content brief for top cluster, (2) Save to Google Sheet, (3) Create content calendar

---

## Quality Gates

**Before presenting results:**
- [ ] Minimum 1 gap keyword found (or explain why zero is OK)
- [ ] All keywords have volume + difficulty estimates
- [ ] Clusters are semantically meaningful (not random groupings)
- [ ] Top 3 clusters clearly identified and prioritized
- [ ] Each cluster shows total volume + avg difficulty
- [ ] Clear next action recommended (content brief for Cluster 1)

---

## Edge Cases

**Scenario: No gap keywords found**
- Means client already ranks competitively
- Inform user this is good news
- Recommend: content depth vs breadth (improve position 5 → 1)

**Scenario: All gaps are "High" difficulty**
- Filter them out (not low-hanging fruit)
- Inform user: "Gaps exist but require high authority to rank"
- Recommend: build authority first with easier keywords

**Scenario: Competitors in different language/region**
- Gap analysis may return irrelevant keywords
- Flag to user: "[WARNING] Competitor {X} appears to target {language/region}, filtering results"
- Filter by target_locations from brand_kit

**Scenario: Competitor has 10,000+ ranking keywords**
- Tool may time out trying to analyze all
- Limit analysis to top 500 keywords per competitor
- Document: "Analyzed top 500 keywords per competitor (full analysis would take 2+ hours)"

**Scenario: Zero keywords for strictly local brick-and-mortar stores**
- Inform user: "Competitor Gap is the wrong strategy for this client"
- Recommend: Local SEO and Google Business Profile (GBP) posting instead

---

## Related Workflows

- `/keyword_research` — Discover new keywords (not just gaps)
- `/content_brief` — Generate brief for gap keyword
- `/audit` — Technical audit before content creation
- `/monthly_report` — Track gap closure over time

---

## Notes

**This workflow is strategic:**
- Focuses on winnable battles (low-hanging fruit only)
- Uses ML to find content themes (not just random keywords)
- Removes guesswork from content calendar planning

**Low-hanging fruit definition:**
- Competitor ranks in top 20
- Client does not rank in top 100
- Difficulty is "Low" or "Medium"
- Monthly volume ≥ 100 searches

**Why clustering matters:**
Instead of 50 random keyword targets, you get 5-10 themed content pillars. Each pillar can become a comprehensive guide that ranks for 10-15 related keywords.
