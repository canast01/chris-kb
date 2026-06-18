---
tags:
  - troubleshooting
  - storage
  - known-issues
---
# Storage — Known Issues Reference

<div class="kb-summary">
Index of storage product known issues and error codes. This top-level page links to per-product known-issues catalogs covering NetApp, Pure Storage, Dell storage, and Ceph.

*Applies to: All storage products in this KB*
</div>

```text
┌────────────────────────────────────── Storage Products Overview ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │            Enterprise storage platforms — block, file, object, and unified storage            │   │
│   │                    Protocols: FC · iSCSI · NFS · SMB · S3 · NVMe-oF · iSER                    │   │
│   │            Management: vendor web UI · REST API · CLI · ONTAP / PURITY / Unisphere            │   │
│   │             Host -> fabric/network -> storage array -> volume/share -> application            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Dell            │  │      PowerStore / Unity     │  │     Block + file unified    │   │
│   │            NetApp           │  │        ONTAP clusters       │  │        NAS + SAN + S3       │   │
│   │             Pure            │  │      FlashArray / Blade     │  │    All-flash + Evergreen    │   │
│   │             Ceph            │  │        RADOS cluster        │  │    Block/file/object OSS    │   │
│   │          Analytics          │  │       CloudIQ / Pure1       │  │      AI-driven insights     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │  Block storage   │   LUN / volume   │     FC / iSCSI    │   CHAP / zones   │ SCSI command set │   │
│   │   File storage   │    NAS share     │     NFS / SMB     │  Kerberos / AD   │POSIX permissions │   │
│   │  Object storage  │   Bucket / key   │     S3 / Swift    │    HMAC / IAM    │Eventual consist. │   │
│   │   Replication    │     DR copy      │   Array-specific  │   Array trust    │  Sync or async   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: host initiators -> SAN/LAN fabric -> storage controllers -> drive shelves                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  LUN          = Logical Unit Number; block storage volume presented to hosts                          │
│  RAID         = Redundant Array of Independent Disks; data protection across drives                   │
│  NVMe-oF      = NVMe over Fabrics; low-latency block storage over FC or RDMA                          │
│  ONTAP        = NetApp unified storage OS for NAS, SAN, and object                                    │
│  Purity       = Pure Storage OS running FlashArray and FlashBlade                                     │
│  Unisphere    = Dell EMC management UI for Unity and PowerStore arrays                                │
│  CloudIQ      = Dell AI-driven storage analytics and anomaly detection                                │
│  RADOS        = Reliable Autonomic Distributed Object Store; Ceph core layer                          │
│  RDO / ROOK   = Ceph deployment methods; bare-metal and Kubernetes respectively                       │
│  Thin provisioning = allocate capacity on demand, not upfront                                         │
│  Snapshot     = point-in-time copy of a volume; space-efficient via CoW                               │
│  Clone        = writable copy of a snapshot; independent of the source                                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

Storage issues often surface as application errors (I/O timeout, permission denied) — identify the protocol layer (NFS, iSCSI, FC, S3) before diving into array-specific known issues.

## Storage Product Known-Issues Pages

### NetApp

| Product | Known Issues |
|---|---|
| ONTAP | [ONTAP — Known Issues](netapp/ontap/troubleshooting/known-issues/) |
| SnapCenter | [SnapCenter — Known Issues](netapp/snapcenter/troubleshooting/known-issues/) |
| SnapMirror | [SnapMirror — Known Issues](netapp/snapmirror/troubleshooting/known-issues/) |
| InsightIQ | [InsightIQ — Known Issues](netapp/insightiq/troubleshooting/known-issues/) |
| Keystone | [Keystone — Known Issues](netapp/keystone/troubleshooting/known-issues/) |
| Superna Eyeglass | [Superna Eyeglass — Known Issues](netapp/superna-eyeglass/troubleshooting/known-issues/) |

### Pure Storage

| Product | Known Issues |
|---|---|
| FlashArray | [FlashArray — Known Issues](pure/flasharray/troubleshooting/known-issues/) |
| FlashBlade | [FlashBlade — Known Issues](pure/flashblade/troubleshooting/known-issues/) |
| Pure1 | [Pure1 — Known Issues](pure/pure1/troubleshooting/known-issues/) |

### Dell Storage

| Product | Known Issues |
|---|---|
| PowerStore | [PowerStore — Known Issues](dell/powerstore/troubleshooting/known-issues/) |
| PowerScale | [PowerScale — Known Issues](dell/powerscale/troubleshooting/known-issues/) |
| PowerMax | [PowerMax — Known Issues](dell/powermax/troubleshooting/known-issues/) |
| Data Domain | [Data Domain — Known Issues](dell/data-domain/troubleshooting/known-issues/) |
| Unity | [Unity — Known Issues](dell/unity/troubleshooting/known-issues/) |
| VPLEX | [VPLEX — Known Issues](dell/vplex/troubleshooting/known-issues/) |
| RecoverPoint | [RecoverPoint — Known Issues](dell/recoverpoint/troubleshooting/known-issues/) |

### Open Source

| Product | Known Issues |
|---|---|
| Ceph | [Ceph — Known Issues](ceph/troubleshooting/known-issues/) |

## See also

- [Storage — Common Issues](index.md)
