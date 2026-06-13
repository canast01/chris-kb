---
tags:
  - servicenow
---
# ServiceNow — Standard Changes

<div class="kb-summary">
Pre-approved standard change catalogue — low-risk repeatable changes that bypass full CAB review; includes template list and approval process.

*Applies to: ServiceNow*
</div>

```text
┌──────────────────────────────────── ServiceNow — Standard Changes ────────────────────────────────────┐
│                                                                                                       │
│   Definition: pre-approved low-risk repeatable changes; no CAB review required per occurrence         │
│   Template approved once by CAB; valid for 12 months; annual re-approval required                     │
│   Operator must follow the registered template exactly; deviation requires a Normal change            │
│   All standard changes still require a change record in ServiceNow for audit trail                    │
│                                                                                                       │
│   Common standard change examples                                                                     │
│   OS patching       Approved patch applied within approved maintenance window                         │
│   SSL cert renewal  Renewal of expiring certificate using existing approved process                   │
│   AD group change   Add/remove user from pre-approved security group                                  │
│   Firewall rule     Add rule matching approved firewall rule template (specific criteria)             │
│   DNS record add    Add A/CNAME/MX record for new or existing service                                 │
│   Service restart   Restart pre-approved service on pre-approved system within change window          │
│                                                                                                       │
│   Registration process (new template)                                                                 │
│   1. Draft template: describe the change, risk, impact, implementation steps, rollback                │
│   2. Submit to CAB for initial approval; include risk justification and test evidence                 │
│   3. CAB votes; if approved, template is added to the Standard Change Catalogue                       │
│   4. Template is published with a catalogue number (SC-XXXX) and effective date                       │
│   5. Teams may use the template without individual CAB review until the annual review date            │
│                                                                                                       │
│   Disqualifying criteria                                                                              │
│   Change affects a CI not listed in the template scope → Normal change required                       │
│   Change deviates from the registered implementation steps → Normal change required                   │
│   Change occurs outside the approved maintenance window → Normal or Emergency required                │
│                                                                                                       │
│   Key terms:                                                                                          │
│   Standard Change Catalogue = registry of all CAB-approved repeatable change templates                │
│   SC-XXXX       = standard change catalogue number; referenced in every occurrence record             │
│   occurrence    = individual use of a standard change template; still requires a change record        │
│   template scope= CI list and conditions under which the standard change template is valid            │
│   deviation     = any step or parameter that differs from the registered template                     │
│   annual review = yearly CAB re-approval of all standard change templates in the catalogue            │
│   maintenance window = pre-agreed time slot when changes to a service or system are permitted         │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
