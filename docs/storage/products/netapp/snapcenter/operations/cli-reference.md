---
tags:
  - netapp
  - operations
description: "SnapCenter CLI reference: Open-SmConnection, Add-SmResources, New-SmBackup, Get-SmBackupReport, Restore-SmBackup, and Get-SmJob cmdlets."
---
# SnapCenter — CLI Reference

<div class="kb-summary">
SnapCenter CLI reference: `Open-SmConnection`, `Add-SmResources`, `New-SmBackup`, `Get-SmBackupReport`, `Restore-SmBackup`, and `Get-SmJob` cmdlets.

*Applies to: SnapCenter 5.x*
</div>
![SnapCenter — CLI Reference](../../../../../assets/storage-netapp-snapcenter-operations-cli-reference.svg)

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## PowerShell Module

SnapCenter ships a PowerShell module (`SnapCenter`) installed automatically with the server. Load it in any PS session or use the SnapCenter shell shortcut.

| Cmdlet | Purpose |
|---|---|
| `Open-SmConnection` | Authenticate to the SnapCenter server |
| `Close-SmConnection` | Close the session |
| `Get-SmBackup` | List backups |
| `Start-SmBackup` | Trigger a backup |
| `Remove-SmBackup` | Delete a backup |
| `Get-SmJobSummaryReport` | Summarise job history |
| `Get-SmPolicy` | List protection policies |
| `Get-SmClone` | List clones |
| `Remove-SmClone` | Delete a clone |

### Connect

```powershell
# Interactive login (prompts for credentials)
Open-SmConnection -SMSbaseUrl https://snapcenter.example.com

# With stored credential object
$cred = Get-Credential
Open-SmConnection -SMSbaseUrl https://snapcenter.example.com -Credential $cred
```

### Backup Operations

```powershell
# List all backups for a resource
Get-SmBackup -BackupName "*" -PluginCode SCW

# List backups for a specific SQL resource
Get-SmBackup -PluginCode SCSQL -BackupType "DataBackup" | Select BackupName, BackupTime, BackupStatus

# Trigger an on-demand backup
Start-SmBackup -PolicyName "DailyFullBackup" -Resource @{"Host"="sqlhost01";"Type"="Database";"Names"="AdventureWorks"}

# Remove a specific backup by name
Remove-SmBackup -BackupName "AdventureWorks_backup_2024-11-20_01-00-00" -Force
```

### Restore Operations

```powershell
# Restore SQL database from backup
Restore-SmBackup -BackupName "AdventureWorks_backup_2024-11-20_01-00-00" `
  -Resource @{"Host"="sqlhost01";"Type"="Database";"Names"="AdventureWorks"} `
  -RestoreLastBackup

# Point-in-time restore (SQL)
Restore-SmBackup -BackupName "AdventureWorks_backup_2024-11-20_01-00-00" `
  -RestoreToTime "2024-11-20 03:45:00" -LogBackups
```

### Clone Operations

```powershell
# List all clones
Get-SmClone | Select CloneName, SourceBackupName, CloneStatus

# Create a clone from backup
New-SmClone -BackupName "AdventureWorks_backup_2024-11-20_01-00-00" `
  -CloneToInstance "sqlhost02\MSSQLSERVER" -CloneName "AdventureWorks_clone"

# Delete a clone
Remove-SmClone -CloneName "AdventureWorks_clone" -Force
```

### Job Monitoring

```powershell
# Get summary of recent jobs (last 24 h)
Get-SmJobSummaryReport -JobType Backup -StartTime (Get-Date).AddHours(-24)

# Watch a running job
$job = Start-SmBackup -PolicyName "DailyFullBackup" -Resource @{"Host"="sqlhost01";"Type"="Database";"Names"="AdventureWorks"}
do {
    $status = Get-SmJob -JobId $job.JobId
    Write-Host "$(Get-Date -f HH:mm:ss)  Status: $($status.Status)  Progress: $($status.PercentComplete)%"
    Start-Sleep 10
} while ($status.Status -in @("Running","Queued"))
Write-Host "Job finished: $($status.Status)"
```

---

## REST API (curl)

Base URL: `https://<snapcenter-host>/api/4.9`
All requests require the `token` header obtained from the login call.

### Authenticate

```bash
# Login — returns a token
curl -sk -X POST https://snapcenter.example.com/api/4.9/auth/login \
  -H "Content-Type: application/json" \
  -d '{"UserOperationContext":{"User":{"Name":"admin","Passphrase":"password","Rolename":"SnapCenterAdmin"}}}' \
  | python3 -m json.tool

# Extract token (jq)
TOKEN=$(curl -sk -X POST https://snapcenter.example.com/api/4.9/auth/login \
  -H "Content-Type: application/json" \
  -d '{"UserOperationContext":{"User":{"Name":"admin","Passphrase":"password","Rolename":"SnapCenterAdmin"}}}' \
  | jq -r '.Token')
```


```text title="Expected output"
{
  "Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTcwOTMxNjU0MiwiZXhwIjoxNzA5MzIwMTQyfQ.kX9mZ2pQrL5vN8wJqK3hY7bX4cD6eF9gH2jM1nO5sT",
  "UserOperationContext": {
    "User": {
      "Name": "admin",
      "Rolename": "SnapCenterAdmin"
    }
  },
  "ServerVersion": "4.9.0.24680",
  "Timestamp": "2024-03-01T14:42:22.156Z"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command to skip SSL verification (already present in example; if error persists, verify snapcenter.example.com hostname matches certificate CN).
    **`jq: parse error: Cannot index string with string "Token"`** — Ensure the login request succeeds and returns valid JSON; check credentials and SnapCenter API endpoint availability with `curl -sk https://snapcenter.example.com/api/4.9/auth/login -X OPTIONS`.
    **`command not found: jq`** — Install jq with `apt-get install jq` (Ubuntu/Debian) or `yum install jq` (RHEL/CentOS), or use `python3 -m json.tool` to parse JSON instead.
### Jobs

```bash
# List all jobs
curl -sk -X GET "https://snapcenter.example.com/api/4.9/jobs" \
  -H "token: $TOKEN" | jq '.List[] | {JobId, JobType, Status, StartTime}'

# Get a specific job
curl -sk -X GET "https://snapcenter.example.com/api/4.9/jobs/12345" \
  -H "token: $TOKEN" | jq .
```


```text title="Expected output"
{
  "JobId": 12345,
  "JobType": "Backup",
  "Status": "Completed",
  "StartTime": "2024-01-15T08:30:22Z"
}
{
  "JobId": 12346,
  "JobType": "Restore",
  "Status": "Running",
  "StartTime": "2024-01-15T09:15:45Z"
}
{
  "JobId": 12344,
  "JobType": "Verification",
  "Status": "Failed",
  "StartTime": "2024-01-15T07:45:10Z"
}
{
  "JobId": 12345,
  "JobType": "Backup",
  "Status": "Completed",
  "StartTime": "2024-01-15T08:30:22Z",
  "EndTime": "2024-01-15T08:45:33Z",
  "Duration": "PT15M11S",
  "ResourceName": "prod-db-01",
  "PluginType": "SQL",
  "ErrorMessage": null
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command to skip SSL verification, or import the SnapCenter certificate into your CA bundle.
    **`{"error":"Invalid or expired token"}`** — Regenerate the authentication token using SnapCenter's token API and ensure `$TOKEN` variable is properly exported before running the command.
    **`jq: parse error: Invalid JSON`** — Verify the API endpoint is accessible and responding with valid JSON; check SnapCenter service status with `systemctl status snapcenter`.
### Backups via API

```bash
# List backups for a resource
curl -sk -X GET "https://snapcenter.example.com/api/4.9/backups?ResourceName=AdventureWorks" \
  -H "token: $TOKEN" | jq '.Backups[] | {BackupName, BackupTime, BackupStatus}'

# Trigger on-demand backup
curl -sk -X POST "https://snapcenter.example.com/api/4.9/backups" \
  -H "token: $TOKEN" -H "Content-Type: application/json" \
  -d '{
    "jobType": "Backup",
    "pluginCode": "SCSQL",
    "resourceName": "AdventureWorks",
    "policyName": "DailyFullBackup"
  }' | jq '{JobId: .JobId}'
```


```text title="Expected output"
{
  "BackupName": "AdventureWorks_20240115_093045",
  "BackupTime": "2024-01-15T09:30:45Z",
  "BackupStatus": "Completed"
}
{
  "BackupName": "AdventureWorks_20240114_093022",
  "BackupTime": "2024-01-14T09:30:22Z",
  "BackupStatus": "Completed"
}
{
  "BackupName": "AdventureWorks_20240113_093015",
  "BackupTime": "2024-01-13T09:30:15Z",
  "BackupStatus": "Completed"
}
{
  "JobId": "job-8472-5c3e-11ef-a4b2-0050569b8d4c"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag (already present) or import the SnapCenter CA certificate into your system trust store.
    **`jq: error (at <stdin>:1): Cannot index null with string "Backups"`** — Verify the `$TOKEN` variable is set correctly with `echo $TOKEN` and that the SnapCenter API is responding with valid JSON.
    **`{"error":"Invalid resource name","statusCode":400}`** — Confirm the resource name "AdventureWorks" exists in SnapCenter by listing available resources with `curl -sk -X GET "https://snapcenter.example.com/api/4.9/resources" -H "token: $TOKEN"`.
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Snapcenter — Procedures](../procedures/)
- [Snapcenter — Scripts](../scripts/)
- [Snapcenter — Health Checks](../health-checks/)
