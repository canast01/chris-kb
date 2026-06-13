# Site Recovery Manager — Learning Path

<div class="kb-summary">
Recommended reading order for VMware Site Recovery Manager (SRM). Follow these stages in order to build a complete mental model before working with it in production.
</div>

```mermaid
graph LR
  S1[Architecture] --> S2[Deploy] --> S3[Operations] --> S4[Security] --> S5[Troubleshoot]
  classDef stage fill:#1e3a5f,stroke:#2563eb,color:#fff
  class S1,S2,S3,S4,S5 stage
```

## Stage 1 — Architecture
**Goal**: Understand how SRM orchestrates DR across paired sites using protection groups, recovery plans, and replication adapters.
**Read in this order**:
- [How It Works](../architecture/how-it-works/) — site pairing model, protection groups (array-based vs. vSphere Replication), recovery plans, and the distinction between planned migration and emergency failover
- [Design Standards](../architecture/design-standards/) — site pair topology, protection group granularity, recovery plan step ordering, IP customisation rules, and RPO/RTO targets
- [Integrations](../architecture/integrations/) — vCenter pairing, vSphere Replication (VRS/VRA), array-based replication adapters (SRA), and NSX network mapping for recovered VMs

**Why first**: SRM's recovery plan behaviour is entirely determined by how protection groups are structured and how network mappings are configured; reading architecture first prevents costly re-mapping work after VMs are already protected.

---

## Stage 2 — Deployment
**Goal**: Deploy SRM at both sites, pair them, configure replication, and validate a test recovery before any production event.
**Read**:
- [Deploy](../deploy/) — SRM appliance deployment at protected and recovery sites, site pairing sequence, vSphere Replication appliance (VRA) deployment, and storage mapping configuration
- [Install & Upgrade](../operations/install-upgrade/) — SRM upgrade order (recovery site first), VRA upgrade, SRA update, and post-upgrade recovery plan validation

**Why second**: Site pairing and replication must be validated with a non-disruptive test recovery before the environment can be considered DR-ready; deploying without a completed test leaves recovery confidence unverified.

---

## Stage 3 — Operations
**Goal**: Run DR drills, monitor replication health, and keep recovery plans current as the protected environment changes.
**Read in this order**:
- [Health Checks](../operations/health-checks/) — run the routine first on every shift
- [CLI Reference](../operations/cli-reference/) — SRM REST API and PowerCLI DR cmdlets for protection group status, recovery plan history, and replication lag queries
- [Procedures](../operations/procedures/) — DR drill execution (test recovery), planned migration workflow, emergency failover, reprotect sequence, and failback procedure
- [Backup & Restore](../operations/backup-restore/) — SRM database backup, recovery plan export, and restore sequence for SRM appliance failure
- [Scripts](../operations/scripts/) — automated replication lag reporting, protection group compliance checks, and recovery plan change-diff scripts

**Why third**: Drill execution and failback are operational skills that require a stable, tested replication baseline; attempting them without prior test recoveries introduces unnecessary risk.

---

## Stage 4 — Security
**Goal**: Restrict recovery plan execution to authorised personnel and protect site-pair credentials.
**Read**:
- [Access Control](../security/access-control/) — SRM administrator and recovery plan operator roles, protection group permission scoping, and audit trail configuration
- [Authentication](../security/authentication/) — vCenter SSO integration for SRM console access, service account credential management for site-pair trust
- [Encryption](../security/encryption/) — vSphere Replication traffic encryption (TLS), SRM appliance certificate management, and encrypted VM replication compatibility
- [Hardening](../security/hardening/) — limiting recovery plan execution permissions, restricting SRM UI to management networks, and disabling test recovery cleanup bypass

**Why fourth**: Recovery plan execution permissions must be validated before any DR drill; unauthorised failover of production VMs is a critical risk in shared environments.

---

## Stage 5 — Troubleshooting
**Goal**: Diagnose replication lag, recovery plan step failures, and reprotect errors before they become DR readiness gaps.
**Read**:
- [Common Issues](../troubleshooting/common-issues/) — replication sync failures, recovery plan step errors (IP customisation, network mapping), reprotect failures after failover, and VRA connectivity issues
- [Diagnostics](../troubleshooting/diagnostics/) — SRM log bundle collection, VRA diagnostic export, replication task event log review, and storage replication adapter (SRA) diagnostics
- [Escalation](../troubleshooting/escalation/) — GSS data requirements for SRM SRs, log bundle packaging, and SR classification for replication data-loss or recovery plan engine failures

**Why last**: Troubleshooting makes most sense once you know the normal operating state.
