#!/usr/bin/env python3
"""
Shared Utilities for SEO AI OS
Ensures consistency across all tools.
"""

import re
from urllib.parse import urlparse


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
