# Dell PowerScale (Isilon) — Learning Path

<div class="kb-summary">
Recommended reading order for Dell PowerScale. Follow these stages in order to build a complete mental model before working with it in production.
</div>

```text
┌───────────────────────────────────── PowerScale — Learning Path ──────────────────────────────────────┐
│                                                                                                       │
│    5 stages in order: Architecture → Deploy → Operations → Security → Troubleshoot                    │
│                                                                                                       │
│   ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐  ┌────────────────┐  ┌────────────────┐ │
│   │  Architecture  │  │     Deploy     │  │    Operations   │  │    Security    │  │  Troubleshoot  │ │
│   │                │  │                │  │                 │  │                │  │                │ │
│   │  How It Works  │  │ Initial Setup  │  │  Health Checks  │  │ Access Control │  │ Common Issues  │ │
│   │Design Standards│  │Install/Upgrade │  │  CLI Reference  │  │ Authentication │  │  Diagnostics   │ │
│   │  Integrations  │  │                │  │    Procedures   │  │   Encryption   │  │   Escalation   │ │
│   │                │  │                │  │ Backup & Restore│  │   Hardening    │  │                │ │
│   │                │  │                │  │     Scripts     │  │                │  │                │ │
│   └────────────────┘  └────────────────┘  └─────────────────┘  └────────────────┘  └────────────────┘ │
│                                                                                                       │
│    Stage 1 (Architecture) builds understanding. Stage 3 (Operations) is daily work. Troubleshoot last.│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```mermaid
graph LR
  S1[Architecture] --> S2[Deploy] --> S3[Operations] --> S4[Security] --> S5[Troubleshoot]
  classDef stage fill:#1e3a5f,stroke:#2563eb,color:#fff
  class S1,S2,S3,S4,S5 stage
```
## Stage 1 — Architecture
**Goal**: Understand how OneFS distributes data and metadata across a cluster of nodes, and how the file system scales linearly without traditional RAID controllers.

**Read in this order**:
- [How It Works](../architecture/how-it-works/) — OneFS clustered OS: distributed file system, FlexProtect (erasure coding), node roles (H-series, F-series, A-series), internal network (InfiniBand/Ethernet), and how reads and writes span the cluster.
- [Design Standards](../architecture/design-standards/) — Node pool design, SmartPools tiering policies, protection levels (N+1 to N+3:1), SmartQuotas capacity planning, and S3 bucket hierarchy.
- [Integrations](../architecture/integrations/) — NFS, SMB, HDFS, S3 protocol stacks, SyncIQ replication topology, InsightIQ performance analytics, and VMware vSphere integration.

**Why first**: OneFS behaves fundamentally differently from traditional NAS. Understanding distributed writes and FlexProtect prevents catastrophic node removal mistakes.

---

## Stage 2 — Deployment
**Goal**: Add nodes to a cluster, configure access zones, and present storage to first clients.

**Read**:
- [Deploy](../deploy/) — Cluster join, network configuration (groupnets, subnets, IP pools), access zone creation, authentication provider setup, and first export or share.
- [Install & Upgrade](../operations/install-upgrade/) — OneFS rolling upgrade procedure, node addition, firmware updates, and upgrade readiness checks.

**Why second**: Access zone and authentication provider configuration at deploy time defines how clients access data. Changing this post-deploy affects all connected clients.

---

## Stage 3 — Operations
**Goal**: Monitor cluster health, manage quotas, tune SmartPools tiering, and operate SyncIQ replication.

**Read in this order**:
- [Health Checks](../operations/health-checks/) — run the routine first on every shift; covers cluster health (isi status), node drive state, SmartPools job engine queue, and SyncIQ replication lag.
- [CLI Reference](../operations/cli-reference/) — isi CLI commands for file system, quota, SmartPools, SyncIQ, SnapshotIQ, and S3 bucket management.
- [Procedures](../operations/procedures/) — SnapshotIQ schedule creation and restore, SyncIQ failover/failback, SmartQuota enforcement change, node decommission, and access zone modification.
- [Backup & Restore](../operations/backup-restore/) — SnapshotIQ retention policies, SyncIQ replication to a DR cluster, and NDMP backup to tape or Data Domain.
- [Scripts](../operations/scripts/) — Automation: quota utilisation reporting, SyncIQ health polling, and SmartPools job status via PowerShell or Python SDK.

**Why third**: OneFS job engine runs background tasks (FlexProtect, SmartPools tiering, dedup) that directly impact performance. You need to monitor and schedule them deliberately.

---

## Stage 4 — Security
**Goal**: Secure multi-protocol access across NFS, SMB, and S3 with consistent identity mapping and audit trails.

**Read**:
- [Access Control](../security/access-control/) — OneFS identity mapping (uid/gid/SID), access zone authentication providers, NFS export permissions, and SMB share ACLs.
- [Authentication](../security/authentication/) — Active Directory integration, Kerberos for NFS v4, LDAP for Unix authentication, and S3 access key management.
- [Encryption](../security/encryption/) — Data at rest encryption (D@RE) with self-encrypting drives, SmartLock WORM compliance, and replication encryption in transit.
- [Hardening](../security/hardening/) — Audit log configuration (CEE), disabling legacy SMBv1, TLS enforcement for management APIs, and role-based access for OneFS admin.

**Why fourth**: Multi-protocol identity mapping is complex. Applying security controls before understanding the mapping model causes access failures across protocols.

---

## Stage 5 — Troubleshooting
**Goal**: Diagnose node drive failures, SyncIQ policy errors, quota enforcement issues, and SMB/NFS client connectivity problems.

**Read**:
- [Common Issues](../troubleshooting/common-issues/) — Drive bay failure and FlexProtect rebuild status, SyncIQ policy suspended, quota exceeded blocking writes, and NFS stale file handle errors.
- [Diagnostics](../troubleshooting/diagnostics/) — isi_gather_info log collection, job engine error review, network diagnostics (isi_for_array), and InsightIQ performance trace.
- [Escalation](../troubleshooting/escalation/) — When to contact Dell support, required log bundles (isi_gather_info output), and node replacement coordination.

**Why last**: Troubleshooting makes most sense once you know the normal operating state.
