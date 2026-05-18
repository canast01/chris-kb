# Change Communication

Structured approach to notifying stakeholders before, during, and after changes to maintain trust and minimize surprise.

```
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐   ┌─────────────────┐
│  Pre-change      │   │  Window Start    │   │ During Change    │   │  Post-change    │
│  Notice          │   │  Announcement    │   │ Updates          │   │  Report         │
│                  │   │                  │   │                  │   │                 │
│ 5+ days (Normal) │   │ [CHANGE-IN-PROG] │   │ Every 30 min     │   │ SUCCESS /       │
│ 24h reminder     │──►│ Slack/Teams ch.  │──►│ for P1-risk      │──►│ FAILED /        │
│ Email + ITSM     │   │ Status page →    │   │ changes          │   │ ROLLED BACK     │
│ All affected     │   │ "In progress"    │   │                  │   │ Lessons learned │
└──────────────────┘   └──────────────────┘   └──────────────────┘   └─────────────────┘
         │                                                                     │
         │                  ┌──────────────────────────────────────────────────┘
         ▼                  ▼
┌──────────────────────────────────┐
│       Audience Matrix                                                                │
│ End users / Owners / On-call /                                                       │
│ Mgmt (P1) / Security (sec chg)                                                       │
└──────────────────────────────────┘
```

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

```
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

## Window Start Announcement

```
[CHANGE-IN-PROGRESS] ITSM-XXXX
Starting: <service-name> maintenance window now open
Estimated end: <time UTC>
Implementing: <name>
Updates in: #ops-alerts
```

## Completion Announcement

```
[CHANGE-COMPLETE] ITSM-XXXX — <service-name>
Status: SUCCESS / FAILED / ROLLED BACK
Duration: <actual duration>
Impact: <confirmed impact>
Next steps: <monitoring period / follow-up ticket / none>
```

## Rollback Announcement

```
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
