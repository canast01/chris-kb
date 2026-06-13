---
tags:
  - operations
  - pure
---
# FlashBlade — Operations


<div class="kb-summary">
FlashBlade — Operations reference: Health Checks, Procedures, Common Issues, CLI Reference, and 3 more.
</div>
```text
┌──────────────────────────────────── Pure FlashBlade — Operations ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        FlashBlade operations: day-2 procedures for administration and maintenance tasks       │   │
│   │          Covers: provisioning, health checks, upgrades, backup/restore, and scripting         │   │
│   │           All operations require approved change tickets in production environments           │   │
│   │         Runbooks available for common tasks; escalation path defined for all incidents        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Open change → pre-check → execute procedure → verify → close                                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Blades           │  │           NVMe+CPU          │  │         Parallel I/O        │   │
│   │             File            │  │           NFS/SMB           │  │        Scale-out NAS        │   │
│   │            Object           │  │           S3/Swift          │  │         Bucket store        │   │
│   │         Replication         │  │            Async            │  │          DR/backup          │   │
│   │           SafeMode          │  │         Locked snaps        │  │      Ransomware resist      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │   File system    │  NAS namespace   │      NFS/SMB      │  Kerberos/NTLM   │   Up to 4 PiB    │   │
│   │  Object bucket   │   S3 namespace   │      S3/Swift     │   S3 keys/IAM    │    Versioning    │   │
│   │   Replication    │     Async DR     │   Encrypted TCP   │   Certificate    │  File or object  │   │
│   │     SafeMode     │ Locked snapshots │      Internal     │   Pure support   │    Immutable     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: FlashBlade//S or //E chassis · storage blades · 100 GbE network · Pure1 SaaS             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    FlashBlade         = Pure massively parallel all-flash NAS and object platform; single namespace   │
│    Blade              = individual storage module in FlashBlade chassis; NVMe and CPU per blade       │
│    File system        = FlashBlade NFS/SMB export namespace; up to 4 PiB per file system              │
│    Object store       = S3-compatible bucket store on FlashBlade; versioning and lifecycle rules      │
│    purefb CLI         = REST CLI client for FlashBlade: purefb fs list, purefb array show commands    │
│    Replication        = async file or object replication between FlashBlade systems for DR            │
│    SafeMode           = admin-locked snapshots; protected from deletion even by local array admin     │
│    S3 multitenancy    = per-bucket policy and IAM-style access control for object storage             │
│    NFS Kerberos       = FlashBlade NFS supports krb5, krb5i, and krb5p security flavours              │
│    SMB multichannel   = FlashBlade uses SMB multichannel for improved Windows client performance      │
│    Inline compression = always-on data reduction; typically 2-10x for unstructured data               │
│    ActiveScale        = enterprise geo-distribution and erasure coding for large object workloads     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


```text
FlashBlade Day-to-Day Operations
  Pure1 Cloud ──► fleet health + AI alerts + capacity forecast
          │
          ▼  phone-home telemetry
  FlashBlade (Purity//FB GUI / CLI / REST)
  ├── purefb alert list   ─── active alerts
  ├── purefb blade list   ─── blade health
  ├── purefb hardware list─── chassis / PSU / fans
  ├── purefb array list   ─── capacity + data reduction
  └── purefb replication  ─── ActiveDR relationship status
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="health-checks/"><strong>Health Checks</strong><span>Routine checks, service validation, and status verification.</span></a>
<a class="kb-card" href="procedures/"><strong>Procedures</strong><span>Day-to-day operational tasks and how-to guides.</span></a>
<a class="kb-card" href="common-issues/"><strong>Common Issues</strong><span>Quick reference for common problems and resolutions.</span></a>
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>Commands, syntax, and quick reference.</span></a>
<a class="kb-card" href="install-upgrade/"><strong>Install & Upgrade</strong><span>Installation, upgrade, patching, and decommission.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts and reusable code.</span></a>
<a class="kb-card" href="backup-restore/"><strong>Backup & Restore</strong><span>Backup configuration, restore procedures, and validation.</span></a>
</div>

