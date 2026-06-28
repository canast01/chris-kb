---
tags:
  - networking
---
# SMB Share Permissions

<div class="kb-summary">
SMB Share Permissions reference covering Overview, Viewing and Setting Share Permissions, Creating Shares with net share, Combining NTFS and Share Permissions, PowerShell Share Creation and 1 more sections.
</div>

```d2
direction: down

viewing_and_setting_share_permission: "Viewing and Setting Share Permissions" {shape: rectangle}
creating_shares_with_net_share: "Creating Shares with net share" {shape: rectangle}
combining_ntfs_and_share_permissions: "Combining NTFS and Share Permissions" {shape: rectangle}
powershell_share_creation: "PowerShell Share Creation" {shape: rectangle}
auditing_share_permission_changes: "Auditing Share Permission Changes" {shape: rectangle}

viewing_and_setting_share_permission -> creating_shares_with_net_share: uses
creating_shares_with_net_share -> combining_ntfs_and_share_permissions: uses
combining_ntfs_and_share_permissions -> powershell_share_creation: uses
powershell_share_creation -> auditing_share_permission_changes: uses
```

## Overview

Share permissions are the first access gate for network clients connecting to an SMB share. They apply only to network access — local access bypasses them entirely. In practice, share permissions are often set to **Everyone: Full Control** and NTFS permissions handle actual access control. Effective permission for a network user is the most restrictive result of both layers combined.

| Share Permission | Allows |
|---|---|
| Full Control | Read, write, delete, change share-level permissions |
| Change | Read, write, delete files and subfolders |
| Read | View file names, read data, run programs |

## Viewing and Setting Share Permissions

```powershell
# List all shares and their paths
Get-SmbShare | Select-Object Name, Path, Description

# View share permissions for a specific share
Get-SmbShareAccess -Name "Finance"

# Grant Read access to a group
Grant-SmbShareAccess -Name "Finance" -AccountName "DOMAIN\Finance_Users" -AccessRight Read -Force

# Grant Full Control to admins
Grant-SmbShareAccess -Name "Finance" -AccountName "DOMAIN\Domain Admins" -AccessRight Full -Force

# Revoke access for a user
Revoke-SmbShareAccess -Name "Finance" -AccountName "DOMAIN\jsmith" -Force
```

## Creating Shares with net share

`net share` is the legacy but widely used command-line tool available on all Windows versions.

```bash
# Create a share with a description and permission
net share Finance=C:\Shares\Finance /GRANT:"DOMAIN\Finance_Users,CHANGE" /REMARK:"Finance dept files"

# Create a hidden share (trailing $ hides it from browse lists)
net share Finance$=C:\Shares\Finance /GRANT:"DOMAIN\Finance_Users,FULL"

# Remove a share
net share Finance /DELETE

# List all shares on the local server
net share
```

## Combining NTFS and Share Permissions

Effective access for a network user equals the intersection (most restrictive) of share and NTFS permissions.

```yaml
Effective = MIN(Share Permission, NTFS Permission)

Example A:
  Share:  Everyone = Read
  NTFS:   DOMAIN\jsmith = Modify
  Result: Read  (share is the bottleneck)

Example B:
  Share:  Everyone = Full Control
  NTFS:   DOMAIN\jsmith = Read
  Result: Read  (NTFS is the bottleneck)
```

Best practice: set share to **Everyone: Full Control**, then use NTFS permissions exclusively. This avoids confusing double-restriction calculations and simplifies troubleshooting.

## PowerShell Share Creation

```powershell
# Create share with granular access tiers
New-SmbShare -Name "Finance" `
             -Path "C:\Shares\Finance" `
             -Description "Finance department share" `
             -FullAccess "DOMAIN\Domain Admins" `
             -ChangeAccess "DOMAIN\Finance_Users" `
             -ReadAccess "DOMAIN\Finance_ReadOnly"

# Modify share properties after creation
Set-SmbShare -Name "Finance" -Description "Updated Finance share" -Force

# Limit concurrent connections
Set-SmbShare -Name "Finance" -ConcurrentUserLimit 50 -Force
```

## Auditing Share Permission Changes

```powershell
# Export all share permissions to CSV for documentation
Get-SmbShare | ForEach-Object {
    $share = $_
    Get-SmbShareAccess -Name $share.Name |
        Select-Object @{n='Share';e={$share.Name}}, AccountName, AccessControlType, AccessRight
} | Export-Csv -Path "C:\Audit\SharePermissions_$(Get-Date -f yyyyMMdd).csv" -NoTypeInformation

# Review share access events (Event ID 5140 = share accessed)
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=5140} -MaxEvents 50 |
    Select-Object TimeCreated, Message
```
