# SRDF/S

<div class="kb-summary">
Dell PowerMax SRDF/S synchronous replication — every host write committed to both R1 and R2 before acknowledgement; guarantees RPO = 0 with ≤10ms inter-site RTT requirement.
</div>

```
┌────────────────────────────────────────── SRDF/S — Overview ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                             SRDF/S                                            │   │
│   │  Synchronous replication for PowerMax/VMAX — RPO=0, write not acknowledged until R2 confirms  │   │
│   │          R1 Volume (Source)  — production PowerMax; write holds until R2 acknowledges         │   │
│   │        R2 Volume (Target)  — DR PowerMax; must confirm write before host I/O completes        │   │
│   │        SRDF/S Engine       — synchronous write mirroring; adds WAN RTT to write latency       │   │
│   │Management: Dark fiber FC (< 5 ms RTT) · Auth: Symmetrix admin credentials; Solutions Enabler; │   │
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
