---
tags:
  - troubleshooting
  - powershell
  - automation
  - known-issues
---
# PowerShell / PowerShell Remoting — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known PowerShell and WinRM bugs, error codes, and workarounds covering remoting, execution policy, and module loading.

*Applies to: PowerShell 5.1 (Windows), PowerShell 7.x (cross-platform)*
</div>

```text
┌──────────────────────────────── Automation Powershell Troubleshooting ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                   Powershell: Automation Powershell Troubleshooting platform                  │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │              Management: Automation Powershell Troubleshooting management console             │   │
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
│    Physical: Automation Powershell Troubleshooting infrastructure · management network · monitoring   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Powershell         = Automation Powershell Troubleshooting platform overview and core concepts     │
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

- Most PowerShell issues are execution policy, WinRM configuration, or TLS version mismatches.
- `$PSVersionTable` shows current PowerShell version and platform.
- Enable transcript logging: `Start-Transcript -Path <log>` for persistent capture.

## Remoting (WinRM)

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Access is denied` during `Enter-PSSession` | PS 5.1/7.x | Current user not in WinRM access group on target | Add user to `Remote Management Users` group on target | N/A |
| `The WinRM client cannot complete the operation` | PS 5.1 | WinRM TrustedHosts not configured for target | Add target: `Set-Item WSMan:\localhost\Client\TrustedHosts -Value "<target>"` | N/A |
| `Cannot connect to server — CredSSP not enabled` | PS 5.1 | CredSSP required but not enabled client or server side | Enable client: `Enable-WSManCredSSP -Role Client -DelegateComputer *`; enable server: `Enable-WSManCredSSP -Role Server` | N/A |

## Execution Policy

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `File ... cannot be loaded because running scripts is disabled` | All | Execution policy set to `Restricted` | Set policy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` | N/A |
| Script blocked even with `RemoteSigned` | PS 5.1 | Script downloaded from internet; has Zone.Identifier NTFS stream | Unblock: `Unblock-File -Path <script.ps1>` | N/A |

## Module Loading

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Module not found` after install | PS 7.x on Linux | Module installed for PS 5.1 on Windows; path not shared | Reinstall module in PS 7.x scope: `Install-Module <name> -Scope CurrentUser` | N/A |
| Module version conflict | PS 5.1 | Multiple versions installed; `Import-Module` loads wrong one | Import specific version: `Import-Module <name> -RequiredVersion <ver>` | N/A |

## See also

- [PowerShell — Common Issues](common-issues.md)
- [Windows Server — Known Issues](../../compute/windows-server/troubleshooting/known-issues/)
- [Ansible — Known Issues](../../automation/ansible/troubleshooting/known-issues/)
