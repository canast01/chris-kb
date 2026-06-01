# Post-Change Validation


<div class="kb-summary">
Post-Change Validation reference covering Overview, Validation Principles, Standard Validation Checklist, Validation by Change Type, Monitoring Observation Period and 1 more sections.
</div>
```text
┌─────────────────────────── Project Management Change Management Validation ───────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Change Management: Project Management Change Management Validation platform          │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │         Management: Project Management Change Management Validation management console        │   │
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
│    Physical: Project Management Change Management Validation infrastructure · management network · m  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Change Management  = Project Management Change Management Validation platform overview and core c  │
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

Validation confirms that a change achieved its intended outcome without introducing new problems. It is distinct from the implementation checklist — implementation confirms tasks were executed; validation confirms the service is healthy and behaving correctly. Both must be completed before a change is closed.

---

## Validation Principles

- Validate against the success criteria defined at the time of change approval — not a retrospective interpretation
- Always check both the directly changed component and its dependencies
- Validation must be performed by someone other than the sole implementer where possible
- Time-box the validation period: agree the duration before the change window starts

---

## Standard Validation Checklist

- [ ] Service health endpoint returns expected status
- [ ] Application logs show no new errors or exceptions introduced by the change
- [ ] Key user journeys tested (login, core function, data retrieval)
- [ ] Monitoring dashboards reviewed — no unexpected alerts firing
- [ ] Performance metrics within normal range (latency, error rate, queue depth)
- [ ] Downstream services confirmed unaffected
- [ ] Backup jobs still scheduled and functional
- [ ] DNS, load balancer, and certificate status verified if networking was touched

---

## Validation by Change Type

| Change Type              | Validation Focus                                          |
|--------------------------|-----------------------------------------------------------|
| OS patching              | Services restarted cleanly; no new errors in system logs  |
| Application deployment   | Smoke test; error rate; key API endpoints return 200      |
| Network change           | Connectivity between affected segments; routing correct   |
| Database change          | Query execution; row counts; replication lag (if clustered)|
| Certificate renewal      | TLS handshake succeeds; expiry date correct               |
| Firewall rule change      | Expected traffic permitted; blocked traffic still blocked |
| Storage change           | Read/write operations; capacity reported correctly        |

---

## Monitoring Observation Period

After validation, maintain an elevated monitoring period proportional to risk.

| Risk Level | Observation Period | Who Monitors               |
|------------|--------------------|-----------------------------|
| Low        | 1 hour             | Implementing engineer       |
| Medium     | 4 hours            | Implementing engineer       |
| High       | 24 hours           | Engineer + on-call team     |
| Critical   | 48–72 hours        | On-call team + management   |

During the observation period, agree on escalation criteria. If a new alert fires within the observation window that may be related to the change, treat it as a post-change issue and raise an incident.

---

## Sign-Off

Validation sign-off must be recorded in the change ticket before the change is closed.

- [ ] Implementer confirms all validation checks passed
- [ ] Change owner (or delegate) provides written sign-off in the ticket
- [ ] If any check failed, document what was done to resolve it or why risk is accepted
- [ ] Monitoring observation period confirmed active and owner assigned
- [ ] Change status updated to reflect validated outcome
