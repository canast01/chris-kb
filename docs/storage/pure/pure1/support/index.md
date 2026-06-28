---
tags:
  - pure
---
# Pure1 — Support

<div class="kb-summary">
Support reference covering Diagnostic Bundle Collection, Severity Definitions, Evergreen Support — What's Covered, Proactive Support Features, Escalation Path and 1 more sections.

*Applies to: Pure1*
</div>

## Escalation Path

```text
L1 Support Case (portal / phone)
  ↓ if unresolved after agreed time
L2 Senior Support Engineer (request via case notes)
  ↓ if design or architecture question
Solutions Architect / Systems Engineer (account team)
  ↓ if software defect confirmed
Engineering (TAC escalation — handled by Pure internally)
```

## Common Support Scenarios

| Scenario | Action |
|---|---|
| Drive failed | Pure1 auto-detects; auto-ships replacement (Evergreen). Confirm shipping address in Pure1 → Profile |
| Controller fault | Open Sev 1 by phone immediately |
| Unexpected performance degradation | Collect `puresupport create` bundle; open Sev 2 case |
| Purity upgrade failed / stuck | Open Sev 1 — do not power off array |
| Need to extend snapshot retention | Adjust snapshot policy in array UI; no case needed |
| Volume restore from snapshot | Perform self-service via CLI/UI; open case only if data appears missing |
