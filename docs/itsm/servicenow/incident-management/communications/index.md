---
tags:
  - servicenow
---
# Incident Communications


<div class="kb-summary">
Incident Communications reference covering Overview, Communication Principles, Update Cadence, Communication Templates, Stakeholder Distribution and 1 more sections.

*Applies to: ServiceNow*
</div>
```text
┌──────────────────────── Project Management Incident Management Communications ────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Incident Management: Project Management Incident Management Communications platform      │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │      Management: Project Management Incident Management Communications management console     │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
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
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Project Management Incident Management Communications infrastructure · management netwo  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Incident Management = Project Management Incident Management Communications platform overview and  │
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

Effective incident communication keeps stakeholders informed, reduces inbound noise to the response team, and builds trust with users and leadership. Poor communications during an incident — silence, vague updates, or contradictory messages — often cause as much damage as the incident itself.

---

## Communication Principles

- Communicate proactively: update stakeholders before they ask
- Be factual: state what is known, what is unknown, and what is being investigated
- Be consistent: one communication lead per incident; no competing updates
- Set expectations: always include a time for the next update
- Avoid speculation: never publish a root cause until it is confirmed

---

## Update Cadence

| Incident Priority | Initial Update    | Ongoing Updates    | Resolution Update  |
|-------------------|-------------------|--------------------|--------------------|
| P1                | Within 15 minutes | Every 30 minutes   | Within 30 min of fix |
| P2                | Within 30 minutes | Every 60 minutes   | Within 1 hour of fix |
| P3                | Within 2 hours    | As material changes occur | Within 4 hours of fix |

Do not skip an update cycle — if there is nothing new to report, send an update saying that investigation is ongoing and the next update will be at a specified time.

---

## Communication Templates

**Initial notification:**
```text
[P1 INCIDENT] <Service Name> degraded — <brief description>
Time detected: <HH:MM TZ>
Impact: <user-facing description>
Affected services: <list>
Status: Investigating
Next update: <HH:MM TZ>
Incident bridge: <link/number>
```

**Ongoing update:**
```text
[P1 UPDATE] <Service Name> — <HH:MM TZ>
Current status: Investigating / Identified / Implementing fix
What we know: <1-2 sentences>
What we're doing: <1-2 sentences>
Next update: <HH:MM TZ>
```

**Resolution:**
```bash
[P1 RESOLVED] <Service Name> — <HH:MM TZ>
Service restored at: <HH:MM TZ>
Duration: <X hours Y minutes>
Root cause summary: <1-2 sentences — only if confirmed>
Full RCA/PIR: To follow within <X days>
```

---

## Stakeholder Distribution

Maintain a distribution list per priority tier. Review and update quarterly.

| Audience               | P1 | P2 | P3 | Channel              |
|------------------------|----|----|----|----------------------|
| On-call engineer       | Y  | Y  | Y  | PagerDuty            |
| Infra lead             | Y  | Y  | N  | Slack + page         |
| CTO / VP Infra         | Y  | N  | N  | Slack DM             |
| Customer Success       | Y  | Y  | N  | Email + Slack        |
| Affected users         | Y  | Y  | N  | Status page          |
| Security (if breach)   | Y  | Y  | N  | Direct escalation    |

---

## Major Incident Bridge

For P1 incidents, open an incident bridge immediately and keep it active until resolution.

- [ ] Bridge opened and link shared in the incident ticket and main comms channel
- [ ] Incident Commander identified and named on the bridge
- [ ] Communications lead identified (separate from technical lead if possible)
- [ ] Roll call of attendees done; non-essential participants asked to drop
- [ ] Updates posted to stakeholders every 30 minutes from the bridge
- [ ] Bridge recording started if your organisation requires it
