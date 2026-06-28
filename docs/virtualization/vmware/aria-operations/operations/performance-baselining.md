---
tags:
  - aria-operations
  - operations
  - vmware
---
# Performance — Baselining

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

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier

## See also

- [Alert Management](alert-management.md)
- [Aria Operations: Alert Definitions and Policies](alerts.md)
- [Aria Operations Backup & Restore](backup-restore.md)
- [Aria Operations — Operations](index.md)
- [Aria Operations — Architecture](../architecture/)
- [Aria Operations — Deploy](../deploy/)
- [Aria Operations — Security](../security/)
- [Aria Operations — Troubleshooting](../troubleshooting/)
