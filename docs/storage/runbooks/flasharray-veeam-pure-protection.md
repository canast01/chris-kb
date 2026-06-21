---
tags:
  - pure-storage
  - flasharray
  - veeam
  - pure-protection
  - safemode
  - backup
  - ransomware-protection
  - snapshots
  - runbook
---

# Pure Storage FlashArray with Veeam and Pure Protection

<div class="kb-summary">
Cross-product runbook integrating Pure Storage FlashArray, Veeam Backup and Replication, and Pure Protection with SafeMode immutable snapshots. Covers FlashArray volume and protection group prep, Veeam storage snapshot integration, SafeMode immutability verification, and restore testing across crash-consistent and app-consistent scenarios.
</div>

```text
  ┌────────────────────────────────────────────────────────────────────────┐
  │                        PROTECTION ARCHITECTURE                         │
  │                                                                        │
  │  ┌──────────────────────────────┐   ┌───────────────────────────────┐  │
  │  │      FlashArray (Primary)    │   │     Veeam B&R Server          │  │
  │  │                              │   │                               │  │
  │  │  ┌──────────┐ ┌───────────┐  │   │  ┌─────────────────────────┐  │  │
  │  │  │  Volumes │ │  Pure     │  │   │  │  Backup Jobs            │  │  │
  │  │  │  vol_vm* │ │  Protection│ │   │  │  ┌─────────────────────┐│  │  │
  │  │  └──────────┘ │  Group    │ │   │  │  │ Storage Snapshot    ││  │  │
  │  │               │  pg_prod  │◄┼───┼──┼─►│ Integration (VADP)  ││  │  │
  │  │               └───────────┘ │   │  │  └─────────────────────┘│  │  │
  │  │                             │   │  └─────────────────────────┘  │  │
  │  │  ┌──────────────────────┐   │   │                               │  │
  │  │  │ SafeMode (Immutable) │   │   │  ┌─────────────────────────┐  │  │
  │  │  │ Snapshots — eradicate│   │   │  │  Backup Copy Job        │  │  │
  │  │  │ protected 24h delay  │   │   │  │  → Object Storage /Tape │  │  │
  │  │  └──────────────────────┘   │   │  └─────────────────────────┘  │  │
  │  └──────────────────────────────┘   └───────────────────────────────┘  │
  │                  │ Hardware snapshots                    │              │
  │                  │ (seconds RPO)                         │              │
  │  ┌───────────────▼──────────────────────────────────────▼───────────┐  │
  │  │                      Pure1 Cloud                                  │  │
  │  │  SafeMode status  │  Capacity analytics  │  Array management     │  │
  │  └───────────────────────────────────────────────────────────────────┘  │
  └────────────────────────────────────────────────────────────────────────┘

  RPO SUMMARY:
  Pure Protection snapshots  : minutes (schedule-driven)
  Veeam backup job           : hours (policy-driven, RPO SLA)
  SafeMode immutable copy    : protected for configured retention
  Backup copy (object/tape)  : daily offsite
```

## Before You Begin

**Prerequisites:**

| Component | Requirement |
|---|---|
| FlashArray | Purity 6.1+; admin credentials; SafeMode must be requested via Pure Support |
| Veeam B&R | v12+; Windows Server 2019+ or VBR appliance; connected to vCenter |
| Pure Storage Plugin for Veeam | Installed on Veeam server (download from Pure1/support portal) |
| Pure1 | Array registered in Pure1 (for SafeMode status view) |
| Network | Veeam server has iSCSI/FC access to FlashArray management and data ports |
| SafeMode | Must be enabled by Pure Support — submit SR before this runbook |

**Accounts needed:**

```text
pureuser (FlashArray) — array admin role
veeam_svc@corp.local  — Veeam service account, local admin on Veeam server
vcenter_backup@corp.local — vCenter read/backup role for Veeam
```

---

## Architecture Overview

```text
DATA PROTECTION TIERS:
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Tier 1: Pure Protection Snapshots (on-array, space-efficient)                                         │
│   Schedule: hourly, retain 24h → daily, retain 30 days                                                │
│   RPO: minutes  RTO: seconds (clone from snapshot)                                                    │
├────────────────────────────────────────────────────────────────┤
│ Tier 2: Veeam Backup (application-consistent, VADP)                                                   │
│   Schedule: nightly  Retain: 14 restore points                                                        │
│   RPO: hours  RTO: minutes (Instant VM Recovery)                                                      │
├────────────────────────────────────────────────────────────────┤
│ Tier 3: Veeam Backup Copy → Object Storage (immutable)                                                │
│   Schedule: daily  Retain: 30 days (GFS monthly 12 months)                                            │
│   RPO: 24h  RTO: minutes to hours (depends on object tier)                                            │
├────────────────────────────────────────────────────────────────┤
│ Tier 4: SafeMode Immutable Snapshots (ransomware protection)                                          │
│   Eradication delay: 24h minimum (configurable)                                                       │
│   Cannot be deleted during lock period — even by array admin                                          │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: FlashArray Preparation

### 1.1 Create Volumes and Host Group

```bash
# Connect to FlashArray CLI
ssh pureuser@flasharray01.corp.local

# Create volumes (one per VM datastore or per application)
purevol create --size 2T vol_vmdata01
purevol create --size 2T vol_vmdata02
purevol create --size 500G vol_veeam_proxy

# Create host entries for ESXi hosts
purehost create --iqn iqn.1998-01.com.vmware:esxi01 esxi01
purehost create --iqn iqn.1998-01.com.vmware:esxi02 esxi02

# Group ESXi hosts
purehgroup create --hostlist esxi01,esxi02 hg-esxi-cluster

# Connect volumes to host group
purevol connect --hgroup hg-esxi-cluster vol_vmdata01
purevol connect --hgroup hg-esxi-cluster vol_vmdata02

# Verify
purevol list --connection
```

### 1.2 Create Pure Protection Group

```bash
# Create protection group for production VMs
pureprotection create --vollist vol_vmdata01,vol_vmdata02 pg_prod

# Set snapshot schedule:
# Hourly snapshots retained for 24 hours
# Daily snapshots retained for 30 days
pureprotection set \
  --snap-frequency 3600 \
  --snap-retention 86400 \
  pg_prod

# Set daily schedule (runs at midnight)
pureprotection set \
  --replfreq 86400 \
  --repl-retention 2592000 \
  pg_prod

# Enable the schedule
pureprotection enable pg_prod

# Verify schedule
pureprotection list --schedule pg_prod
```

### 1.3 Enable SafeMode on Protection Group

```bash
# NOTE: SafeMode must first be activated on the array by Pure Support
# Once enabled, set eradication delay (minimum 24h, default 24h)

pureprotection safemode --enable --eradication-delay 1440 pg_prod
# eradication-delay is in minutes: 1440 = 24h

# Verify SafeMode status
pureprotection list pg_prod
# Look for: safemode = enabled, eradication_delay = 1440

# Take an immediate snapshot to verify SafeMode applies
pureprotection snap --suffix manual-test pg_prod

# List snapshots
pureprotection list --snap pg_prod
```

### 1.4 Verify Initial Snapshot

```bash
# List all snapshots in protection group
pureprotection list --snap --name pg_prod

# Attempt to eradicate a snapshot (will be denied during lock period)
pureprotection eradicate --name "pg_prod.manual-test"
# Expected: Error — SafeMode prevents eradication before delay expires
```

---

## Phase 2: Veeam Integration

### 2.1 Add FlashArray as Storage System in Veeam

1. Open **Veeam Backup and Replication Console**
2. Navigate to **Storage Infrastructure → Add Storage → Pure Storage → FlashArray**
3. Enter:
   - **Management IP/FQDN:** `flasharray01.corp.local`
   - **Credentials:** `pureuser` / `<password>`
4. Click **Next** → Veeam discovers volumes and protection groups
5. On **Storage Access** page — select iSCSI or Fibre Channel paths
6. Click **Finish**

### 2.2 Configure Backup Job with Storage Snapshot Integration

1. Navigate to **Home → Backup Job → Virtual Machine**
2. **Name:** `PROD-VMs-FlashArray`
3. **Virtual Machines:** Add VM folder or individual VMs on FlashArray-backed datastores
4. **Storage:** Backup repository (local repo or Scale-Out Backup Repository)
5. **Advanced settings → Integration tab:**
   - Enable: **Use storage snapshots to provide application consistency**
   - Provider: `Pure Storage FlashArray`
   - Select protection group: `pg_prod`
6. **Schedule:** Daily at 22:00, keep 14 restore points
7. Click **Finish**

### 2.3 Veeam PowerShell — Verify Job Configuration

```powershell
# On Veeam server
Add-PSSnapin VeeamPSSnapIn -ErrorAction SilentlyContinue

# Get job details
$job = Get-VBRJob -Name "PROD-VMs-FlashArray"
$job | Select-Object Name, JobType, ScheduleOptions

# Check storage integration is enabled
$job.GetStorageIntegrationOptions()

# Trigger an immediate backup run
Start-VBRJob -Job $job

# Monitor job progress
Get-VBRBackupSession | Where-Object {$_.JobName -eq "PROD-VMs-FlashArray"} | 
  Select-Object JobName, State, Progress, EndTime | Format-Table
```

### 2.4 Configure Backup Copy to Object Storage

```powershell
# Create S3 object storage repository (if not already done)
$account = New-VBRCredentials -User "s3-access-key" -Password "s3-secret-key" -Description "S3 Immutable"
$s3repo = Add-VBRObjectStorageRepository `
  -Name "S3-Immutable-Archive" `
  -AmazonS3Compatible `
  -ServicePoint "https://s3.corp.local" `
  -Bucket "veeam-immutable" `
  -Credentials $account `
  -EnableSizeLimitGB 10240 `
  -MakeImmutableForDays 30

# Create backup copy job
Add-VBRBackupCopyJob `
  -Name "PROD-VMs-BackupCopy-S3" `
  -SourceJob $job `
  -TargetRepository $s3repo `
  -RestorePoints 30 `
  -GFSMonthlyBackups 12
```

---

## Phase 3: SafeMode Verification

### 3.1 Verify Immutability from CLI

```bash
# Connect to FlashArray
ssh pureuser@flasharray01.corp.local

# List current SafeMode snapshots
pureprotection list --snap pg_prod | head -20

# Attempt to manually delete a SafeMode-protected snapshot
pureprotection delete --name "pg_prod.3600"
# Expected output:
# Error: Snapshot pg_prod.3600 cannot be eradicated — SafeMode lock active
# Remaining lock time: 23h 45m
```

### 3.2 Verify SafeMode Status in Pure1

1. Log into **Pure1:** `https://pure1.purestorage.com`
2. Navigate to your array → **Protection → Protection Groups**
3. Select `pg_prod` → verify **SafeMode: Enabled**
4. Check **Eradication Delay:** 1440 minutes
5. Review snapshot count and oldest/newest timestamps

### 3.3 Deletion Test (Controlled)

```bash
# Take a test snapshot with no-retention intent
pureprotection snap --suffix safemode-test pg_prod

# Immediately attempt eradication
pureprotection eradicate --name "pg_prod.safemode-test"
# Expected: Denied — eradication delay not yet expired

# After 24h+ delay, eradication would succeed
# This confirms SafeMode is active and functioning
echo "SafeMode verification: PASS — deletion denied as expected"
```

---

## Phase 4: Restore Testing

### 4.1 Veeam Instant VM Recovery from FlashArray Snapshot

```powershell
# On Veeam server — restore VM from latest FlashArray-integrated backup
$restorePoint = Get-VBRRestorePoint -Name "webvm01" | 
  Sort-Object CreationTime -Descending | Select-Object -First 1

# Start Instant VM Recovery (VM runs directly from backup storage)
$session = Start-VBRRestoreSession `
  -RestorePoint $restorePoint `
  -Reason "DR Test - Phase 4 Restore Validation"

# Get the recovered VM details
Get-VBRInstantRecoveryMount | Format-List VMName, DatastoreName, MountedAt
```

### 4.2 Granular Item Recovery (File-Level)

```powershell
# Mount backup for file-level restore
$restorePoint = Get-VBRRestorePoint -Name "fileserver01" | 
  Sort-Object CreationTime -Descending | Select-Object -First 1

# Start file-level restore session
Start-VBRWindowsFileRestore -RestorePoint $restorePoint

# For Linux guests:
Start-VBRLinuxFileRestore -RestorePoint $restorePoint
```

### 4.3 FlashArray Volume Restore from Pure Protection Snapshot

```bash
# SSH to FlashArray
ssh pureuser@flasharray01.corp.local

# List available snapshots
pureprotection list --snap pg_prod

# Copy volume from snapshot to a restore target volume
purevol copy pg_prod.86400.vol_vmdata01 vol_vmdata01_restore

# Connect restore volume to a test host
purevol connect --host esxi-test vol_vmdata01_restore

# On ESXi host — rescan and mount the restored datastore
# Then power on the VM from restored volume to validate data
esxcli storage core adapter rescan --all
```

### 4.4 RPO/RTO Summary

| Scenario | RPO | RTO | Method |
|---|---|---|---|
| Pure Protection snapshot (crash-consistent) | 1h | < 5 min | `purevol copy` from snapshot |
| Pure Protection snapshot (app-consistent with Veeam) | 1h | < 5 min | Veeam + FlashArray snap integration |
| Veeam Instant VM Recovery | Hours (last backup) | < 2 min | Instant recovery from repo |
| Veeam full VM restore | Hours (last backup) | 15–45 min | Full restore to datastore |
| Object storage backup copy | 24h | 1–4h | Restore from S3 immutable repo |
| SafeMode snapshot (post-ransomware) | Varies | < 30 min | `purevol copy` after lock expires |

---

## Rollback

If Veeam integration with FlashArray storage snapshots causes backup failures:

### Disable Storage Snapshot Integration

```powershell
# Revert to standard VADP backup (no FlashArray integration)
$job = Get-VBRJob -Name "PROD-VMs-FlashArray"
$options = $job.GetStorageIntegrationOptions()
$options.UseStorageSnapshots = $false
$job.SetStorageIntegrationOptions($options)
$job.SaveOptions()
```

### Disconnect FlashArray from Veeam (Emergency)

1. Open Veeam Console → **Storage Infrastructure**
2. Right-click `flasharray01.corp.local` → **Remove**
3. Existing restore points remain valid — jobs revert to VADP mode

### Revert to Previous Protection Group Schedule

```bash
# Disable protection group schedule if causing issues
pureprotection disable pg_prod

# Re-enable with modified settings
pureprotection set --snap-frequency 7200 pg_prod
pureprotection enable pg_prod
```

---

## See Also

- [Storage Runbooks Index](index/)
- [Veeam + ONTAP SnapVault Integration](veeam-ontap-snapvault-integration/)
- [DR Failover: SRM + SnapMirror](dr-failover-vmware-srm-snapmirror/)
- [Pure Storage FlashArray](../../storage/flasharray/)
- [Veeam Backup and Replication](../../backup/veeam/)
