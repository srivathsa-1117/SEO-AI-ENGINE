# MCP Server Configuration Guide

**Date:** 2026-03-18
**Status:** 3 Active MCP Servers
**Purpose:** Unlock full AIOS potential with direct API access

---

## 🎯 What Are MCPs?

**MCP (Model Context Protocol)** servers give Claude direct access to external tools and APIs without needing Python scripts. This means:

✅ **Faster** - Real-time streaming results
✅ **Safer** - Type-validated arguments prevent errors
✅ **Fresher** - Direct API access = no stale data
✅ **Simpler** - No manual CSV exports or file handling

---

## 📦 Active MCP Servers (3 Total)

### 1. PageSpeed Insights MCP
- **Package:** @ruslanlap/pagespeed-insights-mcp v1.1.1
- **Type:** Node.js server
- **Purpose:** Real-time Core Web Vitals analysis
- **Status:** ACTIVE

### 2. Google Search Console MCP
- **Type:** Python FastMCP server
- **Purpose:** Direct GSC API access for keyword data
- **Status:** ACTIVE

### 3. AIOS Governance Server
- **Type:** Python FastMCP wrapper
- **Purpose:** Type-safe wrapper for core AIOS tools
- **Status:** ACTIVE

---

## Configuration File Location

`C:\Users\HP\AppData\Roaming\Claude\claude_desktop_config.json`

All 3 MCPs are now configured and will auto-connect on Claude Desktop restart.

---

## Verification

After restarting Claude Desktop, all 3 MCPs should show as connected (green dots).

Test with:
- "Analyze https://google.com with PageSpeed"
- "Get top keywords from GSC for metalbarns.in"
- "Crawl example.com with governance server"

---

For full documentation, see CLAUDE.md section: "MCP SERVERS — Supercharged Tool Access"
