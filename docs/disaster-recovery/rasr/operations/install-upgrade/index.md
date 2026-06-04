# RASR — Install & Upgrade

```powershell
# Install silently with logging
Start-Process -FilePath ".\Dell_RASR_2.5.0_Setup.exe" `
    -ArgumentList "/install /quiet /norestart /log C:\Logs\rasr-install.log" `
    -Wait

# Verify installation
Get-Service -Name "DellRASR" | Select-Object Name, Status, StartType

# Verify CLI is accessible
& "C:\Program Files\Dell\RASR\rasrutil.exe" /?
```text
┌────────────────────────────────────── RASR — Install & Upgrade ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               RASR — Installation Prerequisites                               │   │
│   │             OS: supported Linux or Windows Server (see vendor compatibility matrix)           │   │
│   │          Network: 443 (PPDM REST API) · 2049 (NFS vault) — ensure firewall allows these       │   │
│   │       Auth: Vault operator role; 2-person integrity for unlock; AD integration for PPDM UI    │   │
│   │          Storage: Airgap switch · Vault PowerStore/DD appliance · Clean-room ESXi hosts       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                        Install Sequence                                       │   │
│   │                  1  Deploy control plane component and configure network access               │   │
│   │                          2  Configure storage and network connectivity                        │   │
│   │                        3  Install agent/proxy/splitter on protected hosts                     │   │
│   │                      4  Register sources and configure protection policies                    │   │
│   │                        5  Run first job; verify completion; test restore                      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                        Upgrade Sequence                                       │   │
│   │                 1  Review release notes and compatibility matrix before upgrade               │   │
│   │                   2  Snapshot or backup the control plane VM before upgrading                 │   │
│   │                  3  Upgrade control plane first, then proxies/agents/appliances               │   │
│   │                       4  Validate jobs resume automatically after upgrade                     │   │
│   │                        5  Document version change and update CMDB record                      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts     │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest       │
│  Vault         = isolated, air-gapped storage appliance receiving periodic replication copies         │
│  Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies      │
│  CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures        │
│  PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery      │
│  Air Gap       = physical or logical network isolation preventing attacker lateral movement to        │
│  Delta Set     = incremental changed blocks replicated from production to vault each cycle            │
│  Clean Room    = isolated recovery environment: separate vCenter, network, and workstations           │
│  Recovery Point= specific vault snapshot timestamp from which clean recovery is performed             │
│  Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac       │
│  Journal       = write-order-consistent journal on vault enabling point-in-time recovery              │
│  Scan Report   = CyberSense output: clean/suspect classification per file and block                   │
│  Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept                    │
│  RTO           = Recovery Time Objective; time from failover decision to restored service             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```powershell
# Deploy RASR installer from a central share
$installer = "\\deploy\software\dell-rasr\Dell_RASR_2.5.0_Setup.exe"
$args      = "/install /quiet /norestart /log C:\Logs\rasr-install.log"

Start-Process -FilePath $installer -ArgumentList $args -Wait

# Configure and start service
Set-Service  -Name "DellRASR" -StartupType Automatic
Start-Service -Name "DellRASR"
```
```cmd
:: Run new installer — it detects existing version and upgrades
Dell_RASR_2.6.0_Setup.exe /install /quiet /norestart /log C:\Logs\rasr-upgrade.log
```
```powershell
# Verify new version
(Get-Item "C:\Program Files\Dell\RASR\rasrutil.exe").VersionInfo.FileVersion

# Restart service to load new binaries
Restart-Service -Name "DellRASR"

# Confirm service is running
Get-Service -Name "DellRASR"
```
```cmd
:: Regenerate ISO after upgrade
"C:\Program Files\Dell\RASR\rasrutil.exe" /createmedia /dest \\nas01\rasr-media\RASR_SERVER01_WinSrv2022_v2.6.iso
```
```cmd
:: Silent uninstall
Dell_RASR_2.5.0_Setup.exe /uninstall /quiet /norestart /log C:\Logs\rasr-uninstall.log
```
