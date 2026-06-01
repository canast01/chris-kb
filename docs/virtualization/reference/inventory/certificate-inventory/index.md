# VMware Certificate Inventory


<div class="kb-summary">
| Product | FQDN | Certificate Type | Issuer | Expiration | Owner | Last Renewed | Next Review | |---|---|---|---|---|---|---|---| | vCenter | vcenter.domain.local | Machine SSL | VMCA | YYYY-MM-DD | infra-team | YYYY-MM-DD | YYYY-MM-DD | | vCenter | vcenter.domain.local | STS | 
</div>
```
┌───────────────────────────────── Virtualization Reference Inventory ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                     Reference: Virtualization Reference Inventory platform                    │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │               Management: Virtualization Reference Inventory management console               │   │
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
│    Physical: Virtualization Reference Inventory infrastructure · management network · monitoring      │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Reference          = Virtualization Reference Inventory platform overview and core concepts        │
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


| Product | FQDN | Certificate Type | Issuer | Expiration | Owner | Last Renewed | Next Review |
|---|---|---|---|---|---|---|---|
| vCenter | vcenter.domain.local | Machine SSL | VMCA | YYYY-MM-DD | infra-team | YYYY-MM-DD | YYYY-MM-DD |
| vCenter | vcenter.domain.local | STS | Self-signed | YYYY-MM-DD | infra-team | YYYY-MM-DD | YYYY-MM-DD |
| NSX Manager | nsx.domain.local | API/UI | Custom CA | YYYY-MM-DD | infra-team | YYYY-MM-DD | YYYY-MM-DD |
| Aria Operations | aria-ops.domain.local | Endpoint | Custom CA | YYYY-MM-DD | infra-team | YYYY-MM-DD | YYYY-MM-DD |
| Aria Logs | aria-logs.domain.local | Endpoint | Custom CA | YYYY-MM-DD | infra-team | YYYY-MM-DD | YYYY-MM-DD |
| VxRail Manager | vxrail.domain.local | UI/API | Self-signed | YYYY-MM-DD | infra-team | YYYY-MM-DD | YYYY-MM-DD |

## Replacement Method Notes

- **VMCA-issued** — replace via vSphere Client or VAMI
- **Custom CA** — generate CSR, submit to CA, import signed cert
- **Self-signed** — replace via product UI or CLI

## Tracking Notes

- Review all expiration dates monthly
- Flag anything expiring within 60 days
