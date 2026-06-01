# InsightIQ: Throughput, Latency, IOPS, and Protocol Performance Dashboards


<div class="kb-summary">
InsightIQ: Throughput, Latency, IOPS, and Protocol Performance Dashboards reference covering Protocol Performance Breakdown, Identifying Performance Bottlenecks via InsightIQ, Collecting a OneFS Performance Support Bundle, Common Performance Issues.
</div>

```text
┌────────────────────────────────── InsightIQ — Performance Analysis ───────────────────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        IOPS Analysis        │  │       Latency Analysis      │  │          Throughput         │   │
│   │        Per-node IOPS        │  │       Per-protocol lat      │  │        MB/s per node        │   │
│   │      Per-protocol IOPS      │  │         p50/p95/p99         │  │       Network vs disk       │   │
│   │        Read vs write        │  │       Backend vs front      │  │         Peak vs avg         │   │
│   │       Peak vs average       │  │        Trend baseline       │  │       Saturation point      │   │
│   │       Client breakdown      │  │         Cache impact        │  │         Protocol mix        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Metrics from PowerScale nodes · InsightIQ aggregates to cluster and node level                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  p50 latency = Median latency; 50% of operations complete faster than this value                      │
│  p95 latency = 95th percentile latency; 5% of operations are slower; good SLA metric                  │
│  p99 latency = 99th percentile; shows tail latency impacting worst-case user experience               │
│  Frontend latency = Client-to-cluster latency including network and protocol overhead                 │
│  Backend latency = Cluster-to-disk latency; excludes network; shows storage device health             │
│  Cache impact = Reduction in backend IOPS due to read cache (L1 RAM, L2 SSD hits)                     │
│  Saturation point = Throughput level at which latency begins degrading non-linearly                   │
│  Protocol mix = Ratio of NFS/SMB/S3/HDFS IO; different protocols have different overheads             │
│  Trend baseline = Historical average used to identify current deviations                              │
│  Network vs disk = Comparing frontend and backend throughput to find bottleneck tier                  │
│  Read vs write = IO breakdown critical for cache effectiveness and drive wear planning                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Identifying Performance Bottlenecks via InsightIQ

InsightIQ can generate a **Breakout Report** that overlays multiple metrics for the same time range to help identify correlation.

Report path: **InsightIQ > Reports > Performance > Breakout Report**

| Overlay Combination | What to Look For |
|---|---|
| Throughput + CPU | High CPU at throughput ceiling = CPU bottleneck |
| Latency + Cache Hit Rate | High latency + low cache hit = working set too large |
| Throughput + Disk I/O | Throughput matching disk limit = spinning disk bottleneck |
| Latency + Network Errors | Latency spike + errors = network instability |

## Collecting a OneFS Performance Support Bundle

```bash
# Gather a stats snapshot for a support case
ssh admin@powerscale.example.com

# Run the gather script (sends to Dell support or saves locally)
isi_gather_info

# For a targeted performance capture (5 minutes of 30s samples)
isi statistics query list \
  --stats cpu.user.avg,disk.xfer.bytes.rate,net.iface.bytes.in.rate,ifs.ops.read.avg,ifs.ops.write.avg \
  --interval 30 --duration 300
```

## Common Performance Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Latency spike during business hours | Client burst exceeding cache | Tune prefetch settings; review client I/O pattern |
| Low throughput despite spare capacity | Single-node bottleneck | Rebalance client connections via SmartConnect |
| Cache hit rate dropping | Working set growth exceeds L2 cache | Review tiering policy; consider adding SSD nodes |
| SMB latency high, NFS fine | SMB signing overhead | Disable SMB signing for trusted internal clients if policy permits |
| InsightIQ graphs show gaps | Collector disconnected from cluster | Check InsightIQ to OneFS API connectivity |
