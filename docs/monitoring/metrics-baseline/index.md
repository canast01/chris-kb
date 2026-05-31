# Performance Metrics Baseline

```text
┌──────────────────────────────────── Monitoring — Metrics Baseline ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Metrics Baseline — Documenting Normal Ranges to Drive Accurate Alert Thresholds        │   │
│   │        Key metrics: CPU util · memory util · storage IOPS/latency · network throughput        │   │
│   │           Baseline period: 4-week rolling window captures daily and weekly patterns           │   │
│   │       Methods: percentile banding (p50/p95/p99) · seasonal adjustment · learned anomaly       │   │
│   │        Output: documented threshold table per object type used in all monitoring tools        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    A stale baseline creates false positives or misses real anomalies — review quarterly               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Compute Metrics       │  │       Storage Metrics       │  │       Network Metrics       │   │
│   │      CPU util: warn 80%     │  │      IOPS: warn 70% max     │  │       Throughput: 70%       │   │
│   │      Mem util: warn 85%     │  │      Latency: warn 2ms      │  │      Error rate: <0.01%     │   │
│   │      CPU ready: warn 5%     │  │      Cap: warn 75% full     │  │      Drops: warn >10/s      │   │
│   │       Co-stop: warn 3%      │  │      Queue depth: warn      │  │        RTT: warn >5ms       │   │
│   │      Swap: crit >0 MB/s     │  │      Rebuild time: 4hr      │  │        CRC errors: 0        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Baseline data sourced from: Aria Operations · CloudIQ · Pure1 · NDI — reviewed quarterly             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Baseline          = Statistical representation of normal operating behaviour over a time window      │
│  p50               = 50th percentile (median); typical operating value                                │
│  p95               = 95th percentile; near-peak value; used for warn threshold                        │
│  p99               = 99th percentile; extreme peak; used for critical threshold                       │
│  CPU ready         = Time a VM waits for a physical CPU; >5% indicates contention                     │
│  Co-stop           = SMP VM waiting for all vCPUs; >3% indicates over-provisioned vCPUs               │
│  Memory balloon    = VMware reclamation driver; active ballooning indicates memory pressure           │
│  Seasonal adjust   = Accounting for day-of-week or time-of-day patterns in thresholds                 │
│  Queue depth       = Number of outstanding I/O requests; elevated = storage saturation                │
│  Learned anomaly   = ML-derived deviation from historical pattern rather than static threshold        │
│  Threshold table   = Reference document listing warn/crit values per metric per object type           │
│  False positive    = Alert firing when conditions are actually normal; caused by stale baseline       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Linux — disk latency:**
```bash
iostat -xz 5 6   # extended stats, 5 sec interval, 6 samples
# key fields: await (avg I/O wait ms), r_await, w_await, util%
```

**Windows — performance counters:**
```powershell
# CPU
Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 5 -MaxSamples 12

# Memory available
Get-Counter '\Memory\Available MBytes' -SampleInterval 5 -MaxSamples 12

# Disk latency
Get-Counter '\PhysicalDisk(*)\Avg. Disk sec/Read','\PhysicalDisk(*)\Avg. Disk sec/Write' -SampleInterval 5 -MaxSamples 12
```

**NetApp ONTAP — workload stats:**
```bash
qos statistics workload latency show -iterations 5 -interval 5
statistics show -object system -counter total_ops,read_ops,write_ops,latency
```

**Pure FlashArray:**
```bash
purecli array get --mirrored
purecli volume list --performance    # per-volume latency, IOPS, BW
```

## Documenting the Baseline

Record for each system / service:

```text
System:          app-db01
Date captured:   YYYY-MM-DD
Period:          Mon–Fri business hours, 4 weeks

CPU avg:         22%   | peak: 68% (month-end batch)
Memory avg:      71%   | peak: 84%
Disk read lat:   0.8ms | peak: 3ms
Disk write lat:  1.2ms | peak: 5ms
IOPS avg:        3,200 | peak: 12,000
Network (eth0):  120 Mbps avg | 450 Mbps peak
```

## Setting Thresholds from Baseline

Recommended starting point:
- **Warning**: avg + (2 × std deviation), or >75% of peak
- **Critical**: avg + (3 × std deviation), or >90% of peak

Avoid static thresholds that ignore daily/weekly patterns — use dynamic baselines in tools like vROps, Zabbix, or Datadog where available.

## Baseline Review Cadence

| Trigger | Action |
|---|---|
| Quarterly | Review and update baselines for all production systems |
| After major change (hardware refresh, app version) | Re-capture within 2 weeks |
| After sustained alert activity | Investigate: real anomaly or stale baseline |
