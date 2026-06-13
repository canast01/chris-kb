---
tags:
  - netapp
  - operations
---
# SnapCenter — Procedures


<div class="kb-summary">
Part of the [SnapCenter Operations](index.md) reference.
</div>
```text
┌───────────────────────────── NetApp SnapCenter — Operational Procedures ──────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           SnapCenter operational procedures: standard tasks for day-2 administration          │   │
│   │           Covers: provisioning, expansion, maintenance, DR testing, and decommission          │   │
│   │           Pre/post checks required for all maintenance activities affecting storage           │   │
│   │            All procedures require approved change management tickets in production            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Open change → pre-check → execute → verify → post-check → close                                    │
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
│   │    Procedure     │    Pre-check     │       Steps       │      Verify      │    Post-check    │   │
│   │    Provision     │  Capacity free?  │   Create volume   │   Host access    │   Monitor I/O    │   │
│   │      Expand      │   Pool space?    │    Grow volume    │    FS resize     │   Verify size    │   │
│   │     Snapshot     │   Policy set?    │   Take snapshot   │   Snap listed    │   Consistency    │   │
│   │     Failover     │  Repl. in sync?  │    Break repl.    │    App online    │    Verify RTO    │   │
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

## Change Readiness

- [ ] All backup jobs are succeeding — no failures in the last 24 hours before the change window
- [ ] No jobs are currently stuck in `Running` or `Queued` state
- [ ] Plugin connectivity is healthy for all hosts involved in the change
- [ ] SnapCenter Server has sufficient disk space — logs and repository should be below 80% full
- [ ] Backup schedules for affected resources are paused or accounted for in the change window timing
- [ ] Application teams are notified if their resource group schedules will be disrupted
- [ ] A manual on-demand backup has been taken for critical resources before the change: `Invoke-SmBackup -Resources @{...}`

| Item | Status | Notes |
|---|---|---|
| All backup jobs succeeding (last 24h) | | |
| No stuck Running or Queued jobs | | |
| Plugin hosts all connected | | |
| SnapCenter Server disk space < 80% | | |
| Pre-change backup taken for critical resources | | |

## Maintenance Window

1. Disable or pause backup schedules for resource groups affected by the maintenance: in SnapCenter GUI, navigate to Resource Groups → select group → Modify → disable schedule
2. Notify application teams that backup jobs will not run during the window and confirm they accept the backup gap
3. For SnapCenter Server upgrades: take a full backup of the SnapCenter repository database (MySQL on the SnapCenter server) before beginning
4. Complete the planned change (plugin upgrade, ONTAP change, host maintenance, etc.)
5. After the change, re-enable resource group schedules and confirm all hosts still show plugin status `Running`: `Get-SmHost`
6. Trigger a manual on-demand backup for critical resource groups to confirm end-to-end backup functionality: GUI → Resource Groups → Back Up Now
7. Verify secondary copies replicated successfully by checking SnapVault/SnapMirror transfer on the destination ONTAP cluster

## Post-Change Validation

- [ ] Run `Get-SmHost` — all plugin hosts show `PlugInStatus: Running` with no degraded hosts
- [ ] Trigger on-demand backup for at least one representative resource group and confirm it completes with `Completed` status
- [ ] Verify backup job in the GUI shows successful snapshot creation on ONTAP: `snapshot show -vserver <svm> -volume <vol>`
- [ ] Confirm secondary copies are replicating: check SnapMirror/SnapVault relationship is healthy from the destination cluster
- [ ] Verify resource group schedules are re-enabled and next scheduled run is visible
- [ ] Check SnapCenter Server disk usage — confirm log partition has not grown unexpectedly during the change
- [ ] Perform a test restore from the most recent backup snapshot on at least one non-production resource to validate restore functionality

---

## Backup Jobs

### Viewing Job History

In the SnapCenter UI:
1. Navigate to **Monitor → Jobs**
2. Filter by resource group, policy, or date range
3. Click a job to view detailed logs

Job statuses:
| Status | Meaning |
|---|---|
| Completed | Backup succeeded |
| Completed with warnings | Succeeded with non-critical issues |
| Failed | Backup failed — review job log |
| Running | Job in progress |

### Running a Backup On-Demand

1. Navigate to **Resources** → select the resource group or resource
2. Click **Back Up Now**
3. Select the policy to apply
4. Confirm and monitor via **Monitor → Jobs**

---

## Policies

Policies define how SnapCenter performs backups — schedule, retention, SnapMirror/SnapVault replication, and consistency settings.

### Key Policy Attributes

- **Backup type** — Snapshot-based, log backup, full/differential
- **Schedule frequency** — Hourly, daily, weekly, monthly
- **Retention** — Number of snapshots to retain on primary
- **Replication** — Update SnapMirror / SnapVault after backup
- **Consistency** — Crash-consistent vs. application-consistent

### Create a Policy

1. Navigate to **Settings → Policies → New**
2. Select the plug-in type (SQL Server, Oracle, Windows, etc.)
3. Configure backup type, schedule, retention count, and SnapMirror update setting
4. Save the policy

### Assign a Policy to a Resource Group

1. Navigate to **Resources → Resource Groups**
2. Select the resource group → **Modify**
3. In the **Policies** step, attach the required policy
4. Set the schedule (if not already in the policy)

---

## Add a Host to SnapCenter

1. Navigate to **Hosts** in the SnapCenter UI and click **Add**
2. Enter the fully qualified domain name (FQDN) of the host
3. Select the plug-in packages to install — SQL Server, Oracle, Windows File System, or others as required
4. Click **Submit** — SnapCenter connects to the host and installs the selected plug-ins
5. Monitor the installation progress in the **Jobs** pane
6. Once complete, verify the host appears in the Hosts list with status **Connected** and all plug-ins show **Running**

---

## Create a Backup Policy

1. Navigate to **Settings → Policies** and click **New Policy**
2. Select the resource type the policy will cover (SQL Server, Oracle, Windows File System, etc.)
3. Set the backup schedule — hourly, daily, weekly, or monthly as required
4. Configure retention: set the number of snapshot copies to retain on primary storage and the number of SnapVault copies to retain on the vault destination
5. Enable **Update SnapMirror after backup** or **Update SnapVault after backup** if secondary replication is required
6. Review the policy summary and click **Finish** to save

---

## Clone a Database from Snapshot

1. Navigate to **Resources** and select the database to clone
2. Click **Clone** from the resource actions menu
3. Select the snapshot to use as the clone source — choose a known-good snapshot for the target recovery point
4. Specify the destination clone host and the clone database SID (SQL instance name or Oracle SID)
5. Configure any clone-specific settings (mount path, log directory, etc.) and click **Clone**
6. Monitor the clone job in **Monitor → Jobs**
7. Once complete, verify the clone database is accessible and the application can connect successfully

---

## Restore a Database to a Point in Time

1. Navigate to **Resources** and select the database to restore
2. Click **Restore** from the resource actions menu
3. Choose the recovery type: **Complete** (restore to most recent backup) or **Point-in-time** (restore to a specific timestamp)
4. For point-in-time recovery, specify the target date and time
5. Select the snapshot to use as the restore source — SnapCenter maps the snapshot to the appropriate data and log backups
6. Review the restore scope (full database, tablespace, or file-level) and confirm settings
7. Click **Restore** and monitor the job in **Monitor → Jobs**
8. Once the job completes, verify the database is online and confirm data integrity with the application team

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
