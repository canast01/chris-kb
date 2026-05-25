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

| Role | Allowed Commands | Prohibited Commands |
|---|---|---|
| `StorageAdmin` | symrdf failover, establish, split, suspend, set mode | — |
| `StorageMonitor` | symrdf query, symcfg list | All state-changing ops |

Never assign `StorageAdmin` to automated monitoring or backup accounts.

---

## Management API Authentication

The Unisphere REST API should use dedicated service accounts:

- Use client certificate authentication for service accounts
- Scope API accounts to minimum required capabilities
- Rotate service account certificates annually

Verify TLS configuration:
```bash
curl -k https://<unisphere>:8443/univmax/restapi/system/version
# Production systems should use trusted CA cert (remove -k flag)
```
