---
tags:
  - servicenow
---
# Asset Ownership and Accountability


<div class="kb-summary">
Asset Ownership and Accountability reference covering Overview, Ownership Model, Ownership Assignment Process, Ownership Handover, Cost Allocation and 1 more sections.
</div>
```text
┌──────────────────────────── Project Management Asset Inventory Ownership ─────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │             Asset Inventory: Project Management Asset Inventory Ownership platform            │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │          Management: Project Management Asset Inventory Ownership management console          │   │
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
│    Physical: Project Management Asset Inventory Ownership infrastructure · management network · moni  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Asset Inventory    = Project Management Asset Inventory Ownership platform overview and core conc  │
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

Every CI in the CMDB must have a named owner. Ownership determines who approves changes, who is accountable during incidents, who carries the cost, and who authorises decommission. Unowned assets are a governance risk and a common source of audit findings.

---

## Ownership Model

Use a two-level ownership model: Technical Owner and Business Owner.

| Role             | Responsibility                                                   |
|------------------|------------------------------------------------------------------|
| Technical Owner  | Day-to-day operations, patching, incident response, change approval |
| Business Owner   | Funding, strategic direction, decommission approval              |
| Cost Centre       | Chargeback target; not a person but must be set on every CI     |

Both owners must be individuals (not team aliases) so that accountability is unambiguous. Use team aliases only in the notification fields, not the owner fields.

---

## Ownership Assignment Process

When a new CI is onboarded:

- [ ] Identify technical owner from the team responsible for the service
- [ ] Identify business owner from the sponsoring department
- [ ] Confirm cost centre code with Finance
- [ ] Populate all three fields in CMDB before setting status to Active
- [ ] Send confirmation email to both owners with a link to the CI record
- [ ] Set a 90-day review reminder for newly onboarded CIs

For bulk imports, include owner fields in the import template. Do not complete an import that leaves owner fields blank.

---

## Ownership Handover

When an owner changes (role change, team restructure, leaver):

- [ ] Identify replacement owner before the current owner departs
- [ ] Raise a CMDB update ticket with old and new owner details
- [ ] Update CMDB within 5 business days of the handover date
- [ ] Notify the new owner by email with CI list and key responsibilities
- [ ] Update any related service catalogue entries and escalation paths
- [ ] Run a 30-day check-in with the new owner to confirm no issues

| Trigger Event         | Action Required                         | SLA            |
|-----------------------|-----------------------------------------|----------------|
| Staff departure       | Replace owner before last day           | Before last day|
| Team restructure      | Bulk update during transition project   | Within 2 weeks |
| Service transfer      | Formal handover document required       | Before go-live |
| Acquisition / merger  | Asset owner mapping exercise            | Within 30 days |

---

## Cost Allocation

Ownership drives chargeback. The cost centre on a CI determines which department is billed for:

- Cloud compute and storage costs
- Licensing and support contract costs
- Hardware depreciation
- Managed service fees

Review cost allocation quarterly. Ensure CIs transferred between teams have their cost centre updated promptly — delayed updates create reconciliation disputes at financial year-end.

---

## Accountability and Compliance

During audits, every CI must be traceable to a responsible person.

- [ ] Confirm no CIs have blank owner fields before each quarterly audit
- [ ] Run an "unowned CI" report monthly and assign owners within 10 business days
- [ ] Include ownership accuracy in the CMDB health dashboard
- [ ] Escalate unresolved unowned CIs to the line manager of the relevant team
- [ ] Document owner assignment rationale for shared infrastructure (e.g., shared DB clusters)
