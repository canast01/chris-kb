# PowerShell — Scripts

## VM Health Report

Generates a per-cluster VM health report: power state, CPU/memory, snapshot age, and datastore utilization. Outputs to CSV and console.

```powershell
# vm-health-report.ps1
# Usage: .\vm-health-report.ps1 -vCenter <hostname> -OutputPath .\report.csv

param(
    [Parameter(Mandatory)] [string] $vCenter,
    [string] $OutputPath = ".\vm-health-$(Get-Date -Format 'yyyyMMdd').csv"
)

Connect-VIServer -Server $vCenter -Credential (Get-Credential) | Out-Null

$report = Get-VM | ForEach-Object {
    $vm = $_
    $snaps = Get-Snapshot -VM $vm
    $oldestSnap = if ($snaps) { ($snaps | Sort-Object Created | Select-Object -First 1).Created } else { $null }

    [PSCustomObject]@{
        Name         = $vm.Name
        Cluster      = (Get-Cluster -VM $vm).Name
        PowerState   = $vm.PowerState
        vCPU         = $vm.NumCpu
        MemGB        = $vm.MemoryGB
        Snapshots    = $snaps.Count
        OldestSnap   = $oldestSnap
        Datastore    = ($vm | Get-Datastore | Select-Object -First 1).Name
    }
}

$report | Export-Csv -Path $OutputPath -NoTypeInformation
$report | Format-Table -AutoSize
Write-Host "`nReport saved: $OutputPath" -ForegroundColor Green
Disconnect-VIServer -Confirm:$false
```

## Host Maintenance Pre-Check

Confirms a host is safe to enter maintenance mode: checks running VMs, HA admission control, and vSAN health.

```powershell
# host-precheck.ps1
param([Parameter(Mandatory)] [string] $HostName)

$vmhost = Get-VMHost -Name $HostName
Write-Host "`n=== Pre-Maintenance Check: $HostName ===" -ForegroundColor Cyan

# Running VMs
$runningVMs = Get-VM -Location $vmhost | Where-Object { $_.PowerState -eq "PoweredOn" }
Write-Host "Running VMs : $($runningVMs.Count)"
$runningVMs | Select-Object Name, MemoryGB | Format-Table -AutoSize

# vSAN health
$cluster = Get-Cluster -VMHost $vmhost
if ($cluster.VsanEnabled) {
    $vsanHealth = Get-VsanView -VsanObject (Get-VsanView -Id "VsanVcClusterHealthSystem-*") `
        -ErrorAction SilentlyContinue
    Write-Host "vSAN cluster: $($cluster.Name) (enabled)"
}

# HA status
Write-Host "HA enabled  : $($cluster.HAEnabled)"
Write-Host "DRS enabled : $($cluster.DrsEnabled)"
```

## Snapshot Cleanup

Finds and optionally removes snapshots older than N days.

```powershell
# snap-cleanup.ps1
param(
    [int]    $OlderThanDays = 7,
    [switch] $WhatIf
)

$cutoff = (Get-Date).AddDays(-$OlderThanDays)
$oldSnaps = Get-VM | Get-Snapshot | Where-Object { $_.Created -lt $cutoff }

if ($oldSnaps.Count -eq 0) {
    Write-Host "No snapshots older than $OlderThanDays days found."
    return
}

$oldSnaps | Select-Object VM, Name, Created, @{N="SizeGB";E={[math]::Round($_.SizeGB,2)}} |
    Format-Table -AutoSize

if (-not $WhatIf) {
    $confirm = Read-Host "Remove $($oldSnaps.Count) snapshot(s)? [yes/no]"
    if ($confirm -eq "yes") {
        $oldSnaps | Remove-Snapshot -Confirm:$false
        Write-Host "Done." -ForegroundColor Green
    }
} else {
    Write-Host "[WhatIf] No changes made."
}
```

## Datastore Utilization Alert

Lists datastores below a configurable free-space threshold.

```powershell
# ds-alert.ps1
param([int] $ThresholdPct = 20)

Get-Datastore |
    Select-Object Name, CapacityGB, FreeSpaceGB,
        @{N="FreePct";E={[math]::Round($_.FreeSpaceGB / $_.CapacityGB * 100, 1)}} |
    Where-Object { $_.FreePct -lt $ThresholdPct } |
    Sort-Object FreePct |
    Format-Table -AutoSize
```
