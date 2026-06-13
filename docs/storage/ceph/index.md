---
tags:
  - ceph
---
# Ceph Distributed Storage

<!-- diagram:ceph -->

<div class="kb-summary">
Ceph is an open-source distributed storage system providing block (RBD), file (CephFS), and object (RGW/S3) storage from a single cluster. Deployed on commodity hardware with no single point of failure.

*Applies to: Red Hat Ceph Storage · Upstream Ceph*
</div>

```text
┌────────────────────────────────────── Ceph Distributed Storage ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                         Ceph — Open-source Distributed Storage System                         │   │
│   │           Provides block (RBD), file (CephFS), and object (RGW/S3) from one cluster           │   │
│   │         RADOS: object store engine; CRUSH: placement algorithm without metadata server        │   │
│   │           OSD: 1 per disk; MON: 3-5 for quorum; MGR: 2 for orchestration + dashboard          │   │
│   │              Replication: N copies (replica pool) or erasure coding (k+m chunks)              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                 ▼                               ▼                                 ▼                   │
│                                                                                                       │
│   ┌────────────────────────────┐  ┌────────────────────────────┐  ┌───────────────────────────────┐   │
│   │        Block (RBD)         │  │       File (CephFS)        │  │          Object (RGW)         │   │
│   │       Thin-prov images     │  │       POSIX filesystem     │  │       S3/Swift compatible     │   │
│   │      Snapshots + clones    │  │      MDS for namespace     │  │       radosgw-admin users     │   │
│   │     K8s CSI / OpenStack    │  │      NFS-Ganesha export    │  │      Bucket lifecycle/quota   │   │
│   └────────────────────────────┘  └────────────────────────────┘  └───────────────────────────────┘   │
│                                                                                                       │
│                  │                             │                   │                   │              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 RADOS Layer                  │  │                 Daemon Layer                │   │
│   │            Object store (all pools)          │  │                OSD: 1 per disk              │   │
│   │              CRUSH placement algo            │  │            MON: cluster map quorum          │   │
│   │               PG replication/EC              │  │          MGR: metrics + orchestration       │   │
│   │             Self-healing recovery            │  │            cephadm: container mgmt          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│    RADOS   = Reliable Autonomic Distributed Object Store; storage engine for all Ceph services        │
│    OSD     = Object Storage Daemon; one per disk; stores data + handles replication/recovery          │
│    CRUSH   = Controlled Replication Under Scalable Hashing; placement algorithm (no lookup)           │
│    PG      = Placement Group; unit of replication; ~100 per OSD; maps to set of OSDs                  │
│    BlueStore= Default OSD backend; raw block device; superior to older FileStore/XFS                  │
│                                                                                                       │
```
<div class="kb-grid">
  <a class="kb-card" href="architecture/">
    <span class="kb-card-title">Architecture</span>
    <span class="kb-card-desc">RADOS, OSD/MON/MGR/MDS daemons, CRUSH map, replication and erasure coding</span>
  </a>
  <a class="kb-card" href="deploy/">
    <span class="kb-card-title">Deploy</span>
    <span class="kb-card-desc">cephadm bootstrap, OSD provisioning, pool creation, day-0 checklist</span>
  </a>
  <a class="kb-card" href="operations/">
    <span class="kb-card-title">Operations</span>
    <span class="kb-card-desc">Cluster health, OSD management, CRUSH tuning, RBD/RGW/CephFS admin</span>
  </a>
  <a class="kb-card" href="security/">
    <span class="kb-card-title">Security</span>
    <span class="kb-card-desc">CephX authentication, RBAC, encryption at rest, TLS for RGW</span>
  </a>
  <a class="kb-card" href="troubleshooting/">
    <span class="kb-card-title">Troubleshooting</span>
    <span class="kb-card-desc">OSD down, PG degraded, slow requests, full cluster, and escalation</span>
  </a>
</div>
