# FlashArray — Access Control

> Roles, permissions, and least privilege access.

## RBAC

Purity//FA uses a fixed set of built-in roles. Custom roles are not supported — map AD groups to these roles based on the principle of least privilege.

| Role | Permissions | Use Case |
|---|---|---|
| `array_admin` | Full read/write access to all array configuration, user management, and data operations | Storage team leads; break-glass admin accounts |
| `storage_admin` | Read/write access to volumes, hosts, host groups, protection groups, and snapshots; cannot modify array-level configuration or user accounts | Storage administrators performing day-to-day provisioning |
| `ops_admin` | Read/write access to operational tasks (start/stop replication, acknowledge alerts, run diagnostics); cannot modify provisioning or array config | Operations team; on-call engineers |
| `readonly` | Read-only access to all array data and configuration; no ability to make changes | Monitoring integrations; audit accounts; read-only access for application teams |

## Assigning Roles

```bash
# Assign a local account to a role
pureadmin setattr --role storage_admin <username>

# Map an AD group to a role
pureadmin setattr --role ops_admin --group "CN=pure-ops,OU=Groups,DC=example,DC=com"

# List all admin accounts and their roles
pureadmin list
```

## API Tokens

```bash
# Create a service account with API token
pureadmin create --role array_admin svc-monitoring
pureadmin apitoken create svc-monitoring
# Copy the token and store in a secrets manager

# List API tokens
pureadmin list --api-token

# Delete an API token
pureadmin delete svc-monitoring --api-token
```

## Least Privilege Guidelines

- Use `storage_admin` for day-to-day provisioning tasks — avoid using `array_admin` for routine work
- Use `readonly` for monitoring integrations (SNMP, Pure1, SIEM integrations)
- Use `ops_admin` for on-call engineers who need to acknowledge alerts and run diagnostics but should not make configuration changes
- Create named accounts for individuals — no shared `pureuser` credentials in production
- Disable the default `pureuser` account after AD/LDAP authentication is validated
- Review and rotate API tokens quarterly; disable tokens for decommissioned service accounts
