#!/usr/bin/env python3
"""
Schema Checker Tool
Analyzes website schema markup and provides AEO/GEO readiness score.

Usage:
    python schema_checker.py --url https://example.com
    python schema_checker.py --client acme_corp
"""

import argparse
import json
import sys
import time
from pathlib import Path
from datetime import datetime

# Windows console UTF-8 fix (handles ✓ ✗ → characters)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import smart_fetch, extract_schema_types

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "requests", "beautifulsoup4", "lxml"], check=True)
    import requests
    from bs4 import BeautifulSoup


def check_schema(url: str) -> dict:
    """Check schema markup and AEO/GEO readiness for a URL."""
    result = {
        "url": url,
        "checked_at": datetime.now().isoformat(),
        "schema_types": [],
        "aeo_geo_score": 0,
        "findings": [],
        "recommendations": []
    }

    try:
        fetch = smart_fetch(url)
        if not fetch["success"]:
            result["findings"].append(f"ERROR: Cannot fetch page - {fetch['error']}")
            return result

        # If DataForSEO returned pre-parsed data, extract schema types directly
        if fetch["method"] == "dataforseo" and fetch.get("parsed_data"):
            pd = fetch["parsed_data"]
            result["schema_types"] = pd.get("schema_types", [])
            score_points = 0
            has_faq = "FAQPage" in result["schema_types"]
            has_article = any(t in result["schema_types"] for t in ["Article", "BlogPosting", "NewsArticle"])
            has_local_business = "LocalBusiness" in result["schema_types"]
            has_breadcrumb = "BreadcrumbList" in result["schema_types"]
            has_organization = "Organization" in result["schema_types"]
            has_website = "WebSite" in result["schema_types"]
            if result["schema_types"]:
                result["findings"].append(f"Found schema types via DataForSEO: {', '.join(result['schema_types'])}")
            else:
                result["findings"].append("CRITICAL: No schema markup detected (via DataForSEO)")
                result["recommendations"].append("Add at least Organization or WebSite schema")
            if has_faq:
                score_points += 20
                result["findings"].append("✓ FAQPage schema detected (great for GEO)")
            if has_article:
                score_points += 15
            if has_local_business:
                score_points += 20
                result["findings"].append("✓ LocalBusiness schema detected")
            if has_breadcrumb:
                score_points += 10
                result["findings"].append("✓ BreadcrumbList schema detected")
            if has_organization:
                score_points += 15
                result["findings"].append("✓ Organization schema detected")
            if has_website:
                score_points += 10
                result["findings"].append("✓ WebSite schema detected")
            if not has_faq:
                result["recommendations"].append("Add FAQPage schema for GEO visibility")
            if not has_organization:
                result["recommendations"].append("Add Organization schema to homepage")
            if not has_breadcrumb:
                result["recommendations"].append("Add BreadcrumbList schema for better navigation understanding")
            result["aeo_geo_score"] = min(score_points, 100)
            result["rating"] = (
                "Excellent" if score_points >= 80 else
                "Good"      if score_points >= 60 else
                "Fair"      if score_points >= 40 else "Poor"
            )
            result["findings"].append(f"[INFO] Data fetched via DataForSEO On-Page API (bot protection bypass)")
            return result

        soup = BeautifulSoup(fetch["html"], "lxml")
        score_points = 0
        max_score = 100

        # Check for JSON-LD schema
        schema_scripts = soup.find_all("script", attrs={"type": "application/ld+json"})

        if not schema_scripts:
            result["findings"].append("CRITICAL: No JSON-LD schema found on page")
            result["recommendations"].append("Add at least Organization or WebSite schema")
        else:
            result["findings"].append(f"Found {len(schema_scripts)} schema markup blocks")

        # Parse schema types
        schema_types = set()
        has_faq = False
        has_article = False
        has_local_business = False
        has_breadcrumb = False
        has_organization = False
        has_website = False

        for script in schema_scripts:
            try:
                data = json.loads(script.string or "{}")
                # Recursively extract every @type at any nesting depth
                # (handles @graph, nested publisher/breadcrumb/mainEntity, etc.)
                types, same_as = extract_schema_types(data)
                for schema_type in types:
                    if schema_type in schema_types:
                        continue
                    schema_types.add(schema_type)
                    result["schema_types"].append(schema_type)
                    if schema_type == "FAQPage":
                        has_faq = True
                        score_points += 20
                        result["findings"].append("✓ FAQPage schema detected (great for GEO)")
                    elif schema_type in ["Article", "BlogPosting", "NewsArticle"]:
                        has_article = True
                        score_points += 15
                        result["findings"].append(f"✓ {schema_type} schema detected")
                    elif schema_type == "LocalBusiness":
                        has_local_business = True
                        score_points += 20
                        result["findings"].append("✓ LocalBusiness schema detected")
                    elif schema_type == "BreadcrumbList":
                        has_breadcrumb = True
                        score_points += 10
                        result["findings"].append("✓ BreadcrumbList schema detected")
                    elif schema_type == "Organization":
                        has_organization = True
                        score_points += 15
                        result["findings"].append("✓ Organization schema detected")
                    elif schema_type == "WebSite":
                        has_website = True
                        score_points += 10
                        result["findings"].append("✓ WebSite schema detected")
                if same_as and has_organization:
                    result["findings"].append("✓ Organization sameAs entity links present")
            except json.JSONDecodeError:
                result["findings"].append("WARNING: Found invalid JSON-LD schema block")

        # Check for structured "Who/What/Why" answer blocks
        has_clear_structure = False
        # Look for common patterns
        if soup.find("h2", string=lambda t: t and any(kw in t.lower() for kw in ["what is", "who is", "why"])):
            has_clear_structure = True
            score_points += 10
            result["findings"].append("✓ Detected structured answer format (good for GEO)")

        # Check for author entity
        has_author = False
        if soup.find("span", attrs={"itemprop": "author"}) or soup.find("a", {"rel": "author"}):
            has_author = True
            score_points += 5
            result["findings"].append("✓ Author entity present")

        # Calculate final score
        result["aeo_geo_score"] = min(score_points, max_score)

        # Generate recommendations
        if not has_faq:
            result["recommendations"].append("Add FAQPage schema for GEO visibility")
        if not has_article and "blog" in url.lower():
            result["recommendations"].append("Add Article schema for blog posts")
        if not has_organization:
            result["recommendations"].append("Add Organization schema to homepage")
        if not has_breadcrumb:
            result["recommendations"].append("Add BreadcrumbList schema for better navigation understanding")
        if not has_clear_structure:
            result["recommendations"].append("Structure content with clear 'What/Who/Why' sections for GEO")
        if not has_author:
            result["recommendations"].append("Add author entity markup for E-E-A-T signals")

        # Rating
        if result["aeo_geo_score"] >= 80:
            result["rating"] = "Excellent"
        elif result["aeo_geo_score"] >= 60:
            result["rating"] = "Good"
        elif result["aeo_geo_score"] >= 40:
            result["rating"] = "Fair"
        else:
            result["rating"] = "Poor"

    except Exception as e:
        result["findings"].append(f"ERROR: Cannot fetch page - {e}")

    return result


def main():
    parser = argparse.ArgumentParser(description="Schema Markup & AEO/GEO Readiness Checker")
    parser.add_argument("--url", help="URL to check")
    parser.add_argument("--client", help="Client name (checks homepage from brand_kit)")
    parser.add_argument("--output", help="Output JSON file path")
    args = parser.parse_args()

    url = args.url
    if args.client and not url:
        brand_kit_path = Path(f"clients/{args.client}/brand_kit.json")
        if brand_kit_path.exists():
            with open(brand_kit_path, "r") as f:
                brand_kit = json.load(f)
                url = brand_kit.get("technical_settings", {}).get("website_url") or brand_kit.get("client_info", {}).get("website_url")

    if not url:
        print("Error: Must provide --url or --client with valid brand_kit.json")
        return

    print(f"[Schema Checker] Analyzing: {url}")
    result = check_schema(url)

    # Save output FIRST (before any print that might fail on Windows console)
    output_path = args.output or f".tmp/schema_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    # Print summary (replace Unicode symbols for Windows console safety)
    def safe(s): return s.replace("✓", "[OK]").replace("✗", "[X]").replace("→", "->")
    print(f"\n=== AEO/GEO READINESS SCORE: {result['aeo_geo_score']}/100 ({result.get('rating', 'N/A')}) ===")
    print("\nFindings:")
    for finding in result["findings"]:
        print(f"  {safe(finding)}")

    if result["recommendations"]:
        print("\nRecommendations:")
        for rec in result["recommendations"]:
            print(f"  - {safe(rec)}")

    print(f"\n[Output] Saved to: {output_path}")


if __name__ == "__main__":
    main()
