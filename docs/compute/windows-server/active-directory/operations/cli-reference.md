---
tags:
  - operations
  - windows
description: "Active Directory management uses native tools (repadmin, dcdiag, nltest, netdom, dsquery) and the ActiveDirectory PowerShell module. All commands assume..."
---
# Active Directory CLI Reference

<div class="kb-summary">
Active Directory management uses native tools (`repadmin`, `dcdiag`, `nltest`, `netdom`, `dsquery`) and the ActiveDirectory PowerShell module. All commands assume RSAT-AD-PowerShell is installed or the command is run on a Domain Controller.

*Applies to: Windows Server 2019 / 2022*
</div>
![Active Directory CLI Reference](../../../../assets/compute-windows-server-active-directory-operations-cli-refer.svg)

## Before you begin

- **Access:** Local Administrator or Domain Admin on target hosts
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Replication Health Triage Flow

```d2
direction: right

issue: "Suspected replication issue" {shape: rectangle}
replSummary: "repadmin /replsummary\n(high-level success/failure" {shape: rectangle}
errorsFound: "Errors\nfound?" {shape: rectangle}
showRepl: "repadmin /showrepl *\n(identify failing partner" {shape: rectangle}
done: "Replication healthy" {shape: rectangle}
errorCode: "Error code" {shape: rectangle}
checkFw: "Check firewall / DNS\nbetween DCs" {shape: rectangle}
checkPerms: "Check replication\npermissions on NC head" {shape: rectangle}
checkTombstone: "DC offline too long\nCheck tombstone lifetime" {shape: rectangle}
checkTime: "Check time skew\nw32tm /stripchart" {shape: rectangle}
forceSync: "repadmin /syncall /AdeP\n(force full sync after fix" {shape: rectangle}
dcdiag: "dcdiag /test:replications /v" {shape: rectangle}

issue -> replSummary
replSummary -> errorsFound
errorsFound -> showRepl
errorsFound -> done
showRepl -> errorCode
errorCode -> checkFw
errorCode -> checkPerms
errorCode -> checkTombstone
errorCode -> checkTime
checkFw -> forceSync
checkPerms -> forceSync
checkTombstone -> dcdiag
checkTime -> forceSync
```

---

## Replication Health

Replication issues cause authentication failures and stale data. Check replication before and after any DC change.

```bash
# High-level replication health across all DCs
repadmin /replsummary

# Show replication partners and last sync time for a DC
repadmin /showrepl <DC_name>

# Show replication failures only
repadmin /showrepl * /errorsonly

# Force replication from all partners
repadmin /syncall /AdeP

# Check replication queue
repadmin /queue
```


```text title="Expected output"
Replication Summary Start Time: 2024-01-15 14:32:18
Beginning data collection for replication summary, this may take awhile on large enterprises with many servers...
Source DSA          largest delta    fails/total    %-healthy
DC1.corp.local      3m:22s           0/12           100%
DC2.corp.local      5m:18s           0/12           100%
DC3.corp.local      2m:47s           0/12           100%
DC4.corp.local      12m:05s          1/12           91%
...
Replication Latency Summary
Site                 ReplLatency(secs)
Default-First-Site  45
Branch-Site-01      187
Branch-Site-02      312

DSA Options: IS_GC IS_RODC
Naming Context: CN=Configuration,DC=corp,DC=local
    DC1.corp.local via RPC
        Last attempt @ 2024-01-15 14:28:33 was successful.
    DC2.corp.local via RPC
        Last attempt @ 2024-01-15 14:29:15 was successful.
    DC3.corp.local via RPC
        Last attempt @ 2024-01-15 14:27:52 was successful.

Source DSA: DC4.corp.local
    CN=Configuration,DC=corp,DC=local
        DC1.corp.local via RPC
            Last attempt @ 2024-01-15 14:15:22 failed, result 8606 (DSA is unavailable).
        DC2.corp.local via RPC
            Last attempt @ 2024-01-15 14:20:44 was successful.

SyncAll has started; please wait for completion...
Syncing all NC's held on DC1.corp.local
Syncing all NC's held on DC2.corp.local
Syncing all NC's held on DC3.corp.local
Syncing all NC's held on DC4.corp.local
SyncAll terminated with success.

Replication Queue
    DC1.corp.local: 0 pending
    DC2.corp.local: 0 pending
    DC3.corp.local: 0 pending
    DC4.corp.local: 3 pending
```

!!! warning "Common errors"
    **`DsReplicaGetInfo() failed with status 8606 (DSA is unavailable).`** — Verify the DC is online and reachable on the network; check firewall rules for RPC ports 135, 445, and 49152-65535.
    **`The naming context is invalid`** — Ensure the DC name is spelled correctly and exists in Active Directory; use `Get-ADDomainController` to list valid DC names.
    **`Replication access was denied`** — Verify the account running repadmin has Domain Admin or Enterprise Admin credentials; run the command as Administrator.
---

## DC Diagnostics

```bash
# Full verbose DC diagnostic
dcdiag /v

# Replication-only test
dcdiag /test:replications

# DNS diagnostic
dcdiag /test:dns /v

# Run all tests on a remote DC
dcdiag /s:<DC_name> /v

# Locate a DC for a domain
nltest /dsgetdc:<domain_name>

# Verify secure channel to domain
nltest /sc_verify:<domain_name>

# Reset secure channel
nltest /sc_reset:<domain_name>
```


```text title="Expected output"
Directory Server Diagnosis

Performing initial setup:
   Trying to find home server...
   Home Server = DC01.contoso.com
   Identified AD Forest.
   Trying to contact a DC in the domain...
   DC contacted. Retrieving FSMO roles
   Forest Role Owner = DC01.contoso.com
   Domain Role Owner = DC01.contoso.com
   PDC Role Owner = DC01.contoso.com
   RID Role Owner = DC01.contoso.com
   Infrastructure Role Owner = DC01.contoso.com

   Doing initial required tests

      Testing server: Default-First-Site-Name\DC01
      Starting test: Connectivity
         ......................... DC01 passed test Connectivity

      Starting test: Advertising
         ......................... DC01 passed test Advertising

      Starting test: MachineAccount
         ......................... DC01 passed test MachineAccount

      Starting test: Services
         ......................... DC01 passed test Services

      Starting test: FsmoCheck
         ......................... DC01 passed test FsmoCheck

      Starting test: Replications
         ......................... DC01 passed test Replications

      Starting test: DFSREvent
         ......................... DC01 passed test DFSREvent

      Starting test: DNS
         ......................... DC01 passed test DNS

   Running enterprise tests on : contoso.com

      Starting test: CheckSDRefDom
         ......................... contoso.com passed test CheckSDRefDom

      Starting test: CrossRefValidation
         ......................... contoso.com passed test CrossRefValidation

   Passed test ExecutionContext
```

!!! warning "Common errors"
    **`'dcdiag' is not recognized as an internal or external command`** — Run dcdiag from a Windows command prompt or PowerShell on a domain-joined Windows Server with AD DS tools installed, not from a Linux/Unix bash shell.
    **`The specified domain does not exist or could not be contacted`** — Verify the domain name is correct and the DC has network connectivity to DNS and domain controllers using `nslookup <domain_name>`.
    **`Access Denied`** — Run the command with elevated privileges (Run as Administrator) or ensure the user account has sufficient AD permissions.
---

## FSMO Roles

```bash
# List all FSMO role holders
netdom query fsmo

# Transfer PDC emulator role (PowerShell)
Move-ADDirectoryServerOperationMasterRole -Identity <target_dc> -OperationMasterRole PDCEmulator

# Seize a role (only if holder is permanently offline)
Move-ADDirectoryServerOperationMasterRole -Identity <target_dc> -OperationMasterRole PDCEmulator -Force
```


```text title="Expected output"
Schema Master               : dc1.corp.local
Domain Naming Master        : dc1.corp.local
PDC Emulator                : dc1.corp.local
RID Master                  : dc2.corp.local
Infrastructure Master       : dc2.corp.local

WARNING: Transferring the PDC Emulator role to DC2.CORP.LOCAL...
The operation completed successfully.

WARNING: Seizing the PDC Emulator role to DC3.CORP.LOCAL...
The operation completed successfully.
```

!!! warning "Common errors"
    **`Move-ADDirectoryServerOperationMasterRole : Cannot find a domain controller for domain "corp.local".`** — Verify network connectivity to the target DC and ensure the domain name is correct.
    **`Access Denied. The user does not have permission to perform this operation.`** — Run PowerShell as Domain Admin or Enterprise Admin and ensure the account has sufficient AD permissions.
    **`The operation cannot be performed because the object referenced could not be found.`** — Confirm the target DC name exists in Active Directory using `Get-ADDomainController -Filter *`.
---

## Users & Groups

```powershell
# List all users with password metadata
Get-ADUser -Filter * -Properties PasswordLastSet, PasswordExpired, LastLogonDate |
  Select SamAccountName, PasswordLastSet, PasswordExpired, LastLogonDate

# Find users inactive for 90+ days
$cutoff = (Get-Date).AddDays(-90)
Get-ADUser -Filter {LastLogonDate -lt $cutoff} -Properties LastLogonDate

# Find disabled accounts
Get-ADUser -Filter {Enabled -eq $false}

# Find users with passwords set to never expire
Get-ADUser -Filter {PasswordNeverExpires -eq $true} -Properties PasswordNeverExpires

# List members of a group
Get-ADGroupMember -Identity "<group_name>" -Recursive

# List all groups in an OU
Get-ADGroup -Filter * -SearchBase "OU=<ou>,DC=<domain>,DC=<tld>"
```

---

## Computers

```powershell
# List all computers with last logon
Get-ADComputer -Filter * -Properties LastLogonDate |
  Select Name, LastLogonDate | Sort-Object LastLogonDate -Descending

# Find stale computer accounts (90+ days)
$cutoff = (Get-Date).AddDays(-90)
Get-ADComputer -Filter {LastLogonDate -lt $cutoff} -Properties LastLogonDate

# Test and repair machine secure channel
Test-ComputerSecureChannel -Repair

# Check if a computer is joined to the domain
(Get-WmiObject Win32_ComputerSystem).PartOfDomain
```

---

## Domain Controllers

```powershell
# List all DCs in the domain
Get-ADDomainController -Filter * | Select Name, Site, IPv4Address, IsGlobalCatalog

# Show replication failures across the forest
Get-ADReplicationFailure -Scope Forest

# Check AD services on a DC
Get-Service adws, kdc, netlogon, dns | Select Name, Status
```

---

## Trusts

```bash
# List domain trusts
netdom trust <domain> /verify

# List all trusts via PowerShell
Get-ADTrust -Filter * | Select Name, TrustType, Direction, TrustAttributes
```


```text title="Expected output"
The command completed successfully.
Verifying trust for domain: corp.example.com

Trust Name: corp.example.com
Trust Type: DOWNLEVEL
Direction: BIDIRECTIONAL
Status: OK

Name                          TrustType Direction TrustAttributes
----                          --------- --------- ---------------
child.corp.example.com        UPLEVEL   INBOUND   TRANSITIVE
partner.external.com          EXTERNAL  OUTBOUND  NONTRANSITIVE
legacy.local                  DOWNLEVEL BIDIRECTIONAL TRANSITIVE
forest.trusted.net            FOREST    BIDIRECTIONAL TRANSITIVE
vendor-realm.com              REALM     OUTBOUND  NONTRANSITIVE
```

!!! warning "Common errors"
    **`The specified domain could not be found.`** — Verify the domain name spelling and ensure the domain controller is reachable via DNS.
    **`Access Denied`** — Run PowerShell as Administrator or ensure your user account has Domain Admin privileges.
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Active Directory — Procedures](../procedures/)
- [Active Directory — Scripts](../scripts/)
- [Active Directory — Health Checks](../health-checks/)
