#!/usr/bin/env python3
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow

def authenticate():
    print("[*] Starting Google Search Console OAuth Authentication Component...")
    creds_path = "tools/mcp-gsc/gsc_credentials.json"
    
    # Try looking in root as well depending on where they placed it
    if not os.path.exists(creds_path):
        creds_path = "tools/mcp-gsc/gsc_credentials.json.json"
        if not os.path.exists(creds_path):
           creds_path = "gsc_credentials.json"
     
    if not os.path.exists(creds_path):
        print(f"❌ Could not find OAuth Credentials at {creds_path}")
        return
        
    scopes = ['https://www.googleapis.com/auth/webmasters.readonly']
    
    try:
        flow = InstalledAppFlow.from_client_secrets_file(creds_path, scopes)
        print("[!] Opening browser to authenticate with Google...")
        creds = flow.run_local_server(port=0)
        
        token_path = "tools/mcp-gsc/token.pickle"
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
            
        print("✅ Authentication successful! The MCP has been granted access.")
        print("✅ Token saved to 'tools/mcp-gsc/token.pickle'")
        print("\nYou can now use the GSC MCP inside Claude!")
    except Exception as e:
        print(f"\n❌ Error during authentication: {e}")

if __name__ == "__main__":
    authenticate()
