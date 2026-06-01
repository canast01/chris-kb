# InsightIQ Scripts

<div class="kb-summary">
InsightIQ Scripts reference covering Authentication, Threshold Alert Forwarding (SNMP), Automated Weekly Report Generation, Script Inventory, OneFS Performance Query (Direct API).
</div>

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
┌──────────────────────────────────── InsightIQ — Scripts Reference ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │               InsightIQ admin scripts — run on appliance or via management host               │   │
│   │             iiq_backup.sh — wrapper triggering iiq_backup with dated archive name             │   │
│   │                  disk-check.sh — alerts if InsightIQ VM datastore > 80% full                  │   │
│   │                  collection-check.sh — verifies data age < 5 minutes via API                  │   │
│   │           export-report.py — uses InsightIQ API to download scheduled report as PDF           │   │
│   │             top-clients.py — queries InsightIQ for top-IO clients; posts to Slack             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Scripts on InsightIQ VM or management host · Python 3 + requests · SSH for admin                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  iiq_backup = Admin CLI command; wrapper script adds date suffix to archive                           │
│  Disk check = df -h /data check on appliance; alert at 80% to avoid DB fill                           │
│  Data age = Time since last collection point; stale > 5 min suggests collection issue                 │
│  InsightIQ API = Limited REST API at https://<iiq>/api; used for report downloads                     │
│  Session cookie = InsightIQ API uses session auth; POST login to get cookie                           │
│  Top clients = List of client IPs ranked by IO; requires clientstats on cluster                       │
│  Slack webhook = Posting top-client summary to storage team Slack channel                             │
│  Cron schedule = Running scripts via crontab on management host or InsightIQ VM                       │
│  SSH key auth = Prefer SSH key over password for script access to InsightIQ                           │
│  Log check = Tail /var/log/isilon/insightiq/ for collection errors                                    │
│  PDF download = GET /api/v1/reports/{id}/download with session cookie                                 │
│  Python requests = pip install requests; standard HTTP library for InsightIQ API                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
