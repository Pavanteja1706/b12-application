import hashlib
import hmac
import json
import os
from datetime import datetime, timezone


def build_payload():
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") + \
                f"{datetime.now(timezone.utc).microsecond // 1000:03d}Z"

    payload = {
        "action_run_link": os.environ.get("ACTION_RUN_LINK", ""),
        "email": "pavantejajukanti@gmail.com",
        "name": "Pavan Teja Jukanti",
        "repository_link": "https://github.com/Pavanteja1706/b12-application",
        "resume_link": "https://docs.google.com/document/d/1TJFSXXWm5PQT4u6mhUguf9VkuS4fM-8f/edit?usp=sharing",
        "timestamp": timestamp,
    }
    return payload


def sign_payload(payload_bytes, secret):
    secret_bytes = secret.encode("utf-8")
    signature = hmac.new(secret_bytes, payload_bytes, hashlib.sha256).hexdigest()
    return f"sha256={signature}"


def submit():
    payload = build_payload()

    payload_json = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    payload_bytes = payload_json.encode("utf-8")

    signing_secret = "hello-there-from-b12"
    signature = sign_payload(payload_bytes, signing_secret)

    headers = {
        "Content-Type": "application/json",
        "X-Signature-256": signature,
    }

    print(f"Submitting application for: {payload['name']}")
    print(f"Timestamp: {payload['timestamp']}")
    print(f"Payload: {payload_json}")
    print(f"Signature: {signature}")

    import requests
    response = requests.post(
        "https://b12.io/apply/submission",
        data=payload_bytes,
        headers=headers,
    )

    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 200:
        result = response.json()
        print(f"\nSUCCESS! Receipt: {result.get('receipt')}")
    else:
        print(f"\nSubmission failed.")


if __name__ == "__main__":
    submit()
