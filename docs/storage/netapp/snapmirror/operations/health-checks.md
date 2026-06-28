---
tags:
  - netapp
  - operations
---
# SnapMirror — Health Checks

<div class="kb-summary">
SnapMirror health checks: `snapmirror show -fields lag-time,health`, relationship state review, last-transfer-size trend, and broken-off relationship count.

*Applies to: SnapMirror*
</div>

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

1. **Relationship health** — `snapmirror show -health false` — should return empty
2. **Lag time** — `snapmirror show -fields lag-time | sort -k2 -r | head -10` — flag any relationship with lag exceeding 2× its schedule interval
3. **Failed transfers** — `snapmirror show -transfer-error !- | grep -v healthy` — investigate any transfer errors
4. **Broken-off relationships** — `snapmirror show -state broken-off` — should be empty during normal operations
5. **Throttle check** — `snapmirror show -fields throttle` — verify throttle is not inadvertently set to 0 during business hours
6. **Vault relationship status** — `snapmirror show -policy-type vault` — check all SnapVault relationships are current
7. **Policy compliance** — `snapmirror policy show` — verify a schedule is attached to all relationships

---

## Daily Checks

![Daily Checks](../../../../assets/storage-netapp-snapmirror-hc-daily-checks.svg)

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

![Health Check](../../../../assets/storage-netapp-snapmirror-hc-health-check.svg)

- [ ] All relationships show `healthy: true`
- [ ] No relationships in `broken-off` state
- [ ] All lag times are within the defined RPO for their relationship type
- [ ] SnapMirror Synchronous relationships show `In-Sync` (not `Out-of-Sync`)
- [ ] SMBC mediator is reachable if AutomatedFailOver policies are configured
- [ ] Destination aggregate has sufficient free space for incoming transfers
- [ ] No transfer queue backlog on the destination cluster

```bash
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
```

## Relationship States

![Relationship States](../../../../assets/storage-netapp-snapmirror-hc-relationship-states.svg)

| State | Meaning |
|---|---|
| Snapmirrored | Healthy — replication current |
| Uninitialized | Never seeded; baseline transfer needed |
| Broken-off | Intentionally or unintentionally broken |
| Quiesced | Paused; not replicating |
| Transferring | Actively replicating |

## Lag Time

![Lag Time](../../../../assets/storage-netapp-snapmirror-hc-lag-time.svg)

Lag time is the age of the last successful transfer. For async SnapMirror:
- **< 1 hour** — normal for hourly schedule
- **> 4 hours** — investigate
- **> RPO threshold** — escalate

```bash
snapmirror show -fields lag-time
```

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Snapmirror — Procedures](procedures/)
- [Snapmirror — CLI Reference](cli-reference/)
- [Snapmirror — Common Issues](../troubleshooting/common-issues/)
