# SRDF/A — Access Control

> Part of the [SRDF/A](../../index.md) reference.

---

## Solutions Enabler RBAC

Solutions Enabler v9+ enforces role-based access at the array scope. Roles for SRDF operations:

| Role | Permitted Operations |
|---|---|
| `StorageAdmin` | symrdf failover, establish, split, suspend |
| `StorageMonitor` | symrdf query, list — read-only |
| `Audit` | Read-only access to audit logs |

Create a dedicated service account per automation system; never use the root Solutions Enabler account:

```bash
symauth -sid <SID> add -username svc_dr_automation -role StorageAdmin -scope rdfg:<group_number>
```

---

## Preventing Accidental Resync

For async operations, accidentally re-syncing from target to source (after a failover test) destroys production data. Guard against this:

- Set SYMCLI session to confirm mode for destructive operations: `SYMCLI_CONFIRM=prompt`
- Restrict `symrdf restore` and `symrdf establish -full` to a separate break-glass account
- Implement a peer-review process for any SRDF failover in production
