# Horizon — Backup and Restore

```text
  Backup Sources                        Backup Methods
┌─────────────────────┐               ┌────────────────────────────┐
│  Connection Server  │──vdmexport───►│  LDIF file (pod config)    │
│  (ADAM/LDAP)        │               └────────────────────────────┘
├─────────────────────┤               ┌────────────────────────────┐
│  App Volumes SQL DB │──SQL backup──►│  cloudvolumes.bak          │
│  (cloudvolumes)     │               └────────────────────────────┘
├─────────────────────┤               ┌────────────────────────────┐
│  DEM Config Share   │──robocopy────►│  \\fileserver\DEMConfig\   │
│  (\\server\share)   │               └────────────────────────────┘
├─────────────────────┤               ┌────────────────────────────┐
│  Golden Image VM    │──snapshot────►│  PUBLISHED snapshot        │
│  + AppStack VMDKs   │               │  on datastore              │
└─────────────────────┘               └────────────────────────────┘
```

## What to Back Up

| Component | Backup Method | RPO Target | Critical? |
|---|---|---|---|
| Connection Server ADAM/LDAP config | `vdmexport.exe` | Daily | Yes — entire pod config |
| App Volumes Manager SQL database | SQL Server backup | Daily | Yes — all AppStack/writable assignments |
| DEM Config Share | File-level backup (agent-based or SMB snapshot) | Daily | Yes — all user environment policies |
| vCenter golden image VM snapshots | vSphere snapshot + datastore backup | Weekly | Yes — without this, pool rebuilds require re-imaging |
| App Volumes AppStack VMDKs | Datastore-level backup or file copy | Weekly | Yes — application packages |
| UAG configuration | INI file + screenshot of settings | Per change | Yes — allows rapid redeploy |
| Horizon event database (SQL) | SQL Server backup | Daily | No — historical reporting only |

---

## Connection Server ADAM Backup (vdmexport)

The Connection Server configuration is stored in an **ADAM (Active Directory Lightweight Directory Services)** instance on each Connection Server. `vdmexport.exe` exports this as an LDIF file.

### Backup

```cmd
:: Run on the Connection Server (or any CS in the pod)
:: Default install path
cd "C:\Program Files\VMware\VMware View\Server\tools\bin"

:: Export to LDIF
vdmexport.exe -f C:\Backups\horizon-config-backup.ldif

:: Export with date stamp (run from CMD)
vdmexport.exe -f "C:\Backups\horizon-config-%DATE:~10,4%%DATE:~4,2%%DATE:~7,2%.ldif"
```

**Automate with Task Scheduler:**
```cmd
:: Create scheduled task — daily at 02:00
schtasks /create /tn "Horizon ADAM Backup" /tr ^
  "\"C:\Program Files\VMware\VMware View\Server\tools\bin\vdmexport.exe\" -f C:\Backups\horizon-config-latest.ldif" ^
  /sc DAILY /st 02:00 /ru SYSTEM
```

**What is included in the LDIF export:**
- Desktop pool definitions
- Farm definitions
- Entitlements (pool-to-AD-group mappings)
- Persistent disk assignments (Full Clone)
- Global settings (LDAP-stored)
- vCenter server registrations
- App Volumes Manager registrations

**What is NOT included:**
- SSL certificates (backed up separately as .pfx files)
- Event database (SQL — backed up separately)
- Connection Server service account passwords (re-entered at restore time)

### Verify the Backup

```powershell
# Check file was created and is non-zero
$backup = "C:\Backups\horizon-config-latest.ldif"
if ((Get-Item $backup).Length -gt 1MB) {
    Write-Host "Backup OK: $((Get-Item $backup).Length / 1MB) MB"
} else {
    Write-Warning "Backup file is suspiciously small — check vdmexport output"
}

# Quick content check — should contain Connection Server entries
Select-String -Path $backup -Pattern "cn=vdi" | Select-Object -First 5
```

---

## App Volumes Manager Database Backup

App Volumes Manager uses a SQL Server database (`cloudvolumes` by default).

### SQL Server Backup (T-SQL)

```sql
-- Full backup
BACKUP DATABASE [cloudvolumes]
  TO DISK = N'D:\SQLBackups\cloudvolumes_full.bak'
  WITH COMPRESSION, STATS = 10;

-- Verify backup
RESTORE VERIFYONLY FROM DISK = N'D:\SQLBackups\cloudvolumes_full.bak';
```

### SQL Agent Job (PowerShell setup)

```powershell
# Using dbatools module
Install-Module dbatools -Scope CurrentUser

# Backup
Backup-DbaDatabase -SqlInstance sql01.corp.example.com `
  -Database cloudvolumes `
  -BackupDirectory "\\backupserver\SQLBackups\AppVolumes" `
  -CompressBackup `
  -Checksum

# Restore test (to alternate instance)
Restore-DbaDatabase -SqlInstance sql01-test.corp.example.com `
  -Path "\\backupserver\SQLBackups\AppVolumes\cloudvolumes_*.bak" `
  -DatabaseName cloudvolumes_restore_test `
  -WithReplace
```

---

## DEM Config Share Backup

The DEM config share is a standard SMB file share — back it up with whatever agent-based or share-snapshot method you use for file servers.

### Robocopy Backup

```cmd
:: Mirror DEM config share to backup location
robocopy \\fileserver\DEMConfig D:\Backups\DEMConfig /MIR /LOG:D:\Logs\dem-backup.log /NP /R:3 /W:10
```

### PowerShell with Date Stamp

```powershell
$src = "\\fileserver\DEMConfig"
$dst = "D:\Backups\DEMConfig\$(Get-Date -Format 'yyyyMMdd')"
New-Item -ItemType Directory -Path $dst -Force
robocopy $src $dst /MIR /R:3 /W:5 /LOG:"D:\Logs\dem-backup-$(Get-Date -Format 'yyyyMMdd').log"
```

**What is in the DEM Config Share:**

```text
DEMConfig\
  General\          — Global DEM settings
  FlexEngine\       — FlexEngine policies (app settings capture, drive maps, etc.)
  DirectFlex\       — DirectFlex triggers
  Exports\          — Exported settings bundles
  PolicyTemplates\  — Custom policy templates
  Logging\          — DEM agent logs (read/write by all desktops)
```

Note: The `Logging\` subfolder can grow large. Exclude from backup or set a retention policy.

---

## AppStack VMDK Backup

AppStacks are stored as VMDKs on a datastore. Back them up via:

1. **Datastore-level backup** (preferred if using a backup product with VADP support, e.g., Veeam, Commvault) — back up the `cloudvolumes/apps/` folder as VM-agnostic VMDK files
2. **File copy to NFS/CIFS backup share** — AppStacks are read-only so file copy is safe while desktops are running

```powershell
# PowerCLI — copy AppStack VMDKs to backup datastore
Connect-VIServer vcenter.corp.example.com

$srcDS = Get-Datastore "SAN-Datastore01"
$dstDS = Get-Datastore "Backup-Datastore"

# Use Copy-DatastoreItem (requires datastore provider)
New-PSDrive -Name srcDS -PSProvider VimDatastore -Root "\" -Datastore $srcDS
New-PSDrive -Name dstDS -PSProvider VimDatastore -Root "\" -Datastore $dstDS

Copy-DatastoreItem -Item "srcDS:\cloudvolumes\apps\*" `
  -Destination "dstDS:\cloudvolumes-backup\$(Get-Date -Format 'yyyyMMdd')\" `
  -Recurse
```

---

## Golden Image Snapshot Management

Golden image snapshots are the recovery point for Instant Clone pool image quality.

```powershell
# List snapshots on golden image VM
Get-VM "GoldenImage-Win11" | Get-Snapshot | Select-Object Name, Created, Description | Format-Table

# Verify snapshot is in "PUBLISHED" state (by naming convention)
Get-VM "GoldenImage-Win11" | Get-Snapshot | Where-Object { $_.Name -like "*PUBLISHED*" }

# Remove deprecated snapshots older than 90 days
Get-VM "GoldenImage-Win11" | Get-Snapshot | Where-Object {
  $_.Name -like "*DEPRECATED*" -and $_.Created -lt (Get-Date).AddDays(-90)
} | Remove-Snapshot -Confirm:$false
```

---

## Connection Server Restore Procedure

### Scenario: Single CS Failure (Others Still Running)

No restore needed — ADAM replicates automatically. Install a new Connection Server, add it to the pod:

```cmd
:: During Connection Server install, choose "Add a Replica Server"
:: Point to existing Connection Server FQDN
:: ADAM config replicates automatically within minutes
```

### Scenario: All Connection Servers Lost (Full Pod Recovery)

1. Install Windows Server, join domain, install Horizon Connection Server (choose **Standard** install)
2. Import the LDIF backup:

```cmd
cd "C:\Program Files\VMware\VMware View\Server\tools\bin"

:: Import backed-up configuration
vdmimport.exe -f C:\Backups\horizon-config-backup.ldif
```

3. Re-enter credentials for:
   - vCenter service account password
   - AD bind account password (Instant Clone domain join)
   - App Volumes Manager credentials

4. Re-upload SSL certificate (import .pfx to Windows certificate store, bind to Horizon)

5. Verify pools, entitlements, and vCenter registration in Admin Console

6. Install additional Connection Servers as replicas (ADAM replicates from the restored primary)

### Scenario: LDIF Import Fails

```cmd
:: Import with verbose logging
vdmimport.exe -f C:\Backups\horizon-config-backup.ldif -v

:: Common error: duplicate entries — use -u flag to update instead of add
vdmimport.exe -f C:\Backups\horizon-config-backup.ldif -u
```

---

## Writable Volume (App Volumes) Backup

Writable volumes contain user-installed apps and data. They require consistent backup (VM-aware or quiesced).

```powershell
# Using Veeam PowerShell snap-in (example)
Add-PSSnapin VeeamPSSnapIn

# Protect the App Volumes writable volume datastore
# In practice, use VADP-aware backup that quiesces VMDKs
# OR — only back up writables for users who require it (not all deployments need this)

# File copy approach (offline volumes only — only safe when user is logged off)
# Check if writable is attached (in-use) before copying
```

**Recommendation for most environments:** Writable volumes are for user-installed apps, not primary data. Rely on the App Volumes Manager DB backup (which records the assignment) and re-provision the writable volume VMDK if lost. User-installed apps can be re-installed or recaptured as AppStacks.
