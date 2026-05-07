# SRDF/A Health Checks

## Overview

SRDF/A health checks verify that asynchronous replication cycles are completing on schedule, lag is within SLA, DSE is not under pressure, and RDF links are stable. Unlike SRDF/S where the primary indicator is pair synchronization, SRDF/A health is primarily measured by **cycle completion rate** and **lag time**. Run these checks daily and always before any planned activity that touches the DR environment.

## Cycle and Lag Status Check

```bash
# Show cycle state and lag for all devices in group 20
symrdf -g 20 -type A query -detail

# Quick summary — look for Consistent state on all devices
symrdf -g 20 -type A query

# Check lag value specifically
symrdf -g 20 -type A query -detail | grep -E "Lag|Cycle Age"

# Compare lag against SLA threshold (example: alert if > 60 seconds)
LAG=$(symrdf -g 20 -type A query -detail | grep "Lag" | awk '{print $NF}')
echo "Current lag: ${LAG} seconds"
```

## RDF Link and Director Health

```bash
# Check RDF director and port status
symcfg list -dir all -rdf

# Show bandwidth utilization on RDF ports
symstat -rdf -dir RF-2F -i 5 -c 3

# Check link state for SRDF/A group
symcfg list -rdfg 20 -detail

# Confirm remote array is accessible
symcfg list -rdfg 20 -detail | grep "Link"

# Show all RDFG groups (confirm group 20 is type A)
symcfg list -rdfg all
```

## DSE Health Check

DSE (Delta Set Extension) is a spill device that absorbs write bursts when the in-memory delta set is full. A non-zero DSE utilization indicates write workload is exceeding baseline expectations.

```bash
# Check DSE device and utilization
symcfg list -rdfg 20 -detail | grep -A5 "DSE"

# Monitor DSE utilization over time
symstat -rdf -g 20 -i 10 -c 6 | grep DSE

# Check DSE device capacity
symdev show <DSE_devnum> -v | grep -E "Capacity|Track"
```

## Health Check Summary

```bash
# Full health check — save output with timestamp
symrdf -g 20 -type A query -detail > /tmp/srdf_a_health_$(date +%Y%m%d_%H%M%S).txt

# Check for any non-Consistent devices
symrdf -g 20 -type A query | grep -iv "consistent\|transmitting\|await"

# Check cycle completion statistics across all type-A groups
for rdfg in 20 21 22; do
  echo "=== RDFG ${rdfg} ===" 
  symrdf -g ${rdfg} -type A query | tail -5
done
```

## Health Status Reference Table

| Metric | Healthy | Warning | Critical |
|---|---|---|---|
| Cycle state | Consistent / Transmitting | Awaiting Cycle > 2x cycle time | Suspended / Inconsistent |
| Lag | < configured cycle time | 2-5x cycle time | > 5x cycle time or SLA breach |
| DSE utilization | 0% | > 30% | > 70% or Full |
| RDF link | Online | Marginal (> 80% utilization) | Offline / Partitioned |
| Cycle duration | <= configured cycle time | 1.5x cycle time | > 2x cycle time |

## Known Issues and Field Notes

- **Lag spikes during backup windows**: Backup jobs generating large sequential writes can push DSE into active use and extend cycle times. Coordinate backup schedules with the storage team to avoid overlap with SRDF/A monitoring windows.
- **Cycle state shows Consistent but lag is growing**: This usually means cycles are completing but taking longer than the configured cycle time. The Consistent flag refers to the last completed cycle, not the current one. Review `Cycle Age` in the detailed query output.
- **Health check script hangs on large RDFG groups**: Increase the SYMAPI timeout in `/var/symapi/config/daemon_options` if queries time out on groups with > 500 devices.
- **DSE jumps from 0 to 80% overnight**: Points to a batch job or database maintenance task generating large write bursts. Work with the application team to stagger jobs across the week or adjust DSE device size.
