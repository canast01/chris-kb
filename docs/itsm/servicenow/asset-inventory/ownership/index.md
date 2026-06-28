---
tags:
  - servicenow
---
# Asset Ownership and Accountability

<div class="kb-summary">
Asset Ownership and Accountability reference covering Overview, Ownership Model, Ownership Assignment Process, Ownership Handover, Cost Allocation and 1 more sections.

*Applies to: ServiceNow*
</div>

```d2
direction: down

ownership_model: "Ownership Model" {shape: rectangle}
ownership_assignment_process: "Ownership Assignment Process" {shape: rectangle}
ownership_handover: "Ownership Handover" {shape: rectangle}
cost_allocation: "Cost Allocation" {shape: rectangle}
accountability_and_compliance: "Accountability and Compliance" {shape: rectangle}

ownership_model -> ownership_assignment_process: uses
ownership_assignment_process -> ownership_handover: uses
ownership_handover -> cost_allocation: uses
cost_allocation -> accountability_and_compliance: uses
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
