import os
import json
import requests
from base64 import b64encode
from dotenv import load_dotenv

load_dotenv()

TOKEN_FILE = "qb_tokens.json"
TOKEN_URL = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
BASE_URL = "https://sandbox-quickbooks.api.intuit.com"
REALM_ID = os.getenv("QB_REALM_ID")

def load_tokens():
    if not os.path.exists(TOKEN_FILE):
        raise Exception("Token file not found. Run the initial auth code exchange first.")
    with open(TOKEN_FILE, "r") as f:
        return json.load(f)


def save_tokens(tokens):
    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f)
    print("Saved new tokens")


def load_access_token():
    return load_tokens()["access_token"]


def load_refresh_token():
    return load_tokens()["refresh_token"]

def exchange_code_for_tokens(auth_code):
    creds = f"{os.getenv('QB_CLIENT_ID')}:{os.getenv('QB_CLIENT_SECRET')}"
    auth_header = b64encode(creds.encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": os.getenv("QB_REDIRECT_URI"),
    }

    r = requests.post(TOKEN_URL, headers=headers, data=data)
    r.raise_for_status()
    save_tokens(r.json())

def ensure_tokens():
    if os.path.exists(TOKEN_FILE):
        return

    auth_code = os.getenv("QB_AUTHORIZATION_CODE")
    if not auth_code:
        raise Exception(
            "No QuickBooks tokens found and QB_AUTHORIZATION_CODE is not set"
        )

    print("No QuickBooks tokens found. Exchanging authorization code...")
    exchange_code_for_tokens(auth_code)

def refresh_access_token(refresh_token):
    client_id = os.getenv("QB_CLIENT_ID")
    client_secret = os.getenv("QB_CLIENT_SECRET")
    creds = f"{client_id}:{client_secret}"
    auth_header = b64encode(creds.encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    r = requests.post(TOKEN_URL, headers=headers, data=data)
    r.raise_for_status()
    tokens = r.json()
    save_tokens(tokens)
    return tokens

def make_request(access_token, query):
    url = f"{BASE_URL}/v3/company/{REALM_ID}/query?minorversion=65"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Content-Type": "application/text",
    }
    return requests.post(url, headers=headers, data=query)

def qb_request(query):
    token = load_access_token()

    r = make_request(token, query)
    if r.status_code == 401:
        print("Access token expired, refreshing...")
        tokens = refresh_access_token(load_refresh_token())
        r = make_request(tokens["access_token"], query)

    r.raise_for_status()
    return r.json()