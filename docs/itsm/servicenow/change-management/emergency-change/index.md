---
tags:
  - servicenow
---
# Emergency Change Procedure

<div class="kb-summary">
Emergency changes bypass the standard CAB cycle to address active outages or critical security incidents. All approvals and documentation occur during or immediately after implementation.

*Applies to: ServiceNow*
</div>

```d2
direction: down

trigger_conditions: "Trigger Conditions" {shape: rectangle}
preimplementation_30_minutes: "Pre-Implementation (< 30 minutes)" {shape: rectangle}
ecab_minimum_approval: "eCAB — Minimum Approval" {shape: rectangle}
implementation: "Implementation" {shape: rectangle}
guardrails: "Guardrails" {shape: rectangle}

trigger_conditions -> preimplementation_30_minutes: uses
preimplementation_30_minutes -> ecab_minimum_approval: uses
ecab_minimum_approval -> implementation: uses
implementation -> guardrails: uses
```

## Trigger Conditions

| Condition | Example |
|---|---|
| P1/Critical outage | Production service down, SLA breach imminent |
| Security incident | Active exploit, unauthorized access, ransomware |
| Data integrity risk | Corruption spreading, backup failure during backup window |
| Compliance breach | Audit control failure requiring immediate remediation |

## Pre-Implementation (< 30 minutes)

1. **Declare emergency change** — open ITSM ticket; set type = Emergency
2. **Notify on-call manager** — get verbal or chat approval (document who approved and when)
3. **eCAB approval** — email/Slack to eCAB members; single approver required if P1
4. **Brief rollback plan** — even a one-line rollback is required before starting
5. **Notify affected stakeholders** — status page, incident channel

## eCAB — Minimum Approval

| Scenario | Minimum Approver |
|---|---|
| P1 service outage | On-call manager OR service owner |
| Security incident | CISO or security lead |
| Data risk | DBA lead or data owner |
| All others | Team lead + one peer |

## Implementation

## Guardrails

- Emergency changes must still have a ticket — verbal approval alone is insufficient
- No permanent changes to security controls without security sign-off, even in emergency
- All firewall bypasses and temporary rules must be reversed within 24 hours or formally reviewed
