# Nexus Dashboard Scripts

## Authentication

Nexus Dashboard REST API uses OAuth2 token authentication. ACI APIC uses cookie-based authentication. Scripts load credentials from the secrets manager at runtime.

### Nexus Dashboard API Auth

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

### ACI APIC API Auth

```python
APIC_BASE = "https://<apic-vip>"

def apic_login(username: str, password: str) -> requests.Session:
    """Obtain authenticated APIC session."""
    session = requests.Session()
    resp = session.post(f"{APIC_BASE}/api/aaaLogin.json", json={
        "aaaUser": {"attributes": {"name": username, "pwd": password}}
    }, verify=True)
    resp.raise_for_status()
    return session   # session cookie is set automatically

def apic_get(session: requests.Session, path: str) -> dict:
    resp = session.get(f"{APIC_BASE}{path}", verify=True)
    resp.raise_for_status()
    return resp.json()
```

## ND Cluster Health Check

```python
def nd_cluster_health(token: str) -> list:
    """Return node status for all cluster nodes."""
    data = nd_get("/nexus/infra/nodes", token)
    nodes = []
    for node in data.get("nodes", []):
        nodes.append({
            "name": node["name"],
            "status": node["status"],
            "role": node.get("role"),
            "ip": node.get("management_ip")
        })
    return nodes

if __name__ == "__main__":
    token = nd_login("svc-nd-script", "<password>")
    for node in nd_cluster_health(token):
        status = "OK" if node["status"] == "active" else "ALERT"
        print(f"[{status}] {node['name']} ({node['ip']}) — {node['status']}")
```

## Fabric Fault Export

```python
import csv

def export_fabric_faults(token: str, min_severity: str, output_file: str):
    """Export active fabric faults filtered by severity."""
    data = nd_get("/nexus/infra/faults", token,
                  params={"severity": min_severity, "state": "active"})
    faults = data.get("faults", [])
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "title", "severity", "fabric", "node", "created_at"
        ])
        writer.writeheader()
        for fault in faults:
            writer.writerow({
                "id": fault["id"],
                "title": fault.get("title"),
                "severity": fault.get("severity"),
                "fabric": fault.get("fabric_name"),
                "node": fault.get("node_name"),
                "created_at": fault.get("created_at")
            })
    print(f"Exported {len(faults)} faults to {output_file}")
```

## ACI Fault Summary (via APIC)

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

## Forward P1/P2 Faults to ServiceNow

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

## Script Inventory

| Script | Purpose | Schedule |
|---|---|---|
| `nd_health_check.py` | Query ND REST API for cluster node health and service status | Daily |
| `fabric_fault_export.py` | Export active fabric faults to CSV (filtered by severity and fabric) | Daily |
| `ndfc_compliance_report.py` | Generate policy compliance report for all NDFC-managed fabrics | Weekly |
| `alert_to_servicenow.py` | Forward P1/P2 fabric faults to ServiceNow | Event-driven |
| `apic_fault_summary.py` | Query ACI APIC REST API for fault counts by severity and category | Daily |

Scripts are stored in `scripts/nexus-dashboard/`. Load all credentials from the secrets manager. Use `verify=True` for all HTTPS calls (add internal CA bundle path if required: `verify="/path/to/ca-bundle.crt"`).
