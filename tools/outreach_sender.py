import os
import json
import logging
import requests
from typing import Dict, Any

logger = logging.getLogger(__name__)

HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")
CACHE_FILE = ".tmp/hunter_cache.json"

def find_emails_for_outreach(domain: str) -> str:
    """
    Uses Hunter.io API to find emails for a domain and generates basic outreach templates.
    """
    if not HUNTER_API_KEY:
        return json.dumps({"error": "HUNTER_API_KEY is not set in .env. Please configure it to use this feature."})
        
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            try:
                cache = json.load(f)
            except json.JSONDecodeError:
                pass

    emails_data = None
    if domain in cache:
        logger.info(f"Returning cached Hunter data for {domain}")
        emails_data = cache[domain]
    else:
        try:
            url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={HUNTER_API_KEY}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                emails_data = response.json().get('data', {})
                cache[domain] = emails_data
                with open(CACHE_FILE, "w") as f:
                    json.dump(cache, f, indent=4)
            else:
                return json.dumps({"error": f"Hunter API error: {response.status_code}", "message": response.text})
        except Exception as e:
            return json.dumps({"error": str(e)})
            
    emails = emails_data.get('emails', [])
    if not emails:
        return json.dumps({"domain": domain, "message": "No emails found.", "drafts": []})
        
    drafts = []
    for email_obj in emails[:3]: # Limit to top 3 contacts
        first_name = email_obj.get('first_name') or 'there'
        draft = f"Subject: Question about your content on {domain}\n\nHi {first_name},\n\nI was reading your article on {domain} and noticed a resource is outdated or missing. I've put together a comprehensive, updated guide that might be a great fit for your readers.\n\nLet me know if you'd like to check it out!\n\nBest,\n[Your Name]"
        drafts.append({
            "email": email_obj.get('value'),
            "type": email_obj.get('position', 'General'),
            "confidence": email_obj.get('confidence'),
            "template": draft
        })
        
    return json.dumps({"domain": domain, "outreach_opportunities": drafts}, indent=2)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", required=True)
    args = parser.parse_args()
    print(find_emails_for_outreach(args.domain))
