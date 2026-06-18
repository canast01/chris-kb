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
┌─────────────────────────────────────────── Windows Server ────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │             General-purpose server OS — WinRM, RDP, Windows Update, Storage Spaces            │   │
│   │                     Protocols: WinRM (5985/5986) · RDP (3389) · SMB (445)                     │   │
│   │                     Management: Server Manager / PowerShell / Event Viewer                    │   │
│   │             Boot -> Services start -> Network up -> Domain join (if any) -> Login             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │         Remote mgmt         │  │            WinRM            │  │     HTTP/HTTPS listener     │   │
│   │        Remote desktop       │  │             RDP             │  │      TCP 3389, CredSSP      │   │
│   │           Patching          │  │     Windows Update/WSUS     │  │       GPO-driven scan       │   │
│   │           Storage           │  │        Storage Spaces       │  │    Software-defined pool    │   │
│   │           Logging           │  │         Event Viewer        │  │    Sys/App/Security logs    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │      WinRM       │   Remote mgmt    │     HTTP/HTTPS    │  Kerberos/NTLM   │winrm quickconfig │   │
│   │       RDP        │  Remote desktop  │      TCP 3389     │   NLA/CredSSP    │FW must allow 3389│   │
│   │       WSUS       │    Patch mgmt    │     HTTP/HTTPS    │    GPO-scoped    │ Central approval │   │
│   │  Storage Spaces  │  SDS pool/vdisk  │        N/A        │       N/A        │ Add-PhysicalDisk │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: physical/virtual Windows Server host - local/SAN/iSCSI storage                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  WinRM          = Windows Remote Management; remoting over HTTP/HTTPS                                 │
│  CredSSP        = credential delegation provider; vuln if outdated                                    │
│  NLA            = Network Level Authentication; RDP pre-auth                                          │
│  WSUS           = Windows Server Update Services; on-prem patch point                                 │
│  Storage Spaces = software-defined storage virtualizing disks                                         │
│  Storage Pool   = disk collection backing one or more virtual disks                                   │
│  Event Viewer   = GUI for System/Application/Security event logs                                      │
│  sfc /scannow   = System File Checker; repairs corrupted system files                                 │
│  DISM           = repairs the Windows servicing image                                                 │
│  gpresult       = shows which GPOs applied to a computer/user                                         │
│  BITS           = Background Intelligent Transfer Service, used by WU                                 │
│  Encr. Oracle   = CredSSP patch-mismatch RDP remediation error                                        │
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

- [Windows Server — Common Issues](common-issues/)
- [Active Directory — Known Issues](../active-directory/troubleshooting/known-issues/)
- [SQL Server — Known Issues](../sql-server/troubleshooting/known-issues/)
