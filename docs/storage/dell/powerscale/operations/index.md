# Operations

> Part of the [Dell PowerScale](../) reference.

---

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| [ ] Run `isi status` | `isi status` | confirm all nodes show `ONLINE` and no node is in `SMARTFAIL` or `DOWN` state; note any drive alerts |
| [ ] Run `isi job list` | `isi job list` | confirm no active cluster jobs are in `ERROR` or `PAUSED` state; note unusually long-running Restripe or MultiScan jobs |
| [ ] Check SyncIQ policies | `isi sync policies list` | confirm each policy shows `Last Success` with a timestamp within the expected RPO window |
| [ ] Review recent events | `isi event list --limit 20` | triage any CRITICAL or ERROR severity events |
| [ ] Check storage pool capacity | `isi storagepool list` | alert if any pool or tier exceeds 80% used |
| [ ] Check SmartQuota violations | `isi quota quotas list` | look for directories that have exceeded soft or hard thresholds |
| [ ] Review InsightIQ or CloudIQ for performance anomalies |  | flag any node with sustained CPU utilisation above 85% or latency spikes |
| [ ] Confirm SyncIQ RPO compliance by checking `isi sync reports list - | `isi sync reports list --limit 5` |  |

## Health Check

Run these checks before any maintenance or change, or as first steps when investigating a reported issue.

- [ ] `isi status` — cluster health summary, node states, and drive health are all clean (no SMARTFAIL, no DOWN, no drive faults)
- [ ] `isi storagepool list` — all pools and tiers are below 80% used; confirm SmartPool tiering policies are active
- [ ] `isi job list` — no jobs in ERROR or unexpectedly PAUSED; note any job running longer than its typical duration
- [ ] `isi sync reports list --limit 5` — most recent SyncIQ reports for all policies show SUCCESS; check for policies with repeated failures
- [ ] `isi event list` — no unacknowledged CRITICAL events in the last 24 hours
- [ ] `isi license list` — all required licenses (SmartQuotas, SyncIQ, SmartPools, SnapshotIQ) are valid and not near expiry
- [ ] `isi network subnets list` — SmartConnect zones are configured correctly and DNS delegation is in place
- [ ] `isi statistics query current --keys CPU` — no individual nodes showing sustained CPU saturation

~~~bash
# Overall cluster node and drive health summary
isi status

# List all storage pool tiers and their capacity usage
isi storagepool list

# List active and recent cluster background jobs
isi job list

# List SyncIQ policies and their last run status
isi sync policies list

# Show the 5 most recent SyncIQ replication reports
isi sync reports list --limit 5

# List all cluster events (triage CRITICAL severity first)
isi event list --limit 20

# List all SmartQuota entries including directories near threshold
isi quota quotas list

# Query current per-node CPU utilisation
isi statistics query current --keys CPU

# Show installed OneFS version and license status
isi license list
~~~

## Change Readiness

Verify these items before performing any change on a PowerScale cluster — node additions, OneFS upgrades, SyncIQ policy changes, or quota modifications.

- [ ] `isi status` is clean — no SMARTFAIL nodes, no DOWN nodes, no unacknowledged drive faults
- [ ] SyncIQ policies are in a successful or idle state — `isi sync policies list` shows no policies in ERROR; pause scheduled policies during the change window if needed
- [ ] Quota headroom confirmed — `isi quota quotas list` shows no directories at or above hard threshold before the change
- [ ] No active cluster jobs that would conflict: `isi job list` — Restripe, MultiScan, and FSAnalyze should not be running during major changes
- [ ] Snapshot reserve space is within limits — `isi snapshot list` confirms no unexpected snapshot accumulation consuming pool headroom
- [ ] Confirm OneFS version is within the supported upgrade path if this is a software change (Dell upgrade compatibility matrix)
- [ ] Inform NFS and SMB client teams of the change window; confirm application quiesce plan if node-level work is planned
- [ ] If removing or SmartFailing a node, confirm the cluster has sufficient capacity to absorb the restripe

| Item | Status | Notes |
|---|---|---|
| isi status clean (no SMARTFAIL / DOWN) | | |
| SyncIQ policies idle or paused | | |
| No active conflicting cluster jobs | | |
| Quota headroom confirmed | | |
| Snapshot reserve within limits | | |

## Incident Triage

When clients report NFS/SMB errors, SyncIQ failures, or a node is unreachable, work through this sequence first.

- [ ] Run `isi status` immediately — confirm which nodes and drives are in a fault state; note SMARTFAIL nodes, DOWN nodes, and drive error counts
- [ ] Run `isi event list --limit 20` — find CRITICAL or ERROR events timestamped near the start of the incident; note the event code and description
- [ ] Check SyncIQ if the report involves replication failures: `isi sync policies list` and `isi sync reports list --limit 5` — identify the failing policy and the error message in the report
- [ ] Check quota violations if clients report write failures: `isi quota quotas list` — identify directories at or above hard threshold
- [ ] Verify network connectivity for client-facing interfaces: `isi network subnets list` — confirm all SmartConnect zones and IP pools are intact
- [ ] Check cluster job status: `isi job list` — a long-running Restripe after a node SMARTFAIL can cause elevated latency across the cluster
- [ ] Review per-node statistics for the affected time window: `isi statistics query current --keys CPU` and `isi statistics query current --keys DISK`
- [ ] If a node is DOWN, do not manually remove it — open a Dell support case and monitor `isi job list` for Restripe progress

| Question | Answer |
|---|---|
| Which nodes are SMARTFAIL or DOWN in isi status? | |
| What CRITICAL events appear in isi event list? | |
| Which SyncIQ policies are failing and what is the error? | |
| Are any quota directories at or above hard threshold? | |
| Is a Restripe job running and what is its progress? | |

## Maintenance Window

Steps for planned maintenance on a PowerScale cluster — node SmartFail, OneFS upgrade, or network reconfiguration.

1. Notify NFS and SMB client teams; confirm the maintenance window and coordinate any application quiesce if node-level work is planned
2. Confirm `isi status` is clean — no SMARTFAIL, no DOWN nodes, no unresolved drive faults before starting
3. Pause all SyncIQ scheduled policies to prevent replication from running during the change: `isi sync policies modify <name> --enabled false` for each active policy
4. If adding or removing a node, confirm the cluster has sufficient capacity headroom in `isi storagepool list` to absorb the restripe without crossing 80% used
5. To SmartFail a node for planned maintenance: `isi devices node smartfail <node-lnn>` — monitor Restripe job progress in `isi job list` until complete before physically servicing the node
6. Perform the change per the approved runbook
7. After the change, run `isi status` to confirm all nodes are back ONLINE and drive health is clean
8. Re-enable SyncIQ policies: `isi sync policies modify <name> --enabled true`; trigger a manual run with `isi sync policies run <name>` and confirm SUCCESS before closing the window

## Post-Change Validation

Run these checks after any change to confirm the cluster is healthy and client services have resumed normally.

- [ ] `isi status` — all nodes ONLINE, no SMARTFAIL, no DOWN, no drive faults introduced by the change
- [ ] `isi storagepool list` — all pools and tiers below 80% used; Restripe job completed if a node was added or removed
- [ ] `isi sync policies list` — all SyncIQ policies re-enabled and showing a successful run after the change
- [ ] `isi event list --limit 20` — no new CRITICAL events introduced by the change
- [ ] NFS and SMB client connectivity verified from at least one representative client per access zone
- [ ] Snapshot schedules running as expected: `isi snapshot schedules list`
- [ ] Quota thresholds intact: `isi quota quotas list` shows no unexpected threshold exceedances introduced by the change
- [ ] CloudIQ or InsightIQ shows no new performance anomalies in the post-change window
