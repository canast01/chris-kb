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

Built-in roles:
| Role | Capabilities |
|---|---|
| NBU_Admin | Full NetBackup administration |
| NBU_Operator | Start/stop jobs; no policy configuration |
| NBU_Vault_Operator | Vault and tape management |
| NBU_User | Restore own data (self-service) |
| NBU_SAN_Admin | SAN client and storage configuration |

Map AD groups to NBAC roles:
```bash
nbac_admin -add_user -user "domain\\nbu_admins" -role NBU_Admin
nbac_admin -add_user -user "domain\\nbu_operators" -role NBU_Operator
```
