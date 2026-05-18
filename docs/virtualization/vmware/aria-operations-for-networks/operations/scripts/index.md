# Aria Operations for Networks — Scripts

```
┌─────────────── Aria Networks REST API Scripts ─────────────────────────────────┐
│                                                                                 │
│  All scripts follow this pattern:                                               │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  1. get_token()  ── POST /api/ni/auth/token ──► bearer token             │  │
│  │  2. HEADERS = {"Authorization": f"NetworkInsight {TOKEN}"}               │  │
│  │  3. call API endpoint ── parse results                                   │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│  Available scripts:                                                              │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  list_data_sources()        ── vcenters / nsxt / physical devices        │  │
│  │  get_flows_for_vm(name)     ── POST /api/ni/search ── flow query         │  │
│  │  get_open_problems()        ── GET /api/ni/problems ── paginated         │  │
│  │  export_security_recs()     ── GET microseg recommendations ► CSV       │   │
│  │  check_data_source_health() ── all sources Connected? ► exit 0/1        │   │
│  │  add_ips_to_application()   ── POST /api/ni/groups/applications/{id}    │   │
│  │  daily_health_report()      ── problems count + critical list ── cron   │   │
│  └──────────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## Authenticate and Get API Token

```python
#!/usr/bin/env python3
import requests, json, csv

VRNI_HOST = "vrni.corp.local"
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

---

## List All Data Sources and Status

```python
def list_data_sources():
    for endpoint in ["vcenters", "nsxt-managers", "physical-network-devices"]:
        url = f"https://{VRNI_HOST}/api/ni/data-sources/{endpoint}"
        resp = requests.get(url, headers=HEADERS, verify=VERIFY_SSL)
        for ds in resp.json().get("results", []):
            name = ds.get("nickname") or ds.get("ip", "?")
            status = ds.get("connection_status", "UNKNOWN")
            print(f"[{endpoint}] {name} — {status}")

list_data_sources()
```

---

## Get Flows for a Source VM

```python
def get_flows_for_vm(vm_name, limit=100):
    url = f"https://{VRNI_HOST}/api/ni/search"
    payload = {
        "query": f"flows where source_vm.name = '{vm_name}'",
        "page": {"start_index": 0, "end_index": limit}
    }
    resp = requests.post(url, headers=HEADERS, json=payload, verify=VERIFY_SSL)
    results = resp.json().get("results", [])
    print(f"Flows from {vm_name}: {len(results)}")
    for flow in results:
        src = flow.get("source_ip", {}).get("ip_address", "?")
        dst = flow.get("destination_ip", {}).get("ip_address", "?")
        port = flow.get("port", {}).get("port_number", "?")
        proto = flow.get("protocol", "?")
        print(f"  {src} → {dst}:{port}/{proto}")

get_flows_for_vm("web-server-01")
```

---

## Get All Open Problems

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

---

## Export Security Recommendations to CSV

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

---

## Check Data Source Health (Monitoring Integration)

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

---

## Bulk-Add IPs to Application Group

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

---

## Daily Health Report (Cron-ready)

```python
#!/usr/bin/env python3
"""
Cron: 0 7 * * * /opt/scripts/vrni-daily-health.py >> /var/log/vrni-health.log 2>&1
"""
import requests, datetime, sys

VRNI_HOST = "vrni.corp.local"
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
