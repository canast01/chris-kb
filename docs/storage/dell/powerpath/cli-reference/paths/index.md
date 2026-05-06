# Paths

> Part of the Dell PowerPath CLI Reference.

---

```bash
# Count alive paths per device
powermt display dev=all | grep -E "emcpower|alive|dead"

# Restore dead paths
powermt restore

# Remove dead paths
powermt remove dead

# Path failover
powermt fail dev=emcpower<n> path=<hba_port>

# Unblock a failed path
powermt unblock dev=emcpower<n> path=<hba_port>
```
