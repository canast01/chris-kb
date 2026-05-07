# SRDF/S Health Checks

## Overview

Regular health checks on SRDF/S replication confirm that all device pairs are synchronized, RDF directors and links are operational, and no track backlogs exist. These checks should run daily as part of infrastructure monitoring and immediately before any planned failover or maintenance activity.

Health checks cover four layers: pair state, link/director status, performance metrics, and array-level configuration consistency.

## Daily Pair State Check

```bash
# Check all pairs in each active RDFG group
symrdf -g 10 query
symrdf -g 11 query

# Show all RDFG groups and their link state
symcfg list -rdfg all

# Detailed check including track counts (expect 0 for all Synchronized pairs)
symrdf -g 10 query -detail

# Identify any device not Synchronized
symrdf -g 10 query | grep -iv synchronized
```

Any pair showing a state other than `Synchronized` or `Transmit Idle` requires investigation before the next maintenance window.

## RDF Director and Link Health

```bash
# List RDF directors and port status on local array
symcfg list -dir all -rdf

# Show detailed director configuration
symcfg show -dir RF-1F -v

# Query RDF link statistics (bandwidth, utilization)
symstat -rdf -dir RF-1F -i 5 -c 3

# Check remote array connectivity
symcfg list -rdfg 10 -detail

# Confirm remote array is reachable via SYMAPI
symcfg list -v | grep -A2 "Remote"
```

## Performance and Throughput Metrics

```bash
# Monitor RDF write throughput and latency (5-second intervals, 6 samples)
symstat -rdf -i 5 -c 6

# Check for any bandwidth saturation on RDF ports
symstat -rdf -dir RF-1F -type port

# Review historical performance data
symstat -rdf -start_time "2026-05-07 08:00:00" -end_time "2026-05-07 09:00:00"

# Check host-side write latency impact from synchronous commit
symstat -type device -dev 0A1 -i 5 -c 3
```

## Configuration Consistency Check

```bash
# Confirm RDFG group membership matches expected device list
symrdf -g 10 list -v

# Verify OLPAIRS (Online Pair) configuration
symrdf -g 10 query -detail | grep OLPAIRS

# Check SRDF/S mode is correctly set (not accidentally changed to /A)
symcfg list -rdfg 10 -detail | grep "SRDF Mode"

# Confirm both arrays have matching group numbers
symcfg list -rdfg all
```

## Health Check Summary Table

| Check | Command | Healthy Result | Alert Threshold |
|---|---|---|---|
| Pair state | `symrdf -g <rdfg> query` | All Synchronized | Any non-Synchronized |
| Invalid tracks | `symrdf -g <rdfg> query -detail` | 0 tracks | > 0 tracks |
| RDF director | `symcfg list -dir all -rdf` | Online | Any Offline/Failed |
| Link utilization | `symstat -rdf` | < 80% sustained | > 80% for > 5 min |
| Remote connectivity | `symcfg list -rdfg <n> -detail` | Link Online | Link Offline/Partitioned |

## Known Issues and Field Notes

- **Intermittent "Transmit Idle" during off-peak hours**: Normal behaviour when there are no writes to replicate. Does not indicate a problem. Confirm by checking that track count remains 0.
- **Director shows Online but link shows Partitioned**: Usually a transient WAN interruption. Wait 2 minutes and re-query. If it persists, escalate to network team to check the dark fibre or IP WAN path.
- **Health check script timeouts on large arrays**: If `symcfg list -rdfg all` takes > 60 seconds, break queries into per-group calls and parallelize across RDFG groups using a shell loop.
- **Mismatched device counts between R1 and R2**: Investigate immediately — indicates a pairing configuration error. Use `symrdf -g <rdfg> list -v` on both arrays to compare device lists.
