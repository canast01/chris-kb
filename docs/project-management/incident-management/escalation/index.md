# Incident Escalation


<div class="kb-summary">
Incident Escalation reference covering Overview, Priority Definitions, Escalation Matrix, P1/P2 Escalation Checklist, Vendor Escalation and 1 more sections.
</div>
```
┌─────────────────── Project Management Incident Management Escalation — Escalation ────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Incident Management escalation: severity triage, vendor support contact, and required artifac │   │
│   │         L1: basic checks, restart services; L2: log analysis, config review, vendor SR        │   │
│   │        Severity: P1 production down → immediate SR + on-call page; P2/P3 business hours       │   │
│   │         Before escalating: collect support bundle, event timeline, and change history         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Detect issue → triage severity → collect artifacts → open SR → update                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Severity     │     Criteria     │   Response time   │      Owner       │    Vendor SLA    │   │
│   │        P1        │ Production down  │     Immediate     │   On-call + L2   │    1 hr 24x7     │   │
│   │        P2        │  Major degraded  │       1 hour      │   L2 engineer    │   4 hr biz hrs   │   │
│   │        P3        │  Minor degraded  │      4 hours      │   L2 engineer    │   8 hr biz hrs   │   │
│   │        P4        │    No impact     │    Next biz day   │    L1 support    │    2 biz days    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Project Management Incident Management Escalation infrastructure · management network ·  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Incident Management = Project Management Incident Management Escalation platform overview and cor  │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Overview

Escalation ensures that incidents get the right people involved at the right time. Failing to escalate promptly extends outage duration and can breach SLAs. Over-escalating creates alert fatigue and burns out senior staff on minor issues. The matrix below provides clear criteria for when and how to escalate.

---

## Priority Definitions

| Priority | Criteria                                                               | Initial Response |
|----------|------------------------------------------------------------------------|-----------------|
| P1       | Complete service outage; data loss; security breach; SLA breach imminent | 15 minutes      |
| P2       | Significant degradation; partial outage; subset of users affected      | 30 minutes      |
| P3       | Minor degradation; workaround available; no SLA risk                   | 2 hours         |
| P4       | Informational; no current user impact; monitoring warning only         | 8 hours / next day |

Priority is set at triage and can be upgraded or downgraded as more information becomes available. Upgrades must happen immediately; downgrades can wait until impact is confirmed reduced.

---

## Escalation Matrix

| Tier       | When to Escalate                                      | Escalate To                      |
|------------|-------------------------------------------------------|----------------------------------|
| Tier 1     | Initial response; standard tooling and runbooks       | On-call engineer                 |
| Tier 2     | 30 min no progress on P1; P2 escalating; new scope    | Infra Lead / Senior Engineer     |
| Tier 3     | P1 exceeding 1 hour; data loss confirmed; breach      | CTO / VP Infra                   |
| Vendor     | Issue isolated to vendor-managed component            | Vendor support (see below)       |
| Security   | Suspected breach, data exposure, or ransomware        | Security Lead + Legal (immediate)|

Escalation does not transfer ownership — the original responder remains engaged until explicitly handed over.

---

## P1/P2 Escalation Checklist

Before escalating to Tier 2 or above:

- [ ] Incident ticket created with P1/P2 priority set
- [ ] Initial impact assessment documented in the ticket
- [ ] Basic diagnosis steps completed (service status, recent changes, log scan)
- [ ] What you have tried and what you know documented in the ticket
- [ ] Ready to brief the escalation contact with: symptom, impact, duration, steps taken

---

## Vendor Escalation

| Vendor Contact Step      | When                                         | What to Provide                        |
|--------------------------|----------------------------------------------|----------------------------------------|
| Standard support ticket  | Non-urgent, within SLA                       | Description, logs, screenshots         |
| Priority/P1 hotline      | Active P1 with vendor component implicated   | Contract/account number, ticket ref    |
| Account manager          | Escalation stalled; SLA breach at risk       | Ticket ref, business impact statement  |
| Executive escalation     | Vendor unresponsive; major SLA breach        | Formal escalation email via management |

Keep the vendor ticket number in your incident ticket. Update both tickets as the incident progresses.

---

## De-escalation Criteria

Do not maintain P1 status indefinitely. De-escalate when:

- [ ] Primary service fully restored and validated
- [ ] Monitoring confirms stable state for 30+ minutes
- [ ] No further immediate risk to users or data
- [ ] Root cause understood well enough to confirm the fix holds
- [ ] Senior stakeholders notified of de-escalation

Document de-escalation time and reason in the incident ticket. Keep the ticket open for RCA work.
