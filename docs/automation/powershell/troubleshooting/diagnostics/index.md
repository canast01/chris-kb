---
tags:
  - powershell
  - troubleshooting
search:
  boost: 1.5
---
# PowerShell — Diagnostics

<div class="kb-summary">
PowerShell diagnostic techniques: inspect the $Error automatic variable for exception type and stack trace, enable Set-PSDebug -Trace 2 or Trace-Command for targeted subsystem tracing, capture a full transcript log to reproduce failures, diagnose WinRM connectivity issues with Test-WSMan and winrm enumerate, check execution policy at every scope, and collect a PS environment diagnostic snapshot for escalation.

*Applies to: PowerShell 7.x / Windows PowerShell 5.1*
</div>

```text
┌────────────────────────────────────── PowerShell — Diagnostics ───────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  PowerShell diagnostic sequence: check $Error[0] → enable verbose trace → transcript         │    │
│   │  WinRM issue: Test-WSMan -ComputerName srv → winrm enumerate winrm/config/listener           │    │
│   │  Module not found: Import-Module -Verbose → check $env:PSModulePath for search paths         │    │
│   │  Script blocked: Get-ExecutionPolicy -List → Unblock-File -Path .\Script.ps1                 │    │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Error Inspection               │  │               Trace and Debug               │   │
│   │          $Error[0] | Format-List *           │  │             Set-PSDebug -Trace 2            │   │
│   │           $Error[0].InnerException           │  │        $VerbosePreference = Continue        │   │
│   │          $Error[0].ScriptStackTrace          │  │        Set-StrictMode -Version Latest       │   │
│   │         Resolve-Error function (ISE)         │  │        Start-Transcript for full log        │   │
│   │        Get-PSCallStack (in debugger)         │  │        Test-Path, Test-NetConnection        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Set-PSDebug -Trace 2 = traces every line executed with variable assignments; very verbose   │   │
│   │    Set-StrictMode       = raises errors on undefined vars and bad index; catches bugs early   │   │
│   │   ScriptStackTrace     = call stack at the point of error; shows which function called what   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Developer workstation or automation server · WinRM listeners (HTTP 5985 / HTTPS 5986)                │
│  Active Directory (Kerberos for remoting) · PowerShell module paths (PSModulePath)                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│  $Error           = automatic array of recent errors; $Error[0] is the most recent                    │
│  Set-PSDebug      = -Trace 1 traces calls, -Trace 2 adds variable assignments                         │
│  Trace-Command    = targeted tracing of a specific PowerShell subsystem                               │
│  Start-Transcript = captures all session I/O to a file; most complete debug record                    │
│  Set-StrictMode   = fails on undefined variables and invalid properties                               │
│  Test-WSMan       = tests WinRM connectivity without authentication                                   │
│  winrm enumerate  = lists WinRM listener configuration (port, transport, cert)                        │
│  TrustedHosts     = WinRM setting required when Kerberos is not available                             │
│  ExecutionPolicy  = controls which scripts are allowed to run at each scope                           │
│  Zone.Identifier  = NTFS alternate data stream marking downloaded files as untrusted                  │
│  Unblock-File     = removes Zone.Identifier ADS; allows downloaded scripts to run                     │
│  PSModulePath     = semicolon-separated list of directories PowerShell searches for modules           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```mermaid
graph TD
    A([Script or automation fails]) --> B{Error message available?}
    B -->|Yes| C[Inspect $Error[0] then Get-Error]
    B -->|No| D[Enable transcript logging\nStart-Transcript -Path C:\Logs\trace.txt]
    C --> E{Error type?}
    E -->|CommandNotFound| F[Check module install, PATH, and execution policy\nImport-Module -Verbose to see search paths]
    E -->|Remoting or WinRM| G[Test-WSMan -ComputerName srv\nwinrm get winrm/config]
    E -->|AccessDenied| H[Check permissions and credential delegation\nVerify CredSSP or Kerberos config]
    E -->|Exception in script| I[Set-PSDebug -Trace 2\nor Trace-Command for targeted subsystem]
    F --> J[Resolve and retest]
    G --> J
    H --> J
    I --> K[Analyse trace output for failing line]
    K --> J
    D --> L[Reproduce with transcript active\nReview transcript for silent errors]
    L --> C
    J --> M{Resolved?}
    M -->|Yes| N([Document root cause])
    M -->|No| O[Collect Get-PSEnvironmentDiagnostics output\nEscalate with transcript attached]

    classDef dark fill:#1e3a5f,color:#fff
    classDef action fill:#78350f,color:#fff
    classDef escalate fill:#991b1b,color:#fff
    class A,B,E,M dark
    class C,D,F,G,H,I,J,K,L action
    class N,O escalate
```

## Before you begin

- **Access:** Terminal on the affected workstation or automation server; admin rights for execution policy changes and module installation; target system credentials for WinRM issues
- **Gather first:** the exact error message (`$Error[0].Message`), the script name and line number (`$Error[0].InvocationInfo`), and whether the issue occurs on a specific system only or all targets
- **Scope:** confirm whether the error occurs locally or only during remoting — `Test-WSMan -ComputerName <target>` confirms basic WinRM connectivity without triggering auth

---

## Step 1 — Inspect the error object

```powershell
# Most recent error — full detail
$Error[0] | Format-List *

# Inner exception (for wrapped .NET exceptions)
$Error[0].InnerException
$Error[0].InnerException.Message

# Stack trace at the point of error
$Error[0].ScriptStackTrace

# Call info — which script, line number, and command
$Error[0].InvocationInfo | Format-List *

# All recent errors (last 5)
$Error[0..4] | ForEach-Object { $_.Exception.Message }

# Modern PowerShell 7+ — formatted error with hints
Get-Error
```

---

## Step 2 — Enable trace logging

```powershell
# Trace every line executed (Trace 1 = calls only, Trace 2 = + variable values)
Set-PSDebug -Trace 2
.\MyScript.ps1
Set-PSDebug -Off   # disable when done

# Redirect trace output to a file (useful for large scripts)
Set-PSDebug -Trace 2; .\MyScript.ps1 *>&1 | Out-File C:\Logs\trace.txt

# Enable verbose output for all commands in the session
$VerbosePreference = "Continue"
.\MyScript.ps1
$VerbosePreference = "SilentlyContinue"

# Catch undefined variables and property access errors (good for debugging)
Set-StrictMode -Version Latest
```

### Trace-Command for targeted subsystem tracing

`Trace-Command` provides targeted tracing of specific PowerShell subsystems without the full overhead of `Set-PSDebug`.

```powershell
# Trace command discovery (why is a cmdlet not found?)
Trace-Command -Name CommandDiscovery -Expression {
    Get-Widget -Name 'widget-01'
} -PSHost

# Trace parameter binding (diagnose binding failures)
Trace-Command -Name ParameterBinding -Expression {
    Get-Widget -Name 'widget-01' -State Active
} -PSHost

# Trace module loading
Trace-Command -Name Modules -Expression {
    Import-Module MyModule
} -PSHost

# Write trace to file
Trace-Command -Name ParameterBinding -Expression {
    Set-Widget -Name 'widget-01' -Priority 5
} -FilePath C:\Logs\trace.log -FileAppend
```

Available trace sources:

| Trace Source | What it traces |
|---|---|
| `CommandDiscovery` | How commands are resolved |
| `ParameterBinding` | Parameter matching and conversion |
| `Modules` | Module load, import, export |
| `PipelineProcessor` | Pipeline object flow |
| `TypeConversion` | .NET type coercion |
| `ETS` | Extended Type System operations |

---

## Step 3 — Transcript logging

Transcripts capture all input and output in a session — the most complete debugging tool available.

```powershell
# Start transcript
Start-Transcript -Path C:\Logs\ps-transcript-$(Get-Date -Format yyyyMMdd-HHmmss).txt -Append

# Run the failing operation
.\MyScript.ps1

# Stop transcript
Stop-Transcript
```

### Automatic transcripts via Group Policy

For production environments, enforce transcript logging centrally:

```text
Computer Configuration → Administrative Templates → Windows Components →
Windows PowerShell → Turn on PowerShell Transcription
  → Enable: Yes
  → Output Directory: \\fileserver\logs\pstranscripts\%COMPUTERNAME%
  → Include invocation headers: Yes
```

### Script block logging (security and deobfuscation)

```powershell
# Enable script block logging — captures deobfuscated code before execution
$path = 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging'
New-Item $path -Force | Out-Null
Set-ItemProperty $path -Name EnableScriptBlockLogging -Value 1
# Logged to: Windows Event Log → Microsoft-Windows-PowerShell/Operational (Event ID 4104)
```

---

## Step 4 — WinRM connectivity diagnostics

```powershell
# Basic WinRM test (unauthenticated — verifies WinRM is listening)
Test-WSMan -ComputerName srv-prod-01

# Authenticated test
Test-WSMan -ComputerName srv-prod-01 -Authentication Kerberos -Credential (Get-Credential)

# Check WinRM service state on local machine
Get-Service WinRM | Select-Object Name, Status, StartType

# View WinRM listener configuration
winrm enumerate winrm/config/listener

# Check firewall rule
Get-NetFirewallRule -DisplayName '*Windows Remote Management*' |
    Select-Object DisplayName, Enabled, Direction, Profile

# Verify trusted hosts (workgroup environments)
Get-Item WSMan:\localhost\Client\TrustedHosts

# Add a host to trusted hosts (when Kerberos not available)
Set-Item WSMan:\localhost\Client\TrustedHosts -Value 'srv-prod-01' -Concatenate -Force

# Full WinRM configuration dump
winrm get winrm/config
```

### Common WinRM errors

| Error | Likely cause | Fix |
|---|---|---|
| `Access is denied` | Credential or delegation issue | Check `-Credential`, enable CredSSP or Kerberos |
| `The WS-Management service cannot complete the operation` | WinRM not started | `Start-Service WinRM` on target |
| `No such host is known` | DNS resolution failure | Verify DNS, use IP with TrustedHosts |
| `The connection attempt failed` | Firewall blocking 5985/5986 | Open port on host and network firewall |
| `The server certificate on the destination computer has the following errors` | HTTPS cert mismatch | Fix cert or use `-SkipCACheck -SkipCNCheck` (test only) |

---

## Step 5 — Execution policy and module diagnostics

### Execution policy

```powershell
# View effective policy at each scope
Get-ExecutionPolicy -List

# Check why a script is blocked
Get-Item .\MyScript.ps1 | Get-AuthenticodeSignature
(Get-Item .\MyScript.ps1).Attributes   # Look for Zone.Identifier alternate data stream

# Unblock a downloaded script (removes Zone.Identifier ADS)
Unblock-File -Path .\MyScript.ps1

# Bypass for a single invocation (test/CI use)
PowerShell.exe -ExecutionPolicy Bypass -File .\MyScript.ps1
```

### Module import failures

```powershell
# Verbose module loading — see exact search paths tried
Import-Module MyModule -Verbose

# Check module paths
$env:PSModulePath -split [IO.Path]::PathSeparator

# Inspect module manifest for errors
Test-ModuleManifest -Path .\MyModule\MyModule.psd1

# List available versions of a module
Get-Module -Name MyModule -ListAvailable | Select-Object Name, Version, Path

# Force reimport (clears cached version)
Remove-Module MyModule -Force -ErrorAction SilentlyContinue
Import-Module MyModule -Force

# Check for .NET assembly load failures
[System.AppDomain]::CurrentDomain.GetAssemblies() |
    Where-Object Location -like '*MyModule*'
```

---

## Step 6 — Collect diagnostic bundle

Use this as a first-response function when a production failure is reported.

```powershell
function Get-PSEnvironmentDiagnostics {
    [CmdletBinding()]
    param([string]$OutputPath = "$env:TEMP\ps-diag-$(Get-Date -Format yyyyMMdd-HHmmss).txt")

    $data = [ordered]@{
        Timestamp       = Get-Date -Format 'o'
        ComputerName    = $env:COMPUTERNAME
        PSVersion       = $PSVersionTable
        PSEdition       = $PSVersionTable.PSEdition
        ExecutionPolicy = Get-ExecutionPolicy -List
        PSModulePath    = $env:PSModulePath -split [IO.Path]::PathSeparator
        LoadedModules   = Get-Module | Select-Object Name, Version
        RecentErrors    = $Error[0..4] | ForEach-Object {
            [ordered]@{
                Message    = $_.Exception.Message
                Type       = $_.Exception.GetType().FullName
                Script     = $_.InvocationInfo.ScriptName
                Line       = $_.InvocationInfo.ScriptLineNumber
                StackTrace = $_.ScriptStackTrace
            }
        }
        WinRMStatus     = (Get-Service WinRM -ErrorAction SilentlyContinue).Status
    }

    $data | ConvertTo-Json -Depth 5 | Tee-Object -FilePath $OutputPath
    Write-Host "Diagnostics written to: $OutputPath" -ForegroundColor Green
}

Get-PSEnvironmentDiagnostics
```

---

## Log locations

| Source | Path / Command | What to look for |
|---|---|---|
| Transcript | `C:\Logs\ps-transcript-*.txt` | Full session I/O including silent errors |
| Script block log | Windows Event Log → PowerShell/Operational (Event 4104) | Deobfuscated script content before execution |
| WinRM event log | Windows Event Log → Microsoft-Windows-WinRM/Operational | Auth failures, listener errors |
| Trace output | `C:\Logs\trace.log` (Trace-Command -FilePath) | Per-line subsystem trace |
| Diagnostic bundle | `$env:TEMP\ps-diag-*.txt` | PS version, modules, errors, WinRM status |

---

## See also

- [PowerShell — Common Issues](../common-issues/)
- [PowerShell — Escalation](../escalation/)
- [PowerShell — Health Checks](../../operations/health-checks/)

## Verify resolution

- The failing command now completes without error: `$Error.Count` does not increase after re-running
- `$Error[0]` is null or unrelated to the original failure
- `Test-WSMan -ComputerName <target>` returns the server's WinRM configuration (for remoting issues)
- `Get-ExecutionPolicy -List` shows the appropriate policy for the environment (for execution policy issues)
- `Import-Module <ModuleName>` completes without error and `Get-Module <ModuleName>` lists the module (for module issues)
- The original script or automation runs end-to-end without throwing exceptions
