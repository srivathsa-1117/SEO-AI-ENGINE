#!/usr/bin/env python3
"""
Geospatial Local AEO Tool
Mathematically spoofs GPS coordinates to run localized AEO audits across specific zip codes.
Generates heatmaps (via Folium) for Local SEO clients to visualize "AI Share of Voice".

Usage:
    python geospatial_search.py --client local_plumbers --keyword "plumber near me" --zipcodes 90210,90211,90212
"""

import argparse
import json
import os
import random
from pathlib import Path
from datetime import datetime

try:
    from geopy.geocoders import Nominatim
    import folium
    import requests
except ImportError:
    print("Installing geospatial mapping dependencies...")
    import subprocess
    subprocess.run(["pip", "install", "geopy", "folium", "requests"], check=True)
    from geopy.geocoders import Nominatim
    import folium
    import requests

def get_coordinates_for_zip(zipcode: str):
    """Convert zip code to exact Latitude/Longitude."""
    geolocator = Nominatim(user_agent="SEO-AI-OS-GeoLocator")
    location = geolocator.geocode(f"{zipcode}")
    if location:
        return location.latitude, location.longitude
    return None, None

def mock_serp_spoofing(lat, lon, keyword, target_domain):
    """
    Simulates sending a localized API request to an Answer Engine or SERP API
    (In a production environment, this connects to a SERP API or uses Playwright).
    """
    print("[ERROR] Real SERP API integration required to spoof coordinates and fetch real AI share of voice.")
    import sys
    sys.exit(1)

def generate_local_heatmap(client: str, keyword: str, zipcodes: list, target_domain: str, output_dir: Path):
    """Generates an interactive HTML heatmap of AI Share of Voice."""
    print(f"[*] Initializing Geospatial Audit for '{keyword}' across {len(zipcodes)} zones.")

    heatmap_data = []
    center_lat, center_lon = 0, 0
    valid_zips = 0

    for z in zipcodes:
        z = z.strip()
        print(f"[*] Geolocating Zone: {z}")
        lat, lon = get_coordinates_for_zip(z)

        if lat and lon:
            print(f"    -> Spoofing coordinates: {lat}, {lon}")
            metrics = mock_serp_spoofing(lat, lon, keyword, target_domain)
            print(f"    -> AI Share of Voice: {metrics['share_of_voice']}% (Local Rank: {metrics['rank_position']})")

            heatmap_data.append({
                "zip": z,
                "lat": lat,
                "lon": lon,
                "metrics": metrics
            })
            center_lat += lat
            center_lon += lon
            valid_zips += 1
        else:
            print(f"    [!] Could not locate zip: {z}")

    if not heatmap_data:
        print("[Error] No valid zones to map.")
        return

    # Calculate center point for the map
    center_lat /= valid_zips
    center_lon /= valid_zips

    print("[*] Rendering Folium interactive heatmap visualization...")

    # Create map centered on the average coordinates
    m = folium.Map(location=[center_lat, center_lon], zoom_start=11, tiles="CartoDB positron")

    for data in heatmap_data:
        sov = data["metrics"]["share_of_voice"]
        # Color scale: Red (Low SOV) to Green (High SOV)
        color = "green" if sov >= 70 else "orange" if sov >= 40 else "red"

        html_popup = f"""
        <div style="font-family: Arial; min-width: 150px;">
            <h4>Zone {data['zip']}</h4>
            <b>Keyword:</b> {keyword}<br>
            <b>AI Share of Voice:</b> {sov}%<br>
            <b>Est. Local Rank:</b> {data['metrics']['rank_position']}<br>
            <b>AI Mention:</b> {'Yes [OK]' if data['metrics']['cited_in_ai'] else 'No [ERROR]'}
        </div>
        """

        folium.CircleMarker(
            location=[data["lat"], data["lon"]],
            radius=15,
            popup=folium.Popup(html_popup, max_width=300),
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6
        ).add_to(m)

    out_file = output_dir / f"heatmap_{client}_{datetime.now().strftime('%Y%m%d')}.html"
    m.save(str(out_file))
    print(f"\n[SUCCESS] Local AEO Heatmap saved to: {out_file}")

    # Also save raw JSON data
    json_file = output_dir / f"geo_data_{client}_{datetime.now().strftime('%Y%m%d')}.json"
    with open(json_file, "w") as f:
        json.dump(heatmap_data, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Geospatial Local AEO Mapping Tool")
    parser.add_argument("--client", required=True, help="Client slug")
    parser.add_argument("--keyword", required=True, help="Target keyword to map")
    parser.add_argument("--zipcodes", required=True, help="Comma separated list of zip/postal codes")
    parser.add_argument("--domain", default="example.com", help="Client's target domain")
    args = parser.parse_args()

    output_dir = Path(f".tmp/geospatial/{args.client}")
    output_dir.mkdir(parents=True, exist_ok=True)

    zips = args.zipcodes.split(',')
    generate_local_heatmap(args.client, args.keyword, zips, args.domain, output_dir)

if __name__ == "__main__":
    main()
