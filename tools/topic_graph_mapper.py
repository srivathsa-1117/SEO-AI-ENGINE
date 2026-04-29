#!/usr/bin/env python3
"""
Topic Graph Mapper Tool (2026 Standard)
Uses the Wikipedia API to build a semantic knowledge graph for Topical Authority.
In 2026, topical authority is calculated based on coverage of closely related entities, not just keyword permutations.
"""

import argparse
import json
import requests
import networkx as nx
from typing import Dict, List

class TopicGraphMapper:
    def __init__(self):
        self.wiki_api = "https://en.wikipedia.org/w/api.php"

    def fetch_related_entities(self, primary_topic: str, depth: int = 15) -> List[str]:
        """Fetches outgoing links from a Wikipedia page to represent related entities."""
        params = {
            "action": "query",
            "format": "json",
            "titles": primary_topic,
            "prop": "links",
            "pllimit": max(50, depth),
            "plnamespace": "0" # Only standard articles
        }
        
        headers = {
            "User-Agent": "SEOAI-OS/1.0 (https://example.com; bot@example.com)"
        }
        try:
            response = requests.get(self.wiki_api, params=params, headers=headers, timeout=10)
            data = response.json()
            
            pages = data.get("query", {}).get("pages", {})
            for page_id, page_info in pages.items():
                if page_id == "-1":
                    return [] # Page doesn't exist
                    
                links = page_info.get("links", [])
                return [link["title"] for link in links[:depth]]
            
            return []
        except Exception as e:
            print(f"[ERROR] Failed to fetch Wikipedia entities for '{primary_topic}': {str(e)}")
            return []

    def build_topic_graph(self, core_topic: str) -> Dict:
        """Builds a hub-and-spoke graph of related semantic topics."""
        print(f"Building semantic topic graph for core topic: {core_topic}")
        
        G = nx.Graph()
        G.add_node(core_topic, type="hub")
        
        # Level 1 Entities (Sub-Pillars)
        level_1 = self.fetch_related_entities(core_topic, depth=8)
        
        if not level_1:
            return {"error": f"Could not map topic '{core_topic}'. Try a more recognized semantic concept."}
            
        topics = {"core_hub": core_topic, "sub_pillars": []}
        
        for idx, sub_topic in enumerate(level_1):
            G.add_node(sub_topic, type="spoke")
            G.add_edge(core_topic, sub_topic)
            
            # Fetch Level 2 entities (Supporting content)
            print(f"  -> Mapping sub-pillar: {sub_topic}...")
            level_2 = self.fetch_related_entities(sub_topic, depth=5)
            
            # Filter out backwards links to the core topic or the current sub-pillar
            filtered_level_2 = [t for t in level_2 if t.lower() != core_topic.lower() and t.lower() != sub_topic.lower()]
            
            for leaf in filtered_level_2:
                G.add_node(leaf, type="leaf")
                G.add_edge(sub_topic, leaf)
                
            topics["sub_pillars"].append({
                "pillar_name": sub_topic,
                "supporting_articles": filtered_level_2
            })
            
        topics["graph_metrics"] = {
            "total_nodes": G.number_of_nodes(),
            "total_edges": G.number_of_edges()
        }
        
        return topics

def main():
    parser = argparse.ArgumentParser(description="Topic Graph Mapper")
    parser.add_argument("--topic", required=True, help="Core seed topic (e.g., 'Digital marketing')")
    parser.add_argument("--output", help="Path to save output JSON")
    
    args = parser.parse_args()
    
    mapper = TopicGraphMapper()
    results = mapper.build_topic_graph(args.topic)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"[OK] Topic Graph saved to {args.output}")
    else:
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
