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
![Storage — Known Issues Reference](../../assets/storage-troubleshooting-known-issues.svg)





```d2
direction: down

symptom: Identify Symptom {shape: diamond}
storage_product_knownissues_pages: "Storage Product Known-Issues Pages" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> storage_product_knownissues_pages: investigate
storage_product_knownissues_pages -> resolution
```

## Before you begin

Storage issues often surface as application errors (I/O timeout, permission denied) — identify the protocol layer (NFS, iSCSI, FC, S3) before diving into array-specific known issues.

## Storage Product Known-Issues Pages

### NetApp

| Product | Known Issues |
|---|---|
| ONTAP | [ONTAP — Known Issues](../../netapp/ontap/troubleshooting/known-issues/) |
| SnapCenter | [SnapCenter — Known Issues](../../netapp/snapcenter/troubleshooting/known-issues/) |
| SnapMirror | [SnapMirror — Known Issues](../../netapp/snapmirror/troubleshooting/known-issues/) |
| InsightIQ | [InsightIQ — Known Issues](../../netapp/insightiq/troubleshooting/known-issues/) |
| Keystone | [Keystone — Known Issues](../../netapp/keystone/troubleshooting/known-issues/) |
| Superna Eyeglass | [Superna Eyeglass — Known Issues](../../netapp/superna-eyeglass/troubleshooting/known-issues/) |

### Pure Storage

| Product | Known Issues |
|---|---|
| FlashArray | [FlashArray — Known Issues](../../pure/flasharray/troubleshooting/known-issues/) |
| FlashBlade | [FlashBlade — Known Issues](../../pure/flashblade/troubleshooting/known-issues/) |
| Pure1 | [Pure1 — Known Issues](../../pure/pure1/troubleshooting/known-issues/) |

### Dell Storage

| Product | Known Issues |
|---|---|
| PowerStore | [PowerStore — Known Issues](../../dell/powerstore/troubleshooting/known-issues/) |
| PowerScale | [PowerScale — Known Issues](../../dell/powerscale/troubleshooting/known-issues/) |
| PowerMax | [PowerMax — Known Issues](../../dell/powermax/troubleshooting/known-issues/) |
| Data Domain | [Data Domain — Known Issues](../../dell/data-domain/troubleshooting/known-issues/) |
| Unity | [Unity — Known Issues](../../dell/unity/troubleshooting/known-issues/) |
| VPLEX | [VPLEX — Known Issues](../../dell/vplex/troubleshooting/known-issues/) |
| RecoverPoint | [RecoverPoint — Known Issues](../../dell/recoverpoint/troubleshooting/known-issues/) |

### Open Source

| Product | Known Issues |
|---|---|
| Ceph | [Ceph — Known Issues](../../ceph/troubleshooting/known-issues/) |

## See also

- [Storage — Common Issues](index.md)
