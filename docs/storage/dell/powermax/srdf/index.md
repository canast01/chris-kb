# SRDF Operations

Day-2 operational tasks for SRDF/S (synchronous) and SRDF/A (asynchronous) replication on PowerMax. For architecture and standards, see the [DR section](../../../../disaster-recovery/srdf-s/).

## Check SRDF State

```bash
# List all SRDF groups (RDFGs)
symrdf -sid <sid> list -rdfg all

# Query pair states for a specific RDFG
symrdf -sid <sid> query -rdfg <rdfg_id>

# Check for any pairs not in Synchronized state
symrdf -sid <sid> query -rdfg all | grep -v "Synchronized\|InSync\|^$\|Group\|Pair\|---"

# Detailed view of a specific group
symrdf -sid <sid> list -rdfg <rdfg_id> -v
```

## SRDF/S Pair States

| State | Meaning |
|---|---|
| Synchronized | In sync — normal production state |
| Synchronizing | Catching up — data transfer in progress |
| Suspended | Paused — writes queued on R1 |
| Failed Over | R2 is R/W, R1 is NR — after failover |
| Partitioned | Communication lost between R1 and R2 |
| Split | Deliberately separated — R2 is R/W independently |

## SRDF/A (Asynchronous) Specific

```bash
# Check SRDF/A cycle time and RPO
symrdf -sid <sid> list -rdfg <rdfg_id> | grep -E "Cycle|RPO|Delta"

# Check SRDF/A transmit idle state (DSE)
symrdf -sid <sid> query -rdfg <rdfg_id> | grep -i "Transmit\|Idle\|Active"
```

## Suspend and Resume

```bash
# Suspend SRDF (stops replication — R1 continues to accept writes)
symrdf -sid <sid> -rdfg <rdfg_id> suspend -noprompt

# Resume SRDF (R1 re-syncs to R2)
symrdf -sid <sid> -rdfg <rdfg_id> resume -noprompt

# Resume with consistency check
symrdf -sid <sid> -rdfg <rdfg_id> establish -noprompt
```

## Planned Failover (Swap)

```bash
# Step 1 — Suspend SRDF on R1 side
symrdf -g <dg_name> -sid <r1_sid> suspend -noprompt

# Step 2 — Swap roles (R2 becomes R/W, R1 becomes write-disabled)
symrdf -g <dg_name> -sid <r1_sid> swap -noprompt

# Step 3 — After workload moved to DR site, restore to original direction
symrdf -g <dg_name> -sid <r1_sid> restore -noprompt
```

## Failback

```bash
# After restoring primary site — re-establish sync from R1 to R2
symrdf -g <dg_name> -sid <r1_sid> establish -noprompt

# Wait for synchronization to complete
watch -n 30 "symrdf -sid <r1_sid> query -rdfg <rdfg_id> | grep -v Synchronized"
```

## SRDF Health Check

```bash
# Full RDFG health summary
symrdf -sid <sid> list -rdfg all | grep -E "RDFG|State|Mode|Pairs"

# Check for any groups with errors or issues
symrdf -sid <sid> list -rdfg all | grep -iE "error\|partition\|failed\|suspend" 

# Link utilisation
symstat -sid <sid> list -type rdf -i 10 -c 3
```
