---
tags:
  - servicenow
---
# ServiceNow — Templates

<div class="kb-summary">
ServiceNow templates — change request, incident, and CMDB entry templates for consistent record quality.
</div>

```text
┌─────────────────────────────────────── ServiceNow — Templates ────────────────────────────────────────┐
│                                                                                                       │
│   Four template types: change request, incident, change plan, and RCA                                 │
│   Templates ensure consistent record quality and reduce missing-field errors at submission            │
│   Change templates cover Standard, Normal, and Emergency change types                                 │
│   RCA template includes: incident summary, timeline, root cause, 5 Whys, corrective actions           │
│                                                                                                       │
│   Change templates                                                                                    │
│   Standard change  Pre-approved; minimal fields; task list pre-populated from catalogue entry         │
│   Normal change    Full RFC fields: risk score, CAB date, backout plan, deployment steps              │
│   Emergency change Expedited fields: business impact justification, ECAB approvers, retrospective     │
│                                                                                                       │
│   Incident templates                                                                                  │
│   P1 outage        Priority 1; impact = org-wide; assigned group = Major Incident team                │
│   Service degraded P2; impact = multi-user; SLA = 4h resolution target                                │
│   Security incident Assigned to SecOps; evidence-preservation steps pre-populated in template         │
│   Infra failure    Linked to CMDB CI; affected services auto-populated from service map               │
│                                                                                                       │
│   Change plan template                                                                                │
│   Pre/post checks; rollback section; stakeholder sign-off block; go/no-go criteria                    │
│   Used as the implementation plan attachment on all Normal and Emergency change records               │
│                                                                                                       │
│   Key terms:                                                                                          │
│   RFC           = Request for Change; ServiceNow change record type                                   │
│   RCA           = Root Cause Analysis; structured post-incident investigation document                │
│   5 Whys        = root cause analysis technique; iterative "why" questions to find root cause         │
│   CMDB CI       = Configuration Item in the CMDB; linked to incidents and changes for impact mapping  │
│   ECAB          = Emergency CAB; convenes within 30 min for production-impacting emergency changes    │
│   corrective actions = specific tasks assigned after RCA to prevent recurrence                        │
│   service map   = CMDB dependency map showing which services a CI supports                            │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-4">

<a class="kb-card" href="change-templates/"><strong>Change Templates</strong><span>Standard and emergency change request templates.</span></a>
<a class="kb-card" href="incident-templates/"><strong>Incident Templates</strong><span>Incident record templates for common failure types.</span></a>
<a class="kb-card" href="change-plan-template/"><strong>Change Plan Template</strong><span>Change plan template with pre/post checks, rollback section, and stakeholder sign-off.</span></a>
<a class="kb-card" href="rca-template/"><strong>RCA Template</strong><span>Root Cause Analysis template — incident summary, timeline, root cause, and corrective actions.</span></a>

</div>
