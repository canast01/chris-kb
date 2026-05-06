# vCenter CLI Reference (PowerCLI & DCLI)

Commonly used PowerCLI and vCenter shell commands for managing vSphere environments.

> Requires VMware.PowerCLI module. Use `Connect-VIServer -Server <vcenter>` before running PowerCLI commands.

---

## Connection & Session

```powershell
# Install PowerCLI
Install-Module VMware.PowerCLI -Scope CurrentUser
Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false
Set-PowerCLIConfiguration -ParticipateInCeip $false -Confirm:$false

# Connect
Connect-VIServer -Server <vcenter>
Connect-VIServer -Server <vcenter> -User <user> -Password <pass>
Disconnect-VIServer * -Confirm:$false

# Who am I
$global:DefaultVIServer
```

---

## Hosts

```powershell
# List all hosts
Get-VMHost
Get-VMHost | Select-Object Name, State, PowerState, ConnectionState, Version | Format-Table

# Host by name or cluster
Get-VMHost -Name <hostname>
Get-Cluster <cluster_name> | Get-VMHost

# Host details
Get-VMHost <host> | Select-Object *
Get-VMHost <host> | Get-VMHostHardware

# Maintenance mode
Set-VMHost -VMHost <host> -State Maintenance
Set-VMHost -VMHost <host> -State Connected

# Host services
Get-VMHostService -VMHost <host>
Start-VMHostService -HostService (Get-VMHostService -VMHost <host> | Where-Object { $_.Key -eq "TSM-SSH" })
Stop-VMHostService -HostService (Get-VMHostService -VMHost <host> | Where-Object { $_.Key -eq "TSM-SSH" })

# NTP
Get-VMHostNtpServer -VMHost <host>
Add-VMHostNtpServer -VMHost <host> -NtpServer <ip>

# Syslog
Get-VMHostSysLogServer -VMHost <host>
Set-VMHostSysLogServer -VMHost <host> -SysLogServer udp://<ip>:514
```

---

## Clusters

```powershell
Get-Cluster
Get-Cluster -Name <name>
Get-Cluster | Select-Object Name, HAEnabled, DrsEnabled, DrsAutomationLevel | Format-Table
Get-Cluster | Get-VMHost | Select-Object Name, State, @{N="Cluster";E={$_.Parent}} | Format-Table

# New cluster
New-Cluster -Name <name> -Location (Get-Datacenter <dc>) -HAEnabled -DrsEnabled
```

---

## Virtual Machines

```powershell
# List
Get-VM
Get-VM -Name <name>
Get-VM | Where-Object { $_.PowerState -eq "PoweredOff" }
Get-VM | Select-Object Name, PowerState, NumCpu, MemoryGB, VMHost | Format-Table

# Power operations
Start-VM -VM <name>
Stop-VM -VM <name> -Confirm:$false
Shutdown-VMGuest -VM <name> -Confirm:$false
Restart-VM -VM <name> -Confirm:$false
Restart-VMGuest -VM <name> -Confirm:$false
Suspend-VM -VM <name>

# VM config
Get-VM <name> | Get-HardDisk
Get-VM <name> | Get-NetworkAdapter
Set-VM -VM <name> -NumCpu 4 -MemoryGB 16 -Confirm:$false

# Move VM
Move-VM -VM <name> -Destination (Get-VMHost <host>)
Move-VM -VM <name> -Datastore (Get-Datastore <ds>)

# Clone
New-VM -Name <new_name> -VM <source_vm> -VMHost <host> -Datastore <ds>

# Guest OS info
Get-VM <name> | Select-Object @{N="IP";E={$_.Guest.IPAddress -join ", "}}, @{N="OS";E={$_.Guest.OSFullName}}
```

---

## Snapshots

```powershell
Get-Snapshot -VM <name>
Get-VM | Get-Snapshot | Select-Object VM, Name, Created, @{N="SizeGB";E={[math]::Round($_.SizeGB,2)}} | Sort-Object SizeGB -Descending

New-Snapshot -VM <name> -Name "pre-patch-$(Get-Date -Format yyyy-MM-dd)" -Memory:$false -Quiesce:$false
Remove-Snapshot -Snapshot (Get-Snapshot -VM <name> -Name <snap_name>) -Confirm:$false
Remove-Snapshot -VM <name> -RemoveChildren -Confirm:$false

# Revert
Set-VM -VM <name> -Snapshot (Get-Snapshot -VM <name> -Name <snap_name>) -Confirm:$false
```

---

## Datastores

```powershell
Get-Datastore
Get-Datastore | Select-Object Name, CapacityGB, FreeSpaceGB, @{N="UsedPct";E={[math]::Round((1-$_.FreeSpaceGB/$_.CapacityGB)*100,1)}} | Sort-Object UsedPct -Descending

# Datastores below threshold
Get-Datastore | Where-Object { ($_.FreeSpaceGB / $_.CapacityGB) -lt 0.2 } | Select-Object Name, FreeSpaceGB

# Datastore cluster
Get-DatastoreCluster
Get-DatastoreCluster | Get-Datastore
```

---

## Networks

```powershell
# Standard switches
Get-VirtualSwitch -VMHost <host>
Get-VirtualPortGroup -VMHost <host>

# Distributed switches
Get-VDSwitch
Get-VDSwitch | Select-Object Name, NumPorts, Version
Get-VDPortgroup

# VMkernel adapters
Get-VMHostNetworkAdapter -VMHost <host> -VMKernel
Get-VMHostNetworkAdapter -VMHost <host> -VMKernel | Select-Object Name, IP, SubnetMask, VMotionEnabled, ManagementTrafficEnabled
```

---

## Alarms & Events

```powershell
# Triggered alarms
Get-AlarmDefinition
Get-VM | Where-Object { $_.ExtensionData.TriggeredAlarmState.Count -gt 0 }

# Events
Get-VIEvent -MaxSamples 200
Get-VIEvent -Start (Get-Date).AddHours(-24)
Get-VIEvent -Entity (Get-VM <name>) -MaxSamples 50
Get-VIEvent -MaxSamples 500 | Where-Object { $_.GetType().Name -eq "TaskEvent" } | Select-Object CreatedTime, UserName, FullFormattedMessage
```

---

## Permissions & Roles

```powershell
# Roles
Get-VIRole
Get-VIRole -Name "ReadOnly"

# Permissions
Get-VIPermission
Get-VIPermission | Where-Object { $_.Principal -eq "<domain>\<user>" }

# Assign role
New-VIPermission -Entity (Get-Datacenter <dc>) -Principal "<domain>\<user>" -Role (Get-VIRole "ReadOnly") -Propagate:$true
```

---

## Inventory & Reporting

```powershell
# VM inventory to CSV
Get-VM | Select-Object Name, PowerState, NumCpu, MemoryGB,
  @{N="VMHost";E={$_.VMHost.Name}},
  @{N="Cluster";E={$_.VMHost.Parent.Name}},
  @{N="Datastore";E={($_ | Get-Datastore).Name -join ";"}},
  @{N="GuestOS";E={$_.Guest.OSFullName}},
  @{N="IP";E={$_.Guest.IPAddress -join ";"}} |
  Export-Csv -Path vm_inventory.csv -NoTypeInformation

# Host inventory
Get-VMHost | Select-Object Name, Version, Build, Manufacturer, Model,
  @{N="CPUModel";E={$_.ProcessorType}},
  @{N="NumCPU";E={$_.NumCpu}},
  @{N="MemGB";E={[math]::Round($_.MemoryTotalGB,0)}},
  ConnectionState, PowerState |
  Export-Csv -Path host_inventory.csv -NoTypeInformation
```

---

## vCenter Appliance (SSH)

```bash
# Connect to VCSA shell (SSH as root or administrator@vsphere.local)
service-control --status
service-control --start --all
service-control --stop vpxd

# Disk usage
df -h

# Log locations
ls /var/log/vmware/vpxd/
tail -f /var/log/vmware/vpxd/vpxd.log
tail -f /var/log/vmware/vmdird/vmdird-syslog.log

# SSO / identity
/usr/lib/vmware-vmafd/bin/vmafd-cli get-domain-name --server-name localhost
/usr/lib/vmware-vmafd/bin/vmafd-cli get-ls-location --server-name localhost

# Certificate check
/usr/lib/vmware-vmafd/bin/vecs-cli store list
/usr/lib/vmware-vmafd/bin/vecs-cli entry list --store MACHINE_SSL_CERT
```
