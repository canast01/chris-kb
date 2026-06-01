# CyberArk — Diagnostics


<div class="kb-summary">
Use this page for practical CyberArk troubleshooting notes, checks, commands, change notes, and field references.
</div>
```
┌─────────────────────────── Security Cyberark Troubleshooting — Diagnostics ───────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Cyberark diagnostics: log collection, health checks, and performance analysis         │   │
│   │          Tools: management CLI, REST API, vendor support bundle, and system event log         │   │
│   │          Performance: check I/O latency, throughput, queue depth, and cache hit rate          │   │
│   │       Collect support bundle before contacting vendor support to reduce time-to-resolve       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Identify issue → collect logs → run diagnostics → analyse → resolve                                │
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
│    Physical: Security Cyberark Troubleshooting infrastructure · management network · monitoring       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Cyberark           = Security Cyberark Troubleshooting platform overview and core concepts         │
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


## CyberArk Diagnostic Flow

```mermaid
flowchart TD
    issue["CyberArk issue reported\n(login failure / rotation failed / session error)"]
    issue --> component{"Which component?"}
    component -->|"can't log in to PVWA"| pvwaCheck["Check PVWA IIS app pool\nGet-WebApplication PasswordVault\nVerify PVWA → Vault :1858"]
    component -->|"password rotation failed"| cpmCheck["Check CPM service\nGet-Service 'CyberArk Central Policy Manager'\nReview pm.log for error code"]
    component -->|"PSM session fails"| psmCheck["Check PSM service\nGet-Service 'Cyber-Ark Privileged Session Manager'\nReview PSMConsole.log"]
    component -->|"LDAP / MFA issues"| authCheck["Test LDAPS :636 from PVWA\nTest RADIUS :1812 to Duo Proxy\nCheck PVWA auth configuration"]
    pvwaCheck --> vaultConn["Test-NetConnection vault01 -Port 1858"]
    cpmCheck --> vaultConn
    psmCheck --> vaultConn
    vaultConn --> vaultOK{"Vault reachable?"}
    vaultOK -->|"no"| networkFix["Check firewall rules\nbetween component and Vault"]
    vaultOK -->|"yes"| logsReview["Review component logs\nCheck SIEM for audit events"]
```

## Common Checks

- Confirm current health
- Review active alerts
- Check recent changes
- Confirm dependencies
- Check logs, events, and monitoring
- Capture current state before changes

## Incident Notes

Capture:

- Symptom
- Start time
- Impact
- System or service name
- Error message
- What changed
- What was checked
- Next action

## Change Notes

- Confirm change approval
- Confirm maintenance window
- Confirm rollback plan
- Capture current state
- Make one change at a time
- Validate after the change

## Useful Commands

Add tested commands here.
