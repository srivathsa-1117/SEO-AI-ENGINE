#!/usr/bin/env python3
"""
Schema Generator Tool
Generates valid JSON-LD schema markup for AEO/GEO optimization.

[WARNING]  IMPORTANT — Google Schema Deprecation Status (2024-2026):
  - FAQPage schema: RESTRICTED to government and healthcare sites only (since Aug 2023).
    Do NOT use for commercial, agency, or e-commerce clients.
  - HowTo schema: DEPRECATED (since Sept 2023). Not supported by Google.
  - SpecialAnnouncement: DEPRECATED (July 2025).

Supported types for commercial sites:
  Article, LocalBusiness, Organization, WebSite, BreadcrumbList, Product, Service

Usage:
    python schema_gen.py --type Article --title "My Article" --url https://example.com/article
    python schema_gen.py --type LocalBusiness --business-name "Acme Corp" --city "Austin" --state "TX"
"""

import argparse
import json
from datetime import datetime
from pathlib import Path


def generate_article_schema(title: str, url: str, author: str = "Site Author",
                             description: str = "", published: str = None, org_name: str = "") -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title[:110],
        "description": description[:300] if description else "",
        "url": url,
        "datePublished": published or datetime.now().strftime("%Y-%m-%d"),
        "dateModified": datetime.now().strftime("%Y-%m-%d"),
        "author": {
            "@type": "Person",
            "name": author
        },
        "publisher": {
            "@type": "Organization",
            "name": org_name or "Your Agency",
            "logo": {
                "@type": "ImageObject",
                "url": f"https://yoursite.com/logo.png"
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": url
        }
    }


def generate_faq_schema(faq_pairs: list) -> dict:
    """
    faq_pairs: list of {"question": "...", "answer": "..."} dicts
    """
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": q["answer"]
                }
            }
            for q in faq_pairs
        ]
    }


def generate_local_business_schema(name: str, url: str, phone: str = "",
                                    street: str = "", city: str = "", state: str = "",
                                    zip_code: str = "", country: str = "US",
                                    business_type: str = "LocalBusiness",
                                    description: str = "") -> dict:
    return {
        "@context": "https://schema.org",
        "@type": business_type,
        "name": name,
        "url": url,
        "telephone": phone,
        "description": description,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": street,
            "addressLocality": city,
            "addressRegion": state,
            "postalCode": zip_code,
            "addressCountry": country
        }
    }


def generate_organization_schema(name: str, url: str, logo_url: str = "",
                                  description: str = "", social_links: list = None,
                                  entity_mode: bool = False, wikidata_id: str = "",
                                  wikipedia_url: str = "", address: dict = None,
                                  phone: str = "", email: str = "") -> dict:
    schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": name,
        "url": url,
        "description": description,
        "logo": {
            "@type": "ImageObject",
            "url": logo_url or f"{url}/logo.png"
        }
    }
    
    if entity_mode:
        schema["@id"] = f"{url}/#organization"
        
    same_as = []
    if social_links:
        same_as.extend(social_links)
        
    if entity_mode:
        if wikidata_id:
            same_as.append(f"https://www.wikidata.org/wiki/{wikidata_id}")
        if wikipedia_url:
            same_as.append(wikipedia_url)
            
    if same_as:
        schema["sameAs"] = same_as

    if entity_mode and address:
        schema["address"] = {
            "@type": "PostalAddress",
            "streetAddress": address.get("streetAddress", ""),
            "addressLocality": address.get("addressLocality", ""),
            "addressRegion": address.get("addressRegion", ""),
            "postalCode": address.get("postalCode", ""),
            "addressCountry": address.get("addressCountry", "")
        }
        
    if entity_mode and (phone or email):
        schema["contactPoint"] = {
            "@type": "ContactPoint"
        }
        if phone:
            schema["contactPoint"]["telephone"] = phone
        if email:
            schema["contactPoint"]["email"] = email

    return schema


def generate_breadcrumb_schema(breadcrumbs: list) -> dict:
    """
    breadcrumbs: list of {"name": "...", "url": "..."} in order from root to current page
    """
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": idx + 1,
                "name": item["name"],
                "item": item["url"]
            }
            for idx, item in enumerate(breadcrumbs)
        ]
    }


def generate_triple_stack(org_data: dict, article_data: dict = None,
                          breadcrumbs: list = None) -> list:
    """
    Generate triple schema stacking for maximum Gemini/Google optimization.

    Returns a list of 2-3 separate schema objects:
    1. Organization (with entity linking)
    2. Article (if article_data provided)
    3. BreadcrumbList (if breadcrumbs provided)

    Each schema is complete and independent, but can be embedded on the same page.

    Args:
        org_data: dict with keys: name, url, logo_url, description, social_links,
                  wikidata_id, wikipedia_url, address (dict), phone, email
        article_data: dict with keys: title, url, author, description, published
        breadcrumbs: list of {"name": "...", "url": "..."} dicts

    Returns:
        List of schema dicts (2-3 schemas)
    """
    schemas = []

    # 1. Organization schema (always included, with entity linking)
    org_schema = generate_organization_schema(
        name=org_data["name"],
        url=org_data["url"],
        logo_url=org_data.get("logo_url", ""),
        description=org_data.get("description", ""),
        social_links=org_data.get("social_links", []),
        entity_mode=True,  # Always enable entity mode for triple stack
        wikidata_id=org_data.get("wikidata_id", ""),
        wikipedia_url=org_data.get("wikipedia_url", ""),
        address=org_data.get("address"),
        phone=org_data.get("phone", ""),
        email=org_data.get("email", "")
    )
    schemas.append(org_schema)

    # 2. Article schema (if article data provided)
    if article_data:
        article_schema = generate_article_schema(
            title=article_data["title"],
            url=article_data["url"],
            author=article_data.get("author", "Site Author"),
            description=article_data.get("description", ""),
            published=article_data.get("published"),
            org_name=org_data["name"]
        )
        # Link Article to Organization via @id
        article_schema["publisher"]["@id"] = f"{org_data['url']}/#organization"
        schemas.append(article_schema)

    # 3. BreadcrumbList schema (if breadcrumbs provided)
    if breadcrumbs and len(breadcrumbs) > 0:
        breadcrumb_schema = generate_breadcrumb_schema(breadcrumbs)
        schemas.append(breadcrumb_schema)

    return schemas


def wrap_in_script_tag(schema: dict) -> str:
    """Wrap schema dict in a <script> tag for HTML embedding."""
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'


def wrap_schemas_in_script_tags(schemas: list) -> str:
    """
    Wrap multiple schemas in separate <script> tags for triple stacking.
    Each schema gets its own <script type="application/ld+json"> block.
    """
    return "\n\n".join([wrap_in_script_tag(schema) for schema in schemas])


def main():
    parser = argparse.ArgumentParser(description="JSON-LD Schema Generator")
    parser.add_argument("--type", required=True,
                        choices=["Article", "LocalBusiness", "Organization", "BreadcrumbList", "Product", "Service", "TripleStack"],
                        help="Schema type. Use 'TripleStack' for Gemini optimization (Org + Article + Breadcrumbs). Note: FAQPage is restricted to gov/health sites. HowTo is deprecated.")
    parser.add_argument("--output", help="Output file path (JSON or HTML)")
    parser.add_argument("--wrap-html", action="store_true", help="Wrap in <script> tag")

    # Article args
    parser.add_argument("--title")
    parser.add_argument("--url")
    parser.add_argument("--author", default="Site Author")
    parser.add_argument("--description", default="")
    parser.add_argument("--published")
    parser.add_argument("--org-name", default="")

    # FAQ args
    parser.add_argument("--faq-file", help="JSON file with list of {question, answer} pairs")
    parser.add_argument("--faq-json", help="Inline JSON string with FAQ pairs")

    # LocalBusiness args
    parser.add_argument("--business-name")
    parser.add_argument("--phone", default="")
    parser.add_argument("--street", default="")
    parser.add_argument("--city", default="")
    parser.add_argument("--state", default="")
    parser.add_argument("--zip", default="")
    parser.add_argument("--country", default="US")
    parser.add_argument("--business-type", default="LocalBusiness")

    # Organization args
    parser.add_argument("--logo-url", default="")
    parser.add_argument("--social-links", help="Comma-separated social profile URLs")
    parser.add_argument("--entity-mode", action="store_true", help="Enable rich entity schema")
    parser.add_argument("--wikidata-id", default="")
    parser.add_argument("--wikipedia-url", default="")
    parser.add_argument("--email", default="")

    # Breadcrumb args
    parser.add_argument("--breadcrumbs-json", help="JSON string: [{name, url}, ...]")

    args = parser.parse_args()

    schema = {}

    if args.type == "Article":
        assert args.title and args.url, "--title and --url required for Article schema"
        schema = generate_article_schema(args.title, args.url, args.author,
                                          args.description, args.published, args.org_name)

    elif args.type == "FAQPage":
        if args.faq_file:
            with open(args.faq_file, "r", encoding="utf-8") as f:
                faq_pairs = json.load(f)
        elif args.faq_json:
            faq_pairs = json.loads(args.faq_json)
        else:
            print("[Error] --faq-file or --faq-json required for FAQPage"); return
        schema = generate_faq_schema(faq_pairs)

    elif args.type == "LocalBusiness":
        assert args.business_name and args.url, "--business-name and --url required"
        schema = generate_local_business_schema(
            args.business_name, args.url, args.phone,
            args.street, args.city, args.state, args.zip,
            args.country, args.business_type, args.description
        )

    elif args.type == "Organization":
        # Support both --org-name and --business-name for flexibility
        org_name = args.org_name or args.business_name
        assert org_name and args.url, "--org-name (or --business-name) and --url required"
        social = [s.strip() for s in args.social_links.split(",")] if args.social_links else []
        
        address_dict = None
        if args.entity_mode and (args.street or args.city or args.state or args.zip or args.country):
            address_dict = {
                "streetAddress": args.street,
                "addressLocality": args.city,
                "addressRegion": args.state,
                "postalCode": args.zip,
                "addressCountry": args.country
            }
            
        schema = generate_organization_schema(org_name, args.url,
                                              args.logo_url, args.description, social,
                                              args.entity_mode, args.wikidata_id,
                                              args.wikipedia_url, address_dict,
                                              args.phone, args.email)

    elif args.type == "TripleStack":
        # Triple schema stacking for Gemini/Google optimization
        org_name = args.org_name or args.business_name
        assert org_name and args.url, "--org-name (or --business-name) and --url required for TripleStack"

        # Build org_data dict
        social = [s.strip() for s in args.social_links.split(",")] if args.social_links else []
        address_dict = None
        if args.street or args.city or args.state or args.zip or args.country:
            address_dict = {
                "streetAddress": args.street,
                "addressLocality": args.city,
                "addressRegion": args.state,
                "postalCode": args.zip,
                "addressCountry": args.country
            }

        org_data = {
            "name": org_name,
            "url": args.url,
            "logo_url": args.logo_url,
            "description": args.description,
            "social_links": social,
            "wikidata_id": args.wikidata_id,
            "wikipedia_url": args.wikipedia_url,
            "address": address_dict,
            "phone": args.phone,
            "email": args.email
        }

        # Build article_data dict (optional)
        article_data = None
        if args.title:
            article_data = {
                "title": args.title,
                "url": args.url,  # Can be different if needed
                "author": args.author,
                "description": args.description,
                "published": args.published
            }

        # Build breadcrumbs list (optional)
        breadcrumbs = None
        if args.breadcrumbs_json:
            breadcrumbs = json.loads(args.breadcrumbs_json)

        # Generate triple stack
        schemas = generate_triple_stack(org_data, article_data, breadcrumbs)

        # For triple stack, we need to handle output differently
        if args.wrap_html:
            output_content = wrap_schemas_in_script_tags(schemas)
        else:
            # Output as JSON array
            output_content = json.dumps(schemas, indent=2)

        # Write output and exit early (skip single-schema logic below)
        if args.output:
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output_content)
            print(f"[Output] Triple schema stack saved to: {args.output}")
            print(f"[Info] Generated {len(schemas)} schemas: {', '.join([s['@type'] for s in schemas])}")
        else:
            print(output_content)
        return  # Exit early to avoid single-schema output logic

    elif args.type == "BreadcrumbList":
        assert args.breadcrumbs_json, "--breadcrumbs-json required"
        schema = generate_breadcrumb_schema(json.loads(args.breadcrumbs_json))

    # Output
    output_content = wrap_in_script_tag(schema) if args.wrap_html else json.dumps(schema, indent=2)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_content)
        print(f"[Output] Saved to: {args.output}")
    else:
        print(output_content)


if __name__ == "__main__":
    main()
