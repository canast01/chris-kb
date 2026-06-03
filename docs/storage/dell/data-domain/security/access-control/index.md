```bash
# Create a user and assign a role
user add <username> role backup-operator

# Assign LDAP group to a role
authentication roles assign role backup-operator group <ldap-group-name>

# List current users and roles
user show
```

```text
┌─────────────────────────────────── Dell Data Domain Access Control ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     DD access layers: NFS client IP restriction, CIFS ACLs, DD Boost user roles, CLI RBAC     │   │
│   │             MTree access: NFS exports scoped by client IP; CIFS shares by AD group            │   │
│   │         Admin access: local admin, LDAP/AD group mapping, role-based CLI access levels        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Data Access         │  │         Admin Access        │  │       DD Boost Access       │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │      NFS: IP allowlist      │  │       Local admin user      │  │      DD Boost username      │   │
│   │        CIFS: AD group       │  │        LDAP/AD groups       │  │      Storage unit bind      │   │
│   │        MTree per app        │  │      Roles: admin/user      │  │     No direct FS access     │   │
│   │       Deny by default       │  │         SSH key auth        │  │       Backup app creds      │   │
│   │      IP range restrict      │  │          Audit log          │  │      Encrypted channel      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   │     Control      │      Method      │       Scope       │     Default      │      Review      │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │    NFS export    │  Client IP list  │     Per MTree     │     Deny all     │    Quarterly     │   │
│   │    CIFS share    │     AD group     │     Per MTree     │     Deny all     │    Quarterly     │   │
│   │    Admin CLI     │    LDAP role     │    System-wide    │    Local only    │    Quarterly     │   │
│   │  DD Boost user   │  Named account   │       Per SU      │     Per app      │    Quarterly     │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    MTree isolation = Each backup app has its own MTree; prevents cross-application data access        │
│    NFS IP restrict = Export allows only backup media server IPs; block all other hosts                │
│    DD Boost user   = Service account used by backup app to authenticate DD Boost connection           │
│    Storage unit    = DD Boost logical unit mapping to an MTree path; app credential scoped            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
