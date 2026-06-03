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
┌────────────────────────────────────── Pure1 — Integration Guide ──────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               ITSM Integration               │  │               Monitoring Stack              │   │
│   │              ServiceNow webhook              │  │                 Aria Ops PAK                │   │
│   │                Auto-incident                 │  │                Grafana panels               │   │
│   │               PagerDuty events               │  │                  Splunk HEC                 │   │
│   │                Slack webhook                 │  │              Custom REST script             │   │
│   │                 Email alerts                 │  │                py-pure-client               │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Pure1 in cloud · webhooks outbound to ITSM SaaS · REST API for on-prem consumers                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ServiceNow webhook = Pure1 POST to ServiceNow event endpoint on proactive alert                      │
│  Auto-incident = ServiceNow incident created from Pure1 alert payload                                 │
│  PagerDuty = On-call routing; Pure1 webhook delivers to PagerDuty Events API v2                       │
│  Slack webhook = Pure1 proactive alert posted to storage channel                                      │
│  Aria Ops PAK = VMware adapter pulling FlashArray/FlashBlade metrics into Aria Ops                    │
│  Grafana panels = Pure1 REST API proxied as Grafana data source                                       │
│  Splunk HEC = Pure1 alerts forwarded as events to Splunk for SIEM correlation                         │
│  py-pure-client = Pure-provided Python library for Pure1 and Purity REST APIs                         │
│  Custom REST script = Polling Pure1 API and pushing to proprietary dashboard/tooling                  │
│  Email = Pure1 SMTP notification for proactive alerts; configure in org settings                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
