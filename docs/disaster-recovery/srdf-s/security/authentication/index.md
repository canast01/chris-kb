# SRDF/S — Authentication

> Part of the [SRDF/S Security](../index.md) reference.

---

## Solutions Enabler RBAC

Control who can execute SRDF failover and resync operations:

```bash
# List current user roles
symauth -sid <SID> list

# Add DR operator role — failover-capable, scoped to specific SRDF groups
symauth -sid <SID> add -username svc_dr_ops -role StorageAdmin -scope rdfg:<group_number>

# Add monitoring account — read-only
symauth -sid <SID> add -username svc_monitoring -role StorageMonitor
```
