# ServiceNow — Architecture

<div class="kb-summary">
ServiceNow is a multi-instance SaaS platform with fully isolated per-customer stacks. On-premises integration is handled via MID Servers — outbound-only Java agents that eliminate inbound firewall requirements.
</div>

```
┌───────────────────────────────── ServiceNow — Architecture Overview ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                    ServiceNow Architecture                                    │   │
│   │              SaaS: customer instance on ServiceNow cloud; no on-prem app servers              │   │
│   │            MID Server: on-prem JVM agent; polls ServiceNow ECC Queue for work items           │   │
│   │             Data: proprietary Glide DB (MySQL-based); accessed via GlideRecord API            │   │
│   │           API: REST Table API + Scripted REST API; HTTPS to instance.service-now.com          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    ServiceNow is SaaS; the only on-prem component is the optional MID Server                          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Cloud (ServiceNow SaaS)            │  │              On-Prem (Customer)             │   │
│   │             Now Platform runtime             │  │                MID Server JVM               │   │
│   │               Glide DB (MySQL)               │  │             MID polls ECC Queue             │   │
│   │                REST Table API                │  │               Discovery probes              │   │
│   │                Flow Designer                 │  │               JDBC/SNMP probes              │   │
│   │               Integration Hub                │  │            Firewall: outbound 443           │   │
│   │             GlideScript runtime              │  │               No inbound ports              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ServiceNow data centres (customer-invisible) · MID Server VM on-prem · outbound firewall             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Now Platform  = ServiceNow application runtime; hosts all ITSM apps                                  │
│  Glide DB      = ServiceNow proprietary DB layer; built on MySQL; accessed via GlideRecord            │
│  GlideRecord   = server-side JS API for DB CRUD; used in Business Rules and Scripts                   │
│  ECC Queue     = External Communication Channel; MID Server polls for work items                      │
│  MID Server    = on-prem Java agent; runs discovery, orchestration, and event probes                  │
│  Table API     = /api/now/table/{tableName}; REST CRUD for any ServiceNow table                       │
│  Flow Designer = drag-drop workflow builder; uses Actions and Triggers                                │
│  Integration Hub = connector library for Flow Designer; REST, JDBC, LDAP steps                        │
│  Discovery     = ITOM module; auto-populates CMDB by probing network devices                          │
│  Outbound only = MID Server initiates connection to ServiceNow; no inbound                            │
│  Instance URL  = https://customer.service-now.com; unique per customer tenant                         │
│  Prod/dev/test = separate ServiceNow instances; clone prod to dev for testing                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────── ServiceNow — Architecture Overview ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                    ServiceNow Architecture                                    │   │
│   │              SaaS: customer instance on ServiceNow cloud; no on-prem app servers              │   │
│   │            MID Server: on-prem JVM agent; polls ServiceNow ECC Queue for work items           │   │
│   │             Data: proprietary Glide DB (MySQL-based); accessed via GlideRecord API            │   │
│   │           API: REST Table API + Scripted REST API; HTTPS to instance.service-now.com          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    ServiceNow is SaaS; the only on-prem component is the optional MID Server                          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Cloud (ServiceNow SaaS)            │  │              On-Prem (Customer)             │   │
│   │             Now Platform runtime             │  │                MID Server JVM               │   │
│   │               Glide DB (MySQL)               │  │             MID polls ECC Queue             │   │
│   │                REST Table API                │  │               Discovery probes              │   │
│   │                Flow Designer                 │  │               JDBC/SNMP probes              │   │
│   │               Integration Hub                │  │            Firewall: outbound 443           │   │
│   │             GlideScript runtime              │  │               No inbound ports              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ServiceNow data centres (customer-invisible) · MID Server VM on-prem · outbound firewall             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Now Platform  = ServiceNow application runtime; hosts all ITSM apps                                  │
│  Glide DB      = ServiceNow proprietary DB layer; built on MySQL; accessed via GlideRecord            │
│  GlideRecord   = server-side JS API for DB CRUD; used in Business Rules and Scripts                   │
│  ECC Queue     = External Communication Channel; MID Server polls for work items                      │
│  MID Server    = on-prem Java agent; runs discovery, orchestration, and event probes                  │
│  Table API     = /api/now/table/{tableName}; REST CRUD for any ServiceNow table                       │
│  Flow Designer = drag-drop workflow builder; uses Actions and Triggers                                │
│  Integration Hub = connector library for Flow Designer; REST, JDBC, LDAP steps                        │
│  Discovery     = ITOM module; auto-populates CMDB by probing network devices                          │
│  Outbound only = MID Server initiates connection to ServiceNow; no inbound                            │
│  Instance URL  = https://customer.service-now.com; unique per customer tenant                         │
│  Prod/dev/test = separate ServiceNow instances; clone prod to dev for testing                         │
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


