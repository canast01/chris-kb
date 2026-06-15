---
tags:
  - troubleshooting
  - cisco-dcnm
  - san
  - known-issues
---
# Cisco DCNM — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Cisco DCNM (Data Center Network Manager) bugs, error codes, and workarounds covering switch discovery, deployment, and licensing.

*Applies to: Cisco DCNM 11.x / NDFC 12.x*
</div>

```text
┌──────────────────────────────────────── San Cisco Cisco Dcnm ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Cisco: San Cisco Cisco Dcnm platform                             │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                      Management: San Cisco Cisco Dcnm management console                      │   │
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
│    Physical: San Cisco Cisco Dcnm infrastructure · management network · monitoring                    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Cisco              = San Cisco Cisco Dcnm platform overview and core concepts                      │
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

- DCNM errors appear in the DCNM Dashboard → Alarms.
- DCNM → Administration → Logs for service-level diagnostics.
- Most discovery failures are SSH or SNMP connectivity issues.

## Switch Discovery

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Cannot discover switch — SSH timeout` | DCNM 11.x | TCP 22 blocked from DCNM to switch management IP | Verify TCP 22 from DCNM server to switch management IP | N/A |
| Switch discovered but showing `Out of Sync` | DCNM 11.x | Config in DCNM DB doesn't match live switch config | Trigger sync: DCNM → Inventory → Devices → right-click → Sync | N/A |

## Deployment

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Config deployment fails: `Cannot push to switch` | DCNM 11.x | DCNM write credentials (SSH) no longer valid | Update switch credentials in DCNM → Administration → Credentials | N/A |
| `Deployment preview differs from expected` | DCNM 11.x | Manual change made directly on switch (out-of-band) | Review diff in DCNM; reconcile with `Recalculate` before deploying | N/A |

## See also

- [Cisco DCNM — Common Issues](common-issues.md)
- [Cisco MDS — Known Issues](../../mds/troubleshooting/known-issues/)
- [Cisco Nexus Dashboard — Known Issues](../../nexus-dashboard/troubleshooting/known-issues/)
