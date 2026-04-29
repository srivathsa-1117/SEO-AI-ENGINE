#!/usr/bin/env python3
"""
SERP & Data Scraper Tool — ENTERPRISE EDITION
Powered by DataForSEO API (primary) with Playwright fallback.

Handles multiple scraping modes:
  - autosuggest: Google Autocomplete suggestions
  - trends: Google Trends data via pytrends
  - serp_top10: Top 10 organic results for a keyword [DATAFORSEO POWERED]
  - competitor_gap: Keyword gap vs competitor pages
  - link_prospects: Find guest post / resource page opportunities
  - unlinked_mentions: Find unlinked brand mentions
  - find_email: Extract contact emails from URLs

Usage:
    python serp_scraper.py --mode autosuggest --keyword "project management software"
    python serp_scraper.py --mode trends --keywords "keyword1,keyword2,keyword3"
    python serp_scraper.py --mode serp_top10 --keyword "best CRM software" [USES DATAFORSEO]
    python serp_scraper.py --mode serp_top10 --keyword "best CRM software" --fallback [USES PLAYWRIGHT]
    python serp_scraper.py --mode link_prospects --industry "marketing" --type guest_post
"""

import argparse
import json
import time
import re
import string
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse, quote_plus
import os

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "requests", "beautifulsoup4", "lxml"], check=True)
    import requests
    from bs4 import BeautifulSoup

# Import DataForSEO client
try:
    from dataforseo_client import DataForSEOClient
    DATAFORSEO_AVAILABLE = True
except ImportError:
    DATAFORSEO_AVAILABLE = False
    print("[Warning] DataForSEO client not available. Using Playwright fallback only.")


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


# ===========================
# AUTOSUGGEST
# ===========================
def scrape_autosuggest(keyword: str, location: str = "us") -> dict:
    """Scrape Google Autocomplete for a keyword with A-Z suffix variations."""
    suggestions = []
    session = requests.Session()
    session.headers.update(HEADERS)

    # Base keyword
    suffixes = [""] + list(string.ascii_lowercase)

    for suffix in suffixes:
        query = f"{keyword} {suffix}".strip()
        url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={quote_plus(query)}&hl=en&gl={location}"
        try:
            resp = session.get(url, timeout=10)
            data = resp.json()
            new_suggestions = data[1] if len(data) > 1 else []
            for s in new_suggestions:
                if s not in suggestions and s != keyword:
                    suggestions.append(s)
        except Exception as e:
            print(f"  [Autosuggest] Error for suffix '{suffix}': {e}")
        time.sleep(0.3)

    # Also scrape People Also Ask
    paa_questions = scrape_paa(keyword, session)

    return {
        "keyword": keyword,
        "suggestions": suggestions,
        "paa_questions": paa_questions,
        "total_found": len(suggestions),
        "scraped_at": datetime.now().isoformat()
    }


def scrape_paa(keyword: str, session: requests.Session) -> list:
    """Scrape People Also Ask questions for a keyword."""
    url = f"https://www.google.com/search?q={quote_plus(keyword)}&hl=en"
    questions = []
    try:
        resp = session.get(url, timeout=15)
        soup = BeautifulSoup(resp.text, "lxml")
        # PAA questions are typically in <div> with jsname attribute or data-expandable
        for el in soup.find_all(attrs={"data-q": True}):
            q = el.get("data-q", "").strip()
            if q and q not in questions:
                questions.append(q)

        # Fallback: look for question-like text in results
        for el in soup.find_all("div", class_=re.compile("related")):
            text = el.get_text(strip=True)
            if text.endswith("?") and len(text) > 20:
                questions.append(text)

    except Exception as e:
        print(f"  [PAA] Error: {e}")
    return questions[:20]  # Return up to 20


# ===========================
# GOOGLE TRENDS
# ===========================
def fetch_trends(keywords: list) -> dict:
    """Fetch Google Trends interest data for a list of keywords."""
    try:
        from pytrends.request import TrendReq
    except ImportError:
        import subprocess
        subprocess.run(["pip", "install", "pytrends"], check=True)
        from pytrends.request import TrendReq

    pytrends = TrendReq(hl="en-US", tz=360, timeout=(10, 25))
    results = {}

    # pytrends handles max 5 keywords at once
    for i in range(0, len(keywords), 5):
        batch = keywords[i:i+5]
        try:
            pytrends.build_payload(batch, timeframe="today 12-m")
            interest = pytrends.interest_over_time()
            if not interest.empty:
                for kw in batch:
                    if kw in interest.columns:
                        series = interest[kw]
                        results[kw] = {
                            "avg_interest": int(series.mean()),
                            "trend": "Rising" if series.iloc[-1] > series.iloc[0] else "Declining" if series.iloc[-1] < series.iloc[0] else "Stable",
                            "peak_month": series.idxmax().strftime("%B") if not series.empty else "N/A",
                        }
        except Exception as e:
            print(f"  [Trends] Error for batch {batch}: {e}")
        time.sleep(1)

    return {"trends": results, "scraped_at": datetime.now().isoformat()}


# ===========================
# SERP TOP 10 — DATAFORSEO EDITION
# ===========================
def scrape_serp_top10(keyword: str, use_fallback: bool = False, location_code: int = 2840) -> dict:
    """
    Scrape the top 10 organic Google results for a keyword.

    Priority:
      1. DataForSEO API (100% reliable, CAPTCHA-free, $0.001/query)
      2. Playwright (if DataForSEO unavailable or --fallback flag used)
      3. Requests (last resort)

    Args:
        keyword: Search query
        use_fallback: Force use of Playwright instead of DataForSEO
        location_code: DataForSEO location code (2840 = USA, 2356 = India)

    Returns:
        Dictionary with keyword and results array
    """

    # Try DataForSEO first (unless fallback is forced)
    if DATAFORSEO_AVAILABLE and not use_fallback:
        try:
            print(f"  [SERP] Using DataForSEO API (enterprise-grade, CAPTCHA-free)")
            client = DataForSEOClient()
            results = client.get_serp_results(keyword, location_code=location_code, depth=10)

            if results:
                return {
                    "keyword": keyword,
                    "results": results,
                    "source": "dataforseo_api",
                    "cost_usd": 0.001,
                    "scraped_at": datetime.now().isoformat()
                }
            else:
                print(f"  [SERP] DataForSEO returned no results, trying Playwright fallback...")

        except Exception as e:
            print(f"  [SERP] DataForSEO error: {e}")
            print(f"  [SERP] Falling back to Playwright...")

    # Fallback to Playwright
    results = []

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  [SERP] Playwright not installed, falling back to requests (less reliable)")
        return scrape_serp_top10_fallback(keyword)

    url = f"https://www.google.com/search?q={quote_plus(keyword)}&num=10&hl=en"

    try:
        with sync_playwright() as p:
            # Launch browser in headless mode with stealth settings
            browser = p.chromium.launch(
                headless=True,
                args=['--disable-blink-features=AutomationControlled']
            )

            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )

            page = context.new_page()

            # Navigate to Google search
            page.goto(url, wait_until='networkidle', timeout=30000)

            # Wait a bit for JS rendering
            page.wait_for_timeout(2000)

            # Get page content
            html = page.content()
            soup = BeautifulSoup(html, "lxml")

            # Try multiple selectors for organic results
            result_divs = soup.find_all("div", class_="g") or \
                         soup.find_all("div", {"data-hveid": True})

            for g in result_divs[:10]:  # Limit to top 10
                link = g.find("a", href=True)
                h3 = g.find("h3")

                # Try multiple snippet selectors
                snippet_el = (g.find("div", attrs={"data-sncf": True}) or
                             g.find("span", class_="aCOpRe") or
                             g.find("div", class_="VwiC3b"))

                if link and h3:
                    href = link.get("href", "")
                    # Filter out non-organic results
                    if href.startswith("http") and not any(x in href for x in ["/search?", "google.com/search"]):
                        results.append({
                            "position": len(results) + 1,
                            "url": href,
                            "title": h3.get_text(strip=True),
                            "snippet": snippet_el.get_text(strip=True) if snippet_el else "",
                            "domain": urlparse(href).netloc,
                        })

                        if len(results) >= 10:
                            break

            browser.close()

        if not results:
            print("  [SERP] Warning: No results found with Playwright. Google may have shown CAPTCHA.")
            print("  [SERP] Trying fallback method...")
            return scrape_serp_top10_fallback(keyword)

    except Exception as e:
        print(f"  [SERP] Playwright error: {e}")
        print("  [SERP] Trying fallback method...")
        return scrape_serp_top10_fallback(keyword)

    return {
        "keyword": keyword,
        "results": results,
        "source": "playwright_scraper",
        "cost_usd": 0,
        "scraped_at": datetime.now().isoformat()
    }


def scrape_serp_top10_fallback(keyword: str) -> dict:
    """Fallback method using requests (less reliable, kept for compatibility)."""
    session = requests.Session()
    session.headers.update(HEADERS)

    url = f"https://www.google.com/search?q={quote_plus(keyword)}&num=10&hl=en"
    results = []

    try:
        resp = session.get(url, timeout=15)
        soup = BeautifulSoup(resp.text, "lxml")

        for g in soup.find_all("div", class_="g"):
            link = g.find("a", href=True)
            h3 = g.find("h3")
            snippet_el = g.find("div", attrs={"data-sncf": True}) or g.find("span", class_="aCOpRe")

            if link and h3:
                results.append({
                    "position": len(results) + 1,
                    "url": link["href"],
                    "title": h3.get_text(strip=True),
                    "snippet": snippet_el.get_text(strip=True) if snippet_el else "",
                    "domain": urlparse(link["href"]).netloc,
                })

        if not results:
            print("  [SERP] Warning: No results found. Google blocked the request.")
            print("  [SERP] Recommendation: This feature requires Playwright for reliable scraping.")
            print("  [SERP] Install with: pip install playwright && playwright install chromium")

    except Exception as e:
        print(f"  [SERP] Error: {e}")

    return {
        "keyword": keyword,
        "results": results,
        "source": "requests_fallback",
        "cost_usd": 0,
        "scraped_at": datetime.now().isoformat()
    }


# ===========================
# LINK PROSPECTS
# ===========================
def find_link_prospects(industry: str, prospect_type: str = "guest_post") -> dict:
    """Find backlink opportunities using Google advanced search operators."""
    session = requests.Session()
    session.headers.update(HEADERS)

    queries = {
        "guest_post": [
            f'"{industry}" "write for us"',
            f'"{industry}" "guest post guidelines"',
            f'"{industry}" "submit a guest post"',
            f'"{industry}" "become a contributor"',
        ],
        "resource_links": [
            f'"{industry}" inurl:resources',
            f'"{industry}" "helpful resources"',
            f'"{industry}" "tools and resources"',
            f'"{industry}" "best tools"',
        ],
        "unlinked_mentions": [],  # handled separately
    }

    prospects = []
    for query in queries.get(prospect_type, []):
        url = f"https://www.google.com/search?q={quote_plus(query)}&num=10&hl=en"
        try:
            resp = session.get(url, timeout=15)
            soup = BeautifulSoup(resp.text, "lxml")
            for g in soup.find_all("div", class_="g"):
                link = g.find("a", href=True)
                h3 = g.find("h3")
                if link and h3:
                    domain = urlparse(link["href"]).netloc
                    # Filter out massive sites (unlikely to respond)
                    if not any(skip in domain for skip in ["forbes.com", "huffpost.com", "entrepreneur.com"]):
                        prospects.append({
                            "url": link["href"],
                            "domain": domain,
                            "title": h3.get_text(strip=True),
                            "source_query": query,
                            "type": prospect_type,
                        })
            time.sleep(1)
        except Exception as e:
            print(f"  [Prospects] Error for query '{query}': {e}")

    # Deduplicate by domain
    seen_domains = set()
    unique_prospects = []
    for p in prospects:
        if p["domain"] not in seen_domains:
            seen_domains.add(p["domain"])
            unique_prospects.append(p)

    return {
        "industry": industry,
        "type": prospect_type,
        "prospects": unique_prospects,
        "total_found": len(unique_prospects),
        "scraped_at": datetime.now().isoformat()
    }


# ===========================
# EMAIL FINDER
# ===========================
def find_contact_email(url: str) -> dict:
    """Try to find a contact email for a given website."""
    session = requests.Session()
    session.headers.update(HEADERS)
    base_domain = urlparse(url).netloc
    email_pattern = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")

    emails_found = set()
    pages_to_check = [
        url,
        f"https://{base_domain}/contact",
        f"https://{base_domain}/about",
        f"https://{base_domain}/contact-us",
        f"https://{base_domain}/write-for-us",
    ]

    for page in pages_to_check:
        try:
            resp = session.get(page, timeout=10)
            if resp.status_code == 200:
                emails = set(email_pattern.findall(resp.text))
                # Filter out generic/system emails
                filtered = {e for e in emails if not any(skip in e for skip in
                    ["example.com", "sentry.io", "yoursite", "noreply", "no-reply"])}
                emails_found.update(filtered)
        except Exception:
            pass
        time.sleep(0.5)

    return {
        "domain": base_domain,
        "emails_found": list(emails_found),
        "has_contact": len(emails_found) > 0,
    }


# ===========================
# MAIN
# ===========================
def main():
    parser = argparse.ArgumentParser(description="SEO SERP and Data Scraper — DataForSEO Edition")
    parser.add_argument("--mode", required=True, choices=["autosuggest", "trends", "serp_top10", "link_prospects", "find_email"])
    parser.add_argument("--keyword", help="Primary keyword")
    parser.add_argument("--keywords", help="Comma-separated list of keywords (for trends)")
    parser.add_argument("--industry", help="Industry/niche (for link_prospects)")
    parser.add_argument("--type", default="guest_post", choices=["guest_post", "resource_links"], help="Prospect type")
    parser.add_argument("--url", help="URL to check (for find_email)")
    parser.add_argument("--location", default="us", help="Country code for autosuggest")
    parser.add_argument("--location-code", type=int, default=2840, help="DataForSEO location code (2840=USA, 2356=India)")
    parser.add_argument("--fallback", action="store_true", help="Force Playwright instead of DataForSEO")
    parser.add_argument("--output", help="Output JSON file path")
    args = parser.parse_args()

    data = {}
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if args.mode == "autosuggest":
        assert args.keyword, "--keyword is required for autosuggest mode"
        print(f"[Autosuggest] Scraping for: {args.keyword}")
        data = scrape_autosuggest(args.keyword, args.location)

    elif args.mode == "trends":
        keywords = [k.strip() for k in (args.keywords or args.keyword or "").split(",") if k.strip()]
        assert keywords, "--keywords or --keyword is required for trends mode"
        print(f"[Trends] Fetching trends for {len(keywords)} keywords")
        data = fetch_trends(keywords)

    elif args.mode == "serp_top10":
        assert args.keyword, "--keyword is required for serp_top10 mode"
        print(f"[SERP] Scraping top 10 results for: {args.keyword}")
        data = scrape_serp_top10(args.keyword, use_fallback=args.fallback, location_code=args.location_code)

    elif args.mode == "link_prospects":
        assert args.industry, "--industry is required for link_prospects mode"
        print(f"[Prospects] Finding {args.type} opportunities for: {args.industry}")
        data = find_link_prospects(args.industry, args.type)

    elif args.mode == "find_email":
        assert args.url, "--url is required for find_email mode"
        print(f"[Email] Finding contact info for: {args.url}")
        data = find_contact_email(args.url)

    # Save output
    output_path = args.output or f".tmp/{args.mode}_{timestamp}.json"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n[Output] Saved to: {output_path}")
    print(json.dumps(data, indent=2, ensure_ascii=False)[:2000] + "..." if len(json.dumps(data)) > 2000 else json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
