# SRDF — Replication

> Part of the Dell PowerMax CLI Reference (SYMCLI).

SRDF (Symmetrix Remote Data Facility) provides synchronous and asynchronous replication between PowerMax arrays.

## SRDF Modes

| Mode | Description | RPO |
|---|---|---|
| SRDF/S (Synchronous) | Write acknowledged only after replicated | Zero |
| SRDF/A (Asynchronous) | Writes batched and replicated in cycles | Seconds to minutes |
| SRDF/Metro | Active-active with zero RPO | Zero |

## List SRDF Groups and Devices

```bash
# List all SRDF groups on the array
symrdf -sid <sid> list

# List devices in a specific SRDF group
symrdf -sid <sid> -rdfg <rdfg_num> list

# Query status of all devices in an SRDF group
symrdf -sid <sid> -rdfg <rdfg_num> query
```

## Storage Group Operations

```bash
# Query SRDF status for an SG
symrdf -sid <sid> -sg <sg_name> query

# Establish (start replication)
symrdf -sid <sid> -sg <sg_name> establish

# Split (make R2 writable — local copy for testing)
symrdf -sid <sid> -sg <sg_name> split

# Suspend replication
symrdf -sid <sid> -sg <sg_name> suspend

# Resume replication after suspend
symrdf -sid <sid> -sg <sg_name> resume

# Force a delta resync
symrdf -sid <sid> -sg <sg_name> update

# Planned failover (R2 becomes primary)
symrdf -sid <sid> -sg <sg_name> failover

# Failback to original R1
symrdf -sid <sid> -sg <sg_name> failback

# Swap R1/R2 roles
symrdf -sid <sid> -sg <sg_name> swap

# Verify consistency
symrdf -sid <sid> -sg <sg_name> verify
```

## SRDF/A Specific

```bash
# Query SRDF/A cycle and lag info
symrdf -sid <sid> -sg <sg_name> query -srdf_a
symrdf -sid <sid> -rdfg <rdfg_num> verify -srdf_a

# Show SRDF/A cycle details (lag time, delta)
symrdf -sid <sid> -rdfg <rdfg_num> list -v
```

## Common Issues

| Issue | Check | Action |
|---|---|---|
| SRDF link down | RDF group connectivity | Check inter-array FC links |
| High SRDF/A lag | Bandwidth or I/O burst | Monitor cycle time; increase bandwidth |
| Split failed | Existing split | Check device state |
| Failover won't complete | Ongoing I/O | Suspend writes to R1 first |
