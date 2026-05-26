# RASR — Scripts

## Script Inventory

| Script | Purpose |
|---|---|
| [New-RASRImage](#new-rasrimage) | Automated RASR image creation with logging and alerting |
| [Test-RASRImageAge](#test-rasrimageage) | Check if latest image exceeds maximum age threshold |
| [Remove-OldRASRImages](#remove-oldrasrimages) | Clean up images exceeding retention count |
| [Test-RASRImageIntegrity](#test-rasrimageintegrity) | Verify integrity of all images on share |
| [New-RASRScheduledTask](#new-rasrscheduledtask) | Register scheduled backup task via PowerShell |
| [Invoke-PostRestoreValidation](#invoke-postrestorevalidation) | Automated post-restore validation checks |

All scripts assume RASR is installed at `C:\Program Files\Dell\RASR\rasrutil.exe`. Adjust the `$RASRBin` variable as needed.

---

## New-RASRImage

Creates a RASR system image, writes a structured log, and writes a Windows Event Log entry on failure.

```powershell
<#
.SYNOPSIS
    Creates a RASR system image backup to a network share.
.PARAMETER Destination
    UNC path to the backup share directory for this server.
.PARAMETER ShareUser
    Domain\username with write access to the share.
.PARAMETER SharePassword
    Password for ShareUser (use SecureString or retrieve from vault).
.PARAMETER Description
    Human-readable label embedded in the image metadata.
#>
function New-RASRImage {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Destination,

        [Parameter(Mandatory)]
        [string]$ShareUser,

        [Parameter(Mandatory)]
        [string]$SharePassword,

        [string]$Description = "Automated backup $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    )

    $RASRBin = "C:\Program Files\Dell\RASR\rasrutil.exe"
    $LogDir  = "C:\Logs\RASR"
    $LogFile = Join-Path $LogDir "rasr-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"

    # Ensure log directory exists
    if (-not (Test-Path $LogDir)) {
        New-Item -ItemType Directory -Path $LogDir | Out-Null
    }

    Write-Host "[$(Get-Date)] Starting RASR backup to $Destination"

    $arguments = @(
        "/backup",
        "/dest", "`"$Destination`"",
        "/user", $ShareUser,
        "/pass", $SharePassword,
        "/compress",
        "/log", "`"$LogFile`"",
        "/description", "`"$Description`""
    )

    $proc = Start-Process -FilePath $RASRBin `
                          -ArgumentList $arguments `
                          -Wait -PassThru -NoNewWindow

    if ($proc.ExitCode -eq 0) {
        Write-Host "[$(Get-Date)] Backup completed successfully. Log: $LogFile"
    } else {
        $msg = "RASR backup FAILED with exit code $($proc.ExitCode). Log: $LogFile"
        Write-Error $msg

        # Write to Windows Application Event Log
        $eventSource = "RASR-Backup"
        if (-not [System.Diagnostics.EventLog]::SourceExists($eventSource)) {
            [System.Diagnostics.EventLog]::CreateEventSource($eventSource, "Application")
        }
        Write-EventLog -LogName Application -Source $eventSource `
                       -EntryType Error -EventId 9001 -Message $msg
    }

    return $proc.ExitCode
}

# Example usage:
# New-RASRImage -Destination "\\nas01\rasr-images\$env:COMPUTERNAME" `
#               -ShareUser "CORP\svc-rasr" `
#               -SharePassword "S3cr3t!"
```
┌─────────────────────────────────────────── RASR — Scripts ────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                   RASR — Automation Scripts                                   │   │
│   │                Scripts automate routine RASR operations — run via cron or CI/CD               │   │
│   │               Always store credentials in vault (not in script); log all output               │   │
│   │                 Test scripts in non-production before scheduling in production                │   │
│   │                        Scope scripts to least-privilege service account                       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Status / Reporting Scripts          │  │              Automation Scripts             │   │
│   │           Job success rate report            │  │            Auto-expire old points           │   │
│   │              Capacity trending               │  │          Auto-add new VMs to policy         │   │
│   │            SLA compliance report             │  │          Nightly DR test validation         │   │
│   │             RPO / RTO dashboard              │  │             Alert on job failure            │   │
│   │               cybersense scan                │  │             vault lock / unlock             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts     │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest       │
│  Vault         = isolated, air-gapped storage appliance receiving periodic replication copies         │
│  Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies      │
│  CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures        │
│  PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery      │
│  Air Gap       = physical or logical network isolation preventing attacker lateral movement to        │
│  Delta Set     = incremental changed blocks replicated from production to vault each cycle            │
│  Clean Room    = isolated recovery environment: separate vCenter, network, and workstations           │
│  Recovery Point= specific vault snapshot timestamp from which clean recovery is performed             │
│  Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac       │
│  Journal       = write-order-consistent journal on vault enabling point-in-time recovery              │
│  Scan Report   = CyberSense output: clean/suspect classification per file and block                   │
│  Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept                    │
│  RTO           = Recovery Time Objective; time from failover decision to restored service             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Test-RASRImageIntegrity

Iterates all RASR images on a share and runs `rasrutil.exe /verify` against each. Outputs a pass/fail report.

```powershell
<#
.SYNOPSIS
    Verifies the integrity of all RASR images on a network share.
.PARAMETER SharePath
    UNC path to the image directory.
.PARAMETER ShareUser
    Credential username.
.PARAMETER SharePassword
    Credential password.
#>
function Test-RASRImageIntegrity {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$SharePath,

        [string]$ShareUser,
        [string]$SharePassword
    )

    $RASRBin = "C:\Program Files\Dell\RASR\rasrutil.exe"

    if ($ShareUser -and $SharePassword) {
        net use $SharePath /user:$ShareUser $SharePassword 2>$null | Out-Null
    }

    $images = Get-ChildItem -Path $SharePath -Filter "*.rasr" | Sort-Object LastWriteTime

    if ($images.Count -eq 0) {
        Write-Warning "No images found in $SharePath"
        return
    }

    $results = @()

    foreach ($img in $images) {
        Write-Host "Verifying: $($img.Name) ..."
        $proc = Start-Process -FilePath $RASRBin `
                              -ArgumentList "/verify /source `"$($img.FullName)`"" `
                              -Wait -PassThru -NoNewWindow

        $results += [PSCustomObject]@{
            ImageName  = $img.Name
            SizeGB     = [math]::Round($img.Length / 1GB, 2)
            LastWrite  = $img.LastWriteTime
            Status     = if ($proc.ExitCode -eq 0) { "PASS" } else { "FAIL (code $($proc.ExitCode))" }
        }
    }

    $results | Format-Table -AutoSize

    $failed = $results | Where-Object { $_.Status -ne "PASS" }
    if ($failed) {
        Write-Warning "$($failed.Count) image(s) failed integrity check."
    } else {
        Write-Host "All $($results.Count) image(s) passed integrity check."
    }
}

# Example:
# Test-RASRImageIntegrity -SharePath "\\nas01\rasr-images\SERVER01" `
#                         -ShareUser "CORP\svc-rasr" -SharePassword "S3cr3t!"
```

---

## New-RASRScheduledTask

Registers the RASR weekly backup task in Windows Task Scheduler. Idempotent — updates the task if it already exists.

```powershell
<#
.SYNOPSIS
    Creates or updates the RASR weekly backup scheduled task.
.PARAMETER SharePath
    UNC path for backup destination (server-specific subdirectory).
.PARAMETER ShareUser
    Share authentication username.
.PARAMETER SharePassword
    Share authentication password.
.PARAMETER DayOfWeek
    Day of week for the backup schedule.
.PARAMETER StartTime
    Time to run the backup.
#>
function New-RASRScheduledTask {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$SharePath,

        [Parameter(Mandatory)]
        [string]$ShareUser,

        [Parameter(Mandatory)]
        [string]$SharePassword,

        [System.DayOfWeek]$DayOfWeek = [System.DayOfWeek]::Sunday,
        [string]$StartTime = "02:00"
    )

    $taskName  = "RASR Weekly Backup"
    $rasrBin   = "C:\Program Files\Dell\RASR\rasrutil.exe"
    $logPath   = "C:\Logs\RASR\rasr-scheduled.log"
    $arguments = "/backup /dest `"$SharePath`" /user $ShareUser /pass $SharePassword /compress /log `"$logPath`""

    $action    = New-ScheduledTaskAction -Execute $rasrBin -Argument $arguments
    $trigger   = New-ScheduledTaskTrigger -Weekly -DaysOfWeek $DayOfWeek -At $StartTime
    $principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
    $settings  = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Hours 8) `
                                               -MultipleInstances IgnoreNew

    if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
        Set-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings
        Write-Host "Updated existing scheduled task: $taskName"
    } else {
        Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger `
                               -Principal $principal -Settings $settings `
                               -Description "Weekly RASR system image backup"
        Write-Host "Registered scheduled task: $taskName"
    }
}

# Example:
# New-RASRScheduledTask -SharePath "\\nas01\rasr-images\$env:COMPUTERNAME" `
#                       -ShareUser "CORP\svc-rasr" `
#                       -SharePassword "S3cr3t!"
```

---

## Invoke-PostRestoreValidation

Runs automated post-restore health checks and outputs a structured report. Designed to run immediately after a RASR restore completes and the server boots.

```powershell
<#
.SYNOPSIS
    Performs automated post-restore validation checks on a recovered server.
.PARAMETER ExpectedHostname
    The expected hostname of the server (validates no accidental rename).
.PARAMETER DomainName
    FQDN of the domain the server should be joined to.
.PARAMETER CriticalServices
    Array of service names that must be in Running state.
#>
function Invoke-PostRestoreValidation {
    [CmdletBinding()]
    param(
        [string]$ExpectedHostname = $env:COMPUTERNAME,
        [string]$DomainName,

        [string[]]$CriticalServices = @(
            "W32Time", "Netlogon", "BITS", "wuauserv", "EventLog"
        )
    )

    $checks = @()

    # 1. Hostname check
    $hn = $env:COMPUTERNAME
    $checks += [PSCustomObject]@{
        Check  = "Hostname"
        Result = if ($hn -eq $ExpectedHostname) { "PASS" } else { "FAIL: Got '$hn', expected '$ExpectedHostname'" }
    }

    # 2. Domain membership
    if ($DomainName) {
        $cs     = Get-WmiObject Win32_ComputerSystem
        $domain = $cs.Domain
        $checks += [PSCustomObject]@{
            Check  = "Domain Membership"
            Result = if ($domain -eq $DomainName) { "PASS" } else { "FAIL: Domain is '$domain', expected '$DomainName'" }
        }
    }

    # 3. Secure channel to DC
    if ($DomainName) {
        $sc = Test-ComputerSecureChannel
        $checks += [PSCustomObject]@{
            Check  = "Secure Channel to DC"
            Result = if ($sc) { "PASS" } else { "FAIL: Secure channel broken — run Test-ComputerSecureChannel -Repair" }
        }
    }

    # 4. Critical services
    foreach ($svc in $CriticalServices) {
        $s = Get-Service -Name $svc -ErrorAction SilentlyContinue
        $checks += [PSCustomObject]@{
            Check  = "Service: $svc"
            Result = if ($s -and $s.Status -eq "Running") { "PASS" } else { "FAIL: Status '$($s.Status)'" }
        }
    }

    # 5. RASR Agent running
    $rasrSvc = Get-Service -Name "DellRASR" -ErrorAction SilentlyContinue
    $checks += [PSCustomObject]@{
        Check  = "RASR Agent Service"
        Result = if ($rasrSvc -and $rasrSvc.Status -eq "Running") { "PASS" } else { "FAIL: DellRASR not running" }
    }

    # 6. Network connectivity (ping default gateway)
    $gw   = (Get-NetRoute -DestinationPrefix "0.0.0.0/0" | Sort-Object RouteMetric | Select-Object -First 1).NextHop
    $ping = Test-Connection -ComputerName $gw -Count 2 -Quiet
    $checks += [PSCustomObject]@{
        Check  = "Network (gateway ping)"
        Result = if ($ping) { "PASS" } else { "FAIL: Cannot reach gateway $gw" }
    }

    # 7. System event log — critical errors in last 30 minutes
    $since  = (Get-Date).AddMinutes(-30)
    $errors = Get-EventLog -LogName System -EntryType Error,Warning -After $since `
                           -ErrorAction SilentlyContinue | Measure-Object
    $checks += [PSCustomObject]@{
        Check  = "System Event Log (last 30 min)"
        Result = if ($errors.Count -eq 0) { "PASS" } else { "WARN: $($errors.Count) error/warning events found" }
    }

    # Summary output
    Write-Host "`n=== Post-Restore Validation Report ===" -ForegroundColor Cyan
    Write-Host "Server  : $env:COMPUTERNAME"
    Write-Host "Time    : $(Get-Date)"
    Write-Host "======================================`n"
    $checks | Format-Table Check, Result -AutoSize

    $failed = $checks | Where-Object { $_.Result -notlike "PASS*" }
    if ($failed) {
        Write-Warning "$($failed.Count) check(s) require attention."
    } else {
        Write-Host "All checks passed. Server is healthy." -ForegroundColor Green
    }

    return $checks
}

# Example:
# Invoke-PostRestoreValidation -ExpectedHostname "SERVER01" `
#                              -DomainName "corp.example.com" `
#                              -CriticalServices @("W32Time","Netlogon","SQLServer")
```
