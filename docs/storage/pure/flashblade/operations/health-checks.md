---
tags:
  - operations
  - pure
---
# FlashBlade — Health Checks


<div class="kb-summary">
Health Checks reference covering Daily Checks, Health Check, Array Health, Blade Health, Drive / Media Health and 4 more sections.

*Applies to: FlashBlade Purity//FB 4.x*
</div>



![FlashBlade — Health Checks — Diagram](../../../../assets/storage-pure-flashblade-operations-health-checks-diagram.svg)

> Part of the [FlashBlade Operations](index.md) reference.

---

```d2
direction: right

hub: "FlashBlade\nOperations" {shape: hexagon}
run_this_routine: "Run This Routine" {shape: rectangle}
daily_checks: "Daily Checks" {shape: rectangle}
health_check: "Health Check" {shape: rectangle}
array_health: "Array Health" {shape: rectangle}
blade_health: "Blade Health" {shape: rectangle}
drive_media_health: "Drive / Media Health" {shape: rectangle}

hub -> run_this_routine
hub -> daily_checks
hub -> health_check
hub -> array_health
hub -> blade_health
hub -> drive_media_health
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

1. **Blade health** — Pure1 or FlashBlade UI → Hardware — all blades and chassis components should be green
2. **File system health** — `pureds list --flagged` — should return empty for object store datasets
3. **Replication status** — `pureremote list` — all remote connections should show Connected
4. **Snapshot lag** — `purepgroup list --snap` — verify replication snapshots are within RPO
5. **Capacity** — FlashBlade UI → Storage → Capacity — check free space per file system and object store
6. **Client connectivity** — verify NFS/SMB/S3 clients are connecting successfully (check access logs)
7. **Phone home** — Pure1 → Settings → Phone Home — verify FlashBlade is reporting to Pure1
8. **Active alerts** — FlashBlade UI → Alerts — resolve all open alerts

## Daily Checks

![Daily Checks](../../../../assets/storage-pure-flashblade-hc-daily-checks.svg)

| Check | Command | Notes |
|---|---|---|
| [ ] Run `purefb alert list` | `purefb alert list` | review all active alerts; flag any hardware, capacity, or replication warnings |
| [ ] Run `purefb blade list` | `purefb blade list` | confirm all blades are in `healthy` state; flag any `failed` or `missing` blades |
| [ ] Run `purefb hardware list` | `purefb hardware list` | confirm all hardware components (power supplies, fans, fabric modules) are healthy |
| [ ] Run `purefb filesystem list` | `purefb filesystem list` | review filesystem utilization; flag any filesystem above 80% of provisioned limit |
| [ ] Run `purefb bucket list` | `purefb bucket list` | check S3 bucket count and data growth trends |
| [ ] Run `purefb replication list` | `purefb replication list` | confirm all ActiveDR links are in `active` status with lag within RPO |
| [ ] Check Pure1 portal for capacity growth forecasts, anomalies, and hardware alerts | | |

## Health Check

![Health Check](../../../../assets/storage-pure-flashblade-hc-health-check.svg)

- [ ] No active alerts in `purefb alert list`
- [ ] All blades are `healthy` — no `failed` or `missing` blades in `purefb blade list`
- [ ] All hardware components healthy — no PSU, fan, or FM (fabric module) failures
- [ ] No filesystems at or above provisioned limit — clients would receive ENOSPC errors
- [ ] All ActiveDR replication links are `active` and lag is within RPO
- [ ] All network interfaces are `up`: `purefb network interface list`
- [ ] Purity//FB version is within Pure's supported N-2 release window

```bash
# FlashBlade array status and Purity//FB version
purefb array list

# All blades and their health state
purefb blade list

# All hardware components (PSUs, fans, FMs) and status
purefb hardware list

# All filesystems with provisioned and used capacity
purefb filesystem list

# All S3 buckets and usage
purefb bucket list

# All active alerts
purefb alert list

# ActiveDR replication links and lag
purefb replication list

# All snapshots for filesystems and object store
purefb snap list

# Network interfaces and their operational state
purefb network interface list
```

## Array Health

![Array Health](../../../../assets/storage-pure-flashblade-hc-array-health.svg)

```bash
purefb array
purefb hardware
purefb alert list
```

Or via the FlashBlade GUI:
- **Overview → Array** — overall health summary
- **Storage → File Systems** / **Object Store** — capacity and status
- **Alerts → Active** — unacknowledged alerts

## Blade Health

![Blade Health](../../../../assets/storage-pure-flashblade-hc-blade-health.svg)

```bash
purefb blade list
```

All blades should show `status: healthy`. Any blade showing `unhealthy` or `failed` requires investigation.

## Drive / Media Health

![Drive / Media Health](../../../../assets/storage-pure-flashblade-hc-drive-media-health.svg)

FlashBlade uses direct-attached blade storage. Drive-level health is abstracted — monitor at the blade level:

```bash
purefb blade list --all
```

## Network Interface Health

![Network Interface Health](../../../../assets/storage-pure-flashblade-hc-network-interface-health.svg)

```bash
purefb network-interface list
```

All data VIPs should show `enabled: true` and `type: vip`.

## Replication Health

![Replication Health](../../../../assets/storage-pure-flashblade-hc-replication-health.svg)

```bash
purefb fs-replica-link list
purefb bucket-replica-link list
```

Verify replica links show `lag-time` within expected RPO.

## Pre-Change Checklist

- [ ] All blades `healthy`
- [ ] No active critical alerts
- [ ] All network VIPs enabled
- [ ] Replication healthy (lag within RPO)
- [ ] Capacity below 80%

## Health Summary Table

| Check | Command | Expected |
|---|---|---|
| Array health | `purefb array` | No warnings |
| Blades | `purefb blade list` | All healthy |
| Alerts | `purefb alert list` | No critical |
| Network | `purefb network-interface list` | All VIPs enabled |
| Replication | `purefb fs-replica-link list` | Low lag |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [FlashBlade — Procedures](procedures/)
- [FlashBlade — CLI Reference](cli-reference/)
- [FlashBlade — Common Issues](../troubleshooting/common-issues/)
