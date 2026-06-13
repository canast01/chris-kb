---
tags:
  - dell
  - operations
---
# Unity — Health Checks


<div class="kb-summary">
Daily and pre/post-change health checks for Dell Unity storage systems.
</div>
```text
┌──────────────────────────────────── Dell Unity XT — Health Checks ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Unity XT health checks: routine verification of operational status and performance      │   │
│   │         Checks include: controller status, drive health, replication lag, and capacity        │   │
│   │         Frequency: daily quick checks; weekly detailed review; monthly capacity report        │   │
│   │        Configure threshold-based alerts for proactive incident prevention and awareness       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Check status → review alerts → verify replication → capacity → log                                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Ctrl            │  │         SP-A + SP-B         │  │        Cache mirrored       │   │
│   │             Pool            │  │       Dynamic FAST VP       │  │         Auto-tiering        │   │
│   │          NAS server         │  │        File protocols       │  │          Per-tenant         │   │
│   │           Snapshot          │  │        Writable snaps       │  │        Thin PiT copy        │   │
│   │         Replication         │  │         Async/Metro         │  │       Native or RP4VM       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Check area    │  How to verify   │   Pass criteria   │    Frequency     │       Tool       │   │
│   │   Controllers    │   show status    │    All healthy    │      Daily       │     CLI/GUI      │   │
│   │      Drives      │   show drives    │  No failed/pred.  │      Daily       │     CLI/GUI      │   │
│   │   Replication    │ show replication │  Lag < threshold  │      Daily       │     CLI/GUI      │   │
│   │     Capacity     │  show capacity   │     < 80% used    │      Daily       │     CLI/GUI      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Unity XT 380F/480F/680F/880F · dual SPs · DPE/DAE expansion · 10/25 GbE                  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Unity XT           = Dell unified mid-range array; block LUNs, file NAS, and VMware vVols          │
│    Unisphere          = HTML5 GUI and REST API for Unity XT management; SP-hosted management portal   │
│    UEMCLI             = CLI for Unity XT; uemcli -d <ip> -u admin -p <pw> /show commands              │
│    Storage pool       = collection of drives forming a usable pool; FAST VP tiers data automatically  │
│    FAST VP            = Fully Automated Storage Tiering VP; moves hot and cold data between tiers     │
│    NAS server         = virtual file server on Unity; each has its own IP, DNS, and CIFS/NFS shares   │
│    Data Mover         = older EMC term for NAS server; used in VNX and early Unity documentation      │
│    SP-A / SP-B        = storage processors; active-active HA pair with mirrored cache                 │
│    Snapshot           = space-efficient PiT copy of LUN or FS; writable snapshots supported           │
│    RecoverPoint       = RP4VM; journal-based continuous data protection for Unity volumes             │
│    Metro              = synchronous replication between two Unity XT sites; active-active zero RPO    │
│    vVols              = Virtual Volumes; VASA provider exposes per-VM storage objects to vCenter      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

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

```bash
# Active alerts — any critical alerts require immediate attention
uemcli -d <ip> -u admin /prac/alert show
uemcli -d <ip> -u admin /prac/alert show | grep -i "Critical\|Error"

# Event log
uemcli -d <ip> -u admin /event/syslog show
```

## Hardware

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

```bash
# Pool list with capacity and health
uemcli -d <ip> -u admin /stor/config/pool show -detail

# Flag pools above 80% used
uemcli -d <ip> -u admin /stor/config/pool show | awk '
    /Free/ { getline; if ($3 + 0 < 20) print "WARNING: Pool near full:", $0 }'
```

## LUN Status

```bash
# All LUNs and health
uemcli -d <ip> -u admin /stor/config/lun show -detail | grep -E "Name|Health|Size"

# LUNs with non-OK health
uemcli -d <ip> -u admin /stor/config/lun show | grep -v "OK\|Name"
```

## Replication Sessions

```bash
# All replication sessions
uemcli -d <ip> -u admin /prot/rep/session show

# Sessions not in OK state
uemcli -d <ip> -u admin /prot/rep/session show | grep -v "OK\|Session ID"
```

## Network Interfaces

```bash
# Network interface status
uemcli -d <ip> -u admin /net/if show | grep -E "ID|Health|IP"
```

## Health Check Summary

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

```mermaid
graph TD
  START([Begin daily check]) --> SYS["uemcli /env/health show\n-filter 'health.value ne OK'"]
  SYS --> SYS_OK{Any non-OK\ncomponents?}
  SYS_OK -->|Yes| TRIAGE["Triage fault\ncheck Common Issues KB"]
  SYS_OK -->|No| SP["uemcli /env/sp show\nBoth SPs Active?"]
  SP --> SP_OK{Both Active?}
  SP_OK -->|No| SPFAIL["One SP offline —\ncheck fault LEDs\nopen Dell case if hardware"]
  SP_OK -->|Yes| POOL["uemcli /stor/config/pool show\nPool capacity < 80%?"]
  POOL --> POOL_OK{Free > 20%?}
  POOL_OK -->|No| CAPACT["Expand pool or\ndelete snapshots"]
  POOL_OK -->|Yes| REP["uemcli /prot/rep/session show\nAll sessions Active?"]
  REP --> REP_OK{All Active?}
  REP_OK -->|No| REPFIX["Resume or investigate\nreplication session"]
  REP_OK -->|Yes| DISK["uemcli /stor/config/disk show\nAll disks Normal?"]
  DISK --> DISK_OK{Any faulted?}
  DISK_OK -->|Yes| REPLACE["Initiate drive replacement\nmonitor RAID rebuild"]
  DISK_OK -->|No| DONE([All checks passed])
  classDef decision fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef action fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef warn fill:#b45309,stroke:#92400e,color:#fff
  classDef term fill:#15803d,stroke:#166534,color:#fff
  class SYS_OK,SP_OK,POOL_OK,REP_OK,DISK_OK decision
  class SYS,SP,POOL,REP,DISK action
  class TRIAGE,SPFAIL,CAPACT,REPFIX,REPLACE warn
  class START,DONE term
```

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
