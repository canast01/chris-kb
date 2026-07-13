---
tags:
  - powershell
  - troubleshooting
search:
  boost: 1.5
description: "PowerShell troubleshooting: execution policy blocks, module import failures, remoting authentication errors, pipeline object type mismatches, and cmdlet..."
---
# PowerShell — Common Issues

<div class="kb-summary">
PowerShell troubleshooting: execution policy blocks, module import failures, remoting authentication errors, pipeline object type mismatches, and cmdlet version conflicts.

*Applies to: PowerShell 7.x*
</div>

---

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
powershell_troubleshooting_decision_: "PowerShell Troubleshooting Decision Flow" {shape: rectangle}
debugging_scripts: "Debugging Scripts" {shape: rectangle}
common_error_reference: "Common Error Reference" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> powershell_troubleshooting_decision_: investigate
symptom -> debugging_scripts: investigate
symptom -> common_error_reference: investigate
symptom -> verify_resolution: investigate
diagnostic_flow -> resolution
powershell_troubleshooting_decision_ -> resolution
debugging_scripts -> resolution
common_error_reference -> resolution
verify_resolution -> resolution
```

## Diagnostic Flow

```d2
direction: right

D1: "D1" {shape: rectangle}
R1: "Common Error Reference\n— Set-ExecutionPolicy RemoteSigned -Scope CurrentUser" {shape: rectangle}
R2: "Common Error Reference\n— Set-ExecutionPolicy -Scope Process for bypass" {shape: rectangle}
D2: "D2" {shape: rectangle}
R3: "Common Error Reference\n— add module dir to PSModulePath" {shape: rectangle}
R4: "Common Error Reference\n— Install-Module -Force -AllowClobber" {shape: rectangle}
D3: "D3" {shape: rectangle}
R5: "Debugging Scripts\n— Get-Credential again or Import-Clixml" {shape: rectangle}
R6: "Debugging Scripts\n— inspect $Error[0" {shape: rectangle}
B4: "B4" {shape: rectangle}
R7: "Common Error Reference\n— Enable-PSRemoting -Force on target" {shape: rectangle}
B5: "B5" {shape: rectangle}
R8: "Common Error Reference\n— Set-ExecutionPolicy RemoteSigned" {shape: rectangle}
S: "What is the symptom?" {shape: rectangle}
B1: "B1" {shape: rectangle}
B2: "B2" {shape: rectangle}
B3: "B3" {shape: rectangle}

D1 -> R1
D1 -> R2
D2 -> R3
D2 -> R4
D3 -> R5
D3 -> R6
B4 -> R7
B5 -> R8
```

---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## PowerShell Troubleshooting Decision Flow

```d2
direction: right

failure: "Script Error\nor Unexpected Behaviour" {shape: rectangle}
errType: "Error type?" {shape: rectangle}
checkPolicy: "Get-ExecutionPolicy -List\ncheck all scopes" {shape: rectangle}
setPolicy: "Set-ExecutionPolicy RemoteSigned\n-Scope CurrentUser" {shape: rectangle}
checkModPath: "$env:PSModulePath\nmodule path correct?" {shape: rectangle}
addPath: "Add module directory\nto PSModulePath" {shape: rectangle}
reinstallMod: "Install-Module -Force\n-AllowClobber" {shape: rectangle}
testWSMan: "Test-WSMan -ComputerName host\nTest-NetConnection port 5985" {shape: rectangle}
enableRemoting: "Enable-PSRemoting -Force\non target (as admin" {shape: rectangle}
checkCred: "$Error[0" {shape: rectangle}
refreshCred: "Get-Credential again\nor Import-Clixml new file" {shape: rectangle}
strictMode: "Set-StrictMode -Version Latest\nadd breakpoint(" {shape: rectangle}
stepDebug: "Set-PSBreakpoint\nstep through execution" {shape: rectangle}

failure -> errType
errType -> checkPolicy
checkPolicy -> setPolicy
errType -> checkModPath
checkModPath -> addPath
checkModPath -> reinstallMod
errType -> testWSMan
testWSMan -> enableRemoting
errType -> checkCred
checkCred -> refreshCred
errType -> strictMode
strictMode -> stepDebug
```

## Debugging Scripts

```powershell
# Set strict mode to catch undefined variables and functions
Set-StrictMode -Version Latest

# Use Write-Debug statements (only show when $DebugPreference = 'Continue')
$DebugPreference = 'Continue'
Write-Debug "Variable value: $myVar"

# Breakpoints for interactive debugging
Set-PSBreakpoint -Script C:\Scripts\deploy.ps1 -Line 42
Set-PSBreakpoint -Variable myVar -Mode ReadWrite

# Step through script in VS Code
# Set a breakpoint then press F5 or use the Debug panel

# Trace execution
Set-PSDebug -Trace 1   # trace each line
Set-PSDebug -Trace 0   # disable tracing

# Error handling pattern
try {
    Get-Content -Path 'nonexistent.txt' -ErrorAction Stop
} catch [System.IO.FileNotFoundException] {
    Write-Error "File not found: $_"
} catch {
    Write-Error "Unexpected error: $($_.Exception.Message)"
} finally {
    Write-Verbose "Cleanup complete"
}
```

## Common Error Reference

```powershell
# View full error details from $Error automatic variable
$Error[0] | Format-List * -Force
$Error[0].Exception.InnerException

# Check exit code of external tools
ping 192.168.1.1 -n 1
$LASTEXITCODE

# Suppress errors for optional operations
Get-Process -Name nonexistent -ErrorAction SilentlyContinue
```

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [PowerShell — Diagnostics](../diagnostics/)
- [PowerShell — Escalation](../escalation/)
- [PowerShell — Health Checks](../../operations/health-checks/)
