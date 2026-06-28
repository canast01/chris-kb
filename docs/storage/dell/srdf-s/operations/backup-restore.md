---
tags:
  - dell
  - operations
---
# SRDF/S — Backup & Restore
![SRDF/S — Backup & Restore](../../../../assets/storage-dell-srdf-s-operations-backup-restore.svg)


```bash
# Query SRDF state for a storage group
symrdf -sg PROD_SG query

# Detailed output including track counts and sync %
symrdf -sg PROD_SG query -detail

# Query by RDF group number
symrdf list -rdfg <rdf_group_number> -detail
```

```bash
# Suspend SRDF replication (I/O continues on R1, no longer replicated)
symrdf -sg PROD_SG suspend

# Query suspended state
symrdf -sg PROD_SG query
# R1 St = WD, Link = Suspended
```
```bash
# Resume SRDF — re-syncs changed tracks from R1 to R2
symrdf -sg PROD_SG resume

# Monitor sync progress — watch Tracks/% fields
symrdf -sg PROD_SG query -detail
```
```bash
# 1. Verify R1 array and volumes are accessible
symdev list -sid <R1_SID> | grep <device_range>

# 2. Restore — overwrites R1 with R2 content, then flips direction
#    This is a DESTRUCTIVE operation on R1 volumes — confirm before running
symrdf -sg PROD_SG restore -force

# 3. Monitor resync from R2 to R1
symrdf -sg PROD_SG query -detail
# Watch: Sync% and Invalid Tracks decrease

# 4. Wait for full synchronization
symrdf -sg PROD_SG verify -consistent

# 5. Confirm synchronized — then fail back to R1
symrdf -sg PROD_SG failover
# Now R1 is promoted back to RW, R2 returns to WD

# 6. Start production workloads on R1
```
```bash
# establish syncs from the current "source" (post-failover this is R2) to R1
symrdf -sg PROD_SG establish -force
```

```d2
direction: right

hub: "SRDF/S\nOperations" {shape: hexagon}
verify: "Verify" {shape: rectangle}

hub -> verify
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Srdf S — Procedures](procedures/)
- [Srdf S — Health Checks](health-checks/)
- [Srdf S — Common Issues](../troubleshooting/common-issues/)
