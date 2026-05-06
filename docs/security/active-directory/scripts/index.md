# Active Directory Scripts

The scripts below are PowerShell automation tools for routine Active Directory health and audit tasks. Each script should be run from a host with the ActiveDirectory PowerShell module installed, using an account with at minimum Read access to the domain (audit scripts) or Domain Admin rights (replication and GPO tasks).

| Script | Purpose |
|---|---|
| `Get-DCReplicationHealth.ps1` | Runs `Get-ADReplicationFailure -Scope Forest` and outputs a formatted report of all replication errors with DC name, partner, and failure count |
| `Find-AccountLockoutSource.ps1` | Queries Security event logs (4740) across all DCs to identify the originating machine for a locked-out account |
| `Get-StaleComputerAccounts.ps1` | Reports computer accounts where `LastLogonDate` is older than 90 days and `Enabled -eq $true` |
| `Get-GroupMembershipAudit.ps1` | Exports all members of specified privileged groups (Domain Admins, Schema Admins, Enterprise Admins) to CSV |
| `Get-ExpiringPasswords.ps1` | Reports users whose passwords expire within 14 days, filtered by OU scope |
| `Backup-AllGPOs.ps1` | Uses `Backup-GPO -All -Path <path>` to export all GPOs to a timestamped folder; intended for pre-change and scheduled weekly backups |
