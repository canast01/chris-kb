---
tags:
  - aria-networks
  - operations
  - vmware
---
# vRNI Scripts

```python
#!/usr/bin/env python3
import requests, json, csv

VRNI_HOST = "vrni.example.local"
USERNAME = "admin@local"
PASSWORD = "changeme"
VERIFY_SSL = False

def get_token():
    url = f"https://{VRNI_HOST}/api/ni/auth/token"
    payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "domain": {"domain_type": "LOCAL"}
    }
    resp = requests.post(url, json=payload, verify=VERIFY_SSL)
    resp.raise_for_status()
    return resp.json()["token"]

TOKEN = get_token()
HEADERS = {"Authorization": f"NetworkInsight {TOKEN}", "Content-Type": "application/json"}
```
```text
┌──────────────────────────────────────────── vRNI Scripts ─────────────────────────────────────────────┐
│                                                                                                       │
│  REST API scripts for flow querying, data source management, and config export in vRNI.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Auth & Token Scripts             │  │              Flow Query Scripts             │   │
│   │           POST /auth/token + store           │  │            GET /flows?filter=...            │   │
│   │             Token refresh on 401             │  │           Filter by src/dst IP/VM           │   │
│   │         Python requests lib example          │  │           Export flow CSV via API           │   │
│   │          vRNI Python SDK available           │  │          Paginate with cursor param         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Auth scripts obtain tokens; flow scripts query and export; mgmt scripts configure sources.           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Data Source Mgmt Scripts           │  │            Config Export Scripts            │   │
│   │          GET /data-sources list all          │  │         Export all alert-rules JSON         │   │
│   │          POST /data-sources add new          │  │         Export all applications JSON        │   │
│   │          DELETE /data-sources/{id}           │  │            Export pinboards JSON            │   │
│   │         PUT /data-sources/{id} edit          │  │          Automate backup to S3/NFS          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRNI platform VM; scripts run from jump host or CI/CD pipeline with network access                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  REST API            = HTTP/JSON interface; all vRNI automation goes through this                     │
│  Bearer Token        = Short-lived auth token; refresh needed every 24 hours                          │
│  vRNI Python SDK     = VMware-provided library wrapping REST API calls                                │
│  GET /flows          = Flow query endpoint; supports filter, time-range, pagination                   │
│  Cursor Pagination   = API pattern returning next_cursor for large result sets                        │
│  GET /data-sources   = Returns all configured data sources with status and IDs                        │
│  POST /data-sources  = Adds a new data source from JSON body with type and creds                      │
│  Alert Rule Export   = JSON dump of all alert threshold rules for backup/restore                      │
│  Application Export  = JSON dump of application and tier definitions                                  │
│  Pinboard Export     = JSON dump of custom dashboards for backup and migration                        │
│  Filter Params       = Query string params: srcIp, dstIp, vmName, port, protocol                      │
│  CI/CD Integration   = Scripts run in pipelines for automated config drift detection                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```python
def get_open_problems():
    url = f"https://{VRNI_HOST}/api/ni/problems"
    params = {"size": 100, "cursor": ""}
    all_problems = []
    while True:
        resp = requests.get(url, headers=HEADERS, params=params, verify=VERIFY_SSL)
        data = resp.json()
        batch = data.get("results", [])
        all_problems.extend(batch)
        cursor = data.get("cursor", "")
        if not cursor or not batch:
            break
        params["cursor"] = cursor
    print(f"Open problems: {len(all_problems)}")
    for p in sorted(all_problems, key=lambda x: x.get("severity", "")):
        print(f"  [{p.get('severity','?')}] {p.get('name','?')}")
    return all_problems

get_open_problems()
```
```python
def export_security_recommendations(output_file="vrni-security-recs.csv"):
    url = f"https://{VRNI_HOST}/api/ni/micro-segmentation/recommendations"
    resp = requests.get(url, headers=HEADERS, verify=VERIFY_SSL)
    recs = resp.json().get("results", [])
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Application", "Source Group", "Destination Group",
            "Port", "Protocol", "Recommendation Type"
        ])
        for r in recs:
            writer.writerow([
                r.get("application_name", ""),
                r.get("source_security_group", ""),
                r.get("destination_security_group", ""),
                r.get("port", ""),
                r.get("protocol", ""),
                r.get("recommendation_type", "")
            ])
    print(f"Exported {len(recs)} recommendations → {output_file}")

export_security_recommendations()
```
```python
def check_data_source_health():
    """Returns list of unhealthy data sources. Exit 1 if any found."""
    import sys
    issues = []
    for endpoint in ["vcenters", "nsxt-managers", "physical-network-devices"]:
        url = f"https://{VRNI_HOST}/api/ni/data-sources/{endpoint}"
        try:
            resp = requests.get(url, headers=HEADERS, verify=VERIFY_SSL, timeout=10)
            for ds in resp.json().get("results", []):
                if ds.get("connection_status") != "Connected":
                    issues.append(
                        f"{endpoint}: {ds.get('nickname', ds.get('ip', '?'))} "
                        f"— {ds.get('connection_status')}"
                    )
        except Exception as e:
            issues.append(f"{endpoint}: request failed — {e}")
    if issues:
        print("UNHEALTHY:", "\n  ".join([""] + issues))
        sys.exit(1)
    else:
        print("OK: all data sources connected")
        sys.exit(0)

check_data_source_health()
```
```python
def add_ips_to_application(application_id, ip_list):
    url = f"https://{VRNI_HOST}/api/ni/groups/applications/{application_id}/ip-addresses"
    payload = {"ip_addresses": [{"ip_address": ip} for ip in ip_list]}
    resp = requests.post(url, headers=HEADERS, json=payload, verify=VERIFY_SSL)
    resp.raise_for_status()
    print(f"Added {len(ip_list)} IPs to application {application_id}")

add_ips_to_application(
    application_id="<application-entity-id>",
    ip_list=["10.10.1.50", "10.10.1.51", "10.10.1.52"]
)
```
```python
#!/usr/bin/env python3
"""
Cron: 0 7 * * * /opt/scripts/vrni-daily-health.py >> /var/log/vrni-health.log 2>&1
"""
import requests, datetime, sys

VRNI_HOST = "vrni.example.local"
USERNAME = "admin@local"
PASSWORD = "changeme"

def main():
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        token_resp = requests.post(
            f"https://{VRNI_HOST}/api/ni/auth/token",
            json={"username": USERNAME, "password": PASSWORD,
                  "domain": {"domain_type": "LOCAL"}},
            verify=False, timeout=15
        )
        token_resp.raise_for_status()
        headers = {"Authorization": f"NetworkInsight {token_resp.json()['token']}"}

        problems = requests.get(
            f"https://{VRNI_HOST}/api/ni/problems",
            headers=headers, verify=False, timeout=15
        ).json().get("results", [])

        critical = [p for p in problems if p.get("severity") == "CRITICAL"]
        print(f"{ts} problems={len(problems)} critical={len(critical)}")
        for p in critical:
            print(f"  CRITICAL: {p.get('name')}")
        sys.exit(0)
    except Exception as e:
        print(f"{ts} ERROR: {e}")
        sys.exit(1)

main()
```

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## See also

- [vRNI CLI Reference](cli-reference/)
- [AON Operational Procedures](procedures/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
