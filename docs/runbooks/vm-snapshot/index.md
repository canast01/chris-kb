# VM Snapshot Runbook

Snapshots capture a point-in-time VM state before a change. They are not backups — remove within 24–72 hours. Large delta disks degrade performance.
## Pre-Checks

```powershell
# Confirm no existing snapshots
Get-VM <vmname> | Get-Snapshot

# Check datastore free space (need ≥ 20% free)
Get-Datastore | Select Name, @{N="FreePct";E={[math]::Round($_.FreeSpaceMB / $_.CapacityMB * 100,1)}}
```

## Create Snapshot (PowerCLI)

```powershell
# Crash-consistent
New-Snapshot -VM <vmname> \
    -Name "pre-change-$(Get-Date -Format yyyyMMdd-HHmm)" \
    -Description "Before <change>"

# App-consistent (quiesce with VMware Tools)
New-Snapshot -VM <vmname> \
    -Name "pre-change-$(Get-Date -Format yyyyMMdd-HHmm)" \
    -Quiesce -Memory:$false
```

## Create Snapshot (ESXi CLI)

```bash
# Get VM ID
vim-cmd vmsvc/getallvms | grep <vmname>

# Take snapshot (VMID, name, description, memory, quiesce)
vim-cmd vmsvc/snapshot.create <VMID> "pre-change" "Before change" 0 0

# List snapshots
vim-cmd vmsvc/snapshot.get <VMID>
```

## Revert to Snapshot (if change fails)

```powershell
$snap = Get-VM <vmname> | Get-Snapshot -Name "pre-change*"
Set-VM <vmname> -Snapshot $snap -Confirm:$false
```

## Remove Snapshot (after successful change)

```powershell
Get-VM <vmname> | Get-Snapshot | Remove-Snapshot -Confirm:$false

# Confirm no consolidation needed
(Get-VM <vmname>).Extensiondata.Runtime.ConsolidationNeeded
# Should return: False
```

## Checklist

- [ ] No existing snapshots on VM
- [ ] Datastore ≥ 20% free
- [ ] Snapshot created and confirmed
- [ ] Change completed
- [ ] Application validated
- [ ] Snapshot removed within change window
- [ ] Consolidation clean

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Snapshot fails | Datastore space | Clear space; use different datastore |
| Consolidation needed | Delta disks | Run vSphere consolidation |
| Old snapshot exists | Missed cleanup | Remove immediately |
| Quiesce fails | VMware Tools | Use crash-consistent instead |
