---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# SRDF/S — Troubleshooting



<div class="kb-summary">
Diagnosing SRDF/S link failures, synchronisation errors, SUSPENDED state recovery, and RDF group health issues.
</div>

```text
┌────────────────────────────────────── SRDF/S — Troubleshooting ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               SRDF/S — Troubleshooting Approach                               │   │
│   │                   1  Identify: which job, component, or resource is failing                   │   │
│   │                  2  Scope: single job vs all jobs; one source vs all sources                  │   │
│   │             3  Collect: logs and run status command; review recent change history             │   │
│   │                 4  Diagnose: match symptoms to known issues; check error codes                │   │
│   │                     5  Fix: apply resolution; verify fix; monitor next run                    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                        ▼                        ▼                          │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Infrastructure       │  │         Application         │  │             Data            │   │
│   │        Network checks       │  │         Log analysis        │  │        Catalog check        │   │
│   │        Storage space        │  │       Job error codes       │  │         Consistency         │   │
│   │        Process health       │  │        Auth failures        │  │       Corruption scan       │   │
│   │  Dark fiber FC (< 5 ms RTT  │  │        Timeout errors       │  │         Restore test        │   │
│   │        Firewall rules       │  │        Version compat       │  │          RPO drift          │   │
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

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Write latency, pair state problems, ISL failures, and unintended failovers.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Diagnostic commands, log locations, and data collection procedures.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>Dell vendor support, required diagnostics, SLA tiers, and case opening.</span>
</a>

</div>

