# Dell AIOps: Executive Reports, Trend Analysis, and Capacity Planning Exports


<div class="kb-summary">
Dell AIOps extends CloudIQ reporting with AI-enriched content: trend analysis, predicted capacity curves, and executive-level infrastructure health summaries. This page covers the available report types, scheduling, and export options.
</div>

## AIOps Report Types

Navigation: **CloudIQ > AIOps > Reports**

| Report | Audience | Frequency |
|---|---|---|
| Executive Health Summary | CTO/CIO, management | Monthly |
| Infrastructure Trend Analysis | Architects, engineers | Weekly |
| Capacity Planning Forecast | Storage administrators | Monthly |
| Recommendations Effectiveness | Operations leads | Monthly |
| Anomaly and Incident Timeline | Operations, security | On-demand / weekly |
| Bottleneck History | Performance engineers | On-demand |

## Generating an AIOps Report On-Demand

```bash
# Generate an executive health summary report
curl -sk -X POST \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/aiops/reports" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "EXECUTIVE_HEALTH_SUMMARY",
    "scope": "ALL_SYSTEMS",
    "date_range": {
      "start": "2026-04-01T00:00:00Z",
      "end": "2026-04-30T23:59:59Z"
    },
    "format": "PDF",
    "include_recommendations": true,
    "include_predictions": true
  }'

# Check generation status
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/aiops/reports/<reportId>" \
  -H "Authorization: Bearer <access_token>" \
  | jq '{status, download_url}'

# Download the report
curl -sk -X GET "<download_url>" \
  -H "Authorization: Bearer <access_token>" \
  -o aiops-exec-summary.pdf
```
```
┌─────────────────────────────────────── Dell AIOps — Reporting ────────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Built-in Reports               │  │               Export / Custom               │   │
│   │             Fleet health summary             │  │              CSV metric export              │   │
│   │                Alert history                 │  │                  PDF report                 │   │
│   │              Capacity forecast               │  │                API data pull                │   │
│   │            Recommendation status             │  │               Scheduled email               │   │
│   │              Performance trends              │  │                Grafana panels               │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Reports generated on AIOps master · CSV/PDF via browser · API for automation                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Fleet health report = Summary of all monitored systems with health score and issue count             │
│  Alert history = Time-series of alert activity; useful for trend and MTTR analysis                    │
│  Capacity forecast report = Per-system projected fill dates for procurement planning                  │
│  Performance trend = Historical IOPS/latency/throughput per system over custom window                 │
│  Recommendation status = Open/resolved/dismissed counts by category and priority                      │
│  CSV export = Raw metric data download for spreadsheet or BI tool consumption                         │
│  PDF report = Formatted document suitable for management or audit review                              │
│  Scheduled email = AIOps sending report on configured cadence to recipient list                       │
│  API data pull = REST GET to retrieve report data for custom downstream tooling                       │
│  Grafana panels = AIOps metrics exposed via REST and visualised in Grafana dashboards                 │
│  MTTR = Mean Time To Resolve; calculated from alert history open/close timestamps                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Common Reporting Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Executive summary shows incomplete data | Some systems have no telemetry | Check system connectivity status before generating |
| Prediction section blank | < 14 days of data | Allow longer data collection period |
| CSV export missing columns | Old API version | Upgrade to latest API endpoint version |
| Report not delivered | Email relay not configured | Check CloudIQ notification settings |
| Trend shows large unexplained spike | Bulk data migration or test | Note in report commentary; exclude from trend if needed |
