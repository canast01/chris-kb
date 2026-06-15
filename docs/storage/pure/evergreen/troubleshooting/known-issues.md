---
tags:
  - troubleshooting
  - evergreen
  - pure-storage
  - known-issues
---
# Pure Storage Evergreen — Known Issues and Error Codes

<div class="kb-summary">
Evergreen is a commercial subscription program — it has no dedicated software or appliance. All operational known issues are tracked in the underlying array (FlashArray or FlashBlade) known-issues pages. This page covers Evergreen-specific subscription and upgrade process issues.

*Applies to: Evergreen//Forever, Evergreen//Flex*
</div>

```text
┌─────────────────────────────────────── Storage Pure Evergreen ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             Pure: Storage Pure Evergreen platform                             │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                     Management: Storage Pure Evergreen management console                     │   │
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
│    Physical: Storage Pure Evergreen infrastructure · management network · monitoring                  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Pure               = Storage Pure Evergreen platform overview and core concepts                    │
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


## Before you begin

- Evergreen is a subscription program — all operational port/software issues are tracked against the underlying FlashArray or FlashBlade hardware.
- For controller swap scheduling or upgrade process questions, contact **Pure Storage Customer Success**.

## Upgrade Process Issues

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Controller swap window missed — array shows old controller | Any | Pure scheduling gap; controller not swapped during agreed maintenance window | Contact Pure Customer Success to reschedule controller swap | N/A |
| `Cannot upgrade — Pure1 connectivity required` message | Purity 6.x | Non-disruptive controller upgrade requires active phone-home | Restore Pure1 connectivity (TCP 443 to pure1.purestorage.com); retry upgrade scheduling | N/A |

## See also

- [Pure Storage FlashArray — Known Issues](../../flasharray/troubleshooting/known-issues/)
- [Pure Storage FlashBlade — Known Issues](../../flashblade/troubleshooting/known-issues/)
- [Pure1 — Known Issues](../../pure1/troubleshooting/known-issues/)
