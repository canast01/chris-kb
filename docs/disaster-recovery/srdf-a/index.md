# SRDF/A

<div class="kb-summary">
Dell PowerMax SRDF/A asynchronous replication — delta set cycle model buffers host writes and transmits to the R2 target on ~30-second cycles; RPO equals the last completed cycle.
</div>

```
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

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>Delta set mechanics, dual-site topology, pair states, SYMCLI commands, and bandwidth sizing.</span>
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
