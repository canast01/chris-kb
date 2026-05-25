# InsightIQ: Capacity Trending, Protocol Breakdown, and Quota Monitoring

```text
Capacity — InsightIQ
Used ▲
     │                              ╭──── projected full
     │                    ╭─────────╯
     │           ╭────────╯
     │  ╭────────╯
     │  │  volume usage vs quota
     └──┼──────────────────────────────────────► time
       now       +30d       +60d          +90d

┌──────────────────────────────────────────────┐
│  Quota Monitoring                            │
│  /ifs/dept/finance  ████████████░  82%  ⚠   │
│  /ifs/dept/ops      ████████░░░░░  55%       │
│  /ifs/dept/archive  █████░░░░░░░░  38%       │
│  Cluster total      ████████████░  83%  ⚠   │
└──────────────────────────────────────────────┘
```

Dell InsightIQ (now part of the OneFS Analytics suite) provides capacity analytics for PowerScale (Isilon) clusters. This page covers how to monitor capacity trends, break down usage by protocol, and manage quota monitoring.

## Capacity Overview

InsightIQ collects capacity metrics from all nodes in a PowerScale cluster via the OneFS platform APIs. Data is stored locally on the InsightIQ virtual appliance.

Navigation: **InsightIQ > Reports > Capacity**

Key capacity metrics:

| Metric | Description |
|---|---|
| Cluster Used Capacity | Total bytes written across all nodes |
| Cluster Total Capacity | Raw usable capacity after protection overhead |
| Hard Quota Used | Data written under hard quota limits |
| Soft Quota Used | Data approaching soft quota warning thresholds |
| Data Reduction Savings | Dedupe and compression savings (if enabled) |

## Capacity Trending Reports

```bash
# On the InsightIQ appliance (SSH access)
ssh admin@insightiq.example.com

# List available cluster targets
isi_gather_info --list-clusters   # Not available directly; use InsightIQ UI

# On PowerScale OneFS directly - check used vs available capacity
ssh admin@powerscale.example.com
isi statistics query list --stats ifs.bytes.avail,ifs.bytes.total,ifs.bytes.used

# Check capacity in human-readable format
isi storagepool list
```

InsightIQ capacity report settings:

| Setting | Description |
|---|---|
| Granularity | 5 min, 1 hour, 1 day |
| Look-back Period | Up to 365 days (depends on InsightIQ retention) |
| Node Breakdown | Per-node or cluster aggregate |
| Protocol Filter | NFS, SMB, HDFS, S3 |

## Protocol-Level Capacity Breakdown

InsightIQ can show which protocol (NFS, SMB, HDFS, S3) is consuming the most capacity growth over time. This is useful for chargeback and planning.

```bash
# On PowerScale: check per-protocol throughput to correlate with capacity
ssh admin@powerscale.example.com

# Check NFS exports and their sizes
isi nfs exports list

# Check SMB shares
isi smb shares list

# Check directory sizes for top-level paths
isi get -d /ifs/data --numeric
du -sh /ifs/data/* 2>/dev/null | sort -rh | head -20
```

Protocol utilisation breakdown reference:

| Protocol | Typical Use Case | Growth Pattern |
|---|---|---|
| NFS | Linux workloads, VMware datastores | Steady growth |
| SMB | Windows home drives, departmental shares | Burst during business hours |
| HDFS | Analytics clusters (Hadoop/Spark) | Large batch ingest |
| S3 | Object storage for cloud-native apps | Rapid unpredictable growth |

## Quota Monitoring

PowerScale quotas can be monitored through InsightIQ or directly via the OneFS CLI.

```bash
# List all quotas and their usage on PowerScale
ssh admin@powerscale.example.com
isi quota quotas list --long

# Show quotas approaching threshold (>80% used)
isi quota quotas list --format csv | awk -F',' 'NR>1 && ($5/$4) > 0.8 {print $1, $3, $4, $5}'

# Get quota report
isi quota reports list
isi quota reports view --id <reportId>
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
