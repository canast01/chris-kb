# Azure — Security

```
┌────────────────────────────────────────────────────────────────────┐
│                     Azure Security Layers                           │
├────────────────────────────────────────────────────────────────────┤
│  Identity        │  Entra ID  ──  MFA  ──  Conditional Access      │
├────────────────────────────────────────────────────────────────────┤
│  Access Control  │  RBAC  ──  PIM (JIT)  ──  Managed Identities    │
├────────────────────────────────────────────────────────────────────┤
│  Data Protection │  Key Vault  ──  CMK  ──  SSE  ──  TDE           │
├────────────────────────────────────────────────────────────────────┤
│  Network         │  NSG  ──  Private Link  ──  Azure Firewall       │
├────────────────────────────────────────────────────────────────────┤
│  Threat Detect.  │  Defender for Cloud  ──  Secure Score           │
├────────────────────────────────────────────────────────────────────┤
│  Governance      │  Azure Policy  ──  Blueprints  ──  Resource Locks│
└────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>Entra ID, SSO, MFA, Conditional Access, and PIM.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Azure RBAC, management group policies, and service principals.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Key Vault, customer-managed keys, data-at-rest, and Private Link.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Defender for Cloud, Secure Score, NSG hardening, and security baselines.</span>
</a>

</div>
