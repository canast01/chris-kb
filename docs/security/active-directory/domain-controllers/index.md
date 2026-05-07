# Domain Controllers

Domain Controllers host the AD DS database (ntds.dit), authenticate users, and hold FSMO roles. Understanding DC roles and how to manage them is essential for AD operations.

## FSMO Roles

Five Flexible Single Master Operations roles exist across forest and domain levels. Only one DC holds each role at a time.

| Role | Scope | Function |
|---|---|---|
| Schema Master | Forest | Controls AD schema changes |
| Domain Naming Master | Forest | Adds/removes domains in the forest |
| PDC Emulator | Domain | Password sync, time authority, legacy client support |
| RID Master | Domain | Allocates RID pools to DCs for new object SIDs |
| Infrastructure Master | Domain | Resolves cross-domain object references |

```cmd
# Show all FSMO role holders
netdom query fsmo

# Show via PowerShell
Get-ADDomain | Select-Object PDCEmulator, RIDMaster, InfrastructureMaster
Get-ADForest | Select-Object SchemaMaster, DomainNamingMaster
```

## Promoting a New DC

```powershell
# Install AD DS role
Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools

# Promote as additional DC in existing domain
Import-Module ADDSDeployment
Install-ADDSDomainController `
    -DomainName "corp.example.com" `
    -InstallDns:$true `
    -Credential (Get-Credential) `
    -SafeModeAdministratorPassword (ConvertTo-SecureString "P@ssw0rd!" -AsPlainText -Force) `
    -Force:$true
```

## Demoting a DC

```powershell
# Graceful demotion
Uninstall-ADDSDomainController `
    -LocalAdministratorPassword (ConvertTo-SecureString "P@ssw0rd!" -AsPlainText -Force) `
    -Force:$true

# Metadata cleanup if DC is already offline
ntdsutil
  metadata cleanup
  remove selected server CN=DC02,CN=Servers,CN=Default-First-Site,CN=Sites,CN=Configuration,DC=corp,DC=example,DC=com
```

## Transferring and Seizing FSMO Roles

```powershell
# Transfer PDC Emulator gracefully
Move-ADDirectoryServerOperationMasterRole -Identity "DC02" -OperationMasterRole PDCEmulator

# Transfer multiple roles
Move-ADDirectoryServerOperationMasterRole -Identity "DC02" `
    -OperationMasterRole PDCEmulator,RIDMaster,InfrastructureMaster

# Seize a role (only if original holder is permanently offline)
ntdsutil
  roles
  connections
    connect to server DC02
  quit
  seize pdc
```

## DC Health Validation

```cmd
# Run all dcdiag tests
dcdiag /test:all /v

# Check replication health
repadmin /showrepl

# Check DC services
sc query NTDS
sc query Netlogon
sc query W32Time
sc query DFSR

# Verify AD database integrity
ntdsutil "activate instance ntds" "files" "integrity" quit quit
```

## Time Synchronisation

The PDC Emulator is the authoritative time source for the domain. All other DCs and clients sync from the hierarchy.

```cmd
# Check current time source
w32tm /query /source

# Force resync
w32tm /resync /force

# Configure PDC Emulator to sync from external NTP
w32tm /config /manualpeerlist:"pool.ntp.org" /syncfromflags:manual /reliable:YES /update

# Check time skew across DCs
w32tm /monitor /computers:dc01,dc02,dc03
```
