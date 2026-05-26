# InsightIQ: Capacity Trending, Protocol Breakdown, and Quota Monitoring

```
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
