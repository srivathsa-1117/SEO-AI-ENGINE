#!/usr/bin/env python3
"""
Shared Utilities for SEO AI OS
Ensures consistency across all tools.
"""

import re
import os
import sys
import json
from urllib.parse import urlparse


def smart_fetch(url: str, timeout: int = 25) -> dict:
    """
    Fetch a URL with automatic bot-bypass fallback.

    Tier 1 — curl_cffi (Chrome 120 TLS fingerprint): bypasses Akamai/Cloudflare
              TLS-fingerprint checks with zero cost. Returns raw HTML.
    Tier 2 — DataForSEO On-Page instant_pages API: uses distributed headless
              browsers that pass every JS challenge. Returns pre-parsed SEO data.

    Return schema:
        {
            "success":     bool,
            "html":        str | None,   # raw HTML (tiers 1 only)
            "status_code": int,
            "url":         str,          # final URL after redirects
            "method":      str,          # "curl_cffi" | "dataforseo" | None
            "parsed_data": dict | None,  # structured fields from DataForSEO
            "error":       str | None,
        }
    Tools that receive parsed_data should use it directly; otherwise parse html
    with BeautifulSoup as usual.
    """
    # ── Tier 1: curl_cffi (Chrome TLS impersonation, free) ──────────────────
    try:
        from curl_cffi import requests as cffi_req
        resp = cffi_req.get(
            url,
            impersonate="chrome120",
            timeout=timeout,
            allow_redirects=True,
        )
        if resp.status_code == 200 and len(resp.text) > 500:
            return {
                "success": True,
                "html": resp.text,
                "status_code": resp.status_code,
                "url": str(resp.url),
                "method": "curl_cffi",
                "parsed_data": None,
                "error": None,
            }
    except ImportError:
        pass  # not installed — fall through
    except Exception as e:
        print(f"   [smart_fetch/curl_cffi] {e}")

    # ── Tier 2: DataForSEO On-Page API (enterprise bypass) ──────────────────
    try:
        tools_dir = os.path.dirname(os.path.abspath(__file__))
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        from dataforseo_client import DataForSEOClient
        client = DataForSEOClient()
        data = client.get_page_onpage(url)
        if data and not data.get("error"):
            return {
                "success": True,
                "html": None,
                "status_code": data.get("status_code", 200),
                "url": data.get("url", url),
                "method": "dataforseo",
                "parsed_data": data,
                "error": None,
            }
    except Exception as e:
        print(f"   [smart_fetch/dataforseo] {e}")

    return {
        "success": False,
        "html": None,
        "status_code": 0,
        "url": url,
        "method": None,
        "parsed_data": None,
        "error": f"All fetch methods failed for {url}",
    }


def url_to_slug(url: str) -> str:
    """
    Convert URL to consistent slug for file naming.

    CRITICAL: This is the ONLY function that should be used for URL-to-slug conversion.
    All tools MUST use this function to ensure file naming consistency.

    Args:
        url: Full URL (e.g., "https://www.metalbarns.in/about")

    Returns:
        Slug (e.g., "metalbarns")

    Examples:
        >>> url_to_slug("https://metalbarns.in")
        'metalbarns'
        >>> url_to_slug("https://www.example.com/services")
        'exampleclient'
        >>> url_to_slug("http://example.org")
        'example'
    """
    # Remove protocol
    url = url.replace("https://", "").replace("http://", "")

    # Extract just the domain (before first /)
    domain = url.split("/")[0]

    # Remove www prefix
    domain = domain.replace("www.", "")

    # Remove common TLDs
    domain = re.sub(r'\.(com|in|org|net|co|io|ai|dev|app)$', '', domain)

    # Convert remaining dots to empty (for subdomains like blog.example.com → blogexample)
    # Or keep them as is if you want blog_example
    slug = domain.replace(".", "")

    # Remove any special characters, keep only alphanumeric
    slug = re.sub(r'[^a-z0-9]', '', slug.lower())

    return slug


def get_tmp_file(slug: str, file_type: str) -> str:
    """
    Generate consistent .tmp file path.

    Args:
        slug: Client/domain slug from url_to_slug()
        file_type: Type of file (e.g., "framework", "crawl", "lighthouse")

    Returns:
        File path (e.g., ".tmp/metalbarns_framework.json")

    Examples:
        >>> get_tmp_file("metalbarns", "framework")
        '.tmp/metalbarns_framework.json'
    """
    return f".tmp/{slug}_{file_type}.json"


def validate_file_naming(url: str, expected_files: list) -> dict:
    """
    Validate that all expected files exist for a given URL.

    Args:
        url: The website URL
        expected_files: List of file types (e.g., ["framework", "crawl_nojs", "lighthouse"])

    Returns:
        Dict with "valid": bool and "missing": list of missing files
    """
    import os

    slug = url_to_slug(url)
    missing = []

    for file_type in expected_files:
        file_path = get_tmp_file(slug, file_type)
        if not os.path.exists(file_path):
            missing.append(file_path)

    return {
        "valid": len(missing) == 0,
        "slug": slug,
        "missing": missing
    }


if __name__ == "__main__":
    # Self-test
    test_cases = [
        ("https://metalbarns.in", "metalbarns"),
        ("https://www.metalbarns.in", "metalbarns"),
        ("https://www.example.com", "exampleclient"),
        ("http://example.org/about", "example"),
        ("https://blog.example.com", "blogexample"),
    ]

    print("[URL-to-Slug Conversion Test]")
    for url, expected in test_cases:
        result = url_to_slug(url)
        status = "PASS" if result == expected else "FAIL"
        print(f"{status} {url:40s} -> {result:20s} (expected: {expected})")

    print("\n[File Path Generation Test]")
    slug = "metalbarns"
    file_types = ["framework", "crawl_nojs", "lighthouse"]
    for ft in file_types:
        print(f"  {get_tmp_file(slug, ft)}")
