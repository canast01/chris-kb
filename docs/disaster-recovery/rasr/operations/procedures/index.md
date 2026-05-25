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

**Post-capture:**
- Verify image is readable: `dism /Get-ImageInfo /ImageFile:<image-path>`
- Update the server's recovery card with the new image date.
- Remove images beyond retention policy.

---

## Procedure 2: Bare-Metal Recovery (WinPE)

**When:** Server OS is unbootable or hardware replaced. Uses iDRAC virtual media.

**Time required:** 30–90 minutes.

### Pre-recovery checklist

- [ ] iDRAC access confirmed (IP, credentials)
- [ ] Recovery share IP and credentials available (written/offline — do not rely on production systems)
- [ ] RASR ISO mapped in iDRAC
- [ ] Target disks confirmed (correct server, correct RAID config exists or will be rebuilt)

### Step-by-step

```text
Step 1: Boot from RASR Media

  iDRAC → Configuration → Virtual Media → Map Drive → select rasr-media.iso
  iDRAC → Power → Boot Next → Virtual Optical Drive → Reboot
  → WinPE loads, RASR wizard starts automatically

Step 2: Connect to Recovery Share

  In WinPE RASR wizard → "Connect to network share"
  OR from WinPE command prompt (Shift+F10):
    netsh interface ip set address "Ethernet" static <ire-ip> 255.255.255.0 <gateway>
    net use Z: \\nas01\rasr-images\prod\<hostname> /user:nashost\localuser

Step 3: Select Recovery Image

  RASR wizard → Browse → select the image file on Z:\
  Choose recovery point (date/time shown from image metadata)

Step 4: Select Target Disk

  Wizard shows available disks detected by WinPE
  Select the OS disk (verify by size and disk number — use diskpart to confirm if needed)
  WARNING: this will overwrite all data on the selected disk

Step 5: Start Restore

  Wizard → Restore → Confirm → Start
  Progress shown in wizard; typical rate: 5–10 GB/min over gigabit link

Step 6: Post-Restore

  Wizard → Reboot
  Remove virtual media before reboot (iDRAC → Virtual Media → Disconnect)
  Server boots from restored OS
```

### Verify after reboot

```powershell
# Run from the restored server
systeminfo | Select-String "OS Name|Install Date|System Boot"

# Check no VSS or agent errors at startup
Get-WinEvent -LogName Application -MaxEvents 50 |
  Where-Object { $_.LevelDisplayName -eq "Error" -and $_.TimeCreated -gt (Get-Date).AddHours(-1) }

# Verify RASR agent came up
Get-Service RASRAgent

# Confirm network and domain connectivity
Test-ComputerSecureChannel -Repair
```

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
