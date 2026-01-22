import os
import requests

BASE_URL = "https://sandbox-quickbooks.api.intuit.com"

def qb_request(query):
    headers = {
        "Authorization": f"Bearer {os.getenv('QB_ACCESS_TOKEN')}",
        "Accept": "application/json",
        "Content-Type": "text/plain"
    }

    url = f"{BASE_URL}/v3/company/{os.getenv('QB_REALM_ID')}/query?query={query}&minorversion=75"

    r = requests.post(url, headers=headers)
    r.raise_for_status()
    return r.json()