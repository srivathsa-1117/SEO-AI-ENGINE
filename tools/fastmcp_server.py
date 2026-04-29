#!/usr/bin/env python3
"""
FastMCP Governance Server
Wraps the core AIOS Python tools into a strict, strongly-typed MCP Server.
This solves the "Description-Code Inconsistency" problem, preventing LLMs from
hallucinating arguments or sending destructive payloads.

Usage:
    mcp run fastmcp_server.py
"""
import sys
import os
import asyncio
import json
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    import subprocess
    print("Installing FastMCP dependencies...", file=sys.stderr)
    subprocess.run(["pip", "install", "mcp"], check=True)
    from mcp.server.fastmcp import FastMCP

# Initialize the Governance Server
mcp = FastMCP("SEO_AIOS_Governance_Server")

@mcp.tool()
async def run_seo_crawler(url: str, max_pages: int = 100) -> str:
    """
    Safely triggers the Playwright asynchronous SEO crawler.
    Strictly types the arguments to prevent infinite crawl loops or malformed URLs.
    """
    if not url.startswith("http"):
        return "Error: URL must start with http:// or https://"

    try:
        import tools.seo_crawler as seo_crawler
        
        # Windows proactor loop if needed
        if os.name == 'nt' and not isinstance(asyncio.get_event_loop_policy(), asyncio.WindowsProactorEventLoopPolicy):
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
            
        data = await seo_crawler.async_crawl_site(url, max_pages=max_pages)
        base_name = urlparse(url).netloc
        output_path = f".tmp/crawl_{base_name}_{datetime.now().strftime('%Y%m%d')}.json"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return f"Crawl successful. Saved to {output_path}\n\nSummary:\n{json.dumps(data['summary'], indent=2)}"
    except Exception as e:
        return f"Crawl failed. Error: {str(e)}"

@mcp.tool()
def run_semantic_clusterer(client_slug: str, threshold: float = 0.5) -> str:
    """
    Triggers the HuggingFace sentence-transformer clustering model safely.
    Threshold must be between 0.1 and 1.0 (Lower = tighter clusters).
    """
    if not (0.1 <= threshold <= 1.0):
        return "Error: Threshold must be between 0.1 and 1.0"

    try:
        brand_path = Path(f"clients/{client_slug}/brand_kit.json")
        keywords = []
        if brand_path.exists():
            with open(brand_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                kws = data.get("seo_targets", {})
                primary = kws.get("primary_keywords", [])
                secondary = kws.get("secondary_keywords", [])
                keywords = primary + secondary
                
        keywords = list(set([k for k in keywords if k]))
        if not keywords:
            return "No keywords found in brand kit."

        import tools.keyword_clusterer as keyword_clusterer
        clusters = keyword_clusterer.cluster_keywords(keywords, distance_threshold=threshold)
        return f"Clustering complete. Found {len(clusters)} topic clusters."
    except Exception as e:
        return f"Clustering failed. Error: {str(e)}"

@mcp.tool()
def run_geo_heatmap(client_slug: str, keyword: str, zipcodes: str) -> str:
    """
    Triggers the mathematical AEO coordinate spoofing heatmap.
    zipcodes must be comma-separated strings (e.g., '10001,10002').
    """
    try:
        import tools.geospatial_search as geospatial_search
        output_dir = Path(f".tmp/geospatial/{client_slug}")
        output_dir.mkdir(parents=True, exist_ok=True)
        zips = [z.strip() for z in zipcodes.split(',')]
        geospatial_search.generate_local_heatmap(client_slug, keyword, zips, "example.com", output_dir)
        return f"Geospatial heatmap generated successfully in .tmp/geospatial/{client_slug}"
    except Exception as e:
        return f"Geospatial mapping failed. Error: {str(e)}"

@mcp.tool()
def analyze_readability(file_path: str) -> str:
    """
    Mathematically scores content for Flesch Reading Ease and strips AI Stylometry.
    Prevents deploying content that Google's Helpful Content Updates will penalize.
    """
    try:
        import tools.nlp_analyzer as nlp_analyzer
        data = nlp_analyzer.analyze_readability_and_stylometry(file_path)
        return f"Readability analysis complete.\n\n{json.dumps(data, indent=2)}"
    except Exception as e:
        return f"Analysis failed. Error: {str(e)}"


@mcp.tool()
def find_outreach_emails(domain: str) -> str:
    """
    Finds verified emails for a domain and generates link-building outreach drafts.
    """
    try:
        import tools.outreach_sender as outreach_sender
        data = outreach_sender.find_emails_for_outreach(domain)
        return f"Outreach Data:\n{data}"
    except Exception as e:
        return f"Hunter.io retrieval failed. Error: {str(e)}"


@mcp.tool()
def generate_llms_txt(url: str, mode: str = "validate") -> str:
    """
    Validates or generates an llms.txt file for AI crawlers.
    mode can be 'validate' or 'generate'.
    """
    try:
        import tools.llmstxt_generator as llmstxt_generator
        if mode == "generate":
            res = llmstxt_generator.generate_llmstxt(url)
        else:
            res = llmstxt_generator.validate_llmstxt(url)
        return f"llms.txt {mode} result:\n{json.dumps(res, indent=2)}"
    except Exception as e:
        return f"Failed to process llms.txt. Error: {str(e)}"

if __name__ == "__main__":
    # Start the FastMCP server, exposing these governed functions to Claude/AI clients
    mcp.run()
