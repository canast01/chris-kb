---
tags:
  - dell
  - learning-path
description: "Recommended reading order for Dell RecoverPoint. Follow these stages in order to build a complete mental model before working with it in production."
---
# Dell RecoverPoint — Learning Path

<div class="kb-summary">
Recommended reading order for Dell RecoverPoint. Follow these stages in order to build a complete mental model before working with it in production.

*Applies to: RecoverPoint 5.x*
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
**Goal**: Understand how RecoverPoint intercepts writes using splitters, journals them for any-point-in-time recovery, and groups volumes into consistency groups.

**Read in this order**:
- [How It Works](../architecture/how-it-works/) — Write-splitting mechanism (host-based, array-based, fabric-based), journal volumes, RPO bookmarks, consistency group (CG) membership, RPA (RecoverPoint Appliance) cluster topology, and failover modes (test, image access, failover).
- [Design Standards](../architecture/design-standards/) — CG design (which volumes belong together), journal volume sizing (RPO window × write rate), WAN bandwidth calculation, RPA cluster sizing, and splitter placement decisions.
- [Integrations](../architecture/integrations/) — PowerMax and Unity array splitters, Fabric (VPLEX) splitter, host-based splitter (RecoverPoint for Virtual Machines), vCenter integration, and REST API.

**Why first**: Splitter type determines journal placement and failover scope. Choosing the wrong splitter architecture at design time requires a complete rebuild.

---

## Stage 2 — Deployment
**Goal**: Deploy RPA clusters, configure splitters, create consistency groups, and validate RPO bookmarks before production.

**Read**:
- [Deploy](../deploy/) — RPA deployment (hardware or virtual), management network configuration, splitter registration, CG creation with source and target volumes, and journal volume assignment.
- [Install & Upgrade](../operations/install-upgrade/) — RPA software upgrades (non-disruptive rolling upgrade), splitter driver updates on hosts, and post-upgrade CG validation.

**Why second**: Journal volume placement and CG composition choices are performance-critical. Under-sized journals cause RPO bookmark pruning under load.

---

## Stage 3 — Operations
**Goal**: Monitor RPO compliance, manage bookmarks, test image access, and execute failover and failback.

**Read in this order**:
- [Health Checks](../operations/health-checks/) — run the routine first on every shift; covers CG RPO status (lag), journal utilisation percentage, WAN link throughput, and RPA cluster health in Unisphere for RecoverPoint.
- [CLI Reference](../operations/cli-reference/) — RecoverPoint CLI (RecoverPoint Management Application) commands for CG management, bookmark creation, image access, and failover operations.
- [Procedures](../operations/procedures/) — Enabling image access (test mode, virtual access, logged access), CG failover and failback, bookmark-based restore, adding volumes to existing CG, and WAN optimisation tuning.
- [Backup & Restore](../operations/backup-restore/) — Journal-based point-in-time recovery, integration with backup software via image access, and coordination with Data Domain for offload copies.
- [Scripts](../operations/scripts/) — Automation: RPO monitoring and alerting, bookmark creation schedules, and CG health reporting via REST API.

**Why third**: Image access and failover behave differently depending on CG mode (synchronous vs asynchronous). Operational understanding prevents data loss during DR tests.

---

## Stage 4 — Security
**Goal**: Restrict management access to RecoverPoint, secure replication traffic, and audit failover operations.

**Read**:
- [Access Control](../security/access-control/) — Unisphere for RecoverPoint roles (admin, monitor, operator), RPA management network access restriction, and CG-level operational permissions.
- [Authentication](../security/authentication/) — LDAP/AD integration for management console, local accounts, and certificate management for HTTPS management interface.
- [Encryption](../security/encryption/) — WAN replication encryption (IPsec or TLS), encryption of journal volumes on the underlying array, and key management coordination.
- [Hardening](../security/hardening/) — Disabling unused management ports, TLS enforcement, audit log retention, and change control for CG modification.

**Why fourth**: Replication encryption must be coordinated between both sites. Apply after the CG topology is validated and operational.

---

## Stage 5 — Troubleshooting
**Goal**: Diagnose CG synchronisation failures, RPO violations, splitter connectivity loss, and journal overflow conditions.

**Read**:
- [Common Issues](../troubleshooting/common-issues/) — CG in error state, RPO violation due to WAN congestion, journal approaching 100% utilisation, host splitter disconnection, and image access stuck in enabling state.
- [Diagnostics](../troubleshooting/diagnostics/) — RPA log collection, CG statistics export, WAN link throughput analysis, and support bundle generation from Unisphere for RecoverPoint.
- [Escalation](../troubleshooting/escalation/) — When to engage Dell support, required RPA log bundles, and escalation path for splitter driver or array integration issues.

**Why last**: Troubleshooting makes most sense once you know the normal operating state.

---

## See also

- [Recoverpoint — Deploy](../deploy/)
- [Recoverpoint — Procedures](../operations/procedures/)
- [Recoverpoint — Common Issues](../troubleshooting/common-issues/)
