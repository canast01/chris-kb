# Dell VPLEX — Learning Path

<div class="kb-summary">
Recommended reading order for Dell VPLEX. Follow these stages in order to build a complete mental model before working with it in production.
</div>

```mermaid
graph LR
  S1[Architecture] --> S2[Deploy] --> S3[Operations] --> S4[Security] --> S5[Troubleshoot]
  classDef stage fill:#1e3a5f,stroke:#2563eb,color:#fff
  class S1,S2,S3,S4,S5 stage
```

## Stage 1 — Architecture
**Goal**: Understand how VPLEX federates storage from multiple arrays into distributed volumes that hosts access concurrently from two sites.

**Read in this order**:
- [How It Works](../architecture/how-it-works/) — VPLEX cluster architecture (VS2, VS6), distributed volumes and virtual volumes, WAN link (inter-cluster communication), cache coherency protocol between sites, VPLEX Metro (concurrent access) vs VPLEX Geo (non-concurrent), and witness appliance role in split-brain resolution.
- [Design Standards](../architecture/design-standards/) — Distributed volume design (which back-end arrays to federate), WAN latency and bandwidth requirements for Metro, cache size planning, consistency group membership for VPLEX Metro, and witness placement.
- [Integrations](../architecture/integrations/) — PowerMax, PowerStore, and Unity back-end storage connectivity, VMware vSphere Metro Storage Cluster (vMSC) for HA across sites, Site Recovery Manager for orchestrated failover, and VPLEX management (Management Server) REST API.

**Why first**: VPLEX's cache coherency model and the role of the witness are unique. Without understanding them, split-brain scenarios during a site outage cause data integrity failures.

---

## Stage 2 — Deployment
**Goal**: Deploy VPLEX clusters at both sites, federate back-end storage, create distributed volumes, and present them to host clusters.

**Read**:
- [Deploy](../deploy/) — Management Server configuration, back-end storage discovery and claim, virtual volume creation from storage views, distributed device creation across clusters, host view (initiator group, port group, storage view) configuration, and WAN link setup.
- [Install & Upgrade](../operations/install-upgrade/) — VPLEX GeoSynchrony software upgrades (non-disruptive rolling procedure), hardware component replacement, and post-upgrade distributed volume health validation.

**Why second**: Back-end storage visibility and distributed device composition decisions are permanent post-creation. Adding new back-end arrays post-deploy requires careful migration planning.

---

## Stage 3 — Operations
**Goal**: Monitor distributed volume consistency, manage site mobility, and execute Metro failover when a site goes offline.

**Read in this order**:
- [Health Checks](../operations/health-checks/) — run the routine first on every shift; covers distributed device sync state, WAN link status and throughput, cache hit ratio at both clusters, witness connectivity, and back-end array health.
- [CLI Reference](../operations/cli-reference/) — VPLEX CLI (Management Server shell) commands for distributed device, consistency group, storage view, and WAN link management; and Management Server REST API.
- [Procedures](../operations/procedures/) — Planned site migration (move distributed volume to one cluster), Metro failover and failback, consistency group suspend and resume, adding new initiators to storage views, and back-end volume expansion.
- [Backup & Restore](../operations/backup-restore/) — Snapshot from the back-end array (PowerMax SnapVX) on VPLEX-fronted volumes, and RecoverPoint for VPLEX (RPfVPLEX) integration for journal-based CDP.
- [Scripts](../operations/scripts/) — Automation: distributed device health monitoring, WAN link latency alerting, and storage view audit reporting via REST API.

**Why third**: VPLEX Metro failover requires understanding which cluster wins I/O ownership post-split. Operators who skip this can cause data corruption during an unplanned site event.

---

## Stage 4 — Security
**Goal**: Restrict VPLEX management access and secure inter-cluster communication.

**Read**:
- [Access Control](../security/access-control/) — Management Server roles (Monitor, Architect, Operations, Superuser), storage view access restrictions, and separation of duties for Metro failover operations.
- [Authentication](../security/authentication/) — LDAP integration for Management Server users, certificate-based inter-cluster authentication, and management API token management.
- [Encryption](../security/encryption/) — WAN link encryption between VPLEX clusters, back-end array encryption co-existence with distributed volumes, and key management coordination.
- [Hardening](../security/hardening/) — Management Server network isolation, TLS enforcement for REST API, audit logging for storage view and distributed device changes, and witness access restriction.

**Why fourth**: VPLEX Metro failover is a critical operation. Management access controls must be validated before the platform handles production Metro workloads.

---

## Stage 5 — Troubleshooting
**Goal**: Diagnose WAN link failures, cache coherency errors, split-brain conditions, and back-end storage path issues.

**Read**:
- [Common Issues](../troubleshooting/common-issues/) — WAN link down causing Metro degraded mode, witness unreachable blocking automatic failover, back-end array path loss causing distributed device degradation, and storage view masking issues.
- [Diagnostics](../troubleshooting/diagnostics/) — Management Server log collection, distributed device state query, WAN link diagnostics, back-end array connectivity checks, and SupportAssist bundle generation.
- [Escalation](../troubleshooting/escalation/) — When to engage Dell support for VPLEX hardware, required Management Server log bundles, and escalation path for GeoSynchrony software defects.

**Why last**: Troubleshooting makes most sense once you know the normal operating state.
