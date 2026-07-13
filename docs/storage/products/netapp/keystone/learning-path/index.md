---
tags:
  - learning-path
  - netapp
description: "Recommended reading order for NetApp Keystone. Follow these stages in order to build a complete mental model before working with it in production."
---
# NetApp Keystone — Learning Path

<div class="kb-summary">
Recommended reading order for NetApp Keystone. Follow these stages in order to build a complete mental model before working with it in production.

*Applies to: Keystone STaaS*
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

**Goal**: Understand the Keystone STaaS model — what NetApp manages, what you manage, service tiers, and how committed vs burst consumption is metered.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — Keystone as a subscription service: AFF/ASA hardware on-prem managed by NetApp, ONTAP stack, Keystone Collector agent, digital advisor integration
- [Design Standards](../architecture/design-standards/) — Service tier definitions (Extreme, Premium, Performance, Standard, Value), committed capacity sizing, burst overage thresholds, SLA terms
- [Integrations](../architecture/integrations/) — Keystone dashboard via BlueXP, Active IQ Digital Advisor, AutoSupport telemetry to NetApp, NetApp Keystone Success Manager engagement model

**Why first**: Keystone is an operational shared-responsibility model — understanding the boundary between NetApp-managed infrastructure and your workload management is essential before engaging the service.

---

## Stage 2 — Deployment

**Goal**: Understand the Keystone onboarding sequence, service activation, and initial capacity allocation.

**Read**:

- [Install & Upgrade](../operations/install-upgrade/) — Keystone onboarding steps: site readiness, hardware delivery, NetApp-led ONTAP setup, Keystone Collector deployment, BlueXP subscription activation

**Why second**: The deployment is largely NetApp-managed, but your team owns the SVM provisioning and workload onboarding within the delivered cluster.

---

## Stage 3 — Operations

**Goal**: Monitor committed vs burst usage, generate utilization reports, manage SVMs within the subscribed tiers, and engage NetApp for burst overages.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — Run the routine first on every shift; review Keystone dashboard for tier utilization, burst alerts, and SLA compliance indicators
- [CLI Reference](../operations/cli-reference/) — ONTAP CLI commands for SVM and volume management within Keystone tiers; BlueXP API for subscription queries
- [Procedures](../operations/procedures/) — Requesting capacity expansion, escalating to NetApp for hardware issues, SVM provisioning within committed tier allocation
- [Backup & Restore](../operations/backup-restore/) — SnapMirror and SnapVault within Keystone tiers; understanding replication capacity billing impact
- [Scripts](../operations/scripts/) — Capacity utilization reporting scripts, burst early-warning alerts via Active IQ event integration

---

## Stage 4 — Security

**Goal**: Secure tenant SVMs and ensure the Keystone management plane access is appropriately restricted.

**Read**:

- [Access Control](../security/) — SVM-scoped ONTAP RBAC for tenant teams; restricting BlueXP access to authorized Keystone administrators
- [Authentication](../security/) — BlueXP SSO, ONTAP cluster management authentication, Keystone Collector service account security
- [Encryption](../security/) — NVE/NAE for data at rest on Keystone AFF/ASA hardware; encryption key management responsibilities (customer vs NetApp)
- [Hardening](../security/) — Restrict SVM management to dedicated LIFs, audit log export, disable unused protocols per SVM

---

## Stage 5 — Troubleshooting

**Goal**: Identify and resolve metering discrepancies, SVM performance issues, and escalate hardware or software faults to NetApp.

**Read**:

- [Common Issues](../troubleshooting/) — Unexpected burst billing, Keystone Collector not reporting, SVM throughput below committed tier SLA, BlueXP dashboard data lag
- [Diagnostics](../troubleshooting/) — Active IQ event logs, Keystone Collector log review, ONTAP AutoSupport data for NetApp escalation, dashboard vs CLI capacity reconciliation
- [Escalation](../troubleshooting/) — Keystone Success Manager engagement, NetApp support case for hardware faults, SLA breach reporting procedure

**Why last**: Keystone troubleshooting blends ONTAP diagnostic skills (built in Stage 3) with understanding the subscription model and NetApp support boundary (built in Stage 1).

---

## See also

- [Keystone — Deploy](../../deploy/)
