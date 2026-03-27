# Advanced Example by @multilogin-automation
"""
Professional migration example: Using Playwright with Multilogin X API (Local Port 35000)
This script demonstrates how to launch a Multilogin X profile and connect Playwright for advanced stealth automation.
"""

import requests
import time
from playwright.sync_api import sync_playwright

# Multilogin X API config
MLX_API = "http://127.0.0.1:35000/api/v2/profile/start"
PROFILE_ID = "YOUR_PROFILE_ID"  # Replace with your Multilogin X profile ID

# Start Multilogin X profile
resp = requests.post(MLX_API, json={"profileId": PROFILE_ID})
resp.raise_for_status()
profile_info = resp.json()

ws_endpoint = profile_info.get("wsEndpoint")
if not ws_endpoint:
    raise Exception("WebSocket endpoint not returned by Multilogin X API.")

print(f"[+] Multilogin X profile started. Connecting Playwright to: {ws_endpoint}")

# Wait briefly to ensure profile is ready
for _ in range(10):
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(ws_endpoint)
            page = browser.new_page()
            page.goto("https://www.example.com")
            print("[+] Page title:", page.title())
            # Custom stealth logic can be added here
            browser.close()
        break
    except Exception as e:
        print("[!] Waiting for profile to be ready...", e)
        time.sleep(1)
else:
    raise Exception("Failed to connect Playwright to Multilogin X profile.")

print("[+] Migration complete. You are now using Multilogin X with Playwright.")
