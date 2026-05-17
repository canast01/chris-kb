# PowerShell — Backup & Restore

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
```

## Module List Export

Export installed modules so they can be reinstalled on a new system.

```powershell
# Export installed module list
Get-Module -ListAvailable |
    Select-Object Name, Version, ModuleType |
    Export-Csv -Path "$env:USERPROFILE\ps-modules-$(Get-Date -Format 'yyyyMMdd').csv" -NoTypeInformation

# Reinstall from exported list
Import-Csv "$env:USERPROFILE\ps-modules-backup.csv" | ForEach-Object {
    Install-Module -Name $_.Name -RequiredVersion $_.Version -Force -Scope CurrentUser
}
```

## Script Repository Backup

```powershell
# Compress scripts directory
$ScriptsDir  = "$env:USERPROFILE\scripts"
$BackupFile  = "$env:USERPROFILE\scripts-backup-$(Get-Date -Format 'yyyyMMdd').zip"
Compress-Archive -Path $ScriptsDir -DestinationPath $BackupFile -Force
Write-Host "Scripts archived to: $BackupFile"
```

## Restore Checklist

1. Install PowerShell 7+ on the new system
2. Install PowerCLI: `Install-Module VMware.PowerCLI -Scope CurrentUser`
3. Restore profile: `Copy-Item .\Microsoft.PowerShell_profile.ps1 $PROFILE -Force`
4. Reinstall modules from exported CSV
5. Verify: `$PSVersionTable` and `Get-Module -ListAvailable`
