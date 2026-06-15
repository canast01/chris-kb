---
tags:
  - troubleshooting
  - commvault
  - backup
  - known-issues
---
# Commvault — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Commvault bugs, error codes, and workarounds covering backup jobs, media agents, and VSA (VMware) integration.

*Applies to: Commvault 11.x (Feature Release)*
</div>

```text
┌────────────────────────────────── Backup Commvault Troubleshooting ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                      Commvault: Backup Commvault Troubleshooting platform                     │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                Management: Backup Commvault Troubleshooting management console                │   │
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
│    Physical: Backup Commvault Troubleshooting infrastructure · management network · monitoring        │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Commvault          = Backup Commvault Troubleshooting platform overview and core concepts          │
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

- Commvault errors appear in CommCell Console → Job Controller → Failed jobs — expand for event log.
- Commvault KB at `documentation.commvault.com`.
- Run `cvpkgadd` diagnostics or `commvault restart` service tool for service-level issues.

## VMware (VSA)

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| VSA backup fails: `Snapshot operation failed` | Commvault 11.x | ESXi host overloaded; snapshot quiesce timeout | Reduce concurrent VSA streams; increase snapshot timeout in VSA properties | N/A |
| `Access denied` connecting to vCenter | Commvault 11.x | vCenter credentials changed or account locked | Update vCenter credentials in CommCell → Client Computers → vCenter Client | N/A |
| VSA restore fails: `Cannot find datastore` | Commvault 11.x | Datastore name changed or removed | Update restore destination in job restore wizard | N/A |

## Media Agents

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Media agent `Offline` in CommCell | Commvault 11.x | Commvault services not running on MA host | Restart Commvault services: `commvault restart` (Linux) or Services.msc (Windows) | N/A |
| Backup job fails: `Cannot connect to media agent port 8400` | Commvault 11.x | TCP 8400 blocked between CommServe and MA | Verify TCP 8400 open; check MA firewall | N/A |
| DD Boost integration failing | Commvault 11.x | DD Boost user not enabled or port 2052 blocked | Enable DD Boost user on Data Domain; verify TCP 2052 from MA to DD | N/A |

## CommServe

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `CommServe database maintenance` blocking jobs | Commvault 11.x | CSDB maintenance window running during business hours | Reschedule CSDB maintenance to off-peak window | N/A |
| License `Capacity exceeded` alarm | Commvault 11.x | Frontend capacity above licensed tier | Review capacity reporting; purchase additional license capacity | N/A |

## See also

- [Commvault — Common Issues](common-issues.md)
- [Dell Data Domain — Known Issues](../../../storage/dell/data-domain/troubleshooting/known-issues/)
