# Windows Server — How It Works

## Overview

Windows Server delivers infrastructure services through **Roles** (major functions) and **Features** (supporting components) installed on top of the base OS. The current supported versions are 2019, 2022, and 2025, available in Standard and Datacenter editions. All server administration uses PowerShell, WinRM remoting, or RSAT tools. Server Core (no GUI) is the recommended installation type for security and performance.

## Editions and Installation Types

| Version | Edition | Notes |
|---|---|---|
| Windows Server 2019/2022/2025 | Standard | Up to 2 Hyper-V VMs per licence |
| Windows Server 2019/2022/2025 | Datacenter | Unlimited Hyper-V VMs; Storage Spaces Direct, SDN |
| All | Server Core | No GUI; PowerShell remoting / RSAT; smaller attack surface |
| All | Desktop Experience | Full GUI; larger footprint; required for some legacy tools |

## Role Topology

```mermaid
graph TB
  WS["Windows Server 2019 / 2022"]
  WS --> AD["Active Directory DS\n(DC role)"]
  WS --> DNS_R["DNS Server"]
  WS --> FS["File Server\nSMB · DFS"]
  WS --> IIS["IIS / App Roles"]
  WS --> WSUS["Windows Update\nWSUS / Azure Update Manager"]
  WS --> SEC["Windows Defender\nFirewall · Audit Policy"]
  ADMIN(["Windows Admin"]) -->|"RDP / PowerShell"| WS
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class WS ctrl
  class AD,DNS_R,FS,IIS,WSUS,SEC mgmt
  class ADMIN host
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
| Certificate Services | ADCS | Enterprise PKI / CA |
| Failover Clustering | Failover-Clustering | HA for services |

## Critical Services

| Service | Default Start | Purpose |
|---|---|---|
| lsass.exe | Auto | Authentication, security policy |
| WinRM | Auto | PowerShell remoting, WMI |
| EventLog | Auto | Security/Application/System logs |
| Dnscache | Auto | DNS caching and resolution |
| W32tm | Auto | NTP time synchronisation |
| mpssvc | Auto | Windows Defender Firewall |
| NTDS | Auto (on DCs) | Active Directory database |

## Common Service Ports

| Service | Protocol | Port |
|---|---|---|
| SMB (file sharing) | TCP | 445 |
| RDP | TCP | 3389 |
| WinRM (HTTP / HTTPS) | TCP | 5985 / 5986 |
| DNS | TCP/UDP | 53 |
| Kerberos | TCP/UDP | 88 |
| LDAP / LDAPS | TCP | 389 / 636 |
| Global Catalog | TCP | 3268 / 3269 |
| RPC Endpoint Mapper | TCP | 135 |
| RPC Dynamic Ports | TCP | 49152–65535 |
| NTP | UDP | 123 |

## Event Log Channels

| Log | Common Event IDs | Use |
|---|---|---|
| Security | 4624 (logon), 4625 (failed), 4740 (lockout) | Auth and access auditing |
| System | 7034 (service crash), 6008 (unexpected shutdown) | OS health |
| Application | Application-specific | App-level diagnostics |
| PowerShell/Operational | 4104 (script block) | Script audit |

## Key PowerShell Commands

```powershell
# Roles and features
Get-WindowsFeature | Where-Object {$_.Installed -eq $true}
Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools

# Service health
Get-Service | Where-Object {$_.StartType -eq "Automatic" -and $_.Status -ne "Running"}

# Event logs
Get-WinEvent -FilterHashtable @{LogName='System'; Level=2; StartTime=(Get-Date).AddHours(-24)}
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4740} -MaxEvents 20

# Network
Get-NetAdapter | Select-Object Name, Status, LinkSpeed
Get-NetIPAddress | Select-Object InterfaceAlias, IPAddress, PrefixLength
Get-NetTCPConnection -State Listen | Select-Object LocalPort, @{N='Process';E={(Get-Process -Id $_.OwningProcess).Name}}

# Disk and storage
Get-Volume | Select-Object DriveLetter, FileSystem, Size, SizeRemaining, HealthStatus
Get-PhysicalDisk | Select-Object FriendlyName, MediaType, HealthStatus

# Active Directory
repadmin /replsummary
dcdiag /test:all /q
netdom query fsmo

# Windows Update
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 20

# Firewall
Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction
Get-NetFirewallRule -Direction Inbound -Enabled True | Select-Object DisplayName, Action, LocalPort
```
