---
tags:
  - servicenow
---
# ServiceNow — Change Management Procedures

<div class="kb-summary">
ServiceNow change request lifecycle — raising, categorising, routing for CAB approval, implementing, and closing change records.
</div>

```text
┌─────────────────────────────────── ServiceNow — Change Procedures ────────────────────────────────────┐
│                                                                                                       │
│   Change lifecycle: Draft → Assess → Authorise → Scheduled → Implement → Review → Closed              │
│   Three approval paths: Standard (auto), Normal (CAB weekly), Emergency (ECAB ≤30 min)                │
│   Mandatory fields: short description, risk score, backout plan, planned start/end, CI link           │
│   All changes linked to a CMDB CI; impact auto-derived from service map dependencies                  │
│                                                                                                       │
│   Raising a change record                                                                             │
│   Navigate to Change > Create New; select change type (Standard / Normal / Emergency)                 │
│   Fill mandatory fields: assignment group, affected CI, planned start/end, implementation steps       │
│   Attach backout plan as a note or work note attachment before submitting for approval                │
│   Risk assessment: score impact (1–5) × likelihood (1–5) = risk score; auto-routes by threshold       │
│                                                                                                       │
│   CAB process (Normal changes)                                                                        │
│   Submit change at least 48h before CAB meeting to ensure it appears on the agenda                    │
│   CAB reviews: risk score, implementation steps, rollback plan, testing evidence                      │
│   CAB decision: Approved / Rejected / Deferred; decision recorded in the change record                │
│   Post-CAB: notify stakeholders; confirm maintenance window; execute in agreed slot                   │
│                                                                                                       │
│   Implementation and closeout                                                                         │
│   Update change record with live implementation notes during execution                                │
│   Post-change validation: run test cases; confirm service health; update CI state in CMDB             │
│   Close with outcome: Successful / Unsuccessful / Partial; attach test evidence                       │
│   PIR required for: all Emergency changes and any Normal change classified Unsuccessful               │
│                                                                                                       │
│   Key terms:                                                                                          │
│   CAB          = Change Advisory Board; weekly review body for Normal changes                         │
│   CMDB CI      = Configuration Item; infrastructure asset linked to the change record                 │
│   risk score   = impact × likelihood product; drives approval path and documentation level            │
│   work note    = internal note on a ServiceNow record; not visible to end users                       │
│   PIR          = Post-Implementation Review; lessons learned for significant changes                  │
│   service map  = CMDB dependency graph showing which services a CI supports                           │
│   change freeze= period when no changes are permitted; set via CAB and communicated in advance        │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
