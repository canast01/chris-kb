# Inventory & Reporting

> Part of the [vCenter CLI Reference (PowerCLI & DCLI)](../).

## VM Inventory Export

```powershell
# Full VM inventory to CSV
Get-VM | Select-Object Name, PowerState, NumCpu, MemoryGB,
    @{N="VMHost";E={$_.VMHost.Name}},
    @{N="Cluster";E={$_.VMHost.Parent.Name}},
    @{N="Datastore";E={($_ | Get-Datastore).Name -join ";"}},
    @{N="GuestOS";E={$_.Guest.OSFullName}},
    @{N="IP";E={$_.Guest.IPAddress -join ";"}} |
    Export-Csv -Path vm_inventory.csv -NoTypeInformation
```

## Host Inventory Export

```powershell
# Full host inventory to CSV
Get-VMHost | Select-Object Name, Version, Build, Manufacturer, Model,
    @{N="CPUModel";E={$_.ProcessorType}},
    @{N="NumCPU";E={$_.NumCpu}},
    @{N="MemGB";E={[math]::Round($_.MemoryTotalGB, 0)}},
    ConnectionState, PowerState |
    Export-Csv -Path host_inventory.csv -NoTypeInformation
```

## Cluster Inventory

```powershell
# All clusters with host count
Get-Cluster | Select-Object Name, HAEnabled, DrsEnabled,
    @{N="Hosts";E={($_ | Get-VMHost).Count}},
    @{N="VMs";E={($_ | Get-VM).Count}}
```

## Orphaned and Disconnected VMs

```powershell
# VMs with disconnected or inaccessible state
Get-VM | Where-Object { $_.ExtensionData.Summary.Runtime.ConnectionState -ne "connected" } |
    Select-Object Name, PowerState

# Powered-off VMs (orphan candidates)
Get-VM | Where-Object { $_.PowerState -eq "PoweredOff" } |
    Select-Object Name, @{N="Host";E={$_.VMHost.Name}},
    @{N="LastChange";E={$_.ExtensionData.Config.ChangeVersion}}
```

## Snapshots Across All VMs

```powershell
# All snapshots — sorted by size
Get-VM | Get-Snapshot |
    Select-Object @{N="VM";E={$_.VM.Name}}, Name, Created,
    @{N="SizeGB";E={[math]::Round($_.SizeGB, 2)}} |
    Sort-Object SizeGB -Descending

# Snapshots older than 7 days
Get-VM | Get-Snapshot | Where-Object { $_.Created -lt (Get-Date).AddDays(-7) } |
    Select-Object @{N="VM";E={$_.VM.Name}}, Name, Created
```

## Tag and Category Inventory

```powershell
# All tags
Get-Tag

# VMs with a specific tag
Get-VM | Where-Object { (Get-TagAssignment -Entity $_).Tag.Name -contains "production" }

# Tag assignment report
Get-VM | ForEach-Object {
    $vm = $_
    Get-TagAssignment -Entity $vm | ForEach-Object {
        [PSCustomObject]@{ VM = $vm.Name; Tag = $_.Tag.Name; Category = $_.Tag.Category.Name }
    }
} | Export-Csv -Path vm_tags.csv -NoTypeInformation
```

## Resource Pool Inventory

```powershell
# All resource pools
Get-ResourcePool | Select-Object Name, CpuSharesLevel, MemSharesLevel,
    @{N="Cluster";E={$_.Parent.Name}}

# VMs in a resource pool
Get-ResourcePool -Name "<pool_name>" | Get-VM | Select-Object Name, PowerState
```

## Folder Structure

```powershell
# All VM folders
Get-Folder -Type VM | Select-Object Name, @{N="Parent";E={$_.Parent.Name}}

# VMs in a specific folder
Get-Folder -Name "<folder_name>" | Get-VM
```
