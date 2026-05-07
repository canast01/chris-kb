# Emergency Change Procedure

Emergency changes bypass the standard CAB cycle to address active outages or critical security incidents. All approvals and documentation occur during or immediately after implementation.
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

```
1. Start implementation timer (log in ticket)
2. Apply fix / change
3. Validate recovery (service health, smoke tests)
4. Confirm with stakeholders that service is restored
5. Remove any temporary workarounds (firewall rules, bypasses)
```

## Post-Implementation — Required Within 24 Hours

- [ ] ITSM ticket updated with exact change made (commands run, files edited, config changed)
- [ ] Rollback plan documented (even if not used)
- [ ] Root cause identified and linked to problem ticket
- [ ] Formal post-incident review scheduled (within 5 business days for P1)
- [ ] Change closure approved by service owner

## Post-Incident Review Template

```markdown
Emergency Change:    ITSM-XXXX
Date/Time:           2026-05-06 02:14 UTC
Duration:            47 minutes
Approver:            Jane Smith (on-call manager) — approved via Slack 02:18 UTC

Issue:               PostgreSQL replica fell behind; primary OOM-killed
Change Made:         Restarted postgres with increased shared_buffers; promoted replica temporarily
Rollback:            Revert shared_buffers to original value; redeploy replica from backup
Outcome:             Service restored 02:57 UTC; RTO target met
Prevention:          Memory alarm threshold lowered; auto-restart added to systemd unit
Follow-up tickets:   PROB-4421 (root cause), TASK-8874 (memory tuning)
```

## Guardrails

- Emergency changes must still have a ticket — verbal approval alone is insufficient
- No permanent changes to security controls without security sign-off, even in emergency
- All firewall bypasses and temporary rules must be reversed within 24 hours or formally reviewed
