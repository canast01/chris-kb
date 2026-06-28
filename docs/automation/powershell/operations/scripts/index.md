---
tags:
  - operations
  - powershell
---
# PowerShell — Scripts

<div class="kb-summary">
General-purpose PowerShell automation patterns — ITSM scripts for daily checks, incident triage, change management, and health validation. Platform-specific scripts live with their product sections.

*Applies to: PowerShell 7.x*
</div>

See also:
- [Windows Server Scripts](../../../../compute/windows-server/operations/scripts/) — remote health checks, cert expiry monitoring, service health, script runners
- [PowerCLI Scripts](../../../../virtualization/vmware/powercli/operations/scripts/) — VMware vSphere inventory, snapshot audit, host reports

---

```d2
direction: down

daily_check_script: "Daily Check Script" {shape: rectangle}
incident_triage_script: "Incident Triage Script" {shape: rectangle}
change_precheck_script: "Change Pre-Check Script" {shape: rectangle}
postchange_validation_script: "Post-Change Validation Script" {shape: rectangle}
health_check_script: "Health Check Script" {shape: rectangle}
verify: "Verify" {shape: rectangle}

daily_check_script -> incident_triage_script: uses
incident_triage_script -> change_precheck_script: uses
change_precheck_script -> postchange_validation_script: uses
postchange_validation_script -> health_check_script: uses
health_check_script -> verify: uses
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Daily Check Script

Check that scheduled PowerShell tasks ran, review log files for errors, test connectivity to key infrastructure endpoints, and verify required modules are loaded and up to date. Environment variables: `SCRIPT_DIR` (default `C:\Scripts`), `LOG_DIR` (default `C:\Logs`).

```powershell
# ps_daily_check.ps1 — PowerShell automation environment daily health check
# Run: .\ps_daily_check.ps1

$ScriptDir  = $env:SCRIPT_DIR  ?? "C:\Scripts"
$LogDir     = $env:LOG_DIR     ?? "C:\Logs"
$InfraHosts = @("vcenter.local", "192.168.1.100")   # Adjust to your environment

$Fail = 0
function Check($label, $result) {
    if ($result) { Write-Host "[OK]   $label" -ForegroundColor Green }
    else         { Write-Host "[FAIL] $label" -ForegroundColor Red; $script:Fail++ }
}

Write-Host "=== PowerShell Daily Check — $(Get-Date) ==="

# Module checks
Check "VMware.PowerCLI installed"   (Get-Module VMware.PowerCLI -ListAvailable)
Check "Az module installed"          (Get-Module Az -ListAvailable)
Check "Posh-SSH installed"           (Get-Module Posh-SSH -ListAvailable)

# Log file check - any ERROR lines in last 24h?
if (Test-Path $LogDir) {
    $recentErrors = Get-ChildItem $LogDir -Filter "*.log" | 
                    Where-Object { $_.LastWriteTime -gt (Get-Date).AddHours(-24) } |
                    Get-Content | Select-String "ERROR|CRITICAL|FAILED" | Measure-Object | Select-Object -ExpandProperty Count
    Check "No errors in recent logs ($recentErrors found)" ($recentErrors -eq 0)
}

# Connectivity checks
foreach ($h in $InfraHosts) {
    Check "Network reachable: $h" (Test-Connection $h -Count 1 -Quiet -ErrorAction SilentlyContinue)
}

Write-Host ""
Write-Host "Daily check: $Fail failure(s)"
exit ($Fail -gt 0 ? 2 : 0)
```

---

## Incident Triage Script

Captures a full PowerShell automation environment snapshot to a timestamped file. Collects: PS version, all installed modules with versions, scheduled task statuses, last 200 lines of all log files in `$LogDir`, network connectivity to all `$InfraHosts`, and execution policy settings.

```powershell
# ps_incident_triage.ps1 — Capture PowerShell environment snapshot for incident triage
# Run: .\ps_incident_triage.ps1

$LogDir     = $env:LOG_DIR ?? "C:\Logs"
$InfraHosts = @("vcenter.local", "192.168.1.100")   # Adjust to your environment
$OutFile    = "C:\Temp\ps_triage_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"

if (-not (Test-Path "C:\Temp")) { New-Item -ItemType Directory -Path "C:\Temp" | Out-Null }

$output = [System.Text.StringBuilder]::new()
function Log($msg) { $output.AppendLine($msg) | Out-Null; Write-Host $msg }

Log "=== PowerShell Incident Triage — $(Get-Date) ==="
Log ""

# PS version
Log "--- PowerShell Version ---"
Log ($PSVersionTable | Out-String)

# All installed modules with versions
Log "--- Installed Modules ---"
Log (Get-Module -ListAvailable | Sort-Object Name | Select-Object Name, Version, ModuleType | Format-Table -AutoSize | Out-String)

# Scheduled task statuses
Log "--- Scheduled Task Statuses ---"
try {
    Log (Get-ScheduledTask | Select-Object TaskName, TaskPath, State,
         @{n='LastRunTime';e={(Get-ScheduledTaskInfo $_.TaskName -ErrorAction SilentlyContinue).LastRunTime}},
         @{n='LastResult'; e={(Get-ScheduledTaskInfo $_.TaskName -ErrorAction SilentlyContinue).LastTaskResult}} |
         Format-Table -AutoSize | Out-String)
} catch {
    Log "Unable to retrieve scheduled tasks: $_"
}

# Last 200 lines of each log file
Log "--- Recent Log Content ($LogDir) ---"
if (Test-Path $LogDir) {
    Get-ChildItem $LogDir -Filter "*.log" | ForEach-Object {
        Log "--- $($_.FullName) ---"
        Log (Get-Content $_.FullName -Tail 200 | Out-String)
    }
} else {
    Log "Log directory not found: $LogDir"
}

# Network connectivity
Log "--- Network Connectivity ---"
foreach ($h in $InfraHosts) {
    $reachable = Test-Connection $h -Count 1 -Quiet -ErrorAction SilentlyContinue
    Log "$(if ($reachable) { '[REACHABLE]' } else { '[UNREACHABLE]' })  $h"
}

# Execution policy
Log ""
Log "--- Execution Policy ---"
Log (Get-ExecutionPolicy -List | Out-String)

Log ""
Log "=== Triage complete ==="

$output.ToString() | Set-Content -Path $OutFile
Write-Host ""
Write-Host "Triage output saved to: $OutFile"
```

---

## Change Pre-Check Script

Run before modifying or deploying a PowerShell script. Confirms the script exists, performs a syntax check using the PS parser, verifies all required modules are installed, tests connectivity to all target systems, and creates a timestamped backup of the existing script. Exits non-zero on any failure.

```powershell
# ps_pre_check.ps1 — Pre-change validation before deploying a PowerShell script
# Usage: .\ps_pre_check.ps1 -ScriptPath "C:\Scripts\myscript.ps1" -RequiredModules @("Az","Posh-SSH")
param(
    [Parameter(Mandatory)]
    [string]$ScriptPath,

    [string[]]$RequiredModules = @("Az", "Posh-SSH", "VMware.PowerCLI"),
    [string[]]$TargetHosts     = @("vcenter.local", "192.168.1.100")
)

$Fail = 0
function Pass($label) { Write-Host "[PASS] $label" -ForegroundColor Green }
function Fail($label) { Write-Host "[FAIL] $label" -ForegroundColor Red; $script:Fail++ }

Write-Host "=== PowerShell Change Pre-Check — $(Get-Date) ==="
Write-Host "Script: $ScriptPath"
Write-Host ""

# 1. Script file exists
if (Test-Path $ScriptPath) { Pass "Script file exists: $ScriptPath" }
else                        { Fail "Script file NOT found: $ScriptPath"; exit 2 }

# 2. Syntax check using PS parser
Write-Host ""
Write-Host "--- Syntax Check ---"
$errors = $null
[System.Management.Automation.Language.Parser]::ParseFile($ScriptPath, [ref]$null, [ref]$errors) | Out-Null
if ($errors.Count -eq 0) { Pass "Syntax check passed (0 errors)" }
else {
    foreach ($e in $errors) { Write-Host "  Line $($e.Extent.StartLineNumber): $($e.Message)" -ForegroundColor Yellow }
    Fail "Syntax check failed ($($errors.Count) error(s))"
}

# 3. Required modules
Write-Host ""
Write-Host "--- Required Modules ---"
foreach ($mod in $RequiredModules) {
    if (Get-Module $mod -ListAvailable) { Pass "Module installed: $mod" }
    else                                { Fail "Module NOT installed: $mod" }
}

# 4. Connectivity to target systems
Write-Host ""
Write-Host "--- Target System Connectivity ---"
foreach ($h in $TargetHosts) {
    if (Test-Connection $h -Count 1 -Quiet -ErrorAction SilentlyContinue) { Pass "Reachable: $h" }
    else                                                                    { Fail "UNREACHABLE: $h" }
}

# 5. Backup existing script
Write-Host ""
Write-Host "--- Backup ---"
$BackupPath = "$ScriptPath.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
try {
    Copy-Item $ScriptPath $BackupPath -ErrorAction Stop
    Pass "Backup created: $BackupPath"
} catch {
    Fail "Backup FAILED: $_"
}

Write-Host ""
Write-Host "Pre-check complete: $Fail failure(s)"
if ($Fail -gt 0) { exit 2 }
exit 0
```

---

## Post-Change Validation Script

Run after deploying a modified script. Executes the script in test mode where available (`-WhatIf`), checks log output for expected results, compares to a baseline saved during the pre-check, and verifies no new errors have appeared in the log.

```powershell
# ps_post_validate.ps1 — Post-change validation after deploying a PowerShell script
# Usage: .\ps_post_validate.ps1 -ScriptPath "C:\Scripts\myscript.ps1" -BaselineLog "C:\Temp\baseline.txt"
param(
    [Parameter(Mandatory)]
    [string]$ScriptPath,

    [string]$BaselineLog = "",
    [string]$LogDir      = ($env:LOG_DIR ?? "C:\Logs")
)

$Pass = 0; $Fail = 0
function Ok($label)   { Write-Host "[PASS] $label" -ForegroundColor Green; $script:Pass++ }
function Fail($label) { Write-Host "[FAIL] $label" -ForegroundColor Red;   $script:Fail++ }

Write-Host "=== PowerShell Post-Change Validation — $(Get-Date) ==="
Write-Host "Script: $ScriptPath"
Write-Host ""

# 1. Script file exists after deploy
if (Test-Path $ScriptPath) { Ok "Deployed script file exists" }
else                        { Fail "Deployed script NOT found: $ScriptPath" }

# 2. Syntax check on deployed file
$errors = $null
[System.Management.Automation.Language.Parser]::ParseFile($ScriptPath, [ref]$null, [ref]$errors) | Out-Null
if ($errors.Count -eq 0) { Ok "Deployed script syntax valid" }
else                      { Fail "Deployed script has $($errors.Count) syntax error(s)" }

# 3. Test mode run (-WhatIf) if the script supports it
Write-Host ""
Write-Host "--- Test Mode Run (-WhatIf) ---"
try {
    $testOutput = & $ScriptPath -WhatIf 2>&1
    Ok "Script executed in -WhatIf mode without terminating errors"
    Write-Host ($testOutput | Out-String)
} catch {
    # -WhatIf may not be supported — try -Confirm:$false or just parse output
    Write-Host "  Note: -WhatIf not supported by this script; skipping test run." -ForegroundColor Yellow
}

# 4. No new errors in log since deployment
Write-Host ""
Write-Host "--- Log Error Check (since $(Get-Date).AddMinutes(-10) approx) ---"
if (Test-Path $LogDir) {
    $newErrors = Get-ChildItem $LogDir -Filter "*.log" |
                 Where-Object { $_.LastWriteTime -gt (Get-Date).AddMinutes(-15) } |
                 Get-Content |
                 Select-String "ERROR|CRITICAL|FAILED" |
                 Measure-Object | Select-Object -ExpandProperty Count
    if ($newErrors -eq 0) { Ok "No new errors in logs after deployment" }
    else                   { Fail "$newErrors new error line(s) found in logs after deployment" }
} else {
    Write-Host "  Log directory not found — skipping log check" -ForegroundColor Yellow
}

# 5. Compare to baseline output
Write-Host ""
Write-Host "--- Baseline Comparison ---"
if ($BaselineLog -and (Test-Path $BaselineLog)) {
    $currentOutput = & $ScriptPath 2>&1 | Out-String
    $baselineContent = Get-Content $BaselineLog -Raw
    if ($currentOutput -eq $baselineContent) { Ok "Output matches baseline" }
    else {
        Write-Host "  Differences found between current output and baseline:" -ForegroundColor Yellow
        $diff = Compare-Object ($currentOutput -split "`n") ($baselineContent -split "`n")
        $diff | ForEach-Object { Write-Host "  $($_.SideIndicator) $($_.InputObject)" -ForegroundColor Yellow }
        Fail "Output differs from baseline — review differences above"
    }
} else {
    Write-Host "  No baseline log provided or found — skipping comparison" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Post-change validation: $Pass PASS  |  $Fail FAIL"
if ($Fail -gt 0) { exit 2 }
exit 0
```

---

## Health Check Script

Lightweight scheduled health check reporting PS version, key module inventory with versions, log error count in the last 24 hours, scheduled task last run status, and connectivity tests. Exits 0 (healthy), 1 (warning), or 2 (critical).

```powershell
# ps_health_check.ps1 — Scheduled PowerShell automation health check
# Exit codes: 0=healthy  1=warning  2=critical

$LogDir     = $env:LOG_DIR ?? "C:\Logs"
$InfraHosts = @("vcenter.local", "192.168.1.100")   # Adjust to your environment
$KeyModules = @("VMware.PowerCLI", "Az", "Posh-SSH")
$Status     = 0   # 0=OK  1=WARN  2=CRIT

function Warn  { if ($script:Status -lt 1) { $script:Status = 1 } }
function Crit  { if ($script:Status -lt 2) { $script:Status = 2 } }

Write-Host "=== PowerShell Health Check — $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ==="
Write-Host ""

# 1. PS version
Write-Host "PowerShell version : $($PSVersionTable.PSVersion)"
Write-Host ""

# 2. Key module inventory
Write-Host "--- Module Inventory ---"
foreach ($mod in $KeyModules) {
    $installed = Get-Module $mod -ListAvailable | Sort-Object Version -Descending | Select-Object -First 1
    if ($installed) {
        Write-Host "  [OK]      $mod  $($installed.Version)" -ForegroundColor Green
    } else {
        Write-Host "  [MISSING] $mod" -ForegroundColor Red
        Warn
    }
}
Write-Host ""

# 3. Log error count last 24h
Write-Host "--- Log Errors (last 24h) ---"
if (Test-Path $LogDir) {
    $errorCount = Get-ChildItem $LogDir -Filter "*.log" |
                  Where-Object { $_.LastWriteTime -gt (Get-Date).AddHours(-24) } |
                  Get-Content |
                  Select-String "ERROR|CRITICAL|FAILED" |
                  Measure-Object | Select-Object -ExpandProperty Count
    Write-Host "  Error lines in logs: $errorCount"
    if ($errorCount -gt 0) { Warn }
} else {
    Write-Host "  Log directory not found: $LogDir" -ForegroundColor Yellow
    Warn
}
Write-Host ""

# 4. Scheduled task last run status
Write-Host "--- Scheduled Task Last Run ---"
try {
    Get-ScheduledTask | ForEach-Object {
        $info = Get-ScheduledTaskInfo $_.TaskName -ErrorAction SilentlyContinue
        if ($info -and $info.LastTaskResult -ne 0 -and $info.LastTaskResult -ne $null) {
            Write-Host "  [WARN] $($_.TaskName) last result: $($info.LastTaskResult)" -ForegroundColor Yellow
            Warn
        }
    }
    Write-Host "  Scheduled task check complete."
} catch {
    Write-Host "  Unable to check scheduled tasks: $_" -ForegroundColor Yellow
    Warn
}
Write-Host ""

# 5. Connectivity tests
Write-Host "--- Connectivity ---"
foreach ($h in $InfraHosts) {
    $reachable = Test-Connection $h -Count 1 -Quiet -ErrorAction SilentlyContinue
    if ($reachable) { Write-Host "  [OK]          $h" -ForegroundColor Green }
    else            { Write-Host "  [UNREACHABLE] $h" -ForegroundColor Red; Crit }
}
Write-Host ""

$statusLabel = switch ($Status) { 0 { "HEALTHY" } 1 { "WARNING" } 2 { "CRITICAL" } }
Write-Host "Status: $statusLabel"
exit $Status
```

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [PowerShell — Procedures](../procedures/)
- [PowerShell — CLI Reference](../cli-reference/)
- [PowerShell — Health Checks](../health-checks/)
