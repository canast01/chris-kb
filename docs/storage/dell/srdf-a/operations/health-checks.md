---
tags:
  - dell
  - operations
---
# SRDF/A — Health Checks

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


```text title="Expected output"
Symmetrix ID: 000123456789012
Group Number: 20
SRDF/A Pair Information
===============================================
Dev  Sym ID         State           Lag(ms)  Cycle Age(s)
---  -------        -----           -------  -----------
000  000123456789   Consistent      45       120
001  000123456789   Consistent      42       120
002  000123456789   Consistent      48       120
003  000123456789   Consistent      46       120
...

Current lag: 48 seconds
```

!!! warning "Common errors"
    **`symrdf: Command not found`** — Ensure the Symmetrix management tools are installed and the PATH includes the bin directory (typically `/opt/emc/SYMCLI/bin`).
    **`SRDF group 20 not found`** — Verify the group number exists with `symrdf list` and confirm the local Symmetrix is the source array for that group.
    **`Lag: N/A`** — The SRDF pair may be in a non-replicating state (Paused, Failed, or Idle); check full state with `symrdf -g 20 -type A query -detail` and resume replication if needed.
## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

1. **SRDF group state:** `symrdf -g <group> query` — all pairs should show RDF State: Synchronized or Consistent
2. **Cycle time:** `symrdf -g <group> query -detail | grep -i cycle` — verify within RPO target
3. **Delta sets:** `symrdf -g <group> dset show` — check no delta set is accumulating unexpectedly
4. **Link health:** `symrdf -g <group> verifylink` — verify physical paths are all healthy
5. **DSE (Dynamic Synchronization Enabler) status:** `symrdf -g <group> dse query` — check DSE mode active if configured
6. **WAN latency impact:** `symrdf -g <group> perf` — check cycle time trend vs WAN latency
7. **SRDF director health:** `symmaskdb -sid <array-sid> list -dir` — all RDF directors should show Status: Online
8. **Emulation (if synchronous fallback configured):** `symrdf -g <group> query | grep -i mode` — note current mode
9. **Consistency protection:** `symrdf -g <group> query | grep -i protect` — verify consistency protection active
10. **Open replication tracks:** `symrdf -g <group> query | grep -i tracks` — should approach 0 for healthy async

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
```d2
direction: right

startCheck: "Daily Health Check Start" {shape: rectangle}
checkPairState: "Check Pair States\nsymrdf -g 20 -type A query" {shape: rectangle}
allConsistent: "allConsistent" {shape: rectangle}
checkLag: "Check Lag Value\nsymrdf -g 20 -type A query -detail | grep Lag" {shape: rectangle}
investigatePair: "Investigate Pair State\nCheck for link/network issues" {shape: rectangle}
escalate: "Escalate to Storage / Network Team" {shape: rectangle}
lagOk: "lagOk" {shape: rectangle}
checkDSE: "Check DSE Utilization\nsymstat -rdf -g 20 | grep DSE" {shape: rectangle}
investigateLag: "Investigate Lag Growth\nCheck write rate and link utilization" {shape: rectangle}
dseOk: "dseOk" {shape: rectangle}
checkLink: "Check RDF Link\nsymcfg list -rdfg 20 -detail" {shape: rectangle}
investigateDSE: "Investigate DSE\nCheck for write burst or undersized DSE device" {shape: rectangle}
linkOnline: "linkOnline" {shape: rectangle}
allHealthy: "All Checks Passed\nDocument in log" {shape: rectangle}

startCheck -> checkPairState
checkPairState -> allConsistent
allConsistent -> checkLag
allConsistent -> investigatePair
investigatePair -> escalate
checkLag -> lagOk
lagOk -> checkDSE
lagOk -> investigateLag
investigateLag -> escalate
checkDSE -> dseOk
dseOk -> checkLink
dseOk -> investigateDSE
investigateDSE -> escalate
checkLink -> linkOnline
linkOnline -> allHealthy
linkOnline -> escalate
```

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Srdf A — Procedures](../procedures/)
- [Srdf A — CLI Reference](../cli-reference/)
- [Srdf A — Common Issues](../../troubleshooting/common-issues/)
