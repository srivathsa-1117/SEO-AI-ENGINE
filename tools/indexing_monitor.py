#!/usr/bin/env python3
"""
Indexing Monitor Tool (Programmatic SEO 2026)
Monitors GSC indexing rates for bulk-generated pages to detect crawl budget issues
or sitewide algorithmic dampening (Google's "Unhelpful Content" flag).
"""

import argparse
import json
import os
import pickle
from datetime import datetime
from pathlib import Path
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

def get_gsc_service():
    """Authenticates and returns the Google Search Console service."""
    creds = None
    token_path = os.getenv("GSC_TOKEN_PATH", "tools/mcp-gsc/token.pickle")
    
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
            
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception(f"No valid GSC credentials found at {token_path}. Authenticate MCP first.")
            
    return build('webmasters', 'v3', credentials=creds)

class IndexingMonitor:
    def __init__(self, property_url: str):
        self.property_url = property_url
        self.service = get_gsc_service()
        
    def check_urls_indexing_status(self, url_list: list) -> dict:
        """Check indexing status via Search Console API URL Inspection (requires proper OAuth scopes)."""
        metrics = {
            "total_submitted": len(url_list),
            "indexed": 0,
            "crawled_not_indexed": 0,
            "discovered_not_indexed": 0,
            "not_in_index": 0,
            "details": {}
        }
        
        # Batching/throttling required for GSC API
        print(f"Checking {len(url_list)} URLs for property {self.property_url}")
        
        try:
            for url in url_list:
                # GSC Index Inspection API Endpoint
                # Uses Google Search Console URL Inspection API
                request = {
                    "inspectionUrl": url,
                    "siteUrl": self.property_url
                }
                
                try:
                    response = self.service.urlInspection().index().inspect(body=request).execute()
                    status = response.get('inspectionResult', {}).get('indexStatusResult', {})
                    coverage_state = status.get('coverageState', '')
                    
                    metrics["details"][url] = coverage_state
                    
                    if "Submitted and indexed" in coverage_state or "Indexed, not submitted" in coverage_state:
                        metrics["indexed"] += 1
                    elif "Crawled - currently not indexed" in coverage_state:
                        metrics["crawled_not_indexed"] += 1
                    elif "Discovered - currently not indexed" in coverage_state:
                        metrics["discovered_not_indexed"] += 1
                    else:
                        metrics["not_in_index"] += 1
                except Exception as e:
                    metrics["details"][url] = f"Error: {str(e)}"
                    metrics["not_in_index"] += 1
                    
        except Exception as batch_error:
            print(f"[ERROR] Batch processing failed: {batch_error}")
            
        metrics["indexed_percentage"] = (metrics["indexed"] / metrics["total_submitted"]) * 100 if metrics["total_submitted"] > 0 else 0
        return metrics

def main():
    parser = argparse.ArgumentParser(description="Indexing Monitor Tool")
    parser.add_argument("--property", required=True, help="GSC Property URL (e.g., https://example.com/)")
    parser.add_argument("--url-list", required=True, help="Path to text file containing URLs to check (one per line)")
    parser.add_argument("--output", help="Path to save JSON results")
    
    args = parser.parse_args()
    
    try:
        with open(args.url_list, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
            
        monitor = IndexingMonitor(args.property)
        results = monitor.check_urls_indexing_status(urls)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
            print(f"[OK] Indexing health report saved to {args.output}")
            
        print(f"Total Submitted: {results['total_submitted']}")
        print(f"Total Indexed: {results['indexed']} ({results['indexed_percentage']:.2f}%)")
        print(f"Discovered Not Indexed (Index Bloat Warning): {results['discovered_not_indexed']}")
        print(f"Crawled Not Indexed (Quality Warning): {results['crawled_not_indexed']}")
        
        if results['crawled_not_indexed'] > 0:
            print("[CRITICAL WARNING] 'Crawled - currently not indexed' means Google saw the page structure but deemed the content low quality or duplicate. Use programmatic_quality_scorer.py to fix.")
            
    except Exception as e:
        print(f"[ERROR] Failed to run indexing monitor: {str(e)}")

if __name__ == "__main__":
    main()
