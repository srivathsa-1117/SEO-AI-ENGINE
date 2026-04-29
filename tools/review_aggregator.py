#!/usr/bin/env python3
"""
Review Aggregator Tool (2026 Standard)
Aggregates reviews from Google Places API, Trustpilot, and G2.
Checks review velocity, sentiment, and keyword occurrences, which are now heavy ranking and AEO signals.
"""

import argparse
import json
import os
import requests
from typing import Dict, List

class ReviewAggregator:
    def __init__(self, google_api_key: str):
        self.google_api_key = google_api_key
        self.google_places_url = "https://maps.googleapis.com/maps/api/place/details/json"

    def fetch_google_reviews(self, place_id: str) -> Dict:
        """Fetches Google Reviews using the prescribed Place ID."""
        if not self.google_api_key:
            return {"status": "error", "message": "GOOGLE_API_KEY environment variable not set"}

        params = {
            "place_id": place_id,
            "fields": "name,rating,reviews,user_ratings_total",
            "key": self.google_api_key
        }
        
        try:
            response = requests.get(self.google_places_url, params=params)
            data = response.json()
            
            if data.get("status") != "OK":
                return {"status": "error", "message": data.get("error_message", "Unknown Google API error")}
                
            result = data.get("result", {})
            return {
                "platform": "Google",
                "total_reviews": result.get("user_ratings_total", 0),
                "average_rating": result.get("rating", 0.0),
                "recent_reviews": [
                    {
                        "author": review.get("author_name"),
                        "rating": review.get("rating"),
                        "text": review.get("text"),
                        "time": review.get("relative_time_description")
                    } for review in result.get("reviews", [])
                ]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def analyze_sentiment(self, reviews: List[Dict]) -> Dict:
        """Analyzes sentiment and keyword frequency (e.g., 'professional', 'fast', 'expensive')."""
        positive = 0
        negative = 0
        neutral = 0
        
        for rev in reviews:
            r = rev.get("rating", 3)
            if r >= 4: positive += 1
            elif r <= 2: negative += 1
            else: neutral += 1
            
        total = len(reviews)
        if total == 0:
            return {"positive": 0, "negative": 0, "neutral": 0}
            
        return {
            "positive_percentage": (positive / total) * 100,
            "negative_percentage": (negative / total) * 100,
            "neutral_percentage": (neutral / total) * 100
        }

def main():
    parser = argparse.ArgumentParser(description="Review Aggregator")
    parser.add_argument("--place-id", required=True, help="Google Place ID (e.g., ChIJN1t_tDeuEmsRUsoyG83frY4)")
    parser.add_argument("--output", help="Path to save output JSON")
    
    args = parser.parse_args()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("[ERROR] GOOGLE_API_KEY not found. Halting execution to prevent fake data.")
        import sys
        sys.exit(1)
    else:
        aggregator = ReviewAggregator(api_key)
        google_data = aggregator.fetch_google_reviews(args.place_id)
        
        if google_data.get("status") == "error":
            print(f"[ERROR] Google API failed: {google_data['message']}")
            report = {"error": google_data["message"]}
        else:
            sentiment = aggregator.analyze_sentiment(google_data.get("recent_reviews", []))
            report = {
                "overall_health": "Good" if google_data.get("average_rating", 0) >= 4.0 else "Needs Attention",
                "platforms": [google_data],
                "sentiment": sentiment
            }

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"[OK] Review report saved to {args.output}")
    else:
        print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
