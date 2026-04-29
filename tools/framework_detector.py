#!/usr/bin/env python3
"""
Framework Detector Tool — Critical for SPA/CSR Detection
Detects React CRA, Next.js, Vue, Nuxt, Gatsby, and other JS frameworks.
Compares no-JS vs JS-rendered content to determine Google's perspective.

This is the FIRST tool that must run in any audit workflow.

Usage:
    python framework_detector.py --url https://example.com
    python framework_detector.py --url https://example.com --output .tmp/framework.json
"""

import argparse
import json
import time
from pathlib import Path
from datetime import datetime

try:
    import requests
    from bs4 import BeautifulSoup
    from playwright.sync_api import sync_playwright
except ImportError:
    print("[ERROR] Dependencies missing!")
    print("💡 Solution: pip install requests beautifulsoup4 playwright && playwright install chromium")
    exit(1)


def fetch_nojs(url: str, timeout: int = 15) -> dict:
    """Fetch page HTML without JavaScript execution (Google's perspective)."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        }
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)

        if resp.status_code != 200:
            return {"error": f"HTTP {resp.status_code}", "html": "", "word_count": 0}

        soup = BeautifulSoup(resp.text, "lxml")

        # Remove scripts, styles, nav, footer, header
        for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        word_count = len(text.split())

        return {
            "html": resp.text,
            "text": text,
            "word_count": word_count,
            "status_code": resp.status_code
        }

    except requests.exceptions.Timeout:
        return {"error": "Timeout", "html": "", "word_count": 0}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)[:100], "html": "", "word_count": 0}


def fetch_js(url: str, timeout: int = 30000) -> dict:
    """Fetch page with JavaScript execution (User's perspective via Playwright)."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                response = page.goto(url, timeout=timeout, wait_until="domcontentloaded")

                if not response or response.status != 200:
                    browser.close()
                    return {"error": f"HTTP {response.status if response else 'No response'}", "html": "", "word_count": 0}

                # Wait for JS frameworks to render
                page.wait_for_timeout(2000)

                html = page.content()
                soup = BeautifulSoup(html, "lxml")

                # Remove scripts, styles, nav, footer, header
                for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
                    tag.decompose()

                text = soup.get_text(separator=" ", strip=True)
                word_count = len(text.split())

                browser.close()

                return {
                    "html": html,
                    "text": text,
                    "word_count": word_count,
                    "status_code": response.status
                }

            except Exception as e:
                browser.close()
                return {"error": str(e)[:100], "html": "", "word_count": 0}

    except Exception as e:
        return {"error": str(e)[:100], "html": "", "word_count": 0}


def detect_framework(nojs_html: str, js_html: str) -> dict:
    """
    Analyze HTML to detect framework and render mode.

    Returns:
        {
            "framework": "React CRA | Next.js | Gatsby | Vue | Nuxt | Unknown",
            "render_mode": "CSR_SPA | SSR | SSG | HYBRID | STATIC",
            "seo_verdict": "CRITICAL | WARNING | GOOD",
            "signals_found": ["list of detected patterns"]
        }
    """
    signals = []
    framework = "Unknown"
    render_mode = "UNKNOWN"

    nojs_soup = BeautifulSoup(nojs_html, "lxml")
    js_soup = BeautifulSoup(js_html, "lxml")

    # === DETECT FRAMEWORK ===

    # React detection
    if '<div id="root"' in nojs_html or '<div id="app"' in nojs_html:
        signals.append("React root div detected")

        # Check if root is empty in no-JS HTML
        root_div = nojs_soup.find("div", {"id": ["root", "app"]})
        if root_div and len(root_div.get_text(strip=True)) < 20:
            signals.append("Root div EMPTY in no-JS HTML (CSR confirmed)")
            render_mode = "CSR_SPA"

        # Check for Next.js signals
        if "__NEXT_DATA__" in nojs_html:
            signals.append("__NEXT_DATA__ found (Next.js SSR/SSG)")
            framework = "Next.js"
            render_mode = "SSR"  # or SSG, both are SEO-friendly
        elif "chunk.js" in nojs_html or "main.chunk.js" in nojs_html:
            signals.append("React CRA chunk.js pattern")
            framework = "React CRA"
            render_mode = "CSR_SPA"
        else:
            framework = "React (unknown variant)"

    # Gatsby detection
    if "gatsby-chunk" in nojs_html or 'data-gatsby-' in nojs_html:
        signals.append("Gatsby SSG detected")
        framework = "Gatsby"
        render_mode = "SSG"

    # Vue detection
    if '<div id="app"' in nojs_html and "Vue" in js_html:
        signals.append("Vue detected")

        # Check for Nuxt.js
        if "__NUXT__" in nojs_html:
            signals.append("Nuxt.js SSR detected")
            framework = "Nuxt.js"
            render_mode = "SSR"
        else:
            framework = "Vue.js"
            # Check if CSR or SSR
            if len(nojs_soup.get_text(strip=True)) < 100:
                render_mode = "CSR_SPA"
                signals.append("Vue app EMPTY in no-JS HTML (CSR)")
            else:
                render_mode = "SSR"
                signals.append("Vue app has content in no-JS HTML (SSR)")

    # Angular detection
    if '<app-root' in nojs_html or 'ng-version' in nojs_html:
        signals.append("Angular detected")
        framework = "Angular"

        # Angular Universal (SSR) detection
        if "ng-state" in nojs_html:
            signals.append("Angular Universal SSR detected")
            render_mode = "SSR"
        else:
            render_mode = "CSR_SPA"
            signals.append("Angular CSR (no SSR detected)")

    # === CHECK FOR NOSCRIPT FALLBACK ===
    noscript_tags = nojs_soup.find_all("noscript")
    if noscript_tags:
        noscript_content = " ".join([tag.get_text(strip=True) for tag in noscript_tags])
        if "You need to enable JavaScript" in noscript_content or "JavaScript is required" in noscript_content:
            signals.append("CRITICAL: Noscript tag says 'JavaScript required' (bad for SEO)")
        elif len(noscript_content) > 50:
            signals.append("Noscript has meaningful fallback content (good)")

    # === CHECK FOR STATIC HTML ===
    if framework == "Unknown":
        # No JS framework detected
        if len(nojs_soup.get_text(strip=True)) > 200:
            signals.append("Site has full content in no-JS HTML (static or server-rendered)")
            framework = "Static HTML / Server-Rendered"
            render_mode = "STATIC"
        else:
            signals.append("Minimal content in no-JS HTML but no framework detected (possible custom JS)")
            framework = "Custom JavaScript"
            render_mode = "CSR_SPA"

    # === DETERMINE SEO VERDICT ===
    if render_mode == "CSR_SPA":
        seo_verdict = "CRITICAL"
    elif render_mode in ["SSR", "SSG", "STATIC"]:
        seo_verdict = "GOOD"
    elif render_mode == "HYBRID":
        seo_verdict = "WARNING"
    else:
        seo_verdict = "WARNING"

    return {
        "framework": framework,
        "render_mode": render_mode,
        "seo_verdict": seo_verdict,
        "signals_found": signals
    }


def generate_recommendation(framework: str, render_mode: str, content_ratio: float) -> str:
    """Generate specific recommendation based on detection."""

    if render_mode == "CSR_SPA":
        if framework == "React CRA":
            return "CRITICAL: Migrate from Create React App to Next.js with SSR or SSG immediately. Current site is invisible to Google."
        elif "Vue" in framework:
            return "CRITICAL: Migrate from Vue SPA to Nuxt.js with SSR. Current site is invisible to Google."
        elif "Angular" in framework:
            return "CRITICAL: Implement Angular Universal for server-side rendering. Current site is invisible to Google."
        else:
            return "CRITICAL: Site relies on client-side JavaScript rendering. Implement server-side rendering (SSR) or static site generation (SSG)."

    elif render_mode in ["SSR", "SSG"]:
        if content_ratio < 0.9:
            return "WARNING: Some content still rendered client-side. Verify all important content is present in initial HTML."
        else:
            return "GOOD: Site uses server-side rendering or static generation. Google can crawl content effectively."

    elif render_mode == "STATIC":
        return "GOOD: Static HTML site. Fully crawlable by Google."

    else:
        return "WARNING: Unable to determine render mode. Manual verification required with Google Search Console URL Inspection tool."


def detect_and_analyze(url: str) -> dict:
    """Main detection function - compares no-JS vs JS renders."""

    result = {
        "url": url,
        "analyzed_at": datetime.now().isoformat(),
        "status": "success"
    }

    print(f"[1/3] Fetching page WITHOUT JavaScript (Google's perspective)...")
    nojs_data = fetch_nojs(url)

    if "error" in nojs_data:
        result["status"] = "error"
        result["error"] = f"No-JS fetch failed: {nojs_data['error']}"
        return result

    print(f"   [OK] No-JS content: {nojs_data['word_count']} words")

    print(f"[2/3] Fetching page WITH JavaScript (User's perspective)...")
    js_data = fetch_js(url)

    if "error" in js_data:
        result["status"] = "error"
        result["error"] = f"JS fetch failed: {js_data['error']}"
        return result

    print(f"   [OK] JS-rendered content: {js_data['word_count']} words")

    # Calculate content ratio
    if js_data["word_count"] > 0:
        content_ratio = nojs_data["word_count"] / js_data["word_count"]
    else:
        content_ratio = 0

    print(f"[3/3] Analyzing framework and render mode...")

    detection = detect_framework(nojs_data["html"], js_data["html"])

    recommendation = generate_recommendation(
        detection["framework"],
        detection["render_mode"],
        content_ratio
    )

    # Determine if technical_seo should be capped
    score_cap = {}
    if detection["render_mode"] == "CSR_SPA":
        score_cap = {
            "technical_seo": 2,
            "on_page_seo": 3,
            "reason": "Content invisible to Google due to CSR rendering"
        }

    result.update({
        "framework": detection["framework"],
        "render_mode": detection["render_mode"],
        "seo_verdict": detection["seo_verdict"],
        "nojs_word_count": nojs_data["word_count"],
        "js_word_count": js_data["word_count"],
        "content_ratio": round(content_ratio, 3),
        "signals_found": detection["signals_found"],
        "recommendation": recommendation,
        "score_cap": score_cap
    })

    return result


def main():
    parser = argparse.ArgumentParser(description="Framework Detector — Detects CSR/SPA vs SSR/SSG")
    parser.add_argument("--url", required=True, help="URL to analyze")
    parser.add_argument("--output", help="Output JSON file path")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout in seconds")
    args = parser.parse_args()

    # Validate URL
    if not args.url.startswith(("http://", "https://")):
        print(f"[ERROR] Invalid URL format: {args.url}")
        print("💡 URL must start with http:// or https://")
        exit(1)

    print(f"\n{'='*70}")
    print(f"FRAMEWORK DETECTOR — SEO AI OS")
    print(f"{'='*70}\n")
    print(f"Analyzing: {args.url}\n")

    result = detect_and_analyze(args.url)

    # Save output
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\n[Output] Saved to: {args.output}")

    # Print summary
    print(f"\n{'='*70}")
    print(f"DETECTION RESULTS")
    print(f"{'='*70}\n")

    if result["status"] == "error":
        print(f"[ERROR] {result['error']}")
    else:
        verdict_symbols = {
            "CRITICAL": "[🔴 CRITICAL]",
            "WARNING": "[🟡 WARNING]",
            "GOOD": "[✅ GOOD]"
        }

        print(f"{verdict_symbols[result['seo_verdict']]} {result['seo_verdict']}")
        print(f"\nFramework:     {result['framework']}")
        print(f"Render Mode:   {result['render_mode']}")
        print(f"\nContent Analysis:")
        print(f"  No-JS (Google):  {result['nojs_word_count']} words")
        print(f"  JS (Users):      {result['js_word_count']} words")
        print(f"  Ratio:           {result['content_ratio']:.1%} of content visible to Google")

        if result['content_ratio'] < 0.1:
            print(f"  [CRITICAL] < 10% of content visible to Google!")
        elif result['content_ratio'] < 0.5:
            print(f"  [WARNING] < 50% of content visible to Google")

        print(f"\nSignals Detected:")
        for signal in result['signals_found']:
            print(f"  • {signal}")

        print(f"\nRecommendation:")
        print(f"  {result['recommendation']}")

        if result.get('score_cap'):
            print(f"\n[WARNING] Technical SEO Score Capped:")
            print(f"  Maximum score: {result['score_cap']['technical_seo']}/10")
            print(f"  Reason: {result['score_cap']['reason']}")

    print(f"\n{'='*70}\n")

    # Exit code based on verdict
    if result.get("seo_verdict") == "CRITICAL":
        exit(2)  # Critical issues found
    elif result.get("seo_verdict") == "WARNING":
        exit(1)  # Warnings found
    else:
        exit(0)  # All good


if __name__ == "__main__":
    main()
