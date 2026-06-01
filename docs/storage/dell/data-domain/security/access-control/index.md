# Data Domain — Access Control


<div class="kb-summary">
Access Control reference covering RBAC — Role-Based Access Control, Audit Logging, Network Access Control, Security Incident Response.
</div>

## RBAC — Role-Based Access Control

Data Domain has a built-in role model. Assign the minimum required role per user or group.

| Role | Access Level | Use Case |
|---|---|---|
| `sysadmin` | Full system administration | Break-glass account only; never used for day-to-day |
| `admin` | Full configuration access except security settings | Primary operational admin role |
| `backup-operator` | Read access + DD Boost storage unit access | Service account for backup software (Veeam, NBU, CommVault) |
| `user` | Read-only | Monitoring and reporting access |
| `security-officer` | Manages retention lock and compliance settings | Required for compliance mode operations |
| `auditor` | Read-only access to audit logs | Compliance review; SOC/audit team |

```bash
# Create a user and assign a role
user add <username> role backup-operator

# Assign LDAP group to a role
authentication roles assign role backup-operator group <ldap-group-name>

# List current users and roles
user show
```
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
```

Log entries include: user logins, configuration changes, retention lock events, filesystem operations, and administrative commands. The audit log should be forwarded to a SIEM that retains logs for at least 12 months.

## Network Access Control

- Isolate DD management traffic on a dedicated management VLAN
- Restrict SSH and HTTPS access to the DD to admin jump hosts or bastion servers only
- NFS and CIFS export access should be restricted to the backup server IP addresses — not open to all hosts
- DD Boost traffic should use a dedicated backup network, not the production LAN
- Do not expose the DD management interface to the internet under any circumstances

## Security Incident Response

| Event | Action |
|---|---|
| Suspected unauthorised login | `log view audit` — review login events; disable the account immediately; change all shared credentials |
| Ransomware attempt on backup data | Check retention lock status on affected MTree — compliance-mode locked files cannot be encrypted by ransomware; isolate network access; open Dell support case |
| DD Boost credential compromise | Immediately change the DD Boost user password; update backup software; review `ddboost show clients` for unexpected clients |
| Disk failure (potential data exposure) | Dell replaces failed disks; D@RE ensures data on failed disks is unreadable without the encryption key |
