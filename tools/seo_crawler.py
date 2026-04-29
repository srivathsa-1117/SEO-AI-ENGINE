#!/usr/bin/env python3
"""
SEO Crawler Tool (Playwright Edition with Error Recovery)
Crawls a website to find all URLs, their HTTP status codes,
canonical tags, internal link structure, and SEO metadata.
Utilizes Playwright to render JavaScript & extruct to extract Schema.

Features:
- Automatic retry with exponential backoff
- Graceful degradation for blocked/failed requests
- User-friendly error messages with solutions
- Fallback to requests library if Playwright fails

Usage:
    python seo_crawler.py --url https://example.com --sitemap https://example.com/sitemap.xml
    python seo_crawler.py --url https://example.com --max-pages 500
"""

import argparse
import json
import asyncio
import re
import csv
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse
from datetime import datetime
from typing import Optional, Dict, List

try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError
    from bs4 import BeautifulSoup
    import extruct
    from w3lib.html import get_base_url
    import requests
except ImportError:
    print("[ERROR] Dependencies missing!")
    print("💡 Solution: Run the following command:")
    print("   pip install playwright extruct w3lib beautifulsoup4 requests && playwright install chromium")
    exit(1)


def normalize_url(url: str, base: str) -> str | None:
    """Normalize and validate a URL."""
    try:
        full = urljoin(base, url)
        parsed = urlparse(full)
        if parsed.scheme not in ("http", "https"):
            return None
        # Remove fragments
        return parsed._replace(fragment="").geturl()
    except Exception:
        return None

def extract_schema_types(html: str, url: str) -> list:
    """Uses extruct to cleanly extract all structured data (JSON-LD, Microdata, RDFa)."""
    schema_types = set()
    try:
        base_url = get_base_url(html, url)
        data = extruct.extract(html, base_url=base_url, syntaxes=['json-ld', 'microdata', 'rdfa'])
        
        # Deeply extract @type from any nested structure
        def find_types(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k == '@type':
                        if isinstance(v, list):
                            for item in v:
                                schema_types.add(str(item))
                        else:
                            schema_types.add(str(v))
                    else:
                        find_types(v)
            elif isinstance(obj, list):
                for item in obj:
                    find_types(item)
                    
        find_types(data)
    except Exception as e:
        pass
        
    return list(schema_types)

async def crawl_url_with_retry(page, url: str, timeout: int = 15000, max_retries: int = 3) -> dict:
    """Crawl a single URL with automatic retry and exponential backoff."""
    for attempt in range(max_retries):
        try:
            result = await crawl_url(page, url, timeout)
            if result.get("error") and attempt < max_retries - 1:
                wait_time = (2 ** attempt)  # Exponential backoff: 1s, 2s, 4s
                print(f"   [WARNING]  Retry {attempt + 1}/{max_retries} for {url} (waiting {wait_time}s)")
                await asyncio.sleep(wait_time)
                continue
            return result
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt)
                print(f"   [WARNING]  Retry {attempt + 1}/{max_retries} after error: {str(e)[:50]}")
                await asyncio.sleep(wait_time)
            else:
                return {
                    "url": url,
                    "status_code": None,
                    "error": f"Failed after {max_retries} retries: {str(e)[:100]}"
                }

    # Should never reach here, but safety fallback
    return {"url": url, "status_code": None, "error": "Unknown retry failure"}


async def crawl_url(page, url: str, timeout: int = 15000) -> dict:
    """Crawl a single URL and return its SEO metadata."""
    result = {
        "url": url,
        "status_code": None,
        "title": None,
        "meta_description": None,
        "h1": [],
        "canonical": None,
        "noindex": False,
        "internal_links": [],
        "images_missing_alt": 0,
        "word_count": 0,
        "schema_types": [],
        "error": None,
    }
    try:
        response = await page.goto(url, timeout=timeout, wait_until="domcontentloaded")
        if not response:
            result["error"] = "No response received (possible DNS/network issue)"
            return result

        result["status_code"] = response.status
        result["final_url"] = page.url

        # Handle non-200 responses
        if response.status == 403:
            result["error"] = "403 Forbidden - Site may be blocking automated crawlers"
            return result
        elif response.status == 429:
            result["error"] = "429 Rate Limited - Crawler is being throttled"
            return result
        elif response.status >= 500:
            result["error"] = f"{response.status} Server Error - Site experiencing issues"
            return result
        elif response.status != 200:
            return result

        # Wait a bit for JS frameworks (React/Next) to render
        await page.wait_for_timeout(1000)
        html = await page.content()

        if not html or len(html) < 100:
            result["error"] = "Empty or minimal HTML received"
            return result

        soup = BeautifulSoup(html, "lxml")

        # Title
        title_tag = soup.find("title")
        result["title"] = title_tag.get_text(strip=True) if title_tag else None

        # Meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        result["meta_description"] = meta_desc.get("content", "").strip() if meta_desc else None

        # H1s
        result["h1"] = [h.get_text(strip=True) for h in soup.find_all("h1")]

        # Canonical
        canonical = soup.find("link", attrs={"rel": "canonical"})
        result["canonical"] = canonical.get("href") if canonical else None

        # Noindex
        robots_meta = soup.find("meta", attrs={"name": re.compile("robots", re.I)})
        if robots_meta:
            content = robots_meta.get("content", "").lower()
            result["noindex"] = "noindex" in content

        # Internal links
        base_domain = urlparse(url).netloc
        for a in soup.find_all("a", href=True):
            normalized = normalize_url(a["href"], url)
            if normalized and urlparse(normalized).netloc == base_domain:
                if normalized not in result["internal_links"]:
                    result["internal_links"].append(normalized)

        # Images missing alt
        result["images_missing_alt"] = sum(
            1 for img in soup.find_all("img") if not img.get("alt")
        )

        # Word count (visible text)
        for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            tag.decompose()
        text = soup.get_text(separator=" ")
        result["word_count"] = len(text.split())

        # Schema types (Extruct)
        result["schema_types"] = extract_schema_types(html, url)

    except PlaywrightTimeoutError:
        result["error"] = "Timeout - Page took too long to load (increase timeout or check network)"
    except PlaywrightError as e:
        error_msg = str(e).lower()
        if "net::err_name_not_resolved" in error_msg:
            result["error"] = "DNS resolution failed - Check if domain exists"
        elif "net::err_connection_refused" in error_msg:
            result["error"] = "Connection refused - Site may be down or blocking"
        elif "net::err_cert" in error_msg:
            result["error"] = "SSL certificate error - Site has HTTPS issues"
        else:
            result["error"] = f"Playwright error: {str(e)[:100]}"
    except Exception as e:
        result["error"] = f"Unexpected error: {str(e)[:100]}"

    return result

async def async_crawl_site(start_url: str, sitemap_url: str = None, max_pages: int = 500, max_concurrency: int = 5) -> dict:
    """Crawl an entire website utilizing asyncio and Playwright workers."""
    base_domain = urlparse(start_url).netloc
    
    to_visit = [start_url]
    visited = set()
    to_visit_set = set([start_url])
    results = []
    
    # Add sitemap URLs if provided
    if sitemap_url:
        try:
            print(f"[Sitemap] Fetching {sitemap_url}...")
            resp = requests.get(sitemap_url, timeout=10, headers={
                'User-Agent': 'SEO-AI-OS-Crawler/2.0 (compatible; +https://github.com/youragency)'
            })
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "lxml-xml")
            sitemap_urls = {loc.get_text() for loc in soup.find_all("loc")}
            sitemap_valid = {u for u in sitemap_urls if urlparse(u).netloc == base_domain}
            for u in sitemap_valid:
                if u not in to_visit_set:
                    to_visit.append(u)
                    to_visit_set.add(u)
            print(f"[OK] [Sitemap] Added {len(sitemap_valid)} URLs from sitemap")
        except requests.exceptions.Timeout:
            print(f"[WARNING]  [Sitemap] Timeout fetching sitemap - will crawl from homepage only")
        except requests.exceptions.HTTPError as e:
            print(f"[WARNING]  [Sitemap] HTTP {e.response.status_code} error - sitemap may not exist")
        except Exception as e:
            print(f"[WARNING]  [Sitemap] Could not parse sitemap: {str(e)[:80]}")
            print(f"💡 Continuing with homepage crawl only")

    print(f"[Crawl] Starting Playwright async crawl of {start_url} (max {max_pages} pages)")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Create a pool of pages based on concurrency
        context = await browser.new_context(
            user_agent="SEO-AI-OS-Crawler/2.0 (Playwright Bot; contact@youragency.com)"
        )
        
        async def worker(worker_id):
            while True:
                if not to_visit or len(visited) >= max_pages:
                    break
                
                try:
                    url = to_visit.pop(0)
                except IndexError:
                    break
                    
                if url in visited:
                    continue
                visited.add(url)
                print(f"[{len(visited)}/{max_pages}] Crawling: {url}")

                page = await context.new_page()
                # Block heavy resources like images to speed up crawling
                try:
                    await page.route("**/*", lambda route: route.continue_() if route.request.resource_type in ["document", "script", "xhr", "fetch"] else route.abort())
                except Exception as e:
                    print(f"[WARNING]  Warning: Could not set up resource blocking: {str(e)[:50]}")

                try:
                    result = await crawl_url_with_retry(page, url)
                    results.append(result)

                    # Only add links if crawl was successful
                    if result.get("status_code") == 200 and not result.get("error"):
                        for link in result.get("internal_links", []):
                            if link not in visited and link not in to_visit_set and urlparse(link).netloc == base_domain:
                                to_visit.append(link)
                                to_visit_set.add(link)
                except Exception as e:
                    print(f"[ERROR] Worker {worker_id} error: {str(e)[:80]}")
                finally:
                    await page.close()

        workers = [worker(i) for i in range(min(max_concurrency, max_pages))]
        await asyncio.gather(*workers)
        await browser.close()

    # Calculate error statistics
    pages_with_errors = [p for p in results if p.get("error")]
    error_summary = {}
    for page in pages_with_errors:
        error_type = page["error"].split("-")[0].strip()  # Get first part of error message
        error_summary[error_type] = error_summary.get(error_type, 0) + 1

    return {
        "crawl_date": datetime.now().isoformat(),
        "start_url": start_url,
        "pages_crawled": len(results),
        "pages": results,
        "summary": {
            "total_pages": len(results),
            "status_200": sum(1 for p in results if p.get("status_code") == 200),
            "status_301": sum(1 for p in results if p.get("status_code") in [301, 302, 307, 308]),
            "status_404": sum(1 for p in results if p.get("status_code") == 404),
            "status_500": sum(1 for p in results if p.get("status_code", 0) and p.get("status_code", 0) >= 500),
            "missing_h1": sum(1 for p in results if not p.get("h1") and p.get("status_code") == 200),
            "missing_title": sum(1 for p in results if not p.get("title") and p.get("status_code") == 200),
            "missing_meta_desc": sum(1 for p in results if not p.get("meta_description") and p.get("status_code") == 200),
            "noindex_pages": sum(1 for p in results if p.get("noindex") and p.get("status_code") == 200),
            "pages_with_errors": len(pages_with_errors),
            "error_breakdown": error_summary
        }
    }

def crawl_site_nojs(start_url: str, sitemap_url: str = None, max_pages: int = 500) -> dict:
    """Crawl site without JavaScript - Google's perspective using requests library."""
    base_domain = urlparse(start_url).netloc
    to_visit = [start_url]
    visited = set()
    results = []

    # Add sitemap URLs if provided
    if sitemap_url:
        try:
            print(f"[Sitemap] Fetching {sitemap_url}...")
            resp = requests.get(sitemap_url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
            })
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "lxml-xml")
            sitemap_urls = {loc.get_text() for loc in soup.find_all("loc")}
            sitemap_valid = {u for u in sitemap_urls if urlparse(u).netloc == base_domain}
            to_visit.extend(list(sitemap_valid))
            print(f"[OK] [Sitemap] Added {len(sitemap_valid)} URLs from sitemap")
        except Exception as e:
            print(f"[WARNING] [Sitemap] Could not parse sitemap: {str(e)[:80]}")

    print(f"[Crawl] Starting no-JS crawl (requests library) - max {max_pages} pages")

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue

        visited.add(url)
        print(f"[{len(visited)}/{max_pages}] Crawling (no-JS): {url}")

        result = {
            "url": url,
            "status_code": None,
            "title": None,
            "meta_description": None,
            "h1": [],
            "canonical": None,
            "noindex": False,
            "internal_links": [],
            "images_missing_alt": 0,
            "word_count": 0,
            "schema_types": [],
            "error": None,
        }

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
            }
            resp = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
            result["status_code"] = resp.status_code
            result["final_url"] = resp.url

            if resp.status_code != 200:
                result["error"] = f"HTTP {resp.status_code}"
                results.append(result)
                continue

            soup = BeautifulSoup(resp.text, "lxml")

            # Title
            title_tag = soup.find("title")
            result["title"] = title_tag.get_text(strip=True) if title_tag else None

            # Meta description
            meta_desc = soup.find("meta", attrs={"name": "description"})
            result["meta_description"] = meta_desc.get("content", "").strip() if meta_desc else None

            # H1s
            result["h1"] = [h.get_text(strip=True) for h in soup.find_all("h1")]

            # Canonical
            canonical = soup.find("link", attrs={"rel": "canonical"})
            result["canonical"] = canonical.get("href") if canonical else None

            # Noindex
            robots_meta = soup.find("meta", attrs={"name": re.compile("robots", re.I)})
            if robots_meta:
                content = robots_meta.get("content", "").lower()
                result["noindex"] = "noindex" in content

            # Internal links
            for a in soup.find_all("a", href=True):
                normalized = normalize_url(a["href"], url)
                if normalized and urlparse(normalized).netloc == base_domain:
                    if normalized not in result["internal_links"]:
                        result["internal_links"].append(normalized)
                    if normalized not in visited and normalized not in to_visit:
                        to_visit.append(normalized)

            # Images missing alt
            result["images_missing_alt"] = sum(
                1 for img in soup.find_all("img") if not img.get("alt")
            )

            # Word count
            for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
                tag.decompose()
            text = soup.get_text(separator=" ")
            result["word_count"] = len(text.split())

            # Schema types
            result["schema_types"] = extract_schema_types(resp.text, url)

        except requests.exceptions.Timeout:
            result["error"] = "Timeout"
        except requests.exceptions.RequestException as e:
            result["error"] = f"Request error: {str(e)[:100]}"
        except Exception as e:
            result["error"] = f"Unexpected error: {str(e)[:100]}"

        results.append(result)
        time.sleep(0.5)  # Rate limiting

    return {
        "crawl_date": datetime.now().isoformat(),
        "start_url": start_url,
        "crawl_mode": "no-js",
        "pages_crawled": len(results),
        "pages": results,
        "summary": {
            "total_pages": len(results),
            "status_200": sum(1 for p in results if p.get("status_code") == 200),
            "status_301": sum(1 for p in results if p.get("status_code") in [301, 302, 307, 308]),
            "status_404": sum(1 for p in results if p.get("status_code") == 404),
            "status_500": sum(1 for p in results if p.get("status_code", 0) and p.get("status_code", 0) >= 500),
            "missing_h1": sum(1 for p in results if not p.get("h1") and p.get("status_code") == 200),
            "missing_title": sum(1 for p in results if not p.get("title") and p.get("status_code") == 200),
            "missing_meta_desc": sum(1 for p in results if not p.get("meta_description") and p.get("status_code") == 200),
            "noindex_pages": sum(1 for p in results if p.get("noindex") and p.get("status_code") == 200),
        }
    }

def main():
    parser = argparse.ArgumentParser(description="SEO Async Playwright Crawler with Error Recovery")
    parser.add_argument("--url", required=True, help="Website URL to crawl")
    parser.add_argument("--sitemap", help="Sitemap XML URL")
    parser.add_argument("--max-pages", type=int, default=500, help="Maximum pages to crawl")
    parser.add_argument("--concurrency", type=int, default=5, help="Number of concurrent pages to crawl")
    parser.add_argument("--output", help="Output JSON file path")
    parser.add_argument("--no-js", action="store_true", help="Disable JavaScript rendering (Google's perspective - uses requests only)")
    args = parser.parse_args()

    # Validate URL format
    if not args.url.startswith(("http://", "https://")):
        print("[ERROR] Error: URL must start with http:// or https://")
        print(f"💡 You provided: {args.url}")
        print(f"💡 Try: https://{args.url}")
        exit(1)

    # Create event loop properly to avoid Windows asyncio issues
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    try:
        if args.no_js:
            print("[Mode] No-JS crawl enabled - using requests library (Google's perspective)")
            data = crawl_site_nojs(args.url, args.sitemap, args.max_pages)
        else:
            data = asyncio.run(async_crawl_site(args.url, args.sitemap, args.max_pages, args.concurrency))
    except PlaywrightError as e:
        error_msg = str(e).lower()
        if "executable doesn't exist" in error_msg or "browser executable not found" in error_msg:
            print("\n[ERROR] Playwright browsers not installed!")
            print("💡 Solution: Run this command:")
            print("   playwright install chromium")
            exit(1)
        else:
            print(f"\n[ERROR] Playwright error: {str(e)}")
            print("💡 Check your internet connection and try again")
            exit(1)
    except KeyboardInterrupt:
        print("\n[WARNING]  Crawl interrupted by user")
        exit(0)
    except Exception as e:
        print(f"\n[Error] Unexpected error: {str(e)}")
        print("[Tip] Please report this issue with the full error message")
        raise

    # Save output FIRST before any print statements that might crash
    base_name = urlparse(args.url).netloc
    output_path = args.output or f".tmp/crawl_{base_name}_{datetime.now().strftime('%Y%m%d')}.json"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n[Success] Output saved to: {output_path}")
    except IOError as e:
        print(f"\n[Error] Could not save file: {str(e)}")
        print("[Tip] Check that the output directory is writable")
        exit(1)

    # Print summary with better formatting (using ASCII-safe symbols)
    print("\n" + "="*60)
    print("CRAWL SUMMARY")
    print("="*60)
    summary = data["summary"]

    # Status codes
    print(f"\nHTTP Status Codes:")
    print(f"   [OK] 200 OK:        {summary['status_200']}")
    print(f"   [->] 301/302:       {summary['status_301']}")
    print(f"   [X] 404 Not Found: {summary['status_404']}")
    print(f"   [!] 5xx Errors:    {summary['status_500']}")

    # SEO issues
    print(f"\nOn-Page SEO Issues:")
    print(f"   Missing H1:           {summary['missing_h1']}")
    print(f"   Missing Title:        {summary['missing_title']}")
    print(f"   Missing Meta Desc:    {summary['missing_meta_desc']}")
    print(f"   Noindex Pages:        {summary['noindex_pages']}")

    # Errors
    if summary.get('pages_with_errors', 0) > 0:
        print(f"\n[Warning] Crawl Errors: {summary['pages_with_errors']} pages")
        if summary.get('error_breakdown'):
            print("   Error breakdown:")
            for error_type, count in summary['error_breakdown'].items():
                print(f"   - {error_type}: {count}")
    else:
        print(f"\n[Success] No crawl errors - all pages loaded successfully!")

    print("="*60 + "\n")

if __name__ == "__main__":
    import os
    main()
