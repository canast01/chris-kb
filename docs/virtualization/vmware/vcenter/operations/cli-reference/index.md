# vCenter — CLI Reference (PowerCLI & DCLI)

```
vCenter CLI Interfaces
════════════════════════════════════════════════════════

  Management Workstation                    VCSA (SSH)
  ┌─────────────────────────────┐           ┌──────────────────────────┐
  │                             │           │                          │
  │  PowerCLI (PowerShell)      │  :443     │  service-control         │
  │  ┌──────────────────────┐   │──────────▶│   --status / --restart   │
  │  │ Connect-VIServer      │   │           │                          │
  │  │ Get-VM / Get-VMHost   │   │           │  vecs-cli                │
  │  │ Get-Cluster           │   │           │   (certificate stores)   │
  │  │ Get-Datastore         │   │           │                          │
  │  │ Get-VIEvent           │   │           │  vmafd-cli               │
  │  │ New-VIPermission      │   │           │   (SSO / domain info)    │
  │  └──────────────────────┘   │           │                          │
  │                             │           │  dcli                    │
  │  REST API (curl/python)     │  :443     │   (vSphere Automation)   │
  │  ┌──────────────────────┐   │──────────▶│                          │
  │  │ POST /api/session     │   │           │  certificate-manager     │
  │  │ GET  /api/vcenter/vm  │   │           │   (cert replace/renew)   │
  │  │ GET  /api/vcenter/host│   │           │                          │
  │  │ GET  /health/system   │   │           │  df -h / top / ss -tlnp  │
  │  └──────────────────────┘   │           │                          │
  └─────────────────────────────┘           └──────────────────────────┘
```

VMware PowerCLI is the official PowerShell module for managing vSphere from the command line. It connects to vCenter Server and gives you scripting access to VMs, hosts, clusters, datastores, networking, permissions, and events. Most PowerCLI commands require an active `Connect-VIServer` session.

> Install with `Install-Module VMware.PowerCLI -Scope CurrentUser`. Run `Connect-VIServer -Server <vcenter>` before any other commands.

---

## Connection & Session

```powershell
# Install from PowerShell Gallery (run once)
Install-Module VMware.PowerCLI -Scope CurrentUser -Force

# Suppress invalid certificate warnings (lab/self-signed environments)
Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false

# Opt out of CEIP telemetry
Set-PowerCLIConfiguration -ParticipateInCeip $false -Confirm:$false

# Connect to vCenter
Connect-VIServer -Server <vcenter_fqdn>
Connect-VIServer -Server vcenter.corp.local -User administrator@vsphere.local -Password <password>
$cred = Get-Credential
Connect-VIServer -Server vcenter.corp.local -Credential $cred
Connect-VIServer -Server vcenter1.corp.local, vcenter2.corp.local   # multiple vCenters

# Session info
$global:DefaultVIServer
$global:DefaultVIServers    # when connected to multiple

# Disconnect
Disconnect-VIServer * -Confirm:$false
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

# Create a new cluster
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

# VM configuration
Get-VM <name> | Get-HardDisk
Get-VM <name> | Get-NetworkAdapter
Set-VM -VM <name> -NumCpu 4 -MemoryGB 16 -Confirm:$false

# Move VM (vMotion)
Move-VM -VM <name> -Destination (Get-VMHost <host>)
Move-VM -VM <name> -Datastore (Get-Datastore <ds>)

# Clone
New-VM -Name <new_name> -VM <source_vm> -VMHost <host> -Datastore <ds>
```

---

## Snapshots

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

# Remove snapshots
Remove-Snapshot `
    -Snapshot (Get-Snapshot -VM "<vm_name>" -Name "<snap_name>") `
    -Confirm:$false
Remove-Snapshot -VM "<vm_name>" -RemoveChildren -Confirm:$false   # all snapshots

# Revert to snapshot
Set-VM -VM "<vm_name>" `
    -Snapshot (Get-Snapshot -VM "<vm_name>" -Name "<snap_name>") `
    -Confirm:$false
```

---

## Datastores

```powershell
# All datastores with capacity and free space
Get-Datastore | Select-Object Name, CapacityGB, FreeSpaceGB,
    @{N="UsedPct";E={[math]::Round((1 - $_.FreeSpaceGB / $_.CapacityGB) * 100, 1)}} |
    Sort-Object UsedPct -Descending

# Datastores below 20% free
Get-Datastore | Where-Object { ($_.FreeSpaceGB / $_.CapacityGB) -lt 0.2 } |
    Select-Object Name, @{N="FreeGB";E={[math]::Round($_.FreeSpaceGB,1)}}

# VMs on a specific datastore
Get-Datastore -Name "<datastore_name>" | Get-VM | Select-Object Name, PowerState

# Export datastore report
Get-Datastore | Select-Object Name,
    @{N="CapacityGB";E={[math]::Round($_.CapacityGB,1)}},
    @{N="FreeGB";E={[math]::Round($_.FreeSpaceGB,1)}},
    @{N="UsedPct";E={[math]::Round((1 - $_.FreeSpaceGB / $_.CapacityGB) * 100, 1)}} |
    Sort-Object UsedPct -Descending |
    Export-Csv -Path datastores.csv -NoTypeInformation
```

---

## Alarms & Events

```powershell
# List all alarm definitions
Get-AlarmDefinition

# VMs with active triggered alarms
Get-VM | Where-Object { $_.ExtensionData.TriggeredAlarmState.Count -gt 0 } |
    Select-Object Name, @{N="Alarms";E={$_.ExtensionData.TriggeredAlarmState.Count}}

# Events
Get-VIEvent -MaxSamples 200 | Select-Object CreatedTime, UserName, FullFormattedMessage
Get-VIEvent -Start (Get-Date).AddHours(-24) | Select-Object CreatedTime, UserName, FullFormattedMessage

# Events for a specific VM
Get-VIEvent -Entity (Get-VM "<vm_name>") -MaxSamples 50 |
    Select-Object CreatedTime, FullFormattedMessage

# Error events only
Get-VIEvent -MaxSamples 1000 | Where-Object { $_.GetType().Name -match "Error|Fault" } |
    Select-Object CreatedTime, FullFormattedMessage
```

---

## Permissions & Roles

```powershell
# Roles
Get-VIRole
Get-VIRole -Name "ReadOnly" | Select-Object Name, PrivilegeList

# Permissions
Get-VIPermission
Get-VIPermission | Where-Object { $_.Principal -eq "<domain>\<user>" }

# Assign a role
New-VIPermission `
    -Entity (Get-Datacenter "<dc_name>") `
    -Principal "<domain>\<user>" `
    -Role (Get-VIRole "ReadOnly") `
    -Propagate:$true

# Audit: export all permissions
Get-VIPermission | Select-Object Entity, Principal, Role, IsGroup, Propagate |
    Export-Csv -Path vcenter_permissions.csv -NoTypeInformation

# Identify users with Administrator role
Get-VIPermission | Where-Object { $_.Role -eq "Admin" } |
    Select-Object Entity, Principal, Propagate
```

---

## vCenter Appliance (SSH)

```bash
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
