# PowerShell VMware (PowerCLI)

## Installing and Connecting PowerCLI

VMware PowerCLI is a set of PowerShell modules for managing vSphere, NSX, and vSAN.

```powershell
# Install PowerCLI (current user, no admin required)
Install-Module -Name VMware.PowerCLI -Scope CurrentUser -AllowClobber -Force

# Disable certificate checking for lab environments
Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false

# Disable CEIP telemetry
Set-PowerCLIConfiguration -Scope User -ParticipateInCEIP $false -Confirm:$false

# Connect to a vCenter Server
Connect-VIServer -Server vcenter.example.com -User administrator@vsphere.local -Password 'P@ssword1'

# Connect using stored credentials
$cred = Get-Credential
Connect-VIServer -Server vcenter.example.com -Credential $cred

# Disconnect when done
Disconnect-VIServer -Server * -Confirm:$false
```

## Get-VM and Filtering

```powershell
# List all VMs
Get-VM

# Filter by name pattern
Get-VM -Name 'web*'

# Filter by power state
Get-VM | Where-Object { $_.PowerState -eq 'PoweredOff' }

# VMs on a specific host
Get-VMHost -Name esx01.example.com | Get-VM

# Get VM hardware details
Get-VM web01 | Select-Object Name, NumCpu, MemoryGB, PowerState,
    @{N='ProvisionedGB';E={[math]::Round($_.ProvisionedSpaceGB,2)}}
```

## Set-VM and VM Configuration

```powershell
# Change vCPU and memory (VM must be powered off for most changes)
Get-VM -Name web01 | Set-VM -NumCpu 4 -MemoryGB 8 -Confirm:$false

# Add a network adapter
Get-VM web01 | New-NetworkAdapter -NetworkName 'VM Network' -Type VMXNET3 -StartConnected

# Add a hard disk
Get-VM web01 | New-HardDisk -CapacityGB 100 -StorageFormat Thin -Confirm:$false

# Power operations
Start-VM -VM web01 -Confirm:$false
Stop-VM -VM web01 -Confirm:$false
Restart-VM -VM web01 -Confirm:$false
Suspend-VM -VM web01 -Confirm:$false
```

## Snapshots

```powershell
# Create a snapshot before patching
New-Snapshot -VM web01 -Name 'Pre-patch-$(Get-Date -Format yyyyMMdd)' `
    -Description 'Snapshot before OS patching' -Memory:$false -Quiesce:$false

# List all snapshots for a VM
Get-Snapshot -VM web01

# List all snapshots across all VMs (useful for audit)
Get-VM | Get-Snapshot | Select-Object VM, Name, Created, SizeMB |
    Sort-Object Created | Format-Table -AutoSize

# Revert to a snapshot
Set-VM -VM web01 -Snapshot (Get-Snapshot -VM web01 -Name 'Pre-patch-*') -Confirm:$false

# Remove a specific snapshot
Remove-Snapshot -Snapshot (Get-Snapshot -VM web01 -Name 'Pre-patch-*') -Confirm:$false

# Remove all snapshots for a VM
Get-Snapshot -VM web01 | Remove-Snapshot -RemoveChildren -Confirm:$false
```

## Datastores and Storage

```powershell
# List all datastores with capacity info
Get-Datastore | Select-Object Name,
    @{N='CapacityGB';E={[math]::Round($_.CapacityGB,0)}},
    @{N='FreeGB';E={[math]::Round($_.FreeSpaceGB,0)}},
    @{N='UsedPct';E={[math]::Round((1-$_.FreeSpaceGB/$_.CapacityGB)*100,1)}} |
    Sort-Object UsedPct -Descending | Format-Table

# Move a VM to a different datastore
Move-VM -VM web01 -Datastore (Get-Datastore 'SSD-01') -Confirm:$false
```

## PowerCLI Command Reference

| Cmdlet | Purpose |
|---|---|
| `Get-VM` | List VMs |
| `Start-VM / Stop-VM` | Power on/off |
| `New-Snapshot / Remove-Snapshot` | Snapshot management |
| `Get-VMHost` | List ESXi hosts |
| `Get-Datastore` | List datastores |
| `Move-VM` | Migrate VM via Storage vMotion |
| `Get-VIEvent` | Query vCenter event log |
| `Invoke-VMScript` | Run script inside guest OS |
