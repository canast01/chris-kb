# Commvault — Access Control

```
┌─────────────────────────── Commvault Access Control — RBAC and Permissions ───────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Built-in Roles                │  │                 Custom Roles                │   │
│   │      Master Admin: full CommCell access      │  │        Define capability set per role       │   │
│   │       Tenant Admin: manage user group        │  │        Assign to user group + entity        │   │
│   │        View: read-only console access        │  │       Entity: client, library, policy       │   │
│   │         Operator: run backup/restore         │  │        Scope: CommCell-wide or subset       │   │
│   │         Report Viewer: reports only          │  │        Audit: all role changes logged       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Least privilege: operators get backup/restore rights only on their assigned clients                │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                   User and Group Management                                   │   │
│   │                Users: local CommCell accounts or AD domain accounts (LDAP sync)               │   │
│   │             Groups: CommCell user groups mirror AD groups for bulk role assignment            │   │
│   │               Association: user-group + role + entity = effective permission set              │   │
│   │           Password policy: min 12 chars, complexity, 90-day rotation, no reuse (12)           │   │
│   │             Service accounts: named accounts for automation; no shared credentials            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  AD integration: CommServe needs LDAP/LDAPS access to domain controller (port 389/636)                │
│  Service accounts: stored in PAM vault (CyberArk/Vault); rotated automatically                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Capability     = Atomic permission unit (e.g. "Run Backup", "View Job", "Modify Client")             │
│  Association    = Binding of user/group + role + entity; determines effective access                  │
│  Entity         = CommCell object (client, client group, library, storage policy, etc.)               │
│  Master Admin   = All-powerful CommCell account; restrict to break-glass only                         │
│  Tenant Admin   = Delegated admin for a user group; cannot see other tenants                          │
│  LDAP Sync      = AD group membership synchronized to CommCell user groups periodically               │
│  PAM            = Privileged Access Management; vault for service account credentials                 │
│  Break-glass    = Emergency admin account; access triggers immediate alert                            │
│  Role Clone     = Creating custom role by copying and modifying a built-in role                       │
│  Object Security= Per-client or per-library permissions overriding role defaults                      │
│  Audit Log      = Record of all CommCell user actions: login, backup trigger, config change           │
│  LDAPS          = LDAP over TLS (port 636); required for secure AD authentication                     │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## RBAC Roles

CommVault roles are assigned through User Groups scoped to specific Client Groups, Storage Policies, or Subclients:

| Role | Capabilities |
|---|---|
| Master | Full CommCell administration |
| Tenant Admin | Manage users and jobs within assigned tenant |
| Operator | Start/stop jobs; no configuration changes |
| End User | Self-service restore of own data only |
| View Only | Read-only — view jobs and configuration |

Assign roles in Command Center: Manage → Security → User Groups.

**Never share admin accounts** — create individual named accounts for each operator; map AD groups to CommVault roles.

## Audit Trail

```powershell
# View CommVault audit log
qoperation execscript -sn GetAuditLog -si starttime=<timestamp>
```

Forward audit logs to SIEM via syslog:
- Command Center: Manage → Alerts → configure syslog destination
- Alert on: admin account creation, policy modifications, job deletion, encryption key access
