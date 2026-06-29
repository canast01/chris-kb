---
tags:
  - operations
  - security
---
# CyberArk CLI Reference

<div class="kb-summary">
CyberArk's primary programmatic interface is the PVWA REST API v2. The `psPAS` PowerShell module wraps the REST API with native cmdlets. The legacy PACLI client provides direct Vault operations outside of PVWA.

*Applies to: CyberArk PAM*
</div>

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## API Interface Hierarchy

```d2
direction: right

operator: "Operator / Script\n(automation or admin" {shape: rectangle}
psPAS: "psPAS Module\n(REST wrapper" {shape: rectangle}
restAPI: "PVWA REST API v2\nhttps://pvwa/PasswordVault/api" {shape: rectangle}
pacli: "PACLI\n(legacy Vault CLI" {shape: rectangle}
pvwa: "PVWA\n(IIS application" {shape: rectangle}
vault: "Digital Vault" {shape: rectangle}

operator -> psPAS
operator -> restAPI
operator -> pacli
psPAS -> restAPI
restAPI -> pvwa
pvwa -> vault
pacli -> vault
```

---

## REST API — Authentication

The PVWA REST API base URL is `https://<pvwa>/PasswordVault/api`. Always end sessions with a Logoff call.

```bash
# Authenticate with CyberArk auth
curl -X POST https://<pvwa>/PasswordVault/api/auth/CyberArk/Logon   -H "Content-Type: application/json"   -d '{"username":"admin","password":"<pass>"}'

# Authenticate with LDAP
curl -X POST https://<pvwa>/PasswordVault/api/auth/LDAP/Logon   -H "Content-Type: application/json"   -d '{"username":"admin","password":"<pass>"}'

# Logoff
curl -X POST https://<pvwa>/PasswordVault/api/auth/Logoff   -H "Authorization: <token>"
```


```text title="Expected output"
{"CyberArkLogonResult":"eyJQVldhVXNlcklkIjoiMzAiLCJVc2VyTmFtZSI6ImFkbWluIiwiU2Vzc2lvbklkIjoiNDU2YzBkZTUtNzc5Yi00ZjA5LWI4YTItOWQzYzFlZmY2YzM1IiwiUGFzc1dvcmRDaGFuZ2VJbmRleCI6IjAiLCJSZW1haW5pbmdBdHRlbXB0cyI6IjMiLCJOZXdQYXNzd29yZFRpbWUiOiIwIn0="}
{"CyberArkLogonResult":"eyJQVldhVXNlcklkIjoiMzAiLCJVc2VyTmFtZSI6ImFkbWluIiwiU2Vzc2lvbklkIjoiOGE5ZjEyMzQtYzU2Ni00YzAxLWE5ZDItZjc4YmU0YzJhMzQ1IiwiUGFzc1dvcmRDaGFuZ2VJbmRleCI6IjAiLCJSZW1haW5pbmdBdHRlbXB0cyI6IjMiLCJOZXdQYXNzd29yZFRpbWUiOiIwIn0="}
(no output — command completes silently)
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command to skip SSL verification, or install the PVWA's CA certificate in your system trust store.
    **`{"Errors":["Logon failed"]}`** — Verify the username and password are correct and the user account is not locked or disabled in CyberArk.
    **`curl: (7) Failed to connect to <pvwa>: Name or service not known`** — Confirm the PVWA hostname or IP address is correct and reachable from your network.
---

## REST API — Accounts

```bash
# List managed accounts
curl -X GET "https://<pvwa>/PasswordVault/api/accounts?limit=100"   -H "Authorization: <token>"

# Search accounts by username
curl -X GET "https://<pvwa>/PasswordVault/api/accounts?search=svc_oracle"   -H "Authorization: <token>"

# Retrieve an account password (CPM must allow retrieval)
curl -X POST "https://<pvwa>/PasswordVault/api/accounts/<id>/password/retrieve"   -H "Authorization: <token>"   -H "Content-Type: application/json"   -d '{"reason":"maintenance","TicketingSystemName":"","TicketId":""}'

# Trigger immediate password rotation
curl -X POST "https://<pvwa>/PasswordVault/api/accounts/<id>/change"   -H "Authorization: <token>"

# Verify current password
curl -X POST "https://<pvwa>/PasswordVault/api/accounts/<id>/verify"   -H "Authorization: <token>"
```


```text title="Expected output"
{
  "accounts": [
    {
      "id": "42_10",
      "name": "root@db-prod-01",
      "address": "192.168.45.12",
      "username": "root",
      "platformId": "Unix",
      "safeName": "Prod-Database"
    },
    {
      "id": "43_11",
      "name": "svc_oracle@db-prod-02",
      "address": "192.168.45.13",
      "username": "svc_oracle",
      "platformId": "Oracle",
      "safeName": "Prod-Database"
    },
    {
      "id": "44_12",
      "name": "admin@app-server-01",
      "address": "10.50.20.8",
      "username": "admin",
      "platformId": "Windows",
      "safeName": "Prod-Apps"
    }
  ],
  "count": 87
}

{
  "accounts": [
    {
      "id": "43_11",
      "name": "svc_oracle@db-prod-02",
      "address": "192.168.45.13",
      "username": "svc_oracle",
      "platformId": "Oracle"
    }
  ]
}

{
  "password": "K9#mP2$xL7vQw4nR8tY"
}

{
  "success": true,
  "taskId": "TASK-2024-0847-5f3a",
  "message": "Password change initiated"
}

{
  "isSuccessful": true,
  "verificationTime": "2024-01-15T14:32:18Z"
}
```

!!! warning "Common errors"
    **`"ErrorCode":"PASWS002E","ErrorMessage":"Invalid token or token expired"`** — Regenerate the authentication token using the login endpoint and update the Authorization header.
    **`"ErrorCode":"PASWS040E","ErrorMessage":"User does not have permission to retrieve password"`** — Verify the user has the "Retrieve Password" permission in the Safe policy for the target account.
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to bypass SSL verification in non-production environments, or import the PVWA certificate into your CA bundle.
---

## REST API — Safes

```bash
# List all safes
curl -X GET "https://<pvwa>/PasswordVault/api/safes"   -H "Authorization: <token>"

# Get safe details
curl -X GET "https://<pvwa>/PasswordVault/api/safes/<safe_name>"   -H "Authorization: <token>"

# List safe members
curl -X GET "https://<pvwa>/PasswordVault/api/safes/<safe_name>/members"   -H "Authorization: <token>"
```


```text title="Expected output"
[
  {
    "SafeUrlId": "safe_prod_db",
    "SafeName": "PROD-DB-Credentials",
    "Description": "Production database credentials",
    "Location": "\\Safes\\Production",
    "CreationTime": 1672531200
  },
  {
    "SafeUrlId": "safe_app_keys",
    "SafeName": "APP-API-Keys",
    "Description": "Application API keys and secrets",
    "Location": "\\Safes\\Applications",
    "CreationTime": 1670025600
  },
  {
    "SafeUrlId": "safe_infra",
    "SafeName": "Infrastructure-Creds",
    "Description": "Infrastructure access credentials",
    "Location": "\\Safes\\Infrastructure",
    "CreationTime": 1668433200
  }
]

{
  "SafeUrlId": "safe_prod_db",
  "SafeName": "PROD-DB-Credentials",
  "Description": "Production database credentials",
  "Location": "\\Safes\\Production",
  "CreationTime": 1672531200,
  "LastModificationTime": 1704067200,
  "OLACEnabled": true,
  "NumberOfVersionsRetention": 5,
  "NumberOfDaysRetention": 90
}

[
  {
    "MemberID": 45,
    "MemberName": "vault_admin",
    "MemberType": "User",
    "Permissions": ["UseAccounts", "RetrieveAccounts", "ListAccounts"]
  },
  {
    "MemberID": 67,
    "MemberName": "dba_team",
    "MemberType": "Group",
    "Permissions": ["UseAccounts", "RetrieveAccounts"]
  }
]
```

!!! warning "Common errors"
    **`{"ErrorCode":"ITATS542E","ErrorMessage":"Invalid token or token expired"}`** — Regenerate the authentication token using the login endpoint and update the Authorization header.
    **`{"ErrorCode":"ITATS300E","ErrorMessage":"The Safe does not exist"}`** — Verify the safe name matches exactly (case-sensitive) using the list safes endpoint and correct the `<safe_name>` parameter.
    **`curl: (7) Failed to connect to <pvwa>: Name or service not known`** — Confirm the PVWA hostname or IP address is correct and reachable from your network.
---

## psPAS PowerShell Module

```powershell
# Install module
Install-Module psPAS

# Authenticate
$session = New-PASSession -Credential (Get-Credential) -BaseURI "https://<pvwa>"

# List accounts
Get-PASAccount | Select UserName, Address, SafeName

# Get a specific account
Get-PASAccount -SafeName "ProdSafe" | Where-Object { $_.UserName -eq "svc_db" }

# Rotate a password
Invoke-PASCPMOperation -AccountID <id> -ChangeTask

# List safes
Get-PASSafe | Select SafeName, NumberOfDaysRetention

# Get safe members
Get-PASSafeMember -SafeName "ProdSafe"

# Component health summary
Get-PASComponentSummary

# End session
Close-PASSession
```

---

## PACLI (Legacy Vault CLI)

PACLI connects directly to the Vault, bypassing PVWA. Use only when PVWA is unavailable.

```bash
# Initialise PACLI
PACLI INIT

# Define the Vault server
PACLI DEFINEVAULT vault=<vault_name> address=<vault_ip>

# Logon
PACLI LOGON vault=<vault_name> user=admin password=<pass>

# Open a safe
PACLI OPENFILE vault=<vault_name> user=admin safe=<safe_name>

# List files in safe
PACLI FILESLIST vault=<vault_name> user=admin safe=<safe_name>

# Retrieve a credential file
PACLI RETRIEVEFILE vault=<vault_name> user=admin safe=<safe_name> folder=Root file=<account_name> localfolder=/tmp

# Logoff
PACLI LOGOFF vault=<vault_name> user=admin
```


```text title="Expected output"
PACLI Version 13.2.0 Initialized
Vault 'prod-vault' defined successfully at 192.168.1.50
Logon successful for user 'admin' to vault 'prod-vault'
Safe 'Finance-Creds' opened successfully
Files in safe 'Finance-Creds':
  db-admin-prod
  app-service-account
  legacy-backup-key
  root-ssh-key
File 'db-admin-prod' retrieved successfully to /tmp
Logoff successful for user 'admin' from vault 'prod-vault'
```

!!! warning "Common errors"
    **`PACLI: Vault connection failed - Address unreachable (192.168.1.50:1858)`** — Verify the vault IP address is correct and the CyberArk Vault server is running and accessible on port 1858.
    **`PACLI: Logon failed - Invalid credentials for user 'admin'`** — Confirm the admin password is correct and the user account is not locked or disabled in the Vault.
    **`PACLI: File not found - 'account_name' does not exist in safe 'Finance-Creds'`** — Check the exact file name in the safe using FILESLIST and ensure the folder path is correct (typically 'Root' for top-level files).
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [CyberArk — Procedures](../procedures/)
- [CyberArk — Health Checks](../health-checks/)
- [CyberArk — Scripts](../scripts/)
- [CyberArk — Backup and Restore](../backup-restore/)
- [CyberArk — Install and Upgrade](../install-upgrade/)
- [CyberArk — Common Issues](../../troubleshooting/common-issues/)
