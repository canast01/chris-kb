---
tags:
  - netapp
  - troubleshooting
search:
  boost: 1.5
---
# SnapCenter — Diagnostics


<div class="kb-summary">
Part of the [SnapCenter Troubleshooting](index.md) reference.
</div>
```text
┌─────────────────────────────────── NetApp SnapCenter — Diagnostics ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        SnapCenter diagnostics: log collection, health checks, and performance analysis        │   │
│   │          Tools: management CLI, REST API, vendor support bundle, and system event log         │   │
│   │          Performance: check I/O latency, throughput, queue depth, and cache hit rate          │   │
│   │       Collect support bundle before contacting vendor support to reduce time-to-resolve       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Identify issue → collect logs → run diagnostics → analyse → resolve                                │
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
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │   SQL plug-in    │  MSSQL backups   │       HTTPS       │   Windows auth   │  App-consistent  │   │
│   │  Oracle plug-in  │  Oracle backups  │       HTTPS       │       SSH        │ RMAN integratio  │   │
│   │  VMware plug-in  │  VM/VMDK backup  │   HTTPS/vCenter   │   vCenter SSO    │   vSphere API    │   │
│   │ SAP HANA plug-in │   HANA backups   │       HTTPS       │     SAP auth     │   Backint API    │   │
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
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Diagnostic Commands

```powershell
# Connect to SnapCenter via PowerShell
Open-SmConnection -SMSbaseurl https://<snapcenter-server>:8146

# List all jobs and filter by failed status
Get-SmJob | Where-Object { $_.Status -eq "Failed" } | Select JobId, JobType, StartDateTime, ErrorMessage

# List all resource groups and their current status
Get-SmResourceGroup | Select ResourceGroupName, Status, LastRunTime

# Check all registered hosts and plugin status
Get-SmHost | Select HostName, HostType, PlugInStatus, HostStatus

# List backups for a specific resource
Get-SmBackup -ResourceName <resource_name> | Select BackupName, BackupTime, BackupType, Status

# Get detailed information about a specific job
Get-SmJobSummaryReport -JobId <job_id>

# List all ONTAP storage connections
Get-SmStorageConnection | Select StorageName, Protocol, ClusterVersion
```

```bash
# On a Linux plugin host — check SnapCenter agent service
systemctl status spl
journalctl -u spl -n 100

# On a Windows plugin host (PowerShell)
Get-Service SnapCenter*
Get-EventLog -LogName Application -Source "SnapCenter*" -Newest 50
```

## Log Locations

| Log Source | Location |
|---|---|
| SnapCenter Server web application logs | `C:\Program Files\NetApp\SnapCenter\SnapCenter Web App\log\` |
| SnapCenter Scheduler service logs | `C:\Program Files\NetApp\SnapCenter\SnapCenter Scheduler\log\` |
| SnapCenter SMCore logs (job engine) | `C:\Program Files\NetApp\SnapCenter\SMCore\log\` |
| Windows plugin agent logs | `C:\Program Files\NetApp\SnapCenter\Snapcenter Plug-in Creator\log\` |
| Linux plugin agent logs | `/var/opt/snapcenter/spl/logs/` |
| SnapCenter Plug-in for VMware logs | `/var/log/netapp/snapcenter/` (inside the OVA appliance) |
| MySQL repository logs | `C:\Program Files\NetApp\SnapCenter\MySQL Data\` → `mysql-error.log` |
| IIS access/error logs | `C:\inetpub\logs\LogFiles\` |

For a full support bundle (all logs + config):
1. In SnapCenter GUI: Help → Support → Generate Support Bundle
2. Alternatively, run PowerShell: `Get-SmSupportBundle -Path C:\temp\snapcenter-bundle`

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
