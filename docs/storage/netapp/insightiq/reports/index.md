---
tags:
  - netapp
---
# InsightIQ: Scheduled Reports, CSV Export, and SLA Reporting


<div class="kb-summary">
InsightIQ: Scheduled Reports, CSV Export, and SLA Reporting reference covering CSV Export for Analysis, SLA Reporting, Common Report Issues.
</div>

```text
┌───────────────────────────────────────── InsightIQ — Reports ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Built-in Reports               │  │             Scheduling & Export             │   │
│   │             Performance summary              │  │             Daily/weekly/monthly            │   │
│   │                Capacity trend                │  │                Email delivery               │   │
│   │              Top clients/shares              │  │                  PDF format                 │   │
│   │              Protocol breakdown              │  │                  CSV format                 │   │
│   │             Latency distribution             │  │              Custom time range              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Reports built in InsightIQ · PDF/CSV download · scheduled email via SMTP                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Performance summary = Cluster IOPS, latency, throughput over selected time window                    │
│  Capacity trend = Space usage over time with growth rate and projected full date                      │
│  Top clients = Ranked list of clients by IO volume; useful for chargeback                             │
│  Top shares = Ranked NFS/SMB shares by IO; identify active workloads                                  │
│  Protocol breakdown = IO split by NFS v3, NFS v4, SMB, S3, HDFS                                       │
│  Latency distribution = Histogram of operation latencies; shows p50/p95/p99                           │
│  Scheduled email = InsightIQ sending report to recipient list on configured cadence                   │
│  Custom time range = User-defined start and end dates for report data window                          │
│  Chargeback = Using top-client IO data to attribute storage cost to teams                             │
│  PDF = Formatted document; suitable for management review or compliance audit                         │
│  CSV = Raw metric data for import into BI tools or spreadsheets                                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Typical SLA thresholds for NAS workloads:

| Workload Type | Latency SLA | Throughput SLA |
|---|---|---|
| VMware NFS datastores | < 5 ms average | > 1 GB/s per cluster |
| Home directories (SMB) | < 20 ms average | > 500 MB/s |
| Analytics (HDFS) | < 100 ms average | > 5 GB/s |
| Archive (cold NFS) | < 200 ms | Best effort |

## Common Report Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Scheduled report not delivered | SMTP not configured or email bounced | Verify SMTP settings under InsightIQ admin settings |
| CSV shows all zeros | Data collection gap during report period | Check InsightIQ collector status and connectivity |
| Report takes too long to generate | Large time range at 5-min granularity | Use daily granularity for periods > 30 days |
| Graphs in PDF are blurry | Low DPI PDF export setting | Not configurable in current InsightIQ versions; use CSV |
| Cluster not available in report dropdown | Cluster not registered in InsightIQ | Add cluster under InsightIQ > Clusters > Add |
