---
tags:
  - azure
---
# Azure Storage

<div class="kb-summary">
Azure Storage articles, operational checks, troubleshooting notes, and references.
</div>

```text
┌─────────────────────────────────────── Azure Storage Overview ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                Azure Storage — Blob, Managed Disks, Files, and Storage Accounts               │   │
│   │  Blob Storage: Hot / Cool / Cold / Archive access tiers; lifecycle management; immutable WORM │   │
│   │     Managed Disks: Premium SSD / Standard SSD / Ultra; ZRS for zone redundancy; snapshots     │   │
│   │  Azure Files: managed SMB and NFS shares; AD integration for Windows shares; Azure File Sync  │   │
│   │     Storage accounts: replication LRS/ZRS/GRS/GZRS; encryption at rest by default; private    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Blob serves objects · Managed Disks serve VM block I/O · Files serve shared mounts                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Blob Storage        │  │        Managed Disks        │  │         Azure Files         │   │
│   │     Hot: frequent access    │  │     Premium SSD: low lat    │  │      SMB 2.1/3.0 shares     │   │
│   │      Cool/Cold: infreq      │  │    Standard SSD: gen use    │  │        NFS 4.1: Linux       │   │
│   │    Archive: offline store   │  │       Ultra: 160K IOPS      │  │       AD auth: Windows      │   │
│   │    Lifecycle: tier rules    │  │     ZRS: zone redundant     │  │      File Sync: on-prem     │   │
│   │      Immutability: WORM     │  │    Snapshots: incremental   │  │      Backup: RSV policy     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Blob for unstructured objects · Managed Disks for VM boot/data · Files for shared SMB/NFS workloads│
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Blob Storage   │  Managed Disks   │    Azure Files    │  Storage Accts   │    Snapshots     │   │
│   │  Upload: AzCopy  │ Create: P10/P30  │    Create share   │   LRS/ZRS/GRS    │ Disk snap: incr  │   │
│   │ Lifecycle: rule  │   Attach to VM   │   Mount: Windows  │  Private endpt   │    Blob snap     │   │
│   │   Immutability   │ Expand: no stop  │    Mount: Linux   │    SAS token     │  Restore: snap   │   │
│   │  Tier: archive   │   ZRS: 3-zone    │     File Sync     │   CMK encrypt    │  Copy to region  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Azure Storage clusters (LRS/ZRS/GRS) · Managed Disk fabric per AZ · Storage account endpoints        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Storage account  = Top-level namespace for Blob, Files, Queue, Table; controls replication and access│
│  LRS              = Locally Redundant Storage; 3 copies in one data centre; cheapest option           │
│  ZRS              = Zone-Redundant Storage; 3 copies across 3 AZs; survives zone failure              │
│  GRS              = Geo-Redundant Storage; 6 copies across 2 regions; async replication to secondary  │
│  GZRS             = Geo-Zone-Redundant Storage; ZRS in primary + LRS in secondary region              │
│  Blob access tier  = Hot (frequent), Cool (infrequent), Cold (rare), Archive (offline); cost tiers    │
│  Lifecycle policy = Automatically transitions or deletes blobs based on age and last-modified date    │
│  Immutable storage= WORM policy on container; Legal hold or time-based; prevents delete/overwrite     │
│  Managed Disk     = Azure-managed block storage for VMs; types: Premium SSD, Standard SSD, Ultra      │
│  ZRS disk         = Zone-Redundant disk; synchronously replicates across 3 AZs; no AZ downtime impact │
│  Azure File Sync  = Syncs Azure Files share to on-premises Windows Server; cloud tiering option       │
│  SAS token        = Shared Access Signature; time-limited URL token for scoped blob/container access  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Articles

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="azure-files/">
  <strong>Azure Files</strong>
  <span>Managed SMB and NFS file shares mountable from Windows, Linux, and macOS.</span>
</a>

<a class="kb-card" href="blob-storage/">
  <strong>Blob Storage</strong>
  <span>Scalable object storage for unstructured data with hot, cool, cold, and archive tiers.</span>
</a>

<a class="kb-card" href="capacity/">
  <strong>Capacity</strong>
  <span>Storage account capacity monitoring, quota review, and growth trend analysis.</span>
</a>

<a class="kb-card" href="disk-snapshots/">
  <strong>Disk Snapshots</strong>
  <span>Point-in-time copies of managed disks for backup, DR, and golden image capture.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Server-side encryption with platform or customer-managed keys, and encryption at rest validation.</span>
</a>

<a class="kb-card" href="lifecycle-management/">
  <strong>Lifecycle Management</strong>
  <span>Automated blob tier transitions and deletion policies based on last access or creation date.</span>
</a>

<a class="kb-card" href="managed-disks/">
  <strong>Managed Disks</strong>
  <span>Azure-managed block storage for VMs including Premium SSD, Standard SSD, Ultra Disk, and HDD.</span>
</a>

<a class="kb-card" href="private-endpoints/">
  <strong>Private Endpoints</strong>
  <span>Private IP access to storage accounts within the VNet, eliminating public internet exposure.</span>
</a>

<a class="kb-card" href="storage-accounts/">
  <strong>Storage Accounts</strong>
  <span>Storage account creation, configuration, networking, and access key and SAS management.</span>
</a>
</div>
