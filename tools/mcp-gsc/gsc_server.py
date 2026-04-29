#!/usr/bin/env python3
"""
Google Search Console (GSC) MCP Server
--------------------------------------
A Model Context Protocol (MCP) server that seamlessly connects the AIOS to 
Google Search Console using FastMCP. It provides tools for fetching search analytics, 
querying top keywords, and inspecting URLs.

Configuration:
    - Requires a Service Account JSON key.
    - Set environment variable GSC_CREDENTIALS_PATH to the key's location.
      (Default expects 'gsc_credentials.json' in the root directory)
"""

import os
import sys
import subprocess
from typing import List, Dict, Any

# Ensure mcp and google-api-python-client are installed
try:
    from mcp.server.fastmcp import FastMCP
    from googleapiclient.discovery import build
    from google.auth.transport.requests import Request
    import pickle
except ImportError:
    print("Installing required GSC MCP dependencies...", file=sys.stderr)
    subprocess.run(["pip", "install", "mcp", "google-api-python-client", "google-auth-oauthlib"], check=True)
    from mcp.server.fastmcp import FastMCP
    from googleapiclient.discovery import build
    from google.auth.transport.requests import Request
    import pickle

# Initialize the MCP Server
mcp = FastMCP("GSC_MCP_Server")

def get_gsc_service(api='webmasters', version='v3'):
    """Authenticates and builds the Google API service client using OAuth 2.0."""
    creds = None
    token_path = os.getenv("GSC_TOKEN_PATH", "tools/mcp-gsc/token.pickle")
    
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
            
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
        else:
            raise PermissionError(
                f"❌ Authentication required! "
                f"Please open a separate terminal and run: `python tools/mcp-gsc/auth.py` to authenticate your Google account via browser."
            )
            
    return build(api, version, credentials=creds)

@mcp.tool()
def list_verified_sites() -> List[str]:
    """
    Retrieves a list of all website properties verified in the Google Search Console account.
    """
    try:
        service = get_gsc_service()
        site_list = service.sites().list().execute()
        sites = [site['siteUrl'] for site in site_list.get('siteEntry', [])]
        return sites if sites else ["No verified sites found for this service account."]
    except Exception as e:
        return [f"Error fetching sites: {str(e)}"]

@mcp.tool()
def get_search_analytics(site_url: str, start_date: str, end_date: str, dimensions: List[str] = ['query'], row_limit: int = 10) -> Dict[str, Any]:
    """
    Fetches Search Analytics data from GSC.
    
    Args:
        site_url: The exact GSC property URL (e.g., 'https://example.com/')
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format
        dimensions: List of dimensions to pivot by. Options: 'query', 'page', 'country', 'device', 'date'.
        row_limit: Number of rows to return (default 10)
    """
    try:
        service = get_gsc_service()
        request_body = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': dimensions,
            'rowLimit': row_limit
        }
        response = service.searchanalytics().query(siteUrl=site_url, body=request_body).execute()
        return response
    except Exception as e:
        return {"error": f"Failed to fetch analytics: {str(e)}"}

@mcp.tool()
def inspect_google_index(site_url: str, inspection_url: str) -> Dict[str, Any]:
    """
    Inspects a specific URL to see its live indexing status in Google's index.
    
    Args:
        site_url: The root GSC property URL
        inspection_url: The exact page URL to inspect
    """
    try:
        # The URL Inspection API uses the 'searchconsole' v1 endpoint
        service = get_gsc_service(api='searchconsole', version='v1')
        request_body = {
            "inspectionUrl": inspection_url,
            "siteUrl": site_url,
            "languageCode": "en-US"
        }
        response = service.urlInspection().index().inspect(body=request_body).execute()
        return response
    except Exception as e:
        return {"error": f"Failed to inspect URL: {str(e)}"}

if __name__ == "__main__":
    # Launch the FastMCP Server on standard input/output (Claude's default mechanism)
    mcp.run()
