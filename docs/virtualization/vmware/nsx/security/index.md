# NSX — Security

<div class="kb-summary">
Security reference for VMware NSX. Covers NSX Manager authentication, role-based access control, data-in-transit encryption, certificate management, and DFW hardening baselines.
</div>

```
┌─────────────────────────────────────────── NSX — Security ────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ NSX security: distributed firewall, microsegmentation, IDPS, URL filtering, and TLS inspection│   │
│   │  Authentication: AD/LDAP integration; NSX admin roles; API token auth; vIDM/Workspace ONE SSO │   │
│   │      Access control: RBAC roles (Enterprise Admin, Security Admin, Auditor); object-level     │   │
│   │  DFW microsegmentation: stateful L4 rules enforced at vNIC; east-west traffic control per VM  │   │
│   │     Advanced security: IDPS signatures, Gateway FW, URL filtering, TLS inspection on Edge     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Authentication controls who manages NSX · RBAC limits scope                                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Access Control       │  │          Encryption         │   │
│   │        AD/LDAP: roles       │  │       Enterprise Admin      │  │        IDPS: L7 sigs        │   │
│   │      vIDM SSO: optional     │  │        Security Admin       │  │       Gateway FW: edge      │   │
│   │      API token: bearer      │  │      Auditor: read-only     │  │        URL filtering        │   │
│   │     Cert-based API auth     │  │      Object-level perms     │  │        TLS inspection       │   │
│   │    Audit log: all events    │  │     Least privilege std     │  │      DFW microseg rules     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Auth gates NSX access · RBAC scopes permissions · DFW and IDPS enforce east-west security policy   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Auth       │   Access Ctrl    │    DFW/Security   │    Hardening     │      Audit       │   │
│   │  AD/LDAP roles   │  Enterprise Adm  │   DFW: L4 rules   │    TLS on API    │  Syslog export   │   │
│   │     vIDM SSO     │  Security Admin  │   IDPS: L7 sigs   │  Cert rotation   │ Event audit log  │   │
│   │    API tokens    │   Auditor role   │   URL filtering   │ Default deny DFW │   Role reviews   │   │
│   │ Cert-based auth  │   Object-level   │   TLS inspection  │   Min-perm API   │   SIEM forward   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 ESXi hosts · Edge VM nodes · ToR switches · Physical NICs · Out-of-band network management       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  DFW           = Distributed Firewall; stateful L4 rules enforced at VM vNIC on every ESXi host       │
│  IDPS          = Intrusion Detection and Prevention System; L7 signature-based; runs on Edge nodes    │
│  Gateway FW    = Stateful firewall on T0/T1 Edge; enforces north-south and inter-segment policy       │
│  TLS inspection = NSX Edge decrypts and inspects HTTPS traffic; re-encrypts after inspection          │
│  URL filtering  = Edge service blocking or categorizing HTTP/HTTPS URLs via category lookup           │
│  Enterprise Admin = Full NSX RBAC role; manage all objects and system config                          │
│  Security Admin  = NSX role for managing DFW and security policy; no system config access             │
│  Auditor        = Read-only NSX role; view all objects and logs; no write access                      │
│  vIDM           = VMware Identity Manager (Workspace ONE Access); provides SSO for NSX Manager UI     │
│  Microsegmentation = Zero-trust approach using DFW to restrict lateral VM-to-VM communication         │
│  API token      = Bearer token for REST API auth; generated per user/service; scoped to role          │
│  Default deny   = DFW policy posture where all traffic is denied unless explicitly allowed by a rule  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>SSO integration, local accounts, and API authentication.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Roles, permissions, and least privilege access.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Data-in-transit encryption and certificate management.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines, DFW policy, and compliance.</span>
</a>

</div>
