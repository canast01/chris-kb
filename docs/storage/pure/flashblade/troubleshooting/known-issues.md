---
tags:
  - troubleshooting
  - flashblade
  - pure-storage
  - known-issues
---
# Pure Storage FlashBlade — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known FlashBlade bugs, error codes, and workarounds covering NFS, SMB, S3, and array health.

*Applies to: Purity//FB 4.x*
</div>

```text
┌─────────────────────────────────────────── Pure FlashBlade ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │            FlashBlade: massively parallel all-flash NAS and object storage platform           │   │
│   │                      Protocols: NFS v3/v4.1 · SMB · S3 · Swift · REST API                     │   │
│   │                            Management: Purity//FB GUI / purefb CLI                            │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
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


## Before you begin

- FlashBlade alerts appear in the web UI under `Health → Alerts`.
- NFS and SMB issues are often permission or mount option mismatches — verify before assuming a bug.
- Pure1 phone-home must be active for proactive support.

## NFS

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| NFS mount succeeds but read/write returns `Permission denied` | Purity FB 4.x | Export policy does not match client IP | Verify export policy client match in FlashBlade web UI → File Systems → Export | N/A |
| NFS client shows `Stale NFS file handle` after FlashBlade upgrade | Purity FB 4.x | NFS session interrupted during upgrade | Remount NFS share after upgrade completes | N/A |
| NFSv4.1 `GETATTR` errors on large directories | Purity FB 4.x | Client-side ACL cache inconsistency | Mount with `actimeo=0` to disable client caching; or use NFSv3 for legacy workloads | N/A |

## S3 Object

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| S3 `403 Forbidden` despite valid credentials | Purity FB 4.x | Bucket policy or IAM policy denying access | Review bucket ACL and access keys in FlashBlade → Object Store → Accounts | N/A |
| S3 multipart upload failing: `Upload ID not found` | Purity FB 4.x | Multipart upload timeout (default 168h) | Increase multipart expiry or complete/abort all pending multipart uploads | N/A |

## Array Health

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Blade failed` alert — client I/O still working | Purity FB 4.x | Single blade failed; FlashBlade automatically redistributed data | Array continues serving I/O; replace blade via Pure support RMA | N/A |
| `Pure1 not receiving data` | Purity FB 4.x | Outbound 443 to pure1.purestorage.com blocked | Verify firewall allows TCP 443 from FlashBlade management IP | N/A |

## See also

- [Pure Storage FlashBlade — Common Issues](common-issues/)
- [Pure Storage FlashArray — Known Issues](../../flasharray/troubleshooting/known-issues.md)
