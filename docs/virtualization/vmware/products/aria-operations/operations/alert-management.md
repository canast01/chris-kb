---
tags:
  - aria-operations
  - operations
  - vmware
description: "Alert Management reference covering Common Alert Sources, Alert Noise Reduction Checklist, Escalation Matrix (template)."
---
# Alert Management

<div class="kb-summary">
Alert Management reference covering Common Alert Sources, Alert Noise Reduction Checklist, Escalation Matrix (template).

*Applies to: Aria Ops 8.x*
</div>

```d2
direction: right

custom_alert_thresholds: "Custom Alert Thresholds" {shape: rectangle}
alert_noise_reduction_checklist: "Alert Noise Reduction Checklist" {shape: rectangle}
escalation_matrix_template: "Escalation Matrix (template)" {shape: rectangle}
verify: "Verify" {shape: rectangle}

custom_alert_thresholds -> alert_noise_reduction_checklist
alert_noise_reduction_checklist -> escalation_matrix_template
escalation_matrix_template -> verify
```

## Custom Alert Thresholds

### Disk Space

```bash
df -h | awk '$5+0 > 75'       # filesystems over 75%
du -sh /var/* | sort -rh | head -10
```


```text title="Expected output"
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   39G  8.5G  80% /
/dev/sdb1       100G   82G   15G  83% /var
tmpfs            16G   13G  3.2G  82% /dev/shm

4.2G	/var/log
2.8G	/var/lib
1.9G	/var/cache
1.2G	/var/spool
680M	/var/tmp
420M	/var/crash
310M	/var/lock
180M	/var/run
95M	/var/mail
42M	/var/opt
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `awk: syntax error in pattern near line 1` | Ensure the awk syntax is correct; use `awk '$5+0 > 75 {print}'` if the pattern alone doesn't work on your awk version. |
    | `cannot access '/var/*': Permission denied` | Run the `du` command with `sudo` to access all directories under /var with restricted permissions. |
### Storage Latency (ONTAP)

```bash
statistics show -object volume -counter read_latency,write_latency -interval 5
qos statistics workload latency show
```


```text title="Expected output"
Volume Read Latency (ms)  Write Latency (ms)  Timestamp
/vol/data01               2.34                1.87                2024-01-15 14:23:45
/vol/data02               3.12                2.56                2024-01-15 14:23:50
/vol/logs                 1.89                1.45                2024-01-15 14:23:55
/vol/backup               4.67                3.92                2024-01-15 14:24:00
/vol/archive              2.11                1.73                2024-01-15 14:24:05

Workload Latency Statistics:
Workload Name             P50 (ms)  P95 (ms)  P99 (ms)  Max (ms)
production-db             1.2       3.4       5.1       12.3
analytics-batch           2.8       6.7       9.2       18.5
backup-job                3.5       7.1       10.2      22.1
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `statistics: command not found` | Verify you are connected to the Aria Operations cluster and have the correct CLI context loaded. |
    | `Error: Invalid counter name 'read_latency'` | Use `statistics show -object volume -help` to list valid counter names for your environment. |
### Network Interface Errors

```bash
# Linux
ip -s link show <interface>
ethtool -S <interface> | grep -i error

# Cisco NX-OS
show interface <int> counters errors
```


```text title="Expected output"
# Linux output for ip -s link show eth0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
    link/ether 00:50:56:c0:00:08 brd ff:ff:ff:ff:ff:ff
    RX: bytes  packets  errors  dropped overrun mcast
        2847361024 1924156 12 0 0 18432
    TX: bytes  packets  errors  dropped carrier collsns
        1563847291 1847392 0 0 0 0

# Linux output for ethtool -S eth0 | grep -i error
     rx_errors: 12
     rx_crc_errors: 8
     rx_frame_errors: 4
     tx_errors: 0
     tx_carrier_errors: 0

# Cisco NX-OS output for show interface Ethernet1/1 counters errors
Ethernet1/1
  Errors:
    Input Errors:  0
    CRC errors:    0
    Runts:         0
    Giants:        0
    Output Errors: 0
    Collisions:    0
    Late Collisions: 0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Device "eth0" does not exist.` | Verify the interface name with `ip link show` and use the correct interface identifier. |
    | `Cannot get device settings: No such device` | Ensure the interface is present and not disabled; check with `ethtool <interface>` to confirm device exists. |
## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Alert Noise Reduction Checklist

- [ ] Are thresholds based on documented baselines?
- [ ] Are there duplicate alerts from multiple tools for the same condition?
- [ ] Are acknowledged-but-not-resolved alerts being tracked?
- [ ] Are low-severity alerts reviewed at least weekly, not just critical ones?
- [ ] Are any suppressions older than 30 days without a ticket?

## Escalation Matrix (template)

| Tier | On-call | Escalate After |
|---|---|---|
| L1 | Infra on-call | 30 min no progress |
| L2 | Platform / storage team | 1 hour on Critical |
| L3 | Vendor TAC / architect | 2 hours on Critical |

---

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier

## See also

- [Aria Operations: Alert Definitions and Policies](alerts.md)
- [Aria Operations Backup & Restore](backup-restore.md)
- [Capacity Forecasting](capacity-forecasting.md)
- [Aria Operations — Operations](index.md)
- [Aria Operations — Architecture](../../architecture/)
- [Aria Operations — Deploy](../../deploy/)
- [Aria Operations — Security](../../security/)
- [Aria Operations — Troubleshooting](../../troubleshooting/)
