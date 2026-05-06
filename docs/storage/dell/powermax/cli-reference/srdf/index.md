# SRDF — Replication

> Part of the Dell PowerMax CLI Reference (SYMCLI).

---

```bash
# List SRDF groups
symrdf -sid <sid> list
symrdf -sid <sid> -rdfg <rdfg_num> list
symrdf -sid <sid> -rdfg <rdfg_num> query

# Device group operations (requires a DG or SG)
symrdf -sid <sid> -sg <sg_name> query
symrdf -sid <sid> -sg <sg_name> establish
symrdf -sid <sid> -sg <sg_name> split
symrdf -sid <sid> -sg <sg_name> suspend
symrdf -sid <sid> -sg <sg_name> resume
symrdf -sid <sid> -sg <sg_name> update
symrdf -sid <sid> -sg <sg_name> failover
symrdf -sid <sid> -sg <sg_name> failback
symrdf -sid <sid> -sg <sg_name> swap
symrdf -sid <sid> -sg <sg_name> verify

# SRDF/A specific
symrdf -sid <sid> -sg <sg_name> query -srdf_a
symrdf -sid <sid> -rdfg <rdfg_num> verify -srdf_a

# SRDF cycle / lag info
symrdf -sid <sid> -rdfg <rdfg_num> list -v
```
