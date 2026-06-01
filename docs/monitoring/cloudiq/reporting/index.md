# CloudIQ: Reports — On-Demand, Scheduled, Export, and Sharing


<div class="kb-summary">
Dell CloudIQ provides built-in reporting for capacity, health, alerts, and recommendations across your Dell infrastructure fleet. Reports can be generated on demand or scheduled for recurring delivery.
</div>

## Report Types Available

Navigation: **CloudIQ > Reports**

| Report Type | Content | Audience |
|---|---|---|
| System Health Summary | Health scores, active alerts, component status | Operations team |
| Capacity Forecast | Utilisation trends and days-until-full per system | Storage administrators |
| Alert History | All alerts over a date range by severity | Operations, management |
| Recommendations Summary | Active and resolved recommendations | Architects, engineers |
| Data Reduction | Deduplication and compression ratios | Capacity planners |
| Performance Summary | Throughput, IOPS, latency averages | Performance engineers |

## Generating an On-Demand Report

```bash
# Trigger an on-demand health report via CloudIQ API
curl -sk -X POST \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/reports" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "HEALTH_SUMMARY",
    "system_ids": ["<systemId1>", "<systemId2>"],
    "date_range": {
      "start": "2026-04-01T00:00:00Z",
      "end": "2026-04-30T23:59:59Z"
    },
    "format": "PDF"
  }'

# Check report generation status
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/reports/<reportId>" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json" | jq '{status, download_url}'

# Download completed report
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/reports/<reportId>/download" \
  -H "Authorization: Bearer <access_token>" \
  -o cloudiq-health-report.pdf
```
┌───────────────────────────────────────── CloudIQ — Reporting ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Built-in Reports               │  │               Custom / Export               │   │
│   │             Fleet health summary             │  │             CSV capacity export             │   │
│   │              Capacity forecast               │  │              PDF health report              │   │
│   │                Alert history                 │  │                API data pull                │   │
│   │              Performance trends              │  │                Schedule email               │   │
│   │            Recommendation status             │  │              Custom time range              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Reports generated in Dell cloud · PDF/CSV download via browser · API for automation                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Fleet health summary = Report showing all arrays with current health score and issue count           │
│  Capacity forecast report = Per-array projected full dates for planning horizon                       │
│  Alert history = Time-series of alerts over selected period; useful for trend analysis                │
│  Performance trend = Historical IOPS/latency/bandwidth per array over custom window                   │
│  Recommendation status = Open/resolved/dismissed counts per category and priority                     │
│  CSV export = Comma-separated raw data download; import into Excel or BI tool                         │
│  PDF report = Formatted document suitable for management review or audit                              │
│  Scheduled email = CloudIQ sending report on defined cadence to recipient list                        │
│  API data pull = REST GET calls to retrieve report data programmatically                              │
│  Custom time range = Selecting arbitrary start/end dates for historical report generation             │
│  BI tool = Business intelligence platform (Tableau, Power BI) consuming CloudIQ CSV exports           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```

## Sharing Reports

- **PDF reports** can be emailed directly from the scheduler or manually from the Reports UI using **Share > Email**.
- **Shareable links** are not supported; recipients need a CloudIQ login to view live dashboards.
- For stakeholders without CloudIQ access, schedule PDF delivery to their inbox.

## Common Report Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Report not delivered | Email address not verified or spam filtered | Confirm address in Settings, whitelist cloudiq.dell.com |
| Report shows no data | No systems in selected scope | Re-check system filter in report config |
| CSV export malformed | Special characters in system names | Use API with explicit field selection |
| Scheduled report skipped | Temporary CloudIQ service interruption | Reports auto-retry; check History for status |
| Report download link expired | Links expire after 24 hours | Re-generate the report from Reports > History |
