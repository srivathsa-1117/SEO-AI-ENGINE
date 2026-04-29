---
description: /add_client - Onboard a new client into the SEO AI OS system
---

# Workflow: Add New Client

## Trigger
```
/add_client <client_slug>
```
**Example:** `/add_client acme_corp`

## Objective
Create the full client folder structure and populate the brand_kit.json by asking the user a series of onboarding questions. Then run the first-time audit automatically.

## Step-by-Step Instructions

### Step 1: Create Folder Structure
Copy `clients/_template/` to `clients/<client_slug>/`:
- `brand_kit.json` (from template, pre-filled with placeholders)
- `audit_history/` (empty)
- `reports/` (empty)
- `active_campaigns/` (empty)

### Step 2: Ask Onboarding Questions (one at a time)
Ask the user for the following information to fill in brand_kit.json:

1. "What is the client's full business name and website URL?"
2. "What industry are they in, and do they have a specific target location? (e.g. Local: Austin TX, or National)"
3. "Who is their target customer? Describe their main persona."
4. "What are the client's top 3 competitors? (provide URLs if possible)"
5. "What tone of voice does the brand use? (e.g. professional, friendly, technical, playful)"
6. "What are their top 3 primary keywords they want to rank for?"
7. "Are there any keywords they want to AVOID? (e.g. words that don't match their brand)"
8. "What CMS do they use? (WordPress / Webflow / Shopify / Other)"
9. "Do they have Google Search Console and GA4 set up? Do they have access to share?"
10. "What is the preferred report delivery format? (Monthly PDF / Google Slides / Plain Markdown)"

### Step 3: Save Brand Kit
- Write all answers into `clients/<client_slug>/brand_kit.json`
- Display the completed brand_kit.json to the user and ask: **"Does this look correct? Shall I run the first-time audit now?"**

### Step 4: Trigger Audit (After Approval)
- Run `/audit <client_slug> --type first_time`
- This will follow the `audit.md` workflow and produce the initial baseline report

---

# Workflow: Remove Client

## Trigger
```
/remove_client <client_slug>
```
**Example:** `/remove_client acme_corp`

## Objective
Safely archive or delete a client when they offboard. Prevents accidental data loss.

## Step-by-Step Instructions

### Step 1: Confirm with User
Always ask first:
**"Are you sure you want to remove `<client_slug>`? Type `CONFIRM` to archive them, or `DELETE` to permanently remove all their data."**

### Step 2A: Archive (Recommended)
- Move `clients/<client_slug>/` to `clients/_archived/<client_slug>_<YYYY-MM-DD>/`
- This preserves all reports and history in case the client comes back

### Step 2B: Delete (Permanent)
- Only if user types `DELETE` explicitly
- Permanently delete `clients/<client_slug>/` folder and all contents
- This cannot be undone — warn the user clearly

### Step 3: Confirm
Confirm to the user: "Client `<client_slug>` has been [archived/removed] successfully."
