# RASR — CLI Reference


<div class="kb-summary">
CLI Reference reference covering rasrutil.exe — Primary Command-Line Interface, Exit Codes, WinPE Shell Commands, Scripted Backup Creation, Image Management Commands Reference.
</div>

## rasrutil.exe — Primary Command-Line Interface

`rasrutil.exe` is the main command-line tool for RASR operations on a running Windows Server. It is located at:

```text
C:\Program Files\Dell\RASR\rasrutil.exe
```
```text
┌──────────────────────────────────────── RASR — CLI Reference ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                    RASR — Command Reference                                   │   │
│   │           Use these commands for routine operations, scripting, and troubleshooting           │   │
│   │                                        cr_vault_cli sync                                      │   │
│   │                                       cr_vault_cli status                                     │   │
│   │                                         cybersense scan                                       │   │
│   │                                       vault lock / unlock                                     │   │
│   │                                         ppdm recover vm                                       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Ports: 443 (PPDM REST API) · 2049 (NFS vault) · 9080 (CyberSense)                                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                       Command Categories                                      │   │
│   │                  Status / Query  — check current state, list jobs, show config                │   │
│   │                  Operations      — start, stop, failover, restore, sync, expire               │   │
│   │                Configuration   — add/modify policies, schedules, storage targets              │   │
│   │               Diagnostics     — collect logs, run health checks, test connectivity            │   │
│   │                  Scripting       — REST API or CLI for automation and reporting               │   │
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

---

### /restore — Restore System Image

```text
rasrutil.exe /restore /source <image_path> [options]
```

| Parameter | Description |
|---|---|
| `/source <path>` | Full path to the `.rasr` image file |
| `/target <disk#>` | Target disk number (use `diskpart list disk` to identify) |
| `/user <user>` | Credential for network share (if source is UNC) |
| `/pass <pass>` | Password for network share |
| `/noreboot` | Do not reboot after restore completes |

**Example:**

```cmd
rasrutil.exe /restore /source \\nas01\rasr-images\SERVER01\SERVER01_20260501.rasr ^
  /target 0 /user CORP\svc-rasr /pass S3cr3t!
```

---

### /listimages — List Available Images

```text
rasrutil.exe /listimages /source <path> [/user <user>] [/pass <pass>]
```

Lists all RASR images in the specified directory.

```cmd
rasrutil.exe /listimages /source \\nas01\rasr-images\SERVER01 ^
  /user CORP\svc-rasr /pass S3cr3t!
```

**Output:**

```text
Image File               Created              Size        Description
SERVER01_20260501.rasr   2026-05-01 02:14     48.3 GB     Weekly full
SERVER01_20260408.rasr   2026-04-08 02:11     47.1 GB     Weekly full
```

---

### /verify — Verify Image Integrity

```text
rasrutil.exe /verify /source <image_path> [/user <user>] [/pass <pass>]
```

Verifies the checksum and structural integrity of an image file without performing a restore.

```cmd
rasrutil.exe /verify /source \\nas01\rasr-images\SERVER01\SERVER01_20260501.rasr ^
  /user CORP\svc-rasr /pass S3cr3t!
```

Returns exit code `0` on success, non-zero on failure.

---

### /deleteimage — Remove an Image

```text
rasrutil.exe /deleteimage /source <image_path> [/user <user>] [/pass <pass>]
```

```cmd
rasrutil.exe /deleteimage /source \\nas01\rasr-images\SERVER01\SERVER01_20260201.rasr ^
  /user CORP\svc-rasr /pass S3cr3t!
```

---

### /createmedia — Create RASR Boot Media

```text
rasrutil.exe /createmedia /dest <drive_letter|iso_path>
```

Creates a bootable RASR USB drive or ISO file.

```cmd
:: Create bootable USB
rasrutil.exe /createmedia /dest F:

:: Create ISO file
rasrutil.exe /createmedia /dest C:\RASR\RASR_WinSrv2022.iso
```

---

## Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | General error |
| 2 | Invalid parameters |
| 3 | Destination not accessible |
| 4 | Insufficient disk space |
| 5 | Image file corrupt (verify failure) |
| 6 | Restore target disk not found |
| 10 | Authentication failure |

---

## WinPE Shell Commands

When booted into the RASR WinPE recovery environment, the following commands are available. All standard WinPE commands apply plus the RASR-specific tools.

### Network and Share Access

```cmd
:: Configure network interface (if DHCP not available)
netsh interface ip set address "Ethernet" static 10.0.1.100 255.255.255.0 10.0.1.1
netsh interface ip set dns "Ethernet" static 10.0.1.10

:: Map network share for image access
net use Z: \\nas01.example.com\rasr-images /user:CORP\svc-rasr P@ssw0rd!

:: Verify connectivity
ping nas01.example.com
dir Z:\
```

### Disk Operations

```cmd
:: List disks
diskpart
  list disk
  exit

:: Identify partitions on target disk
diskpart
  select disk 0
  list partition
  exit
```

### Launch RASR Wizard Manually

```cmd
:: If wizard did not auto-start
X:\Dell\RASR\rasrwizard.exe

:: Or run CLI restore from WinPE
X:\Dell\RASR\rasrutil.exe /restore /source Z:\SERVER01\SERVER01_20260501.rasr /target 0
```

### WinPE Utility Commands

```cmd
:: Test network reachability
ping -t 10.0.1.10

:: Check IP configuration
ipconfig /all

:: View event log (limited in WinPE)
wevtutil qe System /c:20 /f:text

:: Edit files (notepad available in RASR WinPE)
notepad X:\Dell\RASR\rasr.conf

:: Restart WinPE session
wpeutil reboot

:: Shut down
wpeutil shutdown
```

---

## Scripted Backup Creation

The following batch script can be called from Task Scheduler or a configuration management tool to perform a RASR backup with error handling:

```batch
@echo off
setlocal

set SERVER=%COMPUTERNAME%
set SHARE=\\nas01.example.com\rasr-images\%SERVER%
set USER=CORP\svc-rasr
set PASS=S3cr3t!
set LOG=C:\Logs\rasr-backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%.log
set RASR=C:\Program Files\Dell\RASR\rasrutil.exe

echo [%date% %time%] Starting RASR backup >> %LOG%

"%RASR%" /backup /dest "%SHARE%" /user %USER% /pass %PASS% /compress /log "%LOG%"

if %errorlevel% equ 0 (
    echo [%date% %time%] Backup completed successfully >> %LOG%
    exit /b 0
) else (
    echo [%date% %time%] Backup FAILED with error code %errorlevel% >> %LOG%
    :: Send alert (example: write to event log)
    eventcreate /T ERROR /ID 9001 /L APPLICATION /SO RASR ^
        /D "RASR backup failed with exit code %errorlevel%"
    exit /b %errorlevel%
)
```

---

## Image Management Commands Reference

| Task | Command |
|---|---|
| Create image (compressed) | `rasrutil.exe /backup /dest <path> /compress` |
| List images on share | `rasrutil.exe /listimages /source <path>` |
| Verify image integrity | `rasrutil.exe /verify /source <image_file>` |
| Delete old image | `rasrutil.exe /deleteimage /source <image_file>` |
| Restore image | `rasrutil.exe /restore /source <image_file> /target <disk#>` |
| Create boot media (USB) | `rasrutil.exe /createmedia /dest <drive:>` |
| Create boot media (ISO) | `rasrutil.exe /createmedia /dest <file.iso>` |
