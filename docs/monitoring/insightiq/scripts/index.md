# InsightIQ Scripts

## Authentication

Scripts authenticate to the InsightIQ REST API using basic authentication with the admin service account. Credentials are loaded from the secrets manager at runtime.

```python
import requests
from requests.auth import HTTPBasicAuth

IIQ_BASE = "https://<insightiq-host>"
AUTH     = HTTPBasicAuth("svc-iiq-admin", "<password-from-secrets-manager>")

def iiq_get(path: str, params: dict = None) -> dict:
    resp = requests.get(f"{IIQ_BASE}/api/v2{path}",
                        auth=AUTH, params=params, verify=True)
    resp.raise_for_status()
    return resp.json()
```

## Export Performance Data

```python
import csv
from datetime import datetime, timedelta, timezone

def export_performance(cluster_name: str, hours: int, output_file: str):
    """Export throughput and latency data for a cluster over the last N hours."""
    end   = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)

    data = iiq_get("/performance", params={
        "cluster": cluster_name,
        "start": int(start.timestamp()),
        "end":   int(end.timestamp()),
        "metrics": "total_throughput,nfs_latency,smb_latency"
    })

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "total_throughput",
                                                "nfs_latency", "smb_latency"])
        writer.writeheader()
        for sample in data.get("samples", []):
            writer.writerow(sample)
    print(f"Exported {len(data.get('samples', []))} samples to {output_file}")
```

## Cluster Connection Health Check

```python
def check_cluster_connections() -> list:
    """Return list of clusters with disconnected status."""
    clusters = iiq_get("/clusters").get("clusters", [])
    disconnected = [
        {"name": c["name"], "status": c["status"], "last_data": c.get("last_data_timestamp")}
        for c in clusters
        if c.get("status") != "active"
    ]
    return disconnected

if __name__ == "__main__":
    issues = check_cluster_connections()
    if issues:
        for c in issues:
            print(f"ALERT: cluster {c['name']} status={c['status']}, last_data={c['last_data']}")
    else:
        print("All clusters are active.")
```

## Threshold Alert Forwarding (SNMP)

```python
from pysnmp.hlapi import *

SNMP_TARGET   = "<monitoring-platform-ip>"
SNMP_PORT     = 162
SNMP_COMMUNITY = "public"

def send_snmp_trap(cluster: str, metric: str, value: float, threshold: float):
    send_notification(
        SnmpEngine(),
        CommunityData(SNMP_COMMUNITY),
        UdpTransportTarget((SNMP_TARGET, SNMP_PORT)),
        ContextData(),
        "trap",
        NotificationType(ObjectIdentity("1.3.6.1.4.1.12345.1")).addVarBinds(
            ("1.3.6.1.4.1.12345.1.1", OctetString(cluster)),
            ("1.3.6.1.4.1.12345.1.2", OctetString(metric)),
            ("1.3.6.1.4.1.12345.1.3", OctetString(f"{value:.2f}")),
        )
    )
    print(f"Sent SNMP trap: {cluster} {metric}={value} (threshold={threshold})")
```

## Automated Weekly Report Generation

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def email_report(report_bytes: bytes, filename: str, recipients: list):
    msg = MIMEMultipart()
    msg["From"]    = "insightiq-reports@company.com"
    msg["To"]      = ", ".join(recipients)
    msg["Subject"] = f"InsightIQ Weekly Utilisation Report — {filename}"

    part = MIMEBase("application", "octet-stream")
    part.set_payload(report_bytes)
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={filename}")
    msg.attach(part)

    with smtplib.SMTP("relay.company.com", 587) as smtp:
        smtp.starttls()
        smtp.send_message(msg)
```

## Script Inventory

| Script | Purpose | Schedule |
|---|---|---|
| `export_performance.py` | Export throughput and latency data for a date range | On demand |
| `generate_report.py` | Automate weekly utilisation report generation and email | Weekly |
| `threshold_alert.py` | Compare latest metrics to thresholds; send SNMP trap on breach | Every 5 minutes (cron) |
| `cluster_health_check.py` | Check all cluster connection statuses; alert on disconnected clusters | Daily |

Scripts are stored in `scripts/insightiq/`. Load credentials from the secrets manager at runtime using an environment variable or vault client. Use the `verify=True` SSL flag to enforce certificate validation.

## OneFS Performance Query (Direct API)

For direct OneFS performance queries (bypass InsightIQ):

```bash
# Query OneFS statistics API directly
curl -sk -u svc-insightiq https://<cluster-ip>:8080/platform/1/statistics/summary/drive | jq .
curl -sk -u svc-insightiq https://<cluster-ip>:8080/platform/3/statistics/current \
  -G --data-urlencode 'keys=node.ifs.bytes.in.rate,node.ifs.bytes.out.rate' | jq .
```
