---
tags:
  - dell
  - operations
---
# Unity — Health Checks

<div class="kb-summary">
Daily and pre/post-change health checks for Dell Unity storage systems.

*Applies to: Unity XT*
</div>

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

1. **System health:** `uemcli /sys/general show` — check Health field
2. **Hardware status:** `uemcli /sys/component/disk show` — all disks Enabled
3. **Pool health:** `uemcli /stor/config/pool show` — check Health, free capacity
4. **SP (Storage Processor) status:** `uemcli /sys/component/sp show`
5. **LUN and filesystem health:** `uemcli /stor/prov/luns/lun show | grep -i health`
6. **Active alerts:** `uemcli /event/alert/hist show -filter "state eq active"` — investigate open alerts
7. **Fan and power:** `uemcli /sys/component/fan show` and `uemcli /sys/component/psu show`

## Daily Checks

![Daily Checks](../../../../assets/storage-dell-unity-hc-daily-checks.svg)

| Check | Command | Notes |
|---|---|---|
| [ ] Run `uemcli /env/health show -filter "health.value ne OK"` | `uemcli /env/health show -filter "health.value ne OK"` | any non-OK result requires immediate investigation before proceeding with other work |
| [ ] Check active alerts | `uemcli /sys/alert show` | triage by severity; acknowledge alerts that have been resolved to keep the alert list clean |
| [ ] Check pool capacity | `uemcli /stor/pool show -detail` | alert if any pool is above 80% consumed or over-subscribed |
| [ ] Verify both SPs are Active | `uemcli /env/sp show` | SP A and SP B should both report `Active`; a single SP active indicates a failover has occurred |
| [ ] Check replication sessions | `uemcli /rep/session show` | all sessions should show `Active` state; investigate any session in `Error`, `Paused`, or `Interrupted` state |
| [ ] Check disk health | `uemcli /stor/disk show` | confirm no disks in `Faulted` or `Degraded` state |
| [ ] Review snapshot capacity consumption | `uemcli /stor/snap show` | confirm snapshots are not consuming unexpected pool space |
| [ ] Review Unisphere Dashboard for any threshold warnings or capacity |  |  |

## Health Check

![Health Check](../../../../assets/storage-dell-unity-hc-health-check.svg)

Run these checks before any planned change or as first-response steps when investigating a reported issue.

- [ ] `uemcli /env/health show -filter "health.value ne OK"` returns no output — all components healthy
- [ ] `uemcli /env/sp show` — both SP A and SP B are `Active` with no faults
- [ ] `uemcli /stor/pool show -detail` — all pools below 80% consumed; FAST Cache status is Enabled if configured
- [ ] `uemcli /sys/alert show` — no unacknowledged alerts of severity `ERROR` or `CRITICAL`
- [ ] `uemcli /rep/session show` — all replication sessions in `Active` state
- [ ] `uemcli /stor/disk show` — no faulted or degraded disks
- [ ] `uemcli /stor/snap show` — no snapshot schedule failures; snapshot count not approaching pool capacity limits
- [ ] `uemcli /sys/sw show` — current software version noted; no pending updates flagged as critical

```bash
# Show all components not in an OK health state
uemcli /env/health show -filter "health.value ne OK"

# Show both SP health and current state
uemcli /env/sp show

# Show detailed pool capacity, health, and FAST Cache status
uemcli /stor/pool show -detail

# Show all active system alerts
uemcli /sys/alert show

# Show all replication sessions and their current state
uemcli /rep/session show

# Show all disks and their health state
uemcli /stor/disk show

# Show all snapshots and their pool consumption
uemcli /stor/snap show

# Show installed software version and any pending upgrades
uemcli /sys/sw show

# Show all LUNs with pool assignment and capacity
uemcli /store/lun show
```

## System Status Commands

![System Status Commands](../../../../assets/storage-dell-unity-hc-system-status-commands.svg)

```bash
# System general info and health
uemcli -d <ip> -u admin /sys/general show -detail

# Software version
uemcli -d <ip> -u admin /sys/sw/version show

# Storage processor status
uemcli -d <ip> -u admin /sys/sp show
uemcli -d <ip> -u admin /sys/sp show -detail | grep -E "Health|State|Model"
```

## Alerts and Events

![Alerts and Events](../../../../assets/storage-dell-unity-hc-alerts-and-events.svg)

```bash
# Active alerts — any critical alerts require immediate attention
uemcli -d <ip> -u admin /prac/alert show
uemcli -d <ip> -u admin /prac/alert show | grep -i "Critical\|Error"

# Event log
uemcli -d <ip> -u admin /event/syslog show
```

## Hardware

![Hardware](../../../../assets/storage-dell-unity-hc-hardware.svg)

```bash
# Disk health
uemcli -d <ip> -u admin /stor/config/disk show
uemcli -d <ip> -u admin /stor/config/disk show | grep -v "Normal"   # Flag non-normal disks

# Disk groups
uemcli -d <ip> -u admin /stor/config/dg show -detail | grep -E "Health|RAID|Disks"

# Storage processors
uemcli -d <ip> -u admin /sys/sp show -detail | grep -E "Health|Power|Temp"
```

## Storage Pool Capacity

![Storage Pool Capacity](../../../../assets/storage-dell-unity-hc-storage-pool-capacity.svg)

```bash
# Pool list with capacity and health
uemcli -d <ip> -u admin /stor/config/pool show -detail

# Flag pools above 80% used
uemcli -d <ip> -u admin /stor/config/pool show | awk '
    /Free/ { getline; if ($3 + 0 < 20) print "WARNING: Pool near full:", $0 }'
```

## LUN Status

![LUN Status](../../../../assets/storage-dell-unity-hc-lun-status.svg)

```bash
# All LUNs and health
uemcli -d <ip> -u admin /stor/config/lun show -detail | grep -E "Name|Health|Size"

# LUNs with non-OK health
uemcli -d <ip> -u admin /stor/config/lun show | grep -v "OK\|Name"
```

## Replication Sessions

![Replication Sessions](../../../../assets/storage-dell-unity-hc-replication-sessions.svg)

```bash
# All replication sessions
uemcli -d <ip> -u admin /prot/rep/session show

# Sessions not in OK state
uemcli -d <ip> -u admin /prot/rep/session show | grep -v "OK\|Session ID"
```

## Network Interfaces

![Network Interfaces](../../../../assets/storage-dell-unity-hc-network-interfaces.svg)

```bash
# Network interface status
uemcli -d <ip> -u admin /net/if show | grep -E "ID|Health|IP"
```

## Health Check Summary

![Health Check Summary](../../../../assets/storage-dell-unity-hc-health-check-summary.svg)

| Check | Command | Healthy |
|---|---|---|
| System health | `/sys/general show` | Health = OK |
| No critical alerts | `/prac/alert show` | 0 critical alerts |
| All disks normal | `/stor/config/disk show` | All = Normal |
| Pools < 80% used | `/stor/config/pool show` | Free > 20% |
| All LUNs OK | `/stor/config/lun show` | All health = OK |
| Replication sessions OK | `/prot/rep/session show` | All OK / Synced |
| Both SPs online | `/sys/sp show` | Both = OK |

## Daily Health Check Sequence

![Daily Health Check Sequence](../../../../assets/storage-dell-unity-hc-daily-health-check-sequence.svg)

```d2
direction: right

START: "Begin daily check" {shape: rectangle}
SYS: "uemcli /env/health show\n-filter" {shape: rectangle}
SYS_OK: "SYS_OK" {shape: rectangle}
TRIAGE: "Triage fault\ncheck Common Issues KB" {shape: rectangle}
SP: "uemcli /env/sp show\nBoth SPs Active?" {shape: rectangle}
SP_OK: "SP_OK" {shape: rectangle}
SPFAIL: "One SP offline —\ncheck fault LEDs\nopen Dell case if hardware" {shape: rectangle}
POOL: "uemcli /stor/config/pool show\nPool capacity < 80%?" {shape: rectangle}
POOL_OK: "POOL_OK" {shape: rectangle}
CAPACT: "Expand pool or\ndelete snapshots" {shape: rectangle}
REP: "uemcli /prot/rep/session show\nAll sessions Active?" {shape: rectangle}
REP_OK: "REP_OK" {shape: rectangle}
REPFIX: "Resume or investigate\nreplication session" {shape: rectangle}
DISK: "uemcli /stor/config/disk show\nAll disks Normal?" {shape: rectangle}
DISK_OK: "DISK_OK" {shape: rectangle}
REPLACE: "Initiate drive replacement\nmonitor RAID rebuild" {shape: rectangle}
DONE: "All checks passed" {shape: rectangle}

START -> SYS
SYS_OK -> TRIAGE
SYS_OK -> SP
SP_OK -> SPFAIL
SP_OK -> POOL
POOL_OK -> CAPACT
POOL_OK -> REP
REP_OK -> REPFIX
REP_OK -> DISK
DISK_OK -> REPLACE
DISK_OK -> DONE
```

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Unity — Procedures](../procedures/)
- [Unity — CLI Reference](../cli-reference/)
- [Unity — Common Issues](../../troubleshooting/common-issues/)
