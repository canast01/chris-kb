# Active Directory CLI Reference

Active Directory management spans native command-line tools (`repadmin`, `dcdiag`, `nltest`, `netdom`, `dsquery`, `dsget`) and the ActiveDirectory PowerShell module, which is the preferred interface for automation and scripting. All commands below assume the RSAT-AD-PowerShell feature is installed or the command is run on a Domain Controller.

| Command | Purpose |
|---|---|
| `repadmin /replsummary` | High-level replication health across all DCs |
| `repadmin /showrepl <DC>` | Full replication partner detail for a specific DC |
| `dcdiag /v` | Verbose DC diagnostic across all tests |
| `dcdiag /test:replications` | Replication-only diagnostic |
| `nltest /dsgetdc:<domain>` | Locate a DC for the specified domain |
| `nltest /sc_verify:<domain>` | Verify secure channel to domain |
| `netdom query fsmo` | List all FSMO role holders |
| `netdom trust <domain> /verify` | Verify trust relationship |
| `dsquery user -inactive 4` | Find users inactive for 4+ weeks |
| `dsget group "CN=..." -members` | List group members |
| `Get-ADUser -Filter * -Properties PasswordLastSet` | Query all users with password metadata |
| `Get-ADGroup -Filter * -SearchBase "OU=..."` | List groups in an OU |
| `Get-ADComputer -Filter * -Properties LastLogonDate` | List computers with last logon |
| `Get-ADReplicationFailure -Scope Forest` | Forest-wide replication failures |
| `Get-ADDomainController -Filter *` | List all DCs in the domain |
| `Test-ComputerSecureChannel -Repair` | Test and repair machine secure channel |
