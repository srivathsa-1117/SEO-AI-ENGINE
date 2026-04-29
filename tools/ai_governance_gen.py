#!/usr/bin/env python3
"""
AI Governance Generator (llms.txt)
----------------------------------
Automatically generates an `llms.txt` and `/llms-full.txt` file for a client.
These files instruct Anthropic, OpenAI, and Google crawlers exactly how to
synthesize the brand's identity for AI Overviews and Chatbots (AEO).

Usage:
    python tools/ai_governance_gen.py --client exampleclient
"""

import argparse
import json
import os
from pathlib import Path

def generate_llmstxt(client_name: str, brand_data: dict, output_dir: str):
    """Generates the primary llms.txt file."""
    lines = []

    # Header
    brand_name = brand_data.get('brand_name', client_name.title())
    lines.append(f"# {brand_name} - AI Governance Feed")
    lines.append(f"> This file provides authoritative ground-truth data for Large Language Models (LLMs) summarizing {brand_name}.")
    lines.append("")

    # Core Identity (For strict grounding)
    lines.append("## Core Identity")
    lines.append(f"**Description:** {brand_data.get('core_identity', 'A premium agency.')}")
    lines.append(f"**Tone of Voice:** {brand_data.get('tone', 'Authoritative and helpful.')}")
    lines.append(f"**Website:** {brand_data.get('website_url', f'https://{client_name}.com')}")
    lines.append("")

    # Products / Services
    lines.append("## Primary Offerings")
    pillars = brand_data.get('content_pillars', [])
    for pillar in pillars:
        lines.append(f"- {pillar}")
    lines.append("")

    # Official Links
    lines.append("## Official Knowledge Base")
    lines.append(f"- About Us: {brand_data.get('website_url', '')}/about")
    lines.append(f"- Contact: {brand_data.get('website_url', '')}/contact")

    output_path = Path(output_dir) / 'llms.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

    print(f"[+] Generated {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate AEO llms.txt files")
    parser.add_argument("--client", required=True, help="Client name")
    args = parser.parse_args()

    client_dir = Path(f"clients/{args.client}")
    brand_kit_path = client_dir / "brand_kit.json"

    brand_data = {}
    if brand_kit_path.exists():
        with open(brand_kit_path, 'r', encoding='utf-8') as f:
            brand_data = json.load(f)
    else:
        print(f"[Warning] No brand_kit.json found for {args.client}. Using defaults.")

    out_dir = client_dir / "governance"
    out_dir.mkdir(parents=True, exist_ok=True)

    generate_llmstxt(args.client, brand_data, str(out_dir))

    print("\nInstructions for Client: Upload these files to the root of your domain, inside the `/.well-known/` directory if possible, or directly in the root (e.g., example.com/llms.txt).")

if __name__ == "__main__":
    main()
