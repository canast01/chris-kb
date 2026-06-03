# Aria Operations — Scripts


<div class="kb-summary">
Scripts reference covering Export Active Alerts to CSV (Python), Capacity Report (PowerShell), Cluster Health Check (Bash), Alert Export via REST (Bash / curl), Related Sections.
</div>

Aria Operations API — Script Interaction Pattern
```text
┌─────────────────────────────────────────────────────┐
│  Script / Automation Pipeline                                                                         │
└──────────────────────┬──────────────────────────────┘
```
```text
┌─────────────────────────────────────── Aria Operations Scripts ───────────────────────────────────────┐
│                                                                                                       │
│  REST API scripts for alert management, metric queries, and resource ops in vROps.                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Auth & Token Scripts             │  │           Alert Management Scripts          │   │
│   │        POST /suite-api/api/auth/token        │  │         GET /api/alerts active list         │   │
│   │         Store token in env variable          │  │          PATCH /api/alerts/{id} ack         │   │
│   │           Refresh on 401 response            │  │         Filter by severity/resource         │   │
│   │          vROps Python SDK available          │  │             Export alerts to CSV            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Auth scripts get tokens; alert scripts manage state; metric scripts extract data.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Metric Query Scripts             │  │            Resource Mgmt Scripts            │   │
│   │        GET /api/resources/{id}/stats         │  │           GET /api/resources list           │   │
│   │         Query by resource+metric key         │  │            Filter by adapter kind           │   │
│   │           Set begin/end time range           │  │          Tag resources via REST API         │   │
│   │          Export to InfluxDB/Grafana          │  │             Delete stale objects            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vROps cluster; scripts run from jump host or CI/CD with HTTPS access to master node                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  suite-api           = vROps REST API base path; all automation uses this prefix                      │
│  Auth Token          = Bearer token; obtained via POST /auth/token; 24h TTL                           │
│  GET /alerts         = Returns active alerts; filterable by criticality and resource                  │
│  PATCH /alerts       = Acknowledge or cancel an alert by ID                                           │
│  GET /resources      = Lists all monitored objects with adapter kind and ID                           │
│  GET /stats          = Returns metric time-series for a specific resource ID                          │
│  Metric Key          = Unique identifier for a metric; e.g. cpu|usage_average                         │
│  Time Range          = begin/end epoch ms parameters for metric query                                 │
│  vROps Python SDK    = Broadcom-provided library wrapping REST API calls                              │
│  InfluxDB Export     = Send vROps metrics to InfluxDB for Grafana dashboards                          │
│  Stale Object Delete = Remove objects from vROps no longer in source                                  │
│  Tag                 = Custom label on vROps resource for grouping and filtering                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
                       │ 2. Parse JSON response
                       ▼
```text
```
```text
┌─────────────────────────────────────────────────────┐
│  Output / Integration                                                                                 │
│  → CSV export (alerts, capacity, idle VMs)                                                            │
│  → monitoring dashboard (HTTP POST)                                                                   │
│  → ITSM integration                                                                                   │
│  NOTE: re-authenticate every 25 min for long runs                                                     │
└─────────────────────────────────────────────────────┘
```text
┌─────────────────────────────────────── Aria Operations Scripts ───────────────────────────────────────┐
│                                                                                                       │
│  REST API scripts for alert management, metric queries, and resource ops in vROps.                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Auth & Token Scripts             │  │           Alert Management Scripts          │   │
│   │        POST /suite-api/api/auth/token        │  │         GET /api/alerts active list         │   │
│   │         Store token in env variable          │  │          PATCH /api/alerts/{id} ack         │   │
│   │           Refresh on 401 response            │  │         Filter by severity/resource         │   │
│   │          vROps Python SDK available          │  │             Export alerts to CSV            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Auth scripts get tokens; alert scripts manage state; metric scripts extract data.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Metric Query Scripts             │  │            Resource Mgmt Scripts            │   │
│   │        GET /api/resources/{id}/stats         │  │           GET /api/resources list           │   │
│   │         Query by resource+metric key         │  │            Filter by adapter kind           │   │
│   │           Set begin/end time range           │  │          Tag resources via REST API         │   │
│   │          Export to InfluxDB/Grafana          │  │             Delete stale objects            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vROps cluster; scripts run from jump host or CI/CD with HTTPS access to master node                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  suite-api           = vROps REST API base path; all automation uses this prefix                      │
│  Auth Token          = Bearer token; obtained via POST /auth/token; 24h TTL                           │
│  GET /alerts         = Returns active alerts; filterable by criticality and resource                  │
│  PATCH /alerts       = Acknowledge or cancel an alert by ID                                           │
│  GET /resources      = Lists all monitored objects with adapter kind and ID                           │
│  GET /stats          = Returns metric time-series for a specific resource ID                          │
│  Metric Key          = Unique identifier for a metric; e.g. cpu|usage_average                         │
│  Time Range          = begin/end epoch ms parameters for metric query                                 │
│  vROps Python SDK    = Broadcom-provided library wrapping REST API calls                              │
│  InfluxDB Export     = Send vROps metrics to InfluxDB for Grafana dashboards                          │
│  Stale Object Delete = Remove objects from vROps no longer in source                                  │
│  Tag                 = Custom label on vROps resource for grouping and filtering                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Capacity Report (PowerShell)

```powershell
## Export cluster capacity summary via REST API
$AriaOpsHost = "aria-ops.domain.local"
$Token       = "your-token-here"

$Headers = @{ Authorization = "vRealizeOpsToken $Token" }

## Get all cluster compute resources
$Uri = "https://$AriaOpsHost/suite-api/api/resources?resourceKind=ClusterComputeResource"
$Response = Invoke-RestMethod -Uri $Uri -Headers $Headers -SkipCertificateCheck

foreach ($cluster in $Response.resourceList) {
    Write-Output "Cluster: $($cluster.resourceKey.name)"
}
```

---

## Cluster Health Check (Bash)

```bash
#!/usr/bin/env bash
## Quick Aria Operations cluster health check
HOST="aria-ops.domain.local"

echo "=== Aria Operations Cluster Health ==="
ssh admin@$HOST "vracli cluster health"

echo ""
echo "=== Adapter Status ==="
ssh admin@$HOST "vracli adapter list"

echo ""
echo "=== Service Status ==="
ssh admin@$HOST "vracli status"
```

---

## Alert Export via REST (Bash / curl)

```bash
#!/usr/bin/env bash
HOST="aria-ops.domain.local"
USER="admin"
PASS="changeme"

## Get token
TOKEN=$(curl -sk -X POST "https://$HOST/suite-api/api/auth/token/acquire" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USER\",\"authSource\":\"LOCAL\",\"password\":\"$PASS\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

echo "Token acquired"

## Export active alerts
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://$HOST/suite-api/api/alerts?activeOnly=true" \
  | python3 -m json.tool > /tmp/aria-ops-alerts-$(date +%Y%m%d).json

echo "Alerts saved to /tmp/aria-ops-alerts-$(date +%Y%m%d).json"
```

---

## Related Sections

- [CLI Reference](../cli-reference/index.md) — vracli and REST API basics
- [Operations](../index.md) — operational runbooks
- [Troubleshooting](../../troubleshooting/index.md) — diagnostic use cases
