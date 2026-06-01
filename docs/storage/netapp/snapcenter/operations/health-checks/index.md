# SnapCenter — Health Checks


<div class="kb-summary">
> Part of the [SnapCenter Operations](../index.md) reference.
</div>
```
┌────────────────────────────────── NetApp SnapCenter — Health Checks ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      SnapCenter health checks: routine verification of operational status and performance     │   │
│   │         Checks include: controller status, drive health, replication lag, and capacity        │   │
│   │         Frequency: daily quick checks; weekly detailed review; monthly capacity report        │   │
│   │        Configure threshold-based alerts for proactive incident prevention and awareness       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Check status → review alerts → verify replication → capacity → log                                 │
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
│   │    Check area    │  How to verify   │   Pass criteria   │    Frequency     │       Tool       │   │
│   │   Controllers    │   show status    │    All healthy    │      Daily       │     CLI/GUI      │   │
│   │      Drives      │   show drives    │  No failed/pred.  │      Daily       │     CLI/GUI      │   │
│   │   Replication    │ show replication │  Lag < threshold  │      Daily       │     CLI/GUI      │   │
│   │     Capacity     │  show capacity   │     < 80% used    │      Daily       │     CLI/GUI      │   │
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

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| [ ] Review backup jobs from the last 24 hours | `Get-SmJob -StartTime (Get-Date).AddHours(-24) \| Select JobId,JobType,Status,StartDateTime,EndDateTime` | |
| [ ] Flag any failed or stuck jobs (Status = `Failed` or `Running` for > expected duration) | `Failed` | |
| [ ] Check plugin host connectivity | `Get-SmHost \| Select HostName,HostType,PlugInStatus` | all hosts should show `Running` |
| [ ] Verify secondary (SnapVault/SnapMirror) copies exist for critical resources | `Get-SmBackup -ResourceName <resource>` | |
| [ ] Check SnapCenter Server disk usage | | review log partition growth (default logs under `C:\Program Files\NetApp\SnapCenter\SMCore\logs\`) |
| [ ] Confirm all resources are within their backup SLA window | | no resource should be missing a backup beyond the defined retention interval |
| [ ] Check certificate expiry on the SnapCenter Server | | |

## Health Check

- [ ] All backup jobs in the last 24 hours completed with `Completed` status
- [ ] No jobs are currently stuck in `Running` or `Queued` state
- [ ] All plugin hosts show `PlugInStatus: Running`
- [ ] SnapVault/SnapMirror relationships on secondary storage are healthy (verify from ONTAP: `snapmirror show -fields healthy`)
- [ ] SnapCenter Server has sufficient disk space on the log and repository partitions
- [ ] No unprotected resources flagged in the SnapCenter Dashboard
- [ ] Server TLS certificate is valid and not expiring within 30 days

~~~bash
# Connect to SnapCenter (run from a host with SnapCenter PowerShell toolkit installed)
Open-SmConnection -SMSbaseurl https://<snapcenter-server>:8146

# List all backup jobs from the last 24 hours with status
Get-SmJob -StartTime (Get-Date).AddHours(-24) | Select JobId, JobType, Status, StartDateTime, EndDateTime

# List all jobs currently in Running or Queued state
Get-SmJob | Where-Object { $_.Status -in @("Running","Queued") } | Select JobId, JobType, Status, StartDateTime

# Check plugin host connectivity and status
Get-SmHost | Select HostName, HostType, PlugInStatus, OverallStatus

# List all resource groups and their protection status
Get-SmResourceGroup | Select ResourceGroupName, PluginCode, Status

# List available backups for a specific resource
Get-SmBackup -ResourceName <resource_name> | Select BackupName, BackupTime, Status

# Check all policies
Get-SmPolicy | Select PolicyName, PluginType, BackupType
~~~
