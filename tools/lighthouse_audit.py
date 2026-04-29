#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lighthouse Audit Tool with Error Recovery
Runs PageSpeed Insights API to get Core Web Vitals and Lighthouse scores.

Features:
- Automatic retry with exponential backoff
- Graceful degradation when API is unavailable
- User-friendly error messages
- Validates API key before running

Usage:
    python lighthouse_audit.py --url https://example.com
    python lighthouse_audit.py --url https://example.com --strategy mobile
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
from typing import Dict, Optional

# Fix Windows console encoding for emoji support
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        # Python < 3.7
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

try:
    import requests
    from dotenv import load_dotenv
except ImportError:
    print("[ERROR] Dependencies missing!")
    print("💡 Solution: pip install requests python-dotenv")
    import subprocess
    subprocess.run(["pip", "install", "requests", "python-dotenv"], check=True)
    import requests
    from dotenv import load_dotenv

load_dotenv()


def run_lighthouse(url: str, strategy: str = "mobile", api_key: str = None, max_retries: int = 3) -> dict:
    """Run PageSpeed Insights API for a URL with retry logic."""

    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("[WARNING]  GOOGLE_API_KEY not set in .env")
        print("💡 Solution:")
        print("   1. Go to console.cloud.google.com → Credentials")
        print("   2. Create API Key")
        print("   3. Enable 'PageSpeed Insights API'")
        print("   4. Add GOOGLE_API_KEY=your_key to .env file")
        return {
            "url": url,
            "strategy": strategy,
            "status": "skipped",
            "reason": "GOOGLE_API_KEY not configured"
        }

    api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

    params = {
        "url": url,
        "strategy": strategy,
        "key": api_key,
        "category": ["performance", "accessibility", "best-practices", "seo"]
    }

    print(f"[Lighthouse] Running audit for {url} ({strategy})...")

    # Retry logic
    for attempt in range(max_retries):
        try:
            response = requests.get(api_url, params=params, timeout=60)

            # Handle rate limiting
            if response.status_code == 429:
                wait_time = (2 ** attempt) * 10  # 10s, 20s, 40s
                if attempt < max_retries - 1:
                    print(f"   [!] Rate limited by Google API, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                else:
                    return {
                        "url": url,
                        "strategy": strategy,
                        "status": "error",
                        "error": "429 Rate Limited - PageSpeed API quota exceeded"
                    }

            # Handle invalid API key
            if response.status_code == 400:
                error_data = response.json().get("error", {})
                if "API key not valid" in str(error_data):
                    return {
                        "url": url,
                        "strategy": strategy,
                        "status": "error",
                        "error": "Invalid GOOGLE_API_KEY - Check your .env file"
                    }

            response.raise_for_status()
            data = response.json()

            # Validate response structure
            if "lighthouseResult" not in data:
                return {
                    "url": url,
                    "strategy": strategy,
                    "status": "error",
                    "error": "Invalid API response - lighthouseResult missing"
                }

            break  # Success, exit retry loop

        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                print(f"   [WARNING]  Timeout, retry {attempt + 1}/{max_retries}...")
                time.sleep(5)
                continue
            else:
                return {
                    "url": url,
                    "strategy": strategy,
                    "status": "error",
                    "error": "Timeout - PageSpeed API took too long to respond"
                }

        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                print(f"   [WARNING]  Connection error, retry {attempt + 1}/{max_retries}...")
                time.sleep(5)
                continue
            else:
                return {
                    "url": url,
                    "strategy": strategy,
                    "status": "error",
                    "error": "Connection error - Check internet connection"
                }

        except requests.exceptions.HTTPError as e:
            return {
                "url": url,
                "strategy": strategy,
                "status": "error",
                "error": f"HTTP {e.response.status_code} - {str(e)[:100]}"
            }

        except Exception as e:
            return {
                "url": url,
                "strategy": strategy,
                "status": "error",
                "error": f"Unexpected error: {str(e)[:100]}"
            }

    # Parse successful response
    try:
        lighthouse_result = data.get("lighthouseResult", {})
        categories = lighthouse_result.get("categories", {})
        audits = lighthouse_result.get("audits", {})

        # Extract Core Web Vitals — INP replaced FID on March 12 2024
        cwv = {
            "lcp": audits.get("largest-contentful-paint", {}).get("numericValue"),
            "inp": audits.get("interaction-to-next-paint", {}).get("numericValue"),
            "cls": audits.get("cumulative-layout-shift", {}).get("numericValue"),
            "fcp": audits.get("first-contentful-paint", {}).get("numericValue"),
            "tti": audits.get("interactive", {}).get("numericValue"),
            "tbt": audits.get("total-blocking-time", {}).get("numericValue"),
            "speed_index": audits.get("speed-index", {}).get("numericValue"),
        }

        # Add pass/fail assessment for each CWV metric (with null safety)
        def assess_lcp(value):
            if value is None:
                return "Unknown"
            return "Good" if value < 2500 else "Needs Improvement" if value < 4000 else "Poor"

        def assess_inp(value):
            if value is None:
                return "Unknown"
            return "Good" if value < 200 else "Needs Improvement" if value < 500 else "Poor"

        def assess_cls(value):
            if value is None:
                return "Unknown"
            return "Good" if value < 0.1 else "Needs Improvement" if value < 0.25 else "Poor"

        cwv_assessment = {
            "lcp_status": assess_lcp(cwv["lcp"]),
            "inp_status": assess_inp(cwv["inp"]),
            "cls_status": assess_cls(cwv["cls"])
        }
        cwv.update(cwv_assessment)

        # Extract scores
        scores = {
            "performance": categories.get("performance", {}).get("score"),
            "accessibility": categories.get("accessibility", {}).get("score"),
            "best_practices": categories.get("best-practices", {}).get("score"),
            "seo": categories.get("seo", {}).get("score"),
        }

        # Convert scores from 0-1 to 0-100
        scores = {k: int(v * 100) if v is not None else 0 for k, v in scores.items()}

        # Get SEO audit details (only failed ones)
        seo_audits = {}
        seo_audit_refs = categories.get("seo", {}).get("auditRefs", [])
        for ref in seo_audit_refs:
            audit_id = ref.get("id")
            if audit_id in audits:
                audit_data = audits[audit_id]
                # Only include failed audits (score < 1) - with null safety
                score = audit_data.get("score")
                if score is not None and score < 1:
                    seo_audits[audit_id] = {
                        "score": score,
                        "title": audit_data.get("title"),
                        "description": audit_data.get("description")
                    }

        print(f"   [OK] Complete - Performance: {scores['performance']}/100")

        return {
            "url": url,
            "strategy": strategy,
            "fetch_time": datetime.now().isoformat(),
            "scores": scores,
            "core_web_vitals": cwv,
            "seo_audits": seo_audits,
            "status": "success"
        }

    except (KeyError, TypeError, ValueError) as e:
        return {
            "url": url,
            "strategy": strategy,
            "fetch_time": datetime.now().isoformat(),
            "status": "error",
            "error": f"Failed to parse PageSpeed API response: {str(e)[:100]}"
        }


def audit_url(url: str, output_path: str = None) -> dict:
    """Run Lighthouse audit for both mobile and desktop."""

    results = {
        "url": url,
        "audit_date": datetime.now().isoformat(),
        "mobile": run_lighthouse(url, "mobile"),
        "desktop": run_lighthouse(url, "desktop")
    }

    # Calculate overall status
    mobile_perf = results["mobile"].get("scores", {}).get("performance", 0)
    desktop_perf = results["desktop"].get("scores", {}).get("performance", 0)

    results["summary"] = {
        "mobile_performance": mobile_perf,
        "desktop_performance": desktop_perf,
        "mobile_lcp_ms": results["mobile"].get("core_web_vitals", {}).get("lcp"),
        "mobile_cls": results["mobile"].get("core_web_vitals", {}).get("cls"),
        "mobile_inp_ms": results["mobile"].get("core_web_vitals", {}).get("inp"),
        "overall_status": "Good" if mobile_perf >= 90 else "Needs Improvement" if mobile_perf >= 50 else "Poor"
    }

    # Save output
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n[Output] Saved to: {output_path}")

    return results


def main():
    parser = argparse.ArgumentParser(description="Lighthouse/PageSpeed Insights Audit with Error Recovery")
    parser.add_argument("--url", required=True, help="URL to audit")
    parser.add_argument("--output", help="Output JSON file path")
    parser.add_argument("--strategy", choices=["mobile", "desktop", "both"], default="both",
                        help="Device strategy to test")
    args = parser.parse_args()

    # Validate URL format
    if not args.url.startswith(("http://", "https://")):
        print("[ERROR] Error: URL must start with http:// or https://")
        print(f"💡 You provided: {args.url}")
        print(f"💡 Try: https://{args.url}")
        exit(1)

    # Check if API key is configured
    if not os.getenv("GOOGLE_API_KEY"):
        print("\n[Error] GOOGLE_API_KEY not found in .env file")
        print("[Tip] This tool requires a Google PageSpeed Insights API key")
        print("[Tip] Get one for free at: https://console.cloud.google.com/apis/credentials")
        print("[Tip] Then add to .env: GOOGLE_API_KEY=your_key_here\n")
        exit(1)

    print(f"\n[Audit] Starting PageSpeed Insights audit...")
    print(f"[URL] {args.url}")
    print(f"[Strategy] {args.strategy}\n")

    if args.strategy == "both":
        results = audit_url(args.url, args.output)
    else:
        results = run_lighthouse(args.url, args.strategy)
        if args.output:
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            try:
                with open(args.output, "w", encoding="utf-8") as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                print(f"[Success] Saved to: {args.output}")
            except IOError as e:
                print(f"[Error] Could not save output: {str(e)}")

    # Print summary with error handling (using ASCII-safe symbols)
    print("\n" + "="*60)
    print("LIGHTHOUSE AUDIT SUMMARY")
    print("="*60)

    if args.strategy == "both":
        mobile_status = results.get("mobile", {}).get("status")
        desktop_status = results.get("desktop", {}).get("status")

        if mobile_status == "success" or desktop_status == "success":
            summary = results.get("summary", {})
            print(f"\n[Mobile] Performance:  {summary.get('mobile_performance', 'N/A')}/100")
            print(f"[Desktop] Performance: {summary.get('desktop_performance', 'N/A')}/100")

            if summary.get('mobile_lcp_ms'):
                lcp_ms = summary['mobile_lcp_ms']
                lcp_s = lcp_ms / 1000
                lcp_status = "GOOD" if lcp_ms < 2500 else "NEEDS IMPROVEMENT" if lcp_ms < 4000 else "POOR"
                print(f"\n[CWV] Core Web Vitals (Mobile):")
                print(f"   LCP: {lcp_s:.2f}s [{lcp_status}] (target: < 2.5s)")

            if summary.get('mobile_cls') is not None:
                cls = summary['mobile_cls']
                cls_status = "GOOD" if cls < 0.1 else "NEEDS IMPROVEMENT" if cls < 0.25 else "POOR"
                print(f"   CLS: {cls:.3f} [{cls_status}] (target: < 0.1)")

            if summary.get('mobile_inp_ms'):
                inp_ms = summary['mobile_inp_ms']
                inp_status = "GOOD" if inp_ms < 200 else "NEEDS IMPROVEMENT" if inp_ms < 500 else "POOR"
                print(f"   INP: {inp_ms:.0f}ms [{inp_status}] (target: < 200ms)")

            print(f"\n[Status] Overall: {summary.get('overall_status', 'Unknown')}")
        else:
            print(f"\n[X] Mobile audit: {results.get('mobile', {}).get('error', 'Failed')}")
            print(f"[X] Desktop audit: {results.get('desktop', {}).get('error', 'Failed')}")

    else:
        if results.get("status") == "success":
            scores = results.get("scores", {})
            cwv = results.get("core_web_vitals", {})

            print(f"\n[Scores] Lighthouse Scores:")
            print(f"   Performance:   {scores.get('performance', 0)}/100")
            print(f"   SEO:           {scores.get('seo', 0)}/100")
            print(f"   Accessibility: {scores.get('accessibility', 0)}/100")
            print(f"   Best Practices:{scores.get('best_practices', 0)}/100")

            if cwv.get('lcp'):
                print(f"\n[CWV] Core Web Vitals:")
                print(f"   LCP: {cwv['lcp']/1000:.2f}s ({cwv.get('lcp_status', 'Unknown')})")
            if cwv.get('inp') is not None:
                print(f"   INP: {cwv['inp']:.0f}ms ({cwv.get('inp_status', 'Unknown')})")
            if cwv.get('cls') is not None:
                print(f"   CLS: {cwv['cls']:.3f} ({cwv.get('cls_status', 'Unknown')})")

            failed_audits = results.get("seo_audits", {})
            if failed_audits:
                print(f"\n[!] Failed SEO Audits: {len(failed_audits)}")
                for audit_id, audit in list(failed_audits.items())[:3]:
                    print(f"   - {audit.get('title', audit_id)}")

        elif results.get("status") == "skipped":
            print(f"\n[!] Audit skipped: {results.get('reason')}")
        else:
            print(f"\n[X] Audit failed: {results.get('error', 'Unknown error')}")

    print("="*60 + "\n")


if __name__ == "__main__":
    main()
