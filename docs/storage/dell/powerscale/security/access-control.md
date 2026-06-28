---
tags:
  - dell
  - security
---
# PowerScale — Access Control

<div class="kb-summary">
Roles, permissions, and least privilege access for Dell PowerScale.

*Applies to: PowerScale (Isilon) 9.x*
</div>
![PowerScale — Access Control](../../../../assets/storage-dell-powerscale-security-access-control.svg)

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## RBAC

PowerScale uses role-based administration for cluster management:

| Role | Permissions |
|---|---|
| `SystemAdmin` | Full cluster administration including security, users, and hardware |
| `AuditAdmin` | Read access to all audit logs and events; cannot change configuration |
| `BackupAdmin` | Permission to read all files for backup purposes (NDMP/snapshot) regardless of file ACLs |
| `VMwareAdmin` | Access to VMware-related cluster functions (vVols, VAAI) |
| `SecurityAdmin` | Manage authentication providers, zones, and user role assignments |
| `ISI_PRIV_AUTH` | Privilege to manage authentication configuration (AD, LDAP, NIS) |
| `ISI_PRIV_SNAPSHOT` | Privilege to create and manage SnapshotIQ policies |
| `ISI_PRIV_SYNCIQ` | Privilege to manage SyncIQ replication policies |

Create custom roles and assign specific privileges:
```bash
isi auth roles create --name ReadOnlyMonitor --description "Read-only cluster monitoring"
isi auth roles modify ReadOnlyMonitor --add-priv ISI_PRIV_LOGIN_CONSOLE
isi auth roles modify ReadOnlyMonitor --add-priv ISI_PRIV_STATISTICS
isi auth roles modify ReadOnlyMonitor --add-user <username>
```

## Access Zones

Access zones partition the cluster into separate namespaces — each with its own NFS exports, SMB shares, and authentication providers:

```bash
# List zones
isi zone zones list
isi zone zones view <zone_name>

# Create a zone
isi zone zones create <zone_name> --path /ifs/<path>

# Assign auth providers to a zone
isi zone zones modify <zone_name> --add-auth-providers <provider>
```

## Audit Logging

```bash
# Enable protocol audit logging (NFS, SMB events)
isi audit settings global modify --auditing-enabled true

# View audit configuration
isi audit settings global view

# Set syslog forwarding for audit events
isi audit settings global modify \
  --cee-server-uri http://siem.example.com:12228/cee

# View recent audit log entries (protocol access events)
isi audit log view
```

- Audit events cover: file open, read, write, delete, rename, permission change, and authentication events.
- Forward to a syslog receiver or a Dell Common Event Enabler (CEE) API endpoint for SIEM integration.
- Retain audit logs for a minimum of 12 months; 24 months for regulated environments.

## Compliance Notes

| Framework | Relevant Control | PowerScale Capability |
|---|---|---|
| PCI-DSS | Requirement 3 (data at rest encryption) | SED-based AES-256 encryption |
| PCI-DSS | Requirement 10 (audit logging) | Protocol and admin audit logging via CEE |
| HIPAA | §164.312 (access control) | Access zones, RBAC, and per-share ACLs |
| GDPR | Article 32 (security of processing) | Encryption in transit (SMB3, SyncIQ TLS) and at rest (SED) |
| ISO 27001 | A.9 (access control) | RBAC roles, AD/LDAP integration, root squash on NFS |

---

## See also

- [Powerscale — Authentication](authentication/)
- [Powerscale — Hardening](hardening/)
- [Powerscale — Encryption](encryption/)
