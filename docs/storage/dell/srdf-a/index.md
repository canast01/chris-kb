---
tags:
  - dell
---
# SRDF/A

<div class="kb-summary">
Dell PowerMax SRDF/A asynchronous replication — delta set cycle model buffers host writes and transmits to the R2 target on ~30-second cycles; RPO equals the last completed cycle.

*Applies to: SRDF/A*
</div>

```text
┌────────────────────────────────────────── SRDF/A — Overview ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                             SRDF/A                                            │   │
│   │       Asynchronous replication for PowerMax/VMAX — delta-set cycle-based RPO in seconds       │   │
│   │          R1 Volume (Source)  — primary data on production PowerMax; host writes here          │   │
│   │        R2 Volume (Target)  — replica on DR PowerMax; receives delta sets asynchronously       │   │
│   │        SRDF/A Engine       — delta-set formation: groups writes per cycle, ships to R2        │   │
│   │  Management: FC dark fiber / DWDM · Auth: Symmetrix/PowerMax admin credentials; Solutions En  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture: components work together to deliver SRDF/A capabilities                              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Architecture                 │  │                  Operations                 │   │
│   │ R1 Volume (Source)  — primary data on produ  │  │               symrdf establish              │   │
│   │ R2 Volume (Target)  — replica on DR PowerMa  │  │          symrdf failover / failback         │   │
│   │ SRDF/A Engine       — delta-set formation:   │  │                 symrdf query                │   │
│   │ PowerMax Mgmt       — Unisphere for PowerMa  │  │           symrdf suspend / resume           │   │
│   │ SRDF Link           — dedicated FC or FCIP   │  │                symrdf verify                │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
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


```text
┌────────────────────────── SRDF/A Asynchronous Replication — Setup Sequence ───────────────────────────┐
│                                                                                                       │
│  Step 1 · Prerequisites                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  PowerMax / VMAX arrays at R1 (production) and R2 (DR) site  ·  Enginuity 6079+                       │
│  SRDF licence active on both arrays  ·  GigE or FC RDF links between directors                        │
│  Round-trip latency measured  ·  no RTT hard limit for SRDF/A (cycle absorbs delay)                   │
│  SRDF Director pairs identified: RA-GRP on each array must include same director IDs                  │
│  Capacity: R2 devices must equal or exceed R1 in size  ·  same emulation type                         │
│                                                                                                       │
│                                        │  create SRDF groups                                          │
│                                        ▼                                                              │
│  Step 2 · SRDF Group Configuration                                                                    │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Create dynamic RDF group: symrdf addgrp -rdfg <id> -type RDF1 -remote_rdfg <id>                      │
│  Assign RA director ports to the group: symrdf -rdfg <id> addport -port <dir:port>                    │
│  Set SRDF/A mode on the group: symrdf -rdfg <id> set async                                            │
│  Configure cycle time: default 30 seconds  ·  reduce to 15 s for tighter RPO if link allows           │
│  Verify group: symrdf -rdfg <id> -dir <d> query  ·  link state should show Ready                      │
│                                                                                                       │
│                                        │  create SRDF device pairs                                    │
│                                        ▼                                                              │
│  Step 3 · Device Pairs                                                                                │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Identify R1 devices: symdev list -sid <R1> -dev <range>  ·  note device IDs                          │
│  Create SRDF pairs: symrdf -sid <R1> -f <dev_file> createpair -rdfg <id> -type R1                     │
│  Initial synchronisation begins automatically  ·  monitor with symrdf -sid <R1> query                 │
│  Verify pair state transitions: Invalid → SyncInProg → Consistent (SRDF/A) or Synchronized            │
│  Confirm R2 devices visible on DR array: symdev -sid <R2> list -rdfg <id>                             │
│                                                                                                       │
│                                        │  enable SRDF/A and monitor                                   │
│                                        ▼                                                              │
│  Step 4 · SRDF/A Activation & Monitoring                                                              │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Enable SRDF/A: symrdf -sid <R1> -rdfg <id> set async  ·  verify Consistent state                     │
│  Delta set cycle: R1 buffers writes per cycle  ·  transmits at cycle boundary to R2                   │
│  Monitor lag: symrdf -sid <R1> query  ·  field 'Delta(s)' is current delta set age                    │
│  Alert if delta set lag > 2 × cycle time: indicates network congestion or bandwidth issue             │
│  SRDF/A compliance: check Async Cyclic mode  ·  verify no Adaptive Copy active                        │
│                                                                                                       │
│                                        │  test and document failover                                  │
│                                        ▼                                                              │
│  Step 5 · Consistency & Performance                                                                   │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  SRDF/A Consistency Group: symrdf cg create  ·  add device groups  ·  enables crash-consistent        │
│  Monitor with Solutions Enabler: symrdf -cg <name> query  ·  check CG state                           │
│  Performance: SRDF/A adds ~30-second RPO at minimum  ·  verify production write latency               │
│  Bandwidth: plan for peak write rate × 2 for burst headroom on WAN link                               │
│  Use symrdf -sid <R1> -rdfg <id> verify to confirm data consistency on R2                             │
│                                                                                                       │
│                                        │  failover testing                                            │
│                                        ▼                                                              │
│  Step 6 · Failover Testing                                                                            │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Suspend SRDF/A: symrdf -sid <R1> -dev <range> suspend  ·  I/O continues on R1                        │
│  Test R2 access: symrdf -sid <R2> -dev <range> failover  ·  bring up DR app                           │
│  Validate data at last completed cycle  ·  note actual RPO achieved in test record                    │
│  Restore: symrdf -sid <R2> -dev <range> failback  ·  resync R1 ← R2                                   │
│  Monitor resync progress: symrdf query  ·  state returns to Consistent after full sweep               │
│  Document: achieved RPO, RTO, resync duration  ·  review against SLA targets                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>Delta set mechanics, dual-site topology, pair states, SYMCLI commands, and bandwidth sizing.</span>
</a>

<a class="kb-card" href="deploy/">
  <strong>Deploy</strong>
  <span>Installation, initial configuration, and deployment procedures.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
