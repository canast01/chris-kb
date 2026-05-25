# PowerStore

<div class="kb-summary">
Mid-range all-flash platform with active-active dual-node appliance architecture — inline dedup/compression, Metro Volume zero-RPO sync replication, NVMe-oF, vVols, and AppsOn (X-series).
</div>

```
┌─────────────────────────────── Dell PowerStore Mid-Range NVMe Storage ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       PowerStore: Dell NVMe mid-range array; block (FC/iSCSI/NVMe-oF) and file (NFS/SMB)      │   │
│   │      Inline deduplication and compression; DARE encryption; CloudIQ via SCG for analytics     │   │
│   │           Replication: async native (volume groups); Metro Volume for zero-RPO sync           │   │
│   │               Managed via PowerStore Manager (REST API + web GUI) and pstcli CLI              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Host HBA/NIC → FC/iSCSI/NVMe-oF → PowerStore appliance → NVMe RAID → inline dedup/compress         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        NVMe appliance       │  │        PowerStore Mgr       │  │       DARE encryption       │   │
│   │         Block + File        │  │            pstcli           │  │        LDAP / AD auth       │   │
│   │         Inline dedup        │  │           REST API          │  │          RBAC roles         │   │
│   │         Metro Volume        │  │        Snap policies        │  │        Audit logging        │   │
│   │        CloudIQ / SCG        │  │          Async repl         │  │        TLS mgmt plane       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Host I/O → NVMe drives → inline dedup/compress → snapshot delta → async/sync replication           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Feature      │     T-series     │      X-series     │     Protocol     │      Notes       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │     Workload     │   Block + File   │     Block only    │    FC / iSCSI    │ NVMe/FC support  │   │
│   │    Efficiency    │   Dedup + comp   │    Dedup + comp   │    NFS / SMB     │ Inline always on │   │
│   │   Replication    │  Async + Metro   │   Async + Metro   │     NVMe/TCP     │  Zero-RPO Metro  │   │
│   │      Media       │     All-NVMe     │      All-NVMe     │        —         │  RAID 5 inline   │   │
│                                                                                                       │
│    Physical: PowerStore 500T/1000T/3000T appliance (2U); dual node cluster optional                   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Metro Volume   = Active-active sync replication between two PowerStore appliances; zero RPO        │
│    Inline dedup   = Deduplication at write time; data compared against existing blocks before write   │
│    Inline compress= Compression at write time; reduces media consumption without post-process lag     │
│    PowerStore Mgr = Web GUI and REST API management interface for PowerStore appliances               │
│    pstcli         = PowerStore CLI; connects to appliance REST API from admin workstation             │
│    DARE           = Data At Rest Encryption; SED drives with key management via KMIP                  │
│    CloudIQ        = Dell SaaS analytics platform; receives telemetry from PowerStore via SCG          │
│    SCG            = Secure Connect Gateway; phone-home proxy for CloudIQ telemetry upload             │
│    Async repl     = Volume group replication to remote PowerStore; configurable RPO schedule          │
│    NVMe/FC        = NVMe over Fibre Channel; lower latency than iSCSI for NVMe-native hosts           │
│    NVMe/TCP       = NVMe over TCP/IP; enables NVMe performance over standard Ethernet                 │
│    RAID 5 inline  = NVMe RAID calculated inline on write; no separate RAID rebuild after failure      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌─────────────────────────────── Dell PowerStore Mid-Range NVMe Storage ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       PowerStore: Dell NVMe mid-range array; block (FC/iSCSI/NVMe-oF) and file (NFS/SMB)      │   │
│   │      Inline deduplication and compression; DARE encryption; CloudIQ via SCG for analytics     │   │
│   │           Replication: async native (volume groups); Metro Volume for zero-RPO sync           │   │
│   │               Managed via PowerStore Manager (REST API + web GUI) and pstcli CLI              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Host HBA/NIC → FC/iSCSI/NVMe-oF → PowerStore appliance → NVMe RAID → inline dedup/compress         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        NVMe appliance       │  │        PowerStore Mgr       │  │       DARE encryption       │   │
│   │         Block + File        │  │            pstcli           │  │        LDAP / AD auth       │   │
│   │         Inline dedup        │  │           REST API          │  │          RBAC roles         │   │
│   │         Metro Volume        │  │        Snap policies        │  │        Audit logging        │   │
│   │        CloudIQ / SCG        │  │          Async repl         │  │        TLS mgmt plane       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Host I/O → NVMe drives → inline dedup/compress → snapshot delta → async/sync replication           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Feature      │     T-series     │      X-series     │     Protocol     │      Notes       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │     Workload     │   Block + File   │     Block only    │    FC / iSCSI    │ NVMe/FC support  │   │
│   │    Efficiency    │   Dedup + comp   │    Dedup + comp   │    NFS / SMB     │ Inline always on │   │
│   │   Replication    │  Async + Metro   │   Async + Metro   │     NVMe/TCP     │  Zero-RPO Metro  │   │
│   │      Media       │     All-NVMe     │      All-NVMe     │        —         │  RAID 5 inline   │   │
│                                                                                                       │
│    Physical: PowerStore 500T/1000T/3000T appliance (2U); dual node cluster optional                   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Metro Volume   = Active-active sync replication between two PowerStore appliances; zero RPO        │
│    Inline dedup   = Deduplication at write time; data compared against existing blocks before write   │
│    Inline compress= Compression at write time; reduces media consumption without post-process lag     │
│    PowerStore Mgr = Web GUI and REST API management interface for PowerStore appliances               │
│    pstcli         = PowerStore CLI; connects to appliance REST API from admin workstation             │
│    DARE           = Data At Rest Encryption; SED drives with key management via KMIP                  │
│    CloudIQ        = Dell SaaS analytics platform; receives telemetry from PowerStore via SCG          │
│    SCG            = Secure Connect Gateway; phone-home proxy for CloudIQ telemetry upload             │
│    Async repl     = Volume group replication to remote PowerStore; configurable RPO schedule          │
│    NVMe/FC        = NVMe over Fibre Channel; lower latency than iSCSI for NVMe-native hosts           │
│    NVMe/TCP       = NVMe over TCP/IP; enables NVMe performance over standard Ethernet                 │
│    RAID 5 inline  = NVMe RAID calculated inline on write; no separate RAID rebuild after failure      │
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
