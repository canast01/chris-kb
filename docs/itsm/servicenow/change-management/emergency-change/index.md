# Emergency Change Procedure


<div class="kb-summary">
Emergency changes bypass the standard CAB cycle to address active outages or critical security incidents. All approvals and documentation occur during or immediately after implementation.
</div>

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

```text
┌────────────────────────────────────────── Emergency Change ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Emergency change: expedited process for P1/P2 incidents requiring immediate action      │   │
│   │       ECAB approval: verbal/email from ECAB quorum; document before or immediately after      │   │
│   │          Retrospective RFC required within 24 hours; post-change review within 5 days         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Emergency Change Criteria           │  │                 ECAB Process                │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │            Active P1/P2 incident             │  │          Call ECAB members (min 2)          │   │
│   │             Service unavailable              │  │            Explain risk + action            │   │
│   │           Imminent security threat           │  │           Verbal or email approval          │   │
│   │             Regulatory deadline              │  │             Execute immediately             │   │
│   │            No time for normal CAB            │  │           Document retrospectively          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   │     Timeline     │      Action      │       Owner       │     Artefact     │     Deadline     │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │       T=0        │Incident declared │    Incident mgr   │    P1 ticket     │    Immediate     │   │
│   │     T+30 min     │  ECAB approval   │     Change mgr    │   Approval log   │      30 min      │   │
│   │     T+24 hr      │    RFC raised    │     Change mgr    │    Retro RFC     │     24 hours     │   │
│   │     T+5 days     │       PIR        │     Change mgr    │    PIR report    │ 5 business days  │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    ECAB         = Emergency CAB; subset of CAB members available 24/7 for emergency approval          │
│    Retrospective= RFC created after emergency change to formalise the record                          │
│    PIR          = Post-Implementation Review; required after emergency changes within 5 days          │
│    Quorum       = Minimum 2 ECAB members must approve; single approver insufficient                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Guardrails

- Emergency changes must still have a ticket — verbal approval alone is insufficient
- No permanent changes to security controls without security sign-off, even in emergency
- All firewall bypasses and temporary rules must be reversed within 24 hours or formally reviewed
