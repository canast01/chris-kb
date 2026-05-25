# Performance Baselining

A documented performance baseline defines normal system behaviour, enabling accurate anomaly detection and meaningful alert thresholds.

> See also: [Metrics Baseline](../../monitoring/metrics-baseline/index.md) — similar coverage from the monitoring perspective.

```text
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐   ┌─────────────────┐
│ Collect Metrics  │   │ Establish Normal │   │  Store Baseline  │   │ Compare Current │
│                  │   │                  │   │                  │   │  vs Baseline    │
│ CPU / Mem / Disk │   │ avg + peak + σ   │   │ Time-series DB   │   │                 │
│ Net / App / DB   │──►│ per time window  │──►│ or documented    │──►│ Deviation > 2σ  │
│ (30-day minimum) │   │ (biz hrs vs off) │   │ baseline record  │   │ → alert / review│
└──────────────────┘   └──────────────────┘   └──────────────────┘   └─────────────────┘
                                                        │                      │
                                               ┌────────┘          ┌───────────┘
                                               ▼                   ▼
                                     ┌──────────────────┐  ┌──────────────────┐
                                     │  Review Triggers │  │  Set Thresholds  │
                                     │  (HW refresh /   │  │  Warning / Crit  │
                                     │   app upgrade)   │  │  from baseline   │
                                     └──────────────────┘  └──────────────────┘
```

## What to Baseline

| Resource | Metrics to Capture |
|---|---|
| CPU | Avg utilisation (business hours vs off-hours), peak, standard deviation |
| Memory | Avg used, peak, swap usage |
| Disk I/O | Read/write IOPS, throughput (MB/s), avg latency (ms), peak |
| Network | Interface avg utilisation, peak throughput |
| Application | Request rate, response time (P50/P95/P99), error rate |
| Database | QPS, avg query latency, connection count |

## Collection Period

- Minimum: **2 weeks** (covers Mon–Fri patterns and weekend)
- Recommended: **30 days** (captures month-end peaks)
- For seasonal systems: **90 days** minimum

## Linux — Baseline Collection

```bash
# CPU — 30 days from sar
# For each day's summary:
for d in $(seq 1 30); do
    sar -u -f /var/log/sa/sa$(date -d "$d days ago" +%d) 2>/dev/null | \
      awk '/Average/ {print $3}'
done | awk '{sum+=$1; n++} END {printf "CPU 30d avg: %.1f%%\n", sum/n}'

# Disk I/O — per device
iostat -x 5 12 > /tmp/iostat-baseline.txt
# Key fields: await (ms), r_await, w_await, util%

# Memory
free -m
vmstat -S M 5 12
```

## Windows — Baseline Collection

```powershell
# Capture 5-minute samples for 1 hour
$counters = @(
    '\Processor(_Total)\% Processor Time',
    '\Memory\Available MBytes',
    '\PhysicalDisk(*)\Avg. Disk sec/Read',
    '\PhysicalDisk(*)\Avg. Disk sec/Write',
    '\Network Interface(*)\Bytes Total/sec'
)
Get-Counter -Counter $counters -SampleInterval 300 -MaxSamples 12 |
  Export-Counter -Path C:\baseline\$(Get-Date -Format yyyyMMdd).blg
```

## Application Performance Baseline

```bash
# Apache/nginx access log — requests per minute and response time
awk '{print $10, $NF}' /var/log/nginx/access.log | \
  awk '{sum+=$1; count++} END {print "Avg response:", sum/count "ms; Total:", count "requests"}'

# Database — PostgreSQL slow query analysis
psql -c "SELECT query, mean_exec_time, calls FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 20;"
```

## Documenting the Baseline

```yaml
System:         web-prod-01
Date:           2026-05-06
Period:         30 days (Mon–Fri 08:00–18:00 business hours)

CPU:            avg 28% | peak 74% | std dev ±12%
Memory:         avg 61% | peak 82%
Disk reads:     avg 1.2ms | peak 8ms
Disk writes:    avg 2.1ms | peak 15ms
IOPS:           avg 4,200 | peak 18,000
Network (eth0): avg 180 Mbps | peak 620 Mbps

App requests:   avg 340 req/min | peak 1,200
Response (P95): avg 85ms | peak 340ms
Error rate:     avg 0.02%
```

## Setting Thresholds from Baseline

| Metric | Warning | Critical |
|---|---|---|
| CPU | avg + 2σ or >75% sustained | >90% sustained |
| Memory | >85% | >95% |
| Disk latency | >3× baseline avg | >10× baseline avg |
| Response time P95 | >2× baseline | >5× baseline |

## Baseline Review Triggers

- After hardware refresh or VM resize
- After major application upgrade
- After sustained alert activity (anomaly or stale baseline?)
- Quarterly routine review
