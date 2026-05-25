# CloudIQ: Capacity Forecasting and Pool Utilisation

```text
Capacity Analytics — CloudIQ
                                         ← 90-day warning
                   consumed              │
Used ▲  ╭─────────────────────╮         │ ← 30-day critical
     │  │ current: 68%        │──────────────────────►
     │  │                     │ forecast (linear trend)
     │  │  reclaimable: 12%   │
     │  │                     ▼
     │  │  net projected full:  ~75 days
     │  │
     └──┼─────────────────────────────────────► time
       now        +30d      +60d         +90d

┌──────────────────────────────────────────┐
│  Threshold Alerts                        │
│  Days Until Full < 90  → Minor   alert  │
│  Days Until Full < 30  → Major   alert  │
│  Days Until Full <  7  → Critical alert │
└──────────────────────────────────────────┘
```

Dell CloudIQ provides capacity forecasting across all registered storage systems. It uses telemetry data to project when pools, volumes, and file systems will reach defined thresholds. This page covers capacity views, forecasting methodology, and threshold alert configuration.

## Capacity Dashboard Overview

Navigation: **CloudIQ > Capacity**

The Capacity dashboard shows aggregate utilisation across all registered systems and allows drill-down to individual arrays or pools.

| View | What it Shows |
|---|---|
| Fleet Overview | Percentage full across all systems |
| By System Type | PowerStore, PowerMax, PowerScale breakout |
| Top 10 Fullest | Systems or pools closest to capacity |
| Forecast Timeline | Projected full dates plotted on a timeline |

## System-Level Capacity Metrics

```bash
# Get capacity summary for all storage systems
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/storage_systems?select=id,name,capacity_used_tb,capacity_total_tb,capacity_used_percent" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json" | jq '.results[] | {name, used: .capacity_used_percent}'

# Get capacity for a specific PowerStore system
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/storage_systems/<systemId>/capacity" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json"
```

Key capacity metrics available via API:

| Field | Description |
|---|---|
| `capacity_used_tb` | Currently used raw capacity in TB |
| `capacity_total_tb` | Total usable capacity in TB |
| `capacity_used_percent` | Percentage utilisation |
| `days_until_full` | Projected days until pool full |
| `efficiency_ratio` | Data reduction ratio (dedupe + compression) |

## Capacity Forecasting

CloudIQ forecasts capacity exhaustion using a linear regression over the last 30 days of growth data. The forecast is updated daily.

Navigation: **CloudIQ > Capacity > [System] > Forecast**

Forecast indicators:

| Indicator | Threshold | Typical Alert Severity |
|---|---|---|
| Days Until Full < 90 | Warning | Minor |
| Days Until Full < 30 | Escalated warning | Major |
| Days Until Full < 7 | Critical runway | Critical |

Forecast accuracy is highest when growth is consistent. Spikes from bulk data migrations can skew short-term projections; use the 90-day trend for planning.

## Pool and Volume Utilisation

For block storage systems (PowerStore, PowerMax):

```bash
# List storage pools with utilisation
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/storage_pools?select=name,capacity_used_percent,days_until_full&filter=system_id%20eq%20'<systemId>'" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json" | jq '.results[]'
```

For file systems (PowerScale/Isilon), check file system capacity:

```bash
# List file systems with utilisation
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/file_systems?select=name,capacity_used_percent,capacity_total_gb" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json"
```

## Threshold Alerts for Capacity

Configure capacity threshold alerts so the team is notified before pools reach critical levels.

Navigation: **CloudIQ > Settings > Notifications > Capacity Thresholds**

| Threshold Type | Recommended Value | Alert Severity |
|---|---|---|
| Pool utilisation | 75% | Minor |
| Pool utilisation | 85% | Major |
| Days until full | 30 days | Major |
| Days until full | 7 days | Critical |

## Common Capacity Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Forecast shows N/A | Less than 7 days of data | Wait for more telemetry to accumulate |
| Days until full wildly inaccurate | Bulk migration skewing trend | Use 90-day view to smooth out spikes |
| Used capacity not matching array UI | Data reduction ratio difference | CloudIQ shows logical used; check raw vs logical |
| New pool not showing | System telemetry not yet pushed | Check SRS connectivity and wait 1 collection cycle |
