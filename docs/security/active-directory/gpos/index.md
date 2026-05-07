# Group Policy Objects

GPOs apply configuration to computers and users in AD. They are linked to Sites, Domains, or OUs and processed in that order (SDOU). Understanding GPO inheritance, filtering, and result sets is essential for managing policy reliably.

## GPO Processing Order

| Level | Priority (low to high) | Notes |
|---|---|---|
| Local | 1 | Machine-local policy |
| Site | 2 | Rarely used in practice |
| Domain | 3 | Domain-wide defaults |
| OU | 4 | Closest OU wins |
| Child OU | 5 | Overrides parent OU |

Later-processed policies win unless Block Inheritance or Enforced (No Override) is set.

## Creating and Linking a GPO

```powershell
# Create a new GPO
New-GPO -Name "Security Baseline - Servers" -Comment "CIS Level 1 server policy"

# Link GPO to an OU
New-GPLink -Name "Security Baseline - Servers" -Target "OU=Servers,DC=corp,DC=example,DC=com"

# Create and link in one step
New-GPO -Name "Desktop Lockscreen" | New-GPLink -Target "OU=Workstations,DC=corp,DC=example,DC=com"

# Set link order (lower number = higher priority)
Set-GPLink -Name "Desktop Lockscreen" -Target "OU=Workstations,DC=corp,DC=example,DC=com" -Order 1
```

## Viewing Applied Policy

```cmd
# Show applied GPOs for the current user and computer
gpresult /r

# Verbose HTML report
gpresult /h C:\Temp\gpresult.html /f

# Show GPOs for a specific user on a remote computer
gpresult /s DC01 /u corp\jsmith /r

# Force immediate policy refresh
gpupdate /force

# Refresh user policy only (no reboot)
gpupdate /target:user
```

## RSoP (Resultant Set of Policy)

```cmd
# RSoP wizard (GUI)
rsop.msc

# Full RSoP output to file
gpresult /z > C:\Temp\rsop-full.txt

# Check which GPO set a specific setting
gpresult /r /scope computer | findstr /i "password"
```

## GPO Backup and Restore

```powershell
# Backup all GPOs
Backup-GPO -All -Path "C:\GPOBackups"

# Backup a single GPO
Backup-GPO -Name "Security Baseline - Servers" -Path "C:\GPOBackups"

# Restore a GPO from backup
Restore-GPO -Name "Security Baseline - Servers" -Path "C:\GPOBackups"

# Import settings from backup into existing GPO
Import-GPO -BackupGpoName "Security Baseline - Servers" `
    -TargetName "Security Baseline - Servers" -Path "C:\GPOBackups"
```

## GPO Inheritance and Filtering

```powershell
# Block inheritance on an OU
Set-GPInheritance -Target "OU=Test,DC=corp,DC=example,DC=com" -IsBlocked Yes

# Enforce a GPO link (cannot be blocked by child OUs)
Set-GPLink -Name "Domain Security Policy" -Target "DC=corp,DC=example,DC=com" -Enforced Yes

# Apply GPO to a specific security group only
Set-GPPermission -Name "Desktop Lockscreen" -TargetName "Workstation Admins" `
    -TargetType Group -PermissionLevel GpoApply

# Remove Authenticated Users (for targeted group filtering)
Set-GPPermission -Name "Desktop Lockscreen" -TargetName "Authenticated Users" `
    -TargetType Group -PermissionLevel None
```
