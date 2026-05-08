# Windows Server — Scripts

Automation scripts and reusable code.

## Daily Health Check

Generates a summary report of disk space, services, and recent errors. Run via scheduled task or manually.

```powershell
<#
.SYNOPSIS
  Windows Server daily health check report
.DESCRIPTION
  Checks disk space, stopped automatic services, recent event log errors,
  and Windows Defender status. Outputs a summary to the console and optionally
  emails the report.
#>

param(
    [string]$ComputerName = $env:COMPUTERNAME,
    [int]$DiskWarnPct     = 20,
    [int]$DiskCritPct     = 10,
    [int]$EventHours      = 24
)

$report = [System.Collections.Generic.List[string]]::new()
$report.Add("=== Windows Server Health Check: $ComputerName ===")
$report.Add("Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm')")
$report.Add("")

# --- Disk Space ---
$report.Add("--- Disk Space ---")
Get-PSDrive -PSProvider FileSystem | Where-Object { ($_.Used + $_.Free) -gt 0 } | ForEach-Object {
    $total = $_.Used + $_.Free
    $freePct = [math]::Round($_.Free / $total * 100, 1)
    $freeGB  = [math]::Round($_.Free / 1GB, 1)
    $totalGB = [math]::Round($total / 1GB, 1)
    $status  = if ($freePct -le $DiskCritPct) { "CRITICAL" } elseif ($freePct -le $DiskWarnPct) { "WARNING" } else { "OK" }
    $report.Add("  [$status] $($_.Name): $freeGB GB free of $totalGB GB ($freePct%)")
}
$report.Add("")

# --- Stopped Automatic Services ---
$report.Add("--- Stopped Automatic Services ---")
$stopped = Get-Service | Where-Object { $_.StartType -eq 'Automatic' -and $_.Status -ne 'Running' }
if ($stopped) {
    $stopped | ForEach-Object { $report.Add("  [WARNING] $($_.DisplayName) ($($_.Name)) - $($_.Status)") }
} else {
    $report.Add("  [OK] All automatic services are running")
}
$report.Add("")

# --- Recent Event Log Errors ---
$report.Add("--- Event Log Errors (last $EventHours hours) ---")
$since = (Get-Date).AddHours(-$EventHours)
$events = Get-EventLog -LogName System -EntryType Error -After $since -ErrorAction SilentlyContinue
if ($events) {
    $events | Select-Object -First 10 | ForEach-Object {
        $report.Add("  [ERROR] $($_.TimeGenerated) | EventID $($_.EventID) | $($_.Source) | $($_.Message -replace '\s+', ' ' | Select-Object -First 1)")
    }
} else {
    $report.Add("  [OK] No errors in System log")
}
$report.Add("")

# --- Defender Status ---
$report.Add("--- Windows Defender ---")
try {
    $def = Get-MpComputerStatus
    $report.Add("  Real-time protection: $($def.RealTimeProtectionEnabled)")
    $report.Add("  Signature date: $($def.AntivirusSignatureLastUpdated)")
    $report.Add("  Last quick scan: $($def.QuickScanStartTime)")
} catch {
    $report.Add("  [WARNING] Could not retrieve Defender status")
}

$report | ForEach-Object { Write-Host $_ }
```

## Disk Space Alert

Sends an alert when any drive falls below a threshold.

```powershell
<#
.SYNOPSIS
  Disk space threshold alert — email if any drive is below threshold
#>

param(
    [int]$ThresholdPct  = 15,
    [string]$SmtpServer = "smtp.internal.local",
    [string]$From       = "monitoring@internal.local",
    [string]$To         = "ops@internal.local"
)

$alerts = Get-PSDrive -PSProvider FileSystem | Where-Object {
    $total = $_.Used + $_.Free
    $total -gt 0 -and ($_.Free / $total * 100) -lt $ThresholdPct
} | ForEach-Object {
    $total  = $_.Used + $_.Free
    $pct    = [math]::Round($_.Free / $total * 100, 1)
    "$($_.Name): $([math]::Round($_.Free/1GB,1)) GB free ($pct%)"
}

if ($alerts) {
    $body = "Low disk space on $($env:COMPUTERNAME):`n`n" + ($alerts -join "`n")
    Send-MailMessage -From $From -To $To -Subject "ALERT: Disk space on $env:COMPUTERNAME" `
        -Body $body -SmtpServer $SmtpServer
}
```

## Service Monitor

Restarts stopped automatic services and logs the event.

```powershell
<#
.SYNOPSIS
  Monitors critical services and attempts restart on failure
#>

param(
    [string[]]$Services = @('W32Time', 'EventLog', 'WinRM', 'wuauserv'),
    [string]$LogPath    = "C:\Logs\ServiceMonitor.log"
)

function Write-Log {
    param([string]$Message)
    $entry = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | $Message"
    Add-Content -Path $LogPath -Value $entry
    Write-Host $entry
}

foreach ($svc in $Services) {
    $s = Get-Service -Name $svc -ErrorAction SilentlyContinue
    if (-not $s) {
        Write-Log "WARNING: Service '$svc' not found on this server"
        continue
    }
    if ($s.Status -ne 'Running') {
        Write-Log "ALERT: Service '$($s.DisplayName)' is $($s.Status) — attempting restart"
        try {
            Start-Service -Name $svc -ErrorAction Stop
            Write-Log "INFO: Service '$($s.DisplayName)' restarted successfully"
        } catch {
            Write-Log "ERROR: Failed to restart '$($s.DisplayName)': $_"
        }
    } else {
        Write-Log "OK: Service '$($s.DisplayName)' is running"
    }
}
```

## Event Log Query

Extracts events matching specific IDs for incident investigation.

```powershell
<#
.SYNOPSIS
  Query event logs for specific event IDs
#>

param(
    [string]$LogName  = "System",
    [int[]]$EventIDs  = @(7034, 7036, 1001, 6008),
    [int]$HoursBack   = 72,
    [string]$Output   = "C:\Temp\EventQuery.csv"
)

$since = (Get-Date).AddHours(-$HoursBack)

Get-WinEvent -FilterHashtable @{
    LogName   = $LogName
    Id        = $EventIDs
    StartTime = $since
} -ErrorAction SilentlyContinue |
    Select-Object TimeCreated, Id, LevelDisplayName, ProviderName,
        @{N="Message"; E={ $_.Message -replace '\s+', ' ' }} |
    Export-Csv -Path $Output -NoTypeInformation
Write-Host "Exported to $Output"
```

## Patch Status Report

Reports installed and missing patches for a list of servers.

```powershell
<#
.SYNOPSIS
  Generate patch compliance report across multiple servers
#>

param(
    [string[]]$Servers  = @($env:COMPUTERNAME),
    [string]$OutputPath = "C:\Temp\PatchReport_$(Get-Date -Format yyyyMMdd).csv"
)

$results = foreach ($server in $Servers) {
    try {
        $hotfixes = Invoke-Command -ComputerName $server -ScriptBlock {
            Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 5
        } -ErrorAction Stop
        foreach ($hf in $hotfixes) {
            [PSCustomObject]@{
                Server      = $server
                HotFixID    = $hf.HotFixID
                InstalledOn = $hf.InstalledOn
                Description = $hf.Description
                Status      = "OK"
            }
        }
    } catch {
        [PSCustomObject]@{
            Server      = $server
            HotFixID    = "N/A"
            InstalledOn = $null
            Description = "ERROR: $_"
            Status      = "UNREACHABLE"
        }
    }
}

$results | Export-Csv -Path $OutputPath -NoTypeInformation
Write-Host "Report saved: $OutputPath"
```
