---
tags:
  - dell
  - security
---
# Dell Data Domain Access Control

*Applies to: Dell EMC Storage*
![Dell Data Domain Access Control](../../../../../assets/storage-dell-data-domain-security-access-control.svg)

```bash
# Create a user and assign a role
user add <username> role backup-operator

# Assign LDAP group to a role
authentication roles assign role backup-operator group <ldap-group-name>

# List current users and roles
user show
```


```text title="Expected output"
User <username> added successfully
Role backup-operator assigned to group <ldap-group-name>

Username                Role                  Status
admin                   system-admin          active
backup-svc              backup-operator       active
<username>              backup-operator       active
restore-user            restore-operator      active
audit-admin             audit-admin           active
```

!!! warning "Common errors"
    **`Error: User <username> already exists`** — Choose a different username or delete the existing user with `user remove <username>` first.
    **`Error: Role backup-operator not found`** — Verify the role name is correct; use `authentication roles show` to list available roles.
    **`Error: LDAP group <ldap-group-name> not found or not configured`** — Ensure LDAP authentication is configured and the group exists in your directory with `authentication show`.
## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Data Domain — Authentication](../authentication/)
- [Data Domain — Hardening](../hardening/)
- [Data Domain — Encryption](../encryption/)
