---
tags:
  - troubleshooting
  - windows-server
  - known-issues
---
# Windows Server — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Windows Server bugs, error codes, and workarounds covering WinRM, RDP, patching, and storage.

*Applies to: Windows Server 2019 / 2022*
</div>

```text
┌─────────────────────────────── Compute Windows Server Troubleshooting ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                Windows Server: Compute Windows Server Troubleshooting platform                │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │             Management: Compute Windows Server Troubleshooting management console             │   │
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
│    Physical: Compute Windows Server Troubleshooting infrastructure · management network · monitoring  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Windows Server     = Compute Windows Server Troubleshooting platform overview and core concepts    │
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

- Windows Event Viewer (System, Application, Security logs) is the primary diagnostic source.
- `Get-EventLog -LogName System -Newest 50 -EntryType Error` for recent errors.
- For remote management issues, always check WinRM and firewall first.

## Remote Management

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `WinRM cannot complete the operation` | Windows Server 2019/2022 | WinRM service stopped or TCP 5985/5986 blocked | Enable WinRM: `winrm quickconfig`; verify TCP 5985 from management host | N/A |
| RDP `The connection was denied` | All | Remote Desktop not enabled or Windows Firewall blocking 3389 | Enable RDP via `sysdm.cpl → Remote`; allow TCP 3389 in Windows Firewall | N/A |
| `CredSSP encryption oracle remediation` RDP error | Windows 2019 | CredSSP protocol version mismatch between client and server (post-May 2018 patch) | Apply CredSSP patch to both client and server; or set `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\CredSSP\Parameters\AllowEncryptionOracle = 2` temporarily | Fully patched systems |

## Patching

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Windows Update stuck at 0% | All | BITS or wuauserv service in bad state | Restart update services: `net stop wuauserv; net stop bits; net start wuauserv; net start bits` | N/A |
| `0x800705B4` Windows Update error | All | Windows Update service timeout | Run: `sfc /scannow`; if fails: `DISM /Online /Cleanup-Image /RestoreHealth` | N/A |
| WSUS client not scanning | All | WSUS GPO pointing to wrong WSUS server or WSUS certificate error | Check GPO: `gpresult /H report.html`; verify WSUS URL and cert | N/A |

## Storage

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Disk `Online (Errors)` in Disk Management | All | File system errors on volume | Run: `chkdsk /f /r <drive>:` | N/A |
| Storage Spaces `Degraded` after disk replacement | Windows Server 2019/2022 | New disk not added to Storage Pool automatically | Add disk to pool: `Add-PhysicalDisk -StoragePoolFriendlyName <pool> -PhysicalDisks <disk>` | N/A |

## See also

- [Windows Server — Common Issues](common-issues.md)
- [Active Directory — Known Issues](active-directory/troubleshooting/known-issues/)
- [SQL Server — Known Issues](sql-server/troubleshooting/known-issues/)
