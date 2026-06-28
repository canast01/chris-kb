---
tags:
  - dell
  - learning-path
---
# Dell PowerStore — Learning Path

<div class="kb-summary">
Recommended reading order for Dell PowerStore. Follow these stages in order to build a complete mental model before working with it in production.

*Applies to: PowerStore 3.x*
</div>

```mermaid
graph LR
  S1[Architecture] --> S2[Deploy] --> S3[Operations] --> S4[Security] --> S5[Troubleshoot]
  classDef stage fill:#1e3a5f,stroke:#2563eb,color:#fff
  class S1,S2,S3,S4,S5 stage
```

## Stage 1 — Architecture
**Goal**: Understand the ApplX software-defined architecture, NVMe-native data path, and how PowerStore T and X models differ before any configuration work.

**Read in this order**:
- [How It Works](../architecture/how-it-works/) — ApplX architecture: unified NVMe core, inline deduplication and compression, and how block, file, and VMware workloads share a single appliance.
- [Design Standards](../architecture/design-standards/) — Volume and file system placement, NVMe/NVMe-oF host connectivity, Metro Volume active-active topology, and appliance cluster sizing.
- [Integrations](../architecture/integrations/) — Native replication to a second PowerStore, import from Unity/VNX using the Import Utility, Container Storage Interface (CSI) for Kubernetes, and REST API.

**Why first**: PowerStore's ApplX architecture breaks from traditional controller pairs. Understanding it prevents misconfigurations around Metro Volume active-active behaviour and NVMe path management.

---

## Stage 2 — Deployment
**Goal**: Commission a PowerStore appliance from initial power-on through first workload presentation.

**Read**:
- [Deploy](../deploy/) — Initial setup wizard, network configuration (management, iSCSI/NVMe-oF, replication), host group creation, volume mapping, and file system export.
- [Install & Upgrade](../operations/install-upgrade/) — Non-disruptive software upgrades, appliance expansion, and node addition to an existing cluster.

**Why second**: PowerStore initial configuration determines which connectivity modes are available. Changing from iSCSI to NVMe-oF post-deploy requires re-zoning and host updates.

---

## Stage 3 — Operations
**Goal**: Manage PowerStore day-to-day — capacity, replication health, snapshot schedules, and host performance.

**Read in this order**:
- [Health Checks](../operations/health-checks/) — run the routine first on every shift; covers appliance health, Metro Volume sync state, replication session status, and capacity utilisation.
- [CLI Reference](../operations/cli-reference/) — PowerStore CLI (pstcli) and REST API commands for volume, host, replication session, and snapshot management.
- [Procedures](../operations/procedures/) — Volume snapshot creation and restore, Metro Volume failover, replication failover/failback, and host migration between appliances.
- [Backup & Restore](../operations/backup-restore/) — Snapshot policies, replication-based DR, and integration with PowerProtect Data Manager.
- [Scripts](../operations/scripts/) — Automation: bulk volume creation, replication session health polling, and capacity reporting via REST API.

**Why third**: Metro Volume active-active failover is transparent to hosts but requires operational understanding of sync state before you initiate a failover.

---

## Stage 4 — Security
**Goal**: Enforce role-based access, enable data-at-rest encryption, and harden the management plane.

**Read**:
- [Access Control](../security/access-control/) — PowerStore Manager roles (Administrator, Storage Operator, VM Administrator), local users, and RBAC boundaries.
- [Authentication](../security/authentication/) — Active Directory integration, LDAP configuration, and certificate management for the management UI and REST API.
- [Encryption](../security/encryption/) — Self-encrypting drives, external key manager (KMIP), and key lifecycle management.
- [Hardening](../security/hardening/) — TLS enforcement, disabling unused protocols, audit log retention, and network access restrictions on the management interface.

**Why fourth**: Security settings are applied after the platform is operational and do not require downtime on a properly configured cluster.

---

## Stage 5 — Troubleshooting
**Goal**: Diagnose Metro Volume sync delays, replication session faults, NVMe path issues, and appliance hardware alerts.

**Read**:
- [Common Issues](../troubleshooting/common-issues/) — Metro Volume out-of-sync, replication RPO breach, NVMe initiator connectivity loss, and capacity threshold alerts.
- [Diagnostics](../troubleshooting/diagnostics/) — SupportAssist log collection, event log analysis in PowerStore Manager, REST API health queries, and performance tracing.
- [Escalation](../troubleshooting/escalation/) — Support case creation, required log bundles, and how to engage Dell engineering for appliance hardware or ApplX firmware issues.

**Why last**: Troubleshooting makes most sense once you know the normal operating state.

---

## See also

- [Powerstore — Deploy](../deploy/)
- [Powerstore — Procedures](../operations/procedures/)
- [Powerstore — Common Issues](../troubleshooting/common-issues/)
