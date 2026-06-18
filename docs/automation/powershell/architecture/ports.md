---
tags:
  - powershell
  - automation
  - networking
  - firewall
  - ports
  - windows
---
# PowerShell — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for PowerShell remoting. PowerShell itself has no listening ports. The relevant ports are WinRM (Windows) and SSH (cross-platform) for remote sessions and Invoke-Command.

*Applies to: PowerShell 7.x / Windows PowerShell 5.1*
</div>

```text
┌───────────────────────────────── Automation Powershell Architecture ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                    Powershell: Automation Powershell Architecture platform                    │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │               Management: Automation Powershell Architecture management console               │   │
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
│    Physical: Automation Powershell Architecture infrastructure · management network · monitoring      │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Powershell         = Automation Powershell Architecture platform overview and core concepts        │
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


## WinRM — Windows Remoting (Primary)

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 5985 | TCP | PS remoting source host | Windows target | WinRM HTTP — unencrypted; avoid in production |
| 5986 | TCP | PS remoting source host | Windows target | WinRM HTTPS — encrypted; required for production |

## SSH-Based PS Remoting (Cross-Platform)

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 22 | TCP | PS remoting source | Linux or Windows target (with OpenSSH) | SSH transport for `Enter-PSSession` / `Invoke-Command` |

## PowerShell to Infrastructure APIs

When scripts call remote APIs (vCenter, REST, etc.):

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 443 | TCP | API targets (vCenter, Azure, REST services) | HTTPS API calls from PowerShell scripts |
| 1433 | TCP | SQL Server | Invoke-Sqlcmd / SQL queries |

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| PS source (Ansible, jump host, CI) | Windows targets | 5986 | WinRM HTTPS — production |
| PS source | Linux / Windows (OpenSSH) | 22 | SSH-based PS remoting |
| PS source | API endpoints | 443 | REST API calls from scripts |

## Verify

```powershell
# Test WinRM connectivity from source
Test-WSMan -ComputerName <target> -UseSSL

# Test PS Session
$s = New-PSSession -ComputerName <target> -UseSSL -Credential (Get-Credential)
Invoke-Command -Session $s { $env:COMPUTERNAME }

# Test SSH-based remoting
Enter-PSSession -HostName <linux-host> -UserName ansible
```

## See also

- [PowerShell — Architecture](how-it-works/)
- [Windows Server — Ports](../../../compute/windows-server/architecture/ports.md)
- [Ansible — Ports](../../ansible/architecture/ports.md)
