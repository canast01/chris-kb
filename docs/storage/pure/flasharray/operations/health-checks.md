---
tags:
  - operations
  - pure
---
# FlashArray — Health Checks


<div class="kb-summary">
Health Checks reference covering Daily Checks, Health Check, Controller Health, Drive Health, Volume Health and 5 more sections.
</div>
```text
┌─────────────────────────────────── Pure FlashArray — Health Checks ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      FlashArray health checks: routine verification of operational status and performance     │   │
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
│   │         Controllers         │  │        Active-active        │  │           No SPOF           │   │
│   │            Drives           │  │         DirectFlash         │  │         NVMe native         │   │
│   │           Volumes           │  │       Thin provisioned      │  │        Instant clone        │   │
│   │        ActiveCluster        │  │       Sync replication      │  │           Zero RPO          │   │
│   │           SafeMode          │  │       Immutable snaps       │  │      Ransomware resist      │   │
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
│    Physical: FlashArray//X or //C controllers · DirectFlash NVMe modules · 25/100 GbE / 32Gb FC       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    FlashArray         = Pure all-NVMe block/file array; inline dedup and compression always enabled   │
│    DirectFlash        = Pure proprietary NVMe modules; direct flash access without SAS translation    │
│    ActiveCluster      = synchronous active-active stretch cluster; hosts see a single namespace       │
│    ActiveDR           = asynchronous replication to DR site; recovery point objective in seconds      │
│    SafeMode           = admin-locked immutable snapshots; cannot be deleted even by array administr...│
│    Protection group   = set of volumes and hosts sharing a snapshot and replication schedule          │
│    purefa CLI         = REST CLI tool for FlashArray; purefa CLI connects via REST API key            │
│    purearray          = purectl CLI command: purearray list and purearray show monitoring             │
│    Volume tag         = user-defined key-value label on volumes for policy and reporting purposes     │
│    Host group         = logical collection of hosts sharing volume access via a host group object     │
│    Inline dedup       = content-based deduplication performed inline before data is written to flash  │
│    Evergreen          = Pure architecture; controllers upgrade non-disruptively, shelves remain in ...│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


```text
FlashArray Health Check Sequence
  purealert list ──► Any error/warning alerts?
         │
         ▼
  puredrive list ──► All drives healthy?
         │
         ▼
  purearray list --controller ──► Both CT0 + CT1 ok?
         │
         ▼
  purepod list ──► ActiveCluster pods stretched + replicating?
         │
         ▼
  purearray list --space ──► Capacity < 80% used?
         │
         ▼
  purehost list ──► All hosts connected (no zero-path hosts)?
         │
         ▼
         OK — check Pure1 for fleet-level anomalies
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

1. **Array health** — `purediag --run basic` or Pure1 → Array → Health — verify all components are green
2. **Drive status** — `pureadm list` — all drives should be Healthy; `pureadm list --failed` should return empty
3. **Volume health** — `purevol list --flagged` — should return empty
4. **Protection group lag** — `purepgroup list --snap` — verify snapshot lag is within RPO
5. **ActiveDR / ActiveCluster status** — `purehgroup list` — verify host group and pod status
6. **Performance baseline** — `purearray monitor` — check IOPS, bandwidth, and latency vs baseline
7. **Capacity trend** — `purearray monitor --resolution 86400 --length 604800` — review 7-day capacity trend
8. **Phone home status** — Pure1 → Settings → Phone Home — verify array is connected and reporting

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| [ ] Run `purealert list` | `purealert list` | review all active alerts; flag any with severity `error` or `warning` |
| [ ] Run `puredrive list` | `puredrive list` | confirm all drives are in `healthy` state; flag any `failed`, `recovering`, or `missing` drives |
| [ ] Run `purearray list --space` | `purearray list --space` | review array capacity and data reduction ratio; flag if used capacity > 80% |
| [ ] Run `purepod list` | `purepod list` | confirm all ActiveCluster pods are `stretched` and online (if configured) |
| [ ] Check Pure1 portal for AI-driven health recommendations, anomalies |  |  |
| [ ] Run `purevol list --space` | `purevol list --space` | review volume space usage; flag any volumes approaching their allocated limit |
| [ ] Run `puresnap list` | `puresnap list` | check snapshot count; flag runaway snapshot growth from misconfigured protection group schedules |
| [ ] Confirm replication to the secondary array is current | `purepod list --replicating` |  |

## Health Check

- [ ] No active alerts in `purealert list`
- [ ] All drives healthy — `puredrive list` shows no `failed` or `recovering` drives
- [ ] Array capacity below 80% used
- [ ] Both controllers are healthy and running the same Purity version: `purearray list --controller`
- [ ] ActiveCluster pods are stretched and replicating: `purepod list --replicating` shows `true`
- [ ] All host connections are active — no hosts with zero paths: `purehost list`
- [ ] No runaway snapshot growth consuming unexpected capacity

```bash
# Array overall status and Purity version
purearray list

# Controller status and firmware version
purearray list --controller

# Array capacity, data reduction, and space usage
purearray list --space

# All active alerts
purealert list

# All drives and health state
puredrive list

# ActiveCluster pods and replication state
purepod list
purepod list --replicating

# All volumes with space usage
purevol list --space

# Snapshot count and usage
puresnap list

# Real-time performance (latency, IOPS, bandwidth)
purearray monitor

# Host and host group connectivity
purehost list
purehgroup list
```

## Controller Health

```bash
purehw list | grep -i ct
```

Both controllers (CT0, CT1) should show `status: ok` and `temperature` within normal range.

## Drive Health

```bash
puredrive list
```

All drives should show `status: healthy`. Any drive in `failed`, `unhealthy`, or `recovering` state requires attention.

## Volume Health

```bash
purevol list
purevol list --space
```

Verify no volumes are in an unexpected state and capacity is within expected range.

## Host Connectivity

```bash
# List hosts and their connected volumes
purehost list
purehost list --connect

# List host connections
purehost list --connection
```

Confirm all expected hosts are connected.

## Replication Health

```bash
# FlashArray Async Replication (ActiveDR or async)
purepod list
purepod list --replicating
purepod list --schedule
```

Verify pod/protection group replication is healthy.

## Pure1 Cloud Monitoring

Pure1 provides proactive health monitoring and AI-driven alerts:
- Log in to **Pure1 → Arrays** → verify all arrays show green
- **Analysis → Capacity** — no arrays approaching full
- **Alerts** — no critical unacknowledged alerts

## Pre-Change Checklist

- [ ] All drives `healthy`
- [ ] Both controllers `ok`
- [ ] No critical active alerts
- [ ] Replication healthy
- [ ] Capacity below 80%

## Health Summary Table

| Check | Command | Expected |
|---|---|---|
| Array health | `purearray list` | No warnings |
| Drives | `puredrive list` | All healthy |
| Hardware | `purehw list` | All ok |
| Alerts | `purealert list` | No critical |
| Capacity | `purearray list --space` | < 80% used |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
