# Operations

> Part of the [Pure Storage Evergreen](../) reference.

---

## Daily Checks

- [ ] Apply standard FlashArray daily checks: `purealert list`, `puredrive list`, `purearray list --space` — Evergreen is a subscription model; the underlying FlashArray or FlashBlade operations apply
- [ ] Run `purearray list --hardware` — confirm all hardware components are healthy
- [ ] Run `purepod list` — confirm ActiveCluster pods are stretched and replicating (if configured)
- [ ] Verify subscription status is current in the Pure1 portal: no expiry warnings or renewal actions outstanding
- [ ] Confirm Pure1 phone-home (support tunnel) is active — Pure Support visibility depends on continuous telemetry
- [ ] Check Pure Support contract status — confirm support is active and the renewal date is tracked
- [ ] Review Pure1 for any proactive recommendations or upgrade eligibility notifications from Pure

## Health Check

- [ ] No active hardware alerts in Pure1 or from `purealert list`
- [ ] All drives healthy: `puredrive list` — no `failed` or `recovering` drives
- [ ] Both controllers online and running the same Purity version: `purearray list --controller`
- [ ] ActiveCluster pods are stretched and `replicating: true`: `purepod list --replicating`
- [ ] Pure1 phone-home is active (Pure1 portal: Arrays → select array → Support → Phone Home)
- [ ] Purity software version is within Pure's supported N-2 release window
- [ ] Subscription expiry date is documented and renewal is tracked with sufficient lead time

~~~bash
# List array hardware status — controllers, chassis, power, fans
purearray list --hardware

# Review all active alerts
purealert list

# Array capacity, used space, and data reduction
purearray list --space

# Verify host and host group path status
purehost list
purehgroup list

# Review ActiveCluster pod and replication status
purepod list
purepod list --replicating
purepod list --failover-preference

# Check current Purity software version
purearray list

# List snapshot usage (to monitor ahead of controller upgrade)
puresnap list --space
~~~

## Change Readiness

- [ ] ActiveCluster mediator is reachable and all pods are in sync before entering any upgrade window
- [ ] No outstanding drive rebuilds — `puredrive list` shows all drives `healthy`
- [ ] All hosts have at least two active paths: `purehost list --connection` — single-path hosts will see I/O interruption during a controller restart
- [ ] Snapshot count and capacity are within reasonable bounds — clean up stale snapshots before the upgrade window
- [ ] Purity software version is within the compatible range for the target controller generation (verify with Pure's compatibility matrix)
- [ ] Pure Support engaged and upgrade window scheduled at least 30 days before subscription renewal date
- [ ] Host path validation planned: document current host-to-volume connections before the upgrade for post-change comparison

| Item | Status | Notes |
|---|---|---|
| ActiveCluster mediator reachable | | |
| No active drive rebuilds | | |
| All hosts have redundant paths | | |
| Stale snapshots cleaned up | | |
| Controller upgrade scheduled with Pure | | |

## Incident Triage

- [ ] Run `purealert list` — active alerts are the primary indicator; check for hardware, drive, or replication events
- [ ] Run `puredrive list` — identify any drive that failed during or after the controller upgrade
- [ ] Check host path recovery: `purehost list --connection` — confirm all hosts have their expected path count post-upgrade
- [ ] Check ActiveCluster pod state: `purepod list` — a pod in `unhealthy` state after an upgrade may need mediator re-registration
- [ ] Confirm Pure1 phone-home is active — if the support tunnel went offline during maintenance, restore it to ensure Pure proactive support visibility
- [ ] For replication lag after upgrade: monitor `purepod list` and `purearray monitor` — lag should self-recover once the controller restart completes
- [ ] If a controller did not come back online after NDU: contact Pure Support immediately with the array serial number and upgrade job reference

| Question | Answer |
|---|---|
| Did the controller upgrade complete cleanly? | |
| Are all drives still healthy post-upgrade? | |
| Do all hosts have their expected path counts? | |
| Is the ActiveCluster pod in sync? | |
| Is Pure1 phone-home active? | |

## Maintenance Window

1. Validate host multipathing before the upgrade window: confirm all hosts have at least two active paths via `purehost list --connection`; do not proceed with single-path hosts
2. Confirm ActiveCluster mediator connectivity and pod sync state: `purepod list --replicating`
3. Clean up stale snapshots and eradicated volumes to ensure maximum capacity headroom: `puresnap eradicate` for expired snaps
4. Coordinate with Pure Support to confirm the scheduled controller refresh window — Pure performs the hardware swap
5. Monitor `purearray monitor` during the NDU upgrade to detect any unexpected latency impact
6. After each controller upgrade, run `purearray list --controller` — confirm both controllers are online and running the new hardware generation's Purity version
7. Validate pods and replication resume after the upgrade: `purepod list --replicating` should return `true`
8. Confirm all host paths are restored: compare `purehost list --connection` against the pre-upgrade inventory

## Post-Change Validation

- [ ] Both controllers are online: `purearray list --controller` shows both CT0 and CT1 healthy
- [ ] All volumes are accessible: `purevol list` — no volumes in an unavailable state
- [ ] `purepod list --replicating` — all ActiveCluster pods stretched and replicating `true`
- [ ] `puredrive list` — all drives healthy; no drives in `recovering` state
- [ ] `purealert list` — no unresolved error alerts; acknowledge any informational alerts from the upgrade activity
- [ ] Host path counts match pre-upgrade inventory: `purehost list --connection`
- [ ] Pure1 phone-home is active and the new hardware is visible in the Pure1 portal
- [ ] Replication to secondary array is current — check pod state or replication link status
