---
tags:
  - dell
  - operations
---
# SRDF/S — Operations



<div class="kb-summary">
SRDF/S day-to-day operations — synchronous link monitoring, R1/R2 device management, and failover/failback procedures.
</div>

```text
┌───────────────────────────────────────── SRDF/S — Operations ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 SRDF/S — Day-to-Day Operations                                │   │
│   │          Daily: review job status · check health alerts · verify last backup/replica          │   │
│   │            Weekly: review capacity trends · test restore sample · review error logs           │   │
│   │             Monthly: full restore test · review retention · audit service accounts            │   │
│   │              Quarterly: DR failover test · firmware review · update documentation             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                        ▼                        ▼                          │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Backup/Replicate      │  │           Monitor           │  │           Recover           │   │
│   │   symrdf establish -type s  │  │         symrdf query        │  │       symrdf failover       │   │
│   │        Schedule jobs        │  │        Health checks        │  │       Instant restore       │   │
│   │        Retention mgmt       │  │       Capacity alerts       │  │        Failover test        │   │
│   │       Consistency grp       │  │          Log review         │  │          DR runbook         │   │
│   │        Policy updates       │  │         SLA tracking        │  │         Validate RTO        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
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
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>Command reference by category with syntax and examples.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Daily checks, validation, and performance metrics.</span>
</a>

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Failover, resync, failback, suspend/resume, and maintenance runbooks.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Install & Upgrade</strong>
  <span>Version compatibility, firmware upgrades, migration, and decommission.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup & Restore</strong>
  <span>Backup and restore procedures for SRDF/S environments.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts for state checks, failover, health reporting, and latency.</span>
</a>

</div>
