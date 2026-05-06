# Snapshots

> Part of the [vCenter CLI Reference (PowerCLI & DCLI)](../).

## List Snapshots

```powershell
# Snapshots for a specific VM
Get-Snapshot -VM "<vm_name>"

# All snapshots across all VMs — sorted by size
Get-VM | Get-Snapshot |
    Select-Object @{N="VM";E={$_.VM.Name}}, Name, Created,
    @{N="SizeGB";E={[math]::Round($_.SizeGB, 2)}} |
    Sort-Object SizeGB -Descending

# Snapshots older than 7 days (maintenance risk)
Get-VM | Get-Snapshot |
    Where-Object { $_.Created -lt (Get-Date).AddDays(-7) } |
    Select-Object @{N="VM";E={$_.VM.Name}}, Name, Created,
    @{N="AgeDays";E={[math]::Round(((Get-Date) - $_.Created).TotalDays, 0)}}
```

## Create Snapshots

```powershell
# Crash-consistent snapshot (no memory, no quiesce)
New-Snapshot -VM "<vm_name>" -Name "pre-patch-$(Get-Date -Format yyyy-MM-dd)" `
    -Memory:$false -Quiesce:$false

# Application-consistent snapshot (quiesced — requires VMware Tools)
New-Snapshot -VM "<vm_name>" -Name "app-consistent-$(Get-Date -Format yyyy-MM-dd)" `
    -Memory:$false -Quiesce:$true

# Memory snapshot (captures RAM state — slower, larger)
New-Snapshot -VM "<vm_name>" -Name "memory-$(Get-Date -Format yyyy-MM-dd)" `
    -Memory:$true -Quiesce:$false
```

## Remove Snapshots

```powershell
# Remove a named snapshot
Remove-Snapshot `
    -Snapshot (Get-Snapshot -VM "<vm_name>" -Name "<snap_name>") `
    -Confirm:$false

# Remove all snapshots for a VM (consolidates chain)
Remove-Snapshot -VM "<vm_name>" -RemoveChildren -Confirm:$false

# Remove all old snapshots across all VMs (older than 7 days)
Get-VM | Get-Snapshot |
    Where-Object { $_.Created -lt (Get-Date).AddDays(-7) } |
    Remove-Snapshot -Confirm:$false
```

## Revert to Snapshot

```powershell
# Revert a VM to a named snapshot
Set-VM -VM "<vm_name>" `
    -Snapshot (Get-Snapshot -VM "<vm_name>" -Name "<snap_name>") `
    -Confirm:$false
```

## Snapshot Consolidation

Unconsolidated snapshots waste space and degrade performance:

```powershell
# Find VMs needing consolidation
Get-VM | Where-Object { $_.ExtensionData.Runtime.ConsolidationNeeded } |
    Select-Object Name

# Consolidate a VM's snapshots
(Get-VM "<vm_name>").ExtensionData.ConsolidateVMDisks_Task()
```

## Snapshot Best Practices

| Rule | Reason |
|---|---|
| Keep for ≤ 72 hours | Delta files grow rapidly; IOPS penalty worsens over time |
| Never snapshot during backup | Backup tools manage their own snapshots — nested chains cause corruption |
| Use `-Quiesce:$true` for databases | Ensures file-system consistency for SQL/Exchange |
| Remove, don't just revert | Reverting does not delete the chain — `Remove-Snapshot` consolidates |
| Monitor `ConsolidationNeeded` | Failed consolidation = orphaned delta files consuming space |
