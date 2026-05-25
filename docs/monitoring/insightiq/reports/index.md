# InsightIQ: Scheduled Reports, CSV Export, and SLA Reporting

```text
Scheduled Reports — InsightIQ
┌─────────────────────────────────────────┐
│  Report template configured             │
│  (capacity / performance / quota)       │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│  Schedule: weekly  │  format: PDF/CSV   │
│  cluster: ps-cluster1  │  granularity: 1h│
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│  Report generated (InsightIQ appliance) │
└──────────┬──────────────────────────────┘
           │
    ┌──────┴──────────┐
    ▼                 ▼
┌────────┐      ┌──────────┐
│ Email  │      │ Download │
│ distro │      │  (CSV    │
│  list  │      │  / PDF)  │
└────────┘      └──────────┘
```

Dell InsightIQ provides a built-in reporting engine for PowerScale performance and capacity data. Reports can be scheduled for recurring delivery, exported as CSV for further analysis, or used to measure SLA compliance.

## Report Types in InsightIQ

Navigation: **InsightIQ > Reports**

| Report Category | Available Reports |
|---|---|
| Performance | Throughput, latency, IOPS, protocol breakdown |
| Capacity | Used vs available, growth trend, per-directory |
| Clients | Top talkers, per-client throughput and latency |
| Quota | Usage vs limits, approaching thresholds |
| Deduplication | Savings summary, dedupe job history |
| Cluster Summary | Combined health and performance overview |

## Scheduling a Report

InsightIQ allows reports to be scheduled at daily, weekly, or monthly intervals.

Navigation: **InsightIQ > Reports > [Report Type] > Schedule**

Configuration options:

| Field | Description |
|---|---|
| Report Name | Descriptive label for the scheduled job |
| Cluster | Select which PowerScale cluster to report on |
| Time Range | Rolling: Last 7 days, Last 30 days, etc. |
| Granularity | 5-minute, hourly, or daily data points |
| Format | PDF or CSV |
| Email Recipients | Comma-separated addresses |
| Schedule | Daily at HH:MM, Weekly, Monthly |

```bash
# InsightIQ runs as a virtual appliance — schedule management via the web UI
# Access the InsightIQ admin interface
curl -sk -X GET "https://insightiq.example.com/api/json/v2/reports" \
  -u "admin:password" \
  -H "Accept: application/json" | jq '.reports[].name'

# Trigger an on-demand report generation via API
curl -sk -X POST "https://insightiq.example.com/api/json/v2/reports/generate" \
  -u "admin:password" \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "performance_summary",
    "cluster": "powerscale-cluster1",
    "start_time": "2026-04-01T00:00:00",
    "end_time": "2026-04-30T23:59:59",
    "granularity": "1h"
  }'
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
