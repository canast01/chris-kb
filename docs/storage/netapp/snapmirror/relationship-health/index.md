# SnapMirror Relationship Health

## View All Relationships

```bash
snapmirror show
snapmirror show -fields source-path,destination-path,state,health,lag-time,last-transfer-size
```

## Identify Unhealthy Relationships

```bash
# Show only unhealthy relationships
snapmirror show -health false

# Show relationships with high lag
snapmirror show -fields lag-time | sort -k2 -r
```

## Relationship States

| State | Meaning |
|---|---|
| Snapmirrored | Healthy — replication current |
| Uninitialized | Never seeded; baseline transfer needed |
| Broken-off | Intentionally or unintentionally broken |
| Quiesced | Paused; not replicating |
| Transferring | Actively replicating |

## Lag Time

Lag time is the age of the last successful transfer. For async SnapMirror:
- **< 1 hour** — normal for hourly schedule
- **> 4 hours** — investigate
- **> RPO threshold** — escalate

```bash
snapmirror show -fields lag-time
```

## Check Last Transfer

```bash
snapmirror show -destination-path <svm:vol> -fields last-transfer-duration,last-transfer-size,last-transfer-type
```

## Update (Force Sync)

```bash
snapmirror update -destination-path <dest_svm:dest_vol>
snapmirror show -destination-path <dest_svm:dest_vol>
```

## Resume a Quiesced Relationship

```bash
snapmirror resume -destination-path <dest_svm:dest_vol>
```

## Re-initialize a Broken Relationship

```bash
# Initialize from scratch (baseline transfer — may take hours)
snapmirror initialize -destination-path <dest_svm:dest_vol>
```

## Pre-Change Checklist

- [ ] All relationships show `health: true`
- [ ] Lag time within RPO tolerance
- [ ] No relationships in `Uninitialized` or `Broken-off` state
- [ ] Last transfer size not anomalous

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Relationship unhealthy | State and error field | Run `snapmirror update`; check network |
| Lag exceeding RPO | Last transfer time | Check schedule; run manual update |
| Transfer failing | ONTAP event log | Check EMS errors on source/dest |
| Relationship not found | SVM/volume name | Verify source and destination paths |
