# Aria Operations — Security

```
Aria Operations — Security Architecture
┌─────────────────────────────────────────────────────┐
│  Identity and Authentication                        │
│                                                     │
│  Active Directory / LDAPS (port 636)                │
│      │                                              │
│      ▼                                              │
│  Administration → Authentication Sources            │
│  → AD groups imported → roles assigned              │
│                                                     │
│  VIDM (Workspace ONE Access) for SAML SSO           │
│  Local admin account → break-glass only             │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  RBAC Roles                                         │
│  Administrator  → full system access                │
│  Content Admin  → dashboards, alerts, policies      │
│  Operator       → acknowledge alerts, run actions   │
│  Read Only      → view only, no actions             │
│                                                     │
│  Object Permissions → scope users to specific DC    │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  TLS / Encryption                                   │
│  Self-signed → replace with CA-signed cert          │
│  vracli certificate import --cert --key --ca        │
│  Cluster node-to-node: auto-managed TLS             │
│  Data at rest: storage-layer encryption (vSAN/SAN)  │
└─────────────────────────────────────────────────────┘
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
