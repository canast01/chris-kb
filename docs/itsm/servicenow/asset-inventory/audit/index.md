---
tags:
  - servicenow
---
# Asset Audit Process


<div class="kb-summary">
Asset Audit Process reference covering Overview, Audit Scope and Frequency, Discovery Tools, CMDB Reconciliation Steps, Discrepancy Tracking and 1 more sections.

*Applies to: ServiceNow*
</div>
```text
┌────────────────────────────── Project Management Asset Inventory Audit ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │               Asset Inventory: Project Management Asset Inventory Audit platform              │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │            Management: Project Management Asset Inventory Audit management console            │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Project Management Asset Inventory Audit infrastructure · management network · monitoring│
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Asset Inventory    = Project Management Asset Inventory Audit platform overview and core concepts  │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Overview

Regular asset audits ensure your CMDB reflects reality. Without periodic reconciliation, configuration drift accumulates — shadow IT, decommissioned hardware still listed as active, and undocumented dependencies all erode trust in asset data. A structured audit process keeps records accurate and supports change, incident, and capacity management.

---

## Audit Scope and Frequency

Define scope before starting. Audits can cover a single environment or span the full estate.

| Audit Type           | Frequency   | Scope                                |
|----------------------|-------------|--------------------------------------|
| Spot check           | Weekly      | High-risk or recently changed CIs    |
| Environment scan     | Monthly     | Single environment (prod/staging)    |
| Full estate          | Quarterly   | All CIs across all environments      |
| Physical walkthrough | Annually    | Data centre racks, network gear      |

---

## Discovery Tools

Use automated discovery to reduce manual effort and catch undocumented assets.

- **Nmap / Nessus** — network-layer host discovery
- **Lansweeper / Snipe-IT** — agent and agentless inventory
- **Ansible fact gathering** — pull OS, hardware, and software facts at scale
- **AWS Config / Azure Resource Graph / GCP Asset Inventory** — cloud estate
- **ServiceNow Discovery** — for environments already on the platform

Run scans from a consistent source host to avoid NAT and firewall blind spots. Schedule during low-traffic windows to avoid false positives from load-related timeouts.

---

## CMDB Reconciliation Steps

Once discovery data is collected, compare it against the existing CMDB.

- [ ] Export current CMDB CI list (filter by environment and CI class)
- [ ] Run discovery scan and export results
- [ ] Diff the two datasets — identify CIs in CMDB but not discovered, and vice versa
- [ ] Investigate discrepancies (see table below)
- [ ] Update CMDB with confirmed corrections
- [ ] Record audit run date and findings in the audit log

Use a spreadsheet or dedicated reconciliation tool to track row-by-row status: `Matched`, `CMDB Only`, `Discovered Only`, `Attribute Mismatch`.

---

## Discrepancy Tracking

Not all discrepancies are errors. Some require investigation before action.

| Discrepancy Type    | Likely Cause                         | Action                              |
|---------------------|--------------------------------------|-------------------------------------|
| CMDB Only           | Decommissioned but not removed       | Verify offline; retire CI           |
| Discovered Only     | Shadow IT or missed onboarding       | Assess, document, and add to CMDB   |
| Attribute mismatch  | Manual update drift                  | Correct CMDB from authoritative source |
| Status mismatch     | CI marked active but unreachable     | Check monitoring; update status     |

Log every discrepancy with a ticket reference. Assign an owner for resolution within an agreed SLA (e.g., 5 business days for non-critical CIs).

---

## Audit Sign-Off and Reporting

At the end of each audit cycle, produce a summary report covering:

- Total CIs audited
- Number of discrepancies found and resolved
- Outstanding items with owner and target resolution date
- CMDB accuracy score (matched count / total count)

Distribute to the Asset Manager and relevant team leads. Store in the audit log directory with the date in the filename (e.g., `audit-2026-05-07.md`).
