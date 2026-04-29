---
description: /brand_monitor - Brand health monitoring workflow for AI Search
---

# Workflow: Brand Monitoring & Social Proof (2026 Standards)

## Trigger
```
/brand_monitor <client_name>
```

## Objective
Monitor and aggregate high-quality brand mentions and reviews across the web. Brand signals (social proof, unlinked mentions on authority sites, review velocity) are now weighted heavier than traditional backlinks for AI search engines (AEO/GEO) and Google's entity graph.

## Tools Used in This Workflow
- **`tools/brand_mention_tracker.py`** - Discovers brand mentions across the web using Brave Search API, excluding the brand's own domain
- **`tools/review_aggregator.py`** - Aggregates and analyzes reviews from Google Business Profile and other review platforms
- **`tools/entity_auditor.py`** - Checks brand entity strength in Knowledge Graph (related to brand authority)

## Success Metrics
- **Tier-1 Mentions:** ≥3 new mentions per month on Reddit, Quora, News, or GitHub
- **Review Velocity:** ≥5 new reviews per month (local businesses) or ≥10/month (SaaS)
- **Sentiment Ratio:** ≥85% positive sentiment
- **Unlinked Mention Conversion:** Convert ≥30% of unlinked mentions to actual backlinks within 90 days
- **AI Citation Rate:** Brand appears in ≥20% of relevant AI search queries (ChatGPT, Perplexity)

---

## CRITICAL AWARENESS: BRAND PROMINENCE
In 2026, AI engines like Perplexity, ChatGPT, and Gemini use "Tier 1 Domain Mentions" (Reddit, Quora, News Media, GitHub) to determine if a brand is worth citing. If a client is not actively discussed on these platforms, they will not appear in LLM-generated answers.

---

## The 4-Step Brand Monitoring Process

### Step 1: Run the Brand Mention Tracker
Use the Brave Search API to find recent, unlinked, and linked brand mentions across the web, explicitly excluding the client's own domain. This identifies conversation velocity.

**Action**: Run `tools/brand_mention_tracker.py`:
```bash
python tools/brand_mention_tracker.py --brand "The Example Brand" --domain "example.com" --timeframe pw
```
Look for:
- Mentions on Tier-1 sites (Reddit, Quora).
- News coverage or PR placements.
- Negative mentions that require reputation management.

### Step 2: Run the Review Aggregator
Reviews are the ultimate trust signal for Local and SaaS SEO. Google Places reviews dictate Map Pack rankings and are frequently quoted by Gemini.

**Action**: Run `tools/review_aggregator.py`:
```bash
python tools/review_aggregator.py --place-id "ChIJN1t_tDeuEmsRUsoyG83frY4"
```
Assess:
- Review velocity (Are they getting new reviews this month?).
- Sentiment percentage.
- Keywords frequently used in reviews (these must be added to the homepage copy to match search intent).

### Step 3: Analyze "Gap" Opportunities
Compare the data to the client's current PR strategy:
- Are there platforms (like Quora) where competitors are mentioned but the client is not?
- Is there a severe lack of Reddit threads discussing the client's niche?
- Do the reviews mention a specific problem (e.g., "slow support") that threatens conversion rates?

**Run competitive brand mention analysis:**
```bash
# Track client
python tools/brand_mention_tracker.py --brand "Client Brand" --domain "client.com" --timeframe pm --output .tmp/client_mentions.json

# Track top 3 competitors
python tools/brand_mention_tracker.py --brand "Competitor 1" --domain "competitor1.com" --timeframe pm --output .tmp/comp1_mentions.json
python tools/brand_mention_tracker.py --brand "Competitor 2" --domain "competitor2.com" --timeframe pm --output .tmp/comp2_mentions.json
python tools/brand_mention_tracker.py --brand "Competitor 3" --domain "competitor3.com" --timeframe pm --output .tmp/comp3_mentions.json
```

**Compare metrics:**
- Total mentions (client vs competitors)
- Tier-1 mentions (Reddit, Quora, News)
- Platforms where client is absent but competitors are present
- Content themes in competitor mentions (feature discussions, comparisons, problem-solving)

### Step 4: Identify Unlinked Mention Conversion Opportunities
Unlinked mentions are low-hanging fruit for link-building. Review the brand_mention_tracker output and prioritize outreach to:

**Priority 1: News/Media Mentions**
- Journalists often forget to link in articles
- Reach out via email: "Thank you for mentioning us! Here's our official press kit link for future reference."
- Conversion rate: ~60-70%

**Priority 2: Blog Posts & Listicles**
- "Top 10 CRM tools" articles that mention the client but don't link
- Reach out: "We noticed you mentioned [Brand] in your article. Would you like to link to our [specific feature page] for readers?"
- Conversion rate: ~40-50%

**Priority 3: Reddit/Quora Discussions**
- Cannot directly edit, but use these as PR intelligence
- Identify common questions being asked about the client's niche
- Create content that answers these questions, then naturally share in future discussions
- Indirect conversion (brand awareness boost)

**Outreach Template (Save to `clients/<client_name>/templates/unlinked_mention_outreach.md`):**
```markdown
Subject: Quick link request for [Article Title]

Hi [Author Name],

I noticed you mentioned [Client Brand] in your recent article "[Article Title]" – thank you!

Would you be open to linking to our [specific page URL]? It provides [specific value, e.g., "a detailed breakdown of how our X feature works" or "pricing comparisons"].

Here's the suggested anchor text: [Brand Name + Feature]

Appreciate your time!

Best,
[Your Name]
[Client Brand] Marketing Team
```

### Step 5: Review Velocity & Sentiment Analysis
Reviews directly impact:
- **Local SEO:** Google Business Profile ranking in Map Pack
- **AI Search:** ChatGPT & Perplexity cite review snippets as social proof
- **Conversion Rate:** 88% of consumers trust online reviews as much as personal recommendations (BrightLocal 2025)

**Analyze review patterns:**
```bash
python tools/review_aggregator.py --place-id "ChIJN1t_tDeuEmsRUsoyG83frY4" --output .tmp/client_reviews.json
```

**Review the output for:**
1. **Velocity Trends:**
   - Current month: X reviews
   - Previous month: Y reviews
   - Trend: Increasing ✅ / Declining ⚠️ / Flat ⚠️

2. **Sentiment Breakdown:**
   - Positive (4-5 stars): X%
   - Neutral (3 stars): Y%
   - Negative (1-2 stars): Z%
   - **Target:** ≥85% positive

3. **Common Keywords in Reviews:**
   - Extract top 10 most-used words/phrases
   - These are semantic signals Google/AI uses
   - **Action:** Add these exact phrases to homepage copy, service pages, and FAQs

4. **Response Rate:**
   - % of reviews with owner responses
   - **Target:** 100% (respond to ALL reviews within 24 hours)
   - Negative reviews with responses rank better than negatives ignored

### Step 6: Generate Brand Health Report
Generate a comprehensive markdown report inside `clients/<client_name>/reports/brand_health_report_YYYY_MM.md`.

**Report Template Structure:**

```markdown
# Brand Health Report — [Client Name]
**Report Date:** [YYYY-MM-DD]
**Reporting Period:** [Last 30/90 days]

---

## Executive Summary

**Overall Brand Health Score:** X/100

- **Tier-1 Mention Velocity:** [X mentions/month] (Target: ≥3)
- **Review Velocity:** [X reviews/month] (Target: ≥5 for local, ≥10 for SaaS)
- **Sentiment Ratio:** [X% positive] (Target: ≥85%)
- **Unlinked Mentions Found:** [X opportunities]
- **AI Citability:** [Low/Medium/High]

**Key Insight:** [One-sentence summary, e.g., "Brand is gaining traction on Reddit but needs more news coverage for AI search visibility."]

---

## 1. Brand Mentions Overview

### Total Mentions Discovered: [X]
- **Past 7 days:** [X]
- **Past 30 days:** [X]
- **Past 90 days:** [X]

### Platform Breakdown:
| Platform | Mentions | Tier-1? | Linked? |
|----------|----------|---------|---------|
| Reddit | [X] | Yes | [X unlinked] |
| Quora | [X] | Yes | [X unlinked] |
| News/Media | [X] | Yes | [X unlinked] |
| GitHub | [X] | Yes | N/A |
| LinkedIn | [X] | No | [X unlinked] |
| General Blogs | [X] | No | [X unlinked] |

### Top 5 Most Authoritative Mentions:
1. **[Platform]** - [Title](URL) - [Date] - [Linked/Unlinked]
2. **[Platform]** - [Title](URL) - [Date] - [Linked/Unlinked]
3. **[Platform]** - [Title](URL) - [Date] - [Linked/Unlinked]
4. **[Platform]** - [Title](URL) - [Date] - [Linked/Unlinked]
5. **[Platform]** - [Title](URL) - [Date] - [Linked/Unlinked]

---

## 2. Review Health Analysis

### Aggregate Stats:
- **Average Rating:** [X.X] / 5.0
- **Total Reviews:** [X]
- **New Reviews (This Period):** [X]
- **Review Velocity:** [X reviews/month]

### Sentiment Breakdown:
- **Positive (4-5 stars):** [X%] ([X reviews])
- **Neutral (3 stars):** [X%] ([X reviews])
- **Negative (1-2 stars):** [X%] ([X reviews])

### Common Review Keywords:
1. "[keyword 1]" - mentioned [X] times
2. "[keyword 2]" - mentioned [X] times
3. "[keyword 3]" - mentioned [X] times
4. "[keyword 4]" - mentioned [X] times
5. "[keyword 5]" - mentioned [X] times

### Response Rate:
- **Reviews Responded To:** [X%]
- **Avg Response Time:** [X hours]
- **Target:** 100% response rate within 24 hours

---

## 3. Competitive Comparison

| Metric | [Client] | Competitor 1 | Competitor 2 | Competitor 3 |
|--------|----------|--------------|--------------|--------------|
| Total Mentions (30d) | [X] | [X] | [X] | [X] |
| Tier-1 Mentions | [X] | [X] | [X] | [X] |
| Avg Rating | [X.X] | [X.X] | [X.X] | [X.X] |
| Total Reviews | [X] | [X] | [X] | [X] |
| Reddit Presence | [Yes/No] | [Yes/No] | [Yes/No] | [Yes/No] |
| News Coverage | [Yes/No] | [Yes/No] | [Yes/No] | [Yes/No] |

**Key Finding:** [e.g., "Competitor 2 has 3x more Reddit mentions — opportunity to engage in r/saas and r/entrepreneur"]

---

## 4. Action Items for Next 30 Days

### High Priority (Complete Within 7 Days):
1. **Convert Unlinked Mentions:**
   - Reach out to [X] journalists/bloggers who mentioned the brand without linking
   - Use outreach template in `clients/[client]/templates/unlinked_mention_outreach.md`
   - Target: Convert ≥30% to actual backlinks

2. **Respond to All Reviews:**
   - [X] reviews need responses (particularly negative ones)
   - Draft personalized responses addressing specific concerns
   - Post within 24 hours

3. **Fix Negative Sentiment Issues:**
   - [X% negative reviews] cite "[specific issue, e.g., slow support response]"
   - **Immediate Action:** [specific fix, e.g., hire support staff, update help docs, create video tutorials]

### Medium Priority (Complete Within 30 Days):
4. **Launch Review Generation Campaign:**
   - Send review request emails to [X] recent customers
   - Target: Gain [X] new 5-star reviews this month
   - Use automated email sequence via [tool, e.g., BirdEye, Podium, or custom CRM]

5. **Increase Tier-1 Platform Presence:**
   - **Reddit Strategy:**
     - Identify 3-5 relevant subreddits (e.g., r/[niche], r/[industry])
     - Participate in discussions authentically (no spam)
     - Share case studies or unique data (not sales pitches)
   - **Quora Strategy:**
     - Answer 10 questions related to [client's niche]
     - Link to relevant resources (not homepage)
   - **News/PR:**
     - Pitch [X] relevant journalists about [unique angle, e.g., new feature launch, industry trend analysis, original research]

6. **Update Homepage Copy with Review Keywords:**
   - Add phrases: "[keyword 1]", "[keyword 2]", "[keyword 3]" from reviews
   - Update H2 headings and service descriptions to match customer language

### Low Priority (Ongoing Monitoring):
7. **Set Up Brand Monitoring Alerts:**
   - Use Google Alerts for "[Brand Name]"
   - Set up Mention.com or Brand24 for real-time tracking
   - Check weekly for new mentions

8. **Track AI Citation Rate:**
   - Monthly test: Search [X] relevant queries in ChatGPT and Perplexity
   - Document: Is the brand cited in responses?
   - Goal: Appear in ≥20% of relevant AI search queries

---

## 5. Risk Assessment

### Critical Risks:
- [If applicable, e.g., "Negative sentiment spike (25% negative reviews in past 30 days) — immediate reputation management required"]
- [If applicable, e.g., "Zero Tier-1 mentions — brand is invisible to AI search engines"]

### Moderate Risks:
- [If applicable, e.g., "Review velocity declining (-20% vs last month) — need proactive review request campaign"]
- [If applicable, e.g., "Competitors have 2x more Reddit presence — losing mindshare in target audience"]

### Strengths:
- [e.g., "Strong sentiment ratio (92% positive) — high customer satisfaction"]
- [e.g., "Growing news coverage (+3 media mentions this month) — increasing authority"]

---

## 6. Next Report Date
**Next Review:** [30 days from today]

**Monitoring Frequency:**
- Brand mention tracking: Weekly
- Review monitoring: Daily
- Competitive analysis: Monthly
```

---

## Handling Edge Cases

### Zero Discoverable Mentions
If the `brand_mention_tracker.py` returns 0 mentions:
- The brand is considered an "Unknown Entity" by AI engines.
- **Immediate Action Required:**
  1. **Digital PR Campaign:** Pitch 5 industry blogs/news sites with unique angle (case study, research data, contrarian opinion)
  2. **Podcast Outreach:** Appear on 3 niche podcasts in the next 90 days
  3. **Reddit Strategy:** Start discussions in relevant subreddits (authentically, not spam)
  4. **Quora Presence:** Answer 20 questions in the client's niche, linking to helpful resources
  5. **Content Marketing:** Publish original research or data study that journalists will cite

### Negative Sentiment Spike
If `review_aggregator.py` shows >20% negative sentiment in recent reviews:
- **Red Flag Warning:** Semantic search engines interpret persistent negative sentiment as a signal of low E-E-A-T and will actively suppress rankings.
- **Immediate Actions:**
  1. **Root Cause Analysis:** What specific issue do negative reviews cite? (slow support, bugs, pricing, etc.)
  2. **Fix the Core Problem:** This is NOT a marketing problem, it's an operations problem. Fix the underlying issue first.
  3. **Public Response:** Respond to EVERY negative review within 24 hours with:
     - Acknowledgment of the issue
     - Specific action taken to fix it
     - Direct contact (email/phone) to resolve
  4. **Review Generation:** Once issue is fixed, proactively ask satisfied customers for reviews to dilute negative sentiment
  5. **Monitor Daily:** Check review platforms daily for 30 days to catch and respond to new negatives immediately

### No Review Platforms Available (B2B SaaS Edge Case)
If client is B2B SaaS without Google Business Profile:
- **Alternative Review Sources:**
  - G2
  - Capterra
  - TrustRadius
  - Software Advice
- **Action:** Run `review_aggregator.py` against G2 API (requires custom integration)
- **Workaround:** Manually export G2 reviews CSV, parse with Python script

### Competitor Outperforming Significantly
If competitive analysis shows client has <50% of competitor's mention volume:
- **Gap Analysis Required:**
  1. What platforms are competitors dominating? (Reddit? News? LinkedIn?)
  2. What content themes drive their mentions? (thought leadership? case studies? controversy?)
  3. What can client do that competitors aren't? (unique data, contrarian viewpoint, underserved audience segment)
- **Strategic Recommendations:**
  - Focus on 1-2 platforms where gap is smallest (easier to close)
  - Differentiate content strategy (don't copy competitors)
  - Consider paid PR partnerships if organic growth is too slow

---

## Integration with Other Workflows

### Connect to /entity_audit:
Brand mentions directly impact entity strength. After completing brand monitoring:
```bash
python tools/entity_auditor.py --brand "[Client Name]" --website "[client.com]" --output .tmp/entity_audit.json
```
Compare entity score over time. Strong brand mention velocity should increase entity score by 10-15 points within 90 days.

### Connect to /monthly_report:
Include brand health metrics in monthly client reports:
- New mentions this month
- Review velocity trend
- Unlinked mentions converted
- AI citation rate

### Connect to /content_draft:
Use common review keywords as topic ideas for new content:
- If reviews mention "easy to use", create content around "How [Client] Makes [Task] Simple"
- If reviews cite "[specific feature]", create dedicated landing page for that feature

---

## Automation & Monitoring Setup

### Recommended Monitoring Cadence:
- **Daily:** Review platforms (GBP, G2, Capterra) — respond to new reviews
- **Weekly:** Brand mention tracking — check for new unlinked mentions
- **Monthly:** Competitive analysis — compare mention volume and sentiment
- **Quarterly:** Full brand health report — strategic recommendations

### Automation Ideas:
1. **Zapier Integration:**
   - Trigger: New Google review posted
   - Action: Send Slack notification + draft response with GPT-4

2. **Brand Alert System:**
   - Use Google Alerts + Mention.com
   - Email digest weekly with new mentions

3. **Review Request Automation:**
   - CRM integration: 7 days after project completion, auto-send review request email
   - Include direct link to review platform

---

## Quality Checklist

Before finalizing the brand health report, verify:
- [ ] Brand mention tracker ran successfully (no API errors)
- [ ] Review aggregator data is current (<7 days old)
- [ ] Competitive analysis includes ≥3 competitors
- [ ] All unlinked mentions have outreach plan
- [ ] Negative reviews have response strategy
- [ ] Review keywords identified and documented
- [ ] Action items are specific and time-bound
- [ ] Next review date is scheduled
- [ ] Report saved to `clients/<client_name>/reports/brand_health_report_YYYY_MM.md`

---

## Expected Outcomes (90-Day Horizon)

If this workflow is executed monthly for 90 days, expect:
- **+30-50% increase in brand mentions** (from proactive PR and content)
- **+15-25 new reviews** (from review generation campaigns)
- **10-20 new backlinks** (from unlinked mention conversions)
- **+10-15 points in entity score** (measured via entity_auditor.py)
- **2-3x increase in AI search citations** (measured via manual ChatGPT/Perplexity queries)

These signals compound to improve:
- **Organic rankings** (+3-7 positions for competitive terms)
- **Click-through rate** (+1-2% from increased brand recognition)
- **Conversion rate** (+5-10% from social proof and reviews)

---

**End of Workflow**
