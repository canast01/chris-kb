# Operations

> Part of the [NetApp ONTAP](../) reference.

---

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| [ ] Run `cluster show` | `cluster show` | verify all nodes are healthy and HA pairs are configured |
| [ ] Run `storage disk show -broken` | `storage disk show -broken` | confirm zero broken or failed disks |
| [ ] Run `storage aggregate show -fields used-percent` | `storage aggregate show -fields used-percent` | flag any aggregate above 85% used |
| [ ] Run `snapmirror show -fields lag-time,healthy` | `snapmirror show -fields lag-time,healthy` | confirm all relationships healthy and lag within RPO |
| [ ] Run `system health alert show` | `system health alert show` | review and action any active health alerts |
| [ ] Run `storage failover show` | `storage failover show` | confirm HA takeover state is normal on all nodes |
| [ ] Run `volume show -fields volume,state,percent-used` | `volume show -fields volume,state,percent-used` | confirm all volumes are online and below threshold |
| [ ] Run `event log show -messagename callhome.*` | `event log show -messagename callhome.*` | check for any callhome EMS events since last check |

## Health Check

- [ ] Cluster node count and status match expected inventory
- [ ] All HA pairs show `true` for giveback-capability
- [ ] No aggregates above 85% used (warning) or 90% (critical)
- [ ] All SnapMirror relationships show `healthy: true`
- [ ] No active health alerts with severity `error` or higher
- [ ] All SVMs are running: `svm show -state running`
- [ ] Network interfaces all online: `network interface show -status-oper down` returns no results
- [ ] AutoSupport last sent within expected interval: `autosupport history show`

~~~bash
# Cluster node and HA status
cluster show
storage failover show

# Aggregate capacity — flag anything above 85%
storage aggregate show -fields aggr-name,used-percent,state

# Volume space usage across all SVMs
volume show -fields volume,state,percent-used

# SnapMirror relationship health and lag time
snapmirror show -fields source-path,destination-path,lag-time,healthy,state

# Broken or failed disks
storage disk show -broken

# Active health alerts
system health alert show

# Recent callhome EMS events
event log show -messagename callhome.*

# SVM and LIF status
svm show
network interface show -status-oper down
~~~

## Change Readiness

- [ ] All aggregates have at least 15% free capacity to absorb workload shifts during the change
- [ ] HA failover is operational on both nodes (`storage failover show` shows `true` for takeover-enabled)
- [ ] SnapMirror lag is within RPO on all critical relationships before quiescing
- [ ] No active volume move or aggregate rebalance jobs: `volume move show` and `storage aggregate relocation show`
- [ ] AutoSupport is working — send a start-of-maintenance message: `autosupport invoke -node * -type all -message "Starting maintenance"`
- [ ] No open disk rebuild operations: `storage disk show -broken` is clean
- [ ] Snapshots taken of affected volumes before change: `snapshot create -volume <vol> -snapshot pre-change`

| Item | Status | Notes |
|---|---|---|
| Aggregate free capacity ≥ 15% | | |
| HA takeover enabled on all nodes | | |
| SnapMirror lag within RPO | | |
| No active volume moves | | |
| AutoSupport start message sent | | |

## Incident Triage

- [ ] Run `cluster show` first — identify any nodes in degraded or removed state
- [ ] Run `system health alert show` — review all active alerts for severity and subsystem
- [ ] Run `storage disk show -broken` — identify any disk failures driving the incident
- [ ] Run `storage failover show` — check whether any HA takeover has occurred
- [ ] Run `snapmirror show -fields lag-time,healthy` — check if replication is healthy or contributing to the symptom
- [ ] Check specific protocol: `network interface show`, `iscsi session show`, or `fcp show initiator`
- [ ] Review recent EMS events for the affected node: `event log show -node <nodename> -severity error`

| Question | Answer |
|---|---|
| Which node or aggregate is affected? | |
| Is HA takeover currently active? | |
| Are any disks broken or rebuilding? | |
| Is SnapMirror lag outside RPO? | |
| Which protocol is the workload using? | |

## Maintenance Window

1. Send AutoSupport start-of-maintenance: `autosupport invoke -node * -type all -message "Maintenance window starting"`
2. Quiesce SnapMirror relationships on volumes involved in the change: `snapmirror quiesce -destination-path <svm:vol>`
3. For rolling node upgrade — upgrade the non-epsilon node first; initiate takeover on the partner: `storage failover takeover -ofnode <node>`
4. Monitor takeover completion: `storage failover show` should show `In Takeover` then the node comes back up
5. Run `storage failover giveback -ofnode <node>` after the upgraded node is back online; confirm `Waiting for Giveback` transitions to normal
6. Validate cluster health after each node: `cluster show`, `system health alert show`
7. Resume SnapMirror relationships after all changes are complete: `snapmirror resume -destination-path <svm:vol>`
8. Send AutoSupport close-of-maintenance: `autosupport invoke -node * -type all -message "Maintenance window complete"`

## Post-Change Validation

- [ ] `cluster show` — all nodes healthy, HA pairs intact
- [ ] `storage failover show` — all nodes show giveback-enabled true, no takeover active
- [ ] `storage disk show -broken` — no new disk failures introduced during maintenance
- [ ] `snapmirror show -fields lag-time,healthy` — all relationships resumed and healthy
- [ ] `volume show -fields state,percent-used` — all volumes online, no state changes
- [ ] `network interface show -status-oper down` — no LIFs went offline during the change
- [ ] `system health alert show` — no new alerts generated
- [ ] Confirm storage is serving I/O to applications — verify from host side or application monitoring
