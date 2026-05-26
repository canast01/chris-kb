# NetBackup — Access Control

## NetBackup Access Control (NBAC)

NBAC provides role-based access using OS groups or LDAP/AD integration:

```bash
# Enable NBAC (requires restart of NetBackup services)
nbac_admin -enable

# List current NBAC users and roles
nbac_admin -list_users
nbac_admin -list_roles
```
