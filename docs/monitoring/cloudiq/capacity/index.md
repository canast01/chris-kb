# CloudIQ: Capacity Forecasting and Pool Utilisation

```
┌──────────────────────────────────── CloudIQ — Capacity Management ────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Capacity Overview               │  │                 Forecasting                 │   │
│   │              Total raw capacity              │  │            30/60/90 day forecast            │   │
│   │                 Used vs free                 │  │               ML growth model               │   │
│   │                Tier breakdown                │  │             Projected full date             │   │
│   │               Thin provision %               │  │               Confidence band               │   │
│   │              Snapshot overhead               │  │              Add-capacity alert             │   │
│   │              Reclaim candidates              │  │               Seasonal adjust               │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Capacity data from array firmware · Dell cloud processes and stores trend for forecast model         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Raw capacity = Total physical storage before RAID/parity overhead                                    │
│  Usable capacity = Raw minus RAID overhead; available for data                                        │
│  Thin provisioning = Allocating more logical capacity than physical; deduplication + compression expan│
│  Forecast = ML regression on historical consumption predicting when capacity will be exhausted        │
│  Confidence band = Upper/lower bound on forecast based on variance in historical data                 │
│  Add-capacity alert = CloudIQ alert when forecast horizon drops below threshold (e.g., 90 days)       │
│  Reclaim candidate = Volume with zero or near-zero utilisation; flagged for decommission review       │
│  Snapshot overhead = Capacity consumed by snapshots; tracked separately from primary data             │
│  Tier = Storage class within an array (e.g., NVMe, SAS, SSD) each with separate capacity              │
│  Seasonal adjustment = ML model accounting for cyclical usage spikes in forecast                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
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
