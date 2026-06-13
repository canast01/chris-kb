---
tags:
  - netapp
---
# InsightIQ: Capacity Trending, Protocol Breakdown, and Quota Monitoring


<div class="kb-summary">
InsightIQ: Capacity Trending, Protocol Breakdown, and Quota Monitoring reference covering Protocol-Level Capacity Breakdown, Quota Monitoring, Common Capacity Issues.
</div>

```text
┌─────────────────────────────────── InsightIQ — Capacity Management ───────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Capacity Metrics               │  │                 Forecasting                 │   │
│   │              Total usable space              │  │              Growth rate trend              │   │
│   │              Used vs available               │  │             Projected full date             │   │
│   │              Per-tier breakdown              │  │              Linear regression              │   │
│   │             Dedup/compress ratio             │  │                Custom horizon               │   │
│   │              Quota utilisation               │  │             Export for planning             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Capacity data from PAPI · trend analysis in InsightIQ · export for spreadsheet planning              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Usable space = Total cluster capacity after RAID overhead                                            │
│  Tier = Storage class within PowerScale (SSD, SAS, HDD) each with separate capacity                   │
│  Dedup ratio = Data deduplication factor; 2.0 means half the physical space used                      │
│  Compression ratio = Data compression factor; reduces physical footprint of data                      │
│  Quota = Per-directory or per-user space limit; tracked in InsightIQ for trend                        │
│  Growth rate = MB/day or GB/week consumption rate; derived from time-series                           │
│  Linear regression = Statistical method for projecting capacity exhaustion date                       │
│  Projected full date = Estimated date cluster reaches capacity at current growth rate                 │
│  Custom horizon = User-defined forecast window (30/60/90/180 days)                                    │
│  CSV export = Downloading capacity data for external planning tools                                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Quota types in OneFS:

| Quota Type | Enforcement | Use Case |
|---|---|---|
| Hard Quota | Blocks writes when exceeded | Strict per-department limits |
| Soft Quota | Alerts but does not block | Advisory warnings |
| Advisory Quota | Reporting only | Visibility into usage trends |

## Common Capacity Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Capacity trending shows sudden jump | Large file ingest or restore | Correlate with job logs; check `/ifs/data` growth |
| InsightIQ data missing for date range | Collector was offline | Check InsightIQ appliance uptime and data collection logs |
| Quota reports not updating | Quota scanner job not running | Run `isi job jobs start QuotaScan` on PowerScale |
| Used capacity exceeds total | Snapshot space not accounted | Include snapshot usage in capacity calculations |
| Protocol breakdown unavailable | InsightIQ version does not support | Upgrade InsightIQ to v4.1+ for per-protocol views |
