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

![Ceph Distributed Storage — Diagram](../../../assets/storage-ceph-diagram.svg)
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
