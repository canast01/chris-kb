---
tags:
  - operations
  - powercli
  - vmware
---
# PowerCLI — Procedures

<div class="kb-summary">
Common operational procedures using PowerCLI: bulk VM operations, host maintenance workflow, snapshot consolidation, datastore migration, and tag management at scale.

*Applies to: PowerCLI 13.x*
</div>

```text
┌────────────────────────────── PowerCLI — Common Operational Procedures ───────────────────────────────┐
│                                                                                                       │
│   Common administrative procedures with PowerCLI for bulk and single-object operations                │
│   All procedures follow: pre-check → act → verify → report pattern                                    │
│   Use -WhatIf with Set-/Remove- cmdlets to preview impact before committing                           │
│                                                                                                       │
│   Host maintenance mode                                                                               │
│   Get running VMs on host; confirm DRS will drain (Fully Automated cluster required)                  │
│   Set-VMHost -State Maintenance -Evacuate:$true; wait until VMs = 0 before patching                   │
│   Exit: Set-VMHost -State Connected; verify host reconnects and cluster HA recalculates               │
│                                                                                                       │
│   Snapshot management                                                                                 │
│   Audit: Get-VM | Get-Snapshot | Where-Object { $_.Created -lt (Get-Date).AddDays(-2) }               │
│   Remove: Remove-Snapshot -Snapshot $snap -Confirm:$false; one snapshot at a time for safety          │
│   Consolidate: Get-VM | Where-Object { $_.Extensiondata.Runtime.ConsolidationNeeded }                 │
│                                                                                                       │
│   Bulk VM operations                                                                                  │
│   Power off by tag: Get-VM -Tag "maintenance" | Stop-VMGuest -Confirm:$false                          │
│   Restart tools: Get-VM | Where-Object { $_.ExtensionData.Guest.ToolsRunningStatus -eq 'toolsOld' }   │
│   Move to folder: Get-VM -Name "app-*" | Move-VM -Destination (Get-Folder "AppServers")               │
│                                                                                                       │
│   Storage vMotion (datastore migration)                                                               │
│   Single VM: Move-VM -VM $vm -Datastore $target -DiskStorageFormat Thin                               │
│   Bulk: Get-Datastore "old-ds" | Get-VM | Move-VM -Datastore $target                                  │
│   Monitor: track with Get-Task | Where-Object { $_.State -eq 'Running' }                              │
│                                                                                                       │
│   Key terms:                                                                                          │
│   -Evacuate     = with Set-VMHost maintenance; triggers DRS to migrate all VMs off the host           │
│   -Confirm:$false = suppresses the Y/N prompt in scripts; required for unattended automation          │
│   Get-Task      = retrieves running and recent vCenter tasks; monitor long-running operations         │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Put Host in Maintenance Mode

```powershell
# Full maintenance mode workflow with SVMOTION
$hostName = "esxi01.example.com"
$host = Get-VMHost -Name $hostName

# Check VMs running on the host
$runningVMs = Get-VM -VMHost $host | Where-Object { $_.PowerState -eq 'PoweredOn' }
Write-Host "$($runningVMs.Count) powered-on VMs on $hostName"

# Enter maintenance mode (triggers vMotion of all VMs)
Set-VMHost -VMHost $host -State Maintenance -Confirm:$false
# Wait for state
do {
    Start-Sleep 10
    $state = (Get-VMHost -Name $hostName).ConnectionState
    Write-Host "Current state: $state"
} until ($state -eq 'Maintenance')
Write-Host "$hostName is in maintenance mode"

# After patching/maintenance — exit maintenance mode
Set-VMHost -VMHost (Get-VMHost -Name $hostName) -State Connected -Confirm:$false
```

## Bulk Snapshot Cleanup

```powershell
# Remove snapshots older than N days across all VMs in a cluster
$cluster = "Production"
$daysOld = 14
$cutoff = (Get-Date).AddDays(-$daysOld)

$snaps = Get-VM -Location (Get-Cluster -Name $cluster) | Get-Snapshot | Where-Object { $_.Created -lt $cutoff }
Write-Host "Found $($snaps.Count) snapshots older than $daysOld days"
$snaps | Select-Object @{N="VM";E={$_.VM.Name}}, Name, Created | Format-Table

# Remove with confirmation per VM
$snaps | Group-Object { $_.VM.Name } | ForEach-Object {
    $vmName = $_.Name
    $vmSnaps = $_.Group
    $resp = Read-Host "Remove $($vmSnaps.Count) snapshot(s) for $vmName? (y/n)"
    if ($resp -eq 'y') {
        $vmSnaps | Remove-Snapshot -RemoveChildren -Confirm:$false
        Write-Host "Removed snapshots for $vmName" -ForegroundColor Green
    }
}
```

## Bulk VM Power Operations

```powershell
# Graceful shutdown of all VMs in a folder (ordered)
$folder = Get-Folder -Name "Pre-Maintenance-VMs"
$vms = Get-VM -Location $folder | Where-Object { $_.PowerState -eq 'PoweredOn' } | Sort-Object Name

# Graceful shutdown via guest OS
$vms | ForEach-Object {
    Write-Host "Shutting down $($_.Name)..."
    Shutdown-VMGuest -VM $_ -Confirm:$false
}

# Wait for all to power off
do {
    Start-Sleep 15
    $still_on = Get-VM -Location $folder | Where-Object { $_.PowerState -eq 'PoweredOn' }
    Write-Host "Still running: $($still_on.Count)"
} until ($still_on.Count -eq 0)
Write-Host "All VMs powered off"

# Power on in batch (reverse order for startup sequence)
Get-VM -Location $folder | Where-Object { $_.PowerState -eq 'PoweredOff' } | Sort-Object Name -Descending |
    ForEach-Object {
        Start-VM -VM $_ -Confirm:$false
        Start-Sleep 5    # stagger starts
    }
```

## Storage vMotion (Datastore Migration)

```powershell
# Move VMs from one datastore to another
$sourceDS = Get-Datastore -Name "OldDatastore"
$targetDS = Get-Datastore -Name "vSAN-Production"

# Find VMs on source datastore
$vms = Get-VM | Where-Object { ($_ | Get-Datastore) -contains $sourceDS }
Write-Host "Found $($vms.Count) VMs on $($sourceDS.Name)"

# Move VMs (one at a time to avoid overloading)
$vms | ForEach-Object {
    Write-Host "Moving $($_.Name) to $($targetDS.Name)..."
    Move-VM -VM $_ -Datastore $targetDS -Confirm:$false
    Start-Sleep 2
}
```

## Bulk Tag Assignment

```powershell
# Assign environment tags to VMs based on a name pattern
$category = Get-TagCategory -Name "Environment"
$prodTag   = Get-Tag -Name "Production"  -Category $category
$devTag    = Get-Tag -Name "Development" -Category $category
$testTag   = Get-Tag -Name "Test"        -Category $category

Get-VM | ForEach-Object {
    $vm = $_
    $existingTag = Get-TagAssignment -Entity $vm | Select-Object -ExpandProperty Tag
    if ($existingTag) { continue }   # already tagged

    $tag = switch -Wildcard ($vm.Name) {
        "prod-*" { $prodTag }
        "dev-*"  { $devTag  }
        "tst-*"  { $testTag }
        default  { $null    }
    }

    if ($tag) {
        New-TagAssignment -Tag $tag -Entity $vm
        Write-Host "Tagged $($vm.Name) as $($tag.Name)"
    }
}
```

## VM Clone from Template

```powershell
# Clone VMs from a template with customization spec
$template = Get-Template -Name "Win2022-Base"
$custSpec  = Get-OSCustomizationSpec -Name "Windows-Domain-Join"
$cluster   = Get-Cluster -Name "Production"
$datastore = Get-Datastore -Name "vSAN-Production"
$folder    = Get-Folder -Name "Production-VMs"

$vmNames = @("web01", "web02", "app01")

$vmNames | ForEach-Object {
    Write-Host "Cloning $_..."
    New-VM -Name $_ -Template $template -VMHost (Get-VMHost -Location $cluster | Get-Random) `
           -Datastore $datastore -Location $folder -OSCustomizationSpec $custSpec -Confirm:$false
}

# Wait for customization to complete
Start-Sleep 120
$vmNames | ForEach-Object {
    $vm = Get-VM -Name $_
    Start-VM -VM $vm -Confirm:$false
}
Write-Host "All VMs cloned and started"
```
