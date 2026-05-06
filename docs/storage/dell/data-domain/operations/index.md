# Operations

> Part of the [Dell Data Domain](../) reference.

---

## Daily Checks

Run these checks each morning to confirm the Data Domain filesystem, dedup health, replication, and DDBoost client connectivity are all healthy.

- [ ] Run `filesys show space` — check pre- and post-compression capacity; alert if post-compression used exceeds 80% of usable capacity
- [ ] Run `filesys show compression` — confirm the global dedup ratio is above 10:1 (healthy target is 20:1+); a significant drop compared to the previous day warrants investigation
- [ ] Run `alerts show current` — review all active hardware and software alerts; triage by severity
- [ ] Run `replication show` — confirm all replication contexts are in `Normal` or `Replicating` state; investigate any context in `Error` or `Warning` state
- [ ] Run `ddboost show clients` — confirm all expected backup servers are connected and authenticated
- [ ] Confirm backup software jobs (Avamar, NetWorker, Veeam, Commvault) completed successfully overnight — check backup application logs if DDBoost clients show unexpected disconnects
- [ ] Run `filesys status` to confirm the filesystem is `Enabled` and `Running`
- [ ] Review ESRS / CloudIQ / Smart Connect for any proactive support alerts or health recommendations

## Health Check

Run these checks before any planned change or as first-response steps when investigating backup failures or capacity alerts.

- [ ] `filesys status` — filesystem is `Enabled` and `Running`
- [ ] `filesys show space` — post-compression usage below 80%; at least 10–15% raw capacity free for cleaner operation
- [ ] `filesys show compression` — global dedup ratio above 10:1; note if it has dropped since the last check
- [ ] `alerts show current` — no active hardware alerts (disk, fan, PSU, NIC)
- [ ] `replication show` — all contexts in `Normal` or `Replicating` with no lag growing unboundedly
- [ ] `ddboost status` — DDBoost service is active and all storage units are accessible
- [ ] `system show` — system hardware health is clean; note firmware version
- [ ] `mtree list` — all MTrees are accessible; per-MTree quotas are not exhausted

~~~bash
# Check filesystem operational status
filesys status

# Show pre- and post-compression space usage
filesys show space

# Show global deduplication and compression ratio
filesys show compression

# Show all replication contexts, their state, and lag
replication show

# Show per-context replication throughput and detailed status
replication status

# List all MTrees and their individual space usage
mtree list

# Show per-MTree dedup ratio for a specific MTree
mtree show compression mtree /data/col1/<mtree-name>

# List DDBoost-connected clients and storage unit status
ddboost show clients

# Show DDBoost service status
ddboost status

# Show all currently active system alerts
alerts show current

# Show system hardware health and DDOS version
system show
~~~

## Change Readiness

Verify these items before performing any change on the Data Domain — DDOS upgrades, MTree reconfigurations, replication changes, or hardware expansions.

- [ ] `replication show` — all contexts in `Normal` state; do not proceed with a DDOS upgrade while any context is in `Error` or actively lagging
- [ ] No active backup sessions at the time of the change — confirm with backup software that no jobs are running or scheduled during the window
- [ ] `filesys cleaning` is not running: run `filesys clean status` — a cleaning run during a backup window or major change can cause I/O contention
- [ ] `alerts show current` returns no active alerts that indicate pre-existing hardware faults
- [ ] `filesys show space` confirms at least 15% raw capacity free — sufficient headroom for the cleaner to operate post-change
- [ ] Confirm a valid backup of the DD configuration: `system show` — note the current DDOS version; export the configuration backup via System Manager
- [ ] Inform backup application teams of the maintenance window; confirm they will not schedule test restores or new backup jobs during the change
- [ ] Verify ESRS / Smart Connect support connectivity before starting, so Dell support can be reached if needed

| Item | Status | Notes |
|---|---|---|
| Replication contexts in Normal state | | |
| No active backup sessions | | |
| filesys cleaning not running | | |
| No active hardware alerts | | |
| ≥15% raw capacity free | | |
| DD config backup exported | | |

## Incident Triage

When backup jobs fail, replication falls behind, or DDBoost clients disconnect, work through this sequence first.

- [ ] Run `alerts show current` — identify any active hardware or software alerts that correspond to the start of the incident
- [ ] Run `filesys show space` — a filesystem at capacity (post-compression usage approaching 100%) will cause backup writes to fail; this is the most common cause of sudden backup failures
- [ ] Run `replication show` — check whether any replication context has entered `Error` state or is accumulating lag; replication errors can signal network issues or a full filesystem on the destination
- [ ] Run `ddboost show clients` — identify which DDBoost-connected backup servers are disconnected or reporting authentication errors
- [ ] Check `filesys status` — if the filesystem is not `Running`, backup writes will fail regardless of capacity
- [ ] Check disk health: `disk show state` — a faulted or absent disk reduces usable capacity and triggers alerts; do not replace a disk without a Dell support case
- [ ] Review backup application logs for the specific error code reported by the backup job — DDBoost error codes map to specific DD conditions
- [ ] If replication lag is growing: run `replication status` to confirm available bandwidth; check WAN utilisation and consider a temporary `replication throttle` adjustment

| Question | Answer |
|---|---|
| What is the current post-compression usage percentage? | |
| Which replication contexts are in Error or lagging? | |
| Which DDBoost clients are disconnected or erroring? | |
| Is the filesystem status Enabled and Running? | |
| Are there any faulted or absent disks? | |

## Maintenance Window

Steps for planned maintenance on a Data Domain — schedule outside the backup window whenever possible.

1. Confirm the maintenance window does not overlap with the backup window — check backup software schedules and confirm no jobs will run during the change
2. Run `replication show` to note the current state of all contexts; if the change requires a replication pause, run `replication sync <context>` to bring the context to current before pausing
3. Confirm no active backup sessions by checking backup software dashboards; wait for any running jobs to complete before starting
4. If this is a DDOS upgrade: run `filesys clean start` and wait for it to complete before the upgrade to reduce post-upgrade clean time
5. Export a configuration backup via System Manager before any upgrade or hardware change
6. Perform the change per the approved runbook (DDOS upgrade, shelf expansion, or configuration change)
7. After the change, run `filesys status`, `replication show`, and `alerts show current` to confirm all services are healthy
8. Run a test DDBoost backup from at least one backup server and confirm the job completes successfully before closing the window

## Post-Change Validation

Run these checks after any change to confirm the Data Domain is healthy and backup services are restored.

- [ ] `filesys status` — filesystem is `Enabled` and `Running`
- [ ] `alerts show current` — no new alerts introduced by the change
- [ ] `replication show` — all replication contexts back to `Normal` state; confirm lag has not grown during the change window
- [ ] `ddboost show clients` — all backup servers reconnected and authenticated
- [ ] `filesys show compression` — dedup ratio is consistent with the pre-change ratio; a significant drop post-change may indicate a configuration issue
- [ ] Backup job success: confirm at least one DDBoost backup job completes successfully after the change
- [ ] `system show` — confirms DDOS version (if this was an upgrade) and hardware health is clean
- [ ] ESRS / CloudIQ shows no new proactive alerts after the change
