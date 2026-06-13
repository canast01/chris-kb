---
tags:
  - operations
  - vmware
  - vxrail
---
# VxRail Appliance — Scripts

<div class="kb-summary">
PowerCLI and bash scripts for VxRail automation. Includes vSAN health summary, cluster capacity report, pre-upgrade validation, node firmware version report, and a configurable vSAN capacity alert script.

*Applies to: VxRail 7.x / 8.x*
</div>

```text
┌────────────────────────────────────────── VxRail — Scripts ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   All PowerCLI scripts require: Connect-VIServer before running                               │   │
│   │   Bash scripts run over SSH to an ESXi host or VxRail Manager                                │    │
│   │   Scripts are parameterised at the top — edit the variable block before running               │   │
│   │   Pre-upgrade validation script is the recommended gate before any LCM upgrade                │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      vSAN Health Summary    │  │    Cluster Capacity Report  │  │    Pre-Upgrade Validation   │   │
│   │   Loop all nodes            │  │   All datastores            │  │   vSAN health green         │   │
│   │   Output per-check result   │  │   Used% + FreeGB per DS     │  │   Resync = 0                │   │
│   │   Flag any non-green checks │  │   Alert threshold flag      │  │   DRS Fully Automated       │   │
│   │   Group by check category   │  │   Sorted by used%           │  │   All nodes connected       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────────────────────────────────────┐    │
│   │    Firmware Version Report  │  │           vSAN Capacity Alert Script                        │    │
│   │   ESXi version + build/host │  │   Configurable threshold (default 70%)                      │    │
│   │   iDRAC version via RACADM  │  │   Sends console alert or email on breach                    │    │
│   │   BIOS version per node     │  │   Run on schedule via Task Scheduler / cron                 │    │
│   └─────────────────────────────┘  └─────────────────────────────────────────────────────────────┘    │
│                                                                                                       │
│  Key terms:                                                                                           │
│  Connect-VIServer = PowerCLI cmdlet to authenticate against vCenter before running any cmdlets        │
│  Get-VsanClusterHealthSummary = returns per-check vSAN health groups and overall state                │
│  Get-SpbmEntityConfiguration  = returns per-VM storage policy compliance status                       │
│  RACADM                       = iDRAC CLI; used over SSH to pull firmware version info per node       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Prerequisites

All PowerCLI scripts require the VMware.PowerCLI module and an active vCenter connection:

```powershell
# Install PowerCLI (run once)
Install-Module -Name VMware.PowerCLI -Scope CurrentUser -Force

# Suppress certificate warning for lab/self-signed certs
Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false

# Connect to vCenter
Connect-VIServer -Server vcenter.example.local -Credential (Get-Credential)
```

---

## Script 1 — vSAN Health Summary

Loops all health check groups and outputs per-check results. Flags any non-green checks with red output.

```powershell
# === vSAN Health Summary ===
# Outputs all vSAN health checks grouped by category
# Prerequisites: Connect-VIServer

param(
    [string]$ClusterName = "VxRail-Cluster"
)

Write-Host "`n=== vSAN Health Summary: $ClusterName ($(Get-Date -Format 'yyyy-MM-dd HH:mm')) ===" -ForegroundColor Cyan

$summary = Get-VsanClusterHealthSummary -Cluster $ClusterName -ErrorAction Stop

$overallColor = switch ($summary.OverallHealth) {
    "green"  { "Green" }
    "yellow" { "Yellow" }
    default  { "Red" }
}
Write-Host "Overall Health: $($summary.OverallHealth.ToUpper())" -ForegroundColor $overallColor

foreach ($group in ($summary.Groups | Sort-Object GroupName)) {
    $groupColor = switch ($group.GroupHealth) {
        "green"  { "Green" }
        "yellow" { "Yellow" }
        default  { "Red" }
    }
    Write-Host "`n  [$($group.GroupHealth.ToUpper())] $($group.GroupName)" -ForegroundColor $groupColor

    foreach ($check in ($group.GroupChecks | Sort-Object TestName)) {
        $checkColor = switch ($check.TestHealth) {
            "green"  { "Green" }
            "yellow" { "Yellow" }
            default  { "Red" }
        }
        $icon = if ($check.TestHealth -eq "green") { "  [OK]   " } else { "  [FAIL] " }
        Write-Host "$icon $($check.TestName)" -ForegroundColor $checkColor
    }
}

Write-Host "`n=== End of vSAN Health Summary ===" -ForegroundColor Cyan
```

---

## Script 2 — Cluster Capacity Report

Reports used percentage and free GB for all datastores in the cluster, highlighting those above the alert threshold.

```powershell
# === Cluster Capacity Report ===
# Reports capacity for all datastores; flags datastores above threshold
# Prerequisites: Connect-VIServer

param(
    [string]$ClusterName      = "VxRail-Cluster",
    [int]   $AlertThresholdPct = 70
)

Write-Host "`n=== Cluster Capacity Report: $ClusterName ($(Get-Date -Format 'yyyy-MM-dd HH:mm')) ===" -ForegroundColor Cyan
Write-Host "Alert threshold: $AlertThresholdPct%`n"

$cluster = Get-Cluster $ClusterName
$hosts   = Get-VMHost -Location $cluster
$datastores = Get-Datastore -RelatedObject $cluster | Sort-Object Name

$report = foreach ($ds in $datastores) {
    $usedPct = if ($ds.CapacityGB -gt 0) {
        [Math]::Round((1 - $ds.FreeSpaceGB / $ds.CapacityGB) * 100, 1)
    } else { 0 }

    [PSCustomObject]@{
        Datastore  = $ds.Name
        TotalGB    = [Math]::Round($ds.CapacityGB)
        UsedGB     = [Math]::Round($ds.CapacityGB - $ds.FreeSpaceGB)
        FreeGB     = [Math]::Round($ds.FreeSpaceGB)
        "Used%"    = $usedPct
        Alert      = if ($usedPct -ge $AlertThresholdPct) { "ALERT" } else { "OK" }
    }
}

$report | Sort-Object "Used%" -Descending | ForEach-Object {
    $color = if ($_.Alert -eq "ALERT") { "Red" } else { "Green" }
    Write-Host (
        "  {0,-35} {1,8} GB total  {2,8} GB used  {3,6}%  [{4}]" -f `
        $_.Datastore, $_.TotalGB, $_.UsedGB, $_."Used%", $_.Alert
    ) -ForegroundColor $color
}

Write-Host "`n=== End of Capacity Report ===" -ForegroundColor Cyan
```

---

## Script 3 — Pre-Upgrade Validation

Checks all pre-conditions required before an LCM upgrade. Outputs PASS/FAIL for each condition. All conditions must pass before starting LCM.

```powershell
# === Pre-Upgrade Validation Script ===
# Checks all conditions required before a VxRail LCM upgrade
# Prerequisites: Connect-VIServer + network access to VxRail Manager

param(
    [string]$ClusterName  = "VxRail-Cluster",
    [string]$VxmIp        = "<vxm-ip>",
    [string]$VxmPassword  = "<mystic-password>",
    [string]$VsanDS       = "vsanDatastore"
)

$Auth    = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("mystic:$VxmPassword"))
$Headers = @{ Authorization = "Basic $Auth" }
$AllPass = $true

function Check {
    param([string]$Label, [bool]$Result, [string]$Detail = "")
    if ($Result) {
        Write-Host "  [PASS] $Label" -ForegroundColor Green
    } else {
        Write-Host "  [FAIL] $Label $Detail" -ForegroundColor Red
        $script:AllPass = $false
    }
}

Write-Host "`n=== VxRail Pre-Upgrade Validation: $(Get-Date -Format 'yyyy-MM-dd HH:mm') ===" -ForegroundColor Cyan
Write-Host "  Cluster: $ClusterName`n"

# 1. vSAN overall health
$vsan = Get-VsanClusterHealthSummary -Cluster $ClusterName -ErrorAction SilentlyContinue
Check "vSAN health is green" ($vsan -and $vsan.OverallHealth -eq "green") `
    "(current: $($vsan.OverallHealth))"

# 2. All nodes connected
$cluster      = Get-Cluster $ClusterName
$allHosts     = Get-VMHost -Location $cluster
$disconnected = $allHosts | Where-Object {$_.ConnectionState -ne "Connected"}
Check "All ESXi hosts connected" ($disconnected.Count -eq 0) `
    "($($disconnected.Count) disconnected)"

# 3. DRS fully automated
$drsMode = $cluster.DrsMode
Check "DRS is FullyAutomated" ($drsMode -eq "FullyAutomated") `
    "(current: $drsMode)"

# 4. No active vCenter alarms on cluster
$alarmCount = $cluster.ExtensionData.TriggeredAlarmState.Count
Check "No active vCenter alarms on cluster" ($alarmCount -eq 0) `
    "($alarmCount active alarm(s))"

# 5. vSAN datastore capacity < 80%
$ds = Get-Datastore $VsanDS -ErrorAction SilentlyContinue
if ($ds) {
    $usedPct = [Math]::Round((1 - $ds.FreeSpaceGB / $ds.CapacityGB) * 100, 1)
    Check "vSAN capacity < 80%" ($usedPct -lt 80) "(current: $usedPct%)"
} else {
    Check "vSAN capacity check" $false "(datastore '$VsanDS' not found)"
}

# 6. VxRail Manager reachable
try {
    $clusterInfo = Invoke-RestMethod -Uri "https://$VxmIp/rest/vxm/v1/cluster" `
        -Headers $Headers -SkipCertificateCheck -TimeoutSec 10
    Check "VxRail Manager reachable" ($null -ne $clusterInfo)
} catch {
    Check "VxRail Manager reachable" $false "(exception: $($_.Exception.Message))"
}

# 7. All VxRail hosts healthy via API
try {
    $vxmHosts   = Invoke-RestMethod -Uri "https://$VxmIp/rest/vxm/v1/hosts" `
        -Headers $Headers -SkipCertificateCheck -TimeoutSec 10
    $unhealthy  = $vxmHosts | Where-Object {$_.health -ne "NORMAL"}
    Check "All VxRail hosts NORMAL in VxRail Manager" ($unhealthy.Count -eq 0) `
        "($($unhealthy.Count) unhealthy)"
} catch {
    Check "VxRail host health check" $false "(API error)"
}

# 8. No active LCM job
try {
    $lcm = Invoke-RestMethod -Uri "https://$VxmIp/rest/vxm/v1/lcm/upgrade" `
        -Headers $Headers -SkipCertificateCheck -TimeoutSec 10
    $lcmActive = $lcm.state -and $lcm.state -notin @("NONE","COMPLETED","")
    Check "No active LCM job" (-not $lcmActive) "(current state: $($lcm.state))"
} catch {
    Write-Host "  [INFO] LCM endpoint returned no active job (expected)" -ForegroundColor Gray
}

# Summary
Write-Host ""
if ($AllPass) {
    Write-Host "=== ALL CHECKS PASSED — safe to proceed with LCM upgrade ===" -ForegroundColor Green
} else {
    Write-Host "=== VALIDATION FAILED — resolve all FAIL items before starting LCM ===" -ForegroundColor Red
}
Write-Host ""
```

---

## Script 4 — Node Firmware Version Report

Reports ESXi version, build number, iDRAC firmware version, and BIOS version for every node in the cluster. Requires SSH access to each node's iDRAC.

```powershell
# === Node Firmware Version Report ===
# Reports ESXi version + build per host, iDRAC and BIOS versions via RACADM
# Prerequisites: Connect-VIServer + SSH access to iDRAC IPs
# Requires: Posh-SSH module  (Install-Module -Name Posh-SSH)

param(
    [string]$ClusterName  = "VxRail-Cluster",
    [string]$IpmiNetwork  = "10.0.100.",  # OOB management network prefix
    [string]$IdracUser    = "root",
    [string]$IdracPass    = "<idrac-root-password>"
)

Write-Host "`n=== Node Firmware Version Report: $(Get-Date -Format 'yyyy-MM-dd HH:mm') ===" -ForegroundColor Cyan

$cluster  = Get-Cluster $ClusterName
$allHosts = Get-VMHost -Location $cluster | Sort-Object Name

foreach ($vmhost in $allHosts) {
    Write-Host "`n  Host: $($vmhost.Name)" -ForegroundColor Yellow
    Write-Host "    ESXi Version : $($vmhost.Version)"
    Write-Host "    ESXi Build   : $($vmhost.Build)"

    # Derive iDRAC IP from host annotation or known OOB mapping
    # Adjust this to match your iDRAC IP addressing convention
    $shortName = $vmhost.Name.Split('.')[0]
    $idracIp   = $null

    # Try to get iDRAC IP from host custom attributes (if set)
    $attr = $vmhost.ExtensionData.CustomValue |
        Where-Object {$_.Key -eq (
            ($vmhost.ExtensionData.AvailableField | Where-Object {$_.Name -eq "iDRAC_IP"}).Key
        )}
    if ($attr) { $idracIp = $attr.Value }

    if ($idracIp) {
        try {
            $cred    = New-Object PSCredential($IdracUser, (ConvertTo-SecureString $IdracPass -AsPlainText -Force))
            $session = New-SSHSession -ComputerName $idracIp -Credential $cred -AcceptKey $true -ErrorAction Stop
            $bios    = (Invoke-SSHCommand -SSHSession $session -Command "racadm getversion -f bios").Output -join ""
            $idrac   = (Invoke-SSHCommand -SSHSession $session -Command "racadm getversion -f idrac").Output -join ""
            Remove-SSHSession $session | Out-Null
            Write-Host "    iDRAC IP     : $idracIp"
            Write-Host "    BIOS Version : $($bios.Trim())"
            Write-Host "    iDRAC FW     : $($idrac.Trim())"
        } catch {
            Write-Host "    iDRAC        : Could not connect to $idracIp — $($_.Exception.Message)" -ForegroundColor Red
        }
    } else {
        Write-Host "    iDRAC        : IP not found in host attributes — set 'iDRAC_IP' custom attribute" -ForegroundColor Gray
    }
}

Write-Host "`n=== End of Firmware Report ===" -ForegroundColor Cyan
```

**Note:** To populate iDRAC IPs, set a custom attribute `iDRAC_IP` on each host in vCenter, or modify the script to use a static mapping hashtable:

```powershell
# Alternative: static iDRAC IP mapping
$idracMap = @{
    "vxrail-node-01" = "10.0.100.21"
    "vxrail-node-02" = "10.0.100.22"
    "vxrail-node-03" = "10.0.100.23"
    "vxrail-node-04" = "10.0.100.24"
}
# Then replace the dynamic lookup with:
$idracIp = $idracMap[$shortName]
```

---

## Script 5 — Alert on vSAN Capacity Threshold

Monitors vSAN datastore capacity and outputs an alert when usage exceeds the configured threshold. Designed to run on a schedule (Windows Task Scheduler or cron via PowerShell on Linux).

```powershell
# === vSAN Capacity Alert Script ===
# Checks vSAN datastore usage and alerts when threshold is exceeded
# Run on schedule: Task Scheduler (Windows) or cron with pwsh (Linux)
# Prerequisites: Connect-VIServer + optionally configure SMTP for email alerts

param(
    [string]$VCenterServer    = "vcenter.example.local",
    [string]$VCenterUser      = "administrator@vsphere.local",
    [string]$VCenterPass      = "<vcenter-password>",
    [string]$DatastoreName    = "vsanDatastore",
    [int]   $WarningThreshold = 70,   # percent — send warning alert
    [int]   $CriticalThreshold= 80,   # percent — send critical alert
    [bool]  $SendEmail        = $false,
    [string]$SmtpServer       = "smtp.example.local",
    [string]$AlertEmail       = "ops-team@example.local",
    [string]$FromEmail        = "vxrail-alerts@example.local"
)

# Connect to vCenter
$cred = New-Object PSCredential($VCenterUser, (ConvertTo-SecureString $VCenterPass -AsPlainText -Force))
Connect-VIServer -Server $VCenterServer -Credential $cred -ErrorAction Stop | Out-Null

$ds = Get-Datastore $DatastoreName -ErrorAction SilentlyContinue

if (-not $ds) {
    Write-Error "Datastore '$DatastoreName' not found"
    Disconnect-VIServer -Confirm:$false
    exit 1
}

$totalGB  = [Math]::Round($ds.CapacityGB, 1)
$freeGB   = [Math]::Round($ds.FreeSpaceGB, 1)
$usedGB   = [Math]::Round($totalGB - $freeGB, 1)
$usedPct  = [Math]::Round((1 - $ds.FreeSpaceGB / $ds.CapacityGB) * 100, 1)
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"

$message = "[$timestamp] vSAN Capacity: $usedPct% used ($usedGB GB / $totalGB GB) — Free: $freeGB GB"

if ($usedPct -ge $CriticalThreshold) {
    Write-Host "CRITICAL: $message" -ForegroundColor Red
    if ($SendEmail) {
        Send-MailMessage -SmtpServer $SmtpServer -From $FromEmail -To $AlertEmail `
            -Subject "CRITICAL: vSAN capacity $usedPct% on $DatastoreName" `
            -Body $message -Priority High
    }
    $exitCode = 2
} elseif ($usedPct -ge $WarningThreshold) {
    Write-Host "WARNING: $message" -ForegroundColor Yellow
    if ($SendEmail) {
        Send-MailMessage -SmtpServer $SmtpServer -From $FromEmail -To $AlertEmail `
            -Subject "WARNING: vSAN capacity $usedPct% on $DatastoreName" `
            -Body $message
    }
    $exitCode = 1
} else {
    Write-Host "OK: $message" -ForegroundColor Green
    $exitCode = 0
}

Disconnect-VIServer -Confirm:$false
exit $exitCode
```

### Schedule with Windows Task Scheduler

```powershell
# Create a scheduled task to run the capacity alert every 4 hours
$action  = New-ScheduledTaskAction -Execute "pwsh.exe" `
    -Argument "-NonInteractive -File C:\scripts\vxrail\vsan-capacity-alert.ps1"
$trigger = New-ScheduledTaskTrigger -RepetitionInterval (New-TimeSpan -Hours 4) `
    -Once -At (Get-Date)
Register-ScheduledTask -TaskName "VxRail-vSAN-Capacity-Alert" `
    -Action $action -Trigger $trigger -RunLevel Highest -Force
```

### Schedule with cron (Linux/macOS with PowerShell)

```bash
# Edit crontab
crontab -e

# Run capacity alert every 4 hours
0 */4 * * * /usr/bin/pwsh /opt/scripts/vxrail/vsan-capacity-alert.ps1 >> /var/log/vxrail-capacity.log 2>&1
```

---

## See also

- [VxRail — CLI Reference](cli-reference/)
- [VxRail — Procedures](procedures/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
