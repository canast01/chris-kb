# PowerMax Performance

Performance monitoring, analysis, and troubleshooting on Dell PowerMax.

## Quick Performance Check (SYMCLI)

```bash
# Storage Group I/O stats — snapshot
symstat -sid <sid> list -type sg

# Device-level stats — identify hot volumes
symstat -sid <sid> list -type dev | sort -k4 -rn | head -20   # sort by read IOPS

# Cache write pending — should stay below 31%
symstat -sid <sid> list -type cache | grep -E "WP|Write Pending"

# Front-end port utilisation
symstat -sid <sid> list -type port | grep -v "^$" | sort -k5 -rn | head -10
```

## Key Metrics and Thresholds

| Metric | Normal | Warning | Critical |
|---|---|---|---|
| Read Response Time | < 1 ms | 1–3 ms | > 3 ms |
| Write Response Time | < 1 ms | 1–3 ms | > 3 ms |
| Cache Write Pending % | < 15% | 15–30% | > 31% |
| SRP Subscription % | < 70% | 70–85% | > 85% |
| FA Port Utilisation % | < 50% | 50–70% | > 70% |
| BE Utilisation % | < 60% | 60–80% | > 80% |

## Continuous Monitoring

```bash
# Monitor SG stats every 30 seconds for 10 minutes
symstat -sid <sid> list -type sg -i 30 -c 20

# Monitor a specific device
symstat -sid <sid> list -type dev -devn <devname> -i 10 -c 30

# Monitor cache in real time
symstat -sid <sid> list -type cache -i 30
```

## Identify Performance Issues

```bash
# High latency investigation — find the busiest SGs
symstat -sid <sid> list -type sg | sort -k6 -rn | head -10   # sort by response time

# Back-end busy — check disk group saturation
symstat -sid <sid> list -type be | sort -k5 -rn | head -10

# SRDF impact — RDF director stats
symstat -sid <sid> list -type rdf

# Host sending too many IOPS — check IG → SG → device mapping
symaccess show view <view_name> -sid <sid>
```

## Unisphere for PowerMax Performance Dashboard

Unisphere provides 7-day rolling performance history:
- **System → Performance → Array** — overall throughput and latency
- **System → Performance → Storage Group** — per-SG response time, IOPS, MB/s
- **System → Performance → Port** — per-FA-port utilisation and I/O count
- **Alert Policies** — set thresholds to generate email/SNMP alerts

## Dell CloudIQ

CloudIQ provides longer-term performance trending (30+ days) and anomaly detection:
- Automatically collects metrics from connected PowerMax arrays
- Latency forecasting and proactive alerts
- Cross-array comparison and capacity planning
- Access via [cloudiq.dell.com](https://cloudiq.dell.com)

## Performance Data for TAC

```bash
# Collect 15-minute perf data for all subsystems
for type in sg dev dir be cache rdf port; do
    symstat -sid <sid> list -type $type -i 60 -c 15 > /tmp/powermax-${type}-perf-$(date +%Y%m%d).txt &
done
wait
tar czf /tmp/powermax-perf-$(date +%Y%m%d).tar.gz /tmp/powermax-*-perf-*.txt
```
