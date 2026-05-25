# RecoverPoint — Access Control

> Part of the [RecoverPoint](../../index.md) > [Security](../index.md) reference.

---

## Role-Based Access Control

RecoverPoint has three built-in roles. Use individual named accounts, never shared credentials:

| Role | Capabilities |
|---|---|
| Administrator | Full configuration, failover, and system management |
| Security Officer | User management, audit log access — cannot change replication config |
| Monitor | Read-only; can view CG status, RPA health, and lag metrics |

Create accounts via RecoverPoint Management Console → System Settings → Users:

```bash
# Via RecoverPoint CLI
add_user -u svc_monitoring -r monitor -p '<password>'
add_user -u svc_srm_integration -r admin -p '<password>'
```
