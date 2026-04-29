#!/usr/bin/env python3
"""
Programmatic Quality Scorer
Detects doorway page patterns and thin content in bulk-generated pages.

Implements 2026 Google quality guidelines:
- Boilerplate ratio must be < 40%
- Minimum 3 unique variables per page
- Sufficient unique content (200+ words excluding boilerplate)

Usage:
    python programmatic_quality_scorer.py --urls urls.txt --output quality_report.json
    python programmatic_quality_scorer.py --sitemap https://example.com/sitemap.xml --sample 50 --output report.json
"""

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse
from typing import List, Dict, Tuple
from difflib import SequenceMatcher
from collections import Counter
import re

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("[ERROR] Missing dependencies!")
    print("💡 Solution: pip install requests beautifulsoup4")
    sys.exit(1)


class ProgrammaticQualityScorer:
    """Analyzes programmatic pages for doorway/thin content patterns."""

    BOILERPLATE_THRESHOLD = 0.40  # 40% max boilerplate
    MIN_UNIQUE_WORDS = 200        # Minimum unique content words
    MIN_VARIABLES = 3             # Minimum unique data points per page

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.pages_analyzed = []

    def fetch_page_content(self, url: str) -> Tuple[str, str]:
        """Fetch page HTML and extract text content."""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove scripts, styles, nav, footer
            for element in soup(['script', 'style', 'nav', 'footer', 'header']):
                element.decompose()

            # Get main content
            main_content = soup.find('main') or soup.find('article') or soup.find('body')
            text = main_content.get_text(separator=' ', strip=True) if main_content else ""

            # Clean whitespace
            text = re.sub(r'\s+', ' ', text).strip()

            return response.text, text

        except Exception as e:
            if self.verbose:
                print(f"[WARNING] Failed to fetch {url}: {e}")
            return "", ""

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity ratio (0.0 to 1.0)."""
        return SequenceMatcher(None, text1, text2).ratio()

    def extract_unique_elements(self, html: str) -> List[str]:
        """Extract potential variable elements from HTML."""
        soup = BeautifulSoup(html, 'html.parser')

        unique_elements = []

        # Title
        title = soup.find('title')
        if title:
            unique_elements.append(title.get_text().strip())

        # H1
        h1 = soup.find('h1')
        if h1:
            unique_elements.append(h1.get_text().strip())

        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            unique_elements.append(meta_desc['content'])

        # First paragraph
        first_p = soup.find('p')
        if first_p:
            unique_elements.append(first_p.get_text().strip())

        # All headings
        for heading in soup.find_all(['h2', 'h3']):
            unique_elements.append(heading.get_text().strip())

        return unique_elements

    def count_unique_variables(self, elements1: List[str], elements2: List[str]) -> int:
        """Count how many elements differ between two pages."""
        if len(elements1) != len(elements2):
            return max(len(elements1), len(elements2))

        different_count = 0
        for e1, e2 in zip(elements1, elements2):
            if e1 != e2:
                different_count += 1

        return different_count

    def analyze_pages(self, urls: List[str]) -> Dict:
        """Analyze a set of programmatic pages."""
        if len(urls) < 2:
            return {
                "error": "Need at least 2 URLs to compare",
                "urls_provided": len(urls)
            }

        # Fetch all pages
        pages_data = []
        for url in urls[:50]:  # Limit to 50 pages for performance
            if self.verbose:
                print(f"[*] Fetching: {url}")

            html, text = self.fetch_page_content(url)
            if not text:
                continue

            elements = self.extract_unique_elements(html)
            word_count = len(text.split())

            pages_data.append({
                "url": url,
                "html": html,
                "text": text,
                "elements": elements,
                "word_count": word_count
            })

        if len(pages_data) < 2:
            return {
                "error": "Failed to fetch sufficient pages",
                "urls_attempted": len(urls),
                "pages_fetched": len(pages_data)
            }

        # Calculate boilerplate ratio
        similarities = []
        for i in range(len(pages_data) - 1):
            similarity = self.calculate_similarity(
                pages_data[i]['text'],
                pages_data[i + 1]['text']
            )
            similarities.append(similarity)

        avg_similarity = sum(similarities) / len(similarities)
        boilerplate_ratio = avg_similarity  # Higher similarity = more boilerplate

        # Count unique variables
        variable_counts = []
        for i in range(len(pages_data) - 1):
            var_count = self.count_unique_variables(
                pages_data[i]['elements'],
                pages_data[i + 1]['elements']
            )
            variable_counts.append(var_count)

        avg_variables = sum(variable_counts) / len(variable_counts) if variable_counts else 0

        # Word count analysis
        word_counts = [p['word_count'] for p in pages_data]
        avg_word_count = sum(word_counts) / len(word_counts)

        # Calculate score (0-100)
        score = 100
        issues = []

        # Penalty 1: High boilerplate ratio
        if boilerplate_ratio > self.BOILERPLATE_THRESHOLD:
            penalty = (boilerplate_ratio - self.BOILERPLATE_THRESHOLD) * 100
            score -= penalty
            issues.append({
                "type": "high_boilerplate",
                "severity": "critical" if boilerplate_ratio > 0.60 else "warning",
                "message": f"Boilerplate ratio is {boilerplate_ratio:.1%} (max: 40%)",
                "impact": f"-{penalty:.0f} points"
            })

        # Penalty 2: Too few unique variables
        if avg_variables < self.MIN_VARIABLES:
            penalty = (self.MIN_VARIABLES - avg_variables) * 15
            score -= penalty
            issues.append({
                "type": "insufficient_variables",
                "severity": "critical",
                "message": f"Only {avg_variables:.1f} unique variables per page (min: 3)",
                "impact": f"-{penalty:.0f} points"
            })

        # Penalty 3: Low word count
        if avg_word_count < self.MIN_UNIQUE_WORDS:
            penalty = (self.MIN_UNIQUE_WORDS - avg_word_count) / 10
            score -= penalty
            issues.append({
                "type": "thin_content",
                "severity": "warning",
                "message": f"Average {avg_word_count:.0f} words per page (min: 200)",
                "impact": f"-{penalty:.0f} points"
            })

        score = max(0, min(100, score))  # Clamp to 0-100

        # Determine verdict
        if score >= 70:
            verdict = "PASS"
            risk_level = "low"
        elif score >= 50:
            verdict = "WARNING"
            risk_level = "medium"
        else:
            verdict = "FAIL"
            risk_level = "high"

        return {
            "verdict": verdict,
            "score": round(score, 1),
            "risk_level": risk_level,
            "metrics": {
                "boilerplate_ratio": round(boilerplate_ratio, 3),
                "avg_unique_variables": round(avg_variables, 1),
                "avg_word_count": round(avg_word_count, 0),
                "pages_analyzed": len(pages_data)
            },
            "thresholds": {
                "max_boilerplate": self.BOILERPLATE_THRESHOLD,
                "min_variables": self.MIN_VARIABLES,
                "min_words": self.MIN_UNIQUE_WORDS
            },
            "issues": issues,
            "recommendations": self.generate_recommendations(boilerplate_ratio, avg_variables, avg_word_count),
            "sample_pages": [p['url'] for p in pages_data[:5]]
        }

    def generate_recommendations(self, boilerplate: float, variables: float, word_count: float) -> List[str]:
        """Generate actionable recommendations."""
        recs = []

        if boilerplate > self.BOILERPLATE_THRESHOLD:
            recs.append(f"Reduce repeated content. Current boilerplate: {boilerplate:.1%}, target: <40%")
            recs.append("Add unique paragraphs describing local context, case studies, or data specific to each page")

        if variables < self.MIN_VARIABLES:
            recs.append(f"Increase unique data points per page from {variables:.1f} to at least 3")
            recs.append("Example variables: location details, pricing, testimonials, images, local stats")

        if word_count < self.MIN_UNIQUE_WORDS:
            recs.append(f"Increase content length from {word_count:.0f} to at least 200 unique words")
            recs.append("Add location-specific FAQs, process explanations, or service details")

        if not recs:
            recs.append("Quality checks passed! Content meets 2026 programmatic SEO standards.")

        return recs


def fetch_sitemap_urls(sitemap_url: str, sample_size: int = 50) -> List[str]:
    """Fetch URLs from XML sitemap."""
    try:
        response = requests.get(sitemap_url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'xml')
        urls = [loc.text for loc in soup.find_all('loc')]

        # Sample if too many
        if len(urls) > sample_size:
            import random
            urls = random.sample(urls, sample_size)

        return urls
    except Exception as e:
        print(f"[ERROR] Failed to fetch sitemap: {e}")
        return []


def main():
    parser = argparse.ArgumentParser(
        description="Programmatic Quality Scorer — Detect doorway pages & thin content"
    )

    parser.add_argument(
        "--urls",
        type=str,
        help="Path to text file with URLs (one per line)"
    )

    parser.add_argument(
        "--sitemap",
        type=str,
        help="Sitemap URL to analyze"
    )

    parser.add_argument(
        "--sample",
        type=int,
        default=50,
        help="Number of pages to sample from sitemap (default: 50)"
    )

    parser.add_argument(
        "--output",
        type=str,
        default=".tmp/programmatic_quality_report.json",
        help="Output JSON file path"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed progress"
    )

    args = parser.parse_args()

    # Get URLs
    urls = []

    if args.urls:
        urls_file = Path(args.urls)
        if not urls_file.exists():
            print(f"[ERROR] File not found: {args.urls}")
            sys.exit(1)

        with open(urls_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]

    elif args.sitemap:
        print(f"[*] Fetching sitemap: {args.sitemap}")
        urls = fetch_sitemap_urls(args.sitemap, args.sample)

        if not urls:
            print("[ERROR] No URLs found in sitemap")
            sys.exit(1)

        print(f"[OK] Found {len(urls)} URLs")

    else:
        print("[ERROR] Must provide --urls or --sitemap")
        parser.print_help()
        sys.exit(1)

    # Run analysis
    print(f"\n[*] Analyzing {len(urls)} pages for programmatic quality...")

    scorer = ProgrammaticQualityScorer(verbose=args.verbose)
    results = scorer.analyze_pages(urls)

    # Output results
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    # Print summary
    print("\n" + "="*60)
    print("[REPORT] PROGRAMMATIC QUALITY REPORT")
    print("="*60)

    if "error" in results:
        print(f"[ERROR] {results['error']}")
        sys.exit(1)

    print(f"\n[VERDICT] {results['verdict']}")
    print(f"[SCORE] {results['score']}/100")
    print(f"[RISK LEVEL] {results['risk_level'].upper()}")

    print(f"\n[METRICS]")
    metrics = results['metrics']
    print(f"  - Boilerplate Ratio: {metrics['boilerplate_ratio']:.1%}")
    print(f"  - Avg Unique Variables: {metrics['avg_unique_variables']:.1f}")
    print(f"  - Avg Word Count: {metrics['avg_word_count']:.0f}")
    print(f"  - Pages Analyzed: {metrics['pages_analyzed']}")

    if results['issues']:
        print(f"\n[ISSUES FOUND] ({len(results['issues'])}):")
        for issue in results['issues']:
            severity_tag = "[CRITICAL]" if issue['severity'] == 'critical' else "[WARNING]"
            print(f"  {severity_tag} {issue['message']} ({issue['impact']})")

    print(f"\n[RECOMMENDATIONS]")
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"  {i}. {rec}")

    print(f"\n[OUTPUT] Full report: {output_path}")

    # Exit code based on verdict
    if results['verdict'] == 'FAIL':
        print("\n[FAIL] QUALITY CHECK FAILED - Do NOT publish these pages without fixes!")
        sys.exit(1)
    elif results['verdict'] == 'WARNING':
        print("\n[WARNING] QUALITY WARNING - Review recommendations before publishing")
        sys.exit(0)
    else:
        print("\n[PASS] QUALITY CHECK PASSED - Pages meet 2026 standards")
        sys.exit(0)


if __name__ == "__main__":
    main()
