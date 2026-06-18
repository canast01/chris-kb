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
┌───────────────────────────────────────── PowerShell / WinRM ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         PowerShell 5.1 (Windows-only) and 7.x (cross-platform) scripting and remoting         │   │
│   │               Protocols: WinRM (HTTP 5985 / HTTPS 5986) · SSH (PS 7.x remoting)               │   │
│   │                    Management: PowerShell console / ISE / VS Code extension                   │   │
│   │        Script -> Execution policy check -> Module import -> Remoting session -> Target        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Engine           │  │    PS 5.1 / PS 7.x (Core)   │  │    .NET Framework / .NET    │   │
│   │           Remoting          │  │        WinRM listener       │  │    HTTP 5985 / HTTPS 5986   │   │
│   │           Security          │  │       Execution policy      │  │   Restricted/RemoteSigned   │   │
│   │           Modules           │  │   PSGallery / PSRepository  │  │   Per-user or system scope  │   │
│   │          Delegation         │  │      CredSSP / Kerberos     │  │       Double-hop auth       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │ Enter-PSSession  │Interactive remote│       WinRM       │  Kerberos/NTLM   │   Single host    │   │
│   │  Invoke-Command  │  Batch remoting  │       WinRM       │  Kerberos/NTLM   │ Fan-out to many  │   │
│   │     CredSSP      │ Cred. delegation │       WinRM       │ Delegated creds  │  Double-hop fix  │   │
│   │    PSGallery     │  Module source   │       HTTPS       │API key (publish) │   Public repo    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: Windows hosts (WinRM listener) - Linux/macOS hosts (PS 7.x + SSH remoting)                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  WinRM          = Windows Remote Management; SOAP-based remoting over HTTP/HTTPS                      │
│  Execution pol. = local script-running policy: Restricted/AllSigned/RemoteSigned/etc.                 │
│  TrustedHosts   = client allow-list of remote hosts permitted without Kerberos                        │
│  CredSSP        = Credential Security Support Provider; enables credential delegation                 │
│  Double-hop     = a remote session needing to authenticate onward to a third host                     │
│  PSGallery      = Microsoft-hosted public PowerShell module repository                                │
│  Zone.Identifier= NTFS alternate stream marking a file as downloaded from the internet                │
│  Unblock-File   = removes the Zone.Identifier stream so a script will run                             │
│  PSSession      = a persistent remoting connection reusable across multiple commands                  │
│  Desired State Config. = DSC; declarative configuration management built into PS                      │
│  $PSVersionTable= built-in variable reporting PS edition, version, and OS platform                    │
│  Constrained EP = endpoint exposing only a restricted command set for remoting                        │
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

- [PowerShell — Common Issues](common-issues/)
