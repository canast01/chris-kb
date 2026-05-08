# Windows Server — Components

Core components, services, ports, dependencies, and internals.

## Core Windows Server Roles and Features

Windows Server functionality is delivered through **Roles** (major server functions) and **Features** (supporting components). Both are managed via Server Manager or PowerShell.

```powershell
# List installed roles and features
Get-WindowsFeature | Where-Object {$_.Installed -eq $true} | Select-Object Name, DisplayName

# List available roles
Get-WindowsFeature | Where-Object {$_.FeatureType -eq "Role"} | Select-Object Name, DisplayName, Installed

# Install a role
Install-WindowsFeature -Name "Web-Server" -IncludeManagementTools

# Remove a role
Remove-WindowsFeature -Name "Telnet-Client"
```

## Key Server Roles

| Role | Feature Name | Purpose |
|---|---|---|
| Active Directory Domain Services | AD-Domain-Services | Directory services, authentication |
| DNS Server | DNS | Name resolution |
| DHCP Server | DHCP | IP address assignment |
| File Services | FS-FileServer | SMB file sharing |
| Hyper-V | Hyper-V | Hardware virtualisation |
| IIS Web Server | Web-Server | HTTP/HTTPS hosting |
| Remote Desktop Services | RDS-RD-Server | Remote desktop sessions |
| Network Policy Server | NPAS | RADIUS, NAP |
| Print Services | Print-Server | Print spooling |
| Certificate Services | ADCS | Enterprise PKI / CA |
| Windows Deployment Services | WDS | OS deployment over network |
| Failover Clustering | Failover-Clustering | High availability for services |

## Critical System Services

| Service | Display Name | Default Start | Purpose |
|---|---|---|---|
| lsass.exe | Local Security Authority Process | Auto | Authentication, security policy |
| svchost.exe | Service Host | Auto | Container for many services |
| wininit.exe | Windows Start-Up Application | Auto | Session 0 initialisation |
| services.exe | Services Control Manager | Auto | Starts/stops Windows services |
| winlogon.exe | Windows Logon | Auto | Interactive logon |
| smss.exe | Session Manager | Auto | Session initialisation |
| csrss.exe | Client Server Runtime Process | Auto | Win32 subsystem |
| spoolsv.exe | Print Spooler | Auto | Print job management |
| Dnscache | DNS Client | Auto | DNS caching and resolution |
| W32tm | Windows Time | Auto | NTP time synchronisation |
| WinRM | Windows Remote Management | Auto (on Server) | PowerShell remoting, WMI |
| EventLog | Windows Event Log | Auto | Security/Application/System logs |
| mpssvc | Windows Defender Firewall | Auto | Host-based firewall |

```powershell
# Check status of critical services
$criticalServices = @("lsass","EventLog","Dnscache","W32tm","WinRM","mpssvc","wuauserv")
foreach ($svc in $criticalServices) {
    Get-Service -Name $svc -ErrorAction SilentlyContinue |
      Select-Object Name, DisplayName, Status, StartType
}

# Find services that are set to Auto but not running
Get-Service | Where-Object {$_.StartType -eq "Automatic" -and $_.Status -ne "Running"} |
  Select-Object Name, DisplayName, Status
```

## Windows Registry — Key Locations

| Hive | Path | Content |
|---|---|---|
| HKLM\SYSTEM | CurrentControlSet\Services | Service configurations, driver settings |
| HKLM\SOFTWARE | Microsoft\Windows NT\CurrentVersion | OS version, installed software |
| HKLM\SECURITY | — | LSA secrets, security policy (restricted) |
| HKLM\SAM | — | Local account database (restricted) |
| HKCU | — | Per-user settings for the current user |
| HKU | — | Per-user settings for all loaded profiles |

```powershell
# Query OS version from registry
(Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion").ProductName
(Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion").CurrentBuildNumber

# Find installed software
Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*" |
  Select-Object DisplayName, DisplayVersion, Publisher | Sort-Object DisplayName
```

## Windows Event Log

Event logs are the primary diagnostic and audit source on Windows Server.

| Log | Description | Common Event IDs |
|---|---|---|
| Security | Authentication, access control, policy changes | 4624 (logon), 4625 (failed), 4740 (lockout) |
| System | OS-level events, driver failures, service starts | 7034 (service crashed), 6008 (unexpected shutdown) |
| Application | Events from applications and .NET runtime | Application-specific |
| Setup | Role/feature installs, updates | Install events |
| Forwarded Events | Events forwarded from other machines | Central collection |
| Microsoft-Windows-PowerShell/Operational | PowerShell execution | 4104 (script block) |

```powershell
# View recent Security events
Get-WinEvent -LogName Security -MaxEvents 50 |
  Select-Object TimeCreated, Id, LevelDisplayName, Message | Format-Table -Wrap

# View System errors from the last 24 hours
Get-WinEvent -FilterHashtable @{
    LogName = 'System'
    Level   = 2   # Error
    StartTime = (Get-Date).AddHours(-24)
} | Select-Object TimeCreated, Id, ProviderName, Message

# Filter by specific event ID
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4740} -MaxEvents 20

# Export events for analysis
Get-WinEvent -LogName Security -MaxEvents 1000 |
  Export-Csv C:\temp\security-events.csv -NoTypeInformation
```

## Networking Components

### TCP/IP Stack

```powershell
# View network adapters and IP configuration
Get-NetAdapter | Select-Object Name, Status, LinkSpeed, MACAddress
Get-NetIPAddress | Select-Object InterfaceAlias, AddressFamily, IPAddress, PrefixLength

# View routing table
Get-NetRoute | Where-Object {$_.RouteMetric -lt 256} |
  Select-Object DestinationPrefix, NextHop, InterfaceAlias, RouteMetric

# Active TCP connections
Get-NetTCPConnection -State Established |
  Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, OwningProcess |
  Sort-Object LocalPort

# DNS configuration
Get-DnsClientServerAddress | Select-Object InterfaceAlias, ServerAddresses
```

### Windows Firewall

```powershell
# View firewall profiles
Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction, DefaultOutboundAction

# View inbound rules that are enabled
Get-NetFirewallRule -Direction Inbound -Enabled True |
  Select-Object DisplayName, Action, Protocol, LocalPort | Format-Table -AutoSize

# View what is listening (process + port)
Get-NetTCPConnection -State Listen |
  Select-Object LocalAddress, LocalPort,
    @{N='Process';E={(Get-Process -Id $_.OwningProcess).Name}} |
  Sort-Object LocalPort
```

## Common Service Ports

| Service | Protocol | Port(s) |
|---|---|---|
| SMB (file sharing) | TCP | 445 |
| RDP | TCP | 3389 |
| WinRM (PowerShell Remoting) | TCP | 5985 (HTTP), 5986 (HTTPS) |
| DNS | TCP/UDP | 53 |
| DHCP | UDP | 67 (server), 68 (client) |
| Kerberos | TCP/UDP | 88 |
| LDAP | TCP/UDP | 389 |
| LDAPS | TCP | 636 |
| Global Catalog | TCP | 3268, 3269 (SSL) |
| RPC Endpoint Mapper | TCP | 135 |
| RPC Dynamic Ports | TCP | 49152–65535 |
| HTTP | TCP | 80 |
| HTTPS | TCP | 443 |
| NTP | UDP | 123 |
| SNMP | UDP | 161 |

## Windows Update Components

```powershell
# Check Windows Update status
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 20

# List pending updates (requires PSWindowsUpdate module)
# Install-Module PSWindowsUpdate -Force
Get-WindowsUpdate

# Install all available updates
Install-WindowsUpdate -AcceptAll -AutoReboot

# WSUS — check server assignment
(Get-ItemProperty "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate").WUServer
```

## Active Directory Domain Services Components

When the AD-Domain-Services role is installed, these key components are present:

| Component | Description |
|---|---|
| NTDS.dit | AD database file — `C:\Windows\NTDS\ntds.dit` |
| SYSVOL | Shared folder replicating GPOs and scripts — `C:\Windows\SYSVOL` |
| KDC (Key Distribution Center) | Kerberos ticket-granting service (runs in lsass.exe) |
| NetLogon | Domain authentication and DC locator |
| DFSR | DFS Replication — replicates SYSVOL between DCs |
| Active Directory Sites | Defines replication topology |

```powershell
# Check NTDS service (AD DS)
Get-Service NTDS | Select-Object Status, StartType

# Check SYSVOL sharing
Get-SmbShare -Name SYSVOL
Get-SmbShare -Name NETLOGON

# Check DC replication health
repadmin /showrepl
repadmin /replsummary

# Check FSMO roles
netdom query fsmo

# Test AD health
dcdiag /test:all /q   # /q = quiet (only shows failures)
```

## Storage Components

```powershell
# List physical disks
Get-PhysicalDisk | Select-Object FriendlyName, MediaType, Size, HealthStatus, OperationalStatus

# List volumes
Get-Volume | Select-Object DriveLetter, FileSystemLabel, FileSystem, Size, SizeRemaining, HealthStatus

# List storage pools (if using Storage Spaces)
Get-StoragePool | Select-Object FriendlyName, HealthStatus, OperationalStatus, Size

# List virtual disks (Storage Spaces)
Get-VirtualDisk | Select-Object FriendlyName, HealthStatus, ResiliencySettingName, Size

# Disk I/O performance counters
Get-Counter "\PhysicalDisk(*)\Disk Reads/sec","\PhysicalDisk(*)\Disk Writes/sec" -SampleInterval 5 -MaxSamples 3
```

## Hyper-V Components

When Hyper-V is installed:

| Component | Description |
|---|---|
| Hypervisor | vmms.exe — VM management service |
| Virtual Switch | Hyper-V virtual switch connecting VMs to physical network |
| vNIC | Virtual NIC inside VMs |
| VHD/VHDX | Virtual hard disk files |
| Snapshot (Checkpoint) | Point-in-time VM state and disk capture |
| Integration Services | vmicheartbeat, vmicvss, etc. — guest-host communication |

```powershell
# List VMs and their state
Get-VM | Select-Object Name, State, CPUUsage, MemoryAssigned, Uptime

# Check Hyper-V services
Get-Service vmms, vmicheartbeat, vmicvss | Select-Object Name, Status

# List virtual switches
Get-VMSwitch | Select-Object Name, SwitchType, NetAdapterInterfaceDescription
```

## Component Health Quick Check

```powershell
# Run all core checks
Write-Host "=== Services ===" -ForegroundColor Cyan
Get-Service | Where-Object {$_.StartType -eq "Automatic" -and $_.Status -ne "Running"} |
  Select-Object Name, DisplayName

Write-Host "`n=== Disk Health ===" -ForegroundColor Cyan
Get-Volume | Where-Object {$_.HealthStatus -ne "Healthy"} | Select-Object DriveLetter, HealthStatus

Write-Host "`n=== Recent System Errors ===" -ForegroundColor Cyan
Get-WinEvent -FilterHashtable @{LogName='System';Level=2;StartTime=(Get-Date).AddHours(-4)} `
  -MaxEvents 10 -ErrorAction SilentlyContinue | Select-Object TimeCreated, ProviderName, Message

Write-Host "`n=== Firewall Profiles ===" -ForegroundColor Cyan
Get-NetFirewallProfile | Select-Object Name, Enabled

Write-Host "`n=== Windows Update (last 5) ===" -ForegroundColor Cyan
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 5 |
  Select-Object HotFixID, Description, InstalledOn
```
