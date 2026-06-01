# VMware Backup Standards


<div class="kb-summary">
VMware Backup Standards reference covering Critical VM Backup Policy, Standard VM Backup Policy, vCenter Backup, Snapshot Handling, Backup Monitoring and 2 more sections.
</div>
```
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


## Critical VM Backup Policy

- Daily backup minimum
- 30-day retention minimum
- Application-aware backup where supported
- Test restore at least quarterly

## Standard VM Backup Policy

- Daily or weekly backup
- 14-day retention minimum
- Restore test at least annually

## vCenter Backup

- File-based backup via VAMI daily
- Keep at least 3 copies
- Encryption password stored securely
- Backup target must be off the vSAN datastore

## Snapshot Handling

- Backup products must clean up their own snapshots after each job
- Alert if a backup snapshot is older than 24 hours
- Manual change-related snapshots must be removed within 48 hours

## Backup Monitoring

- Review backup job results daily
- Alert on any failed or missed backup
- Include backup status in the weekly health check

## Backup Failure Escalation

- Retry failed backup once
- If retry fails, investigate and escalate within 24 hours
- Critical VMs with no successful backup for more than 48 hours must be escalated immediately

## Backup Evidence Retention

- Keep backup job reports for 90 days
- Document restore tests with date and result
