---
tags:
  - troubleshooting
  - ecs
  - dell
  - known-issues
---
# Dell ECS — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known ECS (Elastic Cloud Storage) bugs, error codes, and workarounds covering S3 API, geo-replication, and cluster health.

*Applies to: ECS 3.x*
</div>

```text
┌────────────────────────────────────────────── Dell ECS ───────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │              ECS: Elastic Cloud Storage enterprise S3-compatible object platform              │   │
│   │           Protocols: S3 · Azure Blob API · Swift · Atmos · NFS (via gateway) · HDFS           │   │
│   │                          Management: ECS Management Portal / REST API                         │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Node            │  │        x86 appliance        │  │        Shared-nothing       │   │
│   │         Storage pool        │  │          Node group         │  │        Erasure coded        │   │
│   │             VDC             │  │          Virtual DC         │  │        Per-site unit        │   │
│   │          Rep. group         │  │          Multi-VDC          │  │        Geo redundancy       │   │
│   │            Bucket           │  │       Object container      │  │        S3/Swift/Blob        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │   Storage pool   │ Drive aggregatio │      Internal     │       N/A        │   Erasure 12+4   │   │
│   │       VDC        │  Site grouping   │      Internal     │       N/A        │   HA per site    │   │
│   │      Bucket      │ Object namespace │   S3/Swift/Blob   │   S3 keys/IAM    │    Per tenant    │   │
│   │ Replication grp  │ Geo replication  │    ECS protocol   │   Certificate    │    3-way geo     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: ECS appliance nodes · 10/25 GbE backend network · commodity SAS drives                   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    ECS                = Elastic Cloud Storage; Dell S3-compatible object store for unstructured data  │
│    VDC                = Virtual Data Center; group of ECS nodes at a single geographic site           │
│    Storage pool       = collection of nodes within a VDC; defines the erasure coding domain           │
│    Replication group  = links VDCs for geo-redundant object storage; 3-way replication                │
│    Bucket             = top-level S3 namespace; equivalent to S3 bucket or Azure container            │
│    Erasure coding     = data protection scheme; default 12+4 provides 4-drive fault tolerance         │
│    Namespace          = tenant-level isolation; multiple tenants share a single ECS cluster           │
│    CAS                = Content Addressed Storage; fixed-content object storage with WORM support     │
│    Replication factor = number of VDC copies; 3-way geo-replication for maximum durability            │
│    Atmos API          = legacy Dell Atmos-compatible API; supported for migration from Atmos systems  │
│    HDFS connector     = ECS Hadoop connector; ECS appears as HDFS namespace for analytics jobs        │
│    Quota              = per-namespace or per-bucket storage quota; enforced as hard or soft limit     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- ECS alerts appear in ECS Portal → Dashboard → Alerts.
- `ecscli` for cluster management; `managementAPI` on port 9101 for REST API.
- Geo-replication issues always involve port 9011 between sites.

## S3 API

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| S3 `403 Forbidden` for valid credentials | ECS 3.x | User not in correct S3 object user group or namespace | Verify user namespace mapping in ECS Portal → Manage → Users | N/A |
| S3 multipart upload returning `400 Bad Request` | ECS 3.x | Part size below ECS minimum (5 MB for all except last part) | Ensure all parts except last are ≥5 MB | N/A |
| `404 NoSuchBucket` immediately after bucket create | ECS 3.x | Consistency delay on new bucket; client retried too fast | Retry S3 operation after 1–2 seconds; ECS has eventual consistency for metadata | N/A |

## Geo-Replication

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Geo-replication `Link Down` | ECS 3.x | TCP 9011 blocked between ECS sites | Verify TCP 9011 open between all ECS nodes across sites | N/A |
| Replication lag growing after network event | ECS 3.x | Backlog built up during outage | Lag clears automatically after connectivity restored; no manual action required | N/A |

## Cluster Health

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Disk failed` alert — cluster healthy | ECS 3.x | Single disk failure; ECS re-protecting data | Replace disk; no data loss as long as cluster has sufficient nodes online | N/A |
| ZooKeeper quorum lost: `Cassandra not available` | ECS 3.x | Multiple nodes offline simultaneously | Restore node count to ≥3 in ZooKeeper quorum; check Cassandra ring | N/A |

## See also

- [Dell ECS — Common Issues](common-issues.md)
- [Dell CloudIQ — Known Issues](../../cloudiq/troubleshooting/known-issues/)
