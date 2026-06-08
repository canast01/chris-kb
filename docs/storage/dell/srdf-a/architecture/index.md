# SRDF/A — Architecture

<div class="kb-summary">
Dell PowerMax SRDF/A asynchronous replication — delta set cycle model buffers writes and transmits to R2 on a ~30-second cycle; RPO equals the last completed cycle.
</div>

```text
┌──────────────────────────────────────── SRDF/A — Architecture ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                SRDF/A — Component Architecture                                │   │
│   │          R1 Volume (Source)  — primary data on production PowerMax; host writes here          │   │
│   │        R2 Volume (Target)  — replica on DR PowerMax; receives delta sets asynchronously       │   │
│   │        SRDF/A Engine       — delta-set formation: groups writes per cycle, ships to R2        │   │
│   │             Ports: FC dark fiber / DWDM · FCIP (TCP 3225) · 9443 (Unisphere HTTPS)            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Three-tier component model — control plane, data plane, and management                             │
│                                                                                                       │
│                          ▼                        ▼                        ▼                          │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Control Plane        │  │          Data Plane         │  │          Management         │   │
│   │ R1 Volume (Source)  — primar│  │ R2 Volume (Target)  — replic│  │ PowerMax Mgmt       — Unisph│   │
│   │          Scheduling         │  │      Replication/Backup     │  │     FC dark fiber / DWDM    │   │
│   │         Policy mgmt         │  │        Data movement        │  │           REST API          │   │
│   │          Catalog/DB         │  │        Dedup/compress       │  │             RBAC            │   │
│   │          Job engine         │  │       FCIP (TCP 3225)       │  │           Alerting          │   │
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
![SRDF/A Architecture](../../../../assets/srdf-a-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Delta set mechanics, SRDF group design, pair states, SYMCLI commands, and bandwidth sizing.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>SRM, Solutions Enabler, and TimeFinder/SnapVX for backup offload.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>SRDF group naming, cycle time standards, lag thresholds, and DSE sizing.</span></a>
</div>

| State | Meaning | Normal? |
|---|---|---|
| Consistent | R2 is consistent and receiving cycles | Yes — normal SRDF/A state |
| SyncInProg | Synchronisation in progress after resume | Transient |
| Transmit Idle | No data being transmitted | Investigate if unexpected |
| Suspended | Replication manually suspended | Expected for maintenance |
| Failed Over | R1 read-only; R2 writable | Active failover underway |


