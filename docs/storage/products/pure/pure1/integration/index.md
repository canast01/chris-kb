---
tags:
  - pure
---
# Pure1 — Integration Guide

```bash
# Verify array connectivity from Purity CLI
purearray list --connection
# Expected: pure1.purestorage.com connected

# Check array network configuration
purearray list --network

# Set proxy if needed
purearray set --proxy https://<proxy-host>:<port>
```

```text
Aria Operations > Admin > Solutions > Pure Storage Management Pack
- Pure1 API endpoint: https://api.pure1.purestorage.com
- API key / private key: (service account key from Pure1)
- Collection interval: 5 minutes
```
```python
# Example: scheduled Pure1 API pull for Splunk index
# Runs every 15 minutes via Splunk scripted input or cron

import requests, json, time

# Auth using Pure1 RSA private key (see scripts/pure1/authentication.py)
headers = {"Authorization": f"Bearer {get_pure1_token()}"}
resp    = requests.get("https://api.pure1.purestorage.com/api/1.latest/arrays",
                       headers=headers)
for array in resp.json()["items"]:
    event = {
        "source": "pure1",
        "name": array["name"],
        "os": array.get("os"),
        "version": array.get("version"),
        "time": int(time.time())
    }
    print(json.dumps(event))  # Splunk scripted input reads stdout
```

```d2
direction: down

component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

component_a -> component_b: uses
component_b -> component_c: uses
```
