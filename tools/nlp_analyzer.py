#!/usr/bin/env python3
"""
NLP Analyzer Tool
Performs NLP-based analysis on page content for:
  - gap: Find keywords competitors have but client doesn't
  - benchmark: Compare client page against top 3 competitors
  - internal_links: Find internal linking opportunities from existing content
  - entities: Extract key entities and topics from content

Usage:
    python nlp_analyzer.py --mode gap --serp-data .tmp/serp_analysis.json --client-url https://example.com/page
    python nlp_analyzer.py --mode internal_links --client acme_corp --keyword "target keyword"
    python nlp_analyzer.py --mode benchmark --urls "url1,url2,url3" --keyword "keyword"
    python nlp_analyzer.py --mode readability --file path/to/draft.md
"""

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime
from collections import Counter

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "requests", "beautifulsoup4", "lxml"], check=True)
    import requests
    from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; SEO-AI-OS/1.0; SEO Analyzer)",
}

# Common English stop words to ignore in frequency analysis
STOP_WORDS = set("""
a about above after again against all am an and any are aren't as at be because been before being below between
both but by can't cannot could couldn't did didn't do does doesn't doing don't down during each few for from
further had hadn't has hasn't have haven't having he he'd he'll he's her here here's hers herself him himself his
how how's i i'd i'll i'm i've if in into is isn't it it's its itself let's me more most mustn't my myself no nor
not of off on once only or other ought our ours ourselves out over own same shan't she she'd she'll she's should
shouldn't so some such than that that's the their theirs them themselves then there there's they they'd they'll
they're they've this those through to too under until up very was wasn't we we'd we'll we're we've were weren't
what what's when when's where where's which while who who's whom why why's will with won't would wouldn't you
you'd you'll you're you've your yours yourself yourselves
""".split())


def extract_text_from_url(url: str) -> dict:
    """Fetch and extract clean text content from a URL."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return {"url": url, "error": f"HTTP {resp.status_code}", "text": "", "h2s": [], "word_count": 0}

        soup = BeautifulSoup(resp.text, "lxml")

        # Get headings
        h1s = [h.get_text(strip=True) for h in soup.find_all("h1")]
        h2s = [h.get_text(strip=True) for h in soup.find_all("h2")]
        h3s = [h.get_text(strip=True) for h in soup.find_all("h3")]

        # Remove nav/footer/sidebar noise
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()

        text = soup.get_text(separator=" ")
        # Clean whitespace
        text = re.sub(r"\s+", " ", text).strip()
        words = [w.lower().strip(".,!?;:'\"()[]{}") for w in text.split() if len(w) > 2]
        words = [w for w in words if w not in STOP_WORDS and w.isalpha()]

        return {
            "url": url,
            "h1s": h1s,
            "h2s": h2s,
            "h3s": h3s,
            "word_count": len(words),
            "text": " ".join(words[:5000]),  # Cap for memory
            "top_terms": [term for term, _ in Counter(words).most_common(50)],
        }
    except Exception as e:
        return {"url": url, "error": str(e), "text": "", "h2s": [], "word_count": 0}


def keyword_gap_analysis(serp_data_path: str, client_url: str) -> dict:
    """Find keywords that top competitors use but the client's page doesn't."""
    with open(serp_data_path, "r", encoding="utf-8") as f:
        serp = json.load(f)

    competitor_urls = [r["url"] for r in serp.get("results", [])[:5] if r.get("url") != client_url]
    client_data = extract_text_from_url(client_url)
    client_terms = set(client_data.get("top_terms", []))

    all_competitor_terms = Counter()
    competitor_data = []
    for url in competitor_urls[:3]:
        data = extract_text_from_url(url)
        competitor_data.append(data)
        for term in data.get("top_terms", []):
            all_competitor_terms[term] += 1

    # Keywords in >=2 competitor pages but NOT in client's page
    gap_keywords = [
        term for term, count in all_competitor_terms.items()
        if count >= 2 and term not in client_terms
    ]

    return {
        "client_url": client_url,
        "client_word_count": client_data.get("word_count", 0),
        "client_top_terms": list(client_terms)[:30],
        "competitor_urls_analyzed": competitor_urls[:3],
        "gap_keywords": gap_keywords[:50],
        "gap_count": len(gap_keywords),
        "analysis_date": datetime.now().isoformat(),
    }


def benchmark_analysis(urls: list, keyword: str) -> dict:
    """Benchmark a set of pages against each other for a target keyword."""
    results = []
    for url in urls:
        data = extract_text_from_url(url)
        kw_lower = keyword.lower()
        kw_words = kw_lower.split()

        # Check keyword presence
        text_lower = data.get("text", "").lower()
        kw_density = text_lower.count(kw_lower) / max(data.get("word_count", 1), 1) * 100
        in_h2 = any(kw_lower in h.lower() for h in data.get("h2s", []))
        in_h1 = any(kw_lower in h.lower() for h in data.get("h1s", []))

        results.append({
            "url": url,
            "word_count": data.get("word_count", 0),
            "h2_count": len(data.get("h2s", [])),
            "has_keyword_in_h1": in_h1,
            "has_keyword_in_h2": in_h2,
            "keyword_density_pct": round(kw_density, 3),
            "h2_structure": data.get("h2s", [])[:10],
            "top_terms": data.get("top_terms", [])[:20],
        })

    return {
        "keyword": keyword,
        "benchmark_results": results,
        "avg_word_count": int(sum(r["word_count"] for r in results) / max(len(results), 1)),
        "analysis_date": datetime.now().isoformat(),
    }


def find_internal_link_opportunities(client_name: str, target_keyword: str) -> dict:
    """
    Scan a client's existing content (from sitemap/crawl data) 
    to find pages that could internally link to a new article about target_keyword.
    """
    tmp_dir = Path(".tmp")
    crawl_files = list(tmp_dir.glob(f"*{client_name}*crawl*.json"))

    if not crawl_files:
        return {
            "error": f"No crawl data found in .tmp/ for client '{client_name}'. Run seo_crawler.py first.",
            "suggestions": []
        }

    with open(crawl_files[-1], "r", encoding="utf-8") as f:
        crawl_data = json.load(f)

    kw_words = set(target_keyword.lower().split())
    suggestions = []

    for page in crawl_data.get("pages", []):
        if page.get("status_code") != 200:
            continue
        title = (page.get("title") or "").lower()
        # Check if page topic is related to the target keyword
        title_words = set(title.split())
        overlap = title_words & kw_words
        if overlap and len(overlap) >= 1:
            suggestions.append({
                "source_url": page.get("url"),
                "source_title": page.get("title"),
                "anchor_text_suggestion": target_keyword,
                "relevance_score": len(overlap),
            })

    # Sort by relevance
    suggestions.sort(key=lambda x: x["relevance_score"], reverse=True)

def analyze_readability_and_stylometry(text_or_file_path: str) -> dict:
    """
    Computes Flesch Reading Ease and detects AI Stylometry (patterns of LLMs).
    """
    if Path(text_or_file_path).exists():
        with open(text_or_file_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = text_or_file_path

    # Flesch Reading Ease Math
    words = len(re.findall(r'\w+', text))
    sentences = len(re.split(r'[.!?]+', text)) - 1
    if sentences == 0: sentences = 1
    if words == 0: words = 1

    def count_syllables(word):
        word = word.lower()
        count = 0
        vowels = "aeiouy"
        if word[0] in vowels: count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith("e"): count -= 1
        if count == 0: count += 1
        return count

    syllables = sum(count_syllables(w) for w in re.findall(r'\w+', text))
    flesch_score = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)

    # Interpreting Flesch
    if flesch_score > 80: level = "Easy (Grade 6)"
    elif flesch_score > 60: level = "Standard (Grade 8-9)"
    elif flesch_score > 30: level = "Difficult (College+)"
    else: level = "Very Difficult (Academic/Technical)"
    
    # AI Stylometry Target Words
    ai_markers = ["furthermore", "moreover", "in conclusion", "crucial", "essential", "vital", "tapestry", "delve", "navigating", "testament", "orchestrate"]
    found_markers = [marker for marker in ai_markers if marker in text.lower()]
    ai_probability = min(len(found_markers) * 15, 100) # Simple heuristic

    return {
        "analysis_date": datetime.now().isoformat(),
        "total_words": words,
        "total_sentences": sentences,
        "flesch_reading_ease": round(flesch_score, 2),
        "reading_level": level,
        "machine_readability": "Excellent" if flesch_score >= 60 else "Poor (Too complex for optimal AI extraction)",
        "ai_stylometry_markers_found": found_markers,
        "ai_probability_score": f"{ai_probability}%",
        "action": "Rewrite required to simplify and humanize text." if ai_probability > 50 or flesch_score < 50 else "Approved for publishing."
    }

def main():
    parser = argparse.ArgumentParser(description="NLP SEO Analyzer")
    parser.add_argument("--mode", required=True, choices=["gap", "benchmark", "internal_links", "readability"])
    parser.add_argument("--serp-data", help="Path to SERP JSON file (for gap mode)")
    parser.add_argument("--client-url", help="Client page URL (for gap mode)")
    parser.add_argument("--client", help="Client name (for internal_links mode)")
    parser.add_argument("--keyword", help="Target keyword")
    parser.add_argument("--urls", help="Comma-separated URLs (for benchmark mode)")
    parser.add_argument("--file", help="File to analyze for readability/stylometry")
    parser.add_argument("--output", help="Output JSON file path")
    args = parser.parse_args()

    data = {}
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if args.mode == "gap":
        assert args.serp_data and args.client_url, "--serp-data and --client-url required"
        print(f"[Gap Analysis] Analyzing keyword gaps for: {args.client_url}")
        data = keyword_gap_analysis(args.serp_data, args.client_url)

    elif args.mode == "benchmark":
        assert args.urls and args.keyword, "--urls and --keyword required"
        urls = [u.strip() for u in args.urls.split(",")]
        print(f"[Benchmark] Comparing {len(urls)} pages for '{args.keyword}'")
        data = benchmark_analysis(urls, args.keyword)

    elif args.mode == "internal_links":
        assert args.client and args.keyword, "--client and --keyword required"
        print(f"[Internal Links] Finding link opportunities for '{args.keyword}' in {args.client}'s content")
        data = find_internal_link_opportunities(args.client, args.keyword)

    elif args.mode == "readability":
        assert args.file, "--file required for readability mode"
        print(f"[Readability & Stylometry] Analyzing file: {args.file}")
        data = analyze_readability_and_stylometry(args.file)

    output_path = args.output or f".tmp/nlp_{args.mode}_{timestamp}.json"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n[Output] Saved to: {output_path}")
    print(json.dumps(data, indent=2)[:2000])


if __name__ == "__main__":
    main()
