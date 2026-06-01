# Windows Server — Backup & Restore


<div class="kb-summary">
Veeam Agent for Windows, Windows Server Backup, restore procedures, and validation steps.
</div>

## Veeam Agent for Windows

Veeam Agent for Windows provides image-level and file-level backup for Windows servers. It can run standalone or be managed centrally by a Veeam Backup & Replication server.

### Installation

```powershell
# Silent installation of Veeam Agent for Windows
Start-Process -Wait -FilePath "VeeamAgentWindows.exe" -ArgumentList "/silent /accepteula"

# Verify service is running
Get-Service -Name "Veeam Agent for Microsoft Windows"
```
```powershell
┌───────────────────────────────── Windows Server — Backup and Restore ─────────────────────────────────┐
│                                                                                                       │
│  Windows Server backup strategies: VSS-based backups, AD backup, and Hyper-V checkpoints.             │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │         Windows Server Backup (WSB)          │  │           Active Directory Backup           │   │
│   │           wbadmin: CLI backup tool           │  │        ntdsutil: AD snapshot + backup       │   │
│   │          VSS: consistent snapshots           │  │         System State includes AD DB         │   │
│   │          Bare metal recovery (BMR)           │  │         Authoritative restore: NTDS         │   │
│   │          Scheduled: daily + monthly          │  │           AD Recycle Bin: 180-day           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    System State backup captures AD; BMR for full server recovery                                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Hyper-V Backup                │  │           Third-Party / Enterprise          │   │
│   │           VM checkpoint: snapshot            │  │           Veeam: agent + VM backup          │   │
│   │         Export VM: offline full copy         │  │          DPM: System Center backup          │   │
│   │          Application-consistent VSS          │  │        Azure Backup: cloud retention        │   │
│   │           Replica: standby VM copy           │  │         Test restore: quarterly SLA         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Physical or virtual server · backup storage (NAS/tape/Azure) · Hyper-V host                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  wbadmin      = command-line tool for Windows Server Backup operations                                │
│  VSS          = Volume Shadow Copy Service; quiesces app for consistent backup                        │
│  BMR          = Bare Metal Recovery; restore entire OS without pre-existing install                   │
│  System State = AD DB + SYSVOL + registry + boot files; AD backup minimum                             │
│  ntdsutil     = AD utility; used for authoritative restore and metadata cleanup                       │
│  Authoritative restore= restore marks AD objects with higher USN to replicate                         │
│  AD Recycle Bin= soft-delete; restore via Get-ADObject + Restore-ADObject                             │
│  VM checkpoint= point-in-time snapshot of VM state; not a backup replacement                          │
│  VM Replica   = Hyper-V async replication to another host; DR option                                  │
│  DPM          = Data Protection Manager; System Center backup product                                 │
│  Azure Backup = cloud backup service; supports on-prem via MARS agent                                 │
│  Test restore = periodic recovery drill; validates backup integrity                                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```powershell

## Windows Server Backup (WSB)

Windows Server Backup (WSB) is the built-in backup tool. Suitable for smaller environments or as a secondary backup.

### Installation

```powershell
# Install Windows Server Backup feature
Install-WindowsFeature Windows-Server-Backup -IncludeManagementTools

# Verify
Get-Command -Module WindowsServerBackup
```

### Configure a Backup Policy

```powershell
# Create a backup policy for the C: volume to a network location
$policy = New-WBPolicy

# Add the C: volume
$volume = Get-WBVolume -VolumePath "C:"
Add-WBVolume -Policy $policy -Volume $volume

# Add system state (recommended for domain controllers)
Add-WBSystemState -Policy $policy

# Add BMR (Bare Metal Recovery) support — includes system reserved partition
Add-WBBareMetalRecovery -Policy $policy

# Set network backup target
$netTarget = New-WBBackupTarget -NetworkPath "\\backupserver\WSB-SERVER01" `
  -Credential (Get-Credential)
Add-WBBackupTarget -Policy $policy -Target $netTarget

# Set daily schedule at 02:00 and 14:00
Set-WBSchedule -Policy $policy -Schedule 02:00, 14:00

# Apply the policy
Set-WBPolicy -Policy $policy -AllowDeleteOldBackups

# Verify policy
Get-WBPolicy
```

### Manual Backup

```powershell
# Start a backup immediately using the existing policy
Start-WBBackup -Policy (Get-WBPolicy)

# Check backup status
Get-WBJob | Select-Object JobType, StartTime, EndTime, HResult, ErrorDescription
```

### View Backup History

```powershell
# List all backup jobs
Get-WBJob -Previous 20 | Select-Object StartTime, EndTime, HResult, ErrorDescription

# Verify last successful backup
$lastBackup = Get-WBSummary
$lastBackup | Select-Object LastSuccessfulBackupTime, LastBackupResultHR, NumberOfVersions
```

## Restore Procedures

### File-Level Restore (Veeam Agent)

1. Open **Veeam Agent for Microsoft Windows** control panel.
2. Click **Restore** > **File Level Restore**.
3. Select a restore point.
4. Browse the backup contents using File Level Restore browser.
5. Right-click files or folders > **Restore to** or **Copy To**.

```powershell
# Veeam: Mount a restore point to a drive letter for manual file copy
# (Available via VBR console for agent backups managed by VBR)
Mount-VBRBackup -BackupName "SERVER01-Daily" -RestorePoint (
    Get-VBRRestorePoint -BackupName "SERVER01-Daily" | Select-Object -Last 1)
```

### Volume-Level Restore (Veeam Agent)

1. Boot from **Veeam Recovery Media** (pre-created ISO/USB).
2. Select **Volume Level Restore**.
3. Connect to backup repository.
4. Select the restore point.
5. Select source and target volumes.
6. Click **Restore** and reboot.

```powershell
# Create Veeam Recovery Media (run before disaster)
# From Veeam Agent control panel: Recovery Media > Create Recovery Media
# Output: ISO file or directly to USB

# Or via VBR server:
New-VBRLinuxIsoMediaFile -OutputPath "C:\Media\VeeamRecovery.iso"
```

### Bare Metal Recovery (Windows Server Backup)

1. Boot from Windows Server installation media.
2. Select **Repair your computer** > **Troubleshoot** > **System Image Recovery**.
3. Select the most recent system image.
4. Follow the wizard to restore.

```powershell
# Alternatively, use wbadmin for BMR from the command line (WinRE environment)
wbadmin get versions -backuptarget:\\backupserver\WSB-SERVER01
wbadmin start sysrecovery -version:<version-identifier> -backuptarget:\\backupserver\WSB-SERVER01 -recreateDisks
```

### File-Level Restore (Windows Server Backup)

```powershell
# List restore points
Get-WBBackupSet -BackupTarget (New-WBBackupTarget -NetworkPath "\\backupserver\WSB-SERVER01" -Credential (Get-Credential))

# Start a file recovery
Start-WBFileRecovery -BackupSet <backupset-object> -SourcePath "C:\Data\file.txt" -TargetPath "C:\Restored\"
```

### System State Restore (Active Directory)

For domain controllers — restore AD from system state backup.

```cmd
REM Boot into Directory Services Restore Mode (DSRM) — F8 at boot
REM Perform authoritative or non-authoritative restore

REM Non-authoritative restore (use when replicating from another DC)
wbadmin start systemstaterecovery -version:<version-identifier>

REM Authoritative restore (use to restore deleted AD objects)
REM After wbadmin restore, run ntdsutil before DC restarts replication:
ntdsutil "activate instance ntds" "authoritative restore" "restore subtree OU=Users,DC=corp,DC=local" quit quit
```

## Backup Validation

```powershell
# Veeam — verify a specific restore point (runs checksum validation)
# In VBR console: Jobs > right-click job > Verify

# Windows Server Backup — verify last backup
$summary = Get-WBSummary
if ($summary.LastBackupResultHR -ne 0) {
    Write-Warning "Last WSB backup failed with HR: $($summary.LastBackupResultHR)"
}

# Test file-level restore monthly
# 1. Mount a restore point or image
# 2. Copy a test file to a staging location
# 3. Verify the file matches the source (compare hash)
$sourceHash = Get-FileHash "C:\Data\critical-file.db" -Algorithm SHA256
$restoredHash = Get-FileHash "C:\Restored\critical-file.db" -Algorithm SHA256
if ($sourceHash.Hash -eq $restoredHash.Hash) {
    Write-Host "Restore validation PASSED" -ForegroundColor Green
} else {
    Write-Warning "Hash mismatch — investigate restore"
}
```

## Backup Monitoring

```powershell
# Check Veeam Agent service
Get-Service -Name "Veeam Agent for Microsoft Windows" | Select-Object Status, StartType

# Check Veeam Agent event log
Get-WinEvent -ProviderName "Veeam Agent" -MaxEvents 20 |
  Select-Object TimeCreated, LevelDisplayName, Message

# Alert on WSB failures (add to monitoring task)
$summary = Get-WBSummary
if ($summary.LastBackupResultHR -ne 0 -or
    $summary.LastSuccessfulBackupTime -lt (Get-Date).AddHours(-25)) {
    Send-MailMessage -To "alerts@corp.local" -From "monitor@corp.local" `
      -Subject "Backup Alert: SERVER01" `
      -Body "Last successful backup: $($summary.LastSuccessfulBackupTime)" `
      -SmtpServer "smtp.example.local"
}
```

## Backup Best Practices

| Practice | Detail |
|---|---|
| 3-2-1 rule | 3 copies, 2 different media types, 1 offsite |
| Retention | 14 daily, 4 weekly, 3 monthly minimum |
| Immutable copy | Use Veeam immutable backup repository |
| Encryption | Enable Veeam backup job encryption (AES-256) |
| Test restores | File-level restore test monthly |
| BMR test | Full bare metal restore test annually |
| Monitor alerts | Alert within 1 hour of a missed backup window |
| DC system state | Backup at least one DC system state daily |
| Application-aware | Enable Veeam application-aware processing for SQL/Exchange |

## Quick Reference

| Task | Tool / Command |
|---|---|
| Start Veeam job | Veeam Agent control panel > Start backup |
| WSB manual backup | `Start-WBBackup -Policy (Get-WBPolicy)` |
| WSB backup history | `Get-WBJob -Previous 20` |
| WSB summary | `Get-WBSummary` |
| WSB restore points | `Get-WBBackupSet` |
| File restore (WSB) | `Start-WBFileRecovery` |
| Veeam event log | `Get-WinEvent -ProviderName "Veeam Agent"` |
| Recovery Media | Veeam Agent > Create Recovery Media |
| System state restore | `wbadmin start systemstaterecovery -version:<id>` |
