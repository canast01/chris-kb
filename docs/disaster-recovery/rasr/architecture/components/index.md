# RASR — Components

> Part of the [RASR Architecture](../) reference.

---

RASR (Recovery and System Restore) consists of five components. Each has specific dependencies and failure modes worth understanding before a recovery operation.

## Component Overview

```
Protected Server
├── RASR Agent (RASRAgent Windows service)
├── RASR Console (GUI in Windows)
└── Captured Image → Network Recovery Share (SMB)

Recovery Media (USB / iDRAC virtual ISO)
└── WinPE boot environment
      └── RASR Recovery Engine
```

## RASR Agent

The RASR Agent (`RASRAgent`) is a Windows service that runs on the protected server and orchestrates image capture.

| Property | Detail |
|---|---|
| Service name | `RASRAgent` |
| Display name | Dell Recovery and System Restore Agent |
| Startup type | Automatic (Delayed Start) |
| Log location | `C:\Program Files\Dell\RASR\Logs\` |
| Config location | `C:\Program Files\Dell\RASR\Config\rasr.ini` |

```powershell
# Check RASR Agent status
Get-Service -Name RASRAgent

# Restart agent
Restart-Service -Name RASRAgent

# Check agent version
Get-ItemProperty "HKLM:\SOFTWARE\Dell\RASR" | Select-Object Version, InstallDate

# View recent agent log
Get-Content "C:\Program Files\Dell\RASR\Logs\RASRAgent.log" -Tail 50
```

## RASR Console

The RASR Console is the GUI interface launched from within a running Windows session. It provides:

- **Backup** — initiate a new system image capture.
- **Schedule** — configure automated image capture schedule.
- **Media** — create bootable RASR USB media or download the boot ISO.
- **Recovery** — initiate recovery from within a running OS (for non-catastrophic failures).

```
Start → Dell OpenManage → Recovery and System Restore → Launch Console
```

The Console is a thin client — all operations are executed by the RASR Agent service.

## Recovery Image

The recovery image is a sector-level copy of the system volume, stored in the proprietary RASR format.

| Property | Detail |
|---|---|
| Format | `.wim` or RASR proprietary block image |
| Contents | OS volume, boot partition, EFI partition, system state |
| Data volumes | Not included by default; scope is OS + system state only |
| Compression | Hardware-dependent; typically 40–60% compression on OS volumes |
| Storage location | Network SMB share (default) or local USB |

```
Typical image size:
  Fresh Windows Server 2022 OS: ~12 GB compressed
  Fully patched + apps installed: 20–40 GB compressed
```

### Network Recovery Share Requirements

| Requirement | Detail |
|---|---|
| Protocol | SMB 2.0 or later |
| Authentication | Domain account or local account on the share host |
| Permissions | Read/write for the RASR service account; read for recovery operations |
| Path example | `\\nas01\rasr-images\server01\` |
| Minimum free space | 2× the compressed image size (for image + staging) |

```powershell
# Test connectivity to the recovery share from the protected server
Test-Path "\\nas01\rasr-images\server01"

# Check available space on the share
(Get-PSDrive -Name Z -ErrorAction SilentlyContinue) | Select-Object Free
# or after mapping:
net use Z: \\nas01\rasr-images /user:domain\rasr-svc
(Get-PSDrive Z).Free / 1GB
```

## RASR Recovery Media (WinPE)

The RASR boot media is a Windows Preinstallation Environment (WinPE) image that contains:

- **RASR Recovery Engine** — the wizard-based restore interface.
- **Network drivers** — Broadcom, Intel, Mellanox drivers for Dell PowerEdge generations 14G, 15G, 16G.
- **Storage drivers** — PERC H730/H740/H755, HBA335/HBA355 drivers.
- **Recovery tools** — `diskpart`, `net use`, `notepad`, `regedit`, `wpeutil`.

| Media type | Use case | Creation method |
|---|---|---|
| Bootable USB | Physical recovery with USB access | RASR Console → Create Media → USB |
| ISO file | iDRAC virtual media (remote recovery) | RASR Console → Create Media → ISO |
| Network boot (PXE) | Large-scale recovery via PXE infrastructure | Manual WinPE customisation required |

```
Boot order for recovery:
  1. Attach ISO via iDRAC → Virtual Media → Map CD/DVD
  2. iDRAC → Power → Boot Once → Virtual CD/DVD
  3. WinPE loads → RASR wizard starts automatically
```

## OpenManage Integration

RASR Agent status is surfaced in the **Dell OpenManage Server Administrator (OMSA)** dashboard:

```
OMSA → System → Recovery → RASR Status
  - Last backup: <timestamp>
  - Last backup result: Success / Failed
  - Schedule: <schedule>
  - Image location: <path>
```

OMSA alerts can be configured to notify on backup failure via SNMP trap or email.

## Component Health Check

```powershell
# Run as part of regular health check cadence
$results = @{
    AgentStatus     = (Get-Service RASRAgent).Status
    LastBackup      = (Get-ItemProperty "HKLM:\SOFTWARE\Dell\RASR").LastBackupTime
    LastBackupResult = (Get-ItemProperty "HKLM:\SOFTWARE\Dell\RASR").LastBackupResult
    ImageShareReach = Test-Path "\\nas01\rasr-images\$(hostname)"
    MediaPresent    = Test-Path "D:\rasr-media.iso"
}
$results | Format-List
```

| Expected result | Indicates |
|---|---|
| Agent: Running | Service operational |
| Last backup: < 24h ago | Backup schedule running |
| Last result: Success | Image capture succeeded |
| Share reachable: True | Network path to image store is available |
