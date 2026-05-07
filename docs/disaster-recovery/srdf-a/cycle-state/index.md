# SRDF/A Cycle State

## Overview

SRDF/A (asynchronous) replication uses a **delta-set / cycle** model instead of per-write synchronous commit. Writes are accumulated in an in-memory delta set on the R1 array during a cycle period (typically 30 seconds). At the end of each cycle the delta set is transmitted to the R2 array and applied atomically. This guarantees R2 is always in a crash-consistent state corresponding to a previous cycle boundary.

The **cycle state** describes what the array is currently doing with the delta sets. Monitoring cycle state is the primary way to assess SRDF/A health.

## Cycle State Definitions

| Cycle State | Description | Impact |
|---|---|---|
| Consistent | R2 is up to date to the last completed cycle | Normal; RPO = last cycle time |
| Transmitting | Current delta set is being sent to R2 | Normal; transmission in progress |
| Awaiting Cycle | Array is accumulating writes; cycle timer running | Normal steady-state |
| Suspended | Replication paused; no cycles transmitting | R2 stale; RPO growing |
| Failed Over | R1 unavailable; R2 made writable | Production on R2 |
| DSE Active | Delta Set Extension activated; cache overflow to DSE device | High write load; monitor closely |
| Inconsistent | R2 cannot be brought to a consistent state | Immediate investigation required |

## Querying Cycle State

```bash
# Show cycle state for all devices in an SRDF/A group
symrdf -g 20 -type A query

# Detailed view including cycle time and lag
symrdf -g 20 -type A query -detail

# Show cycle statistics: cycle time, bytes, completion status
symrdf -g 20 -type A query -detail | grep -E "Cycle|Delta|Lag"

# List all RDFG groups and confirm which are type A
symcfg list -rdfg all

# Show DSE device assignment for a group
symcfg list -rdfg 20 -detail | grep DSE
```

## Cycle Time Configuration and Monitoring

The cycle time controls how frequently delta sets are transmitted. A shorter cycle time reduces RPO but increases overhead. Default is 30 seconds.

```bash
# Check current configured cycle time
symcfg list -rdfg 20 -detail | grep "Cycle Time"

# Monitor consecutive cycle completions (10 cycles)
for i in $(seq 1 10); do
  symrdf -g 20 -type A query -detail | grep "Cycle"
  sleep 30
done

# Check if cycles are completing within the configured window
symrdf -g 20 -type A query -detail | grep -E "Cycle Time|Completed"
```

## DSE (Delta Set Extension) Management

DSE activates when write traffic exceeds the in-memory delta set capacity. DSE uses a dedicated storage device as overflow:

```bash
# Check if DSE is active
symrdf -g 20 -type A query -detail | grep DSE

# List DSE device details
symcfg list -rdfg 20 -detail | grep -A5 "DSE"

# Monitor DSE utilization percentage
symstat -rdf -g 20 -i 5 -c 6 | grep DSE
```

If DSE utilization climbs above 70%, throttle application write I/O or investigate whether the cycle time needs adjustment.

## Cycle State Troubleshooting

```bash
# Identify stuck or excessively long cycles
symrdf -g 20 -type A query -detail | grep -E "Cycle Age|Elapsed"

# Force cycle completion during maintenance
symrdf -g 20 -type A suspend -noprompt
symrdf -g 20 -type A resume -noprompt

# Check for Inconsistent state
symrdf -g 20 -type A query | grep Inconsistent

# Resume from Suspended (starts new cycle)
symrdf -g 20 -type A resume -noprompt
```

## Known Issues and Field Notes

- **Cycles consistently longer than cycle time setting**: Indicates the link cannot keep up with the write workload. Check link utilization with `symstat -rdf` and consider increasing the cycle time or adding RDF director bandwidth.
- **DSE fills up and triggers Suspended state**: The array suspends SRDF/A automatically if DSE reaches 100%. This is a protection mechanism. Immediately investigate write I/O spike and resume replication as soon as DSE drains.
- **Inconsistent state after network outage**: If the link drops during a transmission, the partially transmitted delta set is discarded. Replication resumes from the next cycle boundary on link recovery. Confirm `Consistent` state before measuring RPO.
- **Cycle state shows Consistent but RPO is growing**: This paradox occurs if the cycle time itself is increasing (e.g., cycles taking 5 minutes instead of 30 seconds). Monitor cycle elapsed time, not just the Consistent indicator.
