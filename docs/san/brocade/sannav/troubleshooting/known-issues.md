---
tags:
  - troubleshooting
  - sannav
  - brocade
  - san
  - known-issues
---
# Brocade SANnav — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known SANnav bugs, error codes, and workarounds covering switch discovery, performance data, and upgrade issues.

*Applies to: SANnav 2.3.x*
</div>

```text
┌───────────────────────────────────────── San Brocade Sannav ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Brocade: San Brocade Sannav platform                             │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                       Management: San Brocade Sannav management console                       │   │
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
│    Physical: San Brocade Sannav infrastructure · management network · monitoring                      │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Brocade            = San Brocade Sannav platform overview and core concepts                        │
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

- SANnav errors appear in Dashboard → Events and in SANnav → Administration → Logs.
- Most discovery failures are SNMP or SSH connectivity issues from SANnav to switches.

## Switch Discovery

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Switch not appearing after add | SANnav 2.3 | SNMP community mismatch or UDP 161 blocked | Verify SNMP community string; verify UDP 161 from SANnav to switch | N/A |
| `SSH authentication failed` during discovery | SANnav 2.3 | SANnav credentials incorrect for switch admin | Update switch credentials in SANnav → Administration → Credentials | N/A |
| SNMP trap not appearing in SANnav | SANnav 2.3 | Switch SNMP trap destination not pointing to SANnav | Configure trap on switch: `snmpconfig --set snmpv1` with SANnav IP | N/A |

## Performance Data

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Performance graphs empty for discovered switch | SANnav 2.3 | Performance monitoring not enabled for switch | Enable monitoring: SANnav → Monitoring → Performance Monitoring → Add Targets | N/A |
| Port utilization showing 0% for active ports | SANnav 2.3 | Counter polling interval set too high | Reduce polling interval to 30 seconds for active monitoring | N/A |

## See also

- [Brocade SANnav — Common Issues](common-issues.md)
- [Brocade Fabric OS — Known Issues](../../fabric-os/troubleshooting/known-issues/)
