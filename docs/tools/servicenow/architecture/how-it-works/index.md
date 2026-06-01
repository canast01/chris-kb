# ServiceNow — How It Works

ServiceNow is delivered as a multi-instance SaaS platform running on dedicated infrastructure per customer. Each customer receives isolated database, application, and storage layers — there is no shared compute between tenants.

---

## Multi-Instance Cloud Model

| Characteristic | Detail |
|---|---|
| Database engine | MariaDB (MySQL-compatible) |
| App server | Java / Jetty |
| Storage | SAN-backed, encrypted at rest |
| Redundancy | Active-active within a data center zone |
| Regions | Americas, EMEA, AP-Southeast, GovCloud |
| SLA | 99.8% uptime (standard), 99.95% (Hi) |

Each instance receives a URL in the form `https://<instance-name>.service-now.com`.

---

## Instance Hierarchy

Most enterprise deployments maintain a minimum of three instances arranged in a promotion pipeline:

```mermaid
flowchart LR
    DEV["Dev Instance\n(sub-production)"]
    TEST["Test / UAT Instance\n(sub-production)"]
    PROD["Production Instance"]

    DEV -- "Update Set export" --> TEST
    TEST -- "Update Set export" --> PROD

    subgraph Sub-Production
        DEV
        TEST
    end
```
┌────────────────────────────────────── ServiceNow — How It Works ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             ServiceNow Request and Automation Flow                            │   │
│   │        User/API → HTTPS → Now Platform → GlideDB; Business Rules fire on record change        │   │
│   │            Incident: create → categorise → assign → resolve → close (ITIL workflow)           │   │
│   │           MID Server: ECC Queue poll → probe execution → result posted back to SNOW           │   │
│   │              Flow Designer: trigger (table record event) → actions → integrations             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    ServiceNow processes three parallel flows: ITSM, automation, and discovery                         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          ITSM Flow          │  │       Automation Flow       │  │        Discovery Flow       │   │
│   │     User submits ticket     │  │      Flow trigger fires     │  │        Schedule runs        │   │
│   │      Business Rule runs     │  │       Actions execute       │  │        ECC Queue item       │   │
│   │       Assignment rule       │  │        REST call out        │  │        MID probe runs       │   │
│   │       SLA clock starts      │  │       Response parsed       │  │        Result posted        │   │
│   │      Notification sent      │  │        Record updated       │  │         CMDB updated        │   │
│   │       Resolve / close       │  │      Log entry written      │  │        CI discovered        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ServiceNow cloud infra · MID Server VM on-prem · SMTP relay · LDAP/AD DCs                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Business Rule = server-side GlideScript triggered on DB insert/update/delete/query                   │
│  Assignment rule = auto-assigns incident to group based on category/subcategory                       │
│  SLA clock    = ServiceNow tracks breach time against SLA definition                                  │
│  Flow trigger  = event that starts a Flow Designer flow (e.g. record insert)                          │
│  Action        = Flow Designer step: REST call, approval, sub-flow, script                            │
│  ECC Queue     = ServiceNow table; MID Server polls for probe/sensor commands                         │
│  Discovery probe = MID Server script that probes target IP for CI data                                │
│  CI            = Configuration Item; managed in CMDB (server, app, service, etc.)                     │
│  GlideRecord   = JS API for DB access: gr.addQuery(); gr.query(); gr.next()                           │
│  Notification  = email/SMS/push triggered by SNOW event or Business Rule                              │
│  Resolve       = final active state before Close; SLA stops on resolve                                │
│  CMDB update   = Discovery writes CI attributes to CMDB after probe results                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

MID Servers are customer-managed Java agents deployed on-premises. All communication is **outbound from MID Server to the instance** (port 443), eliminating inbound firewall requirements.

---

## Key Platform Components

### Now Platform (Core)

| Component | Function |
|---|---|
| Workflow Engine | Visual process automation (Flow Designer / Legacy WF) |
| Service Catalog | Self-service request portal |
| Notification Engine | Email, SMS, push via notification rules |
| Scripting Runtime | Server-side JavaScript (Rhino/GraalVM) |
| Update Set Manager | Change packaging and instance promotion |
| Scheduled Jobs | Background execution framework |

### ITSM

| Process | Key Table | SLA Driven |
|---|---|---|
| Incident Management | `incident` | Yes |
| Problem Management | `problem` | No |
| Change Management | `change_request` | No |
| Service Request | `sc_request` / `sc_req_item` | Yes |
| Knowledge Base | `kb_knowledge` | No |

### CMDB

The Configuration Management Database stores Configuration Items (CIs) and their relationships.

- Base CI class: `cmdb_ci`
- Relationship table: `cmdb_rel_ci`
- Identification and Reconciliation Engine (IRE) deduplicates data from multiple discovery sources

### Discovery

Automated infrastructure discovery using MID Servers:

1. Scheduled probes run against IP ranges or cloud accounts
2. MID Server executes discovery scripts (SSH, WMI, SNMP, APIs)
3. Payload data is parsed and mapped to CMDB CI classes via IRE
4. Reconciliation order enforced by source ranking (authoritative source wins)

---

## Upgrade Lifecycle

ServiceNow releases two major versions per year. Cloud instances are auto-upgraded by ServiceNow on a negotiated schedule.

```mermaid
flowchart TD
    A["Upgrade Announcement\n(~3 months lead)"]
    B["Review Release Notes\n& Upgrade Planner"]
    C["Upgrade Sub-Production\n(Dev first)"]
    D["Regression Testing\n(ATF automated + manual)"]
    E["Upgrade UAT"]
    F["UAT Sign-off"]
    G["Schedule Production Upgrade\nwith ServiceNow"]
    H["Production Upgrade\n(maintenance window)"]
    I["Post-Upgrade Validation"]

    A --> B --> C --> D --> E --> F --> G --> H --> I
```

| Phase | Owner | Duration |
|---|---|---|
| Release notes review | Platform team | 1 week |
| Dev upgrade + testing | Platform team + developers | 2–3 weeks |
| UAT upgrade + sign-off | Business stakeholders | 1–2 weeks |
| Production upgrade scheduling | ServiceNow + customer | 1 week |
| Production upgrade window | ServiceNow (automated) | 2–4 hours |
| Post-upgrade validation | Platform team | 1 day |
