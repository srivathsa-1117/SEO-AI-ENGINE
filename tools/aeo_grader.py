#!/usr/bin/env python3
"""
AEO (Answer Engine Optimization) Grader
Scores content for AI search citability across ChatGPT, Perplexity, and Gemini.

This tool analyzes content to determine how likely it is to be cited by AI search
engines when users ask relevant questions.

Features:
- Listicle detection (AI engines prefer numbered lists)
- FAQ schema validation
- Concise answer block detection (50-75 words)
- Structured table detection
- Data citation counting
- Platform-specific scoring (ChatGPT, Perplexity, Gemini)

Usage:
    python aeo_grader.py --url https://example.com --output .tmp/aeo_score.json
    python aeo_grader.py --content article.md --output .tmp/aeo_score.json
    python aeo_grader.py --file content.html --output .tmp/aeo_score.json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from urllib.parse import urlparse

try:
    import requests
    from bs4 import BeautifulSoup
    from dotenv import load_dotenv
except ImportError:
    print("[ERROR] Dependencies missing!")
    print("Solution: pip install requests beautifulsoup4 python-dotenv lxml")
    import subprocess
    subprocess.run(["pip", "install", "requests", "beautifulsoup4", "python-dotenv", "lxml"], check=True)
    import requests
    from bs4 import BeautifulSoup
    from dotenv import load_dotenv

load_dotenv()


class AEOGrader:
    """AEO content grader for AI search optimization"""

    def __init__(self):
        self.scoring_weights = {
            'listicle_format': 20,
            'faq_schema': 15,
            'concise_answers': 15,
            'structured_tables': 10,
            'data_citations': 15,
            'clear_headings': 10,
            'freshness': 10,
            'multimedia': 5
        }

    def grade_content(self, content: str, url: Optional[str] = None, html: Optional[str] = None) -> Dict:
        """
        Grade content for AEO optimization.

        Args:
            content: Plain text or markdown content
            url: Optional URL for metadata
            html: Optional HTML for schema detection

        Returns:
            Dictionary with overall score and platform-specific scores
        """
        results = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'overall_score': 0,
            'platform_scores': {},
            'factors': {},
            'recommendations': []
        }

        # Detect optimization factors
        results['factors']['listicle_format'] = self._detect_listicles(content)
        results['factors']['faq_schema'] = self._detect_faq_schema(html) if html else False
        results['factors']['concise_answers'] = self._detect_answer_blocks(content)
        results['factors']['structured_tables'] = self._detect_tables(content, html)
        results['factors']['data_citations'] = self._count_citations(content)
        results['factors']['clear_headings'] = self._detect_headings(content)
        results['factors']['freshness'] = self._check_freshness(content)
        results['factors']['multimedia'] = self._detect_multimedia(html) if html else 0

        # Calculate overall score
        overall = 0

        if results['factors']['listicle_format']:
            overall += self.scoring_weights['listicle_format']

        if results['factors']['faq_schema']:
            overall += self.scoring_weights['faq_schema']

        # Concise answers (score based on count)
        answer_score = min(results['factors']['concise_answers'] * 3, self.scoring_weights['concise_answers'])
        overall += answer_score

        # Tables (score based on count)
        table_score = min(results['factors']['structured_tables'] * 5, self.scoring_weights['structured_tables'])
        overall += table_score

        # Citations (score based on count)
        citation_score = min(results['factors']['data_citations'] * 3, self.scoring_weights['data_citations'])
        overall += citation_score

        # Headings
        if results['factors']['clear_headings']:
            overall += self.scoring_weights['clear_headings']

        # Freshness
        if results['factors']['freshness']:
            overall += self.scoring_weights['freshness']

        # Multimedia
        if results['factors']['multimedia'] >= 2:
            overall += self.scoring_weights['multimedia']

        results['overall_score'] = min(overall, 100)

        # Platform-specific scores
        results['platform_scores'] = self._calculate_platform_scores(results)

        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(results)

        return results

    def _detect_listicles(self, content: str) -> bool:
        """Detect if content uses numbered list format"""
        # Pattern 1: Markdown numbered lists (1. 2. 3.)
        markdown_pattern = r'^\d+\.\s+.+$'
        markdown_matches = len(re.findall(markdown_pattern, content, re.MULTILINE))

        # Pattern 2: HTML ordered lists would be in HTML
        # Pattern 3: "First, Second, Third" or "Step 1, Step 2"
        sequence_pattern = r'\b(first|second|third|fourth|fifth|step \d+|tip \d+)\b'
        sequence_matches = len(re.findall(sequence_pattern, content, re.IGNORECASE))

        # Consider it a listicle if >=3 numbered items or >=5 sequence markers
        return markdown_matches >= 3 or sequence_matches >= 5

    def _detect_faq_schema(self, html: str) -> bool:
        """Detect FAQ schema markup in HTML"""
        if not html:
            return False

        # Look for FAQ schema
        faq_patterns = [
            r'"@type"\s*:\s*"FAQPage"',
            r'"@type"\s*:\s*"Question"',
            r'itemtype="https://schema\.org/FAQPage"'
        ]

        for pattern in faq_patterns:
            if re.search(pattern, html, re.IGNORECASE):
                return True

        return False

    def _detect_answer_blocks(self, content: str) -> int:
        """
        Detect concise answer blocks (50-75 word paragraphs).
        AI engines prefer direct, concise answers.
        """
        # Split into paragraphs
        paragraphs = content.split('\n\n')

        answer_blocks = 0
        for para in paragraphs:
            words = para.strip().split()
            word_count = len(words)

            # Ideal answer block: 50-75 words, starts with direct statement
            if 50 <= word_count <= 75:
                # Check if it starts like an answer (not a question)
                first_sentence = para.strip().split('.')[0] if '.' in para else para
                if not first_sentence.strip().endswith('?'):
                    answer_blocks += 1

        return answer_blocks

    def _detect_tables(self, content: str, html: Optional[str] = None) -> int:
        """Detect structured tables (markdown or HTML)"""
        table_count = 0

        # Markdown tables (| header | header |)
        markdown_table_pattern = r'\|.+\|.+\|\n\|[-\s|]+\|'
        markdown_tables = len(re.findall(markdown_table_pattern, content))
        table_count += markdown_tables

        # HTML tables
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            html_tables = len(soup.find_all('table'))
            table_count += html_tables

        return table_count

    def _count_citations(self, content: str) -> int:
        """
        Count data citations (links, references, sources).
        AI engines value attributable data.
        """
        citation_count = 0

        # Pattern 1: Markdown links [text](url)
        markdown_links = len(re.findall(r'\[.+?\]\(.+?\)', content))
        citation_count += markdown_links

        # Pattern 2: References like [1], [2] or (Source: ...)
        ref_pattern = r'\[\d+\]|\(Source:|According to|Research shows|Study by'
        refs = len(re.findall(ref_pattern, content, re.IGNORECASE))
        citation_count += refs

        return citation_count

    def _detect_headings(self, content: str) -> bool:
        """Detect clear heading structure (H2, H3 in markdown)"""
        # Markdown headings (## H2, ### H3)
        heading_pattern = r'^#{2,3}\s+.+$'
        headings = len(re.findall(heading_pattern, content, re.MULTILINE))

        # Good heading structure: >=3 headings
        return headings >= 3

    def _check_freshness(self, content: str) -> bool:
        """
        Check if content mentions recent years (2024, 2025, 2026).
        AI engines prefer recent content.
        """
        # Look for year mentions 2024+
        year_pattern = r'\b(202[4-9]|203[0-9])\b'
        recent_years = re.findall(year_pattern, content)

        return len(recent_years) > 0

    def _detect_multimedia(self, html: str) -> int:
        """Detect images, videos, or other multimedia"""
        if not html:
            return 0

        soup = BeautifulSoup(html, 'html.parser')

        # Count images
        images = len(soup.find_all('img'))

        # Count videos
        videos = len(soup.find_all(['video', 'iframe']))

        return images + videos

    def _calculate_platform_scores(self, results: Dict) -> Dict:
        """
        Calculate platform-specific scores based on 2026 best practices.
        Different AI engines weight factors differently.

        ChatGPT (70% market share): Comprehensive depth, citations, author credibility
        Perplexity (citation-heavy): Fresh content (<90 days), numbered format, sources
        Gemini (Knowledge Graph): Triple schema, entity linking, structured data
        """
        overall = results['overall_score']
        factors = results['factors']

        # === CHATGPT SCORING (70% AI Search Market Share) ===
        # Base preferences: Comprehensive (2000+ words assumed from content), deep citations, author expertise
        chatgpt_score = overall

        # Freshness signals (+10 max)
        if factors['freshness']:
            chatgpt_score += 10  # Mentions 2024-2026

        # Citation depth (+15 max)
        if factors['data_citations'] >= 5:
            chatgpt_score += 15  # 5+ sources = authoritative
        elif factors['data_citations'] >= 3:
            chatgpt_score += 10  # 3-4 sources = good
        elif factors['data_citations'] >= 1:
            chatgpt_score += 5   # 1-2 sources = minimal

        # Structured content (+10 max)
        if factors['concise_answers'] >= 5:
            chatgpt_score += 10  # 5+ answer blocks = comprehensive
        elif factors['concise_answers'] >= 3:
            chatgpt_score += 5

        # Headings structure (depth matters for ChatGPT)
        if factors['clear_headings']:
            chatgpt_score += 5  # Deep H2→H3→H4 structure

        chatgpt_score = min(chatgpt_score, 100)

        # === PERPLEXITY SCORING (Citation-Heavy, Fresh Content) ===
        # Base preferences: Freshness <90 days (46.7% citations), numbered format, clear sources
        perplexity_score = overall

        # Freshness is CRITICAL for Perplexity (+20 max)
        if factors['freshness']:
            perplexity_score += 20  # 46.7% of citations from <90 day content

        # Citations are mandatory (+20 max)
        if factors['data_citations'] >= 5:
            perplexity_score += 20  # Heavy citation = Perplexity loves this
        elif factors['data_citations'] >= 3:
            perplexity_score += 10

        # Numbered format (#1, #2, #3) (+10 max)
        if factors['listicle_format']:
            perplexity_score += 10  # Numbered rankings = 3.2x citability

        # Comparison tables (+10 max)
        if factors['structured_tables'] >= 2:
            perplexity_score += 10  # Side-by-side comparisons
        elif factors['structured_tables'] >= 1:
            perplexity_score += 5

        perplexity_score = min(perplexity_score, 100)

        # === GEMINI SCORING (Google Knowledge Graph Integration) ===
        # Base preferences: Triple schema stacking, entity linking, structured markup
        gemini_score = overall

        # Schema markup is CRITICAL for Gemini (+20 max)
        if factors['faq_schema']:
            gemini_score += 20  # FAQ/Article/Organization schema

        # Heading structure for Google indexing (+10 max)
        if factors['clear_headings']:
            gemini_score += 10  # Clear H1/H2/H3 hierarchy

        # Structured data tables (+10 max)
        if factors['structured_tables'] >= 2:
            gemini_score += 10  # Gemini parses tables well
        elif factors['structured_tables'] >= 1:
            gemini_score += 5

        # Multimedia signals (+5 max)
        if factors['multimedia'] >= 3:
            gemini_score += 5  # Images/videos help Google's multimodal understanding

        # Citations (Google still values authority) (+10 max)
        if factors['data_citations'] >= 5:
            gemini_score += 10

        gemini_score = min(gemini_score, 100)

        return {
            'chatgpt': chatgpt_score,
            'perplexity': perplexity_score,
            'gemini': gemini_score,
            'highest_potential': max(chatgpt_score, perplexity_score, gemini_score),
            'optimization_priority': self._determine_optimization_priority(
                chatgpt_score, perplexity_score, gemini_score
            )
        }

    def _determine_optimization_priority(self, chatgpt: int, perplexity: int, gemini: int) -> str:
        """
        Determine which platform to prioritize for optimization based on scores.
        Recommend focusing on the platform where the content has the most potential.
        """
        scores = {
            'ChatGPT (70% market share)': chatgpt,
            'Perplexity (citation-focused)': perplexity,
            'Gemini (Google Knowledge Graph)': gemini
        }

        # Find lowest score (biggest opportunity for improvement)
        lowest_platform = min(scores, key=scores.get)
        lowest_score = scores[lowest_platform]

        # Find highest score (already strong)
        highest_platform = max(scores, key=scores.get)
        highest_score = scores[highest_platform]

        # If all scores are similar (within 10 points), recommend ChatGPT (70% market share)
        if highest_score - lowest_score <= 10:
            return "All platforms: Content is balanced, prioritize ChatGPT (70% market share)"

        # If Perplexity is lowest, prioritize it (biggest impact potential)
        if lowest_score < 60:
            return f"PRIORITY: {lowest_platform} (score: {lowest_score}/100) - Biggest improvement opportunity"

        # If all scores >70, content is strong
        if lowest_score >= 70:
            return f"All platforms are strong (lowest: {lowest_score}/100). Focus on distribution."

        return f"PRIORITY: {lowest_platform} (score: {lowest_score}/100)"

    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recs = []
        factors = results['factors']

        if not factors['listicle_format']:
            recs.append("Add numbered lists or step-by-step formatting (AI engines prefer listicles)")

        if not factors['faq_schema']:
            recs.append("Add FAQ schema with prompt-matched questions (critical for Gemini)")

        if factors['concise_answers'] < 3:
            recs.append(f"Add more concise answer blocks (current: {factors['concise_answers']}, target: >=5)")

        if factors['structured_tables'] < 2:
            recs.append(f"Add structured comparison tables (current: {factors['structured_tables']}, target: >=2)")

        if factors['data_citations'] < 3:
            recs.append(f"Add more data citations with sources (current: {factors['data_citations']}, target: >=5)")

        if not factors['clear_headings']:
            recs.append("Add clear H2/H3 heading structure (minimum 3 headings)")

        if not factors['freshness']:
            recs.append("Mention recent years (2024, 2025, 2026) to signal freshness")

        if factors['multimedia'] < 2:
            recs.append("Add images or videos to enhance multimedia signals")

        if results['overall_score'] >= 70:
            recs.append("[OK] Content is well-optimized for AI search engines")

        return recs


def fetch_url_content(url: str) -> tuple:
    """Fetch content from URL and return (text, html)"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # Remove script and style elements
        for script in soup(['script', 'style']):
            script.decompose()

        # Get text
        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text, html

    except Exception as e:
        print(f"[ERROR] Failed to fetch URL: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='AEO Grader - Score content for AI search optimization')
    parser.add_argument('--url', help='URL to analyze')
    parser.add_argument('--file', help='File path to analyze (HTML or text)')
    parser.add_argument('--content', help='Direct content string to analyze')
    parser.add_argument('--output', default='.tmp/aeo_score.json', help='Output JSON file path')

    args = parser.parse_args()

    # Validate input
    if not any([args.url, args.file, args.content]):
        print("[ERROR] Must provide --url, --file, or --content")
        sys.exit(1)

    # Create output directory
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    grader = AEOGrader()

    # Get content based on input type
    if args.url:
        print(f"[ACTION] Analyzing URL: {args.url}")
        text, html = fetch_url_content(args.url)
        results = grader.grade_content(text, url=args.url, html=html)
    elif args.file:
        print(f"[ACTION] Analyzing file: {args.file}")
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Detect if HTML
        is_html = args.file.endswith('.html') or '<html' in content.lower()
        if is_html:
            soup = BeautifulSoup(content, 'html.parser')
            text = soup.get_text()
            html = content
        else:
            text = content
            html = None

        results = grader.grade_content(text, html=html)
    else:
        print("[ACTION] Analyzing provided content")
        results = grader.grade_content(args.content)

    # Save results
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] AEO Analysis Complete")
    print(f"\nOverall Score: {results['overall_score']}/100")
    print(f"\nPlatform-Specific Scores (2026):")
    print(f"  ChatGPT (70% market):    {results['platform_scores']['chatgpt']}/100")
    print(f"  Perplexity (citations):  {results['platform_scores']['perplexity']}/100")
    print(f"  Gemini (Knowledge Graph): {results['platform_scores']['gemini']}/100")
    print(f"  Highest Potential:       {results['platform_scores']['highest_potential']}/100")
    print(f"\n[RECOMMENDATION] {results['platform_scores']['optimization_priority']}")

    print(f"\nOptimization Factors:")
    for factor, value in results['factors'].items():
        status = "[OK]" if value else "[WARNING]"
        if isinstance(value, int):
            status = "[OK]" if value > 0 else "[WARNING]"
        print(f"  {status} {factor}: {value}")

    print(f"\nRecommendations:")
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"  {i}. {rec}")

    print(f"\n[FILE] Results saved to: {args.output}")


if __name__ == "__main__":
    main()
