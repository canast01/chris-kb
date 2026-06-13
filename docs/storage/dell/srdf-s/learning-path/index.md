# Dell SRDF/S (Synchronous) — Learning Path

<div class="kb-summary">
Recommended reading order for Dell SRDF/S. Follow these stages in order to build a complete mental model before working with it in production.
</div>

```mermaid
graph LR
  S1[Architecture] --> S2[Deploy] --> S3[Operations] --> S4[Security] --> S5[Troubleshoot]
  classDef stage fill:#1e3a5f,stroke:#2563eb,color:#fff
  class S1,S2,S3,S4,S5 stage
```

## Stage 1 — Architecture
**Goal**: Understand how SRDF/S holds host I/O until the remote PowerMax acknowledges the write, the latency impact this creates, and the trade-offs versus SRDF/A.

**Read in this order**:
- [How It Works](../architecture/how-it-works/) — Synchronous write acknowledgement flow: R1 write held until R2 confirms persistence; RDF director path; SRDF/S vs SRDF/A trade-off (zero RPO vs write latency addition); bias setting for split-brain resolution; and triangular SRDF multi-site topology.
- [Design Standards](../architecture/design-standards/) — Maximum viable distance (RTT budget), write I/O size sensitivity, SRDF/S consistency group sizing, bias configuration for automated site preference, and co-existence with SRDF/A in three-site designs.
- [Integrations](../architecture/integrations/) — Unisphere for PowerMax synchronous replication dashboard, SYMCLI for scripted operations, VPLEX Metro combined with SRDF/S for zero-RPO active-active metro, and vSphere Site Recovery Manager integration.

**Why first**: SRDF/S adds write latency proportional to round-trip time between arrays. Architects who skip this end up with unexplained host application timeouts at distance.

---

## Stage 2 — Deployment
**Goal**: Establish a synchronous RDF pair, validate zero data loss under load, and configure bias before production cutover.

**Read**:
- [Deploy](../deploy/) — RDF group creation for synchronous mode, volume pairing with symrdf establish -rdftype S, bias configuration, first-sync completion validation, and host application write latency baseline measurement.
- [Install & Upgrade](../operations/install-upgrade/) — HYPERMAX OS upgrade sequence across a live SRDF/S pair, temporary mode change to async during upgrade window, and post-upgrade validation.

**Why second**: Bias must be set before the first production failover. A default bias setting in a split-brain scenario causes the wrong site to win I/O ownership.

---

## Stage 3 — Operations
**Goal**: Monitor synchronisation state, execute planned suspend/resume cycles, manage triangular SRDF across three sites, and recover from link outages.

**Read in this order**:
- [Health Checks](../operations/health-checks/) — run the routine first on every shift; covers SRDF/S pair state (Synchronized, SyncInProg), RDF link latency, WAN error rate, and bias setting confirmation.
- [CLI Reference](../operations/cli-reference/) — SYMCLI: symrdf query, symrdf suspend, symrdf resume, symrdf failover, symrdf establish; and Unisphere REST API equivalents for automation.
- [Procedures](../operations/procedures/) — Planned suspend for array maintenance, resume and re-sync after link restoration, SRDF/S to SRDF/A mode conversion for distance expansion, triangular SRDF failover sequence, and application-consistent failover with VMware SRM.
- [Backup & Restore](../operations/backup-restore/) — TimeFinder SnapVX on R2 volumes for backup copies without impacting synchronous replication, and snap scheduling aligned to array maintenance windows.
- [Scripts](../operations/scripts/) — Automation: sync state monitoring with alert on Suspended or SyncInProg duration, automated suspend/resume around maintenance scripts, and triangular SRDF topology health reports.

**Why third**: SRDF/S failures impact host write I/O immediately. Operators must know the suspend procedure and the bias behaviour before a link outage forces a decision.

---

## Stage 4 — Security
**Goal**: Restrict SRDF failover operations and protect the synchronous replication channel.

**Read**:
- [Access Control](../security/access-control/) — RBAC control of symrdf failover commands, Unisphere role assignments for synchronous replication operations, and separation of duty between storage admin and DR runbook executor.
- [Authentication](../security/authentication/) — SYMAPI user authentication, Solutions Enabler daemon security, and Unisphere certificate management.
- [Encryption](../security/encryption/) — RDF link encryption for SRDF/S (latency impact assessment at encryption overhead), KMIP key management, and encrypted volume configuration on both R1 and R2.
- [Hardening](../security/hardening/) — Audit trail for all SRDF state changes, change management gate for bias modification, and RDF group access restriction via SYMAPI ACLs.

**Why fourth**: SRDF/S failover is a zero-RPO operation with immediate host impact. Access controls are critical before the platform reaches production readiness.

---

## Stage 5 — Troubleshooting
**Goal**: Diagnose SRDF/S link faults that pause host I/O, split-brain conditions, and re-sync slowness after link restoration.

**Read**:
- [Common Issues](../troubleshooting/common-issues/) — Host I/O paused (SRDF/S link down, no bias configured), split-brain after simultaneous site failure, re-sync taking longer than maintenance window allows, and triangular SRDF third leg degradation.
- [Diagnostics](../troubleshooting/diagnostics/) — symrdf query -v state analysis, RDF director error counts, Unisphere event log for link events, and SYMCLI performance data for re-sync throughput.
- [Escalation](../troubleshooting/escalation/) — When to engage Dell support for RDF director hardware, required SYMAPI and EMC grab bundles, and escalation for triangular SRDF topology issues.

**Why last**: Troubleshooting makes most sense once you know the normal operating state.
