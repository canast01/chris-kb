---
tags:
  - learning-path
  - pure
---
# Pure1 — Learning Path

<div class="kb-summary">
Recommended reading order for Pure1 (SaaS management and AI-driven operations). Follow these stages in order to build a complete mental model before using Pure1 to manage a production fleet.
</div>

```text
┌──────────────────────────────────────── Pure1 — Learning Path ────────────────────────────────────────┐
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

**Goal**: Understand what Pure1 is — a SaaS management plane that aggregates telemetry from all Pure arrays globally — and how its AI-ops features derive value from fleet-wide data.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — Pure1 SaaS architecture (cloud-hosted, connected via call-home telemetry from arrays), global fleet view across FlashArray and FlashBlade, array health dashboard, capacity forecasting engine, anomaly detection (Workload Planner), AI-driven workload matching, Pure1 REST API, and support case creation integration
- [Design Standards](../architecture/design-standards/) — array-to-Pure1 connectivity requirements (outbound HTTPS call-home), Pure1 org structure (sites, tags, fleet grouping), and telemetry retention and data residency considerations
- [Integrations](../architecture/integrations/) — Pure1 API integration with monitoring platforms (Grafana, Datadog), ITSM (ServiceNow) for support case automation, and Evergreen//One billing portal integration

**Why first**: Pure1 is a passive management plane — it observes, forecasts, and alerts, but does not directly control arrays. Understanding this boundary prevents over-reliance on Pure1 for operational actions that require direct Purity CLI or GUI access.

---

## Stage 2 — Deployment

**Goal**: Understand how arrays register with Pure1, how to configure fleet organisation, and how to validate that telemetry is flowing correctly before relying on Pure1 dashboards.

**Read**:

- [Deploy](../deploy/) — array call-home connectivity validation (HTTPS to pure1.purestorage.com), Pure1 org onboarding, array tagging and site assignment, user account provisioning, and initial dashboard review checklist
- [Architecture — Design Standards](../architecture/design-standards/) — network proxy configuration for call-home traffic, firewall rule requirements, and telemetry gap detection

**Why second**: Pure1 dashboards are only as reliable as the call-home telemetry stream. Validating connectivity and checking for telemetry gaps before using Pure1 for capacity planning prevents decisions based on stale data.

---

## Stage 3 — Operations

**Goal**: Use Pure1 as the daily operational window into fleet health — monitoring array health, acting on capacity forecasts, investigating anomaly alerts, and submitting support cases.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — run the routine first on every shift; covers fleet health summary (arrays at WARN/ERROR), capacity utilisation and days-to-full forecast, anomaly detection alerts, open support cases, and Purity version currency across the fleet
- [Capacity](../capacity/) — capacity forecasting methodology, how to interpret days-to-full projections, capacity trend graphs, and using Pure1 to build the business case for capacity-on-demand requests
- [Performance](../performance/) — workload latency and throughput trend analysis, identifying noisy-neighbour workloads, and Pure1 Workload Planner recommendations for array placement
- [Scripts](../scripts/) — Pure1 REST API automation for fleet health reporting, capacity trend exports, anomaly alert polling, and support case status queries
- [Support](../support/) — support case creation from Pure1, case priority and severity selection, diagnostic bundle upload, and tracking case resolution progress

**Why third**: Pure1's value is in trends and early warnings, not point-in-time status. Operators who check it daily and act on forecasts prevent capacity surprises; those who use it reactively miss the lead time Workload Planner provides.

---

## Stage 4 — Security

**Goal**: Secure Pure1 portal access, manage API tokens for automation, and understand what data Pure1 collects from your arrays.

**Read**:

- [Access Control](../security/access-control/) — Pure1 org-level RBAC (org admin/array admin/read-only), per-array access scoping, and delegating finance-team access for Evergreen//One billing views
- [Authentication](../security/authentication/) — Pure1 SSO configuration (SAML 2.0 / OIDC), MFA enforcement for all users, API token generation and rotation, and session timeout policy
- [Encryption](../security/encryption/) — Pure1 telemetry data in transit (TLS 1.2+), data residency and retention policy for call-home telemetry, and what array data Pure1 does and does not collect (no user data, only array metadata)
- [Hardening](../security/hardening/) — IP allowlisting for Pure1 portal access, audit log review for Pure1 user actions, and restricting API token scope to least-privilege for automation accounts

**Why fourth**: Pure1 API tokens with org-admin scope can read health and capacity data across your entire fleet. Token rotation discipline and least-privilege scoping protect against credential compromise.

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose telemetry gaps, dashboard data discrepancies, and anomaly detection false positives before escalating to Pure Support.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — array not appearing in Pure1 (call-home connectivity failure), stale capacity data (telemetry gap), anomaly alerts on healthy workloads, and Pure1 API authentication errors
- [Diagnostics](../troubleshooting/diagnostics/) — call-home connectivity test from Purity CLI (`purearray --list`), Pure1 telemetry last-seen timestamp, API debug logging, and fleet health report export for offline analysis
- [Escalation](../troubleshooting/escalation/) — Pure Support case creation for Pure1 portal issues, telemetry gap investigation, and escalation path for Workload Planner recommendation disputes

**Why last**: Troubleshooting makes most sense once you know the normal operating state — expected telemetry refresh frequency, normal anomaly alert rates for your workload types, and what capacity forecast accuracy to expect from Pure1's AI model.
