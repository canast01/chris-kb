# PowerMax — Access Control

## RBAC

Unisphere for PowerMax roles:

| Role | Permissions |
|---|---|
| `StorageAdmin` | Full read/write on storage provisioning (storage groups, masking views, pools, SnapVX, SRDF). No access to security or user management. |
| `SecurityAdmin` | Manage users, roles, certificates, and LDAP configuration. Cannot provision storage. |
| `Operator` | Read/write on routine operations (alert acknowledgement, scheduled tasks). Cannot create or delete storage objects. |
| `Monitor` | Read-only across all array objects; can view performance data. No configuration changes. |
| `StorageAdminLocal` | Same as StorageAdmin but scoped to a specific SID; used for delegating single-array management. |

Solutions Enabler CLI roles are controlled by the `daemon_users` file and OS-level permissions on the SE host. Restrict root-level SE access to operations accounts only.
