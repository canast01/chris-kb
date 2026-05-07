# SRDF/A Failover

## Overview

SRDF/A failover promotes R2 volumes to read/write. Because SRDF/A is asynchronous, R2 is consistent to the last **completed cycle** rather than the last write, so there is an inherent RPO equal to the lag at the moment of failure. Before failing over, always check the cycle state and lag to understand the data exposure window.

Planned failover (site still accessible) uses `-establish` to immediately reverse replication after the split. Unplanned failover (primary site down) uses the standard `failover` command and requires a separate restore+establish sequence to recover replication.

## Pre-Failover Checks

```bash
# Confirm current cycle state and RPO exposure
symrdf -g 20 -type A query -detail

# Check lag (seconds behind real time)
symrdf -g 20 -type A query -detail | grep -E "Lag|Cycle"

# Confirm R2 is in a Consistent state before failing over
symrdf -g 20 -type A query | grep Consistent

# List all RDFG groups — confirm group number and mode
symcfg list -rdfg all

# Check DSE state (a full DSE at failover time means more data exposure)
symrdf -g 20 -type A query -detail | grep DSE
```

If R2 is in `Transmitting` state at the moment of failover, the current cycle in flight will be discarded. RPO will be one full cycle older than the lag counter shows. Confirm this with stakeholders before proceeding.

## Failover Execution

```bash
# Planned failover — reverses replication after split
symrdf -g 20 -type A failover -establish -noprompt

# Unplanned failover — R2 becomes writable (primary site down)
symrdf -g 20 -type A failover -noprompt

# Failover a single device
symrdf -sid 0001 -dev 0B1 -type A failover -noprompt

# Confirm Failed Over state
symrdf -g 20 -type A query
```

After failover, present R2 volumes to DR hosts using the array's storage masking configuration.

## Confirming RPO at Failover Time

```bash
# Immediately after failover, record the cycle timestamp
symrdf -g 20 -type A query -detail | grep -E "Cycle Time|Completed|Lag"

# The "Last Consistent" timestamp is the effective recovery point
symrdf -g 20 -type A query -detail | grep "Last"
```

| RPO Factor | How to Check | Acceptable Threshold |
|---|---|---|
| Cycle lag at failover | `query -detail` Lag field | Depends on SLA; typical < 30 s |
| Cycles lost (in-flight) | Transmitting state at failover | 0-1 cycles |
| DSE overflow data | DSE utilization at failover | Ideally 0% |
| Time since last Consistent | Last Consistent timestamp | Per business RPO agreement |

## Post-Failover Steps

```bash
# Verify R2 devices are Failed Over and accessible
symrdf -g 20 -type A query

# Confirm write access on R2 (run from DR host)
dd if=/dev/zero of=/dev/sdX bs=1M count=10 oflag=direct

# Confirm no unexpected devices still in Consistent/Transmitting
symrdf -g 20 -type A query | grep -v "Failed Over"
```

## Failback and Replication Restoration

```bash
# After primary site recovery: restore R1 from R2
symrdf -g 20 -type A restore -noprompt

# Wait for restore to complete (R1 returns to RW)
symrdf -g 20 -type A query -detail

# Re-establish SRDF/A replication (R1 -> R2)
symrdf -g 20 -type A establish -noprompt

# Confirm Consistent state restored
symrdf -g 20 -type A query
```

## Known Issues and Field Notes

- **Failover refused when DSE is 100% full**: The array may block the failover operation if DSE is completely full and data has not been transmitted. Suspend the group first to stop accumulating writes, then failover.
- **R2 shows stale data at failover**: This is expected with SRDF/A — check the last completed cycle timestamp to determine the actual recovery point and communicate it to application owners.
- **Establish after failback fails with "Invalid device state"**: Ensure the restore has fully completed (pair state returns to Synchronized) before issuing the establish. Attempting establish while restore is in progress will fail.
- **Lag counter does not reset after planned failover with -establish**: After a planned failover that reverses replication, the new R1 (former R2) will show a brief lag as the first cycles are established. This is normal and should clear within 1-2 cycle periods.
