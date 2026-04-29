#!/usr/bin/env python3
"""
Keyword Clusterer Tool (Semantic ML Edition)
Uses state-of-the-art NLP (`sentence-transformers` via HuggingFace) and 
AgglomerativeClustering to group hundreds of disparate keywords 
into semantic "Topic Clusters" for building Pillar + Cluster strategies.

Usage:
    python keyword_clusterer.py --input .tmp/keywords.txt --output .tmp/clusters.json
    python keyword_clusterer.py --client acme_corp
"""

import argparse
import json
import os
import re
from pathlib import Path
from collections import defaultdict

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.cluster import AgglomerativeClustering
except ImportError:
    print("Installing required machine learning packages...")
    import subprocess
    subprocess.run(["pip", "install", "sentence-transformers", "scikit-learn"], check=True)
    from sentence_transformers import SentenceTransformer
    from sklearn.cluster import AgglomerativeClustering

def clean_keyword(kw):
    """Normalize keyword for clustering."""
    kw = str(kw).lower().strip()
    kw = re.sub(r'[^a-z0-9\s]', '', kw)
    return kw

_MODEL_INSTANCE = None

def get_model():
    global _MODEL_INSTANCE
    if _MODEL_INSTANCE is None:
        print(f"[*] Loading SentenceTransformer model (all-MiniLM-L6-v2) - this runs locally AND is cached in memory...")
        _MODEL_INSTANCE = SentenceTransformer('all-MiniLM-L6-v2')
    return _MODEL_INSTANCE

def cluster_keywords(keywords, distance_threshold=0.4):
    """
    Cluster a list of strings using Semantic Embeddings and Agglomerative Clustering.
    distance_threshold: The linkage distance threshold above which clusters will not be merged.
    Lower = tighter clusters (more clusters). Higher = broader clusters (fewer clusters).
    """
    if not keywords:
        return {}
        
    cleaned_kws = [clean_keyword(kw) for kw in keywords if kw]
    if not cleaned_kws:
        return {}
        
    print(f"[*] Fetching SentenceTransformer model (all-MiniLM-L6-v2)...")
    model = get_model()
    
    print(f"[*] Generating semantic embeddings for {len(cleaned_kws)} keywords...")
    embeddings = model.encode(cleaned_kws)
    
    print(f"[*] Clustering based on semantic meaning (threshold: {distance_threshold})...")
    # Using cosine distance, which maps nicely to semantic similarity
    clustering_model = AgglomerativeClustering(
        n_clusters=None, 
        distance_threshold=distance_threshold,
        linkage='average',
        metric='cosine'
    )
    clustering_model.fit(embeddings)
    
    clusters = defaultdict(list)
    labels = clustering_model.labels_
    
    for i, label in enumerate(labels):
        kw_original = keywords[i]
        
        # We don't have a name for the cluster yet, so use label ID temporarily
        clusters[f"Topic_Cluster_{label}"].append({
            "keyword": kw_original,
            "volume": 0
        })
            
    # Rename clusters based on the shortest, most generic keyword inside it
    renamed_clusters = {}
    for cluster_name, items in clusters.items():
        # Find the most general keyword (usually the shortest one by word count)
        sorted_items = sorted(items, key=lambda x: len(x["keyword"].split()))
        best_name = sorted_items[0]["keyword"].title()
        renamed_clusters[best_name] = items
            
    return renamed_clusters

def main():
    parser = argparse.ArgumentParser(description="SEO Semantic Keyword Clustering via HuggingFace transformers")
    parser.add_argument("--input", help="Path to text file with one keyword per line")
    parser.add_argument("--client", help="Client name to read keywords from brand kit")
    parser.add_argument("--threshold", type=float, default=0.5, help="Distance threshold for clustering (0.1 to 1.0). Higher = broader clusters.")
    parser.add_argument("--output", help="Output JSON path")
    args = parser.parse_args()

    keywords = []
    
    if args.input:
        if Path(args.input).exists():
            with open(args.input, 'r', encoding='utf-8') as f:
                keywords = [line.strip() for line in f if line.strip()]
        else:
            print(f"[Error] Input file not found: {args.input}")
            return
    elif args.client:
        brand_path = Path(f"clients/{args.client}/brand_kit.json")
        if brand_path.exists():
            with open(brand_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Try multiple possible locations for keywords
                keywords = []

                # Check seo_settings.primary_keywords (current format)
                seo_settings = data.get("seo_settings", {})
                primary = seo_settings.get("primary_keywords", [])
                keywords.extend(primary)

                # Check seo_targets (legacy format)
                seo_targets = data.get("seo_targets", {})
                keywords.extend(seo_targets.get("primary_keywords", []))
                keywords.extend(seo_targets.get("secondary_keywords", []))

                # Check content_pillars
                pillars = seo_settings.get("content_pillars", [])
                keywords.extend(pillars)

                # Check competitors to add their brand names as keywords
                competitors = data.get("seo_targets", {}).get("competitors", [])
                for comp in competitors:
                    if isinstance(comp, dict):
                        keywords.append(comp.get("name", ""))
        else:
            print(f"[Error] Brand kit not found: {brand_path}")
            print(f"[Tip] Run '/add_client {args.client}' first to create the client.")
            return
    
    # Remove duplicates and empty strings
    keywords = list(set([k for k in keywords if k]))
    
    if not keywords:
        print("[Error] No keywords found to cluster.")
        return

    print(f"[*] Clustering {len(keywords)} keywords...")
    clusters = cluster_keywords(keywords, distance_threshold=args.threshold)
    
    total_clusters = len(clusters)
    
    print(f"[*] Found {total_clusters} semantic topic clusters.")
    for name, items in clusters.items():
        print(f"\n[Cluster: {name}] ({len(items)} keywords)")
        for item in items[:5]:
            print(f"  - {item['keyword']}")
        if len(items) > 5:
            print(f"  ... and {len(items)-5} more")
            
    output_path = args.output or ".tmp/keyword_clusters.json"
    Path(output_path).parent.mkdir(exist_ok=True, parents=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(clusters, f, indent=2, ensure_ascii=False)
        
    print(f"\n[+] Saved complete semantic cluster mapping to {output_path}")

if __name__ == "__main__":
    main()
