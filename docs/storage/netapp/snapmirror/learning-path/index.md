# NetApp SnapMirror — Learning Path

<div class="kb-summary">
Recommended reading order for NetApp SnapMirror. Follow these stages in order to build a complete mental model before working with it in production.
</div>

```mermaid
graph LR
  S1[Architecture] --> S2[Deploy] --> S3[Operations] --> S4[Security] --> S5[Troubleshoot]
  classDef stage fill:#1e3a5f,stroke:#2563eb,color:#fff
  class S1,S2,S3,S4,S5 stage
```

## Stage 1 — Architecture

**Goal**: Understand the SnapMirror relationship model, transfer mechanics, and the difference between DP (data protection) and XDP (extended data protection) before configuring any replication.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — DP vs XDP relationship types, schedule-based vs policy-based replication, transfer snapshots, baseline and incremental transfers
- [Design Standards](../architecture/design-standards/) — Peering prerequisites, intercluster LIF placement, RPO/RTO mapping to SnapMirror policies, fan-out and cascade topologies
- [Integrations](../architecture/integrations/) — SnapMirror to Cloud (SMTC) for object store targets, SVM-DR for entire SVM failover, SnapVault integration for long-term retention

**Why first**: SnapMirror relationships depend on cluster-peer and SVM-peer trust established at design time; understanding these before deployment prevents common misconfiguration.

---

## Stage 2 — Deployment

**Goal**: Initialize SnapMirror relationships correctly and validate baseline transfer completion.

**Read**:

- [Install & Upgrade](../operations/install-upgrade/) — Cluster peering, SVM peering, intercluster LIF creation, SnapMirror license verification
- [Deploy](../deploy/) — Relationship creation (`snapmirror create`), initialize, schedule assignment, policy selection (MirrorAllSnapshots, MirrorLatest, XDPDefault)

**Why second**: Proper peering and LIF design at deployment avoids split-brain scenarios during failover.

---

## Stage 3 — Operations

**Goal**: Manage the full SnapMirror relationship lifecycle — update, resync, break, reverse resync — and monitor replication lag.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — Run the routine first on every shift; check relationship state, last transfer time, lag duration, and transfer errors
- [CLI Reference](../operations/cli-reference/) — `snapmirror show`, `snapmirror update`, `snapmirror break`, `snapmirror resync`, `snapmirror reverse-resync` command reference
- [Procedures](../operations/procedures/) — Planned failover sequence, unplanned failover recovery, re-establish after DR test, SMTC restore from object store
- [Backup & Restore](../operations/backup-restore/) — SnapVault restore path from secondary, restoring a specific labeled snapshot, NAS file-level restore from vault
- [Scripts](../operations/scripts/) — Lag monitoring scripts, bulk relationship status, scheduled update verification

---

## Stage 4 — Security

**Goal**: Secure replication traffic and enforce access controls on replication management.

**Read**:

- [Access Control](../security/access-control/) — Restricting `snapmirror` command set to dedicated replication accounts; SVM-scoped vs cluster-level permissions
- [Authentication](../security/authentication/) — Certificate-based cluster peering (SSL), intercluster LIF firewall rules, peer authentication validation
- [Encryption](../security/encryption/) — SnapMirror traffic encryption (TLS 1.2+), encryption policy on XDP relationships, KMIP integration for encrypted volumes
- [Hardening](../security/hardening/) — Restrict peering to known intercluster IPs, audit relationship changes, alert on unexpected break or resync

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose stalled transfers, broken relationships, and failed failover operations.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — Transfer stuck in progress, relationship in broken-off state, lag exceeding RPO threshold, initialize failure on large volumes
- [Diagnostics](../troubleshooting/diagnostics/) — `snapmirror show -fields transfer-error`, EMS events for msid mismatch, intercluster connectivity tests, `network ping-cluster`
- [Escalation](../troubleshooting/escalation/) — NetApp support case for persistent transfer errors, AutoSupport bundle from both source and destination cluster

**Why last**: Troubleshooting SnapMirror failures requires knowing the expected relationship state and transfer sequence — both covered in earlier stages.
