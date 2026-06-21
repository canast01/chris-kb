---
tags:
  - operations
  - security
---
# CyberArk — Scripts


<div class="kb-summary">
PowerShell automation using the `psPAS` module and the PVWA REST API. All automation uses a dedicated PVWA service account with the minimum required safe-level and administrative permissions. Never use a personal admin account for scheduled automation.

*Applies to: CyberArk PAM*
</div>
![CyberArk — Scripts](../../../../assets/security-cyberark-operations-scripts-index.svg)


## Before you begin

- **Access:** admin credentials for the target system and any upstream dependencies (DNS, NTP, vCenter, directory services)
- **Timing:** safe to run during a scheduled maintenance window; allow 1-2 hours for initial deployment
- **Dependencies:** network connectivity verified; DNS resolvable; NTP configured; any licence keys available
- **Logging:** record every IP address, hostname, and credential set assigned during this deployment

---




## Automation Workflow

```mermaid
flowchart TD
    schedTask["Scheduled Task / CI-CD pipeline"] --> authPVWA["New-PASSession\n(svc-cyberark-api)"]
    authPVWA --> doWork{"Task type"}
    doWork -->|"onboarding"| onboard["Add-PASAccount\n(from CSV or IaC)"]
    doWork -->|"rotation report"| rotReport["Get-PASAccount\nfilter failed CPM status"]
    doWork -->|"safe audit"| safeAudit["Get-PASSafe + Get-PASSafeMember\nexport to CSV"]
    doWork -->|"session inventory"| sessionInv["Get-PASRecording\ndate-range export"]
    onboard --> closeSess["Close-PASSession"]
    rotReport --> alertEmail["Send-MailMessage\n(failure alert)"]
    alertEmail --> closeSess
    safeAudit --> closeSess
    sessionInv --> closeSess
```

---

## Prerequisites

```powershell
# Install psPAS module
Install-Module psPAS -Scope CurrentUser

# Authenticate to PVWA (CyberArk authentication)
$credential = Get-Credential  # svc-cyberark-api
New-PASSession -BaseURI "https://pvwa.corp.example.com" -Credential $credential -Type CyberArk

# Authenticate using LDAP / AD credentials
New-PASSession -BaseURI "https://pvwa.corp.example.com" -Credential $credential -Type LDAP

# Close session when done
Close-PASSession
```

---

## Account Onboarding

```powershell
# Onboard a single account
$params = @{
    userName     = "svc-app01"
    address      = "db01.corp.example.com"
    accountName  = "db01-svc-app01"
    platformID   = "WinServerLocal"
    SafeName     = "APP-DB01-Accounts"
    secret       = (ConvertTo-SecureString "InitialPassword123!" -AsPlainText -Force)
    automaticManagementEnabled = $true
}
Add-PASAccount @params

# Bulk onboard from CSV
# CSV columns: userName, address, accountName, platformID, SafeName, secret
Import-Csv "accounts_to_onboard.csv" | ForEach-Object {
    Add-PASAccount `
        -userName $_.userName `
        -address $_.address `
        -accountName $_.accountName `
        -platformID $_.platformID `
        -SafeName $_.SafeName `
        -secret (ConvertTo-SecureString $_.secret -AsPlainText -Force) `
        -automaticManagementEnabled $true
    Write-Host "Onboarded: $($_.accountName)"
}
```

---

## Password Retrieval

```powershell
# Retrieve a password (check-out) — used in automation only, not for interactive retrieval
$account = Get-PASAccount -SafeName "APP-DB01-Accounts" -Keywords "svc-app01"
$cred    = Get-PASAccountPassword -AccountID $account.id

# Use the retrieved password in a script
$securePassword = ConvertTo-SecureString $cred.Password -AsPlainText -Force
$psCredential   = New-Object System.Management.Automation.PSCredential($account.userName, $securePassword)

# Invoke-Command using retrieved credentials
Invoke-Command -ComputerName "db01.corp.example.com" -Credential $psCredential -ScriptBlock {
    # task here
}
```

---

## Safe Management

```powershell
# Create a new safe
Add-PASSafe -SafeName "APP-NEWAPP-Accounts" `
  -Description "Managed accounts for NewApp" `
  -ManagingCPM "PasswordManager" `
  -NumberOfVersionsRetention 5

# Add a safe member with specific permissions
Add-PASSafeMember -SafeName "APP-NEWAPP-Accounts" `
  -MemberName "GG_CyberArk_NewApp_Owners" `
  -UseAccounts $true `
  -RetrieveAccounts $true `
  -ListAccounts $true `
  -AddAccounts $true `
  -UpdateAccountContent $true `
  -UpdateAccountProperties $true `
  -InitiateCPMAccountManagementOperations $true

# List all safes
Get-PASSafe | Select-Object SafeName, Description, ManagingCPM | Sort-Object SafeName

# Export safe membership audit (all safes, all members)
$report = Get-PASSafe | ForEach-Object {
    $safeName = $_.SafeName
    Get-PASSafeMember -SafeName $safeName | ForEach-Object {
        [PSCustomObject]@{
            Safe   = $safeName
            Member = $_.MemberName
            Type   = $_.MemberType
            UseAccounts = $_.Permissions.useAccounts
            RetrieveAccounts = $_.Permissions.retrieveAccounts
        }
    }
}
$report | Export-Csv "SafeMembership_Audit.csv" -NoTypeInformation
```

---

## CPM Rotation Status Report

```powershell
# Report accounts with failed rotation or rotation overdue
$accounts = Get-PASAccount -search "*" | Where-Object {
    $_.secretManagement.status -ne "success" -or
    $_.secretManagement.lastModifiedTime -lt ((Get-Date).AddDays(-90).ToUnixTime())
}

$report = $accounts | Select-Object `
    @{N="AccountName";    E={$_.name}},
    @{N="Safe";           E={$_.safeName}},
    @{N="Address";        E={$_.address}},
    @{N="CPMStatus";      E={$_.secretManagement.status}},
    @{N="LastRotation";   E={[DateTimeOffset]::FromUnixTimeSeconds($_.secretManagement.lastModifiedTime).LocalDateTime}}

$report | Export-Csv "CPM_RotationStatus.csv" -NoTypeInformation
$report | Where-Object { $_.CPMStatus -ne "success" }
```

---

## Session Recording Inventory

```powershell
# List PSM recordings for a date range
$from = (Get-Date).AddDays(-7)
$to   = Get-Date

Get-PASRecording -FromTime $from.ToUnixTime() -ToTime $to.ToUnixTime() |
  Select-Object `
    @{N="User";     E={$_.User}},
    @{N="Target";   E={$_.Target}},
    @{N="Safe";     E={$_.Safe}},
    @{N="Start";    E={[DateTimeOffset]::FromUnixTimeSeconds($_.Start).LocalDateTime}},
    @{N="Duration"; E={$_.Duration}} |
  Export-Csv "PSM_Recordings_$(Get-Date -Format 'yyyyMMdd').csv" -NoTypeInformation
```

---

## Failed Rotation Alert

```powershell
# Send email alert for any accounts with CPM failure (run as scheduled task)
Import-Module psPAS
$credential = Import-Clixml "C:\Scripts\CyberArk\svc-cyberark-api.cred"
New-PASSession -BaseURI "https://pvwa.corp.example.com" -Credential $credential -Type CyberArk

$failed = Get-PASAccount -search "*" |
  Where-Object { $_.secretManagement.status -eq "failure" }

if ($failed.Count -gt 0) {
    $body = $failed | Select-Object name, safeName, address,
      @{N="Status"; E={$_.secretManagement.status}} |
      ConvertTo-Html -Fragment

    Send-MailMessage `
        -To "infra-sec@corp.example.com" `
        -From "noreply-cyberark@corp.example.com" `
        -Subject "CyberArk: $($failed.Count) CPM Rotation Failure(s)" `
        -Body "<html><body>$body</body></html>" `
        -BodyAsHtml `
        -SmtpServer "smtp.corp.example.com"
}

Close-PASSession
```

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [CyberArk — Procedures](../procedures/)
- [CyberArk — Health Checks](../health-checks/)
- [CyberArk — CLI Reference](../cli-reference/)
- [CyberArk — Backup and Restore](../backup-restore/)
- [CyberArk — Install and Upgrade](../install-upgrade/)
- [CyberArk — Common Issues](../../troubleshooting/common-issues/)
