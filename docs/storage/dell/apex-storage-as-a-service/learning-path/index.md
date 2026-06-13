---
tags:
  - dell
  - learning-path
---
# Dell APEX Storage as a Service — Learning Path

<div class="kb-summary">
Recommended reading order for Dell APEX Storage as a Service. Follow these stages in order to build a complete mental model before working with it in production.
</div>

```text
┌──────────────────────────────────── APEX Storage — Learning Path ─────────────────────────────────────┐
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
**Goal**: Understand how APEX Storage operates as a consumption-based model with Dell-managed on-premises hardware, and how the APEX Console governs capacity, SLA tiers, and billing.

**Read in this order**:
- [How It Works](../architecture/how-it-works/) — APEX STaaS model: Dell owns and operates hardware on-premises at the customer site, consumption billing (reserved vs burst capacity), APEX Console as the single management plane, SLA tier definitions (Performance, Capacity), and how Dell remote monitoring integrates with on-site infrastructure.
- [Design Standards](../architecture/design-standards/) — Reserved capacity sizing methodology, burst headroom planning, SLA tier selection by workload type, data services (snapshots, replication) included vs add-on, and service catalogue scope.
- [Integrations](../architecture/integrations/) — APEX Console REST API for capacity reporting and billing data, integration with internal chargeback systems, CloudIQ for health visibility, and underlying PowerStore or PowerMax hardware that Dell manages.

**Why first**: APEX Storage flips the operational model — Dell manages hardware, you manage workloads. Understanding where the responsibility boundary sits prevents gaps in both operational coverage and financial governance.

---

## Stage 2 — Deployment
**Goal**: Understand the APEX onboarding process and configure your side of the service boundary before presenting storage to workloads.

**Read**:
- [Install & Upgrade](../operations/install-upgrade/) — APEX onboarding workflow: Dell hardware delivery, remote configuration by Dell, APEX Console account activation, capacity pool activation, and service handover checklist.

**Why second**: APEX deployment is primarily Dell-executed, but the customer must configure APEX Console access, chargeback reporting, and SLA tier assignments before workloads are onboarded.

---

## Stage 3 — Operations
**Goal**: Manage capacity consumption, monitor SLA adherence, and interact with Dell for hardware lifecycle events.

**Read in this order**:
- [Health Checks](../operations/health-checks/) — run the routine first on every shift; covers reserved capacity utilisation percentage, burst consumption (billed vs plan), SLA compliance status per workload, and CloudIQ health score for underlying hardware.
- [CLI Reference](../operations/cli-reference/) — APEX Console REST API: capacity queries, consumption reports, service request submission, and SLA tier management endpoints.
- [Procedures](../operations/procedures/) — Requesting capacity increase (reserved tier), managing burst approval thresholds, SLA tier change process, reporting a hardware fault to Dell, and workload onboarding/offboarding.
- [Backup & Restore](../operations/backup-restore/) — Data services included in the APEX subscription tier (snapshots, replication), customer-managed backup policy configuration, and DR failover coordination with Dell support.
- [Scripts](../operations/scripts/) — Automation: APEX Console API capacity polling, consumption alert thresholds, monthly utilisation report generation, and chargeback data export.

**Why third**: Burst consumption incurs additional charges. Operational monitoring of capacity is essential for cost control under the APEX model.

---

## Stage 4 — Security
**Goal**: Enforce access controls on the APEX Console, understand the shared responsibility model, and ensure data protection obligations are met.

**Read**:
- [Access Control](../security/access-control/) — APEX Console user roles (Account Admin, Storage Admin, Billing Viewer), role assignment, and multi-tenant isolation if multiple business units share a service.
- [Authentication](../security/authentication/) — APEX Console SSO integration, MFA enforcement, and API authentication (OAuth2 tokens for REST API access).
- [Encryption](../security/encryption/) — Encryption responsibilities: Dell manages D@RE on underlying hardware; customer manages data-in-transit encryption and key ownership for compliance workloads.
- [Hardening](../security/hardening/) — APEX Console audit log review, MFA mandate for all admin roles, network access restriction for APEX management endpoints, and shared responsibility matrix documentation.

**Why fourth**: The shared responsibility boundary between Dell and the customer organisation must be documented before security audits or compliance assessments.

---

## Stage 5 — Troubleshooting
**Goal**: Know what you can diagnose yourself versus what requires a Dell support engagement, and how to escalate efficiently.

**Read**:
- [Common Issues](../troubleshooting/common-issues/) — APEX Console capacity data stale or incorrect, SLA tier reporting discrepancy, burst overage unexpected, workload performance below SLA, and Dell hardware fault with no alert received.
- [Diagnostics](../troubleshooting/diagnostics/) — APEX Console health views, CloudIQ alert history, SLA compliance report export, and service request log review.
- [Escalation](../troubleshooting/escalation/) — APEX service request types (billing, hardware, SLA), SLA breach escalation path, executive escalation contacts, and contractual SLA remediation process.

**Why last**: Troubleshooting makes most sense once you know the normal operating state.
