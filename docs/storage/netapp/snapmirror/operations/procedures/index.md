# SnapMirror — Procedures

> Part of the [SnapMirror Operations](../index.md) reference.

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

```bash
# On the destination cluster — break the relationship to enable write access
snapmirror break -destination-path <dest_svm:dest_vol>

# Check how current the destination is (RPO)
snapmirror show -destination-path <dest_svm:dest_vol> -fields lag-time
```

Note: if replication was asynchronous, the `lag-time` value indicates the RPO gap.

### Failover Checklist

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

- After a planned failover (`snapmirror break`) — resync to restore replication
- After data has diverged on both source and destination
- After re-establishing connectivity between clusters following an outage

### Standard Resync (Source → Destination)

```bash
# Re-establish replication from source to destination
snapmirror resync -source-path <src_svm:src_vol> \
    -destination-path <dest_svm:dest_vol>
```

Resync overwrites the destination with data from the source. Any writes to the destination since the break will be lost.

### Reverse Resync (After Failover)

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
