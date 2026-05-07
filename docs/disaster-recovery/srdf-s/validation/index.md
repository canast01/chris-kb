# SRDF/S Validation

## Overview

Validation confirms that SRDF/S replication is protecting data as designed, that pair states are correct, and that a failover would succeed if required. Validation runs are performed after configuration changes, after DR tests, after link maintenance, and on a scheduled basis (typically monthly). Validation differs from health checks in that it actively verifies end-to-end data integrity and failover readiness rather than just checking operational status.

## Pre-Validation Inventory

Before running validation, capture a baseline state snapshot:

```bash
# Save current pair state for all RDFG groups
symcfg list -rdfg all > /tmp/rdfg_inventory_$(date +%Y%m%d).txt

# Capture device-level state for each group
symrdf -g 10 query -detail >> /tmp/rdfg_inventory_$(date +%Y%m%d).txt
symrdf -g 11 query -detail >> /tmp/rdfg_inventory_$(date +%Y%m%d).txt

# Confirm RDF director status
symcfg list -dir all -rdf >> /tmp/rdfg_inventory_$(date +%Y%m%d).txt

# Record SRDF group configuration
symcfg list -rdfg 10 -detail >> /tmp/rdfg_inventory_$(date +%Y%m%d).txt
```

## Pair State and Data Consistency Validation

```bash
# Confirm all pairs are Synchronized (0 invalid tracks)
symrdf -g 10 query -detail | grep -E "Pair State|Invalid Tracks"

# Verify SRDF/S mode (not accidentally switched to /A)
symcfg list -rdfg 10 -detail | grep "SRDF Mode"

# Check for any devices in non-protected states
symrdf -g 10 query | grep -iv "synchronized\|transmit idle"

# Validate device count matches expected configuration
symrdf -g 10 list -v | grep -c "R1"

# Cross-check R2 array shows matching device count
symrdf -sid 0002 -g 10 list -v | grep -c "R2"
```

## Simulated Failover Validation (Non-Disruptive)

A non-disruptive test verifies that the failover command succeeds without actually transferring production I/O. Use `symrdf -testmode` where available, or perform a suspend/resume cycle to confirm link responsiveness:

```bash
# Suspend all pairs (simulates loss of sync link — non-destructive)
symrdf -g 10 -type S suspend -noprompt

# Confirm Suspended state
symrdf -g 10 query

# Resume and verify re-synchronization completes
symrdf -g 10 -type S resume -noprompt

# Wait for Synchronized and confirm 0 tracks
symrdf -g 10 query -detail | grep "Invalid Tracks"
```

For a full DR test failover, follow the DR test runbook and use the SRM test failover workflow to isolate impact to the test bubble network.

## Post-Change Validation

After any SRDF configuration change (adding devices, changing RDFG membership, link maintenance):

```bash
# Confirm new devices appear in group query
symrdf -g 10 list -v

# Confirm all devices reach Synchronized within SLA window
symrdf -g 10 query -detail

# Check no unexpected devices are in Suspended or Split state
symrdf -g 10 query | grep -iv "synchronized\|syncInProg"

# Confirm OLPAIRS configuration is intact
symrdf -g 10 query -detail | grep OLPAIRS
```

## Validation Checklist Table

| Validation Item | Command | Pass Criteria |
|---|---|---|
| All pairs Synchronized | `symrdf -g <rdfg> query` | State = Synchronized |
| Zero invalid tracks | `symrdf -g <rdfg> query -detail` | Invalid Tracks = 0 |
| SRDF mode is /S | `symcfg list -rdfg <n> -detail` | Mode = Synchronous |
| RDF directors Online | `symcfg list -dir all -rdf` | All directors Online |
| Device count matches design | `symrdf -g <rdfg> list -v` | Count matches CMDB |
| Remote array reachable | `symcfg list -rdfg <n> -detail` | Link Online |
| Resync completes within SLA | Monitor `SyncInProg` duration | < agreed RTO window |

## Known Issues and Field Notes

- **Validation script shows false positives during scheduled snapshots**: TimeFinder/SnapVX operations on R1 devices can briefly increase track counts. Schedule validation runs outside snapshot windows.
- **Device count mismatch between arrays**: If R1 and R2 show different device counts, the RDFG was likely modified on one array without the corresponding change on the other. Open a Dell support case immediately — do not attempt manual corrections.
- **SRDF mode shows "Adaptive Copy" instead of "Synchronous"**: This indicates the array temporarily switched to adaptive copy mode due to link congestion. Review link utilization history and correct mode with `symrdf -g <rdfg> -type S set mode synchronous`.
- **Post-DR-test validation shows Suspended pairs**: SRM test failover with array-based replication uses a test bubble snapshot, not a real failover. If pairs appear Suspended after cleanup, run `symrdf -g <rdfg> -type S resume -noprompt` and verify they return to Synchronized.
