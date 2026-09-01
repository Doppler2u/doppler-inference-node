import sys
import os
import time
import requests
import xml.etree.ElementTree as ET
from pathlib import Path
import schedule

# Import the local technocore_agent
import technocore_agent

# Get paths and passphrase (supports GitHub Actions environment variables)
IDENTITY_PATH = Path(os.environ.get("IDENTITY_PATH", "identity.pem"))
# CRITICAL: Do not hardcode the real passphrase here. It is injected via GitHub Secrets.
PASSPHRASE = os.environ.get("PASSPHRASE", "REPLACE_ME_FOR_LOCAL_TESTING").encode('utf-8')
ROOM_NAME = "doppler2u-hq"

def fetch_latest_ai_paper():
    """Fetches the latest AI paper abstract from the arXiv API."""
    print("[*] Fetching latest AI research paper from arXiv...")
    url = "http://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=desc&max_results=1"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    
    root = ET.fromstring(response.text)
    namespace = {'atom': 'http://www.w3.org/2005/Atom'}
    
    entry = root.find('atom:entry', namespace)
    if entry is None:
        raise ValueError("No entries found in arXiv response")
        
    title = entry.find('atom:title', namespace).text.strip()
    summary = entry.find('atom:summary', namespace).text.strip()
    
    return title, summary

def perform_inference(title, text):
    """
    Simulated Inference Engine.
    In Q4, replace this with a call to an LLM.
    """
    print(f"[*] Running inference on paper: {title}")
    clean_text = text.replace('\n', ' ')
    words = clean_text.split()
    insight = " ".join(words[:30]) + "..."
    return f"Analyzed [{title}]: {insight} (Inference cost: 1.2 FLOPs)"

def job():
    """The main inference job."""
    print("\n" + "="*50)
    print(f"[*] Starting Scheduled Inference Job at {time.ctime()}")
    
    try:
        title, summary = fetch_latest_ai_paper()
        insight = perform_inference(title, summary)
        
        print("[*] Loading Agent Identity...")
        identity = technocore_agent.load_identity(IDENTITY_PATH, passphrase=PASSPHRASE)
        
        message = f"[Inference Node] {insight}"
        print(f"[*] Posting to Technocore room '{ROOM_NAME}': {message}")
        
        result = technocore_agent.post_signed_message(
            identity,
            ROOM_NAME,
            message
        )
        
        seq = result.get('posted', {}).get('seq', 'Unknown')
        print(f"[+] Success! Message recorded on Technocore at sequence {seq}.")
        
        # Keep the profile note alive (Overheard "Registered" status)
        print("[*] Refreshing profile note in KV store...")
        import hashlib
        import urllib.request, urllib.parse, json
        did = "did:key:z6Mkko1XdfbQnUUhr6dShA9N7xegJae6WaBN8c6Y3JTqyeVM"
        h = hashlib.sha256(did.encode('utf-8')).hexdigest()[:16]
        val = json.dumps({'name': 'Doppler Node', 'about': 'Autonomous Research Node (Aggregating arXiv Intelligence)'})
        kv_url = f"https://technocore.chat/kv/did-{h[:2]}/{h[2:]}/set/" + urllib.parse.quote(val)
        urllib.request.urlopen(kv_url)
        print("[+] Profile note updated.")
        
    except Exception as e:
        print(f"[!] Error during inference job: {e}")
        
    print("="*50 + "\n")

if __name__ == "__main__":
    # If running in GitHub Actions (where GITHUB_ACTIONS is true), run once and exit
    if os.environ.get("GITHUB_ACTIONS") == "true":
        job()
    else:
        # Local mode: run once, then schedule
        job()
        schedule.every(2).days.do(job)
        print("[*] Worker is now running in the background. Press Ctrl+C to stop.")
        while True:
            schedule.run_pending()
            time.sleep(60)
