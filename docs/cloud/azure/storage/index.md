# Azure Storage

<div class="kb-summary">
Azure Storage articles, operational checks, troubleshooting notes, and references.
</div>

```
┌──────────────────────────────────────────────────────────────────┐
│                     Azure Storage Services                        │
├──────────────────────────────────────────────────────────────────┤
│  ┌───────────┐ ┌───────────┐ ┌──────────┐ ┌──────────────────┐   │
│  │   Blob    │ │  Files    │ │  Queues  │ │  Tables          │   │
│  │ (objects) │ │(SMB/NFS)  │ │(messages)│ │ (NoSQL k-v)      │   │
│  └───────────┘ └───────────┘ └──────────┘ └──────────────────┘   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    Managed Disk                             │ │
│  │        Premium SSD │ Standard SSD │ Ultra │ HDD             │ │
│  └─────────────────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────┤
│  Redundancy:  LRS ──► ZRS ──► GRS ──► GZRS  (ascending cost)     │
├──────────────────────────────────────────────────────────────────┤
│  Access:  Public endpoint │ Service Endpoint │ Private Endpoint  │
└──────────────────────────────────────────────────────────────────┘
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
