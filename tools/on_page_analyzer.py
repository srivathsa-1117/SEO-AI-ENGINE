#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
On-Page Analyzer Tool with Error Recovery
Analyzes on-page SEO health: titles, meta, headings, images, canonical, schema.

Features:
- Automatic retry with exponential backoff
- Graceful degradation for partial data
- User-friendly error messages
- Handles rate limiting and timeouts

Usage:
    python on_page_analyzer.py --urls "https://example.com/page1"
    python on_page_analyzer.py --client acme_corp --top 10 --keyword "target keyword"
"""

import argparse
import json
import time
import re
import sys
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
from typing import Dict, List, Optional

# Fix Windows console encoding for emoji support
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        # Python < 3.7
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

import os as _os
_sys_path_tools = _os.path.dirname(_os.path.abspath(__file__))
if _sys_path_tools not in sys.path:
    sys.path.insert(0, _sys_path_tools)
from utils import smart_fetch

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("[ERROR] Dependencies missing!")
    print("💡 Solution: pip install requests beautifulsoup4 lxml")
    import subprocess
    subprocess.run(["pip", "install", "requests", "beautifulsoup4", "lxml"], check=True)
    import requests
    from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; SEO-AI-OS-OnPage/1.0)"}
TITLE_MIN, TITLE_MAX = 50, 60
META_MIN, META_MAX = 120, 160


def fetch_with_retry(url: str, max_retries: int = 3):
    """
    Fetch URL using smart_fetch (curl_cffi → DataForSEO fallback).
    Returns a duck-typed object with .status_code and .text,
    or a dict with parsed_data when DataForSEO was used.
    """
    result = smart_fetch(url, timeout=25)
    if result["success"]:
        return result  # caller checks result["html"] vs result["parsed_data"]
    # Last-resort: plain requests (original behaviour for non-bot-protected sites)
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        return {"success": True, "html": resp.text, "status_code": resp.status_code,
                "url": resp.url, "method": "requests", "parsed_data": None, "error": None}
    except Exception as e:
        return {"success": False, "html": None, "status_code": 0, "url": url,
                "method": None, "parsed_data": None, "error": str(e)}


def analyze_page(url: str, keyword: str = None) -> dict:
    result = {
        "url": url,
        "analyzed_at": datetime.now().isoformat(),
        "issues": [],
        "overall_score": 0,
        "error": None
    }

    try:
        fetch = fetch_with_retry(url)
        if not fetch or not fetch.get("success"):
            result["error"] = fetch.get("error", "Failed to fetch") if fetch else "Failed to fetch"
            result["issues"].append("CRITICAL: Could not fetch page (bot protection or network error)")
            return result

        result["status_code"] = fetch.get("status_code", 0)

        # ── DataForSEO path: use pre-parsed data directly ────────────────────
        if fetch.get("parsed_data"):
            pd = fetch["parsed_data"]
            title    = pd.get("title") or ""
            meta     = pd.get("meta_description") or ""
            h1s      = pd.get("h1") or []
            h2s      = pd.get("h2") or []
            missing_alt = pd.get("images_missing_alt", 0)

            title_issues = []
            if not title:
                title_issues.append("CRITICAL: Missing title tag")
            else:
                if len(title) < TITLE_MIN: title_issues.append(f"Title too short ({len(title)} chars)")
                if len(title) > TITLE_MAX: title_issues.append(f"Title too long ({len(title)} chars)")
                if keyword and keyword.lower() not in title.lower():
                    title_issues.append(f"Keyword '{keyword}' not in title")
            title_score = max(0, 100 - len(title_issues) * 25)
            result["title"] = {"text": title, "length": len(title), "score": title_score, "issues": title_issues}

            meta_issues = []
            if not meta:
                meta_issues.append("HIGH: Missing meta description")
            else:
                if len(meta) < META_MIN: meta_issues.append(f"Meta too short ({len(meta)} chars)")
                if len(meta) > META_MAX: meta_issues.append(f"Meta too long ({len(meta)} chars)")
                if keyword and keyword.lower() not in meta.lower():
                    meta_issues.append(f"Keyword '{keyword}' not in meta description")
            meta_score = max(0, 100 - len(meta_issues) * 30)
            result["meta"] = {"text": meta, "length": len(meta), "score": meta_score, "issues": meta_issues}

            heading_issues = []
            if not h1s: heading_issues.append("CRITICAL: No H1 tag")
            elif len(h1s) > 1: heading_issues.append(f"HIGH: Multiple H1 tags ({len(h1s)})")
            if keyword and h1s and keyword.lower() not in h1s[0].lower():
                heading_issues.append("MEDIUM: Keyword not in H1")
            if not h2s: heading_issues.append("MEDIUM: No H2 tags")
            heading_score = max(0, 100 - sum(30 if "CRITICAL" in i else 20 if "HIGH" in i else 10 for i in heading_issues))
            result["headings"] = {"h1": h1s, "h2": h2s[:8], "h2_count": len(h2s), "score": heading_score, "issues": heading_issues}

            result["images"] = {"total": "N/A", "missing_alt": missing_alt, "issue": f"{missing_alt} images missing alt" if missing_alt else None}
            result["canonical"] = pd.get("canonical") or None
            result["noindex"]   = pd.get("noindex", False)
            result["word_count"] = pd.get("word_count", 0)
            result["schema_types"] = pd.get("schema_types", [])
            result["onpage_score_dataforseo"] = pd.get("onpage_score", 0)
            result["fetch_method"] = "dataforseo"

            all_issues = title_issues + meta_issues + heading_issues
            result["issues"].extend(all_issues)
            result["overall_score"] = int(sum([title_score, meta_score, heading_score]) / 3)
            return result

        # ── HTML path: existing BeautifulSoup logic ──────────────────────────
        html = fetch.get("html", "")
        if not html or len(html) < 100:
            result["error"] = "Empty or minimal HTML received"
            result["issues"].append("CRITICAL: Page returned empty content")
            return result

        soup = BeautifulSoup(html, "lxml")
        scores = []

        # --- Title ---
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else None
        title_issues = []
        if not title:
            title_issues.append("CRITICAL: Missing title tag")
        else:
            if len(title) < TITLE_MIN: title_issues.append(f"Title too short ({len(title)} chars)")
            if len(title) > TITLE_MAX: title_issues.append(f"Title too long ({len(title)} chars)")
            if keyword and keyword.lower() not in title.lower():
                title_issues.append(f"Keyword '{keyword}' not in title")
        title_score = max(0, 100 - len(title_issues) * 25)
        scores.append(title_score)
        result["title"] = {"text": title, "length": len(title) if title else 0, "score": title_score, "issues": title_issues}

        # --- Meta ---
        meta_tag = soup.find("meta", attrs={"name": re.compile("description", re.I)})
        meta = meta_tag.get("content", "").strip() if meta_tag else None
        meta_issues = []
        if not meta:
            meta_issues.append("HIGH: Missing meta description")
        else:
            if len(meta) < META_MIN: meta_issues.append(f"Meta too short ({len(meta)} chars)")
            if len(meta) > META_MAX: meta_issues.append(f"Meta too long ({len(meta)} chars)")
            if keyword and keyword.lower() not in meta.lower():
                meta_issues.append(f"Keyword '{keyword}' not in meta description")
        meta_score = max(0, 100 - len(meta_issues) * 30)
        scores.append(meta_score)
        result["meta"] = {"text": meta, "length": len(meta) if meta else 0, "score": meta_score, "issues": meta_issues}

        # --- Headings ---
        h1s = [h.get_text(strip=True) for h in soup.find_all("h1")]
        h2s = [h.get_text(strip=True) for h in soup.find_all("h2")]
        heading_issues = []
        if not h1s: heading_issues.append("CRITICAL: No H1 tag")
        elif len(h1s) > 1: heading_issues.append(f"HIGH: Multiple H1 tags ({len(h1s)})")
        if keyword and h1s and keyword.lower() not in h1s[0].lower():
            heading_issues.append(f"MEDIUM: Keyword not in H1")
        if not h2s: heading_issues.append("MEDIUM: No H2 tags")
        heading_score = max(0, 100 - sum(30 if "CRITICAL" in i else 20 if "HIGH" in i else 10 for i in heading_issues))
        scores.append(heading_score)
        result["headings"] = {"h1": h1s, "h2": h2s[:8], "h2_count": len(h2s), "score": heading_score, "issues": heading_issues}

        # --- Images ---
        all_imgs = soup.find_all("img")
        missing_alt = sum(1 for img in all_imgs if not img.get("alt"))
        img_issue = None
        if all_imgs and missing_alt / len(all_imgs) > 0.2:
            img_issue = f"HIGH: {missing_alt}/{len(all_imgs)} images missing alt text"
            result["issues"].append(img_issue)
        result["images"] = {"total": len(all_imgs), "missing_alt": missing_alt, "issue": img_issue}

        # --- Canonical ---
        canonical = soup.find("link", attrs={"rel": "canonical"})
        result["canonical"] = canonical.get("href") if canonical else None
        if not canonical:
            result["issues"].append("MEDIUM: No canonical tag")

        # --- Noindex ---
        robots_meta = soup.find("meta", attrs={"name": re.compile("robots", re.I)})
        result["noindex"] = "noindex" in (robots_meta.get("content", "").lower() if robots_meta else "")
        if result["noindex"]:
            result["issues"].append("CRITICAL: Page has noindex tag!")

        # --- Word Count ---
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        
        body_text = soup.get_text(separator=" ").strip()
        result["word_count"] = len(body_text.split())
        if result["word_count"] < 300:
            result["issues"].append(f"HIGH: Thin content ({result['word_count']} words)")
            
        # --- Advanced CRO & Trust Signals ---
        # 1. Trust Signals
        has_phone = bool(re.search(r'\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b', body_text)) or bool(soup.find("a", href=re.compile(r'^tel:')))
        has_email = bool(re.search(r'[\w\.-]+@[\w\.-]+', body_text)) or bool(soup.find("a", href=re.compile(r'^mailto:')))
        policy_links = len(soup.find_all("a", href=re.compile(r'(policy|privacy|terms|returns|refund)', re.I)))
        result["cro_trust"] = {
            "has_contact_info": has_phone or has_email,
            "policy_links": policy_links,
            "ssl_secure": url.startswith("https://")
        }
        if not (has_phone or has_email): result["issues"].append("MEDIUM: No visible contact info (Trust Signal)")
        
        # 2. Intent-to-CTA Alignment
        ctas = soup.find_all(["a", "button"], class_=re.compile(r'(btn|button|cta)', re.I))
        cta_texts = [cta.get_text(strip=True) for cta in ctas if cta.get_text(strip=True)][:5]
        result["cro_ctas"] = cta_texts
        if not cta_texts and result["word_count"] > 200:
            result["issues"].append("MEDIUM: No clear Call-to-Action buttons found")

        # --- Advanced E-E-A-T & Entity Validation ---
        # 1. Author Profile Validation
        author_meta = soup.find("meta", attrs={"name": "author"})
        author_link = soup.find("a", attrs={"rel": "author"})
        has_author = bool(author_meta) or bool(author_link) or bool(re.search(r'By\s+[A-Z][a-z]+\s+[A-Z][a-z]+', body_text[:1000]))
        result["ee_at_author"] = has_author
        
        # 2. Expert Citations
        external_links = soup.find_all("a", href=re.compile(r'^https?://(?!' + re.escape(urlparse(url).netloc) + ')'))
        edu_gov_links = [link.get('href') for link in external_links if re.search(r'\.(edu|gov|org)', link.get('href', ''))]
        result["ee_at_citations"] = len(edu_gov_links)

        # --- Schema ---
        schema_types = []
        schema_same_as = False
        for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
            try:
                data = json.loads(script.string or "{}")
                if isinstance(data, dict): 
                    schema_types.append(data.get("@type", "Unknown"))
                    if "sameAs" in data and data.get("@type") in ["Organization", "Person"]: schema_same_as = True
                elif isinstance(data, list): 
                    for d in data:
                        if isinstance(d, dict):
                            schema_types.append(d.get("@type", "Unknown"))
                            if "sameAs" in d and d.get("@type") in ["Organization", "Person"]: schema_same_as = True
            except Exception:
                pass
        result["schema_types"] = schema_types
        result["schema_same_as"] = schema_same_as
        if not schema_same_as and ("Organization" in schema_types or "Person" in schema_types):
            result["issues"].append("MEDIUM: Schema Organization/Person missing 'sameAs' entity validation (E-E-A-T gap)")
        result["schema_types"] = schema_types
        if not schema_types:
            result["issues"].append("MEDIUM: No JSON-LD schema found — add Article/FAQ schema for AEO")

        result["overall_score"] = int(sum(scores) / max(len(scores), 1))

    except Exception as e:
        result["error"] = f"Unexpected error: {str(e)[:100]}"
        result["issues"].append(f"CRITICAL: Analysis failed - {result['error']}")

    return result


def main():
    parser = argparse.ArgumentParser(description="On-Page SEO Analyzer with Error Recovery")
    parser.add_argument("--urls", help="Comma-separated URLs")
    parser.add_argument("--client", help="Client name (loads from crawl data)")
    parser.add_argument("--top", type=int, default=10, help="Number of top pages to analyze")
    parser.add_argument("--keyword", help="Target keyword to check")
    parser.add_argument("--output", help="Output JSON file path")
    args = parser.parse_args()

    # Validate input
    if not args.urls and not args.client:
        print("[ERROR] Error: Must provide either --urls or --client")
        print("💡 Examples:")
        print("   python on_page_analyzer.py --urls \"https://example.com\"")
        print("   python on_page_analyzer.py --client acme_corp --top 10")
        exit(1)

    urls = []
    if args.urls:
        urls = [u.strip() for u in args.urls.split(",") if u.strip()]
        # Validate URL format
        for url in urls:
            if not url.startswith(("http://", "https://")):
                print(f"[ERROR] Error: Invalid URL format: {url}")
                print("💡 URLs must start with http:// or https://")
                exit(1)

    elif args.client:
        print(f"🔍 Looking for crawl data for client: {args.client}...")
        crawl_files = list(Path(".tmp").glob(f"*{args.client}*crawl*.json"))
        if not crawl_files:
            print(f"[ERROR] No crawl data found for '{args.client}'")
            print(f"💡 Solution: Run a crawl first:")
            print(f"   python tools/seo_crawler.py --url https://{args.client}.com --output .tmp/{args.client}_crawl.json")
            exit(1)

        try:
            with open(crawl_files[-1], "r", encoding="utf-8") as f:
                crawl = json.load(f)
            print(f"[OK] Loaded crawl data from: {crawl_files[-1].name}")
        except json.JSONDecodeError:
            print(f"[ERROR] Crawl file is corrupted: {crawl_files[-1]}")
            print("💡 Run the crawler again to generate fresh data")
            exit(1)

        pages = sorted(crawl.get("pages", []), key=lambda p: len(p.get("internal_links", [])), reverse=True)
        urls = [p["url"] for p in pages[:args.top] if p.get("status_code") == 200]

        if not urls:
            print(f"[Error] No successful pages (200 status) found in crawl data")
            exit(1)

    print(f"\n[Analysis] Analyzing {len(urls)} page(s)...")
    if args.keyword:
        print(f"[Keyword] Target keyword: {args.keyword}\n")

    all_results = []
    errors_count = 0

    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] Analyzing: {url}")
        result = analyze_page(url, args.keyword)
        all_results.append(result)

        if result.get("error"):
            errors_count += 1
            print(f"   [X] {result['error']}")
        else:
            print(f"   [OK] Score: {result['overall_score']}/100")

        time.sleep(0.5)  # Rate limiting protection

    # Calculate statistics
    successful_analyses = [r for r in all_results if not r.get("error")]
    avg_score = int(sum(r["overall_score"] for r in successful_analyses) / max(len(successful_analyses), 1)) if successful_analyses else 0

    output_data = {
        "pages_analyzed": len(all_results),
        "successful_analyses": len(successful_analyses),
        "failed_analyses": errors_count,
        "avg_score": avg_score,
        "results": all_results,
        "analyzed_at": datetime.now().isoformat(),
        "keyword_checked": args.keyword
    }

    # Save output FIRST before any print statements that might crash
    output_path = args.output or f".tmp/onpage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"\n[Success] Output saved to: {output_path}")
    except IOError as e:
        print(f"\n[Error] Could not save output file: {str(e)}")
        print("[Tip] Check that the output directory is writable")
        exit(1)

    # Print summary (using ASCII-safe symbols)
    print("\n" + "="*60)
    print("ON-PAGE ANALYSIS SUMMARY")
    print("="*60)
    print(f"[OK] Successful: {len(successful_analyses)}/{len(all_results)}")
    if errors_count > 0:
        print(f"[X] Failed:     {errors_count}/{len(all_results)}")
    print(f"[Score] Avg Score:  {avg_score}/100")

    print("\n[Results] Page-by-Page Results:")
    for r in all_results:
        if r.get("error"):
            print(f"   [X] {r['url'][:60]} - {r['error']}")
        else:
            critical_issues = len([i for i in r['issues'] if 'CRITICAL' in i])
            high_issues = len([i for i in r['issues'] if 'HIGH' in i])
            status = "[OK]" if r['overall_score'] >= 80 else "[!]"
            print(f"   {status} {r['url'][:60]} - {r['overall_score']}/100 (CRIT:{critical_issues} HIGH:{high_issues})")

    print("="*60 + "\n")


if __name__ == "__main__":
    main()
