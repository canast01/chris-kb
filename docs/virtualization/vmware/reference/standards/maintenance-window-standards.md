---
tags:
  - reference
---
# VMware Maintenance Window Standards


<div class="kb-summary">
VMware Maintenance Window Standards reference covering Change Ticket Requirement, Stakeholder Notification, Window Definition, Pre-Change Evidence, Rollback Plan and 4 more sections.

*Applies to: vSphere 7.x / 8.x*
</div>
```text
┌───────────────────────────────── Virtualization Reference Standards ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                     Reference: Virtualization Reference Standards platform                    │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │               Management: Virtualization Reference Standards management console               │   │
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
│    Physical: Virtualization Reference Standards infrastructure · management network · monitoring      │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Reference          = Virtualization Reference Standards platform overview and core concepts        │
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


## Change Ticket Requirement

All maintenance windows require an approved change ticket before work begins.

## Stakeholder Notification

- Notify all affected application owners at least 24 hours before the window
- For critical changes, notify 48–72 hours in advance

## Window Definition

- Define a clear start and end time
- Scope the window to the minimum required duration
- Include buffer time for validation and rollback if needed

## Pre-Change Evidence

- Capture health check screenshots before work begins
- Confirm backup status
- Confirm current versions

## Rollback Plan

- Document rollback steps in the change ticket
- Confirm rollback is achievable within the maintenance window

## Communication During the Window

- Notify stakeholders when work starts
- Provide status updates if the window is extended
- Notify stakeholders when work is complete and validated

## Post-Change Validation

- Complete all post-change checks before closing the window
- Confirm with application owners if business validation is required

## Ticket Closure

- Document what was done, how long it took, and the outcome
- Attach pre and post screenshots as evidence
- Close the ticket with a completion note

## Lessons Learned

- Document any issues or unexpected outcomes in the change ticket
- Review with the team if the change did not go as planned
