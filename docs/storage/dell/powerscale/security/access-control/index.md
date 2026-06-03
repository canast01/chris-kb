# PowerScale — Access Control


<div class="kb-summary">
> Roles, permissions, and least privilege access for Dell PowerScale.
</div>
```text
┌────────────────────────────────── Dell PowerScale — Access Control ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        PowerScale access control: RBAC roles, least-privilege, and access audit logging       │   │
│   │        Roles: admin (full), operator (read/modify), read-only (view); map to AD groups        │   │
│   │       Authentication: local accounts, LDAP/AD integration, and MFA for privileged users       │   │
│   │          Audit: log all admin actions; review access logs monthly; rotate credentials         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Identify user → assign role → enforce MFA → audit → review quarterly                               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │           Function          │   │
│   │              OS             │  │            OneFS            │  │        Distributed FS       │   │
│   │           Tiering           │  │          SmartPools         │  │        Auto data move       │   │
│   │         Replication         │  │            SyncIQ           │  │        Async DR copy        │   │
│   │          Snapshots          │  │          SnapshotIQ         │  │       Space-efficient       │   │
│   │         Load balance        │  │         SmartConnect        │  │       DNS client dist.      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Role       │   Permissions    │       Scope       │       Auth       │   Review cycle   │   │
│   │      Admin       │    Full CRUD     │       Global      │   MFA required   │     Monthly      │   │
│   │     Operator     │   Read/modify    │      Assigned     │   MFA required   │    Quarterly     │   │
│   │    Read-only     │    View only     │      Assigned     │     Password     │    Quarterly     │   │
│   │   Service acct   │     API only     │    Specific API   │    Token/cert    │      Annual      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: PowerScale nodes (All-Flash/Hybrid) · InfiniBand backend · 25/100 GbE frontend           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    OneFS              = Dell PowerScale distributed filesystem OS; all nodes share a single namespace │
│    SmartPools         = tiering engine; moves files between All-Flash, Hybrid, and Archive tiers      │
│    SyncIQ             = async replication to DR cluster; RPO-based schedule; failover in minutes      │
│    SnapshotIQ         = space-efficient snapshots; accessed via .snapshot directory in each share     │
│    SmartConnect       = DNS-based load balancing; distributes NFS/SMB client connections across nodes │
│    Access zone        = logical container with separate authentication and export namespace per tenant│
│    Quota              = directory or user quota; hard/soft/advisory limits enforced by OneFS QuotaIQ  │
│    CloudPools         = tiering to cloud object storage (S3/Blob); data remains accessible locally    │
│    isi CLI            = OneFS command-line interface; all management operations available via isi c...│
│    Node pool          = group of same-model nodes sharing protection domain for data distribution     │
│    Protection level   = N+2:1, N+3:1 etc.; defines how many node or drive failures are tolerated      │
│    File pool policy   = rule-based policy assigning files to specific node pools or storage tiers     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


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
