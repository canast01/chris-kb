# CloudIQ: Capacity Forecasting and Pool Utilisation


<div class="kb-summary">
CloudIQ: Capacity Forecasting and Pool Utilisation reference covering Capacity Forecasting, Pool and Volume Utilisation, Threshold Alerts for Capacity, Common Capacity Issues.
</div>

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
│  Thin provisioning = More logical capacity than physical; dedup + compression expand ratio            │
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
