---
tags:
  - netapp
  - operations
---
# SnapCenter — CLI Reference


<div class="kb-summary">
Part of the [SnapCenter Operations](index.md) reference.

*Applies to: SnapCenter 5.x*
</div>
```text
┌────────────────────────────────── NetApp SnapCenter — CLI Reference ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        SnapCenter CLI: command-line interface for all management and operational tasks        │   │
│   │            Access: SSH or REST client to management IP; authenticate as admin role            │   │
│   │        Commands: status, list, create, modify, delete, show, and diagnostic operations        │   │
│   │          Scripting: use REST API or CLI in automation for provisioning and reporting          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    SSH → authenticate → show status → configure → verify → log output                                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Server           │  │          Windows VM         │  │       Central control       │   │
│   │           Plug-in           │  │          Host agent         │  │        App-consistent       │   │
│   │            Policy           │  │       Schedule/retain       │  │         Backup rule         │   │
│   │        Resource group       │  │       Grouped targets       │  │        Shared policy        │   │
│   │           Recovery          │  │       Volume/LUN/file       │  │       Granular restore      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Category     │     Command      │      Purpose      │      Output      │      Notes       │   │
│   │      Status      │   show status    │    Health check   │   State/alerts   │    Daily run     │   │
│   │       List       │     list all     │     Inventory     │   Name/ID/size   │    Read-only     │   │
│   │      Create      │  create volume   │     Provision     │    New object    │    Change req    │   │
│   │      Delete      │ delete resource  │    Decommission   │   Confirmation   │   Irreversible   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SnapCenter Server (Windows) · ONTAP clusters · plug-in hosts · application servers       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SnapCenter         = NetApp backup orchestration; coordinates app-consistent snapshots via plug-ins│
│    Plug-in            = host-side agent; quiesces application before snapshot: SQL, Oracle, VMware    │
│    Resource group     = set of resources sharing a backup policy and schedule in SnapCenter           │
│    Policy             = SnapCenter object defining snapshot frequency, retention, and replication t...│
│    App-consistent     = snapshot taken after DB quiesce; guarantees crash-consistent recovery         │
│    Clone lifecycle    = SnapCenter clone: create from snapshot, provision to host, then delete        │
│    FlexClone          = underlying ONTAP technology; SnapCenter clone maps to an ONTAP FlexClone      │
│    Vault policy       = SnapCenter policy that also replicates snapshots to SnapVault destination     │
│    Mirror policy      = SnapCenter policy that replicates snapshots via SnapMirror to DR cluster      │
│    RBAC               = SnapCenter role-based access; Admin, Backup Operator, Restore Operator roles  │
│    SMF                = SnapCenter MySQL database storing job history, policies, and resource configs │
│    SnapCenter API     = REST API on port 8143; full feature coverage for automation workflows         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


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

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
