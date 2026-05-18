# Site Recovery Manager — Security

```
  SRM Security Layers
┌──────────────────────────────────────────────────────────────┐
│  Identity          Access Control      Encryption            │
│  ┌──────────────┐  ┌──────────────┐    ┌──────────────┐      │
│  │ vCenter SSO  │  │ SRM roles:   │    │ TLS 1.2+ all │      │
│  │ (no local    │  │  Admin       │    │  site-to-site│      │
│  │  user store) │  │  RecovAdmin  │    │  traffic     │      │
│  │ AD groups    │  │  User        │    │              │      │
│  │ → vCenter    │  │              │    │ VR data opt. │      │
│  │   perms      │  │ SRA creds:   │    │  AES-256     │      │
│  └──────────────┘  │  encrypted   │    │  (per VM)    │      │
│                    │  in SRM      │    └──────────────┘      │
│                    └──────────────┘                          │
└──────────────────────────────────────────────────────────────┘
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
