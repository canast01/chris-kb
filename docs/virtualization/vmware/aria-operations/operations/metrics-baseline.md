---
tags:
  - aria-operations
  - operations
  - vmware
---
# Performance Metrics Baseline

<div class="kb-summary">
Performance Metrics Baseline reference covering Documenting the Baseline, Setting Thresholds from Baseline, Baseline Review Cadence.

*Applies to: Aria Ops 8.x*
</div>

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

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

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
