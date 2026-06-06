# Windows Server — Access Control

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
```text
┌─────────────────────────────────── Windows Server — Access Control ───────────────────────────────────┐
│                                                                                                       │
│  Access control enforced through AD groups, NTFS ACLs, share permissions, and privileged access.      │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             AD Group-Based RBAC              │  │           NTFS & Share Permissions          │   │
│   │         Domain groups → resource ACL         │  │         NTFS ACE: Allow/Deny per SID        │   │
│   │        Domain Local groups for access        │  │        Share perms: max allowed users       │   │
│   │         Global groups for user sets          │  │          Effective = NTFS AND Share         │   │
│   │        Universal groups cross-domain         │  │         Inheritance: propagate down         │   │
│   │          Least privilege by default          │  │         icacls command for scripting        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  AD groups define who; NTFS ACLs define what access they get to which objects.                        │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Privileged Access Control           │  │          Protected Users & Tiering          │   │
│   │          PAW for Tier-0 admins only          │  │         Protected Users: no NTLM/DES        │   │
│   │      Admin accounts separate from user       │  │            Tier-0: DCs + PKI + AD           │   │
│   │          Time-bound access via PIM           │  │         Tier-1: servers and services        │   │
│   │         JEA: constrained PS sessions         │  │          Tier-2: workstations only          │   │
│   │          Local admin via LAPS only           │  │         No cross-tier admin allowed         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Physical or virtual server · domain controller · AD database on DC storage                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SID            = Security Identifier; unique identifier for every AD object and account              │
│  ACL            = Access Control List; ordered list of ACEs on a securable object                     │
│  ACE            = Access Control Entry; Allow or Deny rule for a specific SID                         │
│  NTFS ACL       = file/folder permissions enforced by NTFS file system kernel driver                  │
│  Share permission= network share access level; read/change/full — combined with NTFS                  │
│  Domain Local   = AD group scope; members from any domain; access in own domain                       │
│  Global group   = AD group scope; members from same domain; used across domains                       │
│  Universal group = AD group; members from any domain; replicated to global catalog                    │
│  PIM            = Privileged Identity Management; just-in-time admin role elevation                   │
│  PAW            = Privileged Access Workstation; hardened device for admin-only work                  │
│  Tiering        = AD admin tier model: Tier-0/1/2 separates admin account scope                       │
│  icacls         = Windows CLI tool to display and modify NTFS file/folder ACLs                        │
│  Protected Users= AD security group; blocks NTLM, unconstrained delegation, DES                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
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
```powershell
# User connects to the JEA endpoint — only sees permitted commands
Enter-PSSession -ComputerName webserver01 -ConfigurationName WebAdmins

# Test what a user can do in the session
Test-PSSessionConfigurationFile -Path "C:\JEA\WebAdmins.pssc"
```
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
