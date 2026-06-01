# Aria Suite Lifecycle — Security

<div class="kb-summary">
Aria Suite Lifecycle — Security reference.
</div>

```powershell
┌───────────────────────────────────────── Aria LCM — Security ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   vIDM/Workspace ONE for SSO; environment-level RBAC (admin/operator/viewer) for LCM access   │   │
│   │   Password Locker encrypts credentials at rest; Certificate Locker manages product TLS certs  │   │
│   │   All API over HTTPS; audit log for all LCM operations including Locker access and upgrades   │   │
│   │     Break-glass local admin account; session timeout enforcement; API key with TTL policy     │   │
│   │  Least privilege: operator role limited to day-2 tasks; viewer role read-only for dashboards  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Authentication gates LCM access · RBAC scopes environment permissions                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Access Control       │  │          Encryption         │   │
│   │         vIDM/WS1 SSO        │  │        LCM admin role       │  │           LCM TLS           │   │
│   │         LDAP/AD auth        │  │        Operator role        │  │     Locker encr at rest     │   │
│   │         Local admin         │  │         Viewer role         │  │           vIDM TLS          │   │
│   │         LCM API key         │  │        Env-level acc        │  │       Cert management       │   │
│   │         Break-glass         │  │      Locker read/write      │  │        HTTPS only API       │   │
│   │       Session timeout       │  │       Request approve       │  │        Log encryption       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Auth gates LCM access · RBAC scopes per-environment permissions                                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Auth       │   Access Ctrl    │     Encryption    │    Hardening     │      Audit       │   │
│   │     vIDM/WS1     │    Admin role    │    TLS enforced   │  Cert rotation   │  LCM event log   │   │
│   │     LDAP/AD      │  Operator role   │    Locker encr    │   API key TTL    │   Request log    │   │
│   │     API keys     │   Viewer role    │      vIDM TLS     │ Session timeout  │   Cert changes   │   │
│   │   Break-glass    │    Env access    │     HTTPS only    │ Min permissions  │    Role audit    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VM (LCM appliance) · RAM DIMMs · Network NICs · Identity provider (vIDM/AD) · CA infrastructure  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vIDM              = VMware Identity Manager embedded in LCM; provides SSO across all managed Aria    │
│  Workspace ONE     = VMware identity platform; alternative to embedded vIDM for enterprise SSO        │
│  LCM RBAC          = Role-based access control in LCM; scoped per Environment; admin/operator/viewer  │
│  Admin role        = Full LCM access; can install/upgrade products, manage Lockers, and configure     │
│  Operator role     = Day-2 access in LCM; can run cert/password rotation and monitoring; no install   │
│  Viewer role       = Read-only LCM access; can view Environment health and Locker inventory; no write │
│  Password Locker encryption = AES encryption of all credentials stored in LCM Password Locker at rest │
│  Certificate Locker = LCM store for TLS certificates; supports rotation workflows and CA-signed cert  │
│  API key           = Bearer token for LCM REST API access; subject to TTL and minimum privilege policy│
│  HTTPS enforcement = All LCM API and UI traffic requires TLS; HTTP redirected or blocked by policy    │
│  Session timeout   = LCM UI session automatically expires after idle period; configurable per         │
│  Audit event log   = LCM audit trail recording all user actions: logins, upgrades, Locker access,     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>Workspace ONE Access SSO, identity sources, and local accounts.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>LCM roles, RBAC, and AD group assignment.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Locker certificate management, TLS, and password vault.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines and compliance configuration.</span>
</a>

</div>
