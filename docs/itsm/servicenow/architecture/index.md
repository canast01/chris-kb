---
tags:
  - architecture
  - servicenow
---
# ServiceNow — Architecture

<div class="kb-summary">
ServiceNow is a multi-instance SaaS platform with fully isolated per-customer stacks. On-premises integration is handled via MID Servers — outbound-only Java agents that eliminate inbound firewall requirements.

*Applies to: ServiceNow*
</div>

```text
┌───────────────────────── ServiceNow — Enterprise ITSM Platform Architecture ──────────────────────────┐
│                                                                                                       │
│  SaaS-only ITSM; dedicated customer instance; CMDB tracks CI relationships;                           │
│  Integration Hub for third-party connections; release cadence: quarterly.                             │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Instance Architecture             │  │                 Core Modules                │   │
│   │         Dedicated: own DB + compute          │  │           ITSM: incident + change           │   │
│   │           SaaS: ServiceNow-hosted            │  │            CMDB: CI and topology            │   │
│   │          Multi-instance: no sharing          │  │          Service Catalog: requests          │   │
│   │          Prod + non-prod instances           │  │            Knowledge: KB articles           │   │
│   │          MID Server: on-prem bridge          │  │          Asset: inventory tracking          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  MID Server is a Java agent on-prem; required for discovery and integration.                          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Integration Patterns             │  │                Release Model                │   │
│   │             REST API: table API              │  │           Quarterly: named by city          │   │
│   │         Integration Hub: connectors          │  │           Current: Yokohama (2025)          │   │
│   │           MID Server: on-prem push           │  │         2 versions supported at once        │   │
│   │        Event Management: SNMP/syslog         │  │             Subproduction clone             │   │
│   │          LDAP/SAML: user sync + SSO          │  │          Update set: change bundle          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Entirely SaaS; MID Server VM required on-prem for discovery and integrations;                        │
│  network: instance on HTTPS 443; MID Server needs outbound 443 to instance URL.                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ServiceNow     = enterprise ITSM SaaS; incident, change, problem, service catalog                    │
│  Instance       = dedicated ServiceNow environment; own URL (company.service-now.com)                 │
│  CMDB           = Configuration Management DB; CIs and their relationships                            │
│  CI             = Configuration Item; any managed asset in CMDB                                       │
│  MID Server     = on-prem Java agent; bridges ServiceNow cloud to your network                        │
│  Integration Hub= low-code connector platform; 200+ pre-built integrations                            │
│  Update set     = package of changes; moved between non-prod and prod instances                       │
│  Table API      = REST API for every ServiceNow table (incidents, CIs, etc.)                          │
│  Discovery      = automated CI discovery via MID Server + probes                                      │
│  ITSM           = IT Service Management; incident, change, problem, request                           │
│  Quarterly release= new named version every 3 months (Utah, Vancouver, Xanadu...)                     │
│  Subproduction  = dev/test instance; cloned from prod for safe change testing                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![ServiceNow Architecture](../../../assets/servicenow-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Instance model, node topology, MID Servers, platform components, and upgrade lifecycle.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and external systems.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Sizing guidelines, design standards, and best practices.</span></a>
</div>

---

## Instance Hierarchy

| Instance | Purpose |
|---|---|
| Dev | Development and initial testing |
| Test / UAT | Validation before production promotion |
| Production | Live environment |

---

## Platform Node Topology

