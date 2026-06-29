---
tags:
  - ceph
  - learning-path
---
# Ceph Distributed Storage — Learning Path

<div class="kb-summary">
Recommended reading order for Ceph distributed storage. Follow these stages in order to build a complete mental model before working with it in production.

*Applies to: Red Hat Ceph Storage · Upstream Ceph*
</div>

```d2
direction: right

S1: "Architecture" {shape: rectangle}
S2: "Deploy" {shape: rectangle}
S3: "Operations" {shape: rectangle}
S4: "Security" {shape: rectangle}
S5: "Troubleshoot" {shape: rectangle}

S1 -> S2
S2 -> S3
S3 -> S4
S4 -> S5
```

## Stage 1 — Architecture

**Goal**: Understand RADOS as the foundation, how CRUSH maps data to OSDs, and how the three storage interfaces (RBD, CephFS, RGW) sit on top of it.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — RADOS object store, OSD (BlueStore on-disk format), MON quorum and cluster map, MGR active/standby roles, placement groups (PGs) and their replication pipeline
- [Design Standards](../architecture/design-standards/) — CRUSH rule design, failure domain selection (host/rack/DC), PG count formula, replication vs erasure coding trade-offs, and NVMe vs HDD OSD ratios
- [Integrations](../architecture/integrations/) — RBD for block (Kubernetes CSI, VM disks), CephFS for shared file (NFS-Ganesha gateway), RGW for S3/Swift object, and cephadm orchestration model

**Why first**: Ceph's CRUSH algorithm determines data placement and resilience. Operators who skip this stage misinterpret HEALTH_WARN states and make CRUSH rule changes that cause unnecessary rebalancing.

---

## Stage 2 — Deployment

**Goal**: Understand cephadm-based deployment, bootstrap sequence, and how to add OSDs and services to an existing cluster.

**Read**:

- [Deploy](../deploy/) — cephadm bootstrap, SSH key distribution, initial MON/MGR placement, OSD spec files, and enabling RBD/CephFS/RGW services
- [Install & Upgrade](../operations/install-upgrade/) — cephadm upgrade path, upgrading one daemon type at a time, monitoring upgrade progress with `ceph versions`, and rollback considerations

**Why second**: cephadm replaces ceph-deploy and ansible-based workflows. Understanding the orchestration model prevents manual daemon management that fights cephadm's reconciliation loop.

---

## Stage 3 — Operations

**Goal**: Maintain cluster health day-to-day — interpret health states, manage PG rebalancing, and protect data through snapshots and backup.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — run the routine first on every shift; covers `ceph status`, OSD in/out/up/down states, HEALTH_OK/WARN/ERR transitions, and PG stuck detection
- [CLI Reference](../operations/cli-reference/) — `ceph`, `rbd`, `radosgw-admin`, and `ceph fs` command reference for pool management, OSD operations, and quota enforcement
- [Procedures](../operations/procedures/) — OSD replacement workflow, reweight-by-utilization, pool creation and quota setting, RGW user management, and CephFS snapshot policies
- [Backup & Restore](../operations/backup-restore/) — RBD snapshot export, CephFS snapshot-based backup, RGW bucket replication, and point-in-time restore procedures
- [Scripts](../operations/scripts/) — automation for PG health polling, OSD utilisation reporting, and RGW bucket stats collection

**Why third**: PG rebalancing and OSD replacement are the most frequent operational tasks. Mishandling them — marking OSDs out prematurely or ignoring HEALTH_WARN — leads to data unavailability.

---

## Stage 4 — Security

**Goal**: Secure cluster communication with CephX authentication, enforce access controls per pool, and encrypt data at rest on OSDs.

**Read**:

- [Access Control](../security/access-control/) — CephX capability model, per-pool client key scoping, and MGR module permission restrictions
- [Authentication](../security/authentication/) — CephX key generation and rotation, RGW IAM user/bucket policies, and CephFS client authentication via MDS caps
- [Encryption](../security/encryption/) — BlueStore OSD-level encryption at rest (dm-crypt), RGW SSE-S3 and SSE-KMS, and in-transit TLS for messenger v2
- [Hardening](../security/hardening/) — network segmentation (public vs cluster network), MON bind address isolation, and disabling unused RGW endpoints

**Why fourth**: CephX is non-negotiable in production — an uncapped client key can wipe a pool. Understand the capability syntax before issuing keys to application teams.

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose HEALTH_WARN/ERR states, slow ops, and daemon crashes systematically before escalating.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — slow ops and blocked requests, full/nearfull OSDs, flapping MONs, PG inconsistency, and RGW 503 errors
- [Diagnostics](../troubleshooting/diagnostics/) — `ceph health detail`, OSD log analysis, `ceph osd perf`, PG query, and MON election trace interpretation
- [Escalation](../troubleshooting/escalation/) — Red Hat / Ceph upstream support, log collection (`ceph report`), and severity triage for data-at-risk states

**Why last**: Troubleshooting makes most sense once you know the normal operating state — what healthy PG counts look like, which HEALTH_WARN states are benign, and what slow op thresholds are expected.

---

## See also

- [Ceph — Deploy](../deploy/)
- [Ceph — Procedures](../operations/procedures/)
- [Ceph — Common Issues](../troubleshooting/common-issues/)
