# Operations

> Part of the [Dell PowerMax](../) reference.

---
## Daily Checks


| Check | Command | Notes |
|---|---|---|
| [ ] Open Unisphere for PowerMax → Dashboard and review the Alerts pane |  |  |
| [ ] Run `symcfg list` to confirm all registered arrays are online and | `symcfg list` |  |
| [ ] Check SRDF pair states | `symrdf list -sid XXXX` | all R1/R2 pairs should show `Synchronized` (SRDF/S) or `Consistent` (SRDF/A); investigate any pair showing `Transmit Idle`, `R1 Updated`, or `Suspended` |
| [ ] Check failed or degraded physical drives | `sympd list -sid XXXX -failed` | output should be empty |
| [ ] Review active SnapVX sessions | `symsnap list -sid XXXX` | confirm no device is approaching the 256-snapshot limit; expire stale snaps |
| [ ] Check thin device pool utilisation in Unisphere → Storage → Thin P |  | alert if any pool exceeds 80% consumed |
| [ ] Review Unisphere → Performance → Array for I/O response time and t |  |  |
| [ ] Confirm CloudIQ shows no critical findings for the array; review a |  |  |

## Health Check

Run these commands from a host with Solutions Enabler installed to get a complete picture of array health before any change or incident response.

- [ ] `symcfg list` returns the expected array SIDs with status `Online`
- [ ] `symcfg -sid XXXX show` shows all directors and ports in a healthy state with no fault indicators
- [ ] `sympd list -sid XXXX -failed` returns no output (no failed drives)
- [ ] `symrdf list -sid XXXX` shows all SRDF groups and pair states — note any that are not `Synchronized` or `Consistent`
- [ ] `symdg list -sid XXXX` lists all device groups without errors
- [ ] `symsg list -sid XXXX` lists all storage groups and confirms no group is reporting capacity issues
- [ ] `symsnap list -sid XXXX` shows all active SnapVX sessions with no expired or stuck sessions
- [ ] Unisphere → System → Hardware confirms no director, drive, or port faults
- [ ] CloudIQ risk score is green or within accepted threshold

~~~bash
# List all Symmetrix arrays and confirm they are Online
symcfg list

# Full array health and director/port status for a specific SID
symcfg -sid XXXX show

# List all physical drives — check for Failed or Degraded state
sympd list -sid XXXX

# Filter for failed drives only (should return empty on a healthy array)
sympd list -sid XXXX -failed

# List SRDF groups and pair states
symrdf list -sid XXXX

# Show detailed SRDF pair state for a specific RDF group
symrdf -sid XXXX -rdfg <group> query

# List all device groups
symdg list -sid XXXX

# List all storage groups
symsg list -sid XXXX

# List all SnapVX snapshots across the array
symsnap list -sid XXXX

# Show replication sessions (SRDF and SnapVX combined view)
symreplicate list -sid XXXX
~~~

## Change Readiness

Verify these items before performing any change on the PowerMax — array configuration changes, code upgrades, or DR tests.

- [ ] SRDF state confirmed: `symrdf list -sid XXXX` shows all pairs `Synchronized` or `Consistent` — do not proceed if any pair is in a degraded state without a plan to handle it
- [ ] Take a SnapVX snapshot of source devices before making masking or storage group changes: `symsnap -sid XXXX create -sg <sg-name> -name pre-change-$(date +%Y%m%d)`
- [ ] Confirm no active SRDF sessions are in the middle of a mode change or link recovery
- [ ] Verify host I/O path health: `powermt display dev=all` on connected hosts shows no dead paths
- [ ] Confirm no outstanding Unisphere alerts that could indicate a pre-existing fault
- [ ] Validate thin pool headroom — confirm the pool has at least 20% free before adding devices or expanding storage groups
- [ ] Confirm Solutions Enabler version matches the running PowerMaxOS version to avoid CLI compatibility issues
- [ ] Inform application owners of the change window and confirm I/O drain or application quiesce plan if needed

| Item | Status | Notes |
|---|---|---|
| SRDF pairs Synchronized / Consistent | | |
| SnapVX pre-change snapshot created | | |
| No active Unisphere alerts | | |
| Host path health verified (powermt / multipath) | | |
| Thin pool headroom ≥ 20% | | |

## Incident Triage

When a host reports I/O errors, latency, or a LUN is inaccessible, work through this sequence before escalating.

- [ ] Check Unisphere Dashboard immediately for any active alerts flagged in the last 30 minutes — note alert severity and affected component
- [ ] Run `symcfg -sid XXXX show` to confirm array directors and ports are all healthy; look for any director in a degraded or faulted state
- [ ] Check SRDF state: `symrdf list -sid XXXX` — an unexpected `Suspended` or `R1 Updated` state may indicate the cause of host impact
- [ ] Check for failed drives: `sympd list -sid XXXX -failed` — a drive failure can cause I/O latency during rebuild
- [ ] Check host multipath status from the affected host: `powermt display dev=all` — look for dead paths or asymmetric path counts
- [ ] Check Fibre Channel port errors in Unisphere → Hardware → Directors → Ports for CRC errors or login/logout counts
- [ ] Run `symstat -sid XXXX -type r2` to check real-time array I/O statistics for throughput and latency anomalies
- [ ] Review the event log: Unisphere → System → Audit Log and filter by time of the incident

| Question | Answer |
|---|---|
| Which hosts are affected and what is the LUN device ID? | |
| What is the current SRDF state for relevant RDF groups? | |
| Are there active Unisphere alerts at the time of the incident? | |
| What is the host multipath path count and state? | |
| Are there director or port fault indicators in Unisphere? | |

## Maintenance Window

Steps for planned maintenance on a PowerMax array — applies to firmware upgrades, director replacements, and SRDF maintenance.

1. Notify application owners and confirm the maintenance window; record the start and end time
2. Take a full SnapVX snapshot of all production storage groups: `symsnap -sid XXXX create -sg <sg-name> -name maint-pre-$(date +%Y%m%d)`
3. If the maintenance involves SRDF, confirm the current SRDF state with `symrdf list -sid XXXX` and suspend replication if directed by the change procedure: `symrdf -sid XXXX -rdfg <group> suspend`
4. Quiesce or drain host I/O if the change requires a storage group or masking view modification — coordinate with the application team for a clean I/O halt
5. Perform the change per the approved runbook (firmware upgrade, configuration change, or hardware swap)
6. After the change, run `symcfg -sid XXXX show` to confirm all directors and ports returned to a healthy state
7. If SRDF was suspended, resume and monitor resync: `symrdf -sid XXXX -rdfg <group> resume` then `symrdf list -sid XXXX` until all pairs return to `Synchronized` or `Consistent`
8. Validate host I/O has resumed and confirm application health with application owners before closing the window

## Post-Change Validation

Run these checks after any change to the PowerMax to confirm the array is healthy and hosts are unaffected.

- [ ] `symcfg -sid XXXX show` — all directors and ports in healthy state, no new faults introduced
- [ ] `symrdf list -sid XXXX` — all SRDF pairs back to `Synchronized` (SRDF/S) or `Consistent` (SRDF/A); resync time noted if SRDF was suspended
- [ ] `sympd list -sid XXXX -failed` — no failed drives; confirm no drive fault was introduced during the change
- [ ] Host multipath validation: `powermt display dev=all` on each affected host shows all paths alive with the expected path count
- [ ] Unisphere Dashboard shows no new alerts introduced by the change
- [ ] CloudIQ shows no new critical findings post-change
- [ ] Application owners confirm I/O has resumed and application is healthy
- [ ] SnapVX pre-change snapshot retained until the post-change validation period has passed (minimum 24 hours)
