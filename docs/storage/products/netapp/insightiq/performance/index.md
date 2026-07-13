---
tags:
  - netapp
description: "InsightIQ: Throughput, Latency, IOPS, and Protocol Performance Dashboards reference covering Protocol Performance Breakdown, Identifying Performance..."
---
# InsightIQ: Throughput, Latency, IOPS, and Protocol Performance Dashboards

<div class="kb-summary">
InsightIQ: Throughput, Latency, IOPS, and Protocol Performance Dashboards reference covering Protocol Performance Breakdown, Identifying Performance Bottlenecks via InsightIQ, Collecting a OneFS Performance Support Bundle, Common Performance Issues.

*Applies to: InsightIQ*
</div>

```d2
direction: down

common_performance_issues: "Common Performance Issues" {shape: rectangle}

```

## Common Performance Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Latency spike during business hours | Client burst exceeding cache | Tune prefetch settings; review client I/O pattern |
| Low throughput despite spare capacity | Single-node bottleneck | Rebalance client connections via SmartConnect |
| Cache hit rate dropping | Working set growth exceeds L2 cache | Review tiering policy; consider adding SSD nodes |
| SMB latency high, NFS fine | SMB signing overhead | Disable SMB signing for trusted internal clients if policy permits |
| InsightIQ graphs show gaps | Collector disconnected from cluster | Check InsightIQ to OneFS API connectivity |
