---
tags:
  - deployment
  - powershell
---
# PowerShell — Environment Setup

This guide covers the initial setup of a PowerShell automation environment: installing
PowerShell Core, loading required modules, configuring a profile and execution policy,
enabling remote management, and turning on logging.

```text
┌─────────────────────────────────── PowerShell — Environment Setup ────────────────────────────────────┐
│                                                                                                       │
│   PowerShell Core (v7+) is cross-platform: runs on Windows, Linux, and macOS                          │
│   Replaces Windows PowerShell 5.1; both coexist; use pwsh for Core, powershell for 5.1                │
│   Install on Windows: winget install Microsoft.PowerShell                                             │
│   Install on Linux: dnf install powershell  OR  apt install powershell                                │
│                                                                                                       │
│   Module management                                                                                   │
│   PSGallery is the default repository; Install-Module -Name ModuleName -Scope CurrentUser             │
│   List installed: Get-Module -ListAvailable | Select Name, Version, Path                              │
│   Update all: Update-Module; remove: Uninstall-Module -Name ModuleName -AllVersions                   │
│   Trusted gallery: Set-PSRepository -Name PSGallery -InstallationPolicy Trusted                       │
│                                                                                                       │
│   Profile and execution policy                                                                        │
│   Profile path: $PROFILE (per-user, per-host); auto-loaded on each session start                      │
│   Execution policy: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser              │
│   Corporate baseline: RemoteSigned (local scripts run; remote scripts need signing)                   │
│   Test: Get-ExecutionPolicy -List; bypass for one script: pwsh -ExecutionPolicy Bypass                │
│                                                                                                       │
│   Remote management (WinRM)                                                                           │
│   Enable: Enable-PSRemoting -Force (Windows); sets WinRM listeners on 5985/5986                       │
│   Connect: Enter-PSSession -ComputerName server01 -Credential (Get-Credential)                        │
│   Non-interactive: Invoke-Command -ComputerName server01 -ScriptBlock { Get-Service }                 │
│   Kerberos used automatically on domain; HTTPS listener required for cross-domain                     │
│                                                                                                       │
│   Logging                                                                                             │
│   ScriptBlock logging: HKLM:\...\PowerShell\ScriptBlockLogging → EnableScriptBlockLogging             │
│   Transcription: Start-Transcript -Path C:\Logs\ps_session.log -Append                                │
│   Module logging: logs all module pipeline execution details to Windows Event Log                     │
│                                                                                                       │
│   Physical infrastructure                                                                             │
│   Management workstation or jump host with PowerShell 7+ and required modules                         │
│   WinRM listeners on target Windows servers; firewall allows TCP 5985/5986 inbound                    │
│                                                                                                       │
│   Key terms:                                                                                          │
│   PSGallery    = Microsoft-hosted public module repository; default for Install-Module                │
│   profile      = $PROFILE script; runs at session start; customize prompt and aliases                 │
│   execution policy = controls which scripts run; does not apply to interactive commands               │
│   WinRM        = Windows Remote Management; underlying PS remoting transport                          │
│   PSSession    = persistent remote session; keep-alive for multiple commands                          │
│   ScriptBlock logging = logs all executed PS code to Event Log for security auditing                  │
│   cmdlet       = compiled .NET command following Verb-Noun naming (Get-Service, etc.)                 │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Install PowerShell Core (Cross-Platform)

**Windows**

```powershell
winget install Microsoft.PowerShell
```

Alternatively, download the `.msi` installer from the
[GitHub releases page](https://github.com/PowerShell/PowerShell/releases).

**Linux (Debian/Ubuntu)**

```bash
sudo apt install powershell
```

**Linux (RHEL/Fedora/Rocky)**

```bash
sudo dnf install powershell
```

**Verify**

```bash
pwsh --version
```

---

## Install Required Modules

```powershell
Install-Module -Name PSWindowsUpdate, Az, VMware.PowerCLI -Scope CurrentUser -Force
```

| Module | Purpose |
|---|---|
| `PSWindowsUpdate` | Manage Windows Updates programmatically |
| `Az` | Azure resource management |
| `VMware.PowerCLI` | vSphere / ESXi automation |

Verify and update:

```powershell
Get-Module -ListAvailable | Select-Object Name, Version | Sort-Object Name
Update-Module -Force
```

---

## Configure PowerShell Profile

The profile script runs automatically at the start of every `pwsh` session.

```powershell
# Find profile path
$PROFILE

# Create if it does not exist
New-Item -Path $PROFILE -ItemType File -Force

# Open for editing
code $PROFILE
```

Example profile:

```powershell
Import-Module VMware.PowerCLI
Import-Module Az
Set-Alias -Name k -Value kubectl
$env:KUBECONFIG = "$HOME/.kube/config"
```

Reload without restarting:

```powershell
. $PROFILE
```

---

## Configure Execution Policy

`RemoteSigned` allows local scripts and requires signing for scripts downloaded
from the internet.

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
Get-ExecutionPolicy -List
```

**Enterprise (GPO):** `Computer Configuration → Administrative Templates →
Windows Components → Windows PowerShell → Turn on Script Execution`
→ set to `Allow local scripts and remote signed scripts`.

Do not use `Unrestricted` or `Bypass` in production.

---

## Set Up Remote Management (WinRM)

**On each target host** (run as administrator):

```powershell
Enable-PSRemoting -Force
```

**On the management workstation**, add trusted targets:

```powershell
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "192.168.1.50,srv-prod-01"
```

**Test connectivity**:

```powershell
Test-WSMan -ComputerName srv-prod-01
```

If the command hangs, check: Firewall allows TCP 5985/5986, WinRM service is
running, and the target hostname resolves.

---

## Configure Logging and Transcripts

Start a transcript to record a full session:

```powershell
Start-Transcript -Path C:\Logs\ps-session.log -Append
# ... run commands ...
Stop-Transcript
```

**GPO-based logging:** `Computer Configuration → Administrative Templates →
Windows Components → Windows PowerShell`

Enable **Turn on Module Logging** and **Turn on PowerShell Script Block Logging**.

View events in **Event Viewer**:
`Applications and Services Logs → Microsoft → Windows → PowerShell → Operational`
(Event ID 4103 = module log, 4104 = script block content).

---

## Validate the Environment

```powershell
# PowerShell version
$PSVersionTable

# Available modules
Get-Module -ListAvailable | Select-Object Name, Version | Sort-Object Name

# Remote connectivity
Test-WSMan -ComputerName <remote-host>

# Execution policy
Get-ExecutionPolicy -List

# Smoke test
Write-Output "PowerShell environment is ready."
```

| Check | Expected |
|---|---|
| `$PSVersionTable.PSVersion` | 7.x.x |
| `Get-Module -ListAvailable` | Az, VMware.PowerCLI present |
| `Test-WSMan` | Returns WinRM version without error |
| `Get-ExecutionPolicy -Scope CurrentUser` | `RemoteSigned` |
