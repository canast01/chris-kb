# Aria Operations — Security
```
┌───────────────────────────────────── Aria Operations — Security ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   vIDM/Active Directory integration for SSO; RBAC roles (admin/user/viewer) for object-level  │   │
│   │        Certificate management: cluster and adapter TLS certificates rotated on schedule       │   │
│   │    API token authentication: scoped bearer tokens for REST API integrations and automation    │   │
│   │      All REST API communication over TLS; encrypted passwords stored in credential vault      │   │
│   │         Audit event log captures all admin actions; syslog forwarding to SIEM over TLS        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Authentication gates access · RBAC scopes permissions · encryption and audit enforce compliance    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Access Control       │  │          Encryption         │   │
│   │         vIDM/AD auth        │  │      Admin: full access     │  │        REST over TLS        │   │
│   │        LDAP/AD groups       │  │       User: dashboards      │  │       Cert management       │   │
│   │         Local admin         │  │      Viewer: read-only      │  │     Encrypted passwords     │   │
│   │       Cert-based auth       │  │       Object-level acc      │  │       Syslog over TLS       │   │
│   │          API token          │  │         Custom roles        │  │       Data encryption       │   │
│   │          Audit log          │  │        Content share        │  │          FIPS mode          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Auth controls who logs in · access control limits scope · encryption and audit enforce compliance  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Auth       │   Access Ctrl    │     Encryption    │    Hardening     │      Audit       │   │
│   │   vIDM/AD SSO    │    Admin role    │    TLS enforced   │  Cert rotation   │ Event audit log  │   │
│   │   LDAP groups    │    User role     │   Pwd encrypted   │  API token TTL   │   Adapter log    │   │
│   │    API tokens    │   Viewer role    │     Syslog TLS    │   RBAC review    │    Alert log     │   │
│   │    Cert-based    │  Object access   │     FIPS mode     │   Min-perm API   │  Config changes  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VMs (cluster) · RAM DIMMs · Network NICs · Identity provider (AD/LDAP) · CA infrastructure       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vIDM               = VMware Identity Manager; provides SSO and group-based role assignment to Aria   │
│  Active Directory    = LDAP-compatible directory; groups mapped to Aria Ops roles for user access     │
│  RBAC               = Role-Based Access Control; admin/user/viewer roles scoped to object groups      │
│  Admin role         = Full access: manage adapters, alerts, dashboards, users, and system config      │
│  User role          = Dashboard and alert access; can create content but not manage system config     │
│  Viewer role        = Read-only access to dashboards and alerts; cannot create or modify content      │
│  Object-level access = Permissions scoped to specific resource groups or monitored object sets        │
│  API token          = Bearer token for REST API auth; scoped to user role; configurable TTL           │
│  TLS                = Transport Layer Security; all API and UI communication encrypted in transit     │
│  FIPS mode          = Federal Information Processing Standard 140-2 compliant cryptography mode       │
│  Certificate management = Rotate cluster TLS and adapter certs via admin UI or REST API               │
│  Audit event log    = Immutable record of all admin actions: login, config change, user management    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>SSO, LDAP, local accounts, and identity sources.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Roles, permissions, and least privilege access.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>TLS certificate management and data encryption.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines and compliance configuration.</span>
</a>

</div>
