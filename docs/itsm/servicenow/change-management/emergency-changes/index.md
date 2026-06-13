---
tags:
  - servicenow
---
# ServiceNow — Emergency Changes

<div class="kb-summary">
Emergency change process — expedited approval path for urgent production fixes; CAB override criteria, evidence requirements, and post-implementation review.
</div>

```text
┌─────────────────────────────────── ServiceNow — Emergency Changes ────────────────────────────────────┐
│                                                                                                       │
│   Trigger: active P1/P2 production impact where delay causes unacceptable business risk               │
│   Approval path: ECAB Chair + 2 approvers (e.g. Tech Lead + Service Owner) — convene within 30 min    │
│   Post-implementation: retrospective RFC within 24h; PIR within 5 business days                       │
│   Evidence required: business impact statement, risk mitigation, backout plan before execution        │
│                                                                                                       │
│   CAB override criteria                                                                               │
│   Active production outage (P1) with no resolution path without a change                              │
│   Security breach requiring immediate remediation (patch, firewall rule, account disable)             │
│   Data loss risk or compliance deadline that cannot wait for next CAB meeting                         │
│   Not eligible: planned work accelerated due to convenience — must be a genuine emergency             │
│                                                                                                       │
│   Expedited approval process                                                                          │
│   1. Raise emergency change record in ServiceNow; set Type = Emergency                                │
│   2. Populate: short description, business impact, implementation steps, backout plan                 │
│   3. Contact ECAB Chair to convene; minimum 3 approvers (Chair + 2); can approve via phone/chat       │
│   4. Document approver names + timestamps in the change record before execution starts                │
│   5. Execute change; update record with live implementation notes                                     │
│   6. Post-change: raise retrospective RFC; schedule PIR within 5 business days                        │
│                                                                                                       │
│   Risk controls                                                                                       │
│   Backout plan must be approved before execution even in emergency scenarios                          │
│   Implementation window: max 2 hours without additional approval; escalate if overrunning             │
│   All emergency changes reviewed at next standard CAB meeting for process compliance                  │
│                                                                                                       │
│   Key terms:                                                                                          │
│   ECAB         = Emergency CAB; subset who can convene within 30 min for urgent changes               │
│   retrospective RFC = change record raised after an emergency fix to formalise documentation          │
│   PIR          = Post-Implementation Review; lessons learned session after the change                 │
│   CAB Chair    = senior change authority; authorises ECAB activation and emergency approvals          │
│   backout plan = documented rollback steps approved before change is authorised to start              │
│   P1           = Priority 1 incident; full production outage affecting all or most users              │
│   implementation window = scheduled execution time; must be agreed with ECAB before starting          │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
