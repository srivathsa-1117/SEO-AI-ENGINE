---
description: /programmatic_seo - Generate architecture for 50+ unique programmatic pages safely
---

# /programmatic_seo

This command initiates the programmatic SEO workflow.

**Action**: When invoked, immediately read and follow the strict quality-gate workflow defined in `workflows/programmatic_seo.md` to design the schema, content template, and URL structure for building scalable programmatic SEO pages. 

You must:
1. Strictly enforce the "3-Variable Minimum".
2. Run quality simulations using `tools/programmatic_quality_scorer.py` on client data.
3. Mandate the use of `tools/indexing_monitor.py` for phased rollouts to prevent Google Helpful Content Update penalties.
