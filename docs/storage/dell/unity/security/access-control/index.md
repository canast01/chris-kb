# Unity — Access Control

## RBAC

Unisphere for Unity provides role-based access control for all administrative operations.

| Role | Permissions |
|---|---|
| Administrator | Full system access: storage provisioning, system configuration, user management, upgrades |
| Storage Administrator | Storage provisioning operations: create and manage pools, LUNs, filesystems, snapshots, replication |
| Operator | Read access plus limited operational actions: acknowledge alerts, collect service bundles |
| Viewer | Read-only: view health, capacity, configuration; cannot make any changes |

Configure users and role assignments in Unisphere under **Settings > Access > Users**. Use LDAP/AD group-to-role mapping to manage Unisphere access via your directory service rather than managing local accounts individually.
