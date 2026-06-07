# SRDF/S

<div class="kb-summary">
Dell PowerMax SRDF/S synchronous replication — every host write committed to both R1 and R2 before acknowledgement; guarantees RPO = 0 with ≤10ms inter-site RTT requirement.
</div>

```text
┌────────────────────────────────────────── SRDF/S — Overview ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                             SRDF/S                                            │   │
│   │  Synchronous replication for PowerMax/VMAX — RPO=0, write not acknowledged until R2 confirms  │   │
│   │          R1 Volume (Source)  — production PowerMax; write holds until R2 acknowledges         │   │
│   │        R2 Volume (Target)  — DR PowerMax; must confirm write before host I/O completes        │   │
│   │        SRDF/S Engine       — synchronous write mirroring; adds WAN RTT to write latency       │   │
│   │       Management: Dark fiber FC (< 5 ms RTT) · Auth: Symmetrix admin; Solutions Enabler       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture: components work together to deliver SRDF/S capabilities                              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Architecture                 │  │                  Operations                 │   │
│   │ R1 Volume (Source)  — production PowerMax;   │  │           symrdf establish -type s          │   │
│   │ R2 Volume (Target)  — DR PowerMax; must con  │  │               symrdf failover               │   │
│   │ SRDF/S Engine       — synchronous write mir  │  │                 symrdf query                │   │
│   │ PowerMax Mgmt       — Unisphere + symrdf; f  │  │              symrdf -rdfg list              │   │
│   │ SRDF Link           — ultra-low-latency FC/  │  │                symrdf restore               │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
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


```text
┌─────────────────────────── SRDF/S Synchronous Replication — Setup Sequence ───────────────────────────┐
│                                                                                                       │
│  Step 1 · Prerequisites                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  PowerMax / VMAX arrays at R1 and R2  ·  RTT ≤ 10 ms between sites (hard requirement)                 │
│  Measure RTT: ping from R1 director to R2 director management port  ·  must be < 10 ms                │
│  SRDF licence active  ·  dedicated GigE or 16/32 GbE FC RDF links provisioned                         │
│  Bandwidth: provision 1.5× peak write throughput on RDF link for headroom                             │
│  R2 device capacity ≥ R1 capacity  ·  same device emulation type required                             │
│                                                                                                       │
│                                        │  configure SRDF groups                                       │
│                                        ▼                                                              │
│  Step 2 · SRDF Group Configuration                                                                    │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Create synchronous RDF group: symrdf addgrp -rdfg <id> -type RDF1                                    │
│  Set mode to synchronous: symrdf -rdfg <id> set synchronous                                           │
│  Assign RA director ports to group  ·  verify port assignment with symrdf -rdfg query                 │
│  MaxTimeDiffAllowed: default 200 ms  ·  sets max acceptable write-acknowledge latency                 │
│  Verify link state: symrdf -rdfg <id> -dir <dir> query → link state = Ready                           │
│                                                                                                       │
│                                        │  create and synchronise device pairs                         │
│                                        ▼                                                              │
│  Step 3 · Device Pairs & Initial Sync                                                                 │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Create SRDF/S pairs: symrdf -sid <R1> -f <devfile> createpair -rdfg <id> -type R1                    │
│  Initial full sweep: source data copied to R2  ·  may take hours for large volumes                    │
│  Monitor sync progress: symrdf -sid <R1> query  ·  state = SyncInProg then Synchronized               │
│  Once Synchronized: every host write is committed to both R1 and R2 before ACK                        │
│  Confirm: symrdf -sid <R1> -dev <range> verify -consistency → clean output                            │
│                                                                                                       │
│                                        │  tune and validate write performance                         │
│                                        ▼                                                              │
│  Step 4 · Performance Tuning                                                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Baseline write latency: measure before SRDF/S  ·  SRDF/S adds 1× RTT to each write                   │
│  Monitor write latency impact: symstat -type rdf on R1  ·  acceptable if < 5 ms added                 │
│  Adaptive Copy (STAR): option for planned maintenance  ·  temporarily reduces to async                │
│  SRDF/S Consistency Groups: multiple device groups committed atomically                               │
│  WAN optimisation: enable SRDF data compression if link bandwidth is constrained                      │
│                                                                                                       │
│                                        │  monitor and maintain                                        │
│                                        ▼                                                              │
│  Step 5 · Monitoring & Health                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  symrdf query: state = Synchronized means R2 is in-sync  ·  alert on any other state                  │
│  symrdf -cg <name> query for consistency group state  ·  all groups must be Synchronized              │
│  RDF link utilisation: symrdf -rdfg <id> -dir <d> query  ·  check bandwidth metrics                   │
│  Alert thresholds: link RDF error count > 0  ·  state not Synchronized > 60 s                         │
│  SRDF/S Audit: repadmin equivalent  ·  use Unisphere for PowerMax health dashboard                    │
│                                                                                                       │
│                                        │  failover testing                                            │
│                                        ▼                                                              │
│  Step 6 · Failover Testing                                                                            │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Planned failover: symrdf -sid <R1> -dev <range> failover -establish  ·  graceful                     │
│  Unplanned: symrdf -sid <R2> -dev <range> failover -force  ·  if R1 unreachable                       │
│  Test R2 application: RPO = 0 (no writes lost)  ·  RTO = time to bring up app stack                   │
│  Failback: symrdf -sid <R2> failback  ·  R1 resyncs from R2  ·  monitor with query                    │
│  Full resync back to Synchronized state  ·  confirm both sites clean in Unisphere                     │
│  Document: RTO achieved  ·  failback duration  ·  confirm RPO=0 from host perspective                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>Synchronous write commit model, pair states, RTT requirements, SYMCLI commands, and RTO targets.</span>
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
