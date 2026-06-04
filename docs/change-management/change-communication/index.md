# Change Communication

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
```text
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
```bash
[CHANGE-ROLLBACK] ITSM-XXXX
Rolling back <service-name> change due to: <brief reason>
Estimated rollback duration: <time>
Service expected restored by: <time>
```
