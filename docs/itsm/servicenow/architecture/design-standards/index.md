---
tags:
  - architecture
  - servicenow
---
# ServiceNow — ITSM Standards


<div class="kb-summary">
This page documents operational standards enforced within the ServiceNow platform, including incident priority, change risk scoring, CMDB naming conventions, SLA targets, and change governance procedures.

*Applies to: ServiceNow*
</div>
![ServiceNow — ITSM Standards](../../../../assets/itsm-servicenow-architecture-design-standards-index.svg)


---

## Incident Priority Matrix

Priority is calculated from Impact × Urgency. ServiceNow evaluates this automatically on incident submission if auto-calculation is enabled (Business Rule: **Calculate Priority**).

| | **Urgency 1 — Critical** | **Urgency 2 — High** | **Urgency 3 — Medium** | **Urgency 4 — Low** |
|---|---|---|---|---|
| **Impact 1 — Enterprise** | P1 — Critical | P1 — Critical | P2 — High | P3 — Medium |
| **Impact 2 — Department** | P1 — Critical | P2 — High | P3 — Medium | P4 — Low |
| **Impact 3 — Individual** | P2 — High | P3 — Medium | P4 — Low | P4 — Low |

### Definitions

**Impact** — breadth of the disruption:

| Value | Definition |
|---|---|
| 1 — Enterprise | Multiple departments or a business-critical service unavailable |
| 2 — Department | One department or a significant service degraded |
| 3 — Individual | Single user or minor function affected |

**Urgency** — speed at which the business impact increases:

| Value | Definition |
|---|---|
| 1 — Critical | No workaround; business operations halting now |
| 2 — High | Workaround available but costly; significant degradation |
| 3 — Medium | Workaround available; limited business impact |
| 4 — Low | Cosmetic or trivial issue; business fully operational |

---

## SLA Targets

SLA clocks start when the incident moves to **In Progress** and pause when state is **On Hold - Awaiting Vendor** or **On Hold - Awaiting User**.

| Priority | Initial Response | Acknowledgement | Resolution Target |
|---|---|---|---|
| P1 — Critical | 15 minutes | 30 minutes | 4 hours |
| P2 — High | 30 minutes | 1 hour | 8 hours |
| P3 — Medium | 2 hours | 4 hours | 3 business days |
| P4 — Low | 8 hours | 1 business day | 10 business days |

**SLA breach notifications:**

- 75% elapsed — notification to assignee and assignment group manager
- 90% elapsed — escalation to service owner
- 100% elapsed (breach) — auto-escalation to director; OLA breach recorded

---

## Change Risk Scoring

Change risk is assessed using ServiceNow's **Change Risk Assessment** questionnaire. Risk score drives the approval workflow:

| Risk Score | Risk Level | CAB Required | Standard Window |
|---|---|---|---|
| 0–25 | Low | No | Any approved window |
| 26–50 | Medium | Optional (Delegate) | Approved window only |
| 51–75 | High | Yes | Approved change window |
| 76–100 | Critical | Full CAB + ECAB | Emergency window |

### Risk Assessment Factors (weighted inputs)

| Factor | Weight |
|---|---|
| Number of CIs affected | 20% |
| Is the CI in production? | 20% |
| Has this change been done before? | 15% |
| Rollback plan documented? | 15% |
| Testing in sub-production completed? | 15% |
| Off-hours implementation? | 15% |

---

## Change Types

| Type | Description | Auto-Approval | CAB |
|---|---|---|---|
| Standard | Pre-approved, low-risk, repeatable | Yes | No |
| Normal | Assessed, planned change | No | Yes (if High/Critical) |
| Emergency | Urgent fix, post-implementation review | CAB Chair only | ECAB |

**Standard Changes** must be registered in the Standard Change Catalog with a documented template before they can bypass the approval workflow.

---

## Change Advisory Board (CAB) Workflow

```mermaid
flowchart TD
    A["Change Request Submitted\n(Normal or Emergency)"]
    B["Risk Assessment\nCompleted by Submitter"]
    C{Risk Level}
    D["Low / Medium:\nDelegate Approval\n(Change Manager)"]
    E["High / Critical:\nCAB Review Queue"]
    F["CAB Meeting\n(Weekly - Wednesday 14:00)"]
    G{CAB Decision}
    H["Approved:\nSchedule Implementation"]
    I["Rejected / Deferred:\nReturn to Submitter"]
    J["Emergency:\nECAB Chair + 2 Members\n(async approval)"]
    K["Implementation\nin Change Window"]
    L["Post-Implementation Review\n(PIR within 5 business days)"]

    A --> B --> C
    C -- Low/Medium --> D --> H
    C -- High/Critical --> E --> F --> G
    C -- Emergency --> J --> G
    G -- Approved --> H
    G -- Rejected --> I
    H --> K --> L
```


| Token | Values | Example |
|---|---|---|
| `site` | 3-letter site code (LON, NYC, SYD, AWS, AZR) | `LON` |
| `type` | Server type abbreviation | `SRV`, `DB`, `LB`, `FW`, `SW` |
| `function` | Functional descriptor | `WEB`, `APP`, `MQ`, `CACHE` |
| `sequence` | Zero-padded 2-digit number | `01`, `02` |

**Examples:**

| CI Name | Meaning |
|---|---|
| `LON-SRV-WEB-01` | London data center, server, web tier, unit 1 |
| `NYC-DB-MYSQL-02` | New York, database server, MySQL, unit 2 |
| `AWS-LB-APP-01` | AWS hosted, load balancer, application tier, unit 1 |
| `AZR-SRV-APP-03` | Azure hosted, server, application tier, unit 3 |

### CI Class Mapping

| Infrastructure Type | CMDB Class |
|---|---|
| Physical server | `cmdb_ci_server` |
| Virtual machine | `cmdb_ci_vmware_instance` |
| Cloud VM (AWS) | `cmdb_ci_ec2_instance` |
| Cloud VM (Azure) | `cmdb_ci_azure_virtualmachine` |
| Network device | `cmdb_ci_netgear` / `cmdb_ci_ip_switch` |
| Database | `cmdb_ci_database` |
| Application | `cmdb_ci_appl` |
| Business service | `cmdb_ci_service` |

### Prohibited Naming Patterns

- Generic names: `server1`, `test`, `temp`, `myapp`
- IP addresses as CI names
- Spaces or special characters (underscores permitted)
- Duplicate names within the same CI class

---

## CMDB Data Quality Standards

| Attribute | Mandatory | Source |
|---|---|---|
| Name | Yes | Discovery / manual |
| IP Address | Yes (servers) | Discovery |
| OS | Yes (servers) | Discovery |
| Owner (support group) | Yes | Manual / LDAP |
| Environment | Yes | Discovery tag / manual |
| Location | Yes | Discovery / manual |
| Managed by | Recommended | LDAP / manual |

CI completeness is measured by the **CMDB Health Dashboard**. Target: >90% completeness score for Tier 1 CIs.

---

## See also

- [Servicenow — Deploy](../../deploy/)
