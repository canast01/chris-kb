# VMware Backup Coverage Inventory


<div class="kb-summary">
Live register of all VMs, their backup policy, and last verified restore test. Review monthly.
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


## Coverage Register

| VM Name | Application Owner | Criticality | Backup Tool | Policy | Schedule | Retention | Last Successful | Last Restore Test | Notes |
|---|---|---|---|---|---|---|---|---|---|
| vcenter-prod-01 | infra-team | Critical | File-based (VAMI) | Daily | 02:00 | 7 copies | YYYY-MM-DD | YYYY-MM-DD | VAMI built-in backup |
| nsx-mgr-01 | infra-team | Critical | NSX built-in backup + Veeam | Daily | 03:00 | 7 days | YYYY-MM-DD | YYYY-MM-DD | Separate NSX backup + VM snapshot |
| aria-ops-01 | infra-team | High | Veeam VBR | prod-infra-daily | Daily | 30 days | YYYY-MM-DD | YYYY-MM-DD | App-aware |
| app-prod-01 | app-team | Critical | Veeam VBR | prod-vm-daily | Daily | 30 days | YYYY-MM-DD | YYYY-MM-DD | App-aware, SQL |
| app-dev-01 | app-team | Standard | Veeam VBR | dev-vm-weekly | Weekly | 14 days | YYYY-MM-DD | Never | Dev — lower priority |

## Criticality Definitions

| Level | Definition | Backup Minimum |
|---|---|---|
| Critical | Business stops without this VM | Daily backup; quarterly restore test |
| High | Significant impact if lost | Daily backup; bi-annual restore test |
| Standard | Recoverable within hours from build runbook | Weekly backup; annual restore test |
| Low | Easily rebuilt from scratch | Weekly backup; no restore test required |

## Coverage Review Checklist (Monthly)

- [ ] Run a report of all protected VMs from backup tool
- [ ] Compare against vCenter VM inventory — identify any unprotected VMs
  ```powershell
  # List all VMs (PowerCLI)
  Get-VM | Select-Object Name, PowerState | Sort-Object Name | Export-Csv /tmp/all_vms.csv
  # Compare against Veeam/CommVault/NBU job report for protected VMs
  ```
- [ ] For any unprotected VM: check with application owner — intentional or oversight?
- [ ] Confirm all critical VMs have had a successful backup in the last 24 hours
- [ ] Confirm restore tests are not overdue (per criticality schedule above)

## Unprotected VMs Log

If a VM is intentionally not backed up (ephemeral workload, easily rebuilt), document it here:

| VM Name | Reason Not Backed Up | Owner | Review Date |
|---|---|---|---|
| build-agent-01 | Ephemeral CI/CD runner — rebuilt daily | devops-team | Quarterly |
| temp-test-vm | Temporary test VM — approved for deletion by EOQ | dev-team | 2026-06-30 |

## Restore Test Log

Record evidence of restore tests to satisfy audit requirements:

| VM Name | Test Date | Restore Type | RTO Achieved | Tester | Result | Notes |
|---|---|---|---|---|---|---|
| app-prod-01 | YYYY-MM-DD | Full VM restore to isolated network | 12 min | user@corp | Pass | DB came up clean |
| vcenter-prod-01 | YYYY-MM-DD | VAMI restore to alternate host | 35 min | user@corp | Pass | vCenter fully functional after restore |
