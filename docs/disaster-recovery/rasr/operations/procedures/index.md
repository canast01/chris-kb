# RASR — Procedures

> Part of the [RASR Operations](../index.md) reference.

---

## Procedure 1: Capture System Image

**When:** After OS changes, patch events, or on schedule. Run from within the running Windows OS.

**Time required:** 20–60 minutes depending on OS volume size.

```powershell
# Step 1: Verify agent is running
Get-Service RASRAgent   # must be Running

# Step 2: Check available space on recovery share before capture
$share = "\\nas01\rasr-images\prod\$(hostname)"
if (-not (Test-Path $share)) { New-Item -ItemType Directory -Path $share }

# Step 3: Trigger capture via RASR Console (GUI)
#   Start → Dell OpenManage → Recovery and System Restore
#   → Backup → Create New Backup → select share path → Start

# OR trigger via command line (if supported by installed version)
& "C:\Program Files\Dell\RASR\RASRCmd.exe" /backup /target:$share /name:"$(hostname)_prod_$(Get-Date -Format yyyyMMdd)_001"

# Step 4: Monitor progress
Get-Content "C:\Program Files\Dell\RASR\Logs\RASRAgent.log" -Tail 20 -Wait

# Step 5: Verify image created
Get-ChildItem $share | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```
┌────────────────────────────────────────── RASR — Procedures ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Routine Procedures              │  │                DR Procedures                │   │
│   │          Add new protection source           │  │              Initiate failover              │   │
│   │           Modify retention policy            │  │               Validate replica              │   │
│   │          Expire old recover points           │  │              Redirect host I/O              │   │
│   │             Add storage capacity             │  │         Test failover (non-disrupt)         │   │
│   │           Service account rotation           │  │            Failback to production           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Change Control Requirements for RASR                             │   │
│   │           All changes to protection policies require change ticket with rollback plan         │   │
│   │                      Failover tests must be scheduled in maintenance window                   │   │
│   │              Firmware/software upgrades need 48 h pre-approval and backup snapshot            │   │
│   │                  Post-change: verify jobs run successfully for 2 backup cycles                │   │
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

---

## Procedure 3: File-Level Recovery from Image

**When:** Specific files or directories need to be recovered without a full restore.

```powershell
# Mount the RASR WIM image as a drive letter (Windows 10/2019+)
$imagePath = "\\nas01\rasr-images\prod\app01\app01_prod_20260510_001.wim"
$mountPath = "C:\rasr-mount"

New-Item -ItemType Directory -Path $mountPath -Force
dism /Mount-Image /ImageFile:$imagePath /Index:1 /MountDir:$mountPath /ReadOnly

# Browse and copy required files
Get-ChildItem $mountPath\Users\Administrator\AppData\Local\
Copy-Item "$mountPath\Program Files\MyApp\config\app.conf" C:\Recovered\

# Unmount when done
dism /Unmount-Image /MountDir:$mountPath /Discard
```

---

## Procedure 4: Create / Update Recovery Media

**When:** New server generation added; RASR agent updated; media hasn't been rebuilt in 6 months.

```text
RASR Console → Media → Create New Media
  → Select output: ISO file
  → Output path: \\nas01\rasr-images\media\rasr-media-15G-$(Get-Date -Format yyyyMM).iso
  → Build

After creation:
  1. Map new ISO in iDRAC and verify it boots to WinPE.
  2. Confirm network driver loads and share is reachable.
  3. Replace old ISO reference in documentation and iDRAC pre-mapped media.
```

---

## Procedure 5: Retention Cleanup

**When:** Monthly, or when recovery share free space drops below 30%.

```powershell
$share     = "\\nas01\rasr-images\prod"
$keepDaily = 7    # days
$keepWeekly = 4   # weeks

Get-ChildItem $share -Recurse -Filter "*.wim" |
  Where-Object { $_.Name -notmatch "_weekly|_post-patch" -and $_.LastWriteTime -lt (Get-Date).AddDays(-$keepDaily) } |
  ForEach-Object {
    Write-Host "Removing: $($_.FullName) [$(($_.Length / 1GB).ToString('F1')) GB]"
    # Remove-Item $_.FullName   # uncomment after dry-run review
  }

# Review output before uncommenting Remove-Item
```
