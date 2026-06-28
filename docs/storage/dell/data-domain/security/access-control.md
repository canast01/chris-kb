---
tags:
  - dell
  - security
---
# Dell Data Domain Access Control
![Dell Data Domain Access Control](../../../../assets/storage-dell-data-domain-security-access-control.svg)


```bash
# Create a user and assign a role
user add <username> role backup-operator

# Assign LDAP group to a role
authentication roles assign role backup-operator group <ldap-group-name>

# List current users and roles
user show
```


```d2
direction: down

external: External / Untrusted {shape: rectangle}
perimeter_controls: "Perimeter Controls" {shape: rectangle}
identity_access: "Identity & Access" {shape: rectangle}
audit_logging: "Audit & Logging" {shape: rectangle}
core: "Data Domain Core" {shape: hexagon}

external -> perimeter_controls: traffic in
perimeter_controls -> identity_access
identity_access -> audit_logging
audit_logging -> core: secured path
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Data Domain — Authentication](authentication/)
- [Data Domain — Hardening](hardening/)
- [Data Domain — Encryption](encryption/)
