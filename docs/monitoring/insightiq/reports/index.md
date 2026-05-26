# InsightIQ: Scheduled Reports, CSV Export, and SLA Reporting

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

## CSV Export for Analysis

CSV exports are useful for importing into Excel, building Power BI dashboards, or correlating with application-level metrics.

```bash
# Download a CSV performance report from InsightIQ
curl -sk -X GET \
  "https://insightiq.example.com/api/json/v2/reports/<reportId>/export?format=csv" \
  -u "admin:password" \
  -o insightiq-performance.csv

# Parse CSV to find peak throughput days
awk -F',' 'NR>1 {print $1, $3+$4}' insightiq-performance.csv | sort -k2 -rn | head -10
```

CSV column structure (performance reports):

| Column | Content |
|---|---|
| timestamp | ISO 8601 datetime |
| node | Node name or "cluster" for aggregate |
| read_bytes_s | Read throughput in bytes/sec |
| write_bytes_s | Write throughput in bytes/sec |
| latency_ms | Average round-trip latency in milliseconds |
| ops_s | Operations per second |

## SLA Reporting

InsightIQ is commonly used to verify latency and availability SLAs for NAS workloads.

```bash
# On PowerScale: calculate average latency for a time window
ssh admin@powerscale.example.com

# Check average NFS latency (in microseconds) for last hour
isi statistics protocol list --protocol=nfs \
  --stats op_latency_ave --format table
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
