# SnapMirror — Health Checks

> Part of the [SnapMirror Operations](../index.md) reference.

---

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| [ ] Run `snapmirror show -fields lag-time,healthy,state` | `snapmirror show -fields lag-time,healthy,state` | confirm all relationships are healthy with lag within RPO thresholds |
| [ ] Flag any relationship with `healthy: false` | `healthy: false` | review the reason field for root cause |
| [ ] Flag any relationship with lag exceeding the defined RPO (typically) | | |
| [ ] Check for relationships in `broken-off` state from DR tests that have not been resynced | `snapmirror show -relationship-status broken-off` | |
| [ ] Check XDP (SnapVault) relationships are up to date | `snapmirror show -type XDP -fields lag-time,healthy` | |
| [ ] Verify transfer schedules are running as expected | `snapmirror show -fields schedule,last-transfer-end-timestamp` | |
| [ ] For SMBC/AutomatedFailOver, verify mediator reachability | | |

## Health Check

- [ ] All relationships show `healthy: true`
- [ ] No relationships in `broken-off` state
- [ ] All lag times are within the defined RPO for their relationship type
- [ ] SnapMirror Synchronous relationships show `In-Sync` (not `Out-of-Sync`)
- [ ] SMBC mediator is reachable if AutomatedFailOver policies are configured
- [ ] Destination aggregate has sufficient free space for incoming transfers
- [ ] No transfer queue backlog on the destination cluster

~~~bash
# Show all relationships with lag time, health, and state
snapmirror show -fields source-path,destination-path,lag-time,healthy,state,last-transfer-end-timestamp

# Show only unhealthy relationships
snapmirror show -fields lag-time,healthy -health-status unhealthy

# Show relationships in broken-off state
snapmirror show -relationship-status broken-off

# Show XDP (SnapVault) relationships specifically
snapmirror show -type XDP -fields lag-time,healthy,state

# Show transfer history — check for failures in the last 24 hours
snapmirror history show -fields source-path,destination-path,status,transfer-size

# Show SnapMirror Synchronous relationships and sync state
snapmirror show -type sync -fields lag-time,healthy,is-healthy
~~~

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
