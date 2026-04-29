#!/usr/bin/env python3
"""
Entity SEO Auditor
Assesses brand's entity recognition and Knowledge Graph eligibility.

Checks:
1. Wikipedia presence
2. Wikidata entity
3. Google Knowledge Panel
4. NAP consistency across 10+ sources
5. Schema markup with @id and sameAs
6. Brand mentions on authority sites

Outputs entity strength score (0-100) and improvement roadmap.

Usage:
    python entity_auditor.py --brand "The Example Brand" --website https://example.com
    python entity_auditor.py --brand "Acme Corp" --website https://acme.com --output entity_report.json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urlparse, quote_plus

try:
    import requests
    from bs4 import BeautifulSoup
    from dotenv import load_dotenv
except ImportError:
    print("[ERROR] Dependencies missing!")
    print("Solution: pip install requests beautifulsoup4 python-dotenv lxml")
    sys.exit(1)

load_dotenv()


class EntityAuditor:
    """Entity SEO auditor for Knowledge Graph presence"""

    def __init__(self, brand_name: str, website_url: str):
        self.brand_name = brand_name
        self.website_url = website_url
        self.domain = urlparse(website_url).netloc

        # Scoring weights
        self.weights = {
            'wikipedia': 40,
            'wikidata': 15,
            'knowledge_panel': 20,
            'nap_consistency': 10,
            'schema_entity': 5,
            'authority_mentions': 5,
            'crunchbase': 5
        }

    def run_full_audit(self) -> Dict:
        """Run complete entity audit"""
        results = {
            'brand': self.brand_name,
            'website': self.website_url,
            'timestamp': datetime.now().isoformat(),
            'entity_strength_score': 0,
            'checks': {},
            'timeline_estimate': '',
            'roadmap': [],
            'knowledge_panel_eligible': False
        }

        print(f"\n[ACTION] Running Entity Audit for: {self.brand_name}")
        print(f"Website: {self.website_url}\n")

        # Run all checks
        results['checks']['wikipedia'] = self._check_wikipedia()
        results['checks']['wikidata'] = self._check_wikidata()
        results['checks']['knowledge_panel'] = self._check_knowledge_panel()
        results['checks']['nap_consistency'] = self._check_nap_consistency()
        results['checks']['schema'] = self._check_schema()
        results['checks']['mentions'] = self._check_authority_mentions()
        results['checks']['crunchbase'] = self._check_crunchbase()

        # Calculate score
        results['entity_strength_score'] = self._calculate_score(results['checks'])

        # Generate roadmap
        results['roadmap'] = self._generate_roadmap(results['checks'], results['entity_strength_score'])

        # Timeline estimate
        results['timeline_estimate'] = self._estimate_timeline(results['checks'])

        # Knowledge Panel eligibility
        results['knowledge_panel_eligible'] = results['entity_strength_score'] >= 60

        return results

    def _check_wikipedia(self) -> Dict:
        """Check Wikipedia presence"""
        print("[1/7] Checking Wikipedia presence...")

        try:
            # Search Wikipedia
            search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={quote_plus(self.brand_name)}&format=json"
            response = requests.get(search_url, timeout=10)
            data = response.json()

            if 'query' in data and 'search' in data['query'] and len(data['query']['search']) > 0:
                # Found results, check if exact match
                for result in data['query']['search']:
                    if result['title'].lower() == self.brand_name.lower():
                        return {
                            'exists': True,
                            'url': f"https://en.wikipedia.org/wiki/{result['title'].replace(' ', '_')}",
                            'score_contribution': self.weights['wikipedia']
                        }

                # Partial match
                return {
                    'exists': False,
                    'partial_match': data['query']['search'][0]['title'],
                    'score_contribution': 0,
                    'recommendation': f"No exact match. Closest: {data['query']['search'][0]['title']}"
                }

            return {
                'exists': False,
                'score_contribution': 0,
                'recommendation': 'Create Wikipedia article (requires notability)'
            }

        except Exception as e:
            return {
                'exists': False,
                'error': str(e),
                'score_contribution': 0
            }

    def _check_wikidata(self) -> Dict:
        """Check Wikidata entity"""
        print("[2/7] Checking Wikidata entity...")

        try:
            # Search Wikidata
            search_url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={quote_plus(self.brand_name)}&language=en&format=json"
            response = requests.get(search_url, timeout=10)
            data = response.json()

            if 'search' in data and len(data['search']) > 0:
                entity = data['search'][0]
                return {
                    'exists': True,
                    'entity_id': entity['id'],
                    'url': f"https://www.wikidata.org/wiki/{entity['id']}",
                    'description': entity.get('description', 'N/A'),
                    'score_contribution': self.weights['wikidata']
                }

            return {
                'exists': False,
                'score_contribution': 0,
                'recommendation': 'Create Wikidata entity (free, takes 10 minutes)'
            }

        except Exception as e:
            return {
                'exists': False,
                'error': str(e),
                'score_contribution': 0
            }

    def _check_knowledge_panel(self) -> Dict:
        """Check Google Knowledge Panel"""
        print("[3/7] Checking Knowledge Panel...")

        # Note: This requires scraping Google SERP or using Google Knowledge Graph API
        # For now, we'll return a manual check instruction

        return {
            'checked': False,
            'manual_check_required': True,
            'instructions': f"Google search '{self.brand_name}' and check for Knowledge Panel on right side",
            'score_contribution': 0,
            'note': 'Automated Knowledge Panel detection requires Google API or SERP scraping'
        }

    def _check_nap_consistency(self) -> Dict:
        """Check Name, Address, Phone consistency"""
        print("[4/7] Checking NAP consistency...")

        # Simplified version - checks website for NAP data
        # Full version would check across 10+ sources

        try:
            response = requests.get(self.website_url, timeout=10)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            # Extract potential NAP data
            nap_data = {
                'name': self.brand_name,
                'address': None,
                'phone': None
            }

            # Look for address
            address_patterns = [
                soup.find('address'),
                soup.find(itemprop='address'),
                soup.find(class_=re.compile('address', re.I))
            ]
            for pattern in address_patterns:
                if pattern:
                    nap_data['address'] = pattern.get_text(strip=True)
                    break

            # Look for phone
            phone_pattern = re.compile(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
            phone_match = phone_pattern.search(html)
            if phone_match:
                nap_data['phone'] = phone_match.group()

            consistency_score = 0
            if nap_data['address']:
                consistency_score += 5
            if nap_data['phone']:
                consistency_score += 5

            return {
                'data_found': nap_data,
                'consistency_score': consistency_score,
                'score_contribution': consistency_score,
                'recommendation': 'Full NAP audit requires checking Google Business Profile, Yelp, Facebook, etc.'
            }

        except Exception as e:
            return {
                'error': str(e),
                'score_contribution': 0
            }

    def _check_schema(self) -> Dict:
        """Check schema markup with @id and sameAs"""
        print("[5/7] Checking schema markup...")

        try:
            response = requests.get(self.website_url, timeout=10)
            html = response.text

            # Look for JSON-LD schema
            schema_scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)

            if not schema_scripts:
                return {
                    'has_schema': False,
                    'score_contribution': 0,
                    'recommendation': 'Add Organization/LocalBusiness schema with @id and sameAs'
                }

            # Parse schema
            has_id = False
            has_sameas = False
            schema_types = []

            for script in schema_scripts:
                try:
                    data = json.loads(script.strip())
                    if isinstance(data, dict):
                        schema_types.append(data.get('@type', 'Unknown'))
                        if '@id' in data:
                            has_id = True
                        if 'sameAs' in data:
                            has_sameas = True
                except:
                    continue

            score = 0
            if schema_types:
                score += 2
            if has_id:
                score += 2
            if has_sameas:
                score += 1

            return {
                'has_schema': True,
                'schema_types': schema_types,
                'has_id': has_id,
                'has_sameas': has_sameas,
                'score_contribution': score,
                'recommendation': 'Good start. Ensure @id and sameAs include Wikipedia/Wikidata links.'
            }

        except Exception as e:
            return {
                'error': str(e),
                'score_contribution': 0
            }

    def _check_authority_mentions(self) -> Dict:
        """Check brand mentions on authority sites"""
        print("[6/7] Checking authority mentions...")

        # Simplified - would use Brave Search API or scraping in full version
        return {
            'checked': False,
            'manual_check_required': True,
            'instructions': f'Google search: "{self.brand_name}" -site:{self.domain} and count authority mentions',
            'score_contribution': 0,
            'target': '10+ mentions on DA 50+ sites'
        }

    def _check_crunchbase(self) -> Dict:
        """Check Crunchbase presence"""
        print("[7/7] Checking Crunchbase...")

        # Note: Crunchbase API requires paid access
        # Manual check for now

        return {
            'checked': False,
            'manual_check_required': True,
            'instructions': f'Visit crunchbase.com and search "{self.brand_name}"',
            'score_contribution': 0,
            'value': 'Crunchbase profile adds +5 to entity score'
        }

    def _calculate_score(self, checks: Dict) -> int:
        """Calculate overall entity strength score"""
        score = 0

        for check_name, check_data in checks.items():
            if 'score_contribution' in check_data:
                score += check_data['score_contribution']

        return min(score, 100)

    def _generate_roadmap(self, checks: Dict, score: int) -> List[Dict]:
        """Generate improvement roadmap"""
        roadmap = []

        # Priority 1: Wikipedia (if missing)
        if not checks['wikipedia'].get('exists', False):
            roadmap.append({
                'priority': 1,
                'action': 'Create Wikipedia article',
                'impact': '+40 points',
                'difficulty': 'High',
                'timeline': '2-6 months',
                'requirements': 'Brand must meet notability criteria (press coverage, awards, significant impact)'
            })

        # Priority 2: Wikidata (if missing)
        if not checks['wikidata'].get('exists', False):
            roadmap.append({
                'priority': 2,
                'action': 'Create Wikidata entity',
                'impact': '+15 points',
                'difficulty': 'Low',
                'timeline': '1 hour',
                'requirements': 'Free account, basic brand info'
            })

        # Priority 3: Schema with @id and sameAs
        if not checks['schema'].get('has_id', False) or not checks['schema'].get('has_sameas', False):
            roadmap.append({
                'priority': 3,
                'action': 'Add/improve Organization schema with @id and sameAs',
                'impact': '+5 points',
                'difficulty': 'Low',
                'timeline': '30 minutes',
                'requirements': 'Technical: Add JSON-LD to website'
            })

        # Priority 4: NAP consistency
        if checks['nap_consistency'].get('consistency_score', 0) < 10:
            roadmap.append({
                'priority': 4,
                'action': 'Ensure NAP consistency across 10+ sources',
                'impact': '+10 points',
                'difficulty': 'Medium',
                'timeline': '2-4 weeks',
                'requirements': 'Update Google Business Profile, Yelp, Facebook, LinkedIn, directories'
            })

        # Priority 5: Build authority mentions
        roadmap.append({
            'priority': 5,
            'action': 'Build 10+ authority site mentions',
            'impact': '+5 points',
            'difficulty': 'Medium-High',
            'timeline': '3-6 months',
            'requirements': 'PR outreach, guest posts, press releases, industry recognition'
        })

        return roadmap

    def _estimate_timeline(self, checks: Dict) -> str:
        """Estimate timeline to Knowledge Panel"""
        if checks['wikipedia'].get('exists', False):
            return '1-3 months (with Wikipedia article)'
        elif checks['wikidata'].get('exists', False):
            return '6-12 months (with Wikidata but no Wikipedia)'
        else:
            return '12-18 months (starting from scratch)'


def main():
    parser = argparse.ArgumentParser(description='Entity SEO Auditor - Knowledge Graph eligibility checker')
    parser.add_argument('--brand', required=True, help='Brand name to audit')
    parser.add_argument('--website', required=True, help='Website URL')
    parser.add_argument('--output', default='.tmp/entity_audit.json', help='Output JSON file path')

    args = parser.parse_args()

    # Create output directory
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    # Run audit
    auditor = EntityAuditor(args.brand, args.website)
    results = auditor.run_full_audit()

    # Save results
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Print summary
    print(f"\n{'='*60}")
    print("ENTITY AUDIT RESULTS")
    print(f"{'='*60}\n")

    print(f"Brand: {results['brand']}")
    print(f"Website: {results['website']}")
    print(f"\nEntity Strength Score: {results['entity_strength_score']}/100\n")

    # Status interpretation
    score = results['entity_strength_score']
    if score >= 80:
        status = "[OK] Strong entity - Knowledge Panel likely exists or imminent"
    elif score >= 60:
        status = "[OK] Good entity - Knowledge Panel likely within 3-6 months"
    elif score >= 30:
        status = "[WARNING] Moderate entity - 6-12 months to Knowledge Panel with work"
    else:
        status = "[CRITICAL] Weak entity - 12-18+ months, requires significant effort"

    print(f"Status: {status}\n")

    print("Check Results:")
    for check_name, check_data in results['checks'].items():
        if 'exists' in check_data:
            status_icon = "[OK]" if check_data['exists'] else "[ERROR]"
            print(f"  {status_icon} {check_name}: {'Present' if check_data['exists'] else 'Missing'}")
        else:
            print(f"  [INFO] {check_name}: {check_data.get('note', 'See details in JSON')}")

    print(f"\nTimeline Estimate: {results['timeline_estimate']}")
    print(f"Knowledge Panel Eligible: {'Yes' if results['knowledge_panel_eligible'] else 'Not yet'}\n")

    print("Improvement Roadmap:")
    for item in results['roadmap']:
        print(f"  Priority {item['priority']}: {item['action']}")
        print(f"    Impact: {item['impact']} | Difficulty: {item['difficulty']} | Timeline: {item['timeline']}")
        print(f"    Requirements: {item['requirements']}\n")

    print(f"[FILE] Full report saved to: {args.output}")


if __name__ == "__main__":
    main()
