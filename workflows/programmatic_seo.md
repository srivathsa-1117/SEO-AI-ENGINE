---
description: /programmatic_seo - Generate architecture for 50+ unique location or category pages safely
---

# Workflow: Programmatic SEO 2.0 (2026 Standards)

## Trigger
```
/programmatic_seo <client_name>
```

## Objective
Design the schema, content template, and URL structure for building scalable programmatic SEO pages (e.g., location pages, feature vs. feature pages, directory listings) **without triggering Google's Helpful Content Update (HCU) penalties**.

In 2026, Google aggressively penalizes "doorway pages" where only a single variable (like City Name or Competitor Name) is swapped out in a template. Programmatic SEO is no longer about generating thousands of pages; it is about generating *high-value* pages at scale using rich datasets.

## Tools Used in This Workflow
- **`tools/programmatic_quality_scorer.py`** - Analyzes boilerplate ratio, unique variables, and content depth across programmatic pages to prevent Google penalties
- **`tools/indexing_monitor.py`** - Monitors Google Search Console indexing status for bulk-generated pages to detect quality issues early
- **`tools/schema_gen.py`** - Generates dynamic structured data for each programmatic page variant

---

## CRITICAL AWARENESS: RULE 10 (QUALITY GATES)
You MUST enforce **Rule 10 (Quality Gates)** during this workflow. Your job is to ensure the architecture relies on **unique, database-driven value**.

Never allow the user to create a programmatic structure that simply swaps `[City_Name]`. You must act as a strict gatekeeper against low-quality, thin programmatic content.

---

## The 6-Step Programmatic Process

### Step 1: Strategy & Definition
Determine what the user is trying to programmatically build.
Common programmatic architectures:
1. **Location Pages**: Service + City (e.g., "Plumbers in Austin")
2. **Comparison/Alternative Pages**: Product vs. Competitor (e.g., "Mailchimp Alternatives")
3. **Integration Pages**: Product + Tool (e.g., "Slack Integration for Jira")
4. **Glossary/Definition Pages**: Industry terms
5. **Directory/Aggregator Pages**: List of entities in a category

**Action**: Ask the user to define the exact page type and the target audience intent. 

### Step 2: Ensure the 60% Unique Rule (The "3-Variable Minimum")
Once the target is known, design a **Database Schema** that ensures >60% of the page content will be entirely unique to that specific URL. 

**NEW STRICT REGULATION:** You MUST demand the user provides a dataset with at least **3 distinct, real-world semantic variables** per page. If they cannot, you must REFUSE to generate the architecture.

**BAD (Spam / Hard Refusal):**
- Variables: `[City]` only.
- Content: "We are the best plumber in [City]. Call us today for plumbing in [City]."

**GOOD (Helpful Content / Approved):**
- Variables: `[City_Name]`, `[Local_Landmarks]`, `[City_Specific_Regulations]`, `[Local_Team_Member_Profile]`, `[Specific_Completed_Jobs_In_City]`, `[City_Reviews]`. (At least 3 are required).

Present the required database variables to the user. Tell them: *"To safely generate these pages without Google Helpful Content penalties, I require a dataset containing a minimum of 3 specific unique variables per page. Please confirm you can source this data."*

### Step 3: Design the Content Template
Draft a markdown skeleton for how the programmatic page will look.
Include sections that pull from the database variables defined in Step 2.

The template must include:
- A unique H1 combining the core offering and localized/variable constraint.
- An introductory paragraph that is algorithmically spun or deeply reliant on specific data points (using spinning/spintax logic if necessary to avoid standard boilerplate).
- A structured data table or listicle that injects 3+ data points.
- Original FAQs specific to the variable (NOT generic FAQs).
- Schema.org JSON-LD tailored to the programmatic type.

### Step 4: Quality Gate Enforcement (Using the Scorer)
Before finalizing the blueprint, you must run a simulated test using `tools/programmatic_quality_scorer.py`.

**Ask the user: "Please provide 3-5 sample URLs from your programmatic pages (or generate test pages first)."**

**Run the quality scorer:**
```bash
python tools/programmatic_quality_scorer.py --urls sample_urls.txt --output quality_report.json
```

**Or if you have a sitemap:**
```bash
python tools/programmatic_quality_scorer.py --sitemap https://client.com/sitemap-programmatic.xml --sample 20 --output quality_report.json
```

**Interpret the results:**
- **Score ≥70**: PASS - Safe to publish
- **Score 50-69**: WARNING - Review recommendations, test with small batch first
- **Score <50**: FAIL - Do NOT publish, revise template to add more unique variables

If the baseline boilerplate ratio exceeds 40%, you must revise the template to be shorter or demand more variables from the user.

### Step 5: Indexing and Rollout Strategy
Ask the user: **"How many of these pages are you planning to generate?"**

- If **< 30**: "Looks safe. Proceed with building the database."
- If **30 - 50**: "[WARNING] You are approaching the threshold for doorway page penalties. Ensure your database variables provide genuine unique value."
- If **> 50**: "HARD STOP: Launching 50+ programmatic pages simultaneously without authority is highly risky. We must use a phased rollout."

**Phased Rollout Protocol:**
1. Generate and publish Batch 1 (10 pages).
2. Wait 7-14 days.
3. Run `tools/indexing_monitor.py` to check Search Console.
   ```bash
   python tools/indexing_monitor.py --property "https://client.com/" --url-list batch1_urls.txt
   ```
4. If "Crawled - currently not indexed" > 20%, STOP. The content is considered thin. Return to Step 2.
5. If "Submitted and indexed" > 80%, proceed to Batch 2.

### Step 6: Output Generation
If the user passes the quality gates, save the following to `clients/<client_name>/active_campaigns/programmatic_blueprint.md`:
1. The finalized Database Schema (CSV headers).
2. The Content Template (with `{{variable}}` brackets).
3. The Internal Linking logic (how these pages will be found from the homepage/sitemap).
4. The Phased Rollout Schedule.

---

## Deep Dive: Programmatic Database Construction

To succeed in 2026, the database (CSV/JSON) needs to be deep. Here is how to instruct the user to build it.

### Example: SaaS Integration Pages
If a SaaS company wants integration pages.
*Bad Data:* `[Integration_Name]`
*Good Data Schema:*
- `integration_name`: (e.g., Salesforce)
- `category`: (e.g., CRM)
- `setup_time_minutes`: (e.g., 5)
- `top_use_case`: (e.g., Syncing deal stages with marketing emails)
- `required_permissions`: (e.g., Read/Write Contacts)
- `api_limits`: (e.g., 10,000 calls/day)
- `data_sync_frequency`: (e.g., Real-time)

### Example: Local Service Pages
If a plumber wants city pages.
*Bad Data:* `[City_Name]`
*Good Data Schema:*
- `city_name`: (e.g., Austin)
- `county`: (e.g., Travis County)
- `local_water_hardness`: (e.g., 200 ppm - Very Hard)
- `common_local_issue`: (e.g., Limescale buildup in pipes)
- `building_code_quirk`: (e.g., Requires thermal expansion tanks for all new water heaters)
- `local_tech_name`: (e.g., Mike T.)
- `recent_job_neighborhood`: (e.g., East Austin)

---

## Technical Implementation Details

### Internal Linking Automation
Programmatic pages fail if they are "orphan pages". The blueprint must specify how users and bots find the pages.
- **HTML Sitemaps**: A structured `/integrations/` or `/locations/` index page.
- **Faceted Navigation**: Filterable lists.
- **In-Content Links**: Related pages (e.g., "See also: Plumbers in [Neighboring_City]").

### Dynamic Schema Generation
Every programmatic page needs unique structured data.
- **Location Pages**: `LocalBusiness` or `Service` schema.
- **Integration Pages**: `SoftwareApplication` schema.
- **VS Pages**: `Article` or `ItemList` schema.

Ensure the generator script calls `schema_gen.py` dynamically for each page.

---

## Using the Programmatic Quality Scorer

The `programmatic_quality_scorer.py` is your primary defense line.
It checks:
1. **Unique Word Count** (Must be > 300)
2. **Boilerplate Ratio** (Must be < 40%)
3. **Data Depth** (Must have > 5 specific data points injected)

When reviewing a sample, you must enforce the scorer's recommendations. If the script outputs `is_safe_to_publish: false`, you CANNOT proceed with full generation.

### Fixing a Failing Score
If the boilerplate ratio is too high (e.g., 70% template, 30% unique data):
1. **Add More Variables**: The easiest fix.
2. **Use Conditional Logic**: Introduce `{% if %}` statements in the templating language (Jinja2, Handlebars) to completely hide/show sections based on the data.
3. **Spin the Boilerplate**: Create 3-5 variations of the introductory and concluding paragraphs and randomly select them during generation.

---

## Using the Indexing Monitor

The `indexing_monitor.py` script connects to the Google Search Console API.
It allows you to batch-check the precise indexing status of programmatic URLs.

### Interpreting GSC Statuses

**1. Submitted and indexed**
- **Meaning**: Google accepted the page.
- **Action**: Excellent. Keep generating with this template.

**2. Crawled - currently not indexed**
- **Meaning**: DANGER. Google evaluated the page and determined it adds no value to the internet. This is a direct quality penalty.
- **Action**: STOP GENERATION IMMEDIATELY. You have hit the doorway page filter. You must add more unique variables and rewrite the template to lower the boilerplate ratio before continuing.

**3. Discovered - currently not indexed**
- **Meaning**: WARNING. Google knows the URL exists but hasn't bothered to crawl it yet. This usually indicates a crawl budget issue or poor internal linking.
- **Action**: Do not generate more pages yet. Improve internal linking to the existing pages. Build high-quality tier-2 links to the programmatic hub index.

---

## Edge Cases

### The "I have no data" Client
If the user says "I don't have this data, I just want the pages":
**Response**: Refuse. Explain that without unique data, the pages will be classified as Spam under Google's 2024-2026 guidelines, risking a manual action or algorithmic suppression of the *entire domain*. Suggest scraping data via APIs, using Hunter/Clearbit, or manually researching a small batch of 10 pages instead of automating 100 empty ones.

### E-commerce Category Bloat
E-commerce sites often programmatically generate thousands of filter combinations (e.g., `shoes > red > size 10 > nike`).
**Action**: Implement strict `robots.txt` disallows or `noindex` tags for pages with < 3 products, or pages with 3+ overlapping filters. Only allow indexation for primary high-volume intersections.

### Multi-Language / Hreflang Automation
If the programmatic campaign spans multiple regions (e.g., `/en-us/`, `/en-gb/`):
**Action**: Ensure exact identical content isn't published across regions. Force localization of currency, spelling (color vs colour), and local contact info.

---

## Final Review Checklist
Before marking the programmatic blueprint as complete, verify:
- [ ] At least 3 specific semantic variables are defined.
- [ ] Boilerplate ratio is estimated < 40%.
- [ ] Internal linking path is mapped.
- [ ] Phased rollout batch schedule is documented.
- [ ] Dynamic schema is specified.
- [ ] Quality scorer and Indexing monitor have been explained to the user.
