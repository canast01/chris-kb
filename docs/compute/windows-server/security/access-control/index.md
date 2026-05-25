# Windows Server — Access Control

AD group design, GPO user rights, Just Enough Administration (JEA), LAPS, and built-in group review.

```text
┌────────────────────────────────────────────────────────┐
│           Windows Access Control Model (AGDLP)         │
└────────────────────────────────────────────────────────┘
  User Account (A)
       │
       ▼
  Global Group (G)  ──  "GG-ServerAdmins"
       │
       ▼
  Domain Local Group (DL) ── "DL-FileShare-Finance-RW"
       │
       ▼
  ┌────────────────────────────────────────────────────┐
  │  Resource Permissions (P)                         │
  ├──────────────────┬────────────────────────────────┤
  │  Share Perms     │  NTFS ACL                      │
  │  (Full/Read/No)  │  (Allow/Deny + Inheritance)    │
  └──────────────────┴────────────────────────────────┘
       │
       ▼
  GPO User Rights ──► who can log on, debug, backup
  JEA endpoint ──► constrained PS session per role
```

## Active Directory Group Design

Structure groups using the AGDLP (Accounts → Global → Domain Local → Permissions) model to maintain role-based access control.

| Layer | Type | Purpose |
|---|---|---|
| A — Accounts | User/computer objects | Individual identities |
| G — Global Group | Global security group | Collect users by role/department |
| DL — Domain Local Group | Domain local security group | Assigned to resources in one domain |
| P — Permissions | ACL entry | Access to file share, GPO, object |

```powershell
# Create a Global group for a role
New-ADGroup -Name "GG-ServerAdmins" -GroupScope Global -GroupCategory Security `
  -Path "OU=Groups,DC=corp,DC=local" -Description "Server Administrators"

# Create a Domain Local group for the resource
New-ADGroup -Name "DL-FileShare-FinanceData-RW" -GroupScope DomainLocal -GroupCategory Security `
  -Path "OU=Groups,DC=corp,DC=local"

# Add the Global group to the Domain Local group
Add-ADGroupMember -Identity "DL-FileShare-FinanceData-RW" -Members "GG-ServerAdmins"

# Add a user to the Global group
Add-ADGroupMember -Identity "GG-ServerAdmins" -Members "jsmith"

# View group members
Get-ADGroupMember -Identity "GG-ServerAdmins" | Select-Object Name, SamAccountName, objectClass
```

## GPO — User Rights Assignments

User Rights are configured via GPO: Computer Configuration > Windows Settings > Security Settings > Local Policies > User Rights Assignment.

### Critical User Rights

| User Right | Setting | Rationale |
|---|---|---|
| Access this computer from the network | Authenticated Users, Administrators | Baseline access |
| Allow log on locally | Administrators, specific groups only | Block interactive logon on servers |
| Allow log on through Remote Desktop Services | Remote Desktop Users group | Control RDP access |
| Deny log on locally | Guests, service accounts | Prevent misuse |
| Deny access to this computer from the network | Guests | Prevent network access |
| Act as part of the operating system | (Empty) | No accounts should have this |
| Debug programs | (Empty) | Remove from Administrators |
| Back up files and directories | Backup Operators only | Limit who can bypass ACLs |
| Manage auditing and security log | Administrators only | Protect audit log |
| Shut down the system | Administrators only | Server-specific restriction |

```powershell
# Review current local user rights (use secedit)
secedit /export /cfg C:\temp\security-policy.cfg
Get-Content C:\temp\security-policy.cfg | Select-String "SeRemote|SeInteractive|SeNetwork|SeDeny"
```

### Apply User Rights via GPO (PowerShell DSC reference)

```powershell
# Query user right assignment directly
(Get-LocalUser).Name
# For domain-aware rights, query via GPO result:
gpresult /H C:\temp\gpo-report.html /F
```

## Just Enough Administration (JEA)

JEA limits what administrators can do in remote PowerShell sessions to only the commands and parameters they need.

### Create a Role Capability File

```powershell
# Generate the role capability template
New-PSRoleCapabilityFile -Path "C:\JEA\RoleCapabilities\WebAdmins.psrc"
```

```powershell
# C:\JEA\RoleCapabilities\WebAdmins.psrc
@{
    GUID                    = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
    Author                  = 'Corp IT'
    Description             = 'Web server administration role'
    ModulesToImport         = @('WebAdministration')

    VisibleCmdlets          = @(
        'Get-Service',
        @{Name='Restart-Service'; Parameters=@{Name='Name'; ValidateSet='IIS','W3SVC'}}
    )
    VisibleFunctions        = @()
    VisibleExternalCommands = @()
    VisibleProviders        = @()
}
```

### Create a Session Configuration File

```powershell
New-PSSessionConfigurationFile -Path "C:\JEA\WebAdmins.pssc" `
  -SessionType RestrictedRemoteServer `
  -RunAsVirtualAccount `
  -TranscriptDirectory "C:\JEA\Transcripts\" `
  -RoleDefinitions @{
    'CORP\WebAdmins' = @{ RoleCapabilityFiles = 'C:\JEA\RoleCapabilities\WebAdmins.psrc' }
  }

# Register the session configuration
Register-PSSessionConfiguration -Name "WebAdmins" -Path "C:\JEA\WebAdmins.pssc" -Force
Restart-Service WinRM

# Verify
Get-PSSessionConfiguration -Name "WebAdmins"
```

### Connect via JEA

```powershell
# User connects to the JEA endpoint — only sees permitted commands
Enter-PSSession -ComputerName webserver01 -ConfigurationName WebAdmins

# Test what a user can do in the session
Test-PSSessionConfigurationFile -Path "C:\JEA\WebAdmins.pssc"
```

## Built-in Group Review

Built-in privileged groups should contain only required accounts. Review regularly.

```powershell
# Audit Domain Admins
Get-ADGroupMember "Domain Admins" -Recursive | Select-Object Name, SamAccountName, objectClass

# Audit Administrators (local built-in)
Get-ADGroupMember "Administrators" | Select-Object Name

# Audit Schema Admins (should be empty when not in use)
Get-ADGroupMember "Schema Admins" | Select-Object Name, SamAccountName

# Audit Enterprise Admins
Get-ADGroupMember "Enterprise Admins" | Select-Object Name, SamAccountName

# Audit Server Operators (can manage services and files)
Get-ADGroupMember "Server Operators" | Select-Object Name, SamAccountName

# Audit Backup Operators (can bypass ACLs)
Get-ADGroupMember "Backup Operators" | Select-Object Name, SamAccountName
```

```powershell
# Comprehensive privileged group report
$privilegedGroups = @("Domain Admins","Enterprise Admins","Schema Admins",
  "Administrators","Account Operators","Backup Operators","Server Operators","Print Operators")

foreach ($group in $privilegedGroups) {
    $members = Get-ADGroupMember -Identity $group -Recursive -ErrorAction SilentlyContinue
    if ($members) {
        Write-Host "`n=== $group ===" -ForegroundColor Yellow
        $members | Select-Object Name, SamAccountName, objectClass | Format-Table
    }
}
```

## File and Share Permissions

### NTFS Permissions

```powershell
# View NTFS permissions on a folder
(Get-Acl "C:\Data\Finance").Access | Format-Table IdentityReference, FileSystemRights, AccessControlType, IsInherited

# Grant a group read access
$acl = Get-Acl "C:\Data\Finance"
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule(
    "CORP\FinanceReaders", "Read", "ContainerInherit,ObjectInherit", "None", "Allow")
$acl.AddAccessRule($rule)
Set-Acl "C:\Data\Finance" $acl

# Remove all inherited permissions and set explicit (break inheritance)
$acl = Get-Acl "C:\Data\Sensitive"
$acl.SetAccessRuleProtection($true, $false)   # isProtected=true, preserveInheritance=false
Set-Acl "C:\Data\Sensitive" $acl
```

### Share Permissions

```powershell
# Create a share with restricted access
New-SmbShare -Name "Finance" -Path "C:\Data\Finance" `
  -FullAccess "CORP\FinanceAdmins" `
  -ReadAccess "CORP\FinanceReaders" `
  -NoAccess "Everyone"

# View current share permissions
Get-SmbShareAccess -Name "Finance"

# Revoke Everyone from a share
Revoke-SmbShareAccess -Name "Finance" -AccountName "Everyone" -Force

# Best practice: Share = Full Control to Authenticated Users, restrict at NTFS level
```

## Local Administrator Control

```powershell
# Disable the built-in Administrator account (use LAPS-managed account instead)
Disable-LocalUser -Name "Administrator"

# Rename the built-in Administrator (via GPO or locally)
Rename-LocalUser -Name "Administrator" -NewName "CorpAdmin"

# Rename the Guest account and disable it
Rename-LocalUser -Name "Guest" -NewName "CorpGuest"
Disable-LocalUser -Name "CorpGuest"

# View local group members (Administrators)
Get-LocalGroupMember -Group "Administrators"

# Remove domain user from local Administrators (clean up)
Remove-LocalGroupMember -Group "Administrators" -Member "CORP\jsmith"
```

## Delegation in Active Directory

```powershell
# Grant a helpdesk group permission to reset passwords in an OU
# Use the Delegation of Control Wizard in ADUC, or via dsacls:
dsacls "OU=Users,DC=corp,DC=local" /G "CORP\Helpdesk:CA;Reset Password;user"
dsacls "OU=Users,DC=corp,DC=local" /G "CORP\Helpdesk:CA;Change Password;user"

# View current delegation on an OU
dsacls "OU=Users,DC=corp,DC=local"

# View ACL via PowerShell
(Get-Acl "AD:\OU=Users,DC=corp,DC=local").Access |
  Where-Object {$_.IdentityReference -like "*Helpdesk*"} |
  Select-Object IdentityReference, ActiveDirectoryRights
```

## Access Control Audit

```powershell
# Find all accounts with AdminCount=1 (ever been in a protected group)
Get-ADUser -Filter {AdminCount -eq 1} -Properties AdminCount |
  Select-Object Name, SamAccountName, Enabled | Sort-Object Enabled

# Find stale admin accounts (no logon in 90 days)
$cutoff = (Get-Date).AddDays(-90)
Get-ADUser -Filter {AdminCount -eq 1 -and LastLogonDate -lt $cutoff} `
  -Properties LastLogonDate, AdminCount |
  Select-Object Name, SamAccountName, LastLogonDate, Enabled

# Find service accounts with Domain Admin membership
Get-ADGroupMember "Domain Admins" -Recursive |
  Where-Object {$_.SamAccountName -like "svc-*" -or $_.SamAccountName -like "sa_*"}

# Accounts with password set to never expire (flag service accounts only)
Get-ADUser -Filter {PasswordNeverExpires -eq $true -and Enabled -eq $true} `
  -Properties PasswordNeverExpires, Description |
  Select-Object Name, SamAccountName, Description
```

## Quick Reference

| Topic | Tool / Command |
|---|---|
| Group membership | `Get-ADGroupMember -Identity "Group" -Recursive` |
| User rights export | `secedit /export /cfg policy.cfg` |
| GPO result | `gpresult /H report.html /F` |
| JEA session register | `Register-PSSessionConfiguration` |
| NTFS ACL view | `(Get-Acl path).Access` |
| Share permissions | `Get-SmbShareAccess -Name "ShareName"` |
| Local admins | `Get-LocalGroupMember -Group "Administrators"` |
| AdminCount=1 accounts | `Get-ADUser -Filter {AdminCount -eq 1}` |
| Delegation audit | `dsacls "OU=...,DC=corp,DC=local"` |
