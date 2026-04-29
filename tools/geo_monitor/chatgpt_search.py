#!/usr/bin/env python3
"""
GEO Monitor — ChatGPT Brand Visibility Checker (Playwright Scraper)

Uses Playwright to open a real headless browser, query ChatGPT,
and check if a brand is cited in the AI-generated answers.

Usage:
    python tools/geo_monitor/chatgpt_search.py --brand "Example Brand" --queries "top digital marketing agencies India"
    python tools/geo_monitor/chatgpt_search.py --brand "Acme Corp" --domain acmecorp.com

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
        locale="en-US"
    )
    return browser, context


def check_chatgpt(page, query: str, brand: str, domain: str = None) -> dict:
    """Scrape ChatGPT for brand mentions using Playwright (Open search without login)."""
    # ChatGPT now allows open search without login at chatgpt.com
    url = f"https://chatgpt.com/?q={quote_plus(query)}"

    result = {
        "query": query,
        "url": url,
        "brand_mentioned": False,
        "mention_count": 0,
        "domain_mentioned": False,
        "first_mention_position_pct": -1,
        "visibility_score": 0,
        "error": None,
        "content_preview": ""
    }

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        
        # Give generation time to finish
        # We wait for typical length of a standard response
        page.wait_for_timeout(random.randint(15000, 20000))
        
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        
        # Extract main answer text
        content = ""
        
        # ChatGPT uses div with 'markdown' class for assistant messages
        markdown_blocks = soup.find_all("div", class_=lambda c: c and "markdown" in c.lower())
        
        if markdown_blocks:
            # Get the last markdown block (the most recent answer)
            content = markdown_blocks[-1].get_text(separator=" ", strip=True)
        else:
            # Fallback
            main_area = soup.find("main")
            if main_area:
                content = main_area.get_text(separator=" ", strip=True)
            else:
                content = soup.get_text(separator=" ", strip=True)

        result["content_preview"] = content[:300] + "..." if len(content) > 300 else content

        content_lower = content.lower()
        brand_lower = brand.lower()
        domain_lower = domain.lower() if domain else None

        mentions = content_lower.count(brand_lower)
        domain_mentions = content_lower.count(domain_lower) if domain else 0
        
        total_len = len(content_lower)
        first_pos = content_lower.find(brand_lower)
        position_pct = round((first_pos / total_len * 100), 1) if first_pos >= 0 and total_len > 0 else -1

        result["brand_mentioned"] = mentions > 0
        result["mention_count"] = mentions
        result["domain_mentioned"] = domain_mentions > 0
        result["first_mention_position_pct"] = position_pct

        # Score calculation
        score = 0
        if mentions > 0:
            score += min(50, mentions * 15)
            
            if 0 <= position_pct < 20:
                score += 30
            elif position_pct < 50:
                score += 15
                
            if domain_mentions > 0:
                score += 20

        result["visibility_score"] = min(100, score)

    except Exception as e:
        result["error"] = str(e)

    return result


def run_geo_monitor(brand: str, queries: list, domain: str = None) -> dict:
    """Run full ChatGPT tracking across queries via Playwright."""
    results = []
    total_score = 0
    queries_with_mention = 0

    print(f"\n🔍 ChatGPT Monitor (Playwright) — {brand}")
    print(f"{'='*50}")
    print(f"Checking {len(queries)} queries via headless browser\n")

    with sync_playwright() as p:
        browser, context = create_browser_context(p)
        page = context.new_page()

        for i, query in enumerate(queries, 1):
            print(f"[{i}/{len(queries)}] Query: \"{query}\"")

            result = check_chatgpt(page, query, brand, domain)

            if result.get("error"):
                print(f"  ❌ Error: {result['error']}\n")
                results.append(result)
                continue

            total_score += result["visibility_score"]

            if result["brand_mentioned"]:
                queries_with_mention += 1
                status = "✅ CITED"
            else:
                status = "❌ NOT CITED"

            print(f"  {status} | Mentions: {result['mention_count']} | Score: {result['visibility_score']}/100")
            if result["brand_mentioned"]:
                print(f"  Position: {result['first_mention_position_pct']}% into answer")

            results.append(result)
            print()

        browser.close()

    avg_score = round(total_score / len(queries), 1) if queries else 0
    citation_rate = round(queries_with_mention / len(queries) * 100, 1) if queries else 0

    summary = {
        "brand": brand,
        "domain": domain,
        "platform": "ChatGPT (Playwright Scraper)",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "queries_tested": len(queries),
        "queries_with_brand_presence": queries_with_mention,
        "citation_rate_pct": citation_rate,
        "average_visibility_score": avg_score,
        "results": results,
    }

    print(f"{'='*50}")
    print(f"📊 CHATGPT GEO SUMMARY — {brand}")
    print(f"  Citation Rate: {citation_rate}% ({queries_with_mention}/{len(queries)})")
    print(f"  Average Visibility Score: {avg_score}/100")
    
    return summary


def main():
    parser = argparse.ArgumentParser(description="Check brand visibility in ChatGPT via Playwright")
    parser.add_argument("--brand", required=True, help="Brand name to monitor")
    parser.add_argument("--domain", help="Brand domain tracking")
    parser.add_argument("--queries", nargs="+", help="Queries to check")
    parser.add_argument("--output", help="Save JSON results to file path")
    args = parser.parse_args()

    queries = args.queries or [
        f"who is {args.brand}",
        f"reviews of {args.brand}",
        f"is {args.brand} legit",
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
