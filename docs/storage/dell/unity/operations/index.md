# Operations

> Part of the [Dell Unity](../) reference.

---

## Daily Checks

Run these checks each morning to confirm the Unity array, both SPs, pools, and replication sessions are healthy.

- [ ] Run `uemcli /env/health show -filter "health.value ne OK"` — any non-OK result requires immediate investigation before proceeding with other work
- [ ] Check active alerts: `uemcli /sys/alert show` — triage by severity; acknowledge alerts that have been resolved to keep the alert list clean
- [ ] Check pool capacity: `uemcli /stor/pool show -detail` — alert if any pool is above 80% consumed or over-subscribed
- [ ] Verify both SPs are Active: `uemcli /env/sp show` — SP A and SP B should both report `Active`; a single SP active indicates a failover has occurred
- [ ] Check replication sessions: `uemcli /rep/session show` — all sessions should show `Active` state; investigate any session in `Error`, `Paused`, or `Interrupted` state
- [ ] Check disk health: `uemcli /stor/disk show` — confirm no disks in `Faulted` or `Degraded` state
- [ ] Review snapshot capacity consumption: `uemcli /stor/snap show` — confirm snapshots are not consuming unexpected pool space
- [ ] Review Unisphere Dashboard for any threshold warnings or capacity alerts not yet surfaced as active alerts

## Health Check

Run these checks before any planned change or as first-response steps when investigating a reported issue.

- [ ] `uemcli /env/health show -filter "health.value ne OK"` returns no output — all components healthy
- [ ] `uemcli /env/sp show` — both SP A and SP B are `Active` with no faults
- [ ] `uemcli /stor/pool show -detail` — all pools below 80% consumed; FAST Cache status is Enabled if configured
- [ ] `uemcli /sys/alert show` — no unacknowledged alerts of severity `ERROR` or `CRITICAL`
- [ ] `uemcli /rep/session show` — all replication sessions in `Active` state
- [ ] `uemcli /stor/disk show` — no faulted or degraded disks
- [ ] `uemcli /stor/snap show` — no snapshot schedule failures; snapshot count not approaching pool capacity limits
- [ ] `uemcli /sys/sw show` — current software version noted; no pending updates flagged as critical

~~~bash
# Show all components not in an OK health state
uemcli /env/health show -filter "health.value ne OK"

# Show both SP health and current state
uemcli /env/sp show

# Show detailed pool capacity, health, and FAST Cache status
uemcli /stor/pool show -detail

# Show all active system alerts
uemcli /sys/alert show

# Show all replication sessions and their current state
uemcli /rep/session show

# Show all disks and their health state
uemcli /stor/disk show

# Show all snapshots and their pool consumption
uemcli /stor/snap show

# Show installed software version and any pending upgrades
uemcli /sys/sw show

# Show all LUNs with pool assignment and capacity
uemcli /store/lun show
~~~

## Change Readiness

Verify these items before performing any change on the Unity array — pool expansions, LUN provisioning, replication configuration changes, or firmware upgrades.

- [ ] `uemcli /env/health show -filter "health.value ne OK"` returns no output — no pre-existing faults before the change
- [ ] Both SPs are Active: `uemcli /env/sp show` — do not proceed with a firmware upgrade or disruptive change with only one SP active
- [ ] Pool capacity headroom confirmed: `uemcli /stor/pool show -detail` — ensure the pool targeted by the change has at least 20% free capacity
- [ ] Replication session state confirmed: `uemcli /rep/session show` — note the current state for all sessions; confirm no session is in a degraded state before starting
- [ ] Snapshot reserve checked: `uemcli /stor/snap show` — confirm snapshot consumption is not crowding pool capacity
- [ ] No active alerts that relate to the component being changed: `uemcli /sys/alert show`
- [ ] Notify host owners if the change involves a LUN or NAS server they use; coordinate I/O quiesce if needed
- [ ] Confirm the Unisphere System Health Check has been run: `uemcli /sys/general healthcheck`

| Item | Status | Notes |
|---|---|---|
| No pre-existing health faults | | |
| SP A and SP B both Active | | |
| Pool capacity headroom ≥ 20% | | |
| Replication sessions Active | | |
| No unacknowledged critical alerts | | |

## Incident Triage

When hosts report I/O errors, LUNs are inaccessible, or NFS mounts are stale, work through this sequence first.

- [ ] Run `uemcli /env/health show -filter "health.value ne OK"` immediately — identify the faulted component (SP, disk, fan, PSU, pool)
- [ ] Run `uemcli /env/sp show` — confirm whether a SP failover has occurred; a single `Active` SP means the other has faulted or restarted
- [ ] Check pool health: `uemcli /stor/pool show -detail` — a pool below 5% free will cause Unity to automatically invalidate snapshots and replication sessions; check for over-consumption
- [ ] Check active alerts: `uemcli /sys/alert show` — identify the alert that corresponds to the incident start time
- [ ] Check replication sessions if the report involves DR or backup data: `uemcli /rep/session show` — note which sessions are broken and what error is reported
- [ ] For NFS stale file handle errors after a SP failover, instruct clients to remount the export — the NAS interface IP has moved to the surviving SP
- [ ] Check disk health: `uemcli /stor/disk show` — a disk fault that triggers a rebuild can cause latency elevation across the affected pool
- [ ] If the issue is unresolved after these checks, run `uemcli /sys/general healthcheck` and open a Dell support case with the output

| Question | Answer |
|---|---|
| Which component is not OK in /env/health show? | |
| Are both SPs Active or has a failover occurred? | |
| What is the current pool consumed percentage? | |
| Which replication sessions are not Active? | |
| Is there a faulted disk triggering a pool rebuild? | |

## Maintenance Window

Steps for planned maintenance on a Unity array — firmware upgrades, pool expansions, or SP-level work.

1. Notify host and application owners; confirm the maintenance window and any required I/O quiesce
2. Run `uemcli /env/health show -filter "health.value ne OK"` to confirm no pre-existing faults; resolve all faults before starting
3. Confirm both SP A and SP B are in Active state via `uemcli /env/sp show` — a firmware upgrade will restart each SP sequentially and requires both to be healthy
4. Create a pre-maintenance snapshot of critical LUNs or file systems: `uemcli /stor/snap create -storRes <resource_id> -name maint-pre-$(date +%Y%m%d)`
5. Note current replication session states with `uemcli /rep/session show` — be prepared to resume sessions after the maintenance if they are paused
6. Perform the change per the approved runbook; for firmware upgrades, Unisphere upgrades SP B first then SP A — monitor progress and do not interrupt the process
7. After the change, run `uemcli /env/health show`, `uemcli /env/sp show`, and `uemcli /stor/pool show -detail` to confirm the array is healthy
8. Confirm replication sessions return to `Active` state; resume any sessions that remain paused: `uemcli /rep/session -id <id> resume`

## Post-Change Validation

Run these checks after any change to confirm the Unity is healthy and host connectivity is restored.

- [ ] `uemcli /env/health show -filter "health.value ne OK"` returns no output — no new faults introduced
- [ ] `uemcli /env/sp show` — both SP A and SP B are back to `Active` state after any SP-level maintenance
- [ ] `uemcli /stor/pool show -detail` — all pools healthy; capacity consumption within expected range
- [ ] `uemcli /rep/session show` — all replication sessions back to `Active`; note any sessions that need manual resumption
- [ ] `uemcli /sys/sw show` — confirms the new software version is installed (if this was a firmware upgrade)
- [ ] Host connectivity verified: iSCSI or FC LUNs accessible from representative hosts; NFS mounts responding
- [ ] Application owners confirm their applications are running normally
- [ ] Pre-change snapshot retained until the post-change validation period has passed (minimum 24 hours)
