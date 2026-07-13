---
tags:
  - aria-operations
  - operations
  - vmware
description: "Performance Metrics Baseline reference covering Documenting the Baseline, Setting Thresholds from Baseline, Baseline Review Cadence."
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


```text title="Expected output"
Workload Latency Statistics (5 iterations, 5 second intervals):
Iteration 1: avg_latency=2.34ms, p95=4.12ms, p99=6.78ms, max=8.91ms
Iteration 2: avg_latency=2.41ms, p95=4.28ms, p99=7.02ms, max=9.15ms
Iteration 3: avg_latency=2.38ms, p95=4.19ms, p99=6.95ms, max=8.87ms
Iteration 4: avg_latency=2.45ms, p95=4.35ms, p99=7.11ms, max=9.23ms
Iteration 5: avg_latency=2.39ms, p95=4.22ms, p99=7.05ms, max=9.04ms

System Statistics:
Object: system
  total_ops: 1,247,856
  read_ops: 892,341
  write_ops: 355,515
  latency: 2.39ms
Timestamp: 2024-01-15T14:32:18Z
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `qos: command not found` | Verify the QoS monitoring module is installed and the service is running with `systemctl status aria-operations-qos`. |
    | `statistics: invalid object 'system'` | Confirm the correct object name using `statistics show -objects` and replace with a valid object like `datastore` or `host`. |
    | `Connection refused on localhost:8080` | Ensure the Aria Operations service is running and accessible by checking `curl -I http://localhost:8080/api/health`. |
**Pure FlashArray:**
```bash
purecli array get --mirrored
purecli volume list --performance    # per-volume latency, IOPS, BW
```

```d2
direction: right

documenting_the_baseline: "Documenting the Baseline" {shape: rectangle}
setting_thresholds_from_baseline: "Setting Thresholds from Baseline" {shape: rectangle}
baseline_review_cadence: "Baseline Review Cadence" {shape: rectangle}
verify: "Verify" {shape: rectangle}

documenting_the_baseline -> setting_thresholds_from_baseline
setting_thresholds_from_baseline -> baseline_review_cadence
baseline_review_cadence -> verify
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
- [Aria Operations — Architecture](../../architecture/)
- [Aria Operations — Deploy](../../deploy/)
- [Aria Operations — Security](../../security/)
- [Aria Operations — Troubleshooting](../../troubleshooting/)
