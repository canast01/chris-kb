# SRDF/S — Backup & Restore

## SRDF/S Overview

**SRDF/S (Synchronous)** provides zero-data-loss replication between two VMAX/PowerMax arrays. Every host write is mirrored to the remote array before the I/O is acknowledged to the host. This guarantees write-order consistency and ensures R1 and R2 are always at the same recovery point.

| Property | SRDF/S |
|---|---|
| Mode | Synchronous |
| RPO | Zero (no data loss on planned failover) |
| RTO | Minutes (depends on failover procedure and application restart) |
| Impact on host I/O | Write latency includes round-trip to R2 |
| Distance constraint | Typically <200 km (latency sensitive — <5 ms RTT recommended) |
| Use case | Metro DR, financial systems, zero-RPO requirement |

---

## SYMCLI Command Reference

All operations use `symrdf` from SYMCLI. The `-sg` flag (Storage Group level) is preferred in VMAX3 and PowerMax environments over the older device-group `-g` flag.

### Query RDF State

```bash
# Query SRDF state for a storage group
symrdf -sg PROD_SG query

# Detailed output including track counts and sync %
symrdf -sg PROD_SG query -detail

# Query by RDF group number
symrdf list -rdfg <rdf_group_number> -detail
```
┌────────────────────────────────────── SRDF/S — Backup & Restore ──────────────────────────────────────┐
│                                                                                                       │
│    Backup flow: quiesce source → snapshot/copy → transfer → write to target → catalog                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Backup (Protection)              │  │              Restore (Recovery)             │   │
│   │           symrdf establish -type s           │  │               symrdf failover               │   │
│   │              Quiesce source I/O              │  │            Select recovery point            │   │
│   │             Take snapshot / CBT              │  │           Mount or copy to target           │   │
│   │           Transfer changed blocks            │  │              Validate integrity             │   │
│   │             Commit to repository             │  │             Restart application             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                      Key SRDF/S Commands                                      │   │
│   │                            Backup trigger  : symrdf establish -type s                         │   │
│   │                                List points     : symrdf failover                              │   │
│   │                                  Health status   : symrdf query                               │   │
│   │                                 Retention mgmt  : symrdf restore                              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment        │
│  R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency       │
│  R2            = target volume; must acknowledge each write; acts as synchronous mirror               │
│  RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency       │
│  RPO=0         = zero recovery point objective; no data loss possible under normal operation          │
│  RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min       │
│  symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver       │
│  Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split                          │
│  Consistent    = transient state where R1 write is in transit but not yet confirmed on R2             │
│  Failover      = makes R2 read-write; production continues from DR site after R1 failure              │
│  Restore       = re-synchronises after failover; direction is reversed until R1 catches up            │
│  RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters           │
│  FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)            │
│  RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Planned Failover Command

```bash
# Planned failover — requires link to be healthy and synchronized
symrdf -sg PROD_SG failover

# Verify post-failover state
symrdf -sg PROD_SG query
# Expected: R2 devices = RW, R1 devices = WD/NR
```

A planned `failover` without `-force` verifies synchronization first and will abort if data could be lost.

---

## Unplanned Failover Procedure

When the R1 site suffers an outage and the SRDF link is severed, a forced failover is required.

### Unplanned Failover Steps

```bash
# 1. Confirm R1 site is confirmed down (not a transient network issue)
symrdf -sg PROD_SG query
# Expected state: Link shows Suspended or R1 Not Ready

# 2. Suspend the SRDF link (if not already suspended by the array)
symrdf -sg PROD_SG suspend -force

# 3. Force failover — promote R2 devices to RW
symrdf -sg PROD_SG failover -force

# 4. Verify R2 devices are now in RW state
symrdf -sg PROD_SG query

# 5. Present R2 volumes to DR hosts and start workloads
```

**Caution:** In a synchronous pair, forced failover during an outage is effectively zero-data-loss if the link was synchronized before the failure. If the link had suspended writes (e.g., network drop was not immediate), up to the in-flight writes may be lost.

---

## Link Suspension and Recovery

Link suspension halts replication without breaking the SRDF pair. This is used for planned maintenance on the link or array, or as an intermediate step before failover.

### Suspend Replication

```bash
# Suspend SRDF replication (I/O continues on R1, no longer replicated)
symrdf -sg PROD_SG suspend

# Query suspended state
symrdf -sg PROD_SG query
# R1 St = WD, Link = Suspended
```

### Resume Replication

```bash
# Resume SRDF — re-syncs changed tracks from R1 to R2
symrdf -sg PROD_SG resume

# Monitor sync progress — watch Tracks/% fields
symrdf -sg PROD_SG query -detail
```

During suspension, host I/O continues on R1 with no added latency. Invalid tracks accumulate. On resume, only delta tracks are resynced — not a full copy.

---

## symrdf restore — After R1 Site Recovery

After the primary site is recovered and R1 is back online, restore re-establishes R1 as the source using R2 as the authoritative copy. Use this when R1 volumes are stale relative to R2 (i.e., production has been running on R2 during outage).

```bash
# 1. Verify R1 array and volumes are accessible
symdev list -sid <R1_SID> | grep <device_range>

# 2. Restore — overwrites R1 with R2 content, then flips direction
#    This is a DESTRUCTIVE operation on R1 volumes — confirm before running
symrdf -sg PROD_SG restore -force

# 3. Monitor resync from R2 to R1
symrdf -sg PROD_SG query -detail
# Watch: Sync% and Invalid Tracks decrease

# 4. Wait for full synchronization
symrdf -sg PROD_SG verify -consistent

# 5. Confirm synchronized — then fail back to R1
symrdf -sg PROD_SG failover
# Now R1 is promoted back to RW, R2 returns to WD

# 6. Start production workloads on R1
```

### Alternative: Establish (Reverse Sync — R2 to R1)

```bash
# establish syncs from the current "source" (post-failover this is R2) to R1
symrdf -sg PROD_SG establish -force
```

`restore` and `establish` differ in that `restore` explicitly reverses R1/R2 roles before syncing; `establish` syncs in the current direction. After a failover where R2 is active, `restore` is the correct command to recover R1.

---

## Validation Checklist

| # | Check | Command |
|---|---|---|
| 1 | R2 devices in RW state post-failover | `symrdf -sg PROD_SG query` |
| 2 | No outstanding invalid tracks | `symrdf -sg PROD_SG query -detail \| grep Tracks` |
| 3 | Volumes accessible on DR hosts | `lsblk` / disk manager |
| 4 | File systems mounted and consistent | `mount` / `df -h` / `chkdsk` |
| 5 | Applications healthy on DR | Application health check |
| 6 | SRDF link status during outage documented | Query output saved |
| 7 | R1 restore progress monitored to 100% | `symrdf query -detail` |
| 8 | Sync verified before production failback | `symrdf verify -consistent` |
| 9 | Replication direction restored to R1→R2 | `symrdf query` shows normal direction |
| 10 | Backup jobs re-pointed to correct volumes | Backup policy review |
| 11 | DR test / incident documented | DR report / ITSM record |

---

## SRDF/S vs SRDF/A Decision Reference

| Scenario | Recommended Mode |
|---|---|
| Metro site < 100 km, <5 ms RTT | SRDF/S (zero RPO) |
| Regional DR > 100 km, WAN constrained | SRDF/A |
| Financial systems — zero data loss required | SRDF/S |
| Batch workloads tolerating minutes of RPO | SRDF/A |
| Application requires synchronous write confirmation | SRDF/S |
| Write-latency sensitive application (OLTP) | Evaluate SRDF/A or SRDF/Metro |

**SRDF/Metro** (not covered here) provides an Active-Active variant of SRDF/S, where both R1 and R2 accept writes simultaneously — used for workload distribution and non-disruptive planned failover.

---

## Common SYMCLI Commands Summary

| Operation | Command |
|---|---|
| Query SG state | `symrdf -sg <sg> query` |
| Query with detail | `symrdf -sg <sg> query -detail` |
| Planned failover | `symrdf -sg <sg> failover` |
| Forced failover | `symrdf -sg <sg> failover -force` |
| Suspend link | `symrdf -sg <sg> suspend` |
| Resume link | `symrdf -sg <sg> resume` |
| Restore R1 from R2 | `symrdf -sg <sg> restore -force` |
| Establish replication | `symrdf -sg <sg> establish -force` |
| Verify consistency | `symrdf -sg <sg> verify -consistent` |
| List RDF groups | `symcfg list -rdfg all` |
| Check director status | `symcfg list -rdfdir all` |
