# vCenter — Security

<div class="kb-summary">
Security reference for VMware vCenter Server. Covers SSO authentication, identity sources, role-based access control, certificate management, and hardening aligned to VMware security guidance and DISA STIGs.
</div>

```
┌───────────────────────────────────────── vCenter — Security ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     SSO domain with AD/LDAP identity provider; enterprise users map to vCenter RBAC roles     │   │
│   │  RBAC: built-in roles (Admin, Read-only, No-access) and custom roles with granular privileges │   │
│   │  Certificate management: VMCA issues machine certs; custom CA for enterprise PKI integration  │   │
│   │  Audit event export to SIEM via syslog; vCenter events capture all inventory and auth actions │   │
│   │    2FA via SSO plugin (RSA SecurID or RADIUS); API over TLS; VCSA disk encryption optional    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Authentication gates vCenter access · RBAC scopes permissions                                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Access Control       │  │          Encryption         │   │
│   │      SSO domain config      │  │        RBAC: built-in       │  │         API over TLS        │   │
│   │       AD/LDAP provider      │  │         Custom roles        │  │        VMCA cert mgmt       │   │
│   │         2FA via SSO         │  │      Object-level perm      │  │        Custom CA intg       │   │
│   │      Admin acct policy      │  │       Tag-based access      │  │        Cert lifecycle       │   │
│   │       Service accounts      │  │       Least privilege       │  │       Audit syslog TLS      │   │
│   │        IdP federation       │  │         Audit export        │  │        VCSA disk encr       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Auth gates vCenter login · RBAC scopes object access · TLS and certs protect management traffic    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Auth       │   Access Ctrl    │     Encryption    │    Hardening     │      Audit       │   │
│   │    SSO domain    │    RBAC roles    │      TLS API      │  Cert rotation   │  vCenter events  │   │
│   │   AD/LDAP IdP    │   Custom roles   │    VMCA/custom    │   2FA enforce    │  Syslog export   │   │
│   │   2FA via SSO    │   Object perms   │     TLS syslog    │   Min password   │ Audit log review │   │
│   │  Service accts   │ Least privilege  │  Cert auto-renew  │    STIG align    │   Role review    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 server (VCSA VM) · RAM DIMMs · Network NICs · Shared datastore · Trusted CA infrastructure       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SSO domain    = vSphere identity hub; authenticates all UI and API logins to vCenter                 │
│  VMCA          = VMware Certificate Authority; built-in CA; issues certs to VCSA and ESXi hosts       │
│  Custom CA     = Enterprise PKI CA replacing VMCA; certs signed by corporate root for compliance      │
│  RBAC          = Role-Based Access Control; grants privileges on inventory objects; inherited down    │
│  Object-level permission = Permission set at specific VM, cluster, or folder; overrides parent        │
│  2FA           = Two-Factor Authentication via SSO plugin: RSA SecurID or RADIUS integration          │
│  vCenter audit = All inventory and auth events logged in vCenter; export via syslog to SIEM           │
│  Service account = Non-interactive account for automation; scope to minimum required privileges       │
│  Identity source = AD, LDAP, or OpenLDAP added to SSO; maps enterprise users to vCenter roles         │
│  Certificate lifecycle = Monitor cert expiry in VAMI; renew before 60-day warning threshold           │
│  Least privilege = RBAC principle: grant only the permissions needed for a specific role or task      │
│  Tag-based access = vCenter tags used to scope RBAC; assign roles on tag categories for flexibility   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>Local accounts, directory integration, MFA, and certificate-based auth.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>RBAC, roles, permissions, and service accounts.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Data-at-rest, data-in-transit, and key management.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines, hardening guides, and compliance controls.</span>
</a>

</div>
