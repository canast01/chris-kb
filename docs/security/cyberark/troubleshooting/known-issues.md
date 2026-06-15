---
tags:
  - troubleshooting
  - cyberark
  - pam
  - known-issues
---
# CyberArk — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known CyberArk PAM bugs, error codes, and workarounds covering Vault, PVWA, CPM, and PSM components.

*Applies to: CyberArk PAS / Privilege Cloud 13.x+*
</div>

```text
┌────────────────────────────────── Security Cyberark Troubleshooting ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                      Cyberark: Security Cyberark Troubleshooting platform                     │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                Management: Security Cyberark Troubleshooting management console               │   │
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


## Before you begin

- CyberArk errors appear in the PVWA → Monitoring → Session Management, or in Vault audit logs.
- Vault logs: `C:\Program Files (x86)\PrivateArk\Server\Logs\italog.log`.
- PSM logs: `C:\Program Files (x86)\CyberArk\PSM\Logs\PSMConsole.log`.

## Vault Connectivity

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| PVWA `Cannot connect to Vault` | CyberArk 13.x | TCP 1858 blocked between PVWA and Vault | Verify TCP 1858 from all PVWA servers to Vault; test: `telnet <vault-ip> 1858` | N/A |
| CPM `Account reconciliation failed — cannot connect to target` | CyberArk 13.x | CPM cannot reach target system (SSH 22 / RDP 3389) | Verify CPM has network access to target; check CPM firewall rules | N/A |
| DR Vault not promoting after primary failure | CyberArk 13.x | DR Vault replication port 1858 blocked from primary site | Verify TCP 1858 between primary Vault and DR Vault subnets | N/A |

## Password Management

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Account locked out` after CPM rotation | CyberArk 13.x | CPM rotated password but target system not updated; old password cached | Check CPM platform settings for reconcile account; use `Immediate Change` with reconcile | N/A |
| `CPM cannot change password — AD account` | CyberArk 13.x | CPM domain account lacks password change permission in AD | Grant CPM service account `Reset Password` right on target OU | N/A |
| Password rotation failing for Windows local account | CyberArk 13.x | Windows UAC or local security policy blocking remote password change | Configure CPM platform to use `Pass This Object` or reconcile via domain admin | N/A |

## PSM (Privileged Session Manager)

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| PSM RDP session disconnecting after 10 minutes | CyberArk 13.x | Windows RDP idle session timeout on PSM server | Increase `Idle Session Limit` via Group Policy on PSM Windows host | N/A |
| `Cannot initiate connection` for PSM SSH target | CyberArk 13.x | Target SSH host key changed since last PSM connection | Remove cached host key from PSM known_hosts; allow PSM to accept new key | N/A |

## See also

- [CyberArk — Common Issues](common-issues.md)
- [Active Directory — Known Issues](../../compute/windows-server/active-directory/troubleshooting/known-issues/)
