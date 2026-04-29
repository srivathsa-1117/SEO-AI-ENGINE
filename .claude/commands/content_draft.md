---
description: /content_draft - Write a full SEO-optimized article from an approved content brief
---

# Workflow: Content Draft Generation (100% Humanized & Ranking-Optimized)

## Trigger
```
/content_draft <client_name> [--brief <path_to_brief>]
```

## Objective
Generate a fully SEO-optimized, AEO/GEO-ready article that ranks #1. The output MUST bypass AI detectors (100% humanized) through high burstiness, varied sentence lengths, and the absolute elimination of standard AI jargon. It must include exact Titles, Metas, and CMS-ready formatting.

---

## 🚨 CRITICAL RULE: The "100% Human" Writing Guidelines

You must write like a Senior Subject Matter Expert, not an AI. 

**1. BANNED AI VOCABULARY:**
Do NOT use these words under any circumstances: *delve, moreover, furthermore, tapestry, paramount, seamless, dynamic, robust, landscape, testament, elevate, unleash, unlock, navigate, symphony, beacon, in today's digital age, in conclusion, to summarize.*

**2. Burstiness & Perplexity:**
- Vary your sentence lengths drastically. Use very short, punchy sentences (3-5 words). Follow them with longer, descriptive sentences.
- Avoid perfectly symmetrical paragraph lengths. Humans write in asymmetrical blocks.

**3. Tone & Voice:**
- Use active voice only. Avoid passive voice.
- Limit transition words (like "however," "therefore"). Humans use them sparingly.
- Sound opinionated, authoritative, and direct. Get straight to the point. No fluff.

**4. E-E-A-T Elements (Experience & Expertise):**
- Phrase concepts using first-hand terminology where appropriate to the brand: *"In our experience,"* *"When we tested this,"* *"What we usually see is..."*

---

## Step-by-Step Instructions

### Step 1: Load Context
- Read `clients/<client_name>/brand_kit.json`.
- Internalize the `tone`, `persona`, and `target_audience`.
- Read the content brief provided.

### Step 2: The SEO Package (CMS Metadata)
Before writing the article, you must generate the exact metadata the user will copy/paste into their CMS:
- **Title Tag:** Exactly 50-60 characters. Primary Keyword at the front.
- **Meta Description:** Exactly 120-160 characters. End with a Call to Action (CTA).
- **URL Slug:** `primary-keyword-format`

### Step 3: Write the Draft (Section by Section)

**The Hook (Introduction):**
- Maximum 3 paragraphs. 
- Introduce the core problem immediately.
- Use the target keyword in the first 75 words.
- Provide the TL;DR / Direct Answer immediately (for AI Overviews / Google AEO extraction).

**The Body:**
- Follow the H2 and H3 structure from the brief.
- Naturally weave in LSI / Semantic secondary keywords. Do not keyword stuff.
- **Formatting:** Use bullet points, bolded text for emphasis, and short paragraphs to make the content highly scannable (which decreases bounce rate, increasing rankings).
- **Internal Links:** Embed the exact internal links from the brief naturally into the text.

**The FAQ Section (If applicable):**
- Write exactly 2-3 sentences per answer. Be blunt and factual. Format as Q&A for Featured Snippet optimization.

**The Conclusion:**
- Do not write a summary. Write an actionable next step.
- Include the client's specific Call to Action (CTA).

### Step 4: SEO Final Checking
Perform a strict check before outputting:
- [ ] Is the primary keyword in the H1, URL, Title Tag, Meta Description, and first 100 words?
- [ ] Are all banned AI words completely eliminated?
- [ ] Does it sound human (varied sentence length)?
- [ ] Are paragraphs short and scannable?
- [ ] Are internal links included naturally?

### Step 5: Output Generation
Present the final draft in clean Markdown format in the chat so the user can literally "select all, copy, and paste" into WordPress/Shopify.

Ask the user: 
**"Here is the 100% human-optimized draft and CMS package. Would you like me to refine the tone, or shall we save this to the client's folder?"**
