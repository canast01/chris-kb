# SnapCenter — Backup & Restore


<div class="kb-summary">
Part of the [SnapCenter Operations](../index.md) reference.
</div>
```text
┌─────────────────────────────── NetApp SnapCenter — Backup and Restore ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     SnapCenter backup: snapshots, replication, and external backup application integration    │   │
│   │        Snapshot schedule: hourly for 24 h, daily for 7 days, weekly for 4 weeks minimum       │   │
│   │            Replication: async or sync to DR site for off-site data protection copy            │   │
│   │       Restore: volume-level or file-level restore from snapshot; test restore quarterly       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Snapshot → replicate to DR → verify → document → test restore                                      │
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
│   │       Type       │     Schedule     │     Retention     │     Offsite?     │    Test cycle    │   │
│   │     Snapshot     │   Hourly/daily   │    7/30/90 days   │        No        │     Monthly      │   │
│   │   Replication    │  Policy-driven   │     Per policy    │     Yes (DR)     │    Quarterly     │   │
│   │    Backup app    │ Daily full+incr  │      90+ days     │ Yes (tape/cloud  │    Quarterly     │   │
│   │     Archive      │     Monthly      │      7+ years     │   Yes (object)   │      Annual      │   │
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

## Restore from SnapCenter UI

1. Navigate to **Resources** → select the resource (database, file system, VM)
2. Click **Restore**
3. Select the backup copy (snapshot) to restore from
4. Choose restore scope:
   - **Complete restore** — full volume/database restore
   - **File-level restore** — individual files or directories
   - **Item-level** — application-specific (mailbox, database, table)
5. Confirm and monitor via **Monitor → Jobs**

## SQL Server Database Restore

1. Navigate to **Resources → Microsoft SQL Server**
2. Select the database → **Restore**
3. Choose backup set and log chain (for point-in-time)
4. Select restore destination (original or alternate instance)
5. SnapCenter quiesces, reverts snapshot, and replays logs

## Oracle Database Restore

1. Navigate to **Resources → Oracle**
2. Select the database → **Restore**
3. Choose restore point (snapshot + archive log apply)
4. SnapCenter recovers to the selected SCN or timestamp

## File System Restore

1. Navigate to **Resources → Windows / UNIX File Systems**
2. Select the resource → **Restore**
3. Choose snapshot and target path
4. SnapCenter mounts the snapshot and restores files

## Single File Restore

For granular recovery without full volume revert:

1. Navigate to the backup copy
2. Click **Mount** to temporarily mount the snapshot
3. Copy the required file(s) from the mounted path
4. Unmount after recovery

## Alternate Location Restore

Restore to a different host or path:
1. In the restore wizard, select **Alternate location**
2. Specify destination host, instance, or path
3. SnapCenter handles clone/mount operations

## Validate After Restore

- Bring the application online and verify data integrity
- Run application-level checks (DBCC CHECKDB for SQL, RMAN validate for Oracle)
- Confirm backup resumes on the restored resource

## Common Issues

| Issue | Cause | Action |
|---|---|---|
| Restore fails at mount step | Array connectivity | Check ONTAP LIF and iSCSI/NFS |
| Log replay fails | Logs missing | Restore from an earlier consistent point |
| Plugin error during restore | Plugin stopped | Restart plugin on target host |
| Alternate restore fails | Credentials | Verify SnapCenter credentials for destination |
