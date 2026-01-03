import requests
import json

URL = "http://localhost/api/v1/optimize"
PAYLOAD = {"stops": []}

try:
    print(f"Sending request to {URL}...")
    response = requests.post(URL, json=PAYLOAD, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    if response.status_code == 200:
        print("[SUCCESS] Kubernetes Deployment Verification Passed!")
    else:
         print("[FAIL] Verification Failed: Status code not 200")
except Exception as e:
    print(f"[FAIL] Verification Failed: {e}")
