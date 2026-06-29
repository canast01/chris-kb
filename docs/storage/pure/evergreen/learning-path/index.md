---
tags:
  - learning-path
  - pure
---
# Pure Storage Evergreen — Learning Path

<div class="kb-summary">
Recommended reading order for Pure Storage Evergreen subscription model. Follow these stages in order to build a complete mental model before managing Evergreen assets in production.

*Applies to: Evergreen*
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

**Goal**: Understand what Evergreen is — a subscription model that removes forklift upgrades — and how controller upgrades, capacity-on-demand, and SLA guarantees work together.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — Evergreen//Forever vs Evergreen//One tiers, controller upgrade mechanics (non-disruptive controller swap), capacity-on-demand provisioning model, SLA guarantee structure (availability, latency, NPS), and Pure1 as the management and billing plane
- [Design Standards](../architecture/design-standards/) — reserved vs on-demand capacity planning, controller upgrade scheduling windows, subscription term alignment with workload growth, and fleet standardisation across sites
- [Integrations](../architecture/integrations/) — Pure1 API for capacity and billing data, integration with ITSM for controller upgrade scheduling, and Evergreen//One hybrid billing with on-prem hardware

**Why first**: Evergreen is a commercial and operational model, not just hardware. Understanding the distinction between Evergreen//Forever (owned hardware, subscription services) and Evergreen//One (STaaS, Pure-owned hardware) prevents misaligned expectations during contract renewals and controller upgrades.

---

## Stage 2 — Deployment

**Goal**: Understand how Evergreen assets are initially provisioned, how controller upgrades are executed without downtime, and how to validate the array post-upgrade.

**Read**:

- [Controller Upgrades](../controller-upgrades/) — controller swap procedure step-by-step, pre-upgrade checklist (path redundancy, host connectivity), upgrade window coordination with Pure, post-upgrade validation, and rollback considerations
- [Install & Upgrade](../operations/install-upgrade/) — Purity software upgrade scheduling via Pure1, upgrade channel selection, pre-upgrade health validation, and post-upgrade performance baseline check

**Why second**: Non-disruptive controller upgrades are Evergreen's flagship capability, but they require dual-path host connectivity to execute safely. Skipping pre-upgrade validation leads to I/O interruptions during the controller handoff.

---

## Stage 3 — Operations

**Goal**: Track subscription consumption, manage capacity-on-demand requests, and maintain array health across the Evergreen lifecycle.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — run the routine first on every shift; covers array health, Purity version status, controller firmware currency, subscription capacity utilisation vs reserved allocation, and SLA compliance metrics in Pure1
- [CLI Reference](../operations/cli-reference/) — Purity CLI and Pure1 API commands for capacity reporting, subscription status queries, and controller health checks
- [Procedures](../operations/procedures/) — capacity-on-demand request process, controller upgrade scheduling with Pure, subscription renewal coordination, and SLA breach reporting
- [Backup & Restore](../operations/backup-restore/) — protection group and snapshot management within Evergreen-subscribed arrays, ensuring backup SLAs align with Evergreen availability guarantees
- [Scripts](../operations/scripts/) — automation for capacity trending reports, subscription utilisation alerts, and controller firmware age monitoring via Pure1 API

**Why third**: Capacity-on-demand requests are fulfilled by Pure within SLA timeframes — but only if requested proactively. Monitoring utilisation trends against reserved capacity thresholds is the core operational discipline.

---

## Stage 4 — Security

**Goal**: Understand how Evergreen subscription access is controlled through Pure1, and how security posture is maintained across the upgrade lifecycle.

**Read**:

- [Access Control](../security/access-control/) — Pure1 role-based access (org admin/array admin/read-only), per-array permission scoping, and API token management for automation
- [Authentication](../security/authentication/) — Pure1 SSO (SAML 2.0), MFA enforcement for Pure1 portal access, and audit log access for compliance reporting
- [Encryption](../security/encryption/) — encryption validation post-controller upgrade, FIPS 140-2 compliance continuity through controller swap, and KMIP external key management continuity
- [Hardening](../security/hardening/) — SafeMode snapshot protection maintained through controller upgrades, audit log continuity during Purity upgrades, and Pure1 network access restrictions

**Why fourth**: Controller upgrades change physical hardware but must not change the security posture. Validate encryption key continuity and SafeMode status after every controller swap.

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose SLA violations, controller upgrade complications, and capacity provisioning delays before escalating to Pure Support.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — controller upgrade stalls, post-upgrade path connectivity loss, capacity-on-demand provisioning delays, Pure1 connectivity loss, and SLA metric anomalies
- [Diagnostics](../troubleshooting/diagnostics/) — Pure1 alert review, controller upgrade log analysis, pre- and post-upgrade comparison reports, and diagnostic bundle collection for Pure Support
- [Escalation](../troubleshooting/escalation/) — Evergreen SLA escalation contacts, SLA breach documentation, Pure Support case creation via Pure1, and on-site hardware intervention workflow

**Why last**: Troubleshooting makes most sense once you know the normal operating state — expected controller upgrade duration, capacity-on-demand SLA timeframes, and Pure1 reporting baselines.

---

## See also

- [Evergreen — Deploy](../../deploy/)
