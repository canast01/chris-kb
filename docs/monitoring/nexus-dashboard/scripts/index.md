```python
import requests

ND_BASE = "https://<nd-vip>"

def nd_login(username: str, password: str) -> str:
    """Obtain ND API token."""
    resp = requests.post(f"{ND_BASE}/login", json={
        "userName": username,
        "userPasswd": password,
        "domain": "local"   # or LDAP domain name
    }, verify=True)
    resp.raise_for_status()
    return resp.json()["token"]

def nd_get(path: str, token: str, params: dict = None) -> dict:
    headers = {"Authorization": token, "Content-Type": "application/json"}
    resp = requests.get(f"{ND_BASE}{path}", headers=headers,
                        params=params, verify=True)
    resp.raise_for_status()
    return resp.json()
```

```text
┌───────────────────────────────── Nexus Dashboard — Scripts Reference ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             NDI REST API scripts — Python examples                            │   │
│   │                   get-token.py: POST /sedgeapi/v1/auth/token → Bearer token                   │   │
│   │                 get-anomalies.py: GET /sedgeapi/v1/ndi/anomalies?status=ACTIVE                │   │
│   │            site-health.py: GET /sedgeapi/v1/ndi/sites/{id}/health — score per site            │   │
│   │               acs-health-check.sh: SSH to ND master → acs health → parse output               │   │
│   │              nd-backup.sh: SSH to ND → acs backup create → verify archive exists              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Scripts from management host · Python 3 + requests + paramiko · ND TCP 443/22                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  sedgeapi = NDI REST API path prefix; all NDI endpoints start with /sedgeapi/v1                       │
│  Bearer token = Auth credential from /auth/token; pass in Authorization header                        │
│  anomalies endpoint = NDI list of active anomalies with severity and affected objects                 │
│  site health endpoint = NDI health score for a specific fabric site                                   │
│  acs health = CLI command on ND master showing cluster node status                                    │
│  paramiko = Python SSH library for running acs commands remotely                                      │
│  acs backup create = Creates ND config snapshot; verify with acs backup list                          │
│  Status filter = ?status=ACTIVE to return only unresolved anomalies                                   │
│  Site ID = UUID of fabric site; retrieve from /sedgeapi/v1/ndi/sites                                  │
│  Pagination = NDI API uses offset/limit; default 25 records per page                                  │
│  Cron = Schedule scripts via crontab for daily health and backup checks                               │
│  JSON response = NDI API returns JSON; parse with json module or jq                                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```python
def apic_fault_summary(session: requests.Session) -> dict:
    """Return fault counts by severity from APIC."""
    data = apic_get(session, "/api/class/faultSummary.json")
    summary = {"critical": 0, "major": 0, "minor": 0, "warning": 0}
    for fault in data.get("imdata", []):
        attrs = fault["faultSummary"]["attributes"]
        sev = attrs.get("severity", "").lower()
        if sev in summary:
            summary[sev] += int(attrs.get("count", 0))
    return summary
```
```python
import os

SNOW_URL  = os.environ["SNOW_URL"]
SNOW_AUTH = (os.environ["SNOW_USER"], os.environ["SNOW_PASSWORD"])

def create_incident(fault: dict) -> str:
    priority = "1" if fault["severity"] in ("critical",) else "2"
    payload = {
        "short_description": f"Cisco ND Fault: {fault['title']} — {fault.get('fabric')}",
        "description": f"Severity: {fault['severity']}\nFabric: {fault.get('fabric')}\nNode: {fault.get('node')}\nND Fault ID: {fault['id']}",
        "severity": priority,
        "assignment_group": "network-ops"
    }
    resp = requests.post(f"{SNOW_URL}/api/now/table/incident",
                         auth=SNOW_AUTH, json=payload)
    resp.raise_for_status()
    return resp.json()["result"]["number"]
```
