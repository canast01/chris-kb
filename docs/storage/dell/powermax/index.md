# Dell PowerMax

<div class="kb-summary">
High-end all-flash enterprise array — SRDF synchronous and asynchronous replication, NVMe-oF, SnapVX snapshots, FAST VP tiering, and Solutions Enabler management for mission-critical block workloads.
</div>

```
┌────────────────────────────────── Dell PowerMax Enterprise Storage ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         PowerMax: Dell enterprise NVMe array; all-NVMe (2000) or NVMe+SAS (8000) tiers        │   │
│   │    SLO-based provisioning: Diamond/Platinum/Gold/Silver/Bronze maps workload to media tier    │   │
│   │           SRDF replication: Metro (active-active), Sync, Async, Adaptive Copy modes           │   │
│   │             Managed via Unisphere GUI and symcli (SYMAPI); REST API for automation            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Hosts connect via FA directors → SLO maps I/O to SRP tier → SRDF replicates to partner array       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       Director blades       │  │        Unisphere GUI        │  │       DARE encryption       │   │
│   │        SRP thin pools       │  │       symcli / SYMAPI       │  │        LDAP / AD auth       │   │
│   │          SLO tiers          │  │       TimeFinder snaps      │  │        Masking views        │   │
│   │        SRDF directors       │  │       SRDF replication      │  │        Audit logging        │   │
│   │       NVMe / SAS media      │  │           REST API          │  │       Host access ctrl      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Data path: host HBA → FA director port → SRP pool tier → DA director → NVMe/SAS drives             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Category     │  PowerMax 2000   │   PowerMax 8000   │     Protocol     │   Replication    │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │      Media       │     All-NVMe     │     NVMe + SAS    │    FC / FICON    │    SRDF/Metro    │   │
│   │     Capacity     │    Up to 4 PB    │    Up to 4 PB+    │      iSCSI       │    SRDF/Sync     │   │
│   │    Directors     │   6 directors    │    8+ directors   │     NVMe/FC      │    SRDF/Async    │   │
│   │       Tier       │    Mid-range     │      Flagship     │        —         │  Adaptive Copy   │   │
│                                                                                                       │
│    Physical: PowerMax chassis (2U/4U enclosure); director modules; NVMe/SAS bays; dual power          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SRP          = Storage Resource Pool; thin provisioning pool aligned to SLO tier                   │
│    SLO          = Service Level Objective; Diamond/Platinum/Gold/Silver/Bronze/Optimized              │
│    SRDF         = Symmetrix Remote Data Facility; block-level array-to-array replication              │
│    SRDF/Metro   = Active-active sync replication; both sites serve I/O simultaneously                 │
│    TimeFinder   = Local copy: /Snap (thin pointer), /Clone (full), /VP Snap (virtual)                 │
│    FA director  = Front-End Adapter; host-facing FC / iSCSI / NVMe-oF ports                           │
│    DA director  = Disk Adapter; back-end NVMe / SAS drive connectivity                                │
│    RDF director = Remote Data Facility; SRDF link ports between partner arrays                        │
│    DARE         = Data At Rest Encryption; self-encrypting drives managed by key server               │
│    Masking view = Host access control: storage group + port group + initiator group                   │
│    Unisphere    = Web-based management GUI for PowerMax; REST API surface                             │
│    symcli       = SYMAPI command-line toolkit: syminq, symsg, symdg, symrdf, symsnap                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────────── Dell PowerMax Enterprise Storage ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         PowerMax: Dell enterprise NVMe array; all-NVMe (2000) or NVMe+SAS (8000) tiers        │   │
│   │    SLO-based provisioning: Diamond/Platinum/Gold/Silver/Bronze maps workload to media tier    │   │
│   │           SRDF replication: Metro (active-active), Sync, Async, Adaptive Copy modes           │   │
│   │             Managed via Unisphere GUI and symcli (SYMAPI); REST API for automation            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Hosts connect via FA directors → SLO maps I/O to SRP tier → SRDF replicates to partner array       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       Director blades       │  │        Unisphere GUI        │  │       DARE encryption       │   │
│   │        SRP thin pools       │  │       symcli / SYMAPI       │  │        LDAP / AD auth       │   │
│   │          SLO tiers          │  │       TimeFinder snaps      │  │        Masking views        │   │
│   │        SRDF directors       │  │       SRDF replication      │  │        Audit logging        │   │
│   │       NVMe / SAS media      │  │           REST API          │  │       Host access ctrl      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Data path: host HBA → FA director port → SRP pool tier → DA director → NVMe/SAS drives             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Category     │  PowerMax 2000   │   PowerMax 8000   │     Protocol     │   Replication    │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │      Media       │     All-NVMe     │     NVMe + SAS    │    FC / FICON    │    SRDF/Metro    │   │
│   │     Capacity     │    Up to 4 PB    │    Up to 4 PB+    │      iSCSI       │    SRDF/Sync     │   │
│   │    Directors     │   6 directors    │    8+ directors   │     NVMe/FC      │    SRDF/Async    │   │
│   │       Tier       │    Mid-range     │      Flagship     │        —         │  Adaptive Copy   │   │
│                                                                                                       │
│    Physical: PowerMax chassis (2U/4U enclosure); director modules; NVMe/SAS bays; dual power          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SRP          = Storage Resource Pool; thin provisioning pool aligned to SLO tier                   │
│    SLO          = Service Level Objective; Diamond/Platinum/Gold/Silver/Bronze/Optimized              │
│    SRDF         = Symmetrix Remote Data Facility; block-level array-to-array replication              │
│    SRDF/Metro   = Active-active sync replication; both sites serve I/O simultaneously                 │
│    TimeFinder   = Local copy: /Snap (thin pointer), /Clone (full), /VP Snap (virtual)                 │
│    FA director  = Front-End Adapter; host-facing FC / iSCSI / NVMe-oF ports                           │
│    DA director  = Disk Adapter; back-end NVMe / SAS drive connectivity                                │
│    RDF director = Remote Data Facility; SRDF link ports between partner arrays                        │
│    DARE         = Data At Rest Encryption; self-encrypting drives managed by key server               │
│    Masking view = Host access control: storage group + port group + initiator group                   │
│    Unisphere    = Web-based management GUI for PowerMax; REST API surface                             │
│    symcli       = SYMAPI command-line toolkit: syminq, symsg, symdg, symrdf, symsnap                  │
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
