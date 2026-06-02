# RASR — Install & Upgrade


<div class="kb-summary">
Install & Upgrade reference covering Prerequisites, Installation Steps, Agent Deployment at Scale, Upgrade Procedure, Version Compatibility Matrix and 1 more sections.
</div>

## Prerequisites

Before installing RASR, verify the following requirements are met on the target server.

### Hardware Requirements

| Component | Minimum | Recommended |
|---|---|---|
| Vendor | Dell PowerEdge | Dell PowerEdge 14G/15G/16G |
| CPU | Any (no RASR-specific requirement) | — |
| RAM | 4 GB (for WinPE during recovery) | — |
| Free disk space (agent) | 200 MB | — |
| Boot USB (media creation) | 4 GB USB | 8 GB USB (branded, reliable) |

### Software Requirements

| Requirement | Detail |
|---|---|
| Operating System | Windows Server 2016 / 2019 / 2022 / 2025 |
| .NET Framework | 4.7.2 or later |
| PowerShell | 5.1 or later |
| Windows ADK | Installed or available (for WinPE media creation) |
| OpenManage Agent | OMSA 10.x or later (for OME integration, optional) |
| Local Administrator | Required for installation |

### Network Requirements

| Requirement | Detail |
|---|---|
| SMB (TCP 445) | Open between protected server and backup NAS |
| iDRAC network | iDRAC must reach the NAS if using virtual media boot |
| DNS | Server must resolve NAS hostname |

---

## Installation Steps

### Method 1: Interactive Installation

1. Download the RASR installer from [Dell Support](https://www.dell.com/support) — search for **"Dell Recovery and System Restore"** for your PowerEdge model.
2. Copy the installer (`Dell_RASR_<version>_Setup.exe`) to the target server.
3. Run as Administrator:
   ```cmd
   Dell_RASR_2.5.0_Setup.exe /install /quiet /log C:\Logs\rasr-install.log
   ```
4. Accept the license agreement.
5. Choose installation path (default: `C:\Program Files\Dell\RASR\`).
6. The installer deploys:
   - RASR Agent Windows service (`DellRASR`)
   - `rasrutil.exe` CLI tool
   - RASR Console GUI
   - WinPE driver packs for the detected server model
7. Click **Finish**. No reboot required.

### Method 2: Silent/Automated Installation

```powershell
# Install silently with logging
Start-Process -FilePath ".\Dell_RASR_2.5.0_Setup.exe" `
    -ArgumentList "/install /quiet /norestart /log C:\Logs\rasr-install.log" `
    -Wait

# Verify installation
Get-Service -Name "DellRASR" | Select-Object Name, Status, StartType

# Verify CLI is accessible
& "C:\Program Files\Dell\RASR\rasrutil.exe" /?
```
```
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

The ISO can be stored on the NAS and mounted via iDRAC virtual media for remote recovery.

### Media Validation

After creation, test the media boots successfully:

1. Mount the ISO in iDRAC virtual media (see [Integrations](../../architecture/integrations/index.md)).
2. Boot the server from the virtual media.
3. Confirm the WinPE RASR wizard loads.
4. Exit without performing a restore.

Document the media creation date. Regenerate media after major Windows updates or RASR version upgrades.

---

## Agent Deployment at Scale

For deploying RASR across many servers, use your configuration management tooling.

### PowerShell / DSC (example)

```powershell
# Deploy RASR installer from a central share
$installer = "\\deploy\software\dell-rasr\Dell_RASR_2.5.0_Setup.exe"
$args      = "/install /quiet /norestart /log C:\Logs\rasr-install.log"

Start-Process -FilePath $installer -ArgumentList $args -Wait

# Configure and start service
Set-Service  -Name "DellRASR" -StartupType Automatic
Start-Service -Name "DellRASR"
```

### SCCM / Endpoint Manager

Create an application deployment:

- **Detection method:** File exists: `C:\Program Files\Dell\RASR\rasrutil.exe`
- **Install command:** `Dell_RASR_2.5.0_Setup.exe /install /quiet /norestart`
- **Uninstall command:** `Dell_RASR_2.5.0_Setup.exe /uninstall /quiet`
- **Deployment type:** Required, for server device collection

---

## Upgrade Procedure

### In-Place Upgrade

RASR supports in-place upgrade without uninstalling the existing version. The existing configuration and scheduled tasks are preserved.

```cmd
:: Run new installer — it detects existing version and upgrades
Dell_RASR_2.6.0_Setup.exe /install /quiet /norestart /log C:\Logs\rasr-upgrade.log
```

**Post-upgrade:**

```powershell
# Verify new version
(Get-Item "C:\Program Files\Dell\RASR\rasrutil.exe").VersionInfo.FileVersion

# Restart service to load new binaries
Restart-Service -Name "DellRASR"

# Confirm service is running
Get-Service -Name "DellRASR"
```

### Upgrade Boot Media After Upgrade

Boot media must be regenerated after each RASR version upgrade — the WinPE image in the installer is version-specific.

```cmd
:: Regenerate ISO after upgrade
"C:\Program Files\Dell\RASR\rasrutil.exe" /createmedia /dest \\nas01\rasr-media\RASR_SERVER01_WinSrv2022_v2.6.iso
```

Update the ISO path in iDRAC virtual media bookmarks and in your DR runbooks.

---

## Version Compatibility Matrix

| RASR Version | Windows Server 2016 | Windows Server 2019 | Windows Server 2022 | Windows Server 2025 | Dell OpenManage |
|---|---|---|---|---|---|
| 2.3.x | Yes | Yes | No | No | OMSA 9.x+ |
| 2.4.x | Yes | Yes | Yes | No | OMSA 10.x+ |
| 2.5.x | Yes | Yes | Yes | Preview | OMSA 10.x+ |
| 2.6.x | Yes | Yes | Yes | Yes | OMSA 11.x+ |

### PowerEdge Generation Support

| RASR Version | 13G (R730/R630) | 14G (R740/R640) | 15G (R750/R650) | 16G (R760/R660) |
|---|---|---|---|---|
| 2.3.x | Yes | Yes | No | No |
| 2.4.x | Limited | Yes | Yes | No |
| 2.5.x | No | Yes | Yes | Preview |
| 2.6.x | No | Yes | Yes | Yes |

For 13G servers, RASR 2.3.x is the final supported version. Consider migrating workloads to current-generation hardware or using Windows Server Backup as an alternative.

---

## Uninstall

```cmd
:: Silent uninstall
Dell_RASR_2.5.0_Setup.exe /uninstall /quiet /norestart /log C:\Logs\rasr-uninstall.log
```

Or via Windows **Add/Remove Programs** → **Dell Recovery and System Restore** → **Uninstall**.

The uninstaller does NOT remove existing backup images from the network share. Remove those manually if no longer needed.
