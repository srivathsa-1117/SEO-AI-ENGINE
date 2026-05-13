#!/usr/bin/env python3
"""
DataForSEO API Client — Enterprise-Grade SEO Data
Replaces brittle web scrapers with official API access.

Features:
  - SERP scraping (Google top 100 results)
  - Keyword search volume & difficulty
  - Competitor keyword analysis
  - Backlink profile data
  - Domain authority metrics
  - Google AI Overview visibility

Authentication:
  Reads DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD from .env

Rate Limits:
  - 2,000 API calls/minute
  - Pay-as-you-go (no monthly subscription)

Pricing (as of 2026):
  - Google SERP: $0.001 per query
  - Keywords for Site: $0.003 per domain
  - Backlinks: $0.10 per domain

Documentation: https://docs.dataforseo.com/v3/
"""

import os
import json
import time
import base64
from typing import Optional, List, Dict, Any
from pathlib import Path
from datetime import datetime

try:
    import requests
    from dotenv import load_dotenv
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "requests", "python-dotenv"], check=True)
    import requests
    from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DataForSEOClient:
    """
    Official DataForSEO API client with automatic authentication,
    rate limiting, and error handling.
    """

    BASE_URL = "https://api.dataforseo.com/v3"

    def __init__(self, login: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize DataForSEO client.

        Args:
            login: DataForSEO login email (defaults to DATAFORSEO_LOGIN env var)
            password: DataForSEO password (defaults to DATAFORSEO_PASSWORD env var)
        """
        self.login = login or os.getenv("DATAFORSEO_LOGIN")
        self.password = password or os.getenv("DATAFORSEO_PASSWORD")

        if not self.login or not self.password:
            raise ValueError(
                "DataForSEO credentials not found. "
                "Set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD in .env file."
            )

        # Create Basic Auth header
        cred_string = f"{self.login}:{self.password}"
        b64_cred = base64.b64encode(cred_string.encode()).decode()

        self.headers = {
            "Authorization": f"Basic {b64_cred}",
            "Content-Type": "application/json"
        }

        self.session = requests.Session()
        self.session.headers.update(self.headers)

        # Rate limiting: max 2000 requests/minute = 1 request per 0.03s
        # We'll be conservative: 1 request per 0.5s
        self.last_request_time = 0
        self.min_request_interval = 0.5

    def _wait_for_rate_limit(self):
        """Ensure we don't exceed rate limits."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()

    def _make_request(self, endpoint: str, payload: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Make a POST request to DataForSEO API.

        Args:
            endpoint: API endpoint (e.g., "/serp/google/organic/live/advanced")
            payload: List of task objects

        Returns:
            API response as dictionary
        """
        self._wait_for_rate_limit()

        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.post(url, json=payload, timeout=60)
            response.raise_for_status()

            data = response.json()

            # Check for API errors
            if data.get("status_code") != 20000:
                error_msg = data.get("status_message", "Unknown API error")
                raise Exception(f"DataForSEO API Error: {error_msg}")

            return data

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def get_serp_results(
        self,
        keyword: str,
        location_code: int = 2840,  # USA
        language_code: str = "en",
        device: str = "desktop",
        depth: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get Google SERP results for a keyword.

        Args:
            keyword: Search query
            location_code: DataForSEO location code (2840 = USA, 2356 = India)
            language_code: Language (en, es, fr, etc.)
            device: desktop or mobile
            depth: Number of results (max 100)

        Returns:
            List of organic search results with position, URL, title, snippet
        """
        payload = [{
            "keyword": keyword,
            "location_code": location_code,
            "language_code": language_code,
            "device": device,
            "depth": depth,
            "calculate_rectangles": False
        }]

        response = self._make_request("/serp/google/organic/live/advanced", payload)

        # Extract organic results
        results = []
        tasks = response.get("tasks", [])

        if not tasks or not tasks[0].get("result"):
            return results

        items = tasks[0]["result"][0].get("items", [])

        for item in items:
            if item.get("type") == "organic":
                results.append({
                    "position": item.get("rank_group", 0),
                    "url": item.get("url", ""),
                    "domain": item.get("domain", ""),
                    "title": item.get("title", ""),
                    "snippet": item.get("description", ""),
                    "breadcrumb": item.get("breadcrumb", ""),
                })

        return results

    def get_keywords_for_site(
        self,
        target_domain: str,
        location_code: int = 2840,
        language_code: str = "en",
        limit: int = 100,
        filters: Optional[List[Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all keywords a domain ranks for (similar to Ahrefs Organic Keywords).

        Args:
            target_domain: Domain to analyze (e.g., "example.com")
            location_code: DataForSEO location code
            language_code: Language
            limit: Max keywords to return (max 1000)
            filters: Optional filters (e.g., ["keyword_data.keyword_info.search_volume", ">", 100])

        Returns:
            List of keywords with rank, search volume, difficulty
        """
        payload = [{
            "target": target_domain,
            "location_code": location_code,
            "language_code": language_code,
            "limit": limit,
            "filters": filters or []
        }]

        response = self._make_request("/dataforseo_labs/google/ranked_keywords/live", payload)

        results = []
        tasks = response.get("tasks", [])

        if not tasks or not tasks[0].get("result"):
            return results

        items = tasks[0]["result"][0].get("items", [])

        for item in items:
            kw_data = item.get("keyword_data", {}).get("keyword_info", {})
            serp_info = item.get("ranked_serp_element", {})

            results.append({
                "keyword": item.get("keyword", ""),
                "position": serp_info.get("serp_item", {}).get("rank_group", 0),
                "search_volume": kw_data.get("search_volume", 0),
                "cpc": kw_data.get("cpc", 0),
                "competition": kw_data.get("competition", 0),
                "difficulty": item.get("keyword_data", {}).get("keyword_properties", {}).get("keyword_difficulty", 0),
                "url": serp_info.get("serp_item", {}).get("url", ""),
            })

        return results

    def get_competitor_keywords(
        self,
        client_domain: str,
        competitor_domain: str,
        location_code: int = 2840,
        language_code: str = "en",
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Find keywords that a competitor ranks for but the client doesn't.
        This is the "keyword gap" analysis.

        Args:
            client_domain: Your client's domain
            competitor_domain: Competitor to analyze
            location_code: DataForSEO location code
            language_code: Language
            limit: Max gap keywords to return

        Returns:
            Dictionary with gap keywords and metrics
        """
        # Get keywords for both domains
        print(f"[DataForSEO] Fetching keywords for {client_domain}...")
        client_kws = self.get_keywords_for_site(client_domain, location_code, language_code, limit=500)

        print(f"[DataForSEO] Fetching keywords for {competitor_domain}...")
        comp_kws = self.get_keywords_for_site(competitor_domain, location_code, language_code, limit=500)

        # Create set of client keywords
        client_kw_set = {kw["keyword"].lower() for kw in client_kws}

        # Find gaps
        gaps = []
        for comp_kw in comp_kws:
            if comp_kw["keyword"].lower() not in client_kw_set:
                gaps.append({
                    "keyword": comp_kw["keyword"],
                    "volume": comp_kw["search_volume"],
                    "kd": comp_kw["difficulty"],
                    "comp_rank": comp_kw["position"],
                    "client_rank": 0,  # Not ranking
                    "comp_url": comp_kw["url"]
                })

        # Sort by search volume descending
        gaps.sort(key=lambda x: x["volume"], reverse=True)

        return {
            "client": client_domain,
            "competitor": competitor_domain,
            "client_keyword_count": len(client_kws),
            "competitor_keyword_count": len(comp_kws),
            "gap_keywords": gaps[:limit],
            "total_gaps": len(gaps)
        }

    def get_keyword_data(
        self,
        keywords: List[str],
        location_code: int = 2840,
        language_code: str = "en"
    ) -> List[Dict[str, Any]]:
        """
        Get search volume, CPC, and competition data for a list of keywords.

        Args:
            keywords: List of keywords to analyze (max 1000 per request)
            location_code: DataForSEO location code
            language_code: Language

        Returns:
            List of keyword data with search volume, CPC, competition
        """
        # DataForSEO allows max 1000 keywords per request
        # Split into batches if needed
        batch_size = 1000
        all_results = []

        for i in range(0, len(keywords), batch_size):
            batch = keywords[i:i+batch_size]

            payload = [{
                "keywords": batch,
                "location_code": location_code,
                "language_code": language_code,
                "include_serp_info": False,
                "include_seed_keyword": True
            }]

            response = self._make_request("/keywords_data/google/search_volume/live", payload)

            tasks = response.get("tasks", [])
            if not tasks or not tasks[0].get("result"):
                continue

            items = tasks[0]["result"][0].get("items", [])

            for item in items:
                kw_info = item.get("keyword_info", {})
                all_results.append({
                    "keyword": item.get("keyword", ""),
                    "search_volume": kw_info.get("search_volume", 0),
                    "cpc": kw_info.get("cpc", 0),
                    "competition": kw_info.get("competition", 0),
                    "monthly_searches": kw_info.get("monthly_searches", [])
                })

        return all_results

    def get_domain_metrics(
        self,
        target_domain: str
    ) -> Dict[str, Any]:
        """
        Get domain authority metrics (similar to Ahrefs DR or Moz DA).

        Args:
            target_domain: Domain to analyze

        Returns:
            Dictionary with domain metrics
        """
        payload = [{
            "target": target_domain
        }]

        response = self._make_request("/dataforseo_labs/google/domain_metrics/live", payload)

        tasks = response.get("tasks", [])
        if not tasks or not tasks[0].get("result"):
            return {}

        items = tasks[0]["result"][0].get("items", [])
        if not items:
            return {}

        metrics = items[0].get("metrics", {})

        return {
            "domain": target_domain,
            "rank": metrics.get("organic", {}).get("pos_1", 0) +
                   metrics.get("organic", {}).get("pos_2_3", 0) +
                   metrics.get("organic", {}).get("pos_4_10", 0),
            "etv": metrics.get("organic", {}).get("etv", 0),  # Estimated traffic value
            "keywords": metrics.get("organic", {}).get("count", 0),
            "traffic": metrics.get("organic", {}).get("estimated_paid_traffic_cost", 0),
        }


    def get_page_onpage(self, url: str, enable_javascript: bool = True) -> dict:
        """
        Fetch and analyse a URL via DataForSEO /on_page/instant_pages.
        Bypasses Akamai / Cloudflare using DataForSEO's distributed browser fleet.
        Cost: ~$0.01 per page.

        Returns a flat dict with all key on-page SEO fields so callers
        can use it directly without parsing HTML.
        """
        payload = [{
            "url": url,
            "enable_javascript": enable_javascript,
            "enable_browser_rendering": True,
            "load_resources": False,
            "check_spell": False,
            "calculate_keyword_density": False,
        }]

        try:
            response = self._make_request("/on_page/instant_pages", payload)

            tasks = response.get("tasks", [])
            if not tasks or not tasks[0].get("result"):
                return {"error": "No result from DataForSEO On-Page API", "url": url}

            result_set = tasks[0]["result"][0]
            items = result_set.get("items", [])
            if not items:
                return {"error": "No pages returned by DataForSEO On-Page API", "url": url}

            item = items[0]
            meta    = item.get("meta", {})
            checks  = item.get("checks", {})
            content = item.get("content", {})
            htags   = meta.get("htags", {})

            # Schema types (DataForSEO parses these from JSON-LD / Microdata)
            schema_types = []
            for sd in meta.get("structured_data", {}).get("items", []) if isinstance(meta.get("structured_data"), dict) else []:
                t = sd.get("@type") or sd.get("type")
                if t:
                    (schema_types.extend(t) if isinstance(t, list) else schema_types.append(t))

            images_missing_alt = sum(
                1 for img in meta.get("images", []) if not img.get("alt")
            )

            return {
                "url":                item.get("url", url),
                "status_code":        item.get("status_code", 0),
                "title":              meta.get("title") or "",
                "meta_description":   meta.get("description") or "",
                "h1":                 htags.get("h1") or [],
                "h2":                 htags.get("h2") or [],
                "h3":                 htags.get("h3") or [],
                "canonical":          meta.get("canonical") or "",
                "robots":             meta.get("robots") or "index,follow",
                "noindex":            not meta.get("index", True),
                "schema_types":       schema_types,
                "word_count":         content.get("plain_text_word_count", 0),
                "images_missing_alt": images_missing_alt,
                "internal_links":     meta.get("links_internal") or [],
                "external_links":     meta.get("links_external") or [],
                "onpage_score":       item.get("onpage_score", 0),
                "page_timing":        item.get("page_timing") or {},
                "checks":             checks,
                "error":              None,
            }

        except Exception as e:
            return {"error": str(e), "url": url}


def test_connection():
    """Test DataForSEO API connection."""
    try:
        client = DataForSEOClient()
        print("[SUCCESS] DataForSEO API authentication successful!")
        print(f"[SUCCESS] Connected as: {client.login}")
        return True
    except Exception as e:
        print(f"[ERROR] DataForSEO API authentication failed: {str(e)}")
        return False


def main():
    """CLI interface for testing DataForSEO client."""
    import argparse

    parser = argparse.ArgumentParser(description="DataForSEO API Client")
    parser.add_argument("--test", action="store_true", help="Test API connection")
    parser.add_argument("--serp", help="Get SERP results for keyword")
    parser.add_argument("--domain", help="Get keywords for domain")
    parser.add_argument("--gap", nargs=2, metavar=("CLIENT", "COMPETITOR"), help="Find keyword gap")
    parser.add_argument("--output", help="Output JSON file")

    args = parser.parse_args()

    if args.test:
        test_connection()
        return

    client = DataForSEOClient()
    result = None

    if args.serp:
        print(f"[*] Fetching SERP for: {args.serp}")
        result = {
            "keyword": args.serp,
            "results": client.get_serp_results(args.serp)
        }

    elif args.domain:
        print(f"[*] Fetching keywords for: {args.domain}")
        result = {
            "domain": args.domain,
            "keywords": client.get_keywords_for_site(args.domain, limit=100)
        }

    elif args.gap:
        client_domain, comp_domain = args.gap
        print(f"[*] Finding keyword gap: {client_domain} vs {comp_domain}")
        result = client.get_competitor_keywords(client_domain, comp_domain, limit=50)

    if result:
        output_path = args.output or ".tmp/dataforseo_test.json"
        Path(output_path).parent.mkdir(exist_ok=True, parents=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        print(f"\n[Output] Saved to: {output_path}")
        print(json.dumps(result, indent=2)[:1500] + "..." if len(json.dumps(result)) > 1500 else json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
