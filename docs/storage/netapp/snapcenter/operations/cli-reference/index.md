# SnapCenter — CLI Reference

> Part of the [SnapCenter Operations](../) reference.

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

### Jobs

```bash
# List all jobs
curl -sk -X GET "https://snapcenter.example.com/api/4.9/jobs" \
  -H "token: $TOKEN" | jq '.List[] | {JobId, JobType, Status, StartTime}'

# Get a specific job
curl -sk -X GET "https://snapcenter.example.com/api/4.9/jobs/12345" \
  -H "token: $TOKEN" | jq .
```

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
