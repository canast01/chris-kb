# SRDF/S — Backup & Restore

```bash
# Query SRDF state for a storage group
symrdf -sg PROD_SG query

# Detailed output including track counts and sync %
symrdf -sg PROD_SG query -detail

# Query by RDF group number
symrdf list -rdfg <rdf_group_number> -detail
```

```text
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
```bash
# Suspend SRDF replication (I/O continues on R1, no longer replicated)
symrdf -sg PROD_SG suspend

# Query suspended state
symrdf -sg PROD_SG query
# R1 St = WD, Link = Suspended
```
```bash
# Resume SRDF — re-syncs changed tracks from R1 to R2
symrdf -sg PROD_SG resume

# Monitor sync progress — watch Tracks/% fields
symrdf -sg PROD_SG query -detail
```
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
```bash
# establish syncs from the current "source" (post-failover this is R2) to R1
symrdf -sg PROD_SG establish -force
```
