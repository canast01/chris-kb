# Horizon — Backup and Restore


<div class="kb-summary">
Backup and Restore reference covering Verify the Backup, App Volumes Manager Database Backup, DEM Config Share Backup, AppStack VMDK Backup, Golden Image Snapshot Management and 2 more sections.
</div>

  Backup Sources                        Backup Methods
```text
┌────────────────────────────────── VMware Horizon — Backup & Restore ──────────────────────────────────┐
│                                                                                                       │
│  Horizon backup covers the LDAP config database on Connection Servers, golden image                   │
│  VMs, and user profile shares; desktop VMs themselves are stateless (instant clone).                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Config Backup                 │  │             Golden Image Backup             │   │
│   │          LDAP backup: vdmexport.exe          │  │          VM snapshot before update          │   │
│   │           Schedule: daily minimum            │  │         Clone golden image: pre-push        │   │
│   │           Store: secure file share           │  │            Keep N-1 + N-2 images            │   │
│   │          Include: Events DB backup           │  │          VADP: backup if persistent         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  LDAP backup is most critical; without it Horizon config must be rebuilt manually.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Profile & Restore               │  │              Restore Procedure              │   │
│   │          User profiles: FSLogix/DEM          │  │           Restore LDAP: vdmimport           │   │
│   │         Profile share: daily backup          │  │          Re-register CS: reconnect          │   │
│   │           DEM config: GPO + share            │  │          Rebuild pools from golden          │   │
│   │          AppStack: backup VMDK file          │  │             Validate: test login            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Connection Server VMs should be backed up via VADP as well; profile CIFS share                       │
│  must be on backed-up NAS; AppStack VMDKs on backed-up datastore.                                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vdmexport.exe = Horizon LDAP config export tool; run on Connection Server                            │
│  vdmimport     = Horizon LDAP config import; restore from backup                                      │
│  LDAP          = Horizon stores its config in AD LDS (LDAP store)                                     │
│  Golden image  = template VM; all instant clones derive from this                                     │
│  N-1/N-2       = keep two previous golden image versions for rollback                                 │
│  Events DB     = Horizon event log; SQL Server; backup separately                                     │
│  FSLogix       = user profile container; VHDX file on CIFS share                                      │
│  DEM           = Dynamic Environment Manager; policy-based profile                                    │
│  AppStack      = App Volumes VMDK; contains installed applications                                    │
│  VADP          = backup API; use for persistent full clone VMs                                        │
│  CIFS share    = Windows file share; user profile store                                               │
│  Re-register   = reconnect Connection Server to Horizon pod after restore                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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

## Verify the Backup

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
