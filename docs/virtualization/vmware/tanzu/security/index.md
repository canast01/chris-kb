# Tanzu — Security

```
┌──────────────── Tanzu Security Overview ───────────────────────────────────────┐
│                                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐    │
│  │ Authentication│  │Access Control│  │  Encryption  │  │   Hardening     │    │
│  │  Pinniped    │  │  vSphere NS  │  │  etcd secrets│  │  Pod Security   │     │
│  │  OIDC/LDAP   │  │  RBAC roles  │  │  mTLS in     │  │  Net Policy     │     │
│  │  kubeconfig  │  │  Harbor proj │  │  transit     │  │  OPA/Kyverno    │     │
│  └──────────────┘  └──────────────┘  │  vSAN at rest│  │  Harbor scan    │     │
│                                       └──────────────┘  └──────────────────┘   │
└────────────────────────────────────────────────────────────────────────────────┘
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
  <span>Data encryption and certificate management.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines and compliance configuration.</span>
</a>

</div>
