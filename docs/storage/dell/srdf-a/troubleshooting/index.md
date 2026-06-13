---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# SRDF/A — Troubleshooting



<div class="kb-summary">
Diagnosing SRDF/A cycle failures, delta set overflow, link errors, and async RPO violations.
</div>

```text
┌────────────────────────────────────── SRDF/A — Troubleshooting ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               SRDF/A — Troubleshooting Approach                               │   │
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
│   │     FC dark fiber / DWDM    │  │        Timeout errors       │  │         Restore test        │   │
│   │        Firewall rules       │  │        Version compat       │  │          RPO drift          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports      │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology               │
│  R1            = source SRDF volume on production array; host writes flow here                        │
│  R2            = target SRDF volume on DR array; receives replicated data asynchronously              │
│  Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically          │
│  Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO                  │
│  symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore       │
│  SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth             │
│  Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle            │
│  Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts                   │
│  Restore       = after failover resolution, re-establishes replication with R1 as source              │
│  Establish     = initial sync or re-sync operation that copies R1 to R2 in full                       │
│  Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication                 │
│  FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link                      │
│  Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Link down, cycle time growth, suspended groups, capacity mismatches, and invalid pair state.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>On-call triage steps, lag alert response, and diagnostic command reference.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>Opening Dell support cases, required diagnostics, and SLA tiers.</span>
</a>

</div>

