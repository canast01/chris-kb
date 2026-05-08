# PowerShell — Diagnostics

> Part of the [PowerShell Troubleshooting](../) reference.

---

## Diagnostic Flowchart

```mermaid
flowchart TD
    A([Script or automation fails]) --> B{Error message available?}
    B -- Yes --> C[Inspect $Error\[0\] / Get-Error]
    B -- No --> D[Enable transcript logging]
    C --> E{Error type?}
    E -- CommandNotFound --> F[Check module / PATH / execution policy]
    E -- Remoting / WinRM --> G[Test-WSMan / WSMan trace]
    E -- AccessDenied --> H[Check permissions / credential delegation]
    E -- Exception in script --> I[Set-PSDebug -Trace 2\nor Trace-Command]
    F --> J[Resolve and retest]
    G --> J
    H --> J
    I --> K[Analyse trace output]
    K --> J
    D --> L[Reproduce with transcript active]
    L --> C
    J --> M{Resolved?}
    M -- Yes --> N([Document root cause])
    M -- No --> O([Escalate — see Escalation runbook])
    style O fill:#c62828,color:#fff
    style N fill:#2e7d32,color:#fff
```

---

## `$Error` and `Get-Error`

`$Error` is an automatic variable — a fixed-size circular array (default capacity 256) of `ErrorRecord` objects. The most recent error is at index `0`.

```powershell
# Count of errors in current session
$Error.Count

# Most recent error — summary
$Error[0]

# Full structured error detail (PowerShell 7+)
Get-Error

# Inspect specific error record fields
$err = $Error[0]
$err.Exception.Message        # Human-readable message
$err.Exception.GetType().Name  # Exception class
$err.InvocationInfo.ScriptName # Source script
$err.InvocationInfo.ScriptLineNumber
$err.InvocationInfo.Line       # The actual line of code
$err.ScriptStackTrace          # Full stack trace

# Clear the error variable (useful before a test block)
$Error.Clear()
```

---

## `Set-PSDebug`

`Set-PSDebug` enables low-level script tracing. Use `Trace 1` for statement-level tracing and `Trace 2` for variable assignments as well.

```powershell
# Trace every statement (level 1)
Set-PSDebug -Trace 1
.\MyScript.ps1

# Trace statements AND variable assignments (level 2)
Set-PSDebug -Trace 2
.\MyScript.ps1

# Disable tracing
Set-PSDebug -Off
```

Sample trace output:

```
DEBUG:    1+ >>>> $result = Get-Widget -Name 'widget-01'
DEBUG:    2+ >>>> if ($result.State -eq 'Active') {
DEBUG:   Variable: result = @{Name=widget-01; State=Active}
```

> Warning: `-Trace 2` is very verbose. Redirect output to a file for scripts with large loops: `Set-PSDebug -Trace 2; .\MyScript.ps1 *>&1 | Out-File trace.txt`

---

## `Trace-Command`

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

Available trace sources (partial list):

```powershell
Get-TraceSource | Select-Object Name, Description | Sort-Object Name
```

| Trace Source | What it traces |
|---|---|
| `CommandDiscovery` | How commands are resolved |
| `ParameterBinding` | Parameter matching and conversion |
| `Modules` | Module load, import, export |
| `PipelineProcessor` | Pipeline object flow |
| `TypeConversion` | .NET type coercion |
| `ETS` | Extended Type System operations |

---

## Transcript Logging

Transcripts capture all input and output in a session — the most complete debugging tool available.

```powershell
# Start transcript
Start-Transcript -Path C:\Logs\ps-transcript-$(Get-Date -Format yyyyMMdd-HHmmss).txt -Append

# Run the failing operation
.\MyScript.ps1

# Stop transcript
Stop-Transcript
```

### Automatic Transcripts via Group Policy

For production environments, enforce transcript logging centrally:

```
Computer Configuration → Administrative Templates → Windows Components →
Windows PowerShell → Turn on PowerShell Transcription
  → Enable: Yes
  → Output Directory: \\fileserver\logs\pstranscripts\%COMPUTERNAME%
  → Include invocation headers: Yes
```

### Module Logging and Script Block Logging

```powershell
# Enable script block logging (captures deobfuscated code — useful for security)
# Via registry (set in GPO or startup script):
$path = 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging'
New-Item $path -Force | Out-Null
Set-ItemProperty $path -Name EnableScriptBlockLogging -Value 1
```

---

## WinRM Connectivity Diagnostics

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

### Common WinRM Errors

| Error | Likely cause | Fix |
|---|---|---|
| `Access is denied` | Credential or delegation issue | Check `-Credential`, enable CredSSP or Kerberos |
| `The WS-Management service cannot complete the operation` | WinRM not started | `Start-Service WinRM` on target |
| `No such host is known` | DNS resolution failure | Verify DNS, use IP with TrustedHosts |
| `The connection attempt failed` | Firewall blocking 5985/5986 | Open port on host and network firewall |
| `The server certificate on the destination computer has the following errors` | HTTPS cert mismatch | Fix cert or use `-SkipCACheck -SkipCNCheck` (test only) |

---

## Execution Policy Diagnostics

```powershell
# View effective policy at each scope
Get-ExecutionPolicy -List

# Output example:
# Scope          ExecutionPolicy
# -----          ---------------
# MachinePolicy  Undefined
# UserPolicy     Undefined
# Process        Bypass
# CurrentUser    RemoteSigned
# LocalMachine   AllSigned

# Check why a script is blocked
Get-Item .\MyScript.ps1 | Get-AuthenticodeSignature
(Get-Item .\MyScript.ps1).Attributes  # Look for Zone.Identifier alternate data stream

# Unblock a downloaded script (removes Zone.Identifier ADS)
Unblock-File -Path .\MyScript.ps1

# Bypass for a single invocation (test/CI use)
PowerShell.exe -ExecutionPolicy Bypass -File .\MyScript.ps1
```

---

## Module Import Failures

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

## Diagnostic Data Collection Script

Use this as a first-response script when a production failure is reported.

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
