# Access Standards

```
┌────────────────────────────────────── vSphere — Access Standard ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Access standard governing authentication, authorisation, and audit for the vSphere platform  │   │
│   │  All management access via vCenter SSO backed by Active Directory; direct host access blocked │   │
│   │ Three-tier RBAC: Administrator / Operator (custom role) / Read-only; no built-in admin sharing│   │
│   │     Service accounts: one per integration, least-privilege, vault-stored, rotated 90 days     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Authentication gate → authorisation scope → audit trail for all management actions                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Authorisation        │  │            Audit            │   │
│   │       vCenter SSO + AD      │  │      Administrator role     │  │        vCenter events       │   │
│   │       MFA enforcement       │  │      Operator (custom)      │  │       iDRAC audit log       │   │
│   │        Lockdown mode        │  │        Read-only role       │  │        Syslog to SIEM       │   │
│   │       Service accounts      │  │      Scope: DC/cluster      │  │        Login attempts       │   │
│   │       Break-glass acct      │  │       Least privilege       │  │         Role changes        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    All three pillars required: no auth without logging, no access without defined role                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Access tier    │   Auth method    │    vCenter role   │      Scope       │   Review freq    │   │
│   │  Administrator   │  SSO + AD + MFA  │   Administrator   │    Datacenter    │    Quarterly     │   │
│   │     Operator     │  SSO + AD + MFA  │  Custom ops role  │     Cluster      │    Quarterly     │   │
│   │    Read-only     │     SSO + AD     │     Read-only     │    Datacenter    │      Annual      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: ESXi hosts in lockdown mode; iDRAC on OOB VLAN; vCenter on management cluster            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    vCenter SSO   = Single Sign-On; authentication broker for vCenter and connected services           │
│    Lockdown mode = ESXi blocks direct SSH/shell; all access via vCenter API path only                 │
│    RBAC          = Role-Based Access Control; vCenter permissions assigned via role+scope             │
│    Administrator = Full vCenter access; restricted to named infra team members only                   │
│    Operator role = Custom role with write permissions scoped to specific operations                   │
│    Read-only     = No changes; appropriate for monitoring and helpdesk triage access                  │
│    Service acct  = Non-human account for tool integration; one per tool, least-privilege              │
│    Break-glass   = Emergency admin stored in vault; retrieved on MFA failure or lockout               │
│    Least priv.   = Grant only the minimum permissions required for the role to function               │
│    Propagate     = vCenter permission flag that applies a role to all child objects too               │
│    Scope         = vCenter object level where permission is assigned: DC, cluster, folder             │
│    SIEM          = Security Information and Event Management; receives vSphere syslog events          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
- Use AD groups instead of direct user permissions
- Assign least privilege access
- Review admin access regularly
- Remove stale accounts
- Use service accounts for integrations
- Document service account purpose
- Monitor failed logins
- Protect break-glass accounts
