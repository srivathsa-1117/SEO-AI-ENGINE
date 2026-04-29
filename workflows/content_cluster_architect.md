---
description: /content_cluster_architect - Hub & Spoke Generator
---

# Workflow: Content Cluster Architect (2026 Standards)

## Trigger
```
/content_cluster_architect <core_topic> <client_domain>
```

## Objective
Design the complete architecture for an SEO topic cluster. In 2026, creating disconnected, isolated blog posts is a failure. You must design a semantic hub and spoke model to rank for competitive head terms.

---

## The 4-Step Cluster Build Process

### Step 1: Ingest the Topic Graph
Read the output of `tools/topic_graph_mapper.py` or `.tmp/topic_graph.json` generated during the `/topical_audit` workflow.
You need the `core_hub` (the main pillar page) and the `sub_pillars` (the spokes).

### Step 2: Establish the Hub Page Architecture
Design the primary pillar page (the "Hub").
- URL: `https://client.com/core-topic/`
- Goal: Create a 2,000+ word definitive guide.
- **Requirement**: The Hub MUST internally link to every Spoke explicitly. The AI OS must draft the HTML structure of the Hub page highlighting where the "Related Topics" internal link block will sit.

### Step 3: Design the Spoke Pages
For each `sub_pillar` (leaf node) identified in the Topic Graph Mapper:
- Draft a targeted URL: `https://client.com/core-topic/sub-topic/`
- Identify the specific long-tail intent for that Spoke.
- **Requirement**: Every Spoke MUST have a contextual backlink explicitly to the Hub page (`href="/core-topic/"`). Do not use footer/sidebar links; it must be in the main body text.

### Step 4: Output the Master Blueprint
Save a complete Markdown plan inside `clients/<client_name>/active_campaigns/cluster_blueprint_<topic>.md`.
The blueprint MUST include:
1. Hub Page Title, URL, and H2 structure.
2. Spoke Pages (minimum 5-8 pages) with Titles, URLs.
3. Explicit Internal Linking Anchor Text for both Hub -> Spoke and Spoke -> Hub.
4. Required Schema Markup (`Article` or `HowTo` for spokes, `CollectionPage` for the Hub if applicable).

You can then pass this architecture directly to the `/content_brief` workflow to begin drafting actual SEO content.
