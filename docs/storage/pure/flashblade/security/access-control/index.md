# FlashBlade — Access Control

> Part of the [FlashBlade Security](../) reference.

---

## RBAC

Purity//FB uses role-based access control with the following built-in roles:

| Role | Permissions | Use Case |
|---|---|---|
| `array_admin` | Full administrative access including system configuration, user management, and protocol settings | Array administrators responsible for full platform management |
| `storage_admin` | Manage filesystems, buckets, snapshots, and replication; cannot modify system or user configuration | Storage operations team creating and managing data resources |
| `ops_admin` | Read access plus ability to acknowledge and resolve alerts; cannot modify configuration | Operations centre staff performing monitoring and alert response |
| `readonly` | Read-only access to all configuration and status information | Auditors, capacity planners, and monitoring integrations |

To list current user accounts and roles:

```bash
purefb user list
```

SAML 2.0 SSO integration is supported for mapping IdP groups to Purity roles. Configure under **Settings > Access > SSO** in the Purity//FB GUI.
