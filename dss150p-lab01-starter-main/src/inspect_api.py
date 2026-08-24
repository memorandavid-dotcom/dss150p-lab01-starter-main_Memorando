import json
import os
from datetime import datetime, timezone
import requests

# Check README.md for your lab's exact API URL if provided
API_URL = "https://jsonplaceholder.typicode.com/posts"

try:
    response = requests.get(API_URL, timeout=20)
    response.raise_for_status()

    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")

    payload = response.json()
    payload_type = type(payload)
    print(f"Top-level structure: {payload_type.__name__}")

    if isinstance(payload, list):
        print(f"Record Count: {len(payload)}")
        print("\nSample Record:")
        print(json.dumps(payload[0], indent=2))
    elif isinstance(payload, dict):
        print("\nSample Record (Keys):", list(payload.keys()))

    os.makedirs("data/raw", exist_ok=True)

    with open("data/raw/api_snapshot.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    utc_now = datetime.now(timezone.utc).isoformat()
    print(f"\nRetrieved at UTC: {utc_now}")

except requests.exceptions.RequestException as e:
    print(f"API Request Failed: {e}")