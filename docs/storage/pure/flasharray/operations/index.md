# Operations

> Part of the [Pure FlashArray](../) reference.

---

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| [ ] Run `purealert list` | `purealert list` | review all active alerts; flag any with severity `error` or `warning` |
| [ ] Run `puredrive list` | `puredrive list` | confirm all drives are in `healthy` state; flag any `failed`, `recovering`, or `missing` drives |
| [ ] Run `purearray list --space` | `purearray list --space` | review array capacity and data reduction ratio; flag if used capacity > 80% |
| [ ] Run `purepod list` | `purepod list` | confirm all ActiveCluster pods are `stretched` and online (if configured) |
| [ ] Check Pure1 portal for AI-driven health recommendations, anomalies |  |  |
| [ ] Run `purevol list --space` | `purevol list --space` | review volume space usage; flag any volumes approaching their allocated limit |
| [ ] Run `puresnap list` | `puresnap list` | check snapshot count; flag runaway snapshot growth from misconfigured protection group schedules |
| [ ] Confirm replication to the secondary array is current | `purepod list --replicating` |  |

## Health Check

- [ ] No active alerts in `purealert list`
- [ ] All drives healthy — `puredrive list` shows no `failed` or `recovering` drives
- [ ] Array capacity below 80% used
- [ ] Both controllers are healthy and running the same Purity version: `purearray list --controller`
- [ ] ActiveCluster pods are stretched and replicating: `purepod list --replicating` shows `true`
- [ ] All host connections are active — no hosts with zero paths: `purehost list`
- [ ] No runaway snapshot growth consuming unexpected capacity

~~~bash
# Array overall status and Purity version
purearray list

# Controller status and firmware version
purearray list --controller

# Array capacity, data reduction, and space usage
purearray list --space

# All active alerts
purealert list

# All drives and health state
puredrive list

# ActiveCluster pods and replication state
purepod list
purepod list --replicating

# All volumes with space usage
purevol list --space

# Snapshot count and usage
puresnap list

# Real-time performance (latency, IOPS, bandwidth)
purearray monitor

# Host and host group connectivity
purehost list
purehgroup list
~~~

## Change Readiness

- [ ] No active drive rebuilds — `puredrive list` shows all drives `healthy`, no `recovering` drives
- [ ] ActiveCluster mediator is reachable and pods are in sync before any change affecting replication
- [ ] Snapshot count is reasonable — no protection group schedules running away that would fill capacity during the window
- [ ] All host connections are documented — run `purehost list --connection` and note current state for post-change comparison
- [ ] Volume connections validated — confirm which hosts connect to which volumes before any connectivity changes
- [ ] Array capacity is below 70% — leaving headroom for snapshot creation during the change
- [ ] Purity upgrade image staged if upgrading: `purearray upgrade --stage <image>` completed and `purearray upgrade --check` passed

| Item | Status | Notes |
|---|---|---|
| No active drive rebuilds | | |
| ActiveCluster mediator reachable | | |
| Snapshot count reasonable | | |
| Host path inventory documented | | |
| Array capacity < 70% | | |

## Incident Triage

- [ ] Run `purealert list` first — active alerts are the fastest path to identifying the failure domain
- [ ] Run `puredrive list` — a failed or rebuilding drive is the most common hardware event
- [ ] Check host connectivity: `purehost list` — verify which hosts have lost paths; confirm expected path counts per host
- [ ] Check ActiveCluster pod state: `purepod list` — a pod in `unhealthy` or `paused` state indicates a replication or mediator event
- [ ] Review Pure1 portal for array-level health events, historical latency spikes, or capacity anomalies
- [ ] For latency issues: run `purearray monitor` and check which volumes are consuming the most IOPS/bandwidth
- [ ] If all paths lost to a host: check FC zoning or iSCSI network connectivity from the host side before escalating to Pure Support

| Question | Answer |
|---|---|
| What does `purealert list` show? | |
| Are any drives in failed or recovering state? | |
| Which hosts have lost connectivity? | |
| Is the ActiveCluster pod state healthy? | |
| Is this a single-array or dual-site issue? | |

## Maintenance Window

1. Confirm all hosts have at least two active paths before beginning — `purehost list --connection`; the NDU controller restart requires proper multipathing
2. For ActiveCluster environments: confirm both pods are healthy and replicating before upgrading; upgrade one array at a time
3. For Purity NDU upgrade: run pre-upgrade check `purearray upgrade --check` to clear all blockers
4. Execute the upgrade: `purearray upgrade --exec` — monitor with `purearray list` until both controllers are on the new version
5. For NVMe drive replacement: follow the Pure hot-swap procedure; confirm `puredrive list` shows the replacement drive as `healthy` after rebuild
6. For controller refresh (Evergreen): coordinate with Pure Support; monitor `purearray monitor` during the upgrade for any I/O impact
7. After any change, run `purealert list` — acknowledge and clear any informational alerts generated by the maintenance activity

## Post-Change Validation

- [ ] `purealert list` — no unresolved error or warning alerts
- [ ] `puredrive list` — all drives healthy; no drives in `recovering` state
- [ ] `purepod list --replicating` — all ActiveCluster pods stretched and replicating `true`
- [ ] `purehost list --connection` — all hosts have the expected number of active paths (compare against pre-change inventory)
- [ ] `purearray list --controller` — both controllers online and running the same Purity version
- [ ] `purearray list --space` — capacity is as expected; no unexpected snapshot growth
- [ ] Confirm replication to secondary array is current — check replication link status in Pure1 or `purepod list`
- [ ] Validate host I/O from application monitoring — confirm latency and throughput are within normal range
