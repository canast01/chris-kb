# vCenter CLI Reference (PowerCLI & DCLI)

VMware PowerCLI is the official PowerShell module for managing vSphere from the command line. It connects to vCenter Server and gives you scripting access to VMs, hosts, clusters, datastores, networking, permissions, and events. Most PowerCLI commands require an active `Connect-VIServer` session.

> Install with `Install-Module VMware.PowerCLI -Scope CurrentUser`. Run `Connect-VIServer -Server <vcenter>` before any other commands.

---

## Connection & Session

Install PowerCLI, connect to vCenter, manage sessions, and handle credentials securely for scripts.

```powershell
# Install from PowerShell Gallery (run once)
Install-Module VMware.PowerCLI -Scope CurrentUser -Force

# Suppress invalid certificate warnings (lab/self-signed environments)
Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false

# Opt out of CEIP telemetry
Set-PowerCLIConfiguration -ParticipateInCeip $false -Confirm:$false

# Check and update PowerCLI
Get-Module VMware.PowerCLI -ListAvailable | Select-Object Name, Version
Update-Module VMware.PowerCLI

# Connect to vCenter
Connect-VIServer -Server <vcenter_fqdn>
Connect-VIServer -Server vcenter.corp.local -User administrator@vsphere.local -Password <password>
$cred = Get-Credential
Connect-VIServer -Server vcenter.corp.local -Credential $cred
Connect-VIServer -Server vcenter1.corp.local, vcenter2.corp.local   # multiple vCenters

# Session info
$global:DefaultVIServer
$global:DefaultVIServers    # when connected to multiple
$global:DefaultVIServer | Select-Object Name, User, Version, IsConnected, SessionId

# Disconnect
Disconnect-VIServer * -Confirm:$false
Disconnect-VIServer -Server vcenter.corp.local -Confirm:$false

# Store encrypted credential on disk (per-user, per-machine)
$cred = Get-Credential
$cred | Export-Clixml -Path "$env:USERPROFILE\.vcenter_cred.xml"
$cred = Import-Clixml -Path "$env:USERPROFILE\.vcenter_cred.xml"
Connect-VIServer -Server vcenter.corp.local -Credential $cred

# Skip proxy for on-prem vCenter
Set-PowerCLIConfiguration -ProxyPolicy NoProxy -Confirm:$false
```

---

## Hosts

List, inspect, and manage ESXi hosts via vCenter. Put hosts into maintenance mode, configure services, NTP, and syslog — all without direct SSH access to the host.

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

# Host services (SSH, vMotion agent, etc.)
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

View cluster configuration, HA/DRS settings, and host membership. Clusters group hosts to enable vMotion, DRS load balancing, and HA automated restart.

```powershell
Get-Cluster
Get-Cluster -Name <name>
Get-Cluster | Select-Object Name, HAEnabled, DrsEnabled, DrsAutomationLevel | Format-Table
Get-Cluster | Get-VMHost | Select-Object Name, State, @{N="Cluster";E={$_.Parent}} | Format-Table

# Create a new cluster
New-Cluster -Name <name> -Location (Get-Datacenter <dc>) -HAEnabled -DrsEnabled
```

---

## Virtual Machines

List, power-cycle, reconfigure, move, and clone VMs. These are the most common day-to-day operations in vCenter.

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

# VM configuration
Get-VM <name> | Get-HardDisk
Get-VM <name> | Get-NetworkAdapter
Set-VM -VM <name> -NumCpu 4 -MemoryGB 16 -Confirm:$false

# Move VM (vMotion)
Move-VM -VM <name> -Destination (Get-VMHost <host>)
Move-VM -VM <name> -Datastore (Get-Datastore <ds>)

# Clone
New-VM -Name <new_name> -VM <source_vm> -VMHost <host> -Datastore <ds>

# Guest OS info (requires VMware Tools)
Get-VM <name> | Select-Object @{N="IP";E={$_.Guest.IPAddress -join ", "}}, @{N="OS";E={$_.Guest.OSFullName}}
```

---

## Snapshots

List, create, remove, and revert VM snapshots. Monitor snapshot age and size — delta files grow over time and hurt VM performance.

```powershell
# List snapshots for a VM
Get-Snapshot -VM "<vm_name>"

# All snapshots sorted by size
Get-VM | Get-Snapshot |
    Select-Object @{N="VM";E={$_.VM.Name}}, Name, Created,
    @{N="SizeGB";E={[math]::Round($_.SizeGB, 2)}} |
    Sort-Object SizeGB -Descending

# Snapshots older than 7 days
Get-VM | Get-Snapshot |
    Where-Object { $_.Created -lt (Get-Date).AddDays(-7) } |
    Select-Object @{N="VM";E={$_.VM.Name}}, Name, Created,
    @{N="AgeDays";E={[math]::Round(((Get-Date) - $_.Created).TotalDays, 0)}}

# Create snapshots
New-Snapshot -VM "<vm_name>" -Name "pre-patch-$(Get-Date -Format yyyy-MM-dd)" `
    -Memory:$false -Quiesce:$false
New-Snapshot -VM "<vm_name>" -Name "app-consistent-$(Get-Date -Format yyyy-MM-dd)" `
    -Memory:$false -Quiesce:$true    # quiesced — requires VMware Tools

# Remove snapshots
Remove-Snapshot `
    -Snapshot (Get-Snapshot -VM "<vm_name>" -Name "<snap_name>") `
    -Confirm:$false
Remove-Snapshot -VM "<vm_name>" -RemoveChildren -Confirm:$false   # all snapshots

# Remove all old snapshots
Get-VM | Get-Snapshot |
    Where-Object { $_.Created -lt (Get-Date).AddDays(-7) } |
    Remove-Snapshot -Confirm:$false

# Revert to snapshot
Set-VM -VM "<vm_name>" `
    -Snapshot (Get-Snapshot -VM "<vm_name>" -Name "<snap_name>") `
    -Confirm:$false

# Find VMs needing consolidation
Get-VM | Where-Object { $_.ExtensionData.Runtime.ConsolidationNeeded } | Select-Object Name
(Get-VM "<vm_name>").ExtensionData.ConsolidateVMDisks_Task()
```

---

## Datastores

View datastore capacity, identify space pressure, and map datastores to VMs and hosts. Datastores below 20% free should be investigated promptly.

```powershell
# All datastores with capacity and free space
Get-Datastore
Get-Datastore | Select-Object Name, CapacityGB, FreeSpaceGB,
    @{N="UsedPct";E={[math]::Round((1 - $_.FreeSpaceGB / $_.CapacityGB) * 100, 1)}} |
    Sort-Object UsedPct -Descending

# Datastores below 20% free (alert threshold)
Get-Datastore | Where-Object { ($_.FreeSpaceGB / $_.CapacityGB) -lt 0.2 } |
    Select-Object Name, @{N="FreeGB";E={[math]::Round($_.FreeSpaceGB,1)}}, @{N="CapGB";E={[math]::Round($_.CapacityGB,1)}}

# Datastore clusters (SDRS)
Get-DatastoreCluster
Get-DatastoreCluster -Name "<name>" | Get-Datastore
Get-DatastoreCluster | Select-Object Name, CapacityGB, FreeSpaceGB,
    @{N="UsedPct";E={[math]::Round((1 - $_.FreeSpaceGB / $_.CapacityGB) * 100, 1)}}

# VMs on a specific datastore
Get-Datastore -Name "<datastore_name>" | Get-VM | Select-Object Name, PowerState

# Hosts that mount a datastore
Get-Datastore -Name "<datastore_name>" | Get-VMHost | Select-Object Name, ConnectionState

# Export datastore report
Get-Datastore | Select-Object Name,
    @{N="Type";E={$_.Type}},
    @{N="CapacityGB";E={[math]::Round($_.CapacityGB,1)}},
    @{N="FreeGB";E={[math]::Round($_.FreeSpaceGB,1)}},
    @{N="UsedPct";E={[math]::Round((1 - $_.FreeSpaceGB / $_.CapacityGB) * 100, 1)}} |
    Sort-Object UsedPct -Descending |
    Export-Csv -Path datastores.csv -NoTypeInformation
```

---

## Networks

Inspect standard vSwitches, distributed switches (VDS), port groups, VMkernel adapters, and physical NICs. Networking changes on production hosts require careful planning.

```powershell
# Standard vSwitches
Get-VirtualSwitch -VMHost <host>
Get-VirtualSwitch -VMHost <host> | Select-Object Name, NumPorts, Nic, @{N="MTU";E={$_.Mtu}}

# Standard port groups
Get-VirtualPortGroup -VMHost <host>
Get-VirtualPortGroup -VMHost <host> | Select-Object Name, VLanId, @{N="vSwitch";E={$_.VirtualSwitchName}}

# Distributed switches (VDS)
Get-VDSwitch
Get-VDSwitch | Select-Object Name, NumPorts, Version, Mtu,
    @{N="Uplinks";E={$_.ExtensionData.Config.UplinkPortPolicy.UplinkPortName -join ", "}}

# Distributed port groups
Get-VDPortgroup
Get-VDPortgroup | Select-Object Name, VlanConfiguration, NumPorts,
    @{N="VDS";E={$_.VDSwitch.Name}}
Get-VDPortgroup -Name "<portgroup_name>" | Get-VM | Select-Object Name, PowerState

# VMkernel adapters
Get-VMHostNetworkAdapter -VMHost <host> -VMKernel
Get-VMHostNetworkAdapter -VMHost <host> -VMKernel |
    Select-Object Name, IP, SubnetMask, Mac,
    VMotionEnabled, ManagementTrafficEnabled,
    FaultToleranceLoggingEnabled, VsanTrafficEnabled

# Physical NICs
Get-VMHostNetworkAdapter -VMHost <host> -Physical |
    Select-Object Name, Mac, BitRatePerSec,
    @{N="LinkUp";E={$_.ExtensionData.LinkSpeed -ne $null}}

# DNS and gateway
Get-VMHostNetwork -VMHost <host> | Select-Object HostName, DomainName, DnsAddress
(Get-VMHostNetwork -VMHost <host>).ConsoleGateway

# VLAN report across VDS
Get-VDPortgroup | Select-Object Name, @{N="VLAN";E={$_.VlanConfiguration.VlanId}} | Sort-Object VLAN
```

---

## Alarms & Events

Query triggered alarms, acknowledge false positives, and review the vCenter event log for auditing, troubleshooting, and change tracking.

```powershell
# List all alarm definitions
Get-AlarmDefinition

# VMs with active triggered alarms
Get-VM | Where-Object { $_.ExtensionData.TriggeredAlarmState.Count -gt 0 } |
    Select-Object Name, @{N="Alarms";E={$_.ExtensionData.TriggeredAlarmState.Count}}

# Hosts with active triggered alarms
Get-VMHost | Where-Object { $_.ExtensionData.TriggeredAlarmState.Count -gt 0 } |
    Select-Object Name, @{N="Alarms";E={$_.ExtensionData.TriggeredAlarmState.Count}}

# Acknowledge a triggered alarm on a VM
$vm = Get-VM "<vm_name>"
$alarmMgr = Get-View AlarmManager
$alarmMgr.AcknowledgeAlarm($vm.ExtensionData.TriggeredAlarmState[0].Alarm, $vm.ExtensionData.MoRef)

# Reset alarm to green (false positives only)
$alarmMgr.SetAlarmStatus($vm.ExtensionData.TriggeredAlarmState[0].Alarm, $vm.ExtensionData.MoRef, "green")

# Events
Get-VIEvent -MaxSamples 200 | Select-Object CreatedTime, UserName, FullFormattedMessage
Get-VIEvent -Start (Get-Date).AddHours(-24) | Select-Object CreatedTime, UserName, FullFormattedMessage

# Events for a specific VM
Get-VIEvent -Entity (Get-VM "<vm_name>") -MaxSamples 50 |
    Select-Object CreatedTime, FullFormattedMessage

# Task events (change auditing)
Get-VIEvent -MaxSamples 500 |
    Where-Object { $_.GetType().Name -eq "TaskEvent" } |
    Select-Object CreatedTime, UserName, FullFormattedMessage |
    Sort-Object CreatedTime -Descending

# Error events only
Get-VIEvent -MaxSamples 1000 | Where-Object { $_.GetType().Name -match "Error|Fault" } |
    Select-Object CreatedTime, FullFormattedMessage

# Export events to CSV
Get-VIEvent -Start (Get-Date).AddDays(-7) -MaxSamples 5000 |
    Select-Object CreatedTime, UserName, FullFormattedMessage |
    Export-Csv -Path vcenter_events_7d.csv -NoTypeInformation
```

---

## Permissions & Roles

Manage vCenter RBAC — list roles, view and assign permissions, create custom roles, and audit who has what access.

```powershell
# Roles
Get-VIRole
Get-VIRole -Name "ReadOnly" | Select-Object Name, PrivilegeList
Get-VIRole | Where-Object { $_.PrivilegeList -contains "VirtualMachine.Config.Memory" }

# Permissions
Get-VIPermission
Get-VIPermission | Where-Object { $_.Principal -eq "<domain>\<user>" }
Get-VIPermission -Entity (Get-VM "<vm_name>")
Get-VIPermission -Entity (Get-Datacenter "<dc_name>")
Get-VIPermission -Entity (Get-Cluster "<cluster_name>")

# Assign a role
New-VIPermission `
    -Entity (Get-Datacenter "<dc_name>") `
    -Principal "<domain>\<user>" `
    -Role (Get-VIRole "ReadOnly") `
    -Propagate:$true

New-VIPermission `
    -Entity (Get-VM "<vm_name>") `
    -Principal "<domain>\<group>" `
    -Role (Get-VIRole "Virtual Machine User") `
    -Propagate:$false

# Modify a permission
Set-VIPermission `
    -Permission (Get-VIPermission -Entity (Get-Datacenter "<dc>") | Where-Object { $_.Principal -eq "<domain>\<user>" }) `
    -Role (Get-VIRole "Administrator")

# Remove a permission
Get-VIPermission -Entity (Get-VM "<vm_name>") |
    Where-Object { $_.Principal -eq "<domain>\<user>" } |
    Remove-VIPermission -Confirm:$false

# Create a custom role
New-VIRole -Name "VM-PowerOps" -Privilege (
    Get-VIPrivilege -Name "Power On", "Power Off", "Reset", "Suspend"
)
New-VIPermission `
    -Entity (Get-Folder "<folder_name>") `
    -Principal "<domain>\vm-operators" `
    -Role (Get-VIRole "VM-PowerOps") `
    -Propagate:$true

# Audit: export all permissions
Get-VIPermission | Select-Object Entity, Principal, Role, IsGroup, Propagate |
    Export-Csv -Path vcenter_permissions.csv -NoTypeInformation

# Identify users with Administrator role
Get-VIPermission | Where-Object { $_.Role -eq "Admin" } |
    Select-Object Entity, Principal, Propagate
```

---

## Inventory & Reporting

Generate VM and host inventory reports, identify orphaned VMs, audit snapshot usage, and export tag assignments. Essential for capacity planning and change management.

```powershell
# Full VM inventory to CSV
Get-VM | Select-Object Name, PowerState, NumCpu, MemoryGB,
    @{N="VMHost";E={$_.VMHost.Name}},
    @{N="Cluster";E={$_.VMHost.Parent.Name}},
    @{N="Datastore";E={($_ | Get-Datastore).Name -join ";"}},
    @{N="GuestOS";E={$_.Guest.OSFullName}},
    @{N="IP";E={$_.Guest.IPAddress -join ";"}} |
    Export-Csv -Path vm_inventory.csv -NoTypeInformation

# Full host inventory to CSV
Get-VMHost | Select-Object Name, Version, Build, Manufacturer, Model,
    @{N="CPUModel";E={$_.ProcessorType}},
    @{N="NumCPU";E={$_.NumCpu}},
    @{N="MemGB";E={[math]::Round($_.MemoryTotalGB, 0)}},
    ConnectionState, PowerState |
    Export-Csv -Path host_inventory.csv -NoTypeInformation

# Cluster inventory
Get-Cluster | Select-Object Name, HAEnabled, DrsEnabled,
    @{N="Hosts";E={($_ | Get-VMHost).Count}},
    @{N="VMs";E={($_ | Get-VM).Count}}

# Orphaned / disconnected VMs
Get-VM | Where-Object { $_.ExtensionData.Summary.Runtime.ConnectionState -ne "connected" } |
    Select-Object Name, PowerState

# Powered-off VMs (orphan candidates)
Get-VM | Where-Object { $_.PowerState -eq "PoweredOff" } |
    Select-Object Name, @{N="Host";E={$_.VMHost.Name}},
    @{N="LastChange";E={$_.ExtensionData.Config.ChangeVersion}}

# All snapshots sorted by size
Get-VM | Get-Snapshot |
    Select-Object @{N="VM";E={$_.VM.Name}}, Name, Created,
    @{N="SizeGB";E={[math]::Round($_.SizeGB, 2)}} |
    Sort-Object SizeGB -Descending

# Tag assignment report
Get-VM | ForEach-Object {
    $vm = $_
    Get-TagAssignment -Entity $vm | ForEach-Object {
        [PSCustomObject]@{ VM = $vm.Name; Tag = $_.Tag.Name; Category = $_.Tag.Category.Name }
    }
} | Export-Csv -Path vm_tags.csv -NoTypeInformation

# Resource pools
Get-ResourcePool | Select-Object Name, CpuSharesLevel, MemSharesLevel,
    @{N="Cluster";E={$_.Parent.Name}}

# Folder structure
Get-Folder -Type VM | Select-Object Name, @{N="Parent";E={$_.Parent.Name}}
Get-Folder -Name "<folder_name>" | Get-VM
```

---

## vCenter Appliance (SSH)

Direct shell access to the VCSA (vCenter Server Appliance). Use these when the web UI or API is unavailable, when investigating appliance-level issues, or when checking service health.

```bash
# Connect to VCSA shell (SSH as root or administrator@vsphere.local)
# Service management
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

# Certificate inventory
/usr/lib/vmware-vmafd/bin/vecs-cli store list
/usr/lib/vmware-vmafd/bin/vecs-cli entry list --store MACHINE_SSL_CERT
```
