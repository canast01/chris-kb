---
tags:
  - learning-path
  - netapp
---
# NetApp InsightIQ — Learning Path

<div class="kb-summary">
Recommended reading order for NetApp InsightIQ. Follow these stages in order to build a complete mental model before working with it in production.

*Applies to: InsightIQ*
</div>

```text
┌────────────────────────────────────── InsightIQ — Learning Path ──────────────────────────────────────┐
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

**Goal**: Understand how InsightIQ collects and stores performance data from ONTAP and Isilon clusters, and what analytics it provides.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — InsightIQ data collection via ONTAP performance APIs and OneFS statistics; local PostgreSQL datastore; workload analysis engine; dashboard rendering
- [Design Standards](../architecture/design-standards/) — Collection interval settings, retention periods for raw vs aggregated data, multi-cluster federation considerations, VM sizing requirements
- [Integrations](../architecture/integrations/) — ONTAP and Isilon/PowerScale cluster credential registration, SMTP alerting, Active Directory authentication, REST API for custom exports

**Why first**: InsightIQ's analytics are only as useful as the collection baseline — understanding the data model and retention before deployment ensures you capture the right granularity.

---

## Stage 2 — Deployment

**Goal**: Install InsightIQ as a virtual appliance, register storage clusters, and validate data collection.

**Read**:

- [Deploy](../deploy/) — OVA deployment on vSphere, initial configuration wizard, cluster credential registration, collection job validation, SSL certificate configuration

---

## Stage 3 — Operations

**Goal**: Use InsightIQ dashboards to identify performance bottlenecks, capacity trends, and protocol distribution patterns.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — Run the routine first on every shift; verify collection jobs are running, check for data gaps, review cluster reachability status
- [Performance](../performance/) — Throughput/IOPS/latency dashboards, workload heatmaps, top-N client and protocol analysis, percentile latency trending
- [Workloads](../workloads/) — Workload classification, identifying noisy-neighbour volumes, correlating client activity with storage performance
- [Capacity](../capacity/) — Capacity trend projections, aggregate and volume fill-rate analysis, thin-provisioning overcommit risk reporting
- [Reports](../reports/) — Scheduled report generation, custom dashboard export, executive summary reports for capacity planning reviews
- [CLI Reference](../cli-reference/) — InsightIQ REST API endpoints for data export, `iiq` CLI for collection management and database maintenance
- [Scripts](../scripts/) — Custom metric extraction scripts, automated capacity report delivery, alert integration with monitoring platforms

---

## Stage 4 — Security

**Goal**: Restrict InsightIQ access to authorised users and protect storage cluster credentials.

**Read**:

- [Access Control](../security/access-control/) — InsightIQ local user roles (Admin, Analyst, Viewer), AD group mapping, per-cluster visibility scoping
- [Authentication](../security/authentication/) — Active Directory integration for SSO, local admin account hardening, certificate-based HTTPS access
- [Encryption](../security/encryption/) — HTTPS enforcement for the InsightIQ web UI, encrypted storage of cluster credentials, TLS for ONTAP/Isilon API connections
- [Hardening](../security/hardening/) — Restrict management network access to the InsightIQ VM, disable unused API endpoints, log access and report downloads

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose collection failures, data gaps, and dashboard rendering issues.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — Cluster collection stopped, data gap in throughput charts, performance percentiles not calculated, login failure after AD group change
- [Diagnostics](../troubleshooting/diagnostics/) — InsightIQ collection log (`/var/log/iiq`), PostgreSQL query performance checks, cluster credential re-validation, API connectivity tests
- [Escalation](../troubleshooting/escalation/) — NetApp support case for InsightIQ bugs, log bundle collection procedure, ONTAP statistics API troubleshooting with NetApp

**Why last**: Troubleshooting InsightIQ data gaps requires knowing the expected collection cadence and data model — context built in the Architecture and Operations stages.
