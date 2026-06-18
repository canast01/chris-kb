---
tags:
  - troubleshooting
  - powerscale
  - dell
  - known-issues
---
# Dell PowerScale (Isilon) — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known PowerScale / OneFS bugs, error codes, and workarounds covering NFS, SMB, SyncIQ, and cluster health.

*Applies to: OneFS 9.x*
</div>

```text
┌─────────────────────────────────────────── Dell PowerScale ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        PowerScale: scale-out NAS platform (Isilon) for unstructured and file workloads        │   │
│   │                     Protocols: NFS v3/v4.1 · SMB · HDFS · S3 · Swift · FTP                    │   │
│   │                               Management: OneFS WebUI / isi CLI                               │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │           Function          │   │
│   │              OS             │  │            OneFS            │  │        Distributed FS       │   │
│   │           Tiering           │  │          SmartPools         │  │        Auto data move       │   │
│   │         Replication         │  │            SyncIQ           │  │        Async DR copy        │   │
│   │          Snapshots          │  │          SnapshotIQ         │  │       Space-efficient       │   │
│   │         Load balance        │  │         SmartConnect        │  │       DNS client dist.      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │      OneFS       │ Distributed file │  NFS/SMB/S3/HDFS  │  Kerberos/NTLM   │ Single namespac  │   │
│   │    SmartPools    │  Tiering policy  │      Internal     │    Admin role    │  Auto data move  │   │
│   │      SyncIQ      │ Async replicatio │   Encrypted TCP   │   Certificate    │   Policy-based   │   │
│   │    SnapshotIQ    │    Snapshots     │      Internal     │    Admin role    │  Per directory   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: PowerScale nodes (All-Flash/Hybrid) · InfiniBand backend · 25/100 GbE frontend           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    OneFS              = Dell PowerScale distributed filesystem OS; all nodes share a single namespac  │
│    SmartPools         = tiering engine; moves files between All-Flash, Hybrid, and Archive tiers      │
│    SyncIQ             = async replication to DR cluster; RPO-based schedule; failover in minutes      │
│    SnapshotIQ         = space-efficient snapshots; accessed via .snapshot directory in each share     │
│    SmartConnect       = DNS-based load balancing; distributes NFS/SMB client connections across node  │
│    Access zone        = logical container with separate authentication and export namespace per tena  │
│    Quota              = directory or user quota; hard/soft/advisory limits enforced by OneFS QuotaIQ  │
│    CloudPools         = tiering to cloud object storage (S3/Blob); data remains accessible locally    │
│    isi CLI            = OneFS command-line interface; all management operations available via isi co  │
│    Node pool          = group of same-model nodes sharing protection domain for data distribution     │
│    Protection level   = N+2:1, N+3:1 etc.; defines how many node or drive failures are tolerated      │
│    File pool policy   = rule-based policy assigning files to specific node pools or storage tiers     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Run `isi status` from any node for overall cluster health.
- ECS (Error, Condition, Status) codes appear in `isi events list` — filter with `--severity critical`.
- SRS/ESRS phone-home should be active for proactive alerting.

## NFS

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| NFS mount shows `Permission denied` on valid path | OneFS 9.x | Export zone or client mapping not configured for client IP | Verify export zone in `isi nfs exports view`; add client IP to export access list | N/A |
| `Stale file handle` after cluster node removal | OneFS 9.x | SmartConnect DNS TTL cached old node IP | Flush DNS cache on client; set SmartConnect TTL to ≤10 seconds | N/A |
| NFSv4 ACL writes not preserved across NFS remount | OneFS 9.x | NFSv4 ACL support not enabled on export | Enable `security_flavors = krb5` on export and configure Kerberos, or use NFSv3 | N/A |

## SMB

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `The network path was not found` for SMB share | OneFS 9.x | SmartConnect zone not resolving to correct SIP | Verify SmartConnect zone DNS delegation; test with `nslookup <smartconnect-zone>` | N/A |
| Slow SMB enumeration for large directories | OneFS 9.x | Directory enumeration cache disabled | Enable `isi smb settings global modify --directory-cache-size=524288` | N/A |

## SyncIQ

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| SyncIQ job fails: `Target directory access denied` | OneFS 9.x | Source cluster SSH key not trusted by target | Re-add source SSH key to target: `isi sync target policies allow-write <job-name>` | N/A |
| SyncIQ lag growing after network change | OneFS 9.x | TCP 11111 or 7722 blocked between sites | Verify ports 11111/7722 open between SmartConnect management IPs | N/A |

## See also

- [Dell PowerScale — Common Issues](common-issues/)
- [Superna Eyeglass — Known Issues](../../../netapp/superna-eyeglass/troubleshooting/known-issues.md)
