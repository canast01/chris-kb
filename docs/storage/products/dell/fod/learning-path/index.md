---
tags:
  - dell
  - learning-path
description: "Recommended reading order for Dell Features on Demand. Follow these stages in order to build a complete mental model before working with it in production."
---
# Dell Features on Demand (FOD) — Learning Path

<div class="kb-summary">
Recommended reading order for Dell Features on Demand. Follow these stages in order to build a complete mental model before working with it in production.

*Applies to: Dell FOD*
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
**Goal**: Understand how FOD delivers software-activated feature licenses, the difference between trial and permanent keys, and which enterprise features are gated by FOD on each product.

**Read in this order**:
- [How It Works](../architecture/how-it-works/) — FOD model: enterprise features (encryption, advanced replication tiers, additional protocols) are installed on the hardware but software-locked at the factory; a license key from the Dell License Management portal unlocks them without a field visit; trial licenses (typically 30 days) allow evaluation; permanent licenses are tied to the array serial number.
- [Design Standards](../architecture/design-standards/) — FOD feature catalogue by product (PowerMax, PowerStore, Unity, PowerScale), license key management process, trial-to-permanent conversion workflow, license audit requirements, and what happens when a trial license expires.
- [Integrations](../architecture/integrations/) — Unisphere for PowerMax and Unity FOD activation screens, PowerStore Manager license management, Dell License Management portal API, and integration with software asset management (SAM) tooling for license tracking.

**Why first**: FOD gates critical production features like encryption and synchronous replication tiers. Understanding which features require FOD prevents discovering the gap during a production enablement project.

---

## Stage 2 — Deployment
**Goal**: Identify required FOD features for a deployment, generate license keys, and activate them before production cutover.

**Read**:
- [Install & Upgrade](../operations/install-upgrade/) — Pre-deployment FOD audit (which features are needed), license key generation from Dell License Management portal, activation via Unisphere or PowerStore Manager, activation validation, and trial license request process for pre-production testing.

**Why second**: Some FOD features (encryption, specific replication modes) must be enabled before data is written. Activating them post-production can require data migration.

---

## Stage 3 — Operations
**Goal**: Track license expiry, manage trial conversions, audit feature usage, and handle license transfers for array replacements.

**Read in this order**:
- [Health Checks](../operations/health-checks/) — run the routine first on every shift; covers trial license expiry countdown (alert before expiry), active FOD features per system, and feature activation status in Unisphere/PowerStore Manager.
- [CLI Reference](../operations/cli-reference/) — Unisphere REST API for license query and activation, SYMCLI license management commands for PowerMax, and PowerStore Manager CLI equivalents.
- [Procedures](../operations/procedures/) — Trial license activation, permanent license activation, trial-to-permanent conversion, license transfer during array replacement (new serial number), license audit report generation, and emergency feature activation outside change windows.
- [Backup & Restore](../operations/backup-restore/) — Backing up license key records (separate from array backup), documenting activated features per array for DR configuration parity, and license reactivation after a rebuild.
- [Scripts](../operations/scripts/) — Automation: license expiry monitoring and alerting, active FOD feature inventory report across fleet, and Dell License Management portal API integration for licence audit.

**Why third**: Trial license expiry disables production features without warning. Operational monitoring closes the gap between trial evaluation and procurement approval timelines.

---

## Stage 4 — Security
**Goal**: Control who can activate FOD features and maintain an audit trail for software license compliance.

**Read**:
- [Access Control](../security/access-control/) — Unisphere and PowerStore Manager role restriction for license activation (Administrator role required), Dell License Management portal user access, and change management gate for production feature activation.
- [Authentication](../security/authentication/) — Dell License Management portal account management, MFA for portal access, and Unisphere/PowerStore Manager session authentication for activation operations.
- [Encryption](../security/encryption/) — FOD encryption feature activation (D@RE): understand that activating encryption post-data-write does not retroactively encrypt existing data; plan for data migration if encryption is a compliance requirement.
- [Hardening](../security/hardening/) — Audit logging of all FOD activation events in Unisphere, change management documentation for all license activations, and software asset management integration for compliance reporting.

**Why fourth**: FOD activation of encryption features has irreversible implications for data protection compliance. Access controls must gate who can make these changes.

---

## Stage 5 — Troubleshooting
**Goal**: Diagnose failed activations, expired trial features causing functionality loss, and license key errors.

**Read**:
- [Common Issues](../troubleshooting/common-issues/) — License key activation rejected (wrong serial number or already consumed), trial license expired silently disabling a feature, permanent license not persisting after HYPERMAX OS upgrade, and feature missing from Unisphere despite activation.
- [Diagnostics](../troubleshooting/diagnostics/) — Unisphere and PowerStore Manager license event log review, Dell License Management portal activation history, SYMCLI license query for PowerMax, and SupportAssist log for activation failure root cause.
- [Escalation](../troubleshooting/escalation/) — When to engage Dell support for license portal issues, key generation errors, and feature activation failures that require Dell engineering involvement.

**Why last**: Troubleshooting makes most sense once you know the normal operating state.

---

## See also

- [Fod — Procedures](../operations/procedures/)
- [Fod — Common Issues](../troubleshooting/common-issues/)
