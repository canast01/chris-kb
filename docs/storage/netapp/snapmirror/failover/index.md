# SnapMirror Failover

SnapMirror failover activates the destination volume as the primary, allowing client access during a primary site outage.

## Planned Failover (Switchover)

For maintenance or planned migration:

```bash
# On the destination cluster — break the SnapMirror relationship
# This makes the destination volume writable
snapmirror break -destination-path <dest_svm:dest_vol>

# Verify destination is now read-write
volume show -vserver <dest_svm> -volume <dest_vol> -fields state
```

Update client access (DNS, share paths, mount points) to point to the destination.

## Unplanned Failover (Primary Site Down)

```bash
# On the destination cluster — break the relationship to enable write access
snapmirror break -destination-path <dest_svm:dest_vol>

# Check how current the destination is (RPO)
snapmirror show -destination-path <dest_svm:dest_vol> -fields lag-time
```

Note: if replication was asynchronous, the `lag-time` value indicates the RPO gap.

## Verify Data Accessibility After Failover

```bash
# Confirm volume is online and writable
volume show -vserver <dest_svm> -volume <dest_vol>

# Check exports/shares are active
vserver nfs export-policy rule show -vserver <dest_svm>
vserver cifs share show -vserver <dest_svm>
```

## Resync After Primary Recovery

Once the primary site is restored, resync data back from destination to source:

```bash
# Resync: destination becomes new source, primary reseeds
snapmirror resync -source-path <dest_svm:dest_vol> \
    -destination-path <src_svm:src_vol>

# Monitor resync
snapmirror show -destination-path <src_svm:src_vol>
```

## Reverse Resync (Fail Back)

After resync completes and data is consistent:

```bash
# Break the reversed relationship
snapmirror break -destination-path <src_svm:src_vol>

# Restore original replication direction
snapmirror resync -source-path <src_svm:src_vol> \
    -destination-path <dest_svm:dest_vol>
```

## Failover Checklist

- [ ] Determine RPO: check `lag-time` before breaking relationship
- [ ] Break SnapMirror: `snapmirror break`
- [ ] Update DNS/client access to destination
- [ ] Validate application connectivity
- [ ] Document time of failover for change management
- [ ] Plan resync window after primary recovery

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Break fails | Relationship state | Ensure relationship is `snapmirrored` |
| RPO too large | Lag time | Investigate replication schedule/network |
| Resync takes too long | Data delta | Schedule during maintenance window |
| Client can't mount | Export policy | Verify export rules on destination SVM |
