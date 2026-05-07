# SRDF/S Failover

## Overview

SRDF/S failover transfers I/O ownership from the R1 (source) volume to the R2 (target) volume on the remote PowerMax array. Because SRDF/S is synchronous, every write acknowledged to the host has already been committed on both sides, so RPO at the moment of failover is zero. Failover is invoked when the primary site is unavailable or during a planned DR test.

Two modes exist: **failover** (splits the pair and makes R2 read/write) and **failover -establish** (for a planned switch where the primary site remains available and replication is immediately reversed).

## Pre-Failover Checklist

Before initiating failover confirm the following on the R1 (source) array:

```bash
# Confirm all pairs in the group are Synchronized
symrdf -g 10 query

# Show detailed pair state and track percent
symrdf -g 10 query -detail

# List all RDFG groups on the array
symcfg list -rdfg all

# Confirm RDF director port status
symcfg list -dir all -rdf

# Show device-level SRDF info for the group
symrdf -g 10 list -v
```

Do not proceed if any device shows `SyncInProg`, `Transmit Idle`, or a track count above zero unless the business decision is to accept data loss.

## Failover Execution

```bash
# Planned failover (site still accessible — reverses replication after split)
symrdf -g 10 -type S failover -establish -noprompt

# Unplanned failover (primary site down, R2 made writable)
symrdf -g 10 -type S failover -noprompt

# Failover a single device instead of the full group
symrdf -sid 0001 -dev 0A1 failover -noprompt

# Verify R2 devices are now in Failed Over state
symrdf -g 10 query
```

After failover the R2 devices transition to **Failed Over** state and become writable. Present them to hosts at the DR site using standard storage masking procedures.

## Post-Failover Validation

```bash
# Confirm Failed Over state on all devices
symrdf -g 10 query | grep -E "R2|Pair State"

# Check for any devices still in inconsistent state
symrdf -g 10 query | grep -iv "Failed Over"

# Confirm no residual tracks needing flush
symrdf -g 10 query -detail | grep "Tracks"

# Verify host I/O at DR site (run from DR host)
dd if=/dev/sdX of=/dev/null bs=1M count=100 iflag=direct
```

| Check | Expected State | Action if Different |
|---|---|---|
| Pair State | Failed Over | Re-run failover or contact Dell support |
| Invalid Tracks | 0 | Allow sync to complete before failover |
| R2 Write Access | Enabled | Check masking view on DR array |
| RDF Director | Online | Check physical link and port config |
| Host I/O | Responding | Confirm zoning and host masking |

## Failback Preparation

Once the primary site is recovered, restore replication before failing back:

```bash
# After primary site recovery: restore R1 devices (accepts R2 data back)
symrdf -g 10 -type S restore -noprompt

# Confirm Synchronized state restored
symrdf -g 10 query

# Switch back to R1 (optional planned failback)
symrdf -g 10 -type S failover -establish -noprompt
```

## Known Issues and Field Notes

- **Extended RDF link latency before failover**: If the link was degraded and pairs went to `Transmit Idle` prior to the outage, some tracks may be out of sync. Run `symrdf -g <rdfg> query -detail` and check `Invalid Tracks` before proceeding.
- **Failover refused with "SYMAPI not ready"**: Ensure Solutions Enabler is running on the host issuing the command and that it has LUN access to the array management device (gatekeeper).
- **R2 remains read-only after failover**: Verify the array-side masking view includes the DR host's initiators. Failover changes the pair state but does not modify host masking.
- **Split-brain risk**: Never fail over while R1 is still accessible to production hosts without first quiescing I/O and confirming the R1 host is offline.
