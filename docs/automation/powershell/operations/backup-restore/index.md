# PowerShell — Backup & Restore


<div class="kb-summary">
Backup & Restore reference covering Profile and Configuration Backup, Restore Checklist.
</div>

## Profile and Configuration Backup

```powershell
# Locate and back up PowerShell profiles
$ProfilePaths = @(
    $PROFILE.AllUsersAllHosts,
    $PROFILE.AllUsersCurrentHost,
    $PROFILE.CurrentUserAllHosts,
    $PROFILE.CurrentUserCurrentHost
)
$BackupDir = "$env:USERPROFILE\ps-backup-$(Get-Date -Format 'yyyyMMdd')"
New-Item -Path $BackupDir -ItemType Directory -Force | Out-Null
foreach ($p in $ProfilePaths) {
    if (Test-Path $p) {
        Copy-Item $p $BackupDir -Force
        Write-Host "Backed up: $p"
    }
}
```text
┌──────────────────────────────────── PowerShell — Backup & Restore ────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    PowerShell script backup: store all .ps1/.psm1/.psd1 in git — git is the source of truth   │   │
│   │  DSC configurations: check in to git; MOF files are generated from config — do not store MOF  │   │
│   │      Restore: clone repo, install pinned module versions, re-configure remoting endpoints     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               What to Back Up                │  │                Restore Steps                │   │
│   │      Git repo (all .ps1, .psm1, .psd1)       │  │          1. Clone repo to new host          │   │
│   │       Module version list (lock file)        │  │          2. Install pinned modules          │   │
│   │             JEA endpoint configs             │  │           3. Register PSRepository          │   │
│   │          Scheduled task definitions          │  │           4. Restore JEA endpoints          │   │
│   │          PSRepository registrations          │  │          5. Verify test script runs         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Module lock    = document exact versions: Get-InstalledModule | Export-Csv modules.csv    │   │
│   │     JEA config    = .pssc session configuration; Register-PSSessionConfiguration to apply     │   │
│   │      Scheduled task = Export-ScheduledTask | Out-File; Import via Register-ScheduledTask      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Restore Checklist

1. Install PowerShell 7+ on the new system
2. Install PowerCLI: `Install-Module VMware.PowerCLI -Scope CurrentUser`
3. Restore profile: `Copy-Item .\Microsoft.PowerShell_profile.ps1 $PROFILE -Force`
4. Reinstall modules from exported CSV
5. Verify: `$PSVersionTable` and `Get-Module -ListAvailable`
