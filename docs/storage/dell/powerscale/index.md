# Dell PowerScale

<div class="kb-summary">
Scale-out NAS platform running OneFS — multi-protocol access (NFS, SMB, S3, HDFS), SmartQuotas, SyncIQ replication, SmartPools tiering, and cluster-wide management for unstructured data at scale.
</div>

```
┌─────────────────────────────── Dell PowerScale (Isilon) Scale-Out NAS ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        PowerScale: Dell scale-out NAS cluster; OneFS distributed OS across 3–252 nodes        │   │
│   │       Protocols: NFS v3/v4.1, SMB 2/3, S3, HDFS, FTP; single namespace across all nodes       │   │
│   │  SmartPools: automated data tiering; H-series (hybrid), F-series (flash), A-series (archive)  │   │
│   │           Replication via SyncIQ (async to remote cluster); snapshots via SnapshotIQ          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Client → SmartConnect DNS LB → node NFS/SMB → OneFS namespace → SmartPool tier → drives            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        OneFS cluster        │  │           isi CLI           │  │         Access zones        │   │
│   │          Node pools         │  │        isi statistics       │  │       AD / LDAP / KRB       │   │
│   │       SmartPools tiers      │  │         SyncIQ jobs         │  │        SmartLock WORM       │   │
│   │         SmartConnect        │  │          SnapshotIQ         │  │         RBAC / roles        │   │
│   │         FlexProtect         │  │         SmartQuotas         │  │        Audit logging        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Client I/O → node → OneFS journal → data written to drives → SmartPool migrates tier               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Feature      │     H-series     │      F-series     │     A-series     │      Notes       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │      Media       │    SSD + SAS     │    All-NVMe/SSD   │    SAS + SATA    │    Node type     │   │
│   │     Use case     │  Mixed workload  │   High perf NAS   │   Archive/cold   │ Tiered by SmartP │   │
│   │   Cluster min    │     3 nodes      │      3 nodes      │     3 nodes      │  Max 252 nodes   │   │
│   │     Protocol     │    NFS/SMB/S3    │     NFS/SMB/S3    │    NFS/SMB/S3    │  All in one NS   │   │
│                                                                                                       │
│    Physical: nodes in rack; InfiniBand or 25/100GbE back-end; front-end Ethernet for clients          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    OneFS          = PowerScale distributed OS; runs identically on all cluster nodes                  │
│    SmartPools     = Automated tiering across node pools; moves data by file policy and age            │
│    SmartConnect   = DNS round-robin or zone-based client connection balancing across nodes            │
│    SyncIQ         = Async replication to remote PowerScale cluster; policy-driven schedules           │
│    SnapshotIQ     = Local read-only snapshots; accessible via .snapshot directory                     │
│    SmartQuotas    = Directory/user/group capacity quotas; hard and advisory thresholds                │
│    FlexProtect    = Dynamic N+M data protection; rebalances after node failure automatically          │
│    Access zone    = Isolated namespace with own auth providers, IP pools, and share policies          │
│    SmartLock      = WORM compliance (cannot delete/modify files during retention period)              │
│    isi            = OneFS CLI tool; isi status, isi statistics, isi sync, isi quota                   │
│    InsightIQ      = Analytics platform for PowerScale performance reporting                           │
│    InfiniBand BE  = Back-end node interconnect for metadata and data traffic within cluster           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌─────────────────────────────── Dell PowerScale (Isilon) Scale-Out NAS ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        PowerScale: Dell scale-out NAS cluster; OneFS distributed OS across 3–252 nodes        │   │
│   │       Protocols: NFS v3/v4.1, SMB 2/3, S3, HDFS, FTP; single namespace across all nodes       │   │
│   │  SmartPools: automated data tiering; H-series (hybrid), F-series (flash), A-series (archive)  │   │
│   │           Replication via SyncIQ (async to remote cluster); snapshots via SnapshotIQ          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Client → SmartConnect DNS LB → node NFS/SMB → OneFS namespace → SmartPool tier → drives            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        OneFS cluster        │  │           isi CLI           │  │         Access zones        │   │
│   │          Node pools         │  │        isi statistics       │  │       AD / LDAP / KRB       │   │
│   │       SmartPools tiers      │  │         SyncIQ jobs         │  │        SmartLock WORM       │   │
│   │         SmartConnect        │  │          SnapshotIQ         │  │         RBAC / roles        │   │
│   │         FlexProtect         │  │         SmartQuotas         │  │        Audit logging        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Client I/O → node → OneFS journal → data written to drives → SmartPool migrates tier               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Feature      │     H-series     │      F-series     │     A-series     │      Notes       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │      Media       │    SSD + SAS     │    All-NVMe/SSD   │    SAS + SATA    │    Node type     │   │
│   │     Use case     │  Mixed workload  │   High perf NAS   │   Archive/cold   │ Tiered by SmartP │   │
│   │   Cluster min    │     3 nodes      │      3 nodes      │     3 nodes      │  Max 252 nodes   │   │
│   │     Protocol     │    NFS/SMB/S3    │     NFS/SMB/S3    │    NFS/SMB/S3    │  All in one NS   │   │
│                                                                                                       │
│    Physical: nodes in rack; InfiniBand or 25/100GbE back-end; front-end Ethernet for clients          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    OneFS          = PowerScale distributed OS; runs identically on all cluster nodes                  │
│    SmartPools     = Automated tiering across node pools; moves data by file policy and age            │
│    SmartConnect   = DNS round-robin or zone-based client connection balancing across nodes            │
│    SyncIQ         = Async replication to remote PowerScale cluster; policy-driven schedules           │
│    SnapshotIQ     = Local read-only snapshots; accessible via .snapshot directory                     │
│    SmartQuotas    = Directory/user/group capacity quotas; hard and advisory thresholds                │
│    FlexProtect    = Dynamic N+M data protection; rebalances after node failure automatically          │
│    Access zone    = Isolated namespace with own auth providers, IP pools, and share policies          │
│    SmartLock      = WORM compliance (cannot delete/modify files during retention period)              │
│    isi            = OneFS CLI tool; isi status, isi statistics, isi sync, isi quota                   │
│    InsightIQ      = Analytics platform for PowerScale performance reporting                           │
│    InfiniBand BE  = Back-end node interconnect for metadata and data traffic within cluster           │
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
