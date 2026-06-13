---
tags:
  - dell
  - operations
---
# PowerStore — Backup & Restore


<div class="kb-summary">
Backup & Restore reference covering Protection Architecture Overview, Native Snapshots, Backup Integration, Backup Restore Procedures, Recovery Objectives.

*Applies to: PowerStore 3.x*
</div>
```text
┌──────────────────────────────── Dell PowerStore — Backup and Restore ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     PowerStore backup: snapshots, replication, and external backup application integration    │   │
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
│   │           T-model           │  │          Block only         │  │        iSCSI/FC/NVMe        │   │
│   │           X-model           │  │         Block + File        │  │       Unified protocol      │   │
│   │            Metro            │  │       Sync replication      │  │       Zero-RPO stretch      │   │
│   │          Protection         │  │        Snapshot/Clone       │  │       Immutable snaps       │   │
│   │             Mgmt            │  │          PSM / REST         │  │         Unified pane        │   │
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
│    Physical: PowerStore T/X appliance · NVMe drives · SAS expansion shelves · 10/25 GbE               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    PowerStore         = Dell mid-range NVMe storage; T-model block-only, X-model unified block+file   │
│    PowerStore Manager = browser GUI and REST API endpoint for all PowerStore operations               │
│    Volume group       = logical collection of volumes sharing snapshot and replication policies       │
│    Protection policy  = assigned to volumes; defines snapshot schedule, retention, and replication    │
│    Metro volume       = synchronously replicated volume across two sites; zero RPO active-active      │
│    Snapshot           = space-efficient point-in-time copy; crash-consistent or app-consistent        │
│    Clone              = full writable copy of a volume or file system; independent lifecycle          │
│    Applied-to         = PowerStore host mapping; volumes are applied-to a host or host group object   │
│    Capacity license   = PowerStore uses usable-capacity licensing; licensed in TiB increments         │
│    Storage container  = PowerStore X-model; unified block and file from the same storage pool         │
│    Appliance          = single PowerStore node pair (dual controllers); scalable to 4 appliances      │
│    NVMe-oF            = NVMe over Fabrics; FC-NVMe or NVMe/TCP host connectivity on PowerStore        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Protection Architecture Overview

PowerStore data protection is layered: native snapshots and replication provide first-line protection; external backup tools provide secondary copies. Use both — snapshots enable fast local restores; backup copies provide offsite protection and long-term retention.

```text
Protection Layers (outer to inner)
├── 1. External Backup (Veeam / PPDM / Commvault)
│      Offsite copy; long-term retention; covers volume + data
├── 2. Async Replication
│      DR site copy; RPO-based; recovers from site failure
├── 3. Metro Volume (if deployed)
│      Synchronous copy; zero RPO; covers node/site failure
└── 4. Native Snapshots
       Local; fastest restore; covers logical corruption / accidental deletion
```

## Native Snapshots

### Snapshot Policies

PowerStore schedules snapshots via Protection Policies, which combine:

- **Snapshot Rules**: define frequency and retention
- **Replication Rules**: define RPO interval and target
- **Protection Policy**: bundles one or more rules; assigned to a volume group

```bash
# Create a snapshot rule (hourly, keep 7 days)
curl -k -X POST "https://<mgmt-ip>/api/rest/snapshot_rule" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "hourly-7d",
    "interval": "One_Hour",
    "desired_retention": 168,
    "access_type": "Creation"
  }'

# Create a snapshot rule (daily at 21:00, keep 30 days)
curl -k -X POST "https://<mgmt-ip>/api/rest/snapshot_rule" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "daily-21h-30d",
    "time_of_day": "21:00",
    "days_of_week": ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
    "desired_retention": 720,
    "access_type": "Creation"
  }'

# Create a protection policy combining hourly + daily snapshot rules
curl -k -X POST "https://<mgmt-ip>/api/rest/policy" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "tier2-1h",
    "description": "Hourly snapshots 7d + daily 30d",
    "snapshot_rules": ["<hourly-rule-id>", "<daily-rule-id>"]
  }'

# Assign the policy to a volume group
curl -k -X PATCH "https://<mgmt-ip>/api/rest/volume_group/<vg-id>" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{"policy_id": "<policy-id>"}'
```

### Recommended Snapshot Retention by Tier

| Tier | Workload Type | Snapshot Frequency | Local Retention |
|---|---|---|---|
| Tier 1 | Databases, critical apps | 15-minute or hourly | 7 days |
| Tier 2 | Application servers, ERP | Hourly | 14 days |
| Tier 3 | File servers, home directories | Every 4 hours + daily | 30 days |
| Archive | Backup targets, NAS archives | Daily | 90 days |

### Restoring a Volume from Snapshot

Snapshots can be restored in place (replacing the current volume) or cloned to a new volume for validation before committing to production.

```bash
# Option A: Clone the snapshot to a new volume (safe — production is untouched)
curl -k -X POST "https://<mgmt-ip>/api/rest/volume_snapshot/<snap-id>/clone" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "oradb-prod-data-001-snap-restore-validation",
    "description": "Clone for restore validation"
  }'
# Map the clone to a test host; verify data integrity; then either:
#   a) Promote the clone to production (rename) if it's correct
#   b) Delete the clone if the data was the wrong recovery point

# Option B: Restore in place (destructive — replaces current volume content)
# Ensure the volume is unmounted on all hosts before proceeding
curl -k -X POST "https://<mgmt-ip>/api/rest/volume_snapshot/<snap-id>/restore" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{"backup_snap_name": "before-restore-20260507"}'
# PowerStore creates a backup snapshot of the current state before restoring
```

### File System Snapshot Restore (NFS/SMB)

```bash
# List snapshots for a file system
curl -k -X GET "https://<mgmt-ip>/api/rest/filesystem_snapshot?filesystem_id=<fs-id>" \
  -H "DELL-EMC-TOKEN: <token>"

# Restore the file system from a snapshot (in-place)
curl -k -X POST "https://<mgmt-ip>/api/rest/filesystem_snapshot/<snap-id>/restore" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{"backup_snap_name": "pre-restore-fs-20260507"}'
```

**SMB Previous Versions (Shadow Copies):** PowerStore NAS supports Windows Shadow Copies via the NAS server. When snapshots are scheduled, Windows clients can access previous versions of files directly from the share via right-click → Properties → Previous Versions. Enable this in PowerStore Manager → NAS server → SMB configuration → Enable Shadow Access Copies.

## Backup Integration

### Veeam Backup & Replication

Veeam integrates with PowerStore in two modes:

**Mode 1: vSphere VADP (standard VMware backup)**

- Veeam connects to vCenter and uses vStorage APIs to quiesce and snapshot VMs
- PowerStore is transparent — Veeam reads data from the VMFS/NFS datastore via the ESXi host
- No PowerStore-specific configuration required
- Works with all PowerStore models and protocols

**Mode 2: Veeam Storage Integration Plugin for PowerStore**

- Veeam uses PowerStore snapshots as backup proxy — offloads backup I/O from production hosts
- Requires the Veeam Storage Integration Plugin installed on the Veeam backup server
- Veeam creates a PowerStore snapshot, mounts it to a proxy host, and reads data from the snapshot
- PowerStore REST API credentials required in Veeam configuration

```bash
# Veeam PowerStore plugin configuration:
# Veeam Backup Console → Storage Infrastructure → Add Storage → Dell PowerStore
# Enter:
#   Management IP: <powerstore-mgmt-ip>
#   Protocol: HTTPS
#   Username: veeam-svc (dedicated account with StorageOperator role)
#   Password: <password>
```

Recommended service account for Veeam:

| Setting | Value |
|---|---|
| Username | `veeam-svc` |
| PowerStore role | StorageOperator |
| Permissions | Read volumes, create/delete snapshots, read NAS |
| Location | PowerStore Manager → Settings → Security → Users |

### Dell PowerProtect Data Manager (PPDM)

PPDM provides application-aware protection for VMs and databases on PowerStore:

```text
PPDM Workflow:
1. PPDM discovers VMs via vCenter API
2. PPDM coordinates application quiesce (VMware Tools or pre/post scripts)
3. PPDM triggers a PowerStore snapshot via REST API (crash-consistent or app-consistent)
4. PPDM reads the snapshot and writes to the Data Domain (PowerProtect DD) backup target
5. Snapshot is released after backup completes
```

PPDM configuration for PowerStore:

- PPDM → Infrastructure → Storage Systems → Add → Dell PowerStore
- Enter the PowerStore management IP and a service account with StorageOperator role
- PPDM will discover all volumes and associate them with protected VMs

### Commvault (IntelliSnap)

Commvault IntelliSnap uses the PowerStore REST API to create application-consistent snapshots via snap engines:

```text
Commvault Snap Engine for Dell PowerStore:
1. CommServe coordinates application quiesce (SQL Agent, Oracle Agent, etc.)
2. Snap Engine calls PowerStore REST API to create a volume snapshot
3. Commvault catalogues the snapshot as an IntelliSnap restore point
4. Optional: Commvault mounts the snapshot to an access node for secondary copy to tape/object
```

## Backup Restore Procedures

### VM Restore from Veeam

```text
Veeam Restore Options (in order of speed):
1. Instant VM Recovery — starts VM directly from Veeam repository; fastest
2. Restore to Original Location — overwrites current VM; data consistency depends on backup type
3. Restore to New Location — creates a new VM from backup; safest validation option
4. File-Level Restore — extracts individual files from a VM backup without full VM restore
5. Application Item Recovery — Exchange, SQL, SharePoint, Oracle item-level restore
```

### Database Restore from Snapshot

Example: Oracle database restore from a PowerStore volume snapshot.

```bash
# Step 1: Identify the target snapshot (from the snapshot schedule)
curl -k -X GET "https://<mgmt-ip>/api/rest/volume_snapshot?volume_id=<ora-data-vol-id>" \
  -H "DELL-EMC-TOKEN: <token>" | python3 -m json.tool

# Step 2: Clone the snapshot to a test volume for validation
curl -k -X POST "https://<mgmt-ip>/api/rest/volume_snapshot/<snap-id>/clone" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "ora-restore-validation-20260507"}'

# Step 3: Map the clone to a test/restore host
curl -k -X POST "https://<mgmt-ip>/api/rest/host_volume_mapping" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "volume_id": "<clone-id>",
    "host_id": "<restore-host-id>",
    "logical_unit_number": 10
  }'

# Step 4: On the restore host — mount the LUN and start Oracle in read-only mode to validate
# oracle$ sqlplus / as sysdba
# SQL> startup mount;
# SQL> alter database open resetlogs;   (if recovering from an older snapshot)
# Validate data; confirm correct restore point

# Step 5: If validated — detach from restore host; attach to production host
# Or restore in place on production host (schedule downtime)
```

## Recovery Objectives

| Recovery Scenario | Method | Typical RTO | RPO |
|---|---|---|---|
| Single file/object deleted | NAS snapshot (Previous Versions / NFS snapshot) | < 5 minutes | Last snapshot (hourly) |
| VM corrupted (logical) | Veeam Instant Recovery or snapshot clone | < 15 minutes | Last backup or snapshot |
| Volume corrupted (logical) | PowerStore snapshot restore or clone | 10–30 minutes | Last snapshot (hourly) |
| Drive failure | Automatic (RAID reconstruct); no downtime | 0 minutes (transparent) | 0 |
| Node failure | Automatic peer node takeover | < 60 seconds | 0 |
| Site failure (async replication) | Replication failover; bring up at DR | 1–4 hours | Last RPO cycle (e.g., 1 hour) |
| Site failure (Metro Volume) | Automatic promotion via mediator | < 5 minutes | 0 (synchronous) |
| Full array loss | Restore from Veeam / PPDM backup to new array | 4–24 hours | Last backup |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Powerstore — Procedures](procedures/)
- [Powerstore — Health Checks](health-checks/)
- [Powerstore — Common Issues](../troubleshooting/common-issues/)
