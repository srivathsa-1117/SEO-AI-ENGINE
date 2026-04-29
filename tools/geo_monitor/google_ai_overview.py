#!/usr/bin/env python3
"""
GEO Monitor — Google AI Overview scraper (No API Key Required)

Uses Playwright to open a real headless browser, perform a Google search,
and check if a brand appears in the AI Overview (SGE), Knowledge Panel,
or organic results.

Usage:
    python tools/geo_monitor/google_ai_overview.py --brand "Example Brand" --queries "top digital marketing agencies India"
    python tools/geo_monitor/google_ai_overview.py --brand "Acme Corp" --domain acmecorp.com

Requirements:
    pip install playwright beautifulsoup4
    playwright install chromium
"""

import argparse
import json
import sys
import time
import random
from datetime import datetime
from urllib.parse import quote_plus

try:
    from playwright.sync_api import sync_playwright
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: Run: pip install playwright beautifulsoup4")
    print("Then run: playwright install chromium")
    sys.exit(1)


def create_browser_context(p):
    """Create a stealthy browser context to avoid blocks."""
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        locale="en-US",
        timezone_id="America/New_York"
    )
    return browser, context


def check_google_serp(page, query: str, brand: str, domain: str = None) -> dict:
    """Scrape Google SERP for brand mentions using Playwright."""
    url = f"https://www.google.com/search?q={quote_plus(query)}&hl=en&gl=us"

    result = {
        "query": query,
        "url": url,
        "brand_in_snippet": False,
        "brand_in_knowledge_panel": False,
        "brand_in_organic": False,
        "brand_in_people_also_ask": False,
        "organic_rank": None,
        "domain_rank": None,
        "visibility_score": 0,
        "error": None,
    }

    try:
        # Navigate and wait for content to load
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        
        # Handle Google Cookie Consent popup if it appears
        try:
            # Often the 'Accept all' button is the second one, or has specific text
            accept_btn = page.locator("button:has-text('Accept all')").first
            if accept_btn.is_visible(timeout=2000):
                accept_btn.click()
                page.wait_for_timeout(1000)
        except:
            pass
            
        # Give generation time to finish and AJAX to load
        page.wait_for_timeout(random.randint(3000, 5000))
        
        html = page.content()
        
        # DEBUG: Save the HTML and Screenshot to inspect what Google actually returned
        with open(".tmp/google_debug.html", "w", encoding="utf-8") as f:
            f.write(html)
        page.screenshot(path=".tmp/google_debug.png")
            
        soup = BeautifulSoup(html, "html.parser")
        
        brand_lower = brand.lower()
        domain_lower = domain.lower() if domain else None

        # 1. AI Overview / Featured Snippet area
        # Google uses complex dynamic classes, so we look for common container markers
        snippet_markers = [
            {"data-md": True}, 
            {"class_": lambda c: c and "featured" in c.lower()},
            {"class_": lambda c: c and "ai-overview" in c.lower()}
        ]
        
        for marker in snippet_markers:
            featured = soup.find("div", **marker)
            if featured:
                if brand_lower in featured.get_text().lower():
                    result["brand_in_snippet"] = True
                    break

        # 2. Knowledge Panel (usually has data-attrid)
        kp = soup.find("div", attrs={"data-attrid": True})
        if kp:
            if brand_lower in kp.get_text().lower():
                result["brand_in_knowledge_panel"] = True

        # 3. People Also Ask 
        # Usually contained in divs with related questions
        blocks = soup.find_all("div")
        for block in blocks:
            header = block.find("h2")
            if header and "people also ask" in header.get_text().lower():
                if brand_lower in block.get_text().lower():
                    result["brand_in_people_also_ask"] = True
                break

        # 4. Organic Results
        all_results = soup.find_all("div", attrs={"data-ved": True})
        rank = 0
        for item in all_results:
            link = item.find("a", href=True)
            if not link:
                continue
            href = link.get("href", "")
            if href.startswith("/url?") or href.startswith("http"):
                rank += 1
                snippet_text = item.get_text().lower()
                if brand_lower in snippet_text:
                    result["brand_in_organic"] = True
                    if result["organic_rank"] is None:
                        result["organic_rank"] = rank
                if domain_lower and domain_lower in href.lower():
                    if result["domain_rank"] is None:
                        result["domain_rank"] = rank

        # Scoring System
        score = 0
        if result["brand_in_snippet"]:
            score += 40  # Highest value for AI overview/snippet
        if result["brand_in_knowledge_panel"]:
            score += 25
        if result["brand_in_organic"]:
            rank_val = result["organic_rank"] or 10
            score += max(5, 25 - (rank_val * 2))  # Better rank = more points
        if result["brand_in_people_also_ask"]:
            score += 10
        if result["domain_rank"] and result["domain_rank"] <= 3:
            score += 10

        result["visibility_score"] = min(100, score)

    except Exception as e:
        result["error"] = str(e)

    return result


def run_geo_monitor(brand: str, queries: list, domain: str = None) -> dict:
    """Run full Google tracking across multiple queries using Playwright."""
    results = []
    total_score = 0
    queries_with_mention = 0
    snippet_appearances = 0

    print(f"\n🔍 Google AI Overview Monitor (Playwright) — {brand}")
    print(f"{'='*50}")
    print(f"Checking {len(queries)} queries via headless browser\n")

    with sync_playwright() as p:
        browser, context = create_browser_context(p)
        page = context.new_page()

        for i, query in enumerate(queries, 1):
            print(f"[{i}/{len(queries)}] Query: \"{query}\"")

            result = check_google_serp(page, query, brand, domain)

            if result.get("error"):
                print(f"  ❌ Error: {result['error']}\n")
                results.append(result)
                continue

            total_score += result["visibility_score"]
            any_mention = any([
                result["brand_in_snippet"],
                result["brand_in_knowledge_panel"],
                result["brand_in_organic"],
                result["brand_in_people_also_ask"],
            ])

            if any_mention:
                queries_with_mention += 1
            if result["brand_in_snippet"]:
                snippet_appearances += 1

            placements = []
            if result["brand_in_snippet"]:
                placements.append("AI Snippet")
            if result["brand_in_knowledge_panel"]:
                placements.append("Knowledge Panel")
            if result["brand_in_organic"]:
                placements.append(f"Organic #{result['organic_rank']}")
            if result["brand_in_people_also_ask"]:
                placements.append("People Also Ask")

            if placements:
                print(f"  ✅ FOUND in: {', '.join(placements)} | Score: {result['visibility_score']}/100")
            else:
                print(f"  ❌ NOT FOUND | Score: 0/100")

            if result["domain_rank"]:
                print(f"  Domain rank: #{result['domain_rank']}")

            results.append(result)
            print()

        browser.close()

    avg_score = round(total_score / len(queries), 1) if queries else 0
    citation_rate = round(queries_with_mention / len(queries) * 100, 1) if queries else 0

    summary = {
        "brand": brand,
        "domain": domain,
        "platform": "Google Search (Playwright Scraper)",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "queries_tested": len(queries),
        "queries_with_brand_presence": queries_with_mention,
        "ai_snippet_appearances": snippet_appearances,
        "visibility_rate_pct": citation_rate,
        "average_visibility_score": avg_score,
        "results": results,
    }

    print(f"{'='*50}")
    print(f"📊 GOOGLE GEO SUMMARY — {brand}")
    print(f"  Visibility Rate: {citation_rate}% ({queries_with_mention}/{len(queries)} queries)")
    print(f"  AI Snippet Appearances: {snippet_appearances}/{len(queries)}")
    print(f"  Average Visibility Score: {avg_score}/100")
    
    return summary


def main():
    parser = argparse.ArgumentParser(description="Check brand visibility in Google via Playwright")
    parser.add_argument("--brand", required=True, help="Brand name to monitor")
    parser.add_argument("--domain", help="Brand domain for rank tracking")
    parser.add_argument("--queries", nargs="+", help="Queries to check")
    parser.add_argument("--output", help="Save JSON results to file path")
    args = parser.parse_args()

    queries = args.queries or [
        f"who is {args.brand}",
        f"{args.brand} reviews",
        f"{args.brand} services",
    ]

    result = run_geo_monitor(
        brand=args.brand,
        queries=queries,
        domain=args.domain,
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Results saved to: {args.output}")


if __name__ == "__main__":
    main()
