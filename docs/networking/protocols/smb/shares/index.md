---
tags:
  - networking
---
# SMB Shares

<div class="kb-summary">
SMB Shares reference covering Overview, Creating Shares with PowerShell, Creating Shares with net share, DFS Namespace Configuration, Share Enumeration and Auditing and 1 more sections.
</div>

```d2
direction: down

creating_shares_with_powershell: "Creating Shares with PowerShell" {shape: rectangle}
creating_shares_with_net_share: "Creating Shares with net share" {shape: rectangle}
dfs_namespace_configuration: "DFS Namespace Configuration" {shape: rectangle}
share_enumeration_and_auditing: "Share Enumeration and Auditing" {shape: rectangle}
share_properties_and_limits: "Share Properties and Limits" {shape: rectangle}

creating_shares_with_powershell -> creating_shares_with_net_share: uses
creating_shares_with_net_share -> dfs_namespace_configuration: uses
dfs_namespace_configuration -> share_enumeration_and_auditing: uses
share_enumeration_and_auditing -> share_properties_and_limits: uses
```

## Overview

SMB shares expose local filesystem paths to network clients. Shares can be created via Server Manager, PowerShell, or `net share`. DFS namespaces abstract share locations so clients do not need to know which server hosts a share. Hidden shares (trailing `$`) are not visible in browse lists but are fully accessible.

| Share Type | Example | Description |
|---|---|---|
| Standard | `\\server\Finance` | Visible in network browse |
| Hidden | `\\server\Finance$` | Not listed; accessed by direct path |
| Administrative | `C$`, `ADMIN$`, `IPC$` | Built-in, created automatically |
| DFS | `\\domain\Finance` | Namespace target; redirects to physical share |

## Creating Shares with PowerShell

```powershell
# Create a new share with tiered access
New-SmbShare -Name "Finance" `
             -Path "C:\Shares\Finance" `
             -Description "Finance department files" `
             -FullAccess "DOMAIN\Domain Admins" `
             -ChangeAccess "DOMAIN\Finance_Users" `
             -ReadAccess "DOMAIN\Auditors"

# List all shares
Get-SmbShare

# View a specific share
Get-SmbShare -Name "Finance"

# Remove a share (does not delete the folder)
Remove-SmbShare -Name "Finance" -Force
```

## Creating Shares with net share

```bash
# Create share
net share Finance=C:\Shares\Finance /REMARK:"Finance dept"

# Create hidden share
net share Finance$=C:\Shares\Finance

# Set access grants at creation time
net share Finance=C:\Shares\Finance /GRANT:"DOMAIN\Finance_Users,CHANGE" /GRANT:"DOMAIN\Domain Admins,FULL"

# Delete share
net share Finance /DELETE

# List all shares
net share
```

## DFS Namespace Configuration

DFS namespaces allow clients to access shares via a unified path regardless of which server hosts the data.

```powershell
# Install DFS Namespaces role
Install-WindowsFeature FS-DFS-Namespace, RSAT-DFS-Mgmt-Con

# Create a domain-based DFS namespace
New-DfsnRoot -Path "\\corp.example.com\Files" -TargetPath "\\fileserver01\Files" -Type DomainV2

# Add a folder (link) in the namespace
New-DfsnFolder -Path "\\corp.example.com\Files\Finance" -TargetPath "\\fileserver01\Finance"

# Add a second target for redundancy
New-DfsnFolderTarget -Path "\\corp.example.com\Files\Finance" -TargetPath "\\fileserver02\Finance"

# View all namespace folders
Get-DfsnFolder -Path "\\corp.example.com\Files\*"
```

## Share Enumeration and Auditing

```powershell
# List shares on a remote server
Get-SmbShare -CimSession "fileserver01"

# Export share list to CSV
Get-SmbShare | Select-Object Name, Path, Description, ConcurrentUserLimit |
    Export-Csv -Path "C:\Audit\Shares_$(Get-Date -f yyyyMMdd).csv" -NoTypeInformation

# Find shares with Everyone having access
Get-SmbShare | ForEach-Object {
    $name = $_.Name
    Get-SmbShareAccess -Name $name |
        Where-Object { $_.AccountName -eq "Everyone" } |
        Select-Object @{n='Share';e={$name}}, AccessRight
}
```

## Share Properties and Limits

```powershell
# Modify share description and connection limit
Set-SmbShare -Name "Finance" -Description "Finance Q2 archive" -ConcurrentUserLimit 200 -Force

# Enable access-based enumeration (users only see files they can access)
Set-SmbShare -Name "Finance" -FolderEnumerationMode AccessBased -Force

# Disable access-based enumeration
Set-SmbShare -Name "Finance" -FolderEnumerationMode Unrestricted -Force

# Check share caching setting (offline files)
Get-SmbShare -Name "Finance" | Select-Object CachingMode
# Options: None, Manual, Documents, Programs, BranchCache
Set-SmbShare -Name "Finance" -CachingMode None -Force
```
