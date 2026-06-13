---
tags:
  - servicenow
---
# ServiceNow — Change Templates

<div class="kb-summary">
Change request templates — standard, normal, and emergency change record templates ensuring consistent field completion and risk assessment.

*Applies to: ServiceNow*
</div>

```text
┌──────────────────────────────────── ServiceNow — Change Templates ────────────────────────────────────┐
│                                                                                                       │
│   Three templates: Standard (minimal fields), Normal (full RFC), Emergency (expedited)                │
│   Purpose: enforce consistent field completion; reduce missing-field rejections at CAB                │
│   All templates reference a change plan attachment for implementation and backout steps               │
│                                                                                                       │
│   Standard change template fields                                                                     │
│   Type = Standard; Catalogue = SC-XXXX; Assignment group; Planned start/end                           │
│   Short description: [SC-XXXX] <action> on <CI>                                                       │
│   Implementation notes: pre-populated from catalogue template; operator fills CI-specific values      │
│   Approval: auto-approved on submit if template is in catalogue and CI is in scope                    │
│                                                                                                       │
│   Normal change template fields                                                                       │
│   Type = Normal; Risk score (impact × likelihood); CAB meeting date                                   │
│   Business justification; affected CIs; stakeholder notification list                                 │
│   Implementation steps; test plan; backout plan (mandatory); rollback decision criteria               │
│   Attachments: change plan document; test evidence; CAB approval record                               │
│                                                                                                       │
│   Emergency change template fields                                                                    │
│   Type = Emergency; Business impact statement (why this cannot wait for CAB)                          │
│   ECAB approvers: Chair + 2; names and timestamps required before execution                           │
│   Backout plan: mandatory even for emergency; retrospective RFC number (raised post-implementation)   │
│                                                                                                       │
│   Key terms:                                                                                          │
│   RFC           = Request for Change; the ServiceNow change record                                    │
│   SC-XXXX       = standard change catalogue number; ties the record to the approved template          │
│   ECAB approvers= Emergency CAB members who provide expedited approval; minimum 3 required            │
│   backout plan  = documented rollback steps; required on all change types before execution            │
│   risk score    = impact × likelihood matrix score; drives CAB routing and documentation level        │
│   change plan   = attached document detailing all implementation, test, and rollback steps            │
│   retrospective = post-emergency documentation to formalise the change process after the fact         │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
