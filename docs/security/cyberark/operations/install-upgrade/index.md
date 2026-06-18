---
tags:
  - operations
  - security
---
# CyberArk Lifecycle


<div class="kb-summary">
CyberArk follows a structured upgrade sequence to preserve Vault integrity: the Digital Vault is upgraded first, followed by CPM, then PSM, then PVWA; upgrading out of order is unsupported and may result in component incompatibility.

*Applies to: CyberArk PAM*
</div>
```text
┌───────────────────────── Security Cyberark Operations — Install and Upgrade ──────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Cyberark installation and upgrade: deployment and version management procedures        │   │
│   │         Pre-upgrade: back up configuration, check compatibility, review release notes         │   │
│   │      Upgrade: rolling upgrade preserves service; non-disruptive on dual-controller arrays     │   │
│   │           Post-upgrade: verify all services running; run health check; notify users           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Plan → backup config → upgrade staging → upgrade production → validate                             │
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
│    Physical: Security Cyberark Operations infrastructure · management network · monitoring            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Cyberark           = Security Cyberark Operations platform overview and core concepts              │
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


 The DR Vault must also be upgraded and its replication link verified after each major upgrade. CyberArk supports a rolling EOL model where each major version receives 5 years of support, with extended support available under a separate agreement.

| Version (example) | GA Date | End of Support | Notes |
|---|---|---|---|
| CyberArk PAM 14.x | 2024 | ~2029 | Current major release |
| CyberArk PAM 13.x | 2023 | ~2028 | Still supported |
| CyberArk PAM 12.x | 2022 | ~2027 | Extended support tier |
| Legacy CPM/PSM v10 | 2018 | EOL | Upgrade required |

**Upgrade sequence:** Vault → DR Vault → CPM → PSM → PVWA → PSMP

**Pre-upgrade checklist:**
- Full Vault backup (via Vault backup utility) and DR sync confirmation
- Snapshot all Windows VMs hosting PAM components
- Review CyberArk release notes for breaking changes
- Verify licence count covers current account inventory

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [CyberArk — Procedures](../procedures/)
- [CyberArk — Health Checks](../health-checks/)
- [CyberArk — CLI Reference](../cli-reference/)
- [CyberArk — Scripts](../scripts/)
- [CyberArk — Backup and Restore](../backup-restore/)
- [CyberArk — Common Issues](../../troubleshooting/common-issues/)
