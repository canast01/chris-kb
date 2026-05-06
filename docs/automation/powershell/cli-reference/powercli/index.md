# VMware PowerCLI

> Part of the PowerShell CLI Reference.

---

```powershell
# Install / connect
Install-Module VMware.PowerCLI -Scope CurrentUser
Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false
Connect-VIServer -Server <vcenter> -Credential (Get-Credential)
Disconnect-VIServer -Confirm:$false

# VMs
Get-VM
Get-VM -Name <name>
Get-VM | Where-Object { $_.PowerState -eq "PoweredOff" }
Start-VM -VM <name>
Stop-VM -VM <name> -Confirm:$false
Restart-VM -VM <name> -Confirm:$false
Suspend-VM -VM <name>

# VM config
Get-VM <name> | Get-HardDisk
Get-VM <name> | Get-NetworkAdapter
Set-VM -VM <name> -NumCpu 4 -MemoryGB 16 -Confirm:$false

# Snapshots
Get-Snapshot -VM <name>
New-Snapshot -VM <name> -Name "pre-patch" -Memory:$false -Quiesce:$false
Remove-Snapshot -Snapshot <snap> -Confirm:$false
Set-VM -VM <name> -Snapshot <snap> -Confirm:$false  # Revert

# Hosts
Get-VMHost
Get-VMHost -Name <hostname>
Get-VMHost | Select-Object Name, PowerState, ConnectionState, Version
Set-VMHost -VMHost <host> -State Maintenance

# Clusters
Get-Cluster
Get-Cluster <name> | Get-VMHost
Get-Cluster | Get-VM

# Datastores
Get-Datastore
Get-Datastore | Select-Object Name, CapacityGB, FreeSpaceGB
Get-Datastore | Where-Object { ($_.FreeSpaceGB / $_.CapacityGB) -lt 0.2 }

# vSAN
Get-VsanView
Get-VsanClusterConfiguration -Cluster <cluster>

# Resource pools
Get-ResourcePool
Get-ResourcePool -Name <name> | Get-VM

# vCenter events
Get-VIEvent -MaxSamples 100
Get-VIEvent -Start (Get-Date).AddHours(-24)

# Tags
Get-Tag
Get-TagCategory
New-Tag -Name <tag> -Category <category>
Get-VM <name> | Get-TagAssignment
New-TagAssignment -Tag <tag> -Entity (Get-VM <name>)
```
