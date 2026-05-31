# Dell Unity XT

<div class="kb-summary">
Mid-range unified storage — block (FC/iSCSI), file (NFS/SMB), and VMware integration with dual storage processor active-active architecture, FAST Cache, inline data reduction, and native replication.
</div>

```text
┌─────────────────────────────── Dell Unity XT Unified Mid-Range Storage ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Unity XT: Dell unified mid-range; dual Storage Processors (SP A/B); active-passive HA     │   │
│   │         Block: FC and iSCSI LUNs; consistency groups; metro volumes for active-active         │   │
│   │            File: NFS, SMB, FTP, NDMP via NAS Server; multiple NAS servers per array           │   │
│   │         FAST VP automated tiering: Flash, SAS, NL-SAS; schedule-driven data placement         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Host → SP A or SP B → LUN / NAS Server → FAST VP tiering → Flash / SAS / NL-SAS drives             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │          Dual SP HA         │  │        Unisphere GUI        │  │          DARE (SED)         │   │
│   │        FAST VP tiers        │  │            uemcli           │  │        LDAP / AD auth       │   │
│   │          NAS Server         │  │        Snap schedules       │  │          RBAC roles         │   │
│   │         Block + File        │  │          Async repl         │  │        Audit logging        │   │
│   │        CloudIQ / SCG        │  │         FAST VP job         │  │        TLS mgmt plane       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    SP A/B active-passive → LUN or NAS Server → FAST VP moves data → async replication                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │      Layer       │      Block       │        File       │     Protocol     │      Notes       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │      Access      │     LUN / CG     │     NAS Server    │    FC / iSCSI    │    NFS / SMB     │   │
│   │     Snapshot     │     LUN snap     │      FS snap      │   NDMP backup    │   Per schedule   │   │
│   │   Replication    │  Async / Metro   │     Async NAS     │    FC / iSCSI    │   RPO minutes    │   │
│   │     Tiering      │     FAST VP      │      FAST VP      │   Flash/SAS/NL   │   Auto-policy    │   │
│                                                                                                       │
│    Physical: Unity chassis (2U base); expansion DAEs; dual SP blades; SPE/DPE drive enclosures        │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SP A / SP B    = Storage Processors; active-passive pair; SP A owns resources normally             │
│    FAST VP        = Fully Automated Storage Tiering for Virtual Pools; moves data by heat             │
│    NAS Server     = Virtual NAS container on Unity; has own IP, auth provider, shares/exports         │
│    CG             = Consistency Group; set of LUNs snapped/replicated together as a unit              │
│    Metro Volume   = Active-active sync replication between two Unity arrays; zero RPO                 │
│    uemcli         = Unity CLI tool; REST API-backed; uemcli /stor/prov/luns/lun -list                 │
│    Unisphere      = Web GUI for Unity management; login with AD or local admin credentials            │
│    DARE           = Data At Rest Encryption; SED drives with KMIP key management                      │
│    NL-SAS         = Near-Line SAS; high-capacity archive tier; lower IOPS than SAS                    │
│    NDMP           = Network Data Management Protocol; backup NAS data via NDMP client                 │
│    SPE            = Storage Processor Enclosure; base chassis containing SP A and SP B                │
│    DAE            = Disk Array Enclosure; expansion shelf for additional drives                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
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
