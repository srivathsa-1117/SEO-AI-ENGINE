#!/usr/bin/env python3
"""
Competitor Gap Analysis Tool — ENTERPRISE EDITION
Powered by DataForSEO API for 100% accurate keyword gap analysis.

Compares a client's keywords against competitors to find "Low-Hanging Fruit":
Keywords that competitors rank for, but the client does not.

Features:
  - Real keyword rankings (not mock data)
  - Search volume & keyword difficulty
  - Multiple competitor comparison
  - Low-hanging fruit filtering (KD < 35, Volume > 1000)

Usage:
    python competitor_gap.py --client acme_corp
    python competitor_gap.py --client-url acme.com --competitor-urls comp1.com,comp2.com
    python competitor_gap.py --client-url acme.com --competitor-urls comp1.com --location-code 2356 (India)
"""

import argparse
import json
from pathlib import Path
from datetime import datetime

try:
    from dataforseo_client import DataForSEOClient
    DATAFORSEO_AVAILABLE = True
except ImportError:
    DATAFORSEO_AVAILABLE = False
    print("[ERROR] DataForSEO client not found. Please ensure dataforseo_client.py exists in tools/")


def load_brand_kit(client_name):
    """Load client brand kit from clients/ folder."""
    path = Path(f"clients/{client_name}/brand_kit.json")
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def mock_gap_data(client_url, competitors):
    print("[ERROR] DataForSEO credentials missing or API failed.")
    print("Cannot return fake data for enterprise deliverables. Please configure DataForSEO API.")
    import sys
    sys.exit(1)


def analyze_gap_with_dataforseo(client_url, competitor_urls, location_code=2840):
    """
    Use DataForSEO API to find keyword gaps between client and competitors.

    Args:
        client_url: Client domain (e.g., "example.com")
        competitor_urls: List of competitor domains
        location_code: DataForSEO location code (2840=USA, 2356=India)

    Returns:
        List of gap keywords with volume, difficulty, and ranking data
    """
    if not DATAFORSEO_AVAILABLE:
        print("[ERROR] DataForSEO client not available. Returning mock data.")
        return mock_gap_data(client_url, competitor_urls)

    try:
        client = DataForSEOClient()
        all_gaps = []

        # Analyze gap for each competitor
        for comp_url in competitor_urls:
            print(f"\n[*] Analyzing gap: {client_url} vs {comp_url}")
            gap_data = client.get_competitor_keywords(
                client_domain=client_url,
                competitor_domain=comp_url,
                location_code=location_code,
                limit=100
            )

            # Add competitor source to each gap keyword
            for gap in gap_data["gap_keywords"]:
                gap["competitor_source"] = comp_url

            all_gaps.extend(gap_data["gap_keywords"])

        # Deduplicate by keyword (keep highest volume if duplicates)
        unique_gaps = {}
        for gap in all_gaps:
            kw = gap["keyword"]
            if kw not in unique_gaps or gap["volume"] > unique_gaps[kw]["volume"]:
                unique_gaps[kw] = gap

        return list(unique_gaps.values())

    except Exception as e:
        print(f"[ERROR] DataForSEO API failed: {e}")
        print("[Notice] Falling back to mock data")
        return mock_gap_data(client_url, competitor_urls)


def main():
    parser = argparse.ArgumentParser(description="SEO Competitor Gap Analysis — DataForSEO Edition")
    parser.add_argument("--client", help="Client name to read from brand_kit.json")
    parser.add_argument("--client-url", help="Client domain (e.g., example.com)")
    parser.add_argument("--competitor-urls", help="Comma-separated competitor domains")
    parser.add_argument("--location-code", type=int, default=2840, help="DataForSEO location code (2840=USA, 2356=India)")
    parser.add_argument("--output", help="Output JSON path")
    args = parser.parse_args()

    client_url = ""
    competitors = []

    # Load from brand kit if client name provided
    if args.client:
        bk = load_brand_kit(args.client)
        if bk:
            client_url = bk.get("client_info", {}).get("website_url", "")
            comps = bk.get("seo_targets", {}).get("competitors", [])
            competitors = [c.get("website_url", "") for c in comps if c.get("website_url")]

    # Override with command-line arguments if provided
    if args.client_url:
        client_url = args.client_url
    if args.competitor_urls:
        competitors = [c.strip() for c in args.competitor_urls.split(",")]

    # Validation
    if not client_url or not competitors:
        print("[ERROR] Must provide client URL and at least one competitor URL.")
        print("\nUsage:")
        print("  python competitor_gap.py --client acme_corp")
        print("  python competitor_gap.py --client-url acme.com --competitor-urls comp1.com,comp2.com")
        return

    # Clean URLs (remove https://, www.)
    client_url = client_url.replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")
    competitors = [c.replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/") for c in competitors]

    print("=" * 60)
    print("COMPETITOR GAP ANALYSIS — ENTERPRISE EDITION")
    print("=" * 60)
    print(f"Client:      {client_url}")
    print(f"Competitors: {', '.join(competitors)}")
    print(f"Location:    {args.location_code} ({'USA' if args.location_code == 2840 else 'India' if args.location_code == 2356 else 'Custom'})")
    print(f"Powered by:  {'DataForSEO API' if DATAFORSEO_AVAILABLE else 'Mock Data (no API)'}")
    print("=" * 60)

    # Run gap analysis
    opportunities = analyze_gap_with_dataforseo(client_url, competitors, args.location_code)

    # Filter for low-hanging fruit (KD < 35, Volume > 1000)
    low_hanging = [opp for opp in opportunities if opp["kd"] < 35 and opp["volume"] > 1000]

    # Sort by volume descending
    low_hanging.sort(key=lambda x: x["volume"], reverse=True)
    opportunities.sort(key=lambda x: x["volume"], reverse=True)

    result = {
        "analysis_date": datetime.now().isoformat(),
        "client": client_url,
        "competitors_analyzed": competitors,
        "location_code": args.location_code,
        "total_gaps_found": len(opportunities),
        "low_hanging_fruit_count": len(low_hanging),
        "low_hanging_fruit": low_hanging,
        "all_opportunities": opportunities,
        "powered_by": "dataforseo_api" if DATAFORSEO_AVAILABLE else "mock_data"
    }

    # Summary output
    print(f"\n[SUCCESS] Gap Analysis Complete!")
    print(f"[SUCCESS] Found {len(opportunities)} total gap keywords")
    print(f"[SUCCESS] Found {len(low_hanging)} Low-Hanging Fruit targets (KD<35, Vol>1K)")

    if low_hanging:
        print("\n" + "=" * 60)
        print("TOP 10 LOW-HANGING FRUIT KEYWORDS")
        print("=" * 60)
        for i, t in enumerate(low_hanging[:10], 1):
            print(f"{i:2}. '{t['keyword']}'")
            print(f"    Volume: {t['volume']:,} | KD: {t['kd']} | Comp Rank: #{t['comp_rank']}")
            if 'competitor_source' in t:
                print(f"    Found on: {t['competitor_source']}")
            print()

    # Save output
    output_path = args.output or f".tmp/{client_url.replace('.', '_')}_competitor_gap.json"
    Path(output_path).parent.mkdir(exist_ok=True, parents=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"[Output] Saved gap data to: {output_path}")

    # Cost summary
    if DATAFORSEO_AVAILABLE:
        cost = len(competitors) * 0.003  # $0.003 per domain
        print(f"[Cost] Estimated API cost: ${cost:.4f} USD")


if __name__ == "__main__":
    main()
