# FlashArray — Backup & Restore

```
FlashArray Data Protection Tiers
  ┌────────────────────────────────────────────────────────────┐
  │  Tier 1: Local Snapshots (Protection Groups)               │
  │  Volumes → PGroup schedule → hourly/daily snaps on array   │
  └────────────────────────────────────────────────────────────┘
                          │  async replication
  ┌────────────────────────▼───────────────────────────────────┐
  │  Tier 2: Async Replication (ActiveDR)                      │
  │  PGroup snaps ──► remote FlashArray DR site  (RPO: mins)   │
  └────────────────────────────────────────────────────────────┘
                          │  sync replication
  ┌────────────────────────▼───────────────────────────────────┐
  │  Tier 3: Synchronous (ActiveCluster)                       │
  │  Pod stretched ──► site A + site B  (RPO = 0)              │
  └────────────────────────────────────────────────────────────┘
                          │  backup integration
  ┌────────────────────────▼───────────────────────────────────┐
  │  Tier 4: Application-Consistent Backup                     │
  │  Veeam / Commvault ──► FlashArray snap API ──► backup repo │
  └────────────────────────────────────────────────────────────┘

Restore path:
  Snapshot → clone (validate) → overwrite production → remount
```

FlashArray provides multiple data protection tiers. Choose the tier that matches your RPO and RTO requirements for each workload.

| Tier | Technology | RPO | RTO | Use Case |
|---|---|---|---|---|
| Local snapshots (protection groups) | PGroup snapshot schedules | Minutes to hours | Minutes (for clone/mount) | Operational recovery; accidental deletion; application rollback |
| Async replication (ActiveDR) | PGroup async replication to remote array | Minutes to hours | 15–30 minutes (manual pod promote) | DR recovery at a secondary site |
| Synchronous replication (ActiveCluster) | Pod-based sync replication | Zero (RPO=0) | Zero (transparent failover) | Metro HA; zero-downtime site failure |
| SafeMode snapshots | Immutable PGroup snapshots | Same as local schedule | Same as local snapshot restore | Ransomware recovery; protection against admin-level data destruction |
| Application-consistent backup | Veeam / Commvault / NBU via FlashArray snapshot API | RPO of backup schedule | Application-dependent | Long-term retention; offsite backup; compliance archive |

---

## Protection Group Snapshot Configuration

Protection groups (PGroups) are the primary vehicle for snapshot-based data protection. Every production volume set should belong to at least one protection group with an active snapshot schedule.

### Create and Configure a Protection Group

```bash
# Create a protection group
purepgroup create prod-oracle-pg

# Add volumes to the protection group
purepgroup addvollist prod-oracle-pg \
    --vollist prod-oracle-data-01,prod-oracle-data-02,prod-oracle-redo-01,prod-oracle-redo-02,prod-oracle-arch-01

# List protection group members
purepgroup listobj prod-oracle-pg --member-type volume

# Set a snapshot schedule:
# - Snap every 1 hour
# - Keep 24 snapshots per day
# - Retain daily snapshots for 7 days
purepgroup schedule prod-oracle-pg \
    --snap-enabled true \
    --snap-frequency 3600 \
    --snap-per-day 24 \
    --snap-for-days 7

# Verify the schedule is active
purepgroup list prod-oracle-pg --schedule
```

**Schedule parameter guidance:**

| Parameter | Value | Meaning |
|---|---|---|
| `--snap-frequency` | Seconds | How often a snapshot is taken; 3600 = hourly, 14400 = every 4 hours |
| `--snap-per-day` | Integer | Maximum snapshots retained per calendar day |
| `--snap-for-days` | Integer | How many days worth of per-day snapshots to keep |
| `--snap-enabled` | `true`/`false` | Enables or disables the snapshot schedule |

**Retention calculation:** `snap-per-day × snap-for-days` gives the maximum snapshot count on the array from this schedule. For hourly snapshots with 24/day and 7 days: up to 168 snapshots per PG. Monitor capacity consumption with `puresnap list --space`.

---

### Async Replication to a Remote Array

```bash
# Establish a connection to the remote array (run on local array)
purearray connect --management-address <remote_mgmt_ip> \
    --replication-address <remote_repl_ip> \
    --type replication \
    remote-dr-fa-01

# Verify the connection is established
purearray list --connection

# Add the remote array as a replication target on the protection group
purepgroup connect prod-oracle-pg --target remote-dr-fa-01

# Set a replication schedule (replicate every 4 hours)
purepgroup schedule prod-oracle-pg \
    --replicate-enabled true \
    --replicate-frequency 14400

# Verify replication is running
purepgroup list prod-oracle-pg --schedule
purepgroup list prod-oracle-pg --replication
```

---

### Take an On-Demand Snapshot

Take manual snapshots before changes, migrations, or maintenance windows:

```bash
# On-demand snapshot with a descriptive suffix
purepgroup snap \
    --pgroup prod-oracle-pg \
    --suffix premigration-$(date +%Y%m%d)

# List all snapshots for a protection group
purepgroup listsnaps prod-oracle-pg

# List with space usage
puresnap list --space
```

---

## Restore Procedures

### Restore a Volume from a Protection Group Snapshot

Use this procedure when recovering from accidental data corruption, application rollback, or logical data loss. Always restore to a clone first for validation before overwriting production.

**Step 1 — Identify the recovery point:**

```bash
# List all snapshots for the protection group
purepgroup listsnaps prod-oracle-pg

# The output shows snapshot names in the format:
# prod-oracle-pg.<suffix>  e.g.  prod-oracle-pg.premigration-20260501

# List individual volume snapshots inside a PG snapshot
purevol list prod-oracle-pg.premigration-20260501.*
```

**Step 2 — Clone the snapshot to a temporary volume for validation:**

```bash
# Create a writable clone of the snapshot for validation
purevol copy \
    prod-oracle-pg.premigration-20260501.prod-oracle-data-01 \
    restore-validate-oracle-data-01

# Connect the clone to a validation host
purehost connect validate-host-01 --vol restore-validate-oracle-data-01

# Mount and validate the data on the validation host before overwriting production
```

**Step 3 — Overwrite production volume (disruptive — requires host quiesce):**

```bash
# Quiesce or stop the application on the host before proceeding
# Disconnect the production volume from the host
purehost disconnect prod-oracle-01 --vol prod-oracle-data-01

# Overwrite production volume with snapshot content
purevol copy \
    prod-oracle-pg.premigration-20260501.prod-oracle-data-01 \
    --overwrite \
    prod-oracle-data-01

# Reconnect to the host
purehost connect prod-oracle-01 --vol prod-oracle-data-01

# Rescan HBA on the host; mount filesystem; validate at application layer
```

---

### Restore a Volume from a Volume-Level Snapshot

For individual volume snapshots (taken with `purevol snap` or `puresnap create`):

```bash
# List snapshots for a specific volume
purevol list prod-oracle-data-01.*

# Example output: prod-oracle-data-01.preupgrade-20260501

# Clone to a validation volume first
purevol copy prod-oracle-data-01.preupgrade-20260501 restore-validate-01

# After validation, overwrite production (disconnect host first)
purevol copy prod-oracle-data-01.preupgrade-20260501 \
    --overwrite prod-oracle-data-01
```

---

### Restore from an Async Replication Snapshot at the DR Site

For recovery at the DR site from a replicated PGroup snapshot:

```bash
# On the DR array — list replicated snapshots
purepgroup listsnaps prod-oracle-pg --on local
# Snapshots replicated from the production array appear here

# Create a volume from the replicated snapshot on the DR array
purevol copy \
    prod-oracle-pg.premigration-20260501.prod-oracle-data-01 \
    dr-restore-oracle-data-01

# Connect to DR hosts and mount for recovery
purehost connect dr-oracle-01 --vol dr-restore-oracle-data-01
```

---

### ActiveDR: Pod Promotion for DR Failover

ActiveDR uses a replica-link between pods on the production and DR arrays. To activate the DR site (promote the DR pod to writable):

```bash
# On the DR array — check the replica-link status
purepod replica-link list

# Promote the DR pod to primary (makes volumes writable on DR)
# This is a planned failover operation — coordinate with the application team
purepod demote prod-oracle-pod     # On production array (demotes prod pod)
# OR
purepod promote dr-oracle-pod      # On DR array (promotes DR pod)

# Verify pod is promoted and volumes are writable
purepod list dr-oracle-pod
purevol list dr-oracle-pod::*
```

For unplanned failover (production array is offline), promote the DR pod without demoting production first, then reconcile after production is restored.

---

### Recover a Destroyed Volume (Undelete)

Volumes that have been destroyed (`purevol destroy`) remain in a pending-eradication state for 24 hours (or longer if SafeMode is enabled). They can be recovered during this window.

```bash
# List all destroyed volumes awaiting eradication
purevol list --pending

# Recover a destroyed volume (returns it to active state)
purevol recover prod-oracle-data-01

# Verify the volume is back in active state
purevol list prod-oracle-data-01

# Reconnect to the host if needed
purehost connect prod-oracle-01 --vol prod-oracle-data-01
```

> If `purealert list` shows a volume was eradicated (permanent deletion after 24 hours), recovery is not possible from the array. Recovery requires restoring from a protection group snapshot.

---

### Recover a Destroyed Protection Group Snapshot

```bash
# List pending (not yet eradicated) snapshots
puresnap list --pending

# Recover a pending snapshot
puresnap recover prod-oracle-pg.premigration-20260501

# Verify it is available
purepgroup listsnaps prod-oracle-pg
```

---

## Backup Validation

### After Any Restore Operation

- [ ] Rescan HBA on the host side — on Linux: `echo "- - -" > /sys/class/scsi_host/hostX/scan`; on Windows: rescan disks in Disk Management or `rescan` in diskpart; on ESXi: rescan in vCenter
- [ ] Confirm the filesystem is mountable and passes fsck / chkdsk if appropriate
- [ ] Validate data integrity at the application layer — test database connectivity, run application smoke tests, confirm expected row counts or file checksums
- [ ] Run `purealert list` — confirm no alerts were generated by the restore activity
- [ ] Verify the protection group schedule is still active after the restore: `purepgroup list --schedule`
- [ ] Document the restore in the change log: timestamp, snapshot used, volumes restored, engineer, outcome, and sign-off

---

## Snapshot Capacity Management

Snapshots consume capacity proportional to the changed data between the snapshot and the current volume state (space-efficient / redirect-on-write). Uncontrolled snapshot retention causes unexpected capacity growth.

```bash
# List all snapshots with space usage (sorted by size, largest first)
puresnap list --space --sort size-

# Check total snapshot space consumption
purearray list --space
# Review the 'snapshot' field in the space output

# Check protection group schedule and retention
purepgroup list --schedule

# Eradicate snapshots that are past retention and no longer needed
# (Snapshots past their expiry are deleted automatically by the schedule)
# To manually eradicate a specific snapshot:
puresnap eradicate prod-oracle-pg.old-snapshot-20250101

# Eradicate all pending snapshots (use with caution)
puresnap eradicate --all
```

**Capacity thresholds:**

| Snapshot Capacity | Action |
|---|---|
| < 10% of array capacity | Normal; no action |
| 10–20% of array capacity | Review retention policy; confirm schedules are expiring old snaps |
| > 20% of array capacity | Investigate; identify PGs with runaway retention; reduce `snap-for-days` or `snap-per-day` |

---

## Backup Integration with Veeam

Veeam Backup & Replication integrates with FlashArray via the Pure Storage Veeam Plug-in, allowing Veeam to use FlashArray snapshots as a pre-backup step.

**Configuration overview:**

1. Install the Veeam Plug-in for Pure Storage on the Veeam server
2. In Veeam, add the FlashArray as a storage system under `Storage Infrastructure > Add Storage`
3. Provide the array management IP and a `storage_admin` API token
4. In the Veeam backup job, enable `Storage snapshots` as the backup source
5. Veeam creates a FlashArray snapshot before the backup job, mounts it on a proxy server, and backs up from the snapshot rather than live data

**Verify Veeam snapshot jobs from the array:**

```bash
# Snapshots created by Veeam appear with a 'VEEAM' suffix in the name
puresnap list | grep -i veeam

# Check protection groups Veeam is managing
purepgroup list | grep -i veeam
```

> The service account API token provided to Veeam requires `storage_admin` role — it needs to create and delete snapshots and protection groups. Do not give it `array_admin`.
