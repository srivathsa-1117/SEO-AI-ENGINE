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
import time
from pathlib import Path
from datetime import datetime

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
        headers = {"User-Agent": "Mozilla/5.0 (compatible; SEO-AI-OS-Schema-Checker/1.0)"}
        resp = requests.get(url, headers=headers, timeout=15, allow_redirects=True)

        if resp.status_code != 200:
            result["findings"].append(f"ERROR: Cannot access page (HTTP {resp.status_code})")
            return result

        soup = BeautifulSoup(resp.text, "lxml")
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

                # Handle both single objects and arrays
                if isinstance(data, dict):
                    schema_list = [data]
                elif isinstance(data, list):
                    schema_list = data
                else:
                    continue

                for item in schema_list:
                    if isinstance(item, dict):
                        schema_type = item.get("@type")
                        if schema_type:
                            schema_types.add(schema_type)
                            result["schema_types"].append(schema_type)

                            # Check for specific AEO/GEO-friendly schemas
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

    except requests.exceptions.RequestException as e:
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

    # Print summary
    print(f"\n=== AEO/GEO READINESS SCORE: {result['aeo_geo_score']}/100 ({result.get('rating', 'N/A')}) ===")
    print("\nFindings:")
    for finding in result["findings"]:
        print(f"  {finding}")

    if result["recommendations"]:
        print("\nRecommendations:")
        for rec in result["recommendations"]:
            print(f"  • {rec}")

    # Save output
    output_path = args.output or f".tmp/schema_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n[Output] Saved to: {output_path}")


if __name__ == "__main__":
    main()
