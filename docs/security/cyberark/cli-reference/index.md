# CyberArk CLI Reference

CyberArk's primary programmatic interface is the PVWA REST API (v2), which is the preferred method for automation and integration. The `psPAS` PowerShell module wraps the REST API with native PowerShell cmdlets, and the legacy PACLI command-line client provides direct Vault operations outside of PVWA.

**PVWA REST API (base: `https://<pvwa>/PasswordVault/api`)**

| Endpoint | Method | Purpose |
|---|---|---|
| `/auth/CyberArk/Logon` | POST | Authenticate and obtain session token |
| `/auth/Logoff` | POST | End session |
| `/accounts` | GET | List managed accounts |
| `/accounts/{id}/password/retrieve` | POST | Retrieve account password |
| `/accounts/{id}/change` | POST | Trigger immediate password rotation |
| `/safes` | GET | List all safes |
| `/safes/{safeName}/members` | GET | List safe members |
| `/recordings` | GET | List PSM session recordings |

**psPAS PowerShell Module**

| Cmdlet | Purpose |
|---|---|
| `New-PASSession` | Authenticate to PVWA |
| `Close-PASSession` | End session |
| `Get-PASAccount` | List or search accounts |
| `Get-PASSafe` | List safes |
| `Get-PASSafeMember` | List safe members |
| `Invoke-PASCPMOperation` | Trigger CPM rotation or verify |
| `Get-PASComponentSummary` | Health summary of all components |

**PACLI (Legacy CLI)**

| Command | Purpose |
|---|---|
| `PACLI INIT` | Initialise PACLI session |
| `PACLI LOGON` | Authenticate to Vault |
| `PACLI OPENFILE` | Open a safe |
| `PACLI RETRIEVEFILE` | Retrieve a credential file |
