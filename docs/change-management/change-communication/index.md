# Change Communication


<div class="kb-summary">
Structured approach to notifying stakeholders before, during, and after changes to maintain trust and minimize surprise.
</div>

## Communication Timeline

| Phase | When | Audience | Channel |
|---|---|---|---|
| Pre-change notice | 5+ business days (Normal), 24h (Standard) | All affected users, service owners | Email + ITSM notification |
| Reminder | 24h before window | Same audience | Email |
| Window start | At start of change window | On-call team, service owners | Slack/Teams incident channel |
| Progress updates | Every 30 min for P1-risk changes | Service owners | Slack/Teams |
| Completion notice | Immediately on completion | All affected users | Email + status page |
| Post-change summary | Next business day | Management, stakeholders | Email |

## Pre-Change Notification Template

```yaml
Subject: [Planned Maintenance] <Service Name> — <Date> <Start Time> UTC

Service:        <service-name>
Window:         <start-datetime UTC> to <end-datetime UTC>
Expected impact: <None / Degraded performance / Service interruption>
Duration:       <estimated duration>
Change:         <one sentence description>
Rollback:       <one sentence rollback summary>
Contact:        <implementer name and channel>

If you have questions or concerns please reply by <date 2 days before window>.
```
```
┌──────────────────────────────────────── Change Communication ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Communication plan: notify stakeholders before, during, and after each change         │   │
│   │          Downtime notice: send at T-7d, T-1d, T-1h; post-change update on completion          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Pre-Change         │  │        During Change        │  │         Post-Change         │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │     T-7d: initial notice    │  │     T+0: change started     │  │       Change completed      │   │
│   │        T-1d: reminder       │  │        Status updates       │  │       Service restored      │   │
│   │     T-1h: final reminder    │  │         Delay comms         │  │       Outcome summary       │   │
│   │      Affected services      │  │        Rollback comms       │  │         Action items        │   │
│   │     Contact for queries     │  │       Bridge/chat link      │  │        PIR scheduled        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                   Pre-change email template:                                  │   │
│   │               Subject: [Planned Maintenance] <service> — <date> <time> <timezone>             │   │
│   │             Body: What, When, Duration, Affected services, Contact, Rollback trigger          │   │
│   │                                       Post-change email:                                      │   │
│   │               Subject: [Completed] <service> maintenance — result: SUCCESS/FAILED             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Stakeholder map = Who needs to know: business owners, service users, on-call teams                 │
│    Downtime notice = Mandatory for any user-impacting change; minimum T-24h notice                    │
│    Bridge call     = Shared conference line during change; key contacts join for live comms           │
│    Rollback comms  = Notify immediately if rollback triggered; give new ETA for service restore       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Rollback Announcement

```bash
[CHANGE-ROLLBACK] ITSM-XXXX
Rolling back <service-name> change due to: <brief reason>
Estimated rollback duration: <time>
Service expected restored by: <time>
```

## Audience Matrix

| Stakeholder | Pre-notice | Window start | Completion | Rollback |
|---|---|---|---|---|
| End users (if impacted) | Yes | Status page | Yes | Yes |
| Service owner | Yes | Yes | Yes | Yes |
| On-call team | Yes | Yes | Yes | Yes |
| Management (P1 risk) | Yes | No | Yes | Yes |
| Security team (if security change) | Yes | No | Yes | Yes |

## Status Page Update

For any change with user-visible impact:

1. Post planned maintenance notice (when RFC approved)
2. Update to "In progress" at window start
3. Update to "Resolved/Completed" on success
4. Use "Investigating" status if rollback triggered

## Checklist

- [ ] Pre-change notice sent to all affected parties
- [ ] Reminder sent 24h before window
- [ ] Status page updated (if user-impacting)
- [ ] Window start announced in team channel
- [ ] Completion or rollback outcome communicated
- [ ] ITSM ticket updated with communication timestamps
