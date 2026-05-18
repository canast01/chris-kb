# Horizon (VDI) — Security

```
  Horizon Security Layers
┌──────────────────────────────────────────────────────────┐
│  Perimeter          Broker           Desktop             │
│  ┌──────────┐       ┌──────────┐     ┌──────────────┐    │
│  │ UAG      │       │Connection│     │ GPO policies │    │
│  │ TLS term │──────►│ Server   │────►│ Clipboard /  │    │
│  │ DoS mitg │       │ RBAC     │     │ USB / Drive  │    │
│  │ Src IP   │       │ 2FA/SAML │     │ controls     │    │
│  │ rules    │       │ Smart    │     └──────────────┘    │
│  └──────────┘       │ card     │                         │
│                     └──────────┘     ┌──────────────┐    │
│  Identity                            │ vSAN / VM    │    │
│  ┌──────────┐                        │ Encryption   │    │
│  │ Workspace│                        │ (at rest)    │    │
│  │ ONE vIDM │                        └──────────────┘    │
│  │ (SSO/MFA)│                                            │
│  └──────────┘                                            │
└──────────────────────────────────────────────────────────┘
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
