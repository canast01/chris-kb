---
tags:
  - netapp
  - operations
---
# SnapMirror — Procedures


<div class="kb-summary">
SnapMirror procedures: creating protection relationships, scheduling updates, quiescing for maintenance, breaking for failover, resyncing after outage, and deleting stale relationships.

*Applies to: SnapMirror*
</div>



---

```d2
direction: right

hub: "SnapMirror\nOperations" {shape: hexagon}
change_readiness: "Change Readiness" {shape: rectangle}
maintenance_window: "Maintenance Window" {shape: rectangle}
postchange_validation: "Post-Change Validation" {shape: rectangle}
failover_procedure: "Failover Procedure" {shape: rectangle}
resync_procedure: "Resync Procedure" {shape: rectangle}
initialize_a_snapmirror_relationship: "Initialize a SnapMirror Relationship" {shape: rectangle}

hub -> change_readiness
hub -> maintenance_window
hub -> postchange_validation
hub -> failover_procedure
hub -> resync_procedure
hub -> initialize_a_snapmirror_relationship
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Change Readiness

- [ ] All relationships are healthy before quiescing — check `snapmirror show -fields healthy` returns `true` for all
- [ ] Lag is within RPO on all critical volumes — document baseline lag before the change
- [ ] No relationships are in `broken-off` state from a prior DR test — resync before entering the change window
- [ ] Destination aggregate has at least 20% free space to continue receiving transfers after the change
- [ ] Transfer schedules reviewed — plan the maintenance window to avoid overlapping with scheduled large transfers
- [ ] SnapMirror quiesce plan documented for source volumes involved in the change: `snapmirror quiesce -destination-path <svm:vol>`
- [ ] SMBC mediator reachable and pod state healthy before any change to synchronous relationships

| Item | Status | Notes |
|---|---|---|
| All relationships healthy | | |
| Lag within RPO on all critical volumes | | |
| No broken-off relationships | | |
| Destination aggregate has free space | | |
| SMBC mediator reachable (if applicable) | | |

## Maintenance Window

1. Identify all SnapMirror relationships for source volumes involved in the change
2. Quiesce relationships to pause future transfers while finishing any in-progress transfer: `snapmirror quiesce -destination-path <svm:vol>`
3. Confirm quiesce completes — `snapmirror show -destination-path <svm:vol>` should show `Quiesced`
4. Perform the planned source-side change (ONTAP upgrade, volume move, aggregate maintenance, etc.)
5. Resume relationships after the change is complete: `snapmirror resume -destination-path <svm:vol>`
6. Trigger an immediate incremental update to minimize lag catch-up: `snapmirror update -destination-path <svm:vol>`
7. Monitor lag recovery: `snapmirror show -fields lag-time` — confirm lag returns to within RPO
8. For SMBC: confirm pod state returns to `InSync` after resuming; verify mediator is registering both arrays

## Post-Change Validation

- [ ] Run `snapmirror show -fields healthy` — all relationships show `healthy: true`
- [ ] Run `snapmirror show -relationship-status broken-off` — returns no results
- [ ] Lag time is recovering and trending back within RPO on all critical relationships
- [ ] `snapmirror show -type sync -fields is-healthy` — all synchronous relationships show `In-Sync`
- [ ] Transfer history shows successful incremental transfers post-change: `snapmirror history show`
- [ ] Destination aggregate has sufficient free space — no space-related transfer errors
- [ ] SMBC pod state is healthy and mediator connectivity confirmed (if applicable)

---

## Failover Procedure

SnapMirror failover activates the destination volume as the primary, allowing client access during a primary site outage.

### Planned Failover (Switchover)

![Planned Failover (Switchover)](../../../../assets/snapmirror-proc-planned-failover-switchover.svg)

For maintenance or planned migration:

```bash
# On the destination cluster — break the SnapMirror relationship
# This makes the destination volume writable
snapmirror break -destination-path <dest_svm:dest_vol>

# Verify destination is now read-write
volume show -vserver <dest_svm> -volume <dest_vol> -fields state
```

Update client access (DNS, share paths, mount points) to point to the destination.

### Unplanned Failover (Primary Site Down)

![Unplanned Failover (Primary Site Down)](../../../../assets/snapmirror-proc-unplanned-failover-primary-site-down.svg)

```bash
# On the destination cluster — break the relationship to enable write access
snapmirror break -destination-path <dest_svm:dest_vol>

# Check how current the destination is (RPO)
snapmirror show -destination-path <dest_svm:dest_vol> -fields lag-time
```

Note: if replication was asynchronous, the `lag-time` value indicates the RPO gap.

### Failover Checklist

![Failover Checklist](../../../../assets/snapmirror-proc-failover-checklist.svg)

- [ ] Determine RPO: check `lag-time` before breaking relationship
- [ ] Break SnapMirror: `snapmirror break`
- [ ] Update DNS/client access to destination
- [ ] Validate application connectivity
- [ ] Document time of failover for change management
- [ ] Plan resync window after primary recovery

---

## Resync Procedure

Resync re-establishes a SnapMirror relationship after it has been broken (intentionally for failover, or due to an error).

### When to Resync

![When to Resync](../../../../assets/snapmirror-proc-when-to-resync.svg)

- After a planned failover (`snapmirror break`) — resync to restore replication
- After data has diverged on both source and destination
- After re-establishing connectivity between clusters following an outage

### Standard Resync (Source → Destination)

![Standard Resync (Source → Destination)](../../../../assets/snapmirror-proc-standard-resync-source-destination.svg)

```bash
# Re-establish replication from source to destination
snapmirror resync -source-path <src_svm:src_vol> \
    -destination-path <dest_svm:dest_vol>
```

Resync overwrites the destination with data from the source. Any writes to the destination since the break will be lost.

### Reverse Resync (After Failover)

![Reverse Resync (After Failover)](../../../../assets/snapmirror-proc-reverse-resync-after-failover.svg)

When the original destination was activated (failed over to) and is now the active source:

```bash
# Step 1: Resync from destination (now active) back to the original source
snapmirror resync -source-path <dest_svm:dest_vol> \
    -destination-path <src_svm:src_vol>

# Step 2: Monitor until transfer completes
snapmirror show -destination-path <src_svm:src_vol>

# Step 3: After primary is ready to resume, break reverse relationship
snapmirror break -destination-path <src_svm:src_vol>

# Step 4: Re-establish original direction
snapmirror resync -source-path <src_svm:src_vol> \
    -destination-path <dest_svm:dest_vol>
```

---

## Initialize a SnapMirror Relationship

Run the initialize command to perform the first baseline transfer from source to destination:

```bash
snapmirror initialize -source-path <vserver:vol> -destination-path <vserver:vol>
```

Monitor initialization progress — the first transfer copies all data and can take hours depending on volume size:

```bash
snapmirror show -fields state,lag-time
```

Wait until the relationship state shows **Idle** and the lag-time reflects the time since the baseline transfer completed. The destination volume is read-only once initialization finishes.

---

## Update SnapMirror Manually

Trigger an on-demand incremental update outside the scheduled transfer window:

```bash
snapmirror update -source-path <vserver:vol> -destination-path <vserver:vol>
```

Monitor the transfer until it completes:

```bash
snapmirror show -fields state,lag-time
```

Verify that lag-time drops to near-zero after the update completes, confirming the destination is current.

---

## Break and Reactivate a SnapMirror Relationship

**Break (for DR failover or testing):** makes the destination volume read-write and suspends replication.

```bash
snapmirror break -destination-path <vserver:vol>
```

The destination volume is now writable and can accept host I/O. Replication is suspended until the relationship is resynced.

**Resync (reprotect):** re-establishes replication after a break. The destination is overwritten with data from the source; any writes made to the destination since the break will be lost.

```bash
snapmirror resync -source-path <vserver:vol> -destination-path <vserver:vol>
```

---

## Change SnapMirror Schedule

Modify the transfer schedule on an existing relationship:

```bash
snapmirror modify -destination-path <vserver:vol> -schedule hourly
```

Verify the updated schedule is applied:

```bash
snapmirror show -fields schedule
```

Confirm the new schedule aligns with the required RPO — more frequent schedules reduce RPO but increase network utilisation.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## Create a SnapMirror Relationship

Create the destination volume, peer the clusters and SVMs, then create and initialize the relationship.

```bash
# Step 1: Peer the clusters (run on the local cluster, referencing the remote)
cluster peer create -peer-addrs <remote_cluster_mgmt_ip>

# Step 2: Peer the SVMs
vserver peer create -vserver <local_svm> -peer-vserver <remote_svm> \
    -peer-cluster <remote_cluster_name> -applications snapmirror

# Step 3: Create the destination volume as a DP (data protection) type
volume create -vserver <dest_svm> -volume <dest_vol> \
    -aggregate <dest_aggr> -type DP -size <size>

# Step 4: Create the SnapMirror relationship
snapmirror create \
    -source-path <src_svm:src_vol> \
    -destination-path <dest_svm:dest_vol> \
    -policy MirrorAllSnapshots

# Step 5: Initialize (baseline transfer — copies all data; may take hours)
snapmirror initialize -destination-path <dest_svm:dest_vol>

# Monitor initialization progress
snapmirror show -destination-path <dest_svm:dest_vol> -fields state,lag-time
```

Wait until state shows **Idle** before considering the relationship established.

---

## Schedule Management

Create a named cron schedule and assign it to a SnapMirror relationship.

```bash
# Create a cron schedule (runs every hour, on the hour)
job schedule cron create -name hourly-sm -hour 0 -minute 0

# Assign the schedule to an existing relationship
snapmirror modify -destination-path <dest_svm:dest_vol> -schedule hourly-sm

# Verify the schedule is applied
snapmirror show -destination-path <dest_svm:dest_vol> -fields schedule
```

Confirm the schedule aligns with the required RPO — more frequent transfers reduce RPO but increase network utilisation.

---

## Manual Update (On-Demand Transfer)

Trigger an immediate incremental transfer outside the scheduled window.

```bash
# Trigger an on-demand incremental update
snapmirror update -destination-path <dest_svm:dest_vol>

# Check lag after the transfer completes
snapmirror show -destination-path <dest_svm:dest_vol> -fields lag-time
```

Verify lag-time drops to near-zero after the update, confirming the destination is current.

---

## Quiesce and Resume

Pause transfers for maintenance without breaking the relationship.

```bash
# Quiesce — pauses new transfers but lets any in-progress transfer finish
snapmirror quiesce -destination-path <dest_svm:dest_vol>

# Verify the relationship is in Quiesced state before proceeding
snapmirror show -destination-path <dest_svm:dest_vol>

# Perform maintenance on the source or network...

# Resume transfers after maintenance is complete
snapmirror resume -destination-path <dest_svm:dest_vol>

# Trigger an immediate update to minimize lag catch-up
snapmirror update -destination-path <dest_svm:dest_vol>
```

Quiesce does not break the relationship — no resync is needed after resuming.

---

## Monitor Lag and Health

Check the status of all SnapMirror relationships.

```bash
# View health and lag across all relationships
snapmirror show -fields healthy,lag-time,last-transfer-type,last-transfer-size

# Confirm no relationships are in broken-off state (should return nothing)
snapmirror show -relationship-status broken-off

# Check for SnapMirror-related errors in the event log
event log show -severity ERROR -message-name snapmirror.*
```

Alert if `healthy` is `false` on any critical relationship, or if `lag-time` exceeds the agreed RPO threshold.

---

## Delete a Relationship

Cleanly remove a SnapMirror relationship. Quiesce and break before deleting.

```bash
# Step 1: Quiesce to stop transfers
snapmirror quiesce -destination-path <dest_svm:dest_vol>

# Step 2: Break to make destination writable (required before delete)
snapmirror break -destination-path <dest_svm:dest_vol>

# Step 3: Delete the relationship metadata
snapmirror delete -destination-path <dest_svm:dest_vol>

# Optional: remove the destination volume if no longer needed
volume delete -vserver <dest_svm> -volume <dest_vol>
```

Verify with `snapmirror show` that the relationship no longer appears after deletion.

---

## Convert Async to Synchronous (SM-BC)

Convert an async relationship to SnapMirror Business Continuity (SM-BC) for zero-RPO SAN replication. Requires ONTAP Mediator deployed and reachable from both clusters.

```bash
# Step 1: Create a synchronous AutomatedFailOver policy
snapmirror policy create -vserver <svm> \
    -policy AutomatedFailOver \
    -type sync \
    -sync-type AutomatedFailOver

# Step 2: Create the SM-BC relationship using the new policy
snapmirror create \
    -source-path <src_svm:src_vol> \
    -destination-path <dest_svm:dest_vol> \
    -policy AutomatedFailOver

# Step 3: Initialize the relationship
snapmirror initialize -destination-path <dest_svm:dest_vol>

# Step 4: Verify the relationship is InSync
snapmirror show -type sync -fields is-healthy
```

**Note:** SM-BC supports iSCSI and FCP SAN volumes only — NAS (NFS/SMB) volumes are not supported. Confirm ONTAP Mediator is registered and both clusters can reach the mediator before initializing.

---

## See also

- [Snapmirror — Health Checks](health-checks/)
- [Snapmirror — CLI Reference](cli-reference/)
- [Snapmirror — Common Issues](../troubleshooting/common-issues/)
