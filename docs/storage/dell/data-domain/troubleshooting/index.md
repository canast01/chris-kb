# Data Domain — Troubleshooting

## Issue Reference

| Symptom | Likely Cause | First Action |
|---|---|---|
| Dedup ratio dropped significantly | Encrypted or compressed source data; new data type ingested; DD Boost source-side dedup disabled | `filesys show compression` — identify which MTree changed; check backup software settings |
| Replication context stuck in `Replicating` or falling behind | Network bandwidth saturation; high ingest on source; target filesystem full | `replication status` for lag; `filesys show space` on target; check network with `net show stats` |
| NFS/CIFS mount failure | Export/share removed or IP restriction changed; network routing issue | `nfs show exports` / `cifs show shares`; verify client IP in access list; check `net show all` |
| VTL tape import failure | VTL slot configuration mismatch; FC path not zoned | `vtl show slots`; check FC zoning from backup media server to DD VTL ports |
| Filesystem nearly full (above 90%) | Cleaning not running; rapid data growth; expired data not deleted by backup software | `filesys show space`; check `filesys clean status`; run `filesys clean start` if not already running |
| DDBoost client authentication error | Expired or mismatched DD Boost credentials | Re-register storage unit in backup software; verify with `ddboost show clients` |
| `filesys status` shows disabled | Filesystem did not auto-start after reboot; hardware fault | `filesys enable`; check `alerts show current` for hardware errors |
| Disk in `Absent` or `Failed` state | Physical disk failure or loose connection | `disk show state`; open Dell support case for disk replacement |
| Low restore throughput from DD | Filesystem cleaning running during restore window; fragmentation | `filesys clean status`; stop clean if running: `filesys clean stop`; retry restore |
| Replication authentication failure | DD certificates expired or mismatched between source and target | `replication show` for error message; `adminaccess certificate show`; reissue certificates |
| CloudIQ showing array offline | SCG connectivity lost or SCG service down | Check SCG appliance; verify `autosupport status` on DD; check `net show all` for SCG reachability |
| Autosupport fails to send | Network path to Dell support blocked; proxy required | `autosupport test`; check firewall rules for outbound HTTPS; configure proxy if needed |

## Diagnostic Commands

```bash
# Filesystem health and space
filesys status
filesys show space
filesys show compression
filesys clean status

# Replication health
replication show
replication status
replication show errors

# DD Boost status and clients
ddboost status
ddboost show clients
ddboost show storage-units

# Active alerts and hardware status
alerts show current
alerts show history
system show
disk show state

# Network diagnostics
net show all
net show stats
ping <hostname-or-ip>

# MTree status and quotas
mtree list
mtree show compression mtree /data/col1/<mtree-name>
mtree show quota /data/col1/<mtree-name>

# NFS and CIFS
nfs show exports
cifs show shares

# VTL diagnostics
vtl show slots
vtl status

# AutoSupport / SCG connectivity
autosupport status
autosupport test

# User and access configuration
user show
adminaccess show
```

## Log Locations

| Log | Location / Command | Contains |
|---|---|---|
| System log | `log view` | DDOS events, service starts/stops, hardware events |
| Audit log | `log view audit` | User logins, configuration changes, administrative actions |
| Replication log | `log view replication` | Replication context events, errors, throughput records |
| Debug log bundle | `support bundle generate` | Full diagnostic bundle for Dell support case |

## Replication Lag — Step-by-Step Investigation

1. Run `replication status` — note `Pre-Comp Remaining`, `Throughput`, and `Estimated Completion`
2. If throughput is low, run `net show stats` — check for packet loss or interface errors
3. Run `filesys show space` on the **target** DD — confirm it is not full
4. Check if source ingest rate is higher than replication can drain: `filesys show compression` shows recent write rate
5. If bandwidth is limited, adjust throttle: `replication throttle set <schedule> <bandwidth-kbps>`
6. If the context shows `Error` state: `replication show errors` — review the specific error code
7. For persistent errors, disable and re-enable the replication context:

```bash
replication disable <context>
replication enable <context>
```

## Low Dedup Ratio — Step-by-Step Investigation

1. Run `filesys show compression` — note the global ratio and trend over time
2. Run `mtree show compression mtree /data/col1/<mtree-name>` — identify which MTree has low ratio
3. Determine the data type being backed up in that MTree:
   - Encrypted databases or already-compressed files will not dedup well (this is expected)
   - If it was previously deduping well and ratio dropped, a new data type may have been added
4. Confirm DD Boost source-side dedup is enabled in the backup software for that MTree's application
5. Confirm the backup job is not sending synthetic full backups (which may bypass DD Boost dedup)

## Filesystem Full — Emergency Steps

```bash
# Check space immediately
filesys show space

# Check if cleaning is already running
filesys clean status

# If not running, start clean
filesys clean start

# Identify largest MTrees
mtree list  # review Logical and Physical columns

# If cleaning does not recover sufficient space:
# — Ask backup team to expire and delete old backups
# — After backup software deletes, run clean again
# — Consider adding capacity (disk shelf expansion)

# Monitor clean progress
filesys clean status  # check every 30 minutes
```

## Error Code Reference

| Error | Meaning | Action |
|---|---|---|
| `REPL-ERR-001` | Replication context authentication failure | Recheck DD Boost or replication user credentials on both ends |
| `DDFS-ERR-FULL` | Filesystem at or above hard capacity limit | Emergency clean; delete expired backups; add capacity |
| `HW-DISK-FAIL` | Physical disk failure detected | Do not delay — open Dell support case immediately; check `disk show state` |
| `BOOST-ERR-AUTH` | DD Boost client authentication rejected | Re-register storage unit; verify DD Boost user in backup software |
| `NTP-DRIFT` | NTP clock drift exceeds threshold | `ntp sync`; verify NTP server reachability |
