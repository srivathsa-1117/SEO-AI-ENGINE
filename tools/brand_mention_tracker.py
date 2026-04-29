#!/usr/bin/env python3
"""
Brand Mention Tracker (2026 Standard)
Monitors high-quality brand mentions across the web using Brave Search API.
Prioritizes mentions on platforms that influence AI model training (Reddit, Quora, News, Podcasts).
Brand signals are now a primary ranking factor over sheer backlinks.
"""

import argparse
import json
import os
import requests
from datetime import datetime, timedelta
from typing import Dict, List

class BrandMentionTracker:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
        self.headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key
        }
        
    def _search(self, query: str, freshness: str = "pd") -> dict:
        """
        freshness: 'pd' (past day), 'pw' (past week), 'pm' (past month), 'py' (past year)
        """
        params = {
            "q": query,
            "freshness": freshness,
            "count": 20
        }
        response = requests.get(self.base_url, headers=self.headers, params=params)
        
        if response.status_code != 200:
            return {"error": f"API request failed with status {response.status_code}", "raw": response.text}
            
        return response.json()

    def discover_mentions(self, brand_name: str, primary_domain: str, timeframe: str = "pw") -> Dict:
        """
        Finds brand mentions, explicitly excluding the brand's own domain.
        """
        # Exclude their own site
        query = f'"{brand_name}" -site:{primary_domain}'
        print(f"Executing query: {query}")
        
        raw_data = self._search(query, freshness=timeframe)
        
        if "error" in raw_data:
             return {"status": "error", "message": raw_data["error"]}
             
        web_results = raw_data.get("web", {}).get("results", [])
        
        mentions = []
        for result in web_results:
            url = result.get("url", "")
            mentions.append({
                "title": result.get("title", ""),
                "url": url,
                "description": result.get("description", ""),
                "platform": self._categorize_platform(url),
                "is_new": True
            })
            
        # Group by platform
        summary = {
            "total_mentions": len(mentions),
            "tier_1_authority_mentions": len([m for m in mentions if m["platform"] in ["News/Media", "Reddit", "Quora", "GitHub"]]),
            "mentions": mentions
        }
        
        return summary
        
    def _categorize_platform(self, url: str) -> str:
        """Categorize the URL into distinct platform types for AI presence tracking."""
        url_lower = url.lower()
        if "reddit.com" in url_lower: return "Reddit"
        if "quora.com" in url_lower: return "Quora"
        if "github.com" in url_lower: return "GitHub"
        if "youtube.com" in url_lower: return "YouTube"
        if "medium.com" in url_lower: return "Medium"
        if "forbes.com" in url_lower or "techcrunch.com" in url_lower or "news." in url_lower: return "News/Media"
        if "linkedin.com" in url_lower: return "LinkedIn"
        return "General Web"

def main():
    parser = argparse.ArgumentParser(description="Brand Mention Tracker")
    parser.add_argument("--brand", required=True, help="Brand Name (e.g., 'The Example Brand')")
    parser.add_argument("--domain", required=True, help="Primary domain to exclude (e.g., 'example.com')")
    parser.add_argument("--timeframe", default="pw", choices=["pd", "pw", "pm", "py"], help="Search freshness")
    parser.add_argument("--output", help="Path to save output JSON")
    
    args = parser.parse_args()
    
    api_key = os.getenv("BRAVE_API_KEY")
    if not api_key:
         print("[ERROR] BRAVE_API_KEY environment variable not found. Please set it to use the Brave Search API.")
         print("[ERROR] Failing gracefully to prevent hallucinated data in deliverables.")
         import sys
         sys.exit(1)
    else:
         tracker = BrandMentionTracker(api_key)
         res = tracker.discover_mentions(args.brand, args.domain, args.timeframe)
         
    if args.output:
         with open(args.output, "w", encoding="utf-8") as f:
             json.dump(res, f, indent=2)
         print(f"[OK] Mentions saved to {args.output}")
    else:
         print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
